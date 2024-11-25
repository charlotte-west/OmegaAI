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

# rm -r group_*

let avg=1000000/2000
let avg+=1
line_file="$1"



# NOTE THAT ONLY ONE FOR LOOP BELOW SHOULD BE UNCOMMENTED WHEN RUNNING

### baseline ###
#for ((h=1; h<=$2; h++))
#do
#	bsub -g /omega_gen -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "baseline" "train" "clustal" 8 0.5
#	let start+=avg
#	let end+=avg
#	sleep 0.1
#done

## baseline ###
while IFS= read -r line_no;
do
        let start="$((($line_no-1)*avg))"
        let end="$((($line_no)*avg))"
        bsub -o /dev/null -e /dev/null -M 256 -R "rusage[mem=256]" -n 2 python to_groups.py $start $end "0.8" "NB" "0.1" "div08_indistNB_indrate01_tips8_posprop05" "train" "clustal" 8 0.5
        sleep 0.1
done < "$line_file"



# ## baseline ###
# for ((h=1; h<=$2; h++))
# do
# 	bsub -q standard -o /nfs/research/goldman/charwest/omega_ai/rafa_test_out/sim_std_%J.out -e /nfs/research/goldman/charwest/omega_ai/rafa_test_out/sim_std_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_standard" "train" "clustal" 8 0.5
# 	let start+=avg
# 	let end+=avg
# 	sleep 0.1
# done

# ### hl-codon-30-01  ###
# for ((h=1; h<=$2; h++))
# do
#         bsub -q mpi -m hl-codon-30-01 -o /nfs/research/goldman/charwest/omega_ai/rafa_test_out/sim_%J.out -e /nfs/research/goldman/charwest/omega_ai/rafa_test_out/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_hl_codon_30_01" "train" "clustal" 8 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.1
# done

# ### hl-codon-33-01  ###
# for ((h=1; h<=$2; h++))
# do
#         bsub -q mpi -m hl-codon-33-01 -o /nfs/research/goldman/charwest/omega_ai/rafa_test_out/sim_%J.out -e /nfs/research/goldman/charwest/omega_ai/rafa_test_out/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_hl_codon_33_01" "train" "clustal" 8 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.1
# done

# ### hl-codon-32-01  ###
# for ((h=1; h<=$2; h++))
# do
#         bsub -q mpi -m hl-codon-32-01 -o /nfs/research/goldman/charwest/omega_ai/rafa_test_out/sim_%J.out -e /nfs/research/goldman/charwest/omega_ai/rafa_test_out/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "test_hl_codon_32_01" "train" "clustal" 8 0.5
#         let start+=avg
#         let end+=avg
#         sleep 0.1
# done

### hl-codon-31-01  ###
# for ((h=1; h<=$2; h++))
# do
#         bsub -q mpi -m hl-codon-31-01 -o /nfs/research/goldman/charwest/omega_ai/clustal_tests/outputs/norm_benchmark_5000/sim_%J.out -e /nfs/research/goldman/charwest/omega_ai/clustal_tests/outputs/norm_benchmark_5000/sim_%J.err -M 256 -R "rusage[mem=256]" -n 1 python to_groups.py $start $end "baseline" "NB" "0.1" "normal_clustal_bench" "train" "clustal" 8 0.5
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
