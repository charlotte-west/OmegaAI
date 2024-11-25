#!/usr/bin/env bash

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
# tree="(((A:0.5,B:0.5):0.5,(C:0.5,D:0.5):0.5):0.5,((E:0.5,F:0.5):0.5,(G:0.5,H:0.5):0.5):0.5);"
echo ${tree} >> "/hps/nobackup/goldman/charwest/omega_ai/tree_tmp/${DATASET_ID}_${file_only}_${aligner}.tmp"

# ${file} is the msa

# Setup codeml directory
if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}" ]; then
    mkdir "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}"
fi

if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}" ]; then
    mkdir "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}"
fi

if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}" ]; then
    mkdir "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}"
fi

scp /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/codeml \
    "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}/"

# Run PAML script
python /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/paml_test.py \
    ${file} \
    "/hps/nobackup/goldman/charwest/omega_ai/tree_tmp/${DATASET_ID}_${file_only}_${aligner}.tmp" \
    "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}/" \
    "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}/${DATASET_ID}_${aligner}_${file_only}"

# Run again for 

rm "/hps/nobackup/goldman/charwest/omega_ai/tree_tmp/${DATASET_ID}_${file_only}_${aligner}.tmp"

# > "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}/${DATASET_ID}_${aligner}_${file_only}_res.txt"