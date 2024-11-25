#!/usr/local/bin/python

import argparse
import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_curve, precision_recall_curve, auc
import matplotlib.pyplot as plt
import glob
import os

# ===================================== CLI arguments
parser = argparse.ArgumentParser(description="CNN hyperparameters")

# parser.add_argument("--outdir", help="Name of results directory",
#                     default="", type=str, dest="outdir")

# parser.add_argument("--model", help="Path to saved model",
#                     default="na", type=str, dest="saved_model")

parser.add_argument("--first_height", help="Height of initial filter",
                    default=8, type=int, dest="first_height")

args = parser.parse_args()

# ===================================== Functions
def _parse_alignment(example, label=True):
    """
    Parse TF alignments.
    """
    alignment_feature_description = {
        'alignment': tf.io.FixedLenFeature([], tf.string),
        'y_label': tf.io.FixedLenFeature([], tf.int64)
    }
    example = tf.io.parse_single_example(example, alignment_feature_description)
    alignment = tf.io.parse_tensor(example["alignment"], tf.float32)
    y_label = tf.cast(example["y_label"], tf.int32)
    if label:
        return alignment, y_label
    else:
        return alignment

def _extract_y_labels(example):
    """
    Extract the y labels for each test alignment (1 for omega > 1, 0 otherwise)
    """
    alignment_feature_description = {
        'alignment': tf.io.FixedLenFeature([], tf.string),
        'y_label': tf.io.FixedLenFeature([], tf.int64)
    }
    example = tf.io.parse_single_example(example, alignment_feature_description)
    y_label = tf.cast(example["y_label"], tf.int32)
    return y_label

def extract_true_label(ids,dir_path):
    true_labels = []

    for id in ids:
        id = int(id)
        if id <= 500:
            group = "group_0"
        elif (id > 500) & (id < 1002):
            group = "group_501"
        elif (id >= 1002) & (id <= 1502):
            group = "group_1002"
        else:
            group = "group_1503"

        file_path = os.path.join(dir_path, f"{group}/test_y/{id}.txt")
        with open(file_path, 'r') as file:
            for line in file:
                true_label_val = int(line.strip())
                if true_label_val == 1:
                    true_label = 1
                else:
                    true_label = 0
                true_labels.append(true_label)

    return(true_labels)

def get_paml_scores(dir_path):
    id_list = []
    scores = []
    file_pattern = os.path.join(dir_path, '*_probs.txt')
    
    # Find all files matching the pattern
    files = glob.glob(file_pattern)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        id_num = filename.split('_')[-2]
        id_list.append(id_num)

        with open(file_path, 'r') as file:
            for line in file:
                # Assuming each line contains a comma-separated pair of numbers
                numbers = line.strip().split(',')
                if len(numbers) != 2:
                    continue  # Skip lines with invalid format
                
                # # Convert numbers to floats
                # try:
                #     num1, num2 = map(float, numbers)
                # except ValueError:
                #     continue  # Skip lines with non-numeric values
                num1 = float(numbers[0])
                num2 = float(numbers[1])
                
                # Keep track of the smaller number
                min_num = min(num1, num2)
                scores.append(min_num)
    
    return scores, id_list



# ===================================== Main

# Load your trained model
model_path = "/hps/nobackup/goldman/charwest/omega_ai/data/saved_models/2022-12-06-12-42-21_divbase_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001/50"
model = tf.keras.models.load_model(model_path)

x = tf.ones((512, args.first_height, 2000, 5))
model.evaluate(x)
model.summary()

dataset_id = "divbase_indistNB_indrate01_tips8_posprop05"
aligner_list = ["clustal", "mafft", "prankaa", "prankc"]
aligner_colors = {
    'clustal': '#0072B2',
    'mafft': '#E69F00',
    'prankaa': '#CC79A7',
    'prankc': '#009E73'
}
aligner_labels = {
    'clustal': 'Clustal',
    'mafft': 'MAFFT',
    'prankaa': 'PRANKaa',
    'prankc': 'PRANKc'
}

