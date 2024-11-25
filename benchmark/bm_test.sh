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

# NOTE!!
# To be run from generate_datasets directory

# Specify the file to store the timing information
timing_file="/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/test.txt"

# Record the start time
start_time=$(date +%s)

# Start datetime
bash_datetime=$(date +"%Y-%m-%d %H:%M:%S")
echo "start time: $bash_datetime" >> "$timing_file"

# Setup variables
let avg=$1/$2
let avg+=1
start=0
let end=start+avg

echo "$avg genes per host on average"

# Conda environment
conda_com="source /hps/software/users/goldman/charwest/miniconda3/bin/activate && conda deactivate && conda activate omega_ai"

# NOTE THAT ONLY ONE FOR LOOP BELOW SHOULD BE UNCOMMENTED WHEN RUNNING

## baseline ### 0.05
for ((h=1; h<=$2; h++))
do
        sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/sim_out/bm_test.out \
                --error=/hps/nobackup/goldman/charwest/omega_ai/sim_out/bm_test.err \
                --time=1:00:00 \
                --cpus-per-task=2 \
                --ntasks=1 \
                --mem=512M \
                --wrap "$conda_com && python hello.py $start $end"

        let start+=avg
        let end+=avg
        sleep 0.05
done

# # Wait for specific background jobs to complete
# for job_id in "${job_ids[@]}"; do
#     wait "$job_id"
# done

# Record the end time
end_time=$(date +%s)

# Calculate the total execution time
execution_time=$((end_time - start_time))

# Save the timing information to the file
echo "All jobs completed. Total execution time: $execution_time seconds" >> "$timing_file"

echo "Total execution time: $execution_time seconds"
