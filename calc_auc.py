#!/usr/local/bin/python

import argparse
import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_curve, precision_recall_curve, auc
import matplotlib.pyplot as plt
import glob
import os
import pandas as pd
import csv

###########################################
#####--------- CLI arguments ---------#####
###########################################

parser = argparse.ArgumentParser(description="Info to calculate ROC and Precision-Recal AUC")

parser.add_argument("--dataset_id", help="Name of dataset ID",
                    default="", type=str, dest="dataset_id")

parser.add_argument("--test_dataset_id", help="Name of dataset ID",
                    default="", type=str, dest="test_dataset_id")

parser.add_argument("--outdir", help="Name of dataset ID",
                    default="", type=str, dest="outdir")

parser.add_argument("--model", help="Path to saved model",
                    default="na", type=str, dest="model")

parser.add_argument("--first_height", help="Height of initial filter",
                    default=8, type=int, dest="first_height")

args = parser.parse_args()

###########################################
#####----------- Functions -----------#####
###########################################
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
    print(file_pattern)
    
    # Find all files matching the pattern
    files = glob.glob(file_pattern)
    print(files)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        print(filename)
        id_num = filename.split('_')[-2]
        print(id_num)
        id_list.append(id_num)

        with open(file_path, 'r') as file:
            for line in file:
                # Assuming each line contains a comma-separated pair of numbers
                numbers = line.strip().split(',')
                if len(numbers) != 2:
                    continue  # Skip lines with invalid format
                
                # Convert numbers to floats
                num1 = float(numbers[0])
                num2 = float(numbers[1])
                
                # Keep track of the smaller number
                min_num = min(num1, num2)
                scores.append(min_num)

    return scores, id_list

###########################################
#####-------------- Main -------------#####
###########################################

# # Load your trained model
# if "continue" in args.model:
#     model_path = "/hps/nobackup/goldman/charwest/omega_ai/data/saved_models/{0}/4".format(args.model) # not very elegant, should probably fix
# else:
#     model_path = "/hps/nobackup/goldman/charwest/omega_ai/data/saved_models/{0}/50".format(args.model)
# model = tf.keras.models.load_model(model_path)

# x = tf.ones((512, args.first_height, 2000, 5))
# model.evaluate(x)
# model.summary()

# Main loop setup
dataset_id = args.dataset_id
if "true" in dataset_id:
    aligner_list = ["true"]
    print("true dataset run")
else:
    aligner_list = ["clustal", "mafft", "prankaa", "prankc"]
    # aligner_list = ["clustal"]
# aligner_list = ["clustal", "mafft", "prankaa", "prankc", "true"]
# aligner_list = ["clustal", "mafft", "prankaa", "prankc"]


if args.test_dataset_id == "":
    test_dataset_id = dataset_id
else:
    test_dataset_id = args.test_dataset_id

if args.outdir == "":
    outdir = dataset_id
else:
    outdir = args.outdir

for i, aligner in enumerate(aligner_list):
#     if "prankc" in dataset_id:
#         dataset_str = dataset_id[len("prankc_"):]
#     else:
#         dataset_str = dataset_id
#     test_files = glob.glob("/hps/nobackup/goldman/charwest/omega_ai/data/test_tf_records/{0}/{0}.{1}.alignments.tfrecord".format(test_dataset_id, aligner))
#     test_dataset = tf.data.TFRecordDataset(test_files).map(_parse_alignment).padded_batch(
#             batch_size=256,
#             padded_shapes=([None,None,None],[]))

#     y_true = []
#     y_pred = []

#     # Get true labels and predictions
#     for batch in test_dataset:
#         x_test, y_test = batch
#         predictions = model.predict(x_test)
#         y_true.extend(y_test.numpy())
#         y_pred.extend(predictions.flatten())