# ROC
plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
for i, aligner in enumerate(aligner_list):
    test_files = glob.glob("/hps/nobackup/goldman/charwest/omega_ai/data/test_tf_records/{0}/{0}.{1}.alignments.tfrecord".format(dataset_id, aligner))
    test_dataset = tf.data.TFRecordDataset(test_files).map(_parse_alignment).padded_batch(
            batch_size=256,
            padded_shapes=([None,None,None],[]))

    y_true = []
    y_pred = []

    # Get true labels and predictions
    for batch in test_dataset:
        x_test, y_test = batch
        predictions = model.predict(x_test)
        y_true.extend(y_test.numpy())
        y_pred.extend(predictions.flatten())

    # print("this is y_pred: {0}".format(y_pred))
    # print("this is y_true: {0}".format(y_true))
    # Compute ROC curve
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    # print("these are the thresholds: {0}".format(thresholds))
    print("this is roc auc for {0}: {1}".format(aligner, roc_auc))

    # Plot ROC curve
    plt.plot(fpr, tpr, lw=2, color=aligner_colors[aligner], label = f'OmegaAI {aligner_labels[aligner]} (AUC = {roc_auc:.2f})') #, label=f'Dataset {i+1} ROC (AUC = {roc_auc:.2f})')

    # PAML
    paml_pred, id_list = get_paml_scores("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/divbase_indistNB_indrate01_tips8_posprop05/{0}/".format(aligner))
    paml_true = extract_true_label(id_list, "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/divbase_indistNB_indrate01_tips8_posprop05/")
    print(paml_pred)
    print(paml_true)

    paml_fpr, paml_tpr, thresholds = roc_curve(paml_true, paml_pred)
    paml_roc_auc = auc(paml_fpr, paml_tpr)
    print("this is paml roc auc for {0}: {1}".format(aligner, paml_roc_auc))

    plt.plot(paml_fpr, paml_tpr, lw=2, color=aligner_colors[aligner], linestyle='--', label = f'PAML {aligner_labels[aligner]} (AUC = {paml_roc_auc:.2f})')

plt.plot([0, 1], [0, 1], color='gray', linestyle='dotted')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curves')
plt.legend(loc='lower right')
plt.grid(True)

# Precision-recall
plt.subplot(1, 2, 2)
for i, aligner in enumerate(aligner_list):
    test_files = glob.glob("/hps/nobackup/goldman/charwest/omega_ai/data/test_tf_records/{0}/{0}.{1}.alignments.tfrecord".format(dataset_id, aligner))
    test_dataset = tf.data.TFRecordDataset(test_files).map(_parse_alignment).padded_batch(
            batch_size=256,
            padded_shapes=([None,None,None],[]))

    y_true = []
    y_pred = []

    # Get true labels and predictions
    for batch in test_dataset:
        x_test, y_test = batch
        predictions = model.predict(x_test)
        y_true.extend(y_test.numpy())
        y_pred.extend(predictions.flatten())

    # Compute Precision-Recall curve
    precision, recall, _ = precision_recall_curve(y_true, y_pred)
    pr_auc = auc(recall, precision)
    # print("these are the thresholds: {0}".format(thresholds))
    print("this is pr auc for {0}: {1}".format(aligner, pr_auc))

    # Plot Precision-Recall curve
    plt.plot(recall, precision, lw=2, color=aligner_colors[aligner], label = f'OmegaAI {aligner_labels[aligner]} (AUC = {pr_auc:.2f})' ) #, label=f'Dataset {i+1} Precision-Recall (AUC = {pr_auc:.2f})')

    # PAML
    paml_pred, id_list = get_paml_scores("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/divbase_indistNB_indrate01_tips8_posprop05/{0}/".format(aligner))
    paml_true = extract_true_label(id_list, "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/divbase_indistNB_indrate01_tips8_posprop05/")

    paml_precision, paml_recall, _ = precision_recall_curve(paml_true, paml_pred)
    paml_pr_auc = auc(paml_recall, paml_precision)
    print("this is paml pr auc for {0}: {1}".format(aligner, paml_pr_auc))

    plt.plot(paml_recall, paml_precision, lw=2, color=aligner_colors[aligner], linestyle='--', label = f'PAML {aligner_labels[aligner]} (AUC = {paml_pr_auc:.2f})')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curves')
plt.legend(loc='lower left')
plt.grid(True)

plt.tight_layout()

plt.savefig("/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/baseline_cnn_paml_roc_pr.png")

# # Make predictions on the test data
# test_path = ""
# predictions = model.predict(test_images)

# # Compute ROC curve
# fpr, tpr, thresholds = roc_curve(test_labels, predictions)

# # Compute Precision-Recall curve
# precision, recall, _ = precision_recall_curve(test_labels, predictions)

# # Plot ROC curve
# plt.figure(figsize=(8, 6))
# plt.plot(fpr, tpr, color='blue', lw=2, label='ROC Curve')
# plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver Operating Characteristic (ROC) Curve')
# plt.legend(loc='lower right')
# plt.grid(True)
# plt.show()

# # Plot Precision-Recall curve
# plt.figure(figsize=(8, 6))
# plt.plot(recall, precision, color='green', lw=2, label='Precision-Recall Curve')
# plt.xlabel('Recall')
# plt.ylabel('Precision')
# plt.title('Precision-Recall Curve')
# plt.legend(loc='lower left')
# plt.grid(True)
# plt.show()