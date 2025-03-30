#!/usr/bin/env bash

# Code Authorship:
#   Original implementation: Xingze Xu

# bash shell script to parallel the simulation
# generator_v2 python script should be in the directory
# indelible & clustalo executable, pal2nal perl script should be in the directory

# command to run the script on the cluster:
# "bsub ./parallel.sh 乙 甲 "         
# 乙: number of genes to simulate (a few more genes are generated for divisibility reason)
# 甲: number of threads for parallel computing

# In the directory, the folder output_aligned contains Clustal O aligned genes (input of NN)
# the folder parameters contains the parameters of each control file in this
# alpha of Rieman Zetas insertion & deletion size distribution 
# order: p0, p1, w0, w1, w2, root length, kappa, insertion & deletion rate,

let avg=$1/$2
let avg+=1
start=0
let end=start+avg

echo "$avg genes per host on average"

# Conda environment
conda_com="/miniconda3/bin/activate && conda deactivate && conda activate omega_ai"

# baseline
for ((h=1; h<=$2; h++))
do
        sbatch --output=/omega_ai/sim_out/divbase_indistNB_indrate01_tips8_posprop05.out \
                --error=/omega_ai/sim_out/divbase_indistNB_indrate01_tips8_posprop05.err \
                --time=48:00:00 \
                --cpus-per-task=2 \
                --ntasks=1 \
                --mem=512M \
                --wrap "$conda_com && python to_groups.py $start $end 'baseline' 'NB' '0.1' 'divbase_indistNB_indrate01_tips8_posprop05' 'train' 'clustal' 8 0.5"

        let start+=avg
        let end+=avg
        sleep 0.2
done

