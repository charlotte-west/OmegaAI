# bash shell script to parallel the simulation
# generator_v2 python script should be in the directory
# indelible & clustalo executable, pal2nal perl script should be in the directory

# command to run the script on the cluster:
# "bsub ./parallel.sh 乙 甲 "         
# 乙: number of genes to simulate (a few more genes are generated for divisibility reason)
# 甲: number of threads for parallel computing

# In the directory, the folder output_aligned contains Clustal O aligned genes (input of NN)
# the folder parameters contains the parameters of each control file in this
# order: p0, p1, w0, w1, w2, root length, kappa, insertion & deletion rate,
# alpha of Rieman Zetas insertion & deletion size distribution 

# branchLength=0.2
# randomSeed=42

let avg=$1/$2
let avg+=1
start=0
let end=start+avg

echo "$avg genes per host on average"

# Conda environment
conda_com="source /hps/software/users/goldman/charwest/miniconda3/bin/activate && conda deactivate && conda activate omega_ai"

# NOTE THAT ONLY ONE FOR LOOP BELOW SHOULD BE UNCOMMENTED WHEN RUNNING

# baseline ### 0.05
for ((h=1; h<=$2; h++))
do
        sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/sim_out/mixtree_indistNB_indrate01_tips8_posprop05_500k.out \
                --error=/hps/nobackup/goldman/charwest/omega_ai/sim_out/mixtree_indistNB_indrate01_tips8_posprop05_500k.err \
                --time=48:00:00 \
                --cpus-per-task=2 \
                --ntasks=1 \
                --mem=512M \
                --wrap "$conda_com && python to_groups.py $start $end 'baseline' 'NB' '0.1' 'mixtree_indistNB_indrate01_tips8_posprop05_500k' 'train' 'clustal' 'mix' 0.5"

        let start+=avg
        let end+=avg
        sleep 0.2
done

# # baseline ### 0.05
# for ((h=1; h<=$2; h++))
# do
#         sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_highsiteposprop_divbase_indistNB_indrate01_tips8_posprop05_500k.out \
#                 --error=/hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_highsiteposprop_divbase_indistNB_indrate01_tips8_posprop05_500k.err \
#                 --time=48:00:00 \
#                 --cpus-per-task=2 \
#                 --ntasks=1 \
#                 --mem=512M \
#                 --wrap "$conda_com && python to_groups.py $start $end 'baseline' 'NB' '0.1' 'highsiteposprop_divbase_indistNB_indrate01_tips8_posprop05_500k' 'train' 'clustal' 8 0.5"

#         let start+=avg
#         let end+=avg
#         sleep 0.2
# done

# ## baseline ### 0.05
# for ((h=1; h<=$2; h++))
# do
#         sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_divbase_indistNB_indrate01_tips8_posprop05_100k.out \
#                 --error=/hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_divbase_indistNB_indrate01_tips8_posprop05_100k.err \
#                 --time=120:00:00 \
#                 --cpus-per-task=2 \
#                 --ntasks=1 \
#                 --mem=512M \
#                 --wrap "$conda_com && python to_groups.py $start $end 'baseline' 'NB' '0.1' 'divbase_indistNB_indrate01_tips8_posprop05_100k' 'train' 'clustal' 8 0.5"

#         let start+=avg
#         let end+=avg
#         sleep 0.2
# done


# ## MIXED DIVERGENCE MODEL ##
# # Define the values you want to loop through
# div_values=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0)

# # Calculate the step size to divide the array equally
# step_size=$(( $2 / ${#div_values[@]} ))
# k=1
# idx=0
# for ((h=1; h<=$2; h++))
# do
        
#         # Get the current value of $div from the array
#         # echo $k 
#         # echo $idx
#         div=${div_values[$idx]}
#         # echo $div

#         sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_5m_mixed_indistNB_indrate01_tips8_posprop05_validation.out \
#                 --error=/hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_5m_mixed_indistNB_indrate01_tips8_posprop05_validation.err \
#                 --time=72:00:00 \
#                 --cpus-per-task=2 \
#                 --ntasks=1 \
#                 --mem=512M \
#                 --wrap "$conda_com && python to_groups.py $start $end '$div' 'NB' '0.1' 'mixed_indistNB_indrate01_tips8_posprop05_validation' 'train' 'clustal' 8 0.5"

#         let start+=avg
#         let end+=avg