#     ## OmegaAI
#     # Compute ROC curve
#     print(f"This is y_true: {y_true}")
#     fpr, tpr, thresholds = roc_curve(y_true, y_pred)
#     roc_auc = auc(fpr, tpr)
#     roc_df = pd.DataFrame({'fpr': fpr, 'tpr': tpr, 'threshold': thresholds})
#     print(roc_df)
#     if not os.path.exists("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/model_test_results/{0}/{1}".format(outdir, aligner)):
#         os.makedirs("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/model_test_results/{0}/{1}".format(outdir, aligner))
#     print("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/model_test_results/{0}/{1}/roc_res.csv".format(outdir, aligner))
#     roc_df.to_csv("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/model_test_results/{0}/{1}/roc_res.csv".format(outdir, aligner), index=False)
#     # Write ROC AUC to its own file
#     with open("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/model_test_results/{0}/{1}/roc_auc.txt".format(outdir, aligner), 'w') as f:
#         f.write(str(roc_auc))

#     # Compute Precision-Recall curve
#     precision, recall, thresholds = precision_recall_curve(y_true, y_pred)
#     pr_auc = auc(recall, precision)
#     thresholds = np.append(thresholds, 1.0)
#     pr_df = pd.DataFrame({'precision': precision, 'recall': recall, 'threshold': thresholds})
#     print(pr_df)
#     pr_df.to_csv("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/model_test_results/{0}/{1}/pr_res.csv".format(outdir, aligner), index=False)
#     # Write PR AUC to its own file
#     with open("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/model_test_results/{0}/{1}/pr_auc.txt".format(outdir, aligner), 'w') as f:
#         f.write(str(pr_auc))

    if "prankc" not in dataset_id:
        ## PAML
        paml_pred, id_list = get_paml_scores("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/{1}/{0}/".format(aligner, dataset_id))
        print("this is paml_pred: {}".format(paml_pred))
        print("this is paml id_list: {}". format(id_list))
        paml_true = extract_true_label(id_list, "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/{0}/".format(dataset_id))
        print("this is paml_true: {}".format(paml_true))

        # Compute ROC curve
        paml_fpr, paml_tpr, paml_thresholds = roc_curve(paml_true, paml_pred)
        paml_roc_auc = auc(paml_fpr, paml_tpr)
        paml_roc_df = pd.DataFrame({'fpr': paml_fpr, 'tpr': paml_tpr, 'threshold': paml_thresholds})
        paml_roc_df.to_csv("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/{0}/{1}_roc_res.csv".format(dataset_id, aligner), index=False)
        # Write ROC AUC to its own file
        with open("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/{0}/{1}_roc_auc.txt".format(dataset_id, aligner), 'w') as f:
            f.write(str(paml_roc_auc))

        # Compute Precision-Recall curve
        paml_precision, paml_recall, paml_thresholds = precision_recall_curve(paml_true, paml_pred)
        paml_pr_auc = auc(paml_recall, paml_precision)
        paml_thresholds = np.append(paml_thresholds, 1.0)
        paml_pr_df = pd.DataFrame({'precision': paml_precision, 'recall': paml_recall, 'threshold': paml_thresholds})
        paml_pr_df.to_csv("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/{0}/{1}_pr_res.csv".format(dataset_id, aligner), index=False)
        # Write PR AUC to its own file
        with open("/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/{0}/{1}_pr_auc.txt".format(dataset_id, aligner), 'w') as f:
            f.write(str(paml_pr_auc))

    # # Save y_true, y_pred and paml_pred
    # y_true_file = "/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/auc_threshold_data/divbase_indistNB_indrate01_tips8_posprop05/cnn_y_true.csv"
    # with open(y_true_file, 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     csv_writer.writerow(paml_true)

    # y_pred_file = "/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/auc_threshold_data/divbase_indistNB_indrate01_tips8_posprop05/cnn_y_pred.csv"
    # with open(y_pred_file, 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     csv_writer.writerow(y_pred)

    # paml_pred_file = "/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/auc_threshold_data/divbase_indistNB_indrate01_tips8_posprop05/cnn_paml_pred.csv"
    # with open(paml_pred_file, 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     csv_writer.writerow(paml_pred)

    # y_true_file = "/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/auc_threshold_data/divbase_indistNB_indrate01_tips8_posprop05/cnn_real_y_true.csv"
    # with open(y_true_file, 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     csv_writer.writerow(y_true)
