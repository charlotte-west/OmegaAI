#!/usr/bin/env bash

DATASET_ID="$1"

conda_com="source /hps/software/users/goldman/charwest/miniconda3/bin/activate && conda deactivate && conda activate omega_ai"

for FILE in /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_file_lists/${DATASET_ID}/*;
do 
    sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/all_tfrec.out \
        --error=/hps/nobackup/goldman/charwest/omega_ai/all_tfrec.err \
        --time=72:00:00 \
        --cpus-per-task=2 \
        --ntasks=1 \
        --mem=4G \
        --wrap "$conda_com && python /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/generate_datasets/alignments_to_test_tfrecords.py ${DATASET_ID} $FILE;"

done
