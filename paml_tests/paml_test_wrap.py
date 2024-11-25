#!/usr/bin/env python3

import os
import sys
import glob
from datetime import datetime

current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("start datetime: " + current_datetime)

# Conda command
conda_com="source /hps/software/users/goldman/charwest/miniconda3/bin/activate && conda deactivate && conda activate omega_ai"

# Command line Arguments
DATASET_ID = sys.argv[1]

# Check/make dataset ID directory
dataset_dir = f"/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results/{DATASET_ID}"
if not os.path.isdir(dataset_dir):
    os.mkdir(dataset_dir)

run_script_dir = f"/hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{DATASET_ID}"
if not os.path.isdir(run_script_dir):
    os.mkdir(run_script_dir)

# Loop over aligners and test trees in test dataset (usually ~2000 trees)
for aligner in ['clustal','mafft','prankaa','prankc']:
# for aligner in ['clustal']:
# for aligner in ['true']:
# for aligner in ['mafft','prankaa','prankc']:
    counter = 1
    name_counter = 1

    # Check/make aligner directory
    aligner_dir = f"{dataset_dir}/{aligner}"
    if not os.path.isdir(aligner_dir):
        os.mkdir(aligner_dir)

    os.system("touch /hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh".format(name_counter, aligner, DATASET_ID))
    os.system("chmod +x /hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh".format(name_counter, aligner, DATASET_ID))
    with open("/hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh".format(name_counter, aligner, DATASET_ID), "w") as f:
        f.write("#!/usr/bin/env bash\n")

    # os.system('echo "printting file"')
    # os.system('cat /hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh'.format(name_counter, aligner, DATASET_ID))
    file_pattern = f"/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/{DATASET_ID}/*/{aligner}_test_x/*"
    file_list = glob.glob(file_pattern)
    print("len of list is: {}".format(len(file_list)))
    # print(file_list)

    for file in file_list:
        
        file_path = os.path.join(f"/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/{DATASET_ID}/*/{aligner}_test_x/", file)
        with open("/hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh".format(name_counter, aligner, DATASET_ID), "a") as f:        
            f.write(f"/hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/paml_run.sh \\\n")
            f.write(f"  {file_path} \\\n")
            f.write(f"  {DATASET_ID} \\\n")
            f.write(f"  {aligner}\n")
            f.write(f" echo done\n")
            # f.write("sleep 0.01\n")

        if (counter > 49):
            # run ~50 tests
            sbatch_com = f"""
            sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/paml_test_out/loop_%J.out \
                    --error=/hps/nobackup/goldman/charwest/omega_ai/paml_test_out/loop_%J.err \
                    --time=72:00:00 \
                    --cpus-per-task=1 \
                    --ntasks=1 \
                    --mem=2G \
                    --wrap "{conda_com} && /hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{DATASET_ID}/run_50_paml_tests_{name_counter}_{aligner}.sh"
            """

            os.system(sbatch_com)
            
            # Reset the counter to 1 if it reaches 50
            counter = 1
            name_counter += 1

            # Remove 
            # os.system("rm /hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh".format(name_counter, aligner, DATASET_ID))
            os.system("touch /hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh".format(name_counter, aligner, DATASET_ID))
            os.system("chmod +x /hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh".format(name_counter, aligner, DATASET_ID))

            with open("/hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh".format(name_counter, aligner, DATASET_ID), "w") as reset_file:
                reset_file.write("#!/usr/bin/env bash\n")

        else:
            os.system('echo "### COUNTER LESS THAN 50 ###"\n')

        # Increment the counter
        counter += 1
        # print(counter)

    if os.path.exists("/hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{2}/run_50_paml_tests_{0}_{1}.sh".format(name_counter, aligner, DATASET_ID)):
        os.system('echo "### OUTSIDE ### hello"\n')
        sbatch_com = f"""
        sbatch --output=/hps/nobackup/goldman/charwest/omega_ai/paml_test_out/loop_%J.out \
                --error=/hps/nobackup/goldman/charwest/omega_ai/paml_test_out/loop_%J.err \
                --time=72:00:00 \
                --cpus-per-task=1 \
                --ntasks=1 \
                --mem=2G \
                --wrap "{conda_com} && /hps/nobackup/goldman/charwest/omega_ai/data/run_scripts_paml/{DATASET_ID}/run_50_paml_tests_{name_counter}_{aligner}.sh"
        """
        os.system(sbatch_com)
        # os.system('rm /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/paml_tests/run_50_paml_tests_*.sh')
