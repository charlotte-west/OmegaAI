#!/usr/local/bin/python

# Packages
import os
import numpy as np
# import matplotlib.pyplot as plt
import csv
import pandas as pd

################################################
#####------------- Functions --------------####
################################################

def get_ids(directory_path):
    file_extension = ".fas"

    # Get a list of filenames in the directory
    file_list = os.listdir(directory_path)

    # Initialize an empty list to store the extracted numbers
    numbers = []

    # Iterate through the filenames and extract numbers
    for filename in file_list:
        if filename.endswith(file_extension):
            try:
                # Extract the number from the filename
                number = int(filename.split('.')[0])
                numbers.append(number)
            except ValueError:
                print(f"Skipping invalid filename: {filename}")

    # Sort the numbers if needed
    numbers.sort()
    return(numbers)


# def convert_msa_msf(msa, res_dir, group, aligner, id):
#     outfile = "{0}/{1}/{2}_msf/{3}.msf".format(res_dir, group, aligner, id)
#     os.system('mview -in fasta -out msf {0} > {1}'.format(msa, outfile))
    
def score_msa(msa_true, msa, res_dir, group, aligner, identifier):
    sps_file = "{0}/{1}/SPS/{2}/{3}_score.txt".format(res_dir, group, aligner, identifier)
    cs_file = "{0}/{1}/CS/{2}/{3}_score.txt".format(res_dir, group, aligner, identifier)
    # Check if both files already exist
    if os.path.exists(sps_file) and os.path.exists(cs_file):
        return "Files already exist."
    else:
        os.system("java -jar /hps/nobackup/goldman/charwest/omega_ai/tools/FastSP/FastSP.jar -r {0} -e {1} | awk '/SP-Score/ {{print $NF > \"{2}\"}} /TC/ {{print $NF > \"{3}\"}}'".format(msa_true, msa, sps_file, cs_file))


# def score_msf(msa_true, msa, res_dir, group, aligner, id):
#     # os.system("echo 'msf_true' && cat {}".format(msf_true))
#     # os.system("echo 'msf' && cat {}".format(msf))
#     # outfile = "{0}/{1}/{2}_score.tmp".format(res_dir, group, id)
#     sps_file = "{0}/{1}/SPS/{2}/{3}_score.txt".format(res_dir, group, aligner, id)
#     cs_file = "{0}/{1}/CS/{2}/{3}_score.txt".format(res_dir, group, aligner, id)
#     # Check if both files already exist
#     if os.path.exists(sps_file) and os.path.exists(cs_file):
#         return
#     else:
#         # os.system("bali_score {0} {1} | grep auto | awk '{{ print $3 \",\" $4 }}' > {2}".format(msf_true, msf, outfile))
#         # os.system("awk -F ',' '{{print $1 > \"{0}\"; print $2 > \"{1}\"}}' {2}".format(sps_file, cs_file, outfile))
#         # os.system("rm {}".format(outfile))
#         os.system("java -jar /hps/nobackup/goldman/charwest/omega_ai/tools/FastSP/FastSP.jar -r {0} -r {1} |  awk '/SP-Score/ {print $NF > {2}} /TC/ {print $NF > {3}}'".format(msa_true, msa, sps_file, cs_file))



################################################
#####------------- Run scoring -------------####
################################################

# Set working dir
work_dir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/fastsp_alignment_scores"
data_dir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets"

# work_dir = "/Users/charwest/projects/omega_AI/scoring_alignments/local_dev/score_test_alignments"
# data_dir = "/Users/charwest/projects/omega_AI/scoring_alignments/local_dev/test_datasets"


# Set up arrays
# divs = ['01', 'base', '03', '04', '05', '06', '07', '08', '09', '1']
divs = ['03', '04', '05', '06', '07', '08', '09', '1']
# divs = ['03', '04', '05', '06', '07', '08', '09', '1']
div_nums = [i*0.1 for i in range(10)]
inds = ['01', '02', '03']
# inds = ['01']
#inds = ['01']
ind_nums = [i*0.1 for i in range(3)]
groups = ['group_0', 'group_501', 'group_1002', 'group_1503']
aligners = ['clustal', 'mafft', 'prankaa', 'prankc']

for div in divs:
    print('new div')
    for indel in inds:
        print('new ind')
        dataset = 'div' + div + '_indistNB_indrate' + indel + '_tips8_posprop05'
        print(dataset)

        # Create results directory
        res_dir = work_dir + '/' + dataset
        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        for group in groups:
            print('new group')
            
            if not os.path.exists(res_dir + '/' + group):
                os.makedirs(res_dir + '/' + group)
                os.makedirs(res_dir + '/' + group + '/CS')
                os.makedirs(res_dir + '/' + group + '/CS/clustal')
                os.makedirs(res_dir + '/' + group + '/CS/mafft')
                os.makedirs(res_dir + '/' + group + '/CS/prankaa')
                os.makedirs(res_dir + '/' + group + '/CS/prankc')
                os.makedirs(res_dir + '/' + group + '/SPS')
                os.makedirs(res_dir + '/' + group + '/SPS/clustal')
                os.makedirs(res_dir + '/' + group + '/SPS/mafft')
                os.makedirs(res_dir + '/' + group + '/SPS/prankaa')
                os.makedirs(res_dir + '/' + group + '/SPS/prankc')
                # os.makedirs(res_dir + '/' + group + '/true_msf')
                # os.makedirs(res_dir + '/' + group + '/clustal_msf')
                # os.makedirs(res_dir + '/' + group + '/mafft_msf')
                # os.makedirs(res_dir + '/' + group + '/prankaa_msf')
                # os.makedirs(res_dir + '/' + group + '/prankc_msf')

            # Change directory to current results directory
            os.system("cd {0}/{1}".format(res_dir, group))
            
            # Get number ids for group
            ids = get_ids("{0}/{1}/{2}/clustal_test_x".format(data_dir, dataset, group))

            for identifier in ids:
                # # convert true fasta to msf
                true_msa = "{0}/{1}/{2}/reference/output_TRUE/dna_TRUE_{3}.fas".format(data_dir, dataset, group, identifier)
                # convert_msa_msf(true_msa, res_dir, group, 'true', id)
                # true_msf = "{0}/{1}/{2}_msf/{3}.msf".format(res_dir, group, 'true', id)
                

                for aligner in aligners:
                    msa = "{0}/{1}/{2}/{3}_test_x/{4}.fas".format(data_dir, dataset, group, aligner, identifier)
                    # # convert fasta to msf
                    # convert_msa_msf(msa, res_dir, group, aligner, id)
                    # msf = "{0}/{1}/{2}_msf/{3}.msf".format(res_dir, group, aligner, id)
                    # # calculate SPS and CS using baliscore
                    score_msa(true_msa, msa, res_dir, group, aligner, identifier)