#         if [ $k -eq $step_size ]; then
#                 k=1
#                 idx=$((idx + 1))
#         else
#                 k=$((k + 1))
#         fi
        
#         sleep 0.2
# done


# bsub -o /hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_%J.err -M 256 -R "rusage[mem=256]" -n 2 python to_groups.py $start $end "0.4" "NB" "0.1" "true_div04_indistNB_indrate01_tips8_posprop05" "train" "clustal" 8 0.5 "true_align"

# ## baseline ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -g /omega_gen -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "baseline" "train" "clustal" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ## baseline SLURM ### 0.05
# for ((h=1; h<=$2; h++))
# do
#         sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_%J.out --error=/hps/nobackup/goldman/charwest/omega_ai/sim_out/sim_%J.err --mem=256M --cpus-per-task=2 python to_groups.py $start $end "0.8" "NB" "0.1" "tester_div08_indistNB_indrate01_tips8_posprop05" "train" "clustal" 8 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.5
# done


# ## baseline - 4 thread standard ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -q mpi -o /hps/nobackup/goldman/charwest/omega_ai/mpi_6_bsub_6_clustal/sim_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/mpi_6_bsub_6_clustal/sim_%J.err -M 256 -R "rusage[mem=256]" -n 6 python to_groups.py $start $end "baseline" "NB" "0.1" "mpi_6_bsub_6_clustal" "train" "clustal" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done

# ## baseline - mafft run ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -q mpi -o /hps/nobackup/goldman/charwest/omega_ai/mafft_tests/mafft_test_single/sim_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/mafft_tests/mafft_test_single/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "single_baseline_mafft" "train" "mafft" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done

# ## baseline - midsize test no log ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -q mpi -outdir /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/midsize_mpi_no_log_long/"%J"/ -o /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/midsize_mpi_no_log_long/"%J"/output -e /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/midsize_mpi_no_log_long/"%J"/error -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_mid_size_mpi_no_log_long" "train" "clustal" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ## baseline - midsize test ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -q mpi -o /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/midsize_mpi/sim_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/midsize_mpi/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_mid_size_mpi" "train" "clustal" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done

# ### hl-codon-30-01  ###
# for ((h=1; h<=$2; h++))
# do
#         bsub -q mpi -m hl-codon-30-01 -o /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/sim_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_hl_codon_30_01" "train" "clustal" 8 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.1
# done

# ### hl-codon-33-01  ###
# for ((h=1; h<=$2; h++))
# do
#         bsub -q mpi -m hl-codon-33-01 -o /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/sim_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_hl_codon_33_01" "train" "clustal" 8 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.1
# done

# ### hl-codon-32-01  ###
# for ((h=1; h<=$2; h++))
# do
#         bsub -q mpi -m hl-codon-32-01 -o /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/sim_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_hl_codon_32_01" "train" "clustal" 8 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.1
# done

### hl-codon-31-01  ###
# for ((h=1; h<=$2; h++))
# do
#         bsub -q mpi -m hl-codon-31-01 -o /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/sim_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/rafa_test_out/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_hl_codon_31_01" "train" "clustal" 8 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.1
# done

# ### range of branch lengths, baseline parameters otherwise ###
# for bl in 0.01 0.05 0.1 0.3 0.4 0.5 0.7 0.8 0.9 1.0; do
#     for ((h=1; h<=$2; h++))
#     do
#         bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "$bl" "NB" "0.1" "baseline_$bl" "train" "clustal" 8 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.1
#     done
# done


# ### baseline but aligned using MAFFT ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "baseline" "train" "mafft" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ### 10% positive selection ###
# for ((h=1; h<=$2; h++))
# do
#     bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "fraction_positive_0.1" "train" "clustal" 8 0.1
#     let start+=avg
#     let end+=avg
#     sleep 0.1
# done


# ### low indel rate ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.03" "baseline" "train" "clustal" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ### high indel rate ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.6" "baseline" "train" "clustal" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ### power law distributed indel lengths ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "POW" "0.1" "baseline" "train" "clustal" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ### alternate artificial tree topologies ###
# for tips in 32 64; do
#     for ((h=1; h<=$2; h++))
#     do
#         bsub -o /dev/null -e /dev/null -M 512 -R "rusage[mem=512]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "tips_$tips" "train" "clustal" "$tips" 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.1
#     done
# done
