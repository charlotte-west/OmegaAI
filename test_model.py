import argparse
import os
from glob import glob
from pathlib import Path
from unittest import result
import pandas as pd

import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from sklearn.metrics import confusion_matrix  # , roc_curve

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # suppress tensorflow library output

# ===================================== CLI arguments
parser = argparse.ArgumentParser(description="CNN hyperparameters")

parser.add_argument("-bs", help="Batch size (train, test, and validation)",
                    default=512, type=int, dest="batch_size")
parser.add_argument("-p", help="Dropout probability",
                    default=0.5, type=float, dest="dropout_p")
parser.add_argument("-lr", help="Learning rate for Adam optimizer",
                    default=1e-3, type=float, dest="learning_rate")
parser.add_argument("-l", help="L2 penalty (weight decay)",
                    default=0, type=float, dest="weight_decay")
parser.add_argument("-n", help="Number of epochs for training",
                    default=50, type=int, dest="n_epochs")

parser.add_argument("--dataset", help="ID of the dataset to test",
                    default="baseline_0.2", type=str, dest="dataset_id")

### NEW
parser.add_argument("--outdir", help="Name of results directory",
                    default="", type=str, dest="outdir")

parser.add_argument("-w", help="""Maximum number of processes to spin up
                                  when using process-based threading""",
                    default=1, type=int, dest="n_workers")
parser.add_argument("-q", help="Maximum size for the generator queue",
                    default=1, type=int, dest="queue_size")

parser.add_argument("--model", help="Path to saved model",
                    default="na", type=str, dest="saved_model")

parser.add_argument("--aligner", help="Test aligner",
                    default="clustal", type=str, dest="aligner")

parser.add_argument("--alt_arch", help="Test all alt architectures or not",
                    default="single", type=str, dest="alt_arch")

parser.add_argument("--first_height", help="Height of initial filter",
                    default=8, type=int, dest="first_height")

parser.add_argument("--divergences", help="Test across divergence sets",
                    default="no", type=str, dest="divergences")

parser.add_argument("--PAML", help="Use PAML test sets",
                    default=1, type=int, dest="paml")

parser.add_argument("--true_align", help="testing the true alignment",
                    default=False, type=bool, dest="true_align")

args = parser.parse_args()


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


def parse_alignment(file_name):
    """
    Generate one-hot encoded alignment.
    """
    # discard alignment if entirely deleted
    try:
        if os.stat(file_name).st_size == 0:
            print("entire alignment deleted")
            return None
    except FileNotFoundError:
        return None
    encoding = {"-": [1, 0, 0, 0, 0],
                "A": [0, 1, 0, 0, 0],
                "C": [0, 0, 1, 0, 0],
                "G": [0, 0, 0, 1, 0],
                "T": [0, 0, 0, 0, 1]}
    x_seqs = []
    lines_read = 0
    with open(str(file_name), "r") as file:
        sequence = []
        for line in file:
            if line[0] == ">" and lines_read != 0:
                # discard alignment if entirely deleted
                if len(sequence) < 100:
                    print("returning none")
                    return None
                x_seqs.append(np.asarray(sequence, dtype=np.float32))
                sequence = []
            elif line[0].isalpha() or line[0] == "-":
                for char in line.rstrip("\n"):
                    sequence.append(encoding[char])
            lines_read += 1
        x_seqs.append(np.asarray(sequence, dtype=np.float32))
    x_seqs = tf.convert_to_tensor(x_seqs)
    return x_seqs


def get_label(label_file):
    """
    Returns y label.
    """
    with open(label_file, "r") as y_fi:
        if y_fi.read(1) == "1":
            return 1
        else:
            return 0


def pad_up_to(t, max_in_dims, constant_values):
    """
    Determines padding for the test batch.
    """
    s = tf.shape(t)
    paddings = [[0, m-s[i]] for (i,m) in enumerate(max_in_dims)]
    return tf.pad(t, paddings, 'CONSTANT', constant_values=constant_values)


