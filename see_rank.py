#!/usr/local/bin/python

import argparse
import tensorflow as tf

# def inspect_tfrecords(tfrecords_path):
#     record_iterator = tf.data.TFRecordDataset(tfrecords_path).as_numpy_iterator()

#     for record in record_iterator:
#         example = tf.train.Example()
#         example.ParseFromString(record)

#         for feature_key in example.features.feature:
#             feature = example.features.feature[feature_key]
            
#             if feature_key == "fasta_path":
#                 value = feature.bytes_list.value[0].decode("utf-8")
#                 dtype = "string"
#                 shape = None
#                 rank = None
#             elif feature_key == "alignment":
#                 value = tf.io.parse_tensor(feature.bytes_list.value[0], out_type=tf.float32).numpy()
#                 dtype = "float32"
#                 shape = value.shape
#                 rank = len(value.shape)
#             elif feature_key == "y_label":
#                 value = feature.int64_list.value[0]
#                 dtype = "int64"
#                 shape = None
#                 rank = None
#             else:
#                 value = None
#                 dtype = None
#                 shape = None
#                 rank = None
            
#             print(f"Feature: {feature_key}")
#             if dtype is not None:
#                 print(f"  Data Type: {dtype}")
#             if shape is not None:
#                 print(f"  Shape: {shape}")
#             if rank is not None:
#                 print(f"  Rank: {rank}")
#             if value is not None:
#                 print(f"  Value: {value}")
#             print()


def inspect_tfrecords(tfrecords_path):
    record_iterator = tf.data.TFRecordDataset(tfrecords_path).as_numpy_iterator()

    for record_idx, record in enumerate(record_iterator, start=1):
        example = tf.train.Example()
        example.ParseFromString(record)

        print(f"Record {record_idx}:")
        record_info = {}

        for feature_key in example.features.feature:
            feature = example.features.feature[feature_key]
            
            if feature_key == "fasta_path":
                record_info["fasta_path"] = {
                    "value": feature.bytes_list.value[0].decode("utf-8"),
                    "dtype": "string"
                }
            elif feature_key == "alignment":
                value = tf.io.parse_tensor(feature.bytes_list.value[0], out_type=tf.float32).numpy()
                record_info["alignment"] = {
                    "value": value,
                    "dtype": "float32",
                    "shape": value.shape,
                    "rank": len(value.shape)
                }
            elif feature_key == "y_label":
                record_info["y_label"] = {
                    "value": feature.int64_list.value[0],
                    "dtype": "int64"
                }

        # Print the collected information for the current record
        ordered_keys = ["fasta_path", "y_label", "alignment"]
        for feature_key in ordered_keys:
            info = record_info.get(feature_key, {})
            print(f"Feature: {feature_key}")
            print(f"  Data Type: {info.get('dtype', '')}")
            if "shape" in info:
                print(f"  Shape: {info['shape']}")
            if "rank" in info:
                print(f"  Rank: {info['rank']}")
            print(f"  Value: {info.get('value', '')}")
            print()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Inspect TFRecords file.")
    parser.add_argument("--tfrecords_path", type=str, help="Path to the TFRecords file")
    args = parser.parse_args()
    
    inspect_tfrecords(args.tfrecords_path)
