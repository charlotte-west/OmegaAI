#!/usr/local/bin/python

from pathlib import Path
from glob import glob
from sys import argv
from os import stat, path

import tensorflow as tf
import numpy as np


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _bytes_feature(value):
    if isinstance(value, type(tf.constant(0))):  # if value is tensor
        value = value.numpy()  # get value of tensor
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def serialize_array(array):
    array = tf.io.serialize_tensor(array)
    return array


def parse_alignment(file_name):
    # discard alignment if entirely deleted
    if stat(file_name).st_size == 0:
        return None
    encoding = {"-": [1, 0, 0, 0, 0],
                "A": [0, 1, 0, 0, 0],
                "C": [0, 0, 1, 0, 0],
                "G": [0, 0, 0, 1, 0],
                "T": [0, 0, 0, 0, 1]}
    x_seqs = []
    # with open(str(file_name), "r") as file:
    #     sequence = []
    #     for line in file:
    #         if line[0] == ">" and line[1] != "A":
    #             x_seqs.append(np.asarray(sequence, dtype=np.float32))
    #             sequence = []
    #         elif line[0].isalpha() or line[0] == "-":
    #             for char in line.rstrip("\n"):
    #                 sequence.append(encoding[char])
    #     x_seqs.append(np.asarray(sequence, dtype=np.float32))
    # x_seqs = tf.convert_to_tensor(x_seqs)
    # return x_seqs
    with open(str(file_name), "r") as file:
        sequence = []
        first_sequence_header = None
        for line in file:
            if line[0] == ">" and first_sequence_header is None:
                first_sequence_header = line[1:].strip()  # Extract header without ">"
            elif line[0] == ">" and line[1:] != first_sequence_header:
                x_seqs.append(np.asarray(sequence, dtype=np.float32))
                sequence = []
            elif line[0].isalpha() or line[0] == "-":
                for char in line.rstrip("\n"):
                    sequence.append(encoding[char])
        x_seqs.append(np.asarray(sequence, dtype=np.float32))
    x_seqs = tf.convert_to_tensor(x_seqs)
    return x_seqs


def get_label(label_file):
    with open(label_file, "r") as y_fi:
        if y_fi.read(1) == "1":
            return 1
        else:
            return 0


def serialize_example(alignment, y_label, fasta_path):
    """
    Creates a tf.train.Example message ready to be written to a file.
    """
    feature = {
        "fasta_path": _bytes_feature(str.encode(fasta_path)),
        "alignment": _bytes_feature(tf.io.serialize_tensor(alignment)),
        "y_label": _int64_feature([y_label]),
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()


def main():
    dataset = argv[1]
    aligner = argv[2]
    # in directory and files
    test_data_dir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets"
    test_dataset_dir = path.join(test_data_dir, dataset)
    file_list = glob("{0}/*/{1}_test_x/*".format(test_dataset_dir, aligner))
    # out directory
    base_dir = "/hps/nobackup/goldman/charwest/omega_ai/data/test_tf_records/"
    out_dir = path.join(base_dir, dataset)
    # out_dir = base_dir + dataset + "/{}/".format(aligner)  # dataset id
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    #fi_count = file_list.split("/")[-1].split(".")[0]

    # used to write files
    # fi_count = 0
    total_seen = 0
    alignments, labels = [], []

    final_fis = []

    for align_fi in file_list:
        total_seen += 1
        # get y_label files
        label_fi = align_fi.replace("{}_test_x".format(aligner), "test_y").replace("fas", "txt")
        # parse alignments into arrays, get the y_label from files
        parsed_alignment = parse_alignment(align_fi)
        # catch alignments that have been entirely deleted
        if parsed_alignment is None:
            continue
        parsed_label = get_label(label_fi)
        # store temporary chunk of alignment/label pairs
        alignments.append(parsed_alignment)
        labels.append(parsed_label)
        final_fis.append(align_fi)

    out_tf_record = path.join(out_dir, "{}.{}.alignments.tfrecord".format(dataset, aligner))

    with tf.io.TFRecordWriter(out_tf_record) as writer:
        print("len of alignments is: {}".format(len(alignments)))
        for i in range(len(alignments)):
            try:
                example = serialize_example(alignments[i], labels[i], final_fis[i])
                writer.write(example)
            except:
                print("ERROR:")
                print(alignments[i])
                print(labels[i], final_fis[i])


if __name__ == "__main__":
    main()
