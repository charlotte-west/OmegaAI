#!/usr/bin/env python

# Code Authorship:
#   Original implementation: Conor R. Walker and Xingze Xu
#   Contributors:
#       - Charlotte West

import argparse
import os
import pandas as pd
import numpy as np

#--------- CLI Arguments ---------#
parser = argparse.ArgumentParser()
parser.add_argument("--dataset", help="ID of the dataset to test",
                    default="na", type=str, dest="dataset")
parser.add_argument("--aligner", help="aligner used for the MSA",
                    default="", type=str, dest="aligner")
args = parser.parse_args()


# Get list of selection predictions for given dataset/aligner
paml_res_dir = "/omega_ai/data/simulations/paml_test_results/{0}/{1}".format(args.dataset, args.aligner)

# Initialise counts
tp = 0
fp = 0
tn = 0
fn = 0

for file in os.listdir(paml_res_dir):
    paml_file = os.fsdecode(file)

    # Check if the file ends with '_res.txt'
    if paml_file.endswith('_res.txt'):

        # Get numerical ID for run 
        num_id = paml_file.split('_')[-2]
        num_id_float = float(num_id)

        ## Get true selection status
        # Determine group
        if num_id_float <= 500:
            group = "group_0"
        elif (num_id_float > 500) & (num_id_float < 1002):
            group = "group_501"
        elif (num_id_float >= 1002) & (num_id_float <= 1502):
            group = "group_1002"
        else:
            group = "group_1503"

        true_file_path = "/omega_ai/data/simulations/test_datasets/{0}/{1}/test_y/{2}.txt".format(args.dataset, group, num_id)

        # PAML pred
        paml_file_path = paml_res_dir + "/" + paml_file
        paml_file = open(paml_file_path, 'r')
        paml_pred = paml_file.read()
        paml_pred = ''.join(paml_pred.split()) #remove any new lines or blank spaces
        # print(paml_pred)
        paml_file.close()

        # True state
        true_file = open(true_file_path, 'r')
        true_state = true_file.read()
        true_state = ''.join(true_state.split()) #remove any new lines or blank spaces
        # print(true_state)
        true_file.close()

        ## Compare true state and PAML prediction
        if paml_pred == '':
            continue

        paml_pred = float(paml_pred)
        true_state = float(true_state)

        if (true_state == 1) & (paml_pred == 1):
            tp += 1
        elif (true_state == 1) & (paml_pred == 0):
            fn += 1
        elif (true_state != 1) & (paml_pred == 1):
            fp += 1
        else:
            tn += 1


# calculate rates and accuracy
tpr = tp / (tp+fn)
fpr = fp / (fp+tn)
acc = (tp+tn) / (tp+fp+tn+fn)

# Save to csv file
results = { "accuracy" : acc, "tpr" : tpr, "fpr": fpr,  "tp" : tp, "fp" : fp, "tn" : tn, "fn" : fn, "dataset" : args.dataset, "aligner": args.aligner}
res_df = pd.DataFrame(results, index=[0])
res_df.to_csv("/omega_ai/data/simulations/paml_test_results/{0}/{0}_{1}_res.csv".format(args.dataset, args.aligner), index=False)

    

