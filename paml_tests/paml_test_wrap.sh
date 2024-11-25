#!/usr/bin/env bash


# CL Arguments
DATASET_ID="$1"
# N="$2"


# # Define Function
# loop_fn () {

#     file="$1"

#     # Get file number
#     file_and_ext="$(basename -- $file)" 
#     file_only="${file_and_ext%.*}"

#     # Get tree
#     aligner_path="$(dirname -- $file)"
#     group_path="$(dirname -- $aligner_path)"
#     control_file="${group_path}/reference/controlFiles/control_${file_only}.txt"
#     tree=$(grep -oP "\[TREE\] treename  (.*)" "${control_file}" | sed "s/\[TREE\] treename  //")
#     echo ${tree} >> "/hps/nobackup/goldman/charwest/omega_ai/tree_tmp/${file_only}_${aligner}.tmp"

#     # ${file} is the msa

#     # Setup codeml directory
#     if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}" ]; then
#         mkdir "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}"
#     fi

#     if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}" ]; then
#         mkdir "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}"
#     fi

#     if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}" ]; then
#         mkdir "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}"
#     fi

#     scp /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/codeml \
#         "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}/"

#     # Run PAML script
#     python /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/paml_test.py \
#         ${file} \
#         "/hps/nobackup/goldman/charwest/omega_ai/tree_tmp/${file_only}_${aligner}.tmp" \
#         "/hps/nobackup/goldman/charwest/omega_ai/paml_test/${DATASET_ID}/${aligner}/${file_only}/" \
#         > "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}/${DATASET_ID}_${aligner}_${file_only}_res.txt"

#     rm "/hps/nobackup/goldman/charwest/omega_ai/tree_tmp/${file_only}_${aligner}.tmp"
# }

# Check/make dataset ID directory
if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}" ]; then
    mkdir "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}"
fi

# N=20

# # Loop over aligners and test trees in test dataset (usually ~2000 trees)
# for aligner in clustal mafft prankaa prankc; do
#     # Check/make aligner directory
#     if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}" ]; then
#         mkdir "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}"
#     fi

#     ( #parallel
#     for file in $(ls /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/${DATASET_ID}/*/${aligner}_test_x/*); do
#         # ((i=i%N)); ((i++==0)) && wait
#         # loop_fn "$file" & 
#         bsub -o /dev/null -e /dev/null -n 1 -M 2048 -R "rusage[mem=2048]" \
#             /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/paml_run.sh \
#             ${file} \
#             ${DATASET_ID} \
#             ${aligner}
#         sleep 1

#     done
#     ) #parallel
#     wait

#     python /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/paml_accuracy.py \
#         --dataset ${DATASET_ID} \
#         --aligner ${aligner}

# done

# Loop over aligners and test trees in test dataset (usually ~2000 trees)
counter=1
for aligner in clustal; do
    # Check/make aligner directory
    if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}" ]; then
        mkdir "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}"
    fi

    ( #parallel

    touch /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
    chmod +x /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh

    for file in $(ls /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/${DATASET_ID}/*/${aligner}_test_x/*); do

        # # Make new shell run script
        # if [[ "$counter" -eq 1 ]]; then
        #     echo " ######### NEW FILE #########"
        #     touch /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
        #     chmod +x /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
        # fi

        echo "sh /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/paml_run.sh \\" >> /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
        echo "  ${file} \\" >> /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
        echo "  ${DATASET_ID} \\" >> /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
        echo "  ${aligner}" >> /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
        echo "sleep 0.2" >> /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh

        cat /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh

        # Reset the counter to 1 if it reaches 50
        if (( counter > 49 )); then
            echo "### GOT HERE ###"
            
            # bsub /hps/nobackup/goldman/charwest/omega_ai/paml_test_out/loop_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/paml_test_out/loop_%J.err \
            #    -n 1 -M 2048 -R "rusage[mem=2048]" \
            #    /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh 

            counter=1

            rm /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
            touch /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
            chmod +x /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh
        else
            echo "### COUNTER LASS THAN 50 ###"
        
        fi

        # Increment the counter
        counter=$((counter + 1))

        echo $counter

    done
    ) #parallel
    
    if [ -e "/hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh" ]; then

        echo "### OUTSIDE ###"
        bsub -o /hps/nobackup/goldman/charwest/omega_ai/paml_test_out/loop_%J.out -e /hps/nobackup/goldman/charwest/omega_ai/paml_test_out/loop_%J.err -n 1 -M 2048 -R "rusage[mem=2048]" \
            /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh

        rm /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests.sh

    fi

done

    # python /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/paml_accuracy.py \
    #     --dataset ${DATASET_ID} \
    #     --aligner ${aligner}

# selection status is in e.g. /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/divbase_indistNB_indrate01_tips8_posprop05/group_0/test_y 


#####################################

# # CL Arguments
# DATASET_ID="$1"

# # Check/make dataset ID directory
# if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}" ]; then
#   mkdir "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}"
# fi

# # Loop over aligners and test trees in test dataset (usually ~2000 trees)
# for aligner in clustal mafft prankaa prankc; do
#     # Check/make aligner directory
#     if [ ! -d "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}" ]; then
#         mkdir "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}"
#     fi

#     ##### Parallelisation #####
#     N=8 #parallel
#     # ( #parallel

#     for file in $(ls /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/${DATASET_ID}/*/${aligner}_test_x/*); do
#         # Parallelisation stuff
#         ((i=i%N)); ((i++==0)) && wait

#         (
#         # Get file number
#         file_and_ext="$(basename -- $file)" 
#         file_only="${file_and_ext%.*}"

#         # Get tree
#         aligner_path="$(dirname -- $file)"
#         group_path="$(dirname -- $aligner_path)"
#         control_file="${group_path}/reference/controlFiles/control_${file_only}.txt"
#         tree=$(grep -oP "\[TREE\] treename  (.*)" "${control_file}" | sed "s/\[TREE\] treename  //")
#         echo ${tree} >> "/hps/nobackup/goldman/charwest/omega_ai/tree_tmp/${file_only}_${aligner}.tmp"

#         # ${file} is the msa

#         # Run PAML script
#         python /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/paml_test.py \
#             ${file} \
#             "/hps/nobackup/goldman/charwest/omega_ai/tree_tmp/${file_only}_${aligner}.tmp" \
#             > "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/${DATASET_ID}/${aligner}/${DATASET_ID}_${aligner}_${file_only}_res.txt"
        
#         rm "/hps/nobackup/goldman/charwest/omega_ai/tree_tmp/${file_only}_${aligner}.tmp"

#     ) & #parallel  
#     done
#     # ) & #parallel
#     wait

#     python /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/paml_accuracy.py \
#         --dataset ${DATASET_ID} \
#         --aligner ${aligner}

# done

# # selection status is in e.g. /hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/divbase_indistNB_indrate01_tips8_posprop05/group_0/test_y 
