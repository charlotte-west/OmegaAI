#!/usr/bin/env bash

DATASET_ID="$1"

# if [ -d "$DATASET_ID" ]; then
#     echo "dir already exists"
# else
#     mkdir /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_file_lists/${DATASET_ID}
#     find /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/${DATASET_ID}/group_*/*_test_x/*fas > /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_file_lists/${DATASET_ID}/alignment_files.txt
# fi

mkdir /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_file_lists/${DATASET_ID}
find /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/${DATASET_ID}/group_*/*_test_x/*fas > /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_file_lists/${DATASET_ID}/1.txt

bsub -o /hps/nobackup/goldman/charwest/omega_ai/tf_rec_out/${DATASET_ID}_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/tf_rec_out/${DATASET_ID}_%J.err -M 4G -n 2 python /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/generate_datasets/alignments_to_test_tfrecords.py ${DATASET_ID} /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_file_lists/${DATASET_ID}/1.txt
