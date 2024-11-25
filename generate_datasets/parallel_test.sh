# bash shell script to parallel the simulation
# generator_v2 python script should be in the directory
# indelible & clustalo executable, pal2nal perl script should be in the directory

# command to run the script on the cluster:
# "bsub ./parallel.sh 乙 甲 "         
# 乙: number of genes to simulate (a few more genes are generated for divisibility reason)
# 甲: number of threads for parallel computing

# In the directory, the folder output_aligned contains Clustal O aligned genes (inpu of NN)
# the folder paratmeters (typo) contains parameters of each control file, in this order: p0,p1,w0,w1,w2, root length,kappa,insertion & deletion rate, alpha of Rieman Zetas insertion & deletion size distribution 

# branchLength=0.2
# randomSeed=42

let avg=$1/$2
let avg+=1
start=0
let end=start+avg

echo "$avg genes per host on average"

# Conda environment
conda_com="source /hps/software/users/goldman/charwest/miniconda3/bin/activate && conda deactivate && conda activate omega_ai"


# ### baseline ###
# for ((h=1; h<=$2; h++))
# do
#     sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/sim_out/random_32_tips_%J.out \
#                 --error=/hps/nobackup/goldman/charwest/omega_ai/sim_out/random_32_tips_%J.err \
#                 --time=48:00:00 \
#                 --cpus-per-task=2 \
#                 --ntasks=1 \
#                 --mem=512M \
#                 --wrap "$conda_com && python test_to_groups.py $start $end 'baseline' 'NB' '0.1' 'random_32_tips' 'clustal' 8 0.5"

# 	let start+=avg
# 	let end+=avg
# 	sleep 0.5
# done

# exit

## MIXED DIVERGENCE MODEL ##
# Define the values you want to loop through
div_values=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0)

# Calculate the step size to divide the array equally
step_size=$(( $2 / ${#div_values[@]} ))
k=1
idx=0
for ((h=1; h<=$2; h++))
do
        
        # Get the current value of $div from the array
        # echo $k 
        # echo $idx
        div=${div_values[$idx]}
        # echo $div

        sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/sim_out/divmix_indistNB_indrate01_tips8_posprop05_10K%J.out \
                --error=/hps/nobackup/goldman/charwest/omega_ai/sim_out/divmix_indistNB_indrate01_tips8_posprop05_10K%J.err \
                --time=72:00:00 \
                --cpus-per-task=2 \
                --ntasks=1 \
                --mem=512M \
                --wrap "$conda_com && python test_to_groups.py $start $end '$div' 'NB' '0.1' 'mixed_indistNB_indrate01_tips8_posprop05_10k' 'clustal' 8 0.5"

        let start+=avg
        let end+=avg

        if [ $k -eq $step_size ]; then
                k=1
                idx=$((idx + 1))
        else
                k=$((k + 1))
        fi
        
        sleep 0.2
done

exit

# bsub -o /hps/nobackup/goldman/charwest/omega_ai/old_output/sim_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/old_output/sim_%J.err -M 256 -R "rusage[mem=256]" -n 2 -q short python test_to_groups.py $start $end "0.1" "NB" "0.1" "test_shuffle_div01_indistNB_indrate01_tips8_posprop05" "clustal" 8 0.5 "shuffle"
# bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 2 python test_to_groups.py $start $end "baseline" "NB" "0.1" "divbase_indistNB_indrate01_tips8_posprop05" "clustal" 8 0.5


### 10% positive selection ###
# let avg=$1/$2
# let avg+=1
# start=0
# let end=start+avg
# 
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python test_to_groups.py $start $end "baseline" "NB" "0.1" "fraction_positive_0.1" "clustal" "baseline_tree" "0.1"
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done

# ### alternate tree topologies ###
# let avg=$1/$2
# let avg+=1
# start=0
# let end=start+avg

# for tips in 32; do
#     for ((h=1; h<=$2; h++))
#     do
#         bsub -o /dev/null -e /dev/null -M 512 -R "rusage[mem=512]" -n 1 python test_to_groups.py $start $end "baseline" "NB" "0.1" "tips_$tips" "clustal" "$tips" "0.5"
#         let start+=avg
#         let end+=avg
#         sleep 0.1
#     done
# done

# exit

### baseline mafft ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python test_to_groups.py $start $end "baseline" "NB" "0.1" "baseline" "mafft"
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ### range of branch lengths, baseline parameters otherwise ###
# let avg=$1/$2
# let avg+=1
# start=0
# let end=start+avg

# for bl in 0.01 0.05 0.1 0.3 0.4 0.5 0.7 0.8 0.9 1.0; do
#     for ((h=1; h<=$2; h++))
#     do
#         bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python test_to_groups.py $start $end "$bl" "NB" "0.1" "baseline_$bl" "clustal"
#         let start+=avg
#         let end+=avg
#         sleep 0.1
#     done
# done

# exit


# ### higher divergence ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python test_to_groups.py $start $end "high" "NB" "0.1" "high_divergence" "clustal"
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ### lower divergence ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python test_to_groups.py $start $end "low" "NB" "0.1" "low_divergence" "clustal"
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ### higher indel rate ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python test_to_groups.py $start $end "baseline" "NB" "0.6" "high_indel_rate" "clustal"
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ### lower indel rate ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python test_to_groups.py $start $end "baseline" "NB" "0.03" "low_indel_rate" "clustal"
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done


# ### power law ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python test_to_groups.py $start $end "baseline" "POW" "0.1" "power_law_indels" "clustal"
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done

