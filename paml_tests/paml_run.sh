#!/usr/bin/env bash

# Code Authorship:
#   Original implementation: Charlotte West

# CL Arguments
file="$1"
DATASET_ID="$2"
aligner="$3"

# Get file number
file_and_ext="$(basename -- $file)" 
file_only="${file_and_ext%.*}"

# Get tree
aligner_path="$(dirname -- $file)"
group_path="$(dirname -- $aligner_path)"
control_file="${group_path}/reference/controlFiles/control_${file_only}.txt"
tree=$(grep -oP "\[TREE\] treename  (.*)" "${control_file}" | sed "s/\[TREE\] treename  //")
echo ${tree} >> "/omega_ai/tree_tmp/${DATASET_ID}_${file_only}_${aligner}.tmp"

# Setup codeml directory
if [ ! -d "/omega_ai/paml_test/${DATASET_ID}" ]; then
    mkdir "/omega_ai/paml_test/${DATASET_ID}"
fi

if [ ! -d "/omega_ai/paml_test/${DATASET_ID}/${aligner}" ]; then
    mkdir "/omega_ai/paml_test/${DATASET_ID}/${aligner}"
fi

if [ ! -d "/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}" ]; then
    mkdir "/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}"
fi

scp /omega_ai/slurm_cnn_selection/paml_tests/codeml \
    "/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}/"

# Run PAML script
python /omega_ai/slurm_cnn_selection/paml_tests/paml_test.py \
    ${file} \
    "/omega_ai/tree_tmp/${DATASET_ID}_${file_only}_${aligner}.tmp" \
    "/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}/" \
    "/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}/${DATASET_ID}_${aligner}_${file_only}"

# Run again for 
rm "/omega_ai/tree_tmp/${DATASET_ID}_${file_only}_${aligner}.tmp"
