#!/usr/local/bin/python

# Code Authorship:
#   Original implementation: Conor R. Walker

from pathlib import Path
from sys import argv
from os import stat

import tensorflow as tf
import numpy as np
from datetime import datetime


def _int64_feature(value):
    """
    Returns a TF long integer.
    """
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _bytes_feature(value):
    """
    Returns a TF bytes list.
    """
    if isinstance(value, type(tf.constant(0))):  # if value is tensor
        value = value.numpy()  # get value of tensor
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def serialize_array(array):
    """
    Serializes an array.
    """
    array = tf.io.serialize_tensor(array)
    return array


def parse_alignment(file_name):
    """
    Parses an input nucleotide alignment and encodes it first using one-hot
    encoding, then as a TF tensor.
    """
    # discard alignment if entirely deleted
    if stat(file_name).st_size == 0:
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
                    print(line)
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
    Gets the y label of the input alignment (i.e. 0 = omega < 1 at the third 
    site class, 1 is > 1).
    """
    with open(label_file, "r") as y_fi:
        if y_fi.read(1) == "1":
            return 1
        else:
            return 0


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


def main():
    # read in a list of files to store in the same TFRecord file
    file_list = argv[2]

    # parse files
    with open(file_list, "r") as f:
        print("printing f")
        print(f)
        train_files = [i.strip() for i in f.readlines()]
    print("fi_count")
    fi_count = file_list.split("/")[-1].split(".")[0]
    print(fi_count)

    # determine validation/training splits
    val_splits = [10,20,30,40,50]
    # val_splits = [25,75,125,175,225,275,325,375,425,475] # For 5M mixed model
    if int(fi_count) in val_splits:
        set_dir = "validation"
        print("validation")
    else:
        set_dir = "training"
        print("training")

    # out directory
    base_dir = "/omega_ai/data/tf_records/"
    out_dir = base_dir + "/" + argv[1] + "/" + set_dir + "/"  # argv[1] = dataset id
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # used to write files
    total_seen = 0
    alignments, labels = [], []

    # processes training files
    for align_fi in train_files:
        print("got here")
        total_seen += 1
        # get y_label files
        label_fi = align_fi.replace("train_x", "train_y").replace("fas", "txt")
        # parse alignments into arrays, get the y_label from files
        parsed_alignment = parse_alignment(align_fi)
        # do not process entirely deleted genes, raises shape errors when
        # running the CNN - only impacts a couple of alignments
        if parsed_alignment is None:
            continue
        parsed_label = get_label(label_fi)
        # store temporary chunk of alignment/label pairs
        alignments.append(parsed_alignment)
        labels.append(parsed_label)

    # write the trainign alignments into TFRecord files that will be used
    # for network training
    with tf.io.TFRecordWriter(out_dir + "alignments_{}.tfrecord".format(fi_count)) as writer:
        for i in range(len(alignments)):
            print("got to this bit")
            example = serialize_example(alignments[i], labels[i])
            writer.write(example)

    # Timings
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Final datetime is: " + current_datetime)


if __name__ == "__main__":
    main()