def _int64_feature(value):
    """
    Define a long integer.
    """
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _bytes_feature(value):
    """
    Defines a list of byte strings.
    """
    if isinstance(value, type(tf.constant(0))):  # if value is tensor
        value = value.numpy()  # get value of tensor
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def serialize_example(alignment, y_label):
    """
    Creates a tf.train.Example message ready to be written to a file.
    """
    feature = {
        "alignment": _bytes_feature(tf.io.serialize_tensor(alignment)),
        "y_label": _int64_feature([y_label]),
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()


def generate_test_tfrecords(test_dir):
    """
    Generate TFRecords of the alignments used for testing.
    """
    # get all y labels
    y_labs = glob(test_dir + "/test_y/*txt")

    if args.true_align:
        aligner_list = ["true"]
    else:
        aligner_list = ["clustal", "mafft", "prankaa", "prankc"]

    # convert alignments from each aligner to tfrecords
    for aligner in aligner_list:
        # store parsed alignments and y labels
        tf_alignments, tf_labels = [], []

        # define alignment file list
        aligner_fis = [i.replace("test_y", aligner+"_test_x").replace("txt", "fas") for i in y_labs]

        # make output directory
        out_dir = test_dir + "/tfrecords/{}/".format(aligner)
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        # parse and store alignments/y labels
        for y_fi, align_fi in zip(y_labs, aligner_fis):
            parsed_alignment = parse_alignment(align_fi)
            if parsed_alignment is None:
                continue
            parsed_label = get_label(y_fi)
            tf_alignments.append(parsed_alignment)
            tf_labels.append(parsed_label)

        # write tfrecords
        with tf.io.TFRecordWriter(out_dir + "{}.tfrecord".format(aligner)) as writer:
            for i in range(len(tf_alignments)):
                example = serialize_example(tf_alignments[i], tf_labels[i])
                writer.write(example)


def test_alt_archs():
    """
    Test specific architectures (a saved, trained model).
    """
    print("testing...")
    arch_dic = {}
    # dataset_id, model_path, best_val_acc_epoch, test_set_path
    with open("alt_archs.csv", "r") as f:
        next(f)
        for line in f:
            line = line.strip().split(",")
            if args.paml == 1:
                arch_dic[line[0]] = (line[1], line[2], line[3])
            else:
                arch_dic[line[0]] = (line[1], line[2], line[4])

    if args.paml == 1:
        # check if TFRecords exist, otherwise, create them
        for model_id in list(arch_dic.keys()):
            tfrecord_path = line[3] + "/tfrecords/true/true.tfrecord"
            if not os.path.exists(tfrecord_path):
                generate_test_tfrecords(line[3])

    # write headers
    with open("alt_architecture_performance_bs{}.tsv".format(args.batch_size), "w") as f:
        f.write("\t".join(["arch","acc","tpr","fpr","tp","fp","tn","fn","aligner","epoch"]) + "\n")

    # determine which alignments to test
    if args.true_align:
        aligner_list = ["true"]
    elif args.paml == 1:
        aligner_list = ["clustal", "mafft", "prankaa", "prankc"]
    else:
        aligner_list = ["clustal", "mafft", "prankaa", "prankc"]

    # loop through models and test performance
    for model_id in list(arch_dic.keys()):
        print("Evaluating {}...".format(model_id))
        saved_model = arch_dic[model_id][0]
        best_val_acc = arch_dic[model_id][1]
        test_dir = arch_dic[model_id][2]

        # only evaluate final epoch and the epoch with the best validation accuracy
        for epoch in [best_val_acc, "50"]:
            # load model
            model = models.load_model("saved_models/" + saved_model + "/" + epoch)
            x = tf.ones((512, 8, 2000, 5))
            model.evaluate(x)
            # define test alignment paths
            for aligner in aligner_list:
                if args.paml == 1:
                    test_files = test_dir + "/tfrecords/{0}/{0}.tfrecord".format(aligner)
                else:
                    test_files = glob(test_dir + "/{}/*tfrecord".format(aligner))

                test_dataset = tf.data.TFRecordDataset(test_files).map(_parse_alignment).padded_batch(
                    batch_size=args.batch_size,
                    padded_shapes=([None,None,None],[]))

                # get true label
                y_true = np.asarray([int(i) for i in list(tf.data.TFRecordDataset(test_files).map(_extract_y_labels))])
                # get predicted label
                y_pred = np.asarray([int(round(float(i))) for i in model.predict(test_dataset)])
                
                # generate confusion matrix
                conf_mat = confusion_matrix(y_true, y_pred)
                tn, fp, fn, tp = conf_mat.ravel()

                # calculate rates
                tpr = tp / (tp+fn)
                fpr = fp / (fp+tn)
                acc = (tp+tn) / (tp+fp+tn+fn)

                # output model performance
                with open("alt_architecture_performance_bs{}.tsv".format(args.batch_size), "a+") as f:
                    f.write("\t".join([str(i) for i in [model_id,acc,tpr,fpr,tp,fp,tn,fn,aligner,epoch]]) + "\n")


def test_divergences():
    """
    Test models trained on alignments simulated using various divergences.
    """
    paml_dir = "/omega_ai/paml_selection/determining_branch_lengths/output/"

    # get all divergences tested
    div_dic = {}
    with open("divergences.txt", "r") as f:
        next(f)
        for line in f:
            line = line.strip().split(",")
            div_dic[line[0]] = (line[1], line[2])

    # generate alignments in TFRecord format if they don't already exist
    for diverg in list(div_dic.keys()):
        tfrecord_path = paml_dir + diverg + "/tfrecords/true/true.tfrecord"
        if not os.path.exists(tfrecord_path):
            generate_test_tfrecords(paml_dir + diverg)

    # write headers
    with open("divergence_performance.tsv", "w") as f:
        f.write("\t".join(["divergence","acc","tpr","fpr","tp","fp","tn","fn","aligner","epoch"]) + "\n")

    # loop through models trained at various divergences and test performance
    for diverg in list(div_dic.keys()):
        print("Evaluating {}...".format(diverg))
        # load model
        saved_model = div_dic[diverg][0]
        model_files = glob("saved_models/" + saved_model + "/*")
        model_files.sort(key=os.path.getmtime)
        final_epoch = model_files[-1].split("/")[-1]

        # test final epoch 
        for epoch in [final_epoch]:
            model = models.load_model("saved_models/" + saved_model + "/" + epoch)
    
            x = tf.ones((512, 8, 2000, 5))
            model.evaluate(x)

            # loop through various aligner-produced test sets
            for aligner in ["clustal", "mafft", "prankaa", "prankc"]:
                test_files = glob(paml_dir + diverg + "/tfrecords/{0}/{0}.tfrecord".format(aligner))
                test_dataset = tf.data.TFRecordDataset(test_files).map(_parse_alignment).padded_batch(
                    batch_size=args.batch_size,
                    padded_shapes=([None,None,None],[]))

                # get true label
                y_true = np.asarray([int(i) for i in list(tf.data.TFRecordDataset(test_files).map(_extract_y_labels))])
                # predict label
                y_pred = np.asarray([int(round(float(i))) for i in model.predict(test_dataset)])
                
                # generate confusion matrix
                conf_mat = confusion_matrix(y_true, y_pred)

                # calculate rates and accuracy
                tn, fp, fn, tp = conf_mat.ravel()
                tpr = tp / (tp+fn)
                fpr = fp / (fp+tn)
                acc = (tp+tn) / (tp+fp+tn+fn)

                # write output
                with open("divergence_performance.tsv", "a") as f:
                    f.write("\t".join([str(i) for i in [diverg,acc,tpr,fpr,tp,fp,tn,fn,aligner,epoch]]) + "\n")


def main():
    """
    Test the performance of trained networks.
    """
    # Determines if alternate architectures beyond the "base" architecture
    # should be evaluated
    if args.alt_arch != "single":
        test_alt_archs()
        exit()

    # Determines if networks trained across many divergences should be tested
    if args.divergences != "no":
        test_divergences()
        exit()

    # Otherwise, test the base architecture at the "base" divergence (0.2 bl)

    # load trained model
    model = models.load_model("saved_models/" + args.saved_model)
    x = tf.ones((512, args.first_height, 2000, 5))
    model.evaluate(x)
    model.summary()

    # Setup directory
    if args.outdir == "":
        res_outdir = args.dataset_id
    else:
        res_outdir = args.outdir
    
    os.system("mkdir /omega_ai/data/simulations/model_test_results/{0}".format(res_outdir))

    # parse TFRecords of the test data for four aligners
    if args.true_align:
        aligner_list = ["true"]
    else:
        aligner_list = ["clustal", "mafft", "prankaa", "prankc"]

    for aligner in aligner_list:

        # Setup directory 
        os.system("mkdir /omega_ai/data/simulations/model_test_results/{0}/{1}".format(res_outdir, aligner))

        print("=" * len(aligner))
        print(aligner)
        print("=" * len(aligner))
        test_files = glob("/omega_ai/data/test_tf_records/{0}/{0}.{1}.alignments.tfrecord".format(args.dataset_id, aligner))
        test_dataset = tf.data.TFRecordDataset(test_files).map(_parse_alignment).padded_batch(
            batch_size=256,
            padded_shapes=([None,None,None],[]))

        # get true Y labels (1 for omega > 1, 0 otherwise)
        y_true = np.asarray([int(i) for i in list(tf.data.TFRecordDataset(test_files).map(_extract_y_labels))])
        # predict Y label
        y_pred = np.asarray([int(round(float(i))) for i in model.predict(test_dataset)])
        
        # calculate confusion matrix containing TP,FP,TN,FN
        conf_mat = confusion_matrix(y_true, y_pred)

        tn, fp, fn, tp = conf_mat.ravel()

        # calculate rates and accuracy
        tpr = tp / (tp+fn)
        fpr = fp / (fp+tn)
        acc = (tp+tn) / (tp+fp+tn+fn)

        # output results 
        print("True positives:", tp)
        print("False positives:", fp)
        print("True negatives:", tn)
        print("False negatives:", fn)
        print("TPR:", round(tpr, 3))
        print("FPR:", round(fpr,3))
        print("Accuracy:", round(acc,3))
        print("\n")

        results = { "accuracy" : acc, "tpr" : tpr, "fpr": fpr,  "tp" : tp, "fp" : fp, "tn" : tn, "fn" : fn, "aligner": aligner}
        res_df = pd.DataFrame(results, index=[0])
        res_df.to_csv("/omega_ai/data/simulations/model_test_results/{0}/{1}/{0}_{1}_res.csv".format(res_outdir, aligner), index=False)

if __name__ == "__main__":
    main()