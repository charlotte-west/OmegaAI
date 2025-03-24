#!/usr/bin/env bash

DATASET_ID="$1"

# Specify the file to store the timing information
timing_file="/omega_ai/data/benchmark/${DATASET_ID}/tfrecord_start_time.txt"

# Start datetime
bash_datetime=$(date +"%Y-%m-%d %H:%M:%S")
echo "start time: $bash_datetime" >> "$timing_file"

conda_com="source /hps/software/users/goldman/charwest/miniconda3/bin/activate && conda deactivate && conda activate omega_ai"

for FILE in /omega_ai/data/simulations/file_lists/${DATASET_ID}/*;
do
    sbatch --output=/omega_ai/tfrec_out/${DATASET_ID}_%J.out \
        --error=/omega_ai/tfrec_out/${DATASET_ID}_%J.out.err \
        --time=24:00:00 \
        --cpus-per-task=1 \
        --ntasks=1 \
        --mem=12G \
        --wrap "$conda_com && python /omega_ai/slurm_cnn_selection/generate_datasets/alignments_to_tfrecords.py ${DATASET_ID} $FILE"

done
