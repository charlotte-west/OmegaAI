#!/usr/bin/env bash

#for aligner in clustal mafft; do
    # for dset in /hps/nobackup/research/goldmans/conor/omega_ai/data/simulations/test_datasets/*; do
    # for bl in 0.01 0.05 0.1 0.3 0.4 0.5 0.7 0.8 0.9 1.0; do
    #for dataset in baseline tips_64 tips_128 fraction_positive_0.1; do
    #for dataset in baseline_100k; do
# for dataset in baseline; do 

DATASET_ID="$1"
true_flag="$2"
conda_com="source /hps/software/users/goldman/charwest/miniconda3/bin/activate && conda deactivate && conda activate omega_ai"

if [ "$true_flag" = "true" ]; then
    aligner_list="true"
else
    aligner_list="clustal mafft prankaa prankc"
fi

# for aligner in clustal; do
# for aligner in clustal mafft prankaa prankc; do
# for aligner in "true"; do
for aligner in $aligner_list; do
    sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/tfrec_out/${DATASET_ID}_%J.out \
        --error=/hps/nobackup/goldman/charwest/omega_ai/tfrec_out/${DATASET_ID}_%J.err \
        --time=12:00:00 \
        --cpus-per-task=2 \
        --ntasks=1 \
        --mem=4G \
        --wrap "$conda_com && python test_alignments_to_tfrecords.py ${DATASET_ID} $aligner"
    python test_alignments_to_tfrecords.py ${DATASET_ID} $aligner
done

# bsub -o /hps/nobackup/goldman/charwest/omega_ai/tf_rec_out/tfrec_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/tf_rec_out/tfrec_%J.err -n 1 -M 10000 -R "rusage[mem=10000]" \
#         python test_alignments_to_tfrecords.py "${DATASET_ID}" "$aligner"; # "$f";
    # source /hps/software/users/goldman/charwest/miniconda3/bin/activate && conda deactivate && conda activate omega_ai && python test_alignments_to_tfrecords.py ${DATASET_ID} $aligner