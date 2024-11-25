#!/usr/local/bin/python
import os
import subprocess

###########################################
#####------------ Functions ----------#####
###########################################
def check_key_in_value(dictionary):
    for key, value in dictionary.items():
        if key not in value:
            print(f"Key '{key}' is not contained within value '{value}'")


###########################################
#####-------------- Main -------------#####
###########################################

# Make dictionary
# dataset_dict = {
#     "div01_indistNB_indrate01_tips8_posprop05" : "2022-12-19-09-04-29_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div01_indistNB_indrate02_tips8_posprop05" : "2023-08-21-13-58-05_div01_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "div01_indistNB_indrate03_tips8_posprop05" : "2023-08-28-15-03-54_div01_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "divbase_indistNB_indrate01_tips8_posprop05" : "2022-12-06-12-42-21_divbase_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "divbase_indistNB_indrate02_tips8_posprop05" : "2022-11-17-16-08-43_divbase_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "divbase_indistNB_indrate03_tips8_posprop05" : "2022-11-29-16-07-55_divbase_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "div03_indistNB_indrate01_tips8_posprop05" : "2022-12-13-21-08-29_div03_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div03_indistNB_indrate02_tips8_posprop05" : "2023-08-21-14-28-05_div03_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "div03_indistNB_indrate03_tips8_posprop05" : "2023-08-28-19-03-17_div03_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "div04_indistNB_indrate01_tips8_posprop05" : "2022-12-07-14-02-39_div04_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div04_indistNB_indrate02_tips8_posprop05" : "2023-08-21-14-15-05_div04_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "div04_indistNB_indrate03_tips8_posprop05" : "2023-08-28-19-03-17_div04_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "div05_indistNB_indrate01_tips8_posprop05" : "2023-01-05-12-23-00_div05_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div05_indistNB_indrate02_tips8_posprop05" : "2023-08-23-10-26-45_div05_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "div05_indistNB_indrate03_tips8_posprop05" : "2023-08-29-15-16-55_div05_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "div06_indistNB_indrate01_tips8_posprop05" : "2023-01-24-12-08-48_div06_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div06_indistNB_indrate02_tips8_posprop05" : "2023-08-23-10-35-34_div06_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "div06_indistNB_indrate03_tips8_posprop05" : "2023-08-30-10-41-30_div06_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "div07_indistNB_indrate01_tips8_posprop05" : "2022-12-12-16-53-24_div07_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div07_indistNB_indrate02_tips8_posprop05" : "2023-08-23-10-35-59_div07_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "div07_indistNB_indrate03_tips8_posprop05" : "2023-08-30-10-42-58_div07_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "div08_indistNB_indrate01_tips8_posprop05" : "2023-01-03-12-15-45_div08_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div08_indistNB_indrate02_tips8_posprop05" : "2023-08-23-10-39-16_div08_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "div08_indistNB_indrate03_tips8_posprop05" : "2023-08-31-14-07-20_div08_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "div09_indistNB_indrate01_tips8_posprop05" : "2022-12-16-14-17-25_div09_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div09_indistNB_indrate02_tips8_posprop05" : "2023-08-24-09-47-28_div09_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "div09_indistNB_indrate03_tips8_posprop05" : "2023-09-04-15-31-17_div09_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "div1_indistNB_indrate01_tips8_posprop05" : "2022-12-17-23-16-16_div1_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div1_indistNB_indrate02_tips8_posprop05" : "2023-08-25-13-48-01_div1_indistNB_indrate02_tips8_posprop05_average_0.5_512_0.001",
#     "div1_indistNB_indrate03_tips8_posprop05" : "2023-09-04-15-32-03_div1_indistNB_indrate03_tips8_posprop05_average_0.5_512_0.001",
#     "prankc_div01_indistNB_indrate01_tips8_posprop05" : "2023-10-26-12-12-08_prankc_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "prankc_divbase_indistNB_indrate01_tips8_posprop05" : "2023-09-08-11-43-40_prankc_divbase_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "prankc_div03_indistNB_indrate01_tips8_posprop05" : "2023-10-27-11-14-02_prankc_div03_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "prankc_div04_indistNB_indrate01_tips8_posprop05" : "2023-10-27-11-14-53_prankc_div04_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "prankc_div05_indistNB_indrate01_tips8_posprop05" : "2023-09-13-17-10-59_prankc_div05_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "prankc_div06_indistNB_indrate01_tips8_posprop05" : "2023-11-05-19-09-06_prankc_div06_indistNB_indrate01_tips8_posprop05_average_0.5_256_0.001",
#     "prankc_div07_indistNB_indrate01_tips8_posprop05" : "2023-11-05-19-09-10_prankc_div07_indistNB_indrate01_tips8_posprop05_average_0.5_256_0.001",
#     "prankc_div08_indistNB_indrate01_tips8_posprop05" : "2023-11-05-18-57-35_prankc_div08_indistNB_indrate01_tips8_posprop05_average_0.5_256_0.001",
#     "prankc_div09_indistNB_indrate01_tips8_posprop05" : "2023-10-27-11-15-48_prankc_div09_indistNB_indrate01_tips8_posprop05_average_0.5_265_0.001_continue",
#     "prankc_div1_indistNB_indrate01_tips8_posprop05" : "2023-10-27-16-24-02_prankc_div1_indistNB_indrate01_tips8_posprop05_average_0.5_192_0.001_continue",
#     "true_div01_indistNB_indrate01_tips8_posprop05" : "2023-09-04-15-33-40_true_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_divbase_indistNB_indrate01_tips8_posprop05" : "2023-08-09-11-42-51_true_divbase_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div03_indistNB_indrate01_tips8_posprop05" : "2023-09-04-15-35-02_true_div03_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div04_indistNB_indrate01_tips8_posprop05" : "2023-09-04-15-36-47_true_div04_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div05_indistNB_indrate01_tips8_posprop05" : "2023-08-08-15-42-10_true_div05_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div06_indistNB_indrate01_tips8_posprop05" : "2023-09-07-10-47-57_true_div06_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div07_indistNB_indrate01_tips8_posprop05" : "2023-09-08-11-45-26_true_div07_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div08_indistNB_indrate01_tips8_posprop05" : "2023-08-10-14-17-21_true_div08_indistNB_indrate01_tips8_posprop05_average_0.5_256_0.001",
#     "true_div09_indistNB_indrate01_tips8_posprop05" : "2023-09-11-10-20-55_true_div09_indistNB_indrate01_tips8_posprop05_average_0.5_256_0.001",
#     "true_div1_indistNB_indrate01_tips8_posprop05" : "2023-09-11-10-19-22_true_div1_indistNB_indrate01_tips8_posprop05_average_0.5_256_0.001",
# }

# dataset_dict = {
#     "true_div01_indistNB_indrate01_tips8_posprop05" : "2023-09-04-15-33-40_true_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_divbase_indistNB_indrate01_tips8_posprop05" : "2023-08-09-11-42-51_true_divbase_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div03_indistNB_indrate01_tips8_posprop05" : "2023-09-04-15-35-02_true_div03_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div04_indistNB_indrate01_tips8_posprop05" : "2023-09-04-15-36-47_true_div04_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div05_indistNB_indrate01_tips8_posprop05" : "2023-08-08-15-42-10_true_div05_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div06_indistNB_indrate01_tips8_posprop05" : "2023-09-07-10-47-57_true_div06_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div07_indistNB_indrate01_tips8_posprop05" : "2023-09-08-11-45-26_true_div07_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div08_indistNB_indrate01_tips8_posprop05" : "2023-08-10-14-17-21_true_div08_indistNB_indrate01_tips8_posprop05_average_0.5_256_0.001",
#     "true_div09_indistNB_indrate01_tips8_posprop05" : "2023-09-11-10-20-55_true_div09_indistNB_indrate01_tips8_posprop05_average_0.5_256_0.001",
#     "true_div1_indistNB_indrate01_tips8_posprop05" : "2023-09-11-10-19-22_true_div1_indistNB_indrate01_tips8_posprop05_average_0.5_256_0.001",
# }

# dataset_dict = {
#     "div01_indistNB_indrate01_tips8_posprop05" : "2022-12-19-09-04-29_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "prankc_div01_indistNB_indrate01_tips8_posprop05" : "2023-10-26-12-12-08_prankc_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "true_div01_indistNB_indrate01_tips8_posprop05" : "2023-09-04-15-33-40_true_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001"
# }

dataset_dict = {
    "div01_indistNB_indrate01_tips8_posprop05" : "2022-12-19-09-04-29_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001"
}

# dataset_dict = {
#     # "div01_indistNB_indrate01_tips8_posprop05" : "2022-12-19-09-04-29_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     # "divbase_indistNB_indrate01_tips8_posprop05" : "2022-12-06-12-42-21_divbase_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     # "div03_indistNB_indrate01_tips8_posprop05" : "2022-12-13-21-08-29_div03_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     # "div04_indistNB_indrate01_tips8_posprop05" : "2022-12-07-14-02-39_div04_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     # "div05_indistNB_indrate01_tips8_posprop05" : "2023-01-05-12-23-00_div05_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     "div06_indistNB_indrate01_tips8_posprop05" : "2023-01-24-12-08-48_div06_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001"
#     # "div07_indistNB_indrate01_tips8_posprop05" : "2022-12-12-16-53-24_div07_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     # "div08_indistNB_indrate01_tips8_posprop05" : "2023-01-03-12-15-45_div08_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
#     # "div09_indistNB_indrate01_tips8_posprop05" : "2022-12-16-14-17-25_div09_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",    
#     # "div1_indistNB_indrate01_tips8_posprop05" : "2022-12-17-23-16-16_div1_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001"
# }

# Shuffle
dataset_dict = {
    "shuffle_div01_indistNB_indrate01_tips8_posprop05" : "2023-06-22-14-20-48_shuffle_div01_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
    "shuffle_divbase_indistNB_indrate01_tips8_posprop05" : "2023-08-07-12-27-22_shuffle_divbase_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
    "shuffle_div03_indistNB_indrate01_tips8_posprop05" : "2023-09-11-10-11-20_shuffle_div03_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
    "shuffle_div04_indistNB_indrate01_tips8_posprop05" : "2023-06-22-14-21-14_shuffle_div04_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
    "shuffle_div05_indistNB_indrate01_tips8_posprop05" : "2023-09-18-10-32-46_shuffle_div05_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
    "shuffle_div06_indistNB_indrate01_tips8_posprop05" : "2023-09-18-10-33-19_shuffle_div06_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
    "shuffle_div07_indistNB_indrate01_tips8_posprop05" : "2023-09-18-10-34-01_shuffle_div07_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
    "shuffle_div08_indistNB_indrate01_tips8_posprop05" : "2023-06-29-01-11-56_shuffle_div08_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",
    "shuffle_div09_indistNB_indrate01_tips8_posprop05" : "2023-09-18-10-34-35_shuffle_div09_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001",    
    "shuffle_div1_indistNB_indrate01_tips8_posprop05" : "2023-09-18-10-34-57_shuffle_div1_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001"
}

# Shuffle (baseline only)
# dataset_dict = {
#     "shuffle_divbase_indistNB_indrate01_tips8_posprop05" : "2023-08-07-12-27-22_shuffle_divbase_indistNB_indrate01_tips8_posprop05_average_0.5_512_0.001"
# }

# Check dictionary
check_key_in_value(dataset_dict)

# Create sbatch file
base_dir = "/hps/nobackup/goldman/charwest/omega_ai/data"

for dataset, model in dataset_dict.items():
    file_path = "{0}/run_scripts_auc/run_{1}.sh".format(base_dir, dataset)
    with open(file_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("#SBATCH --time=24:00:00\n")
        f.write("#SBATCH --ntasks=1\n")        
        f.write("#SBATCH --cpus-per-task=1\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --mem=64G\n")
        f.write(f"#SBATCH -o {base_dir}/run_scripts_auc/{dataset}_%J.out\n")
        f.write(f"#SBATCH -e {base_dir}/run_scripts_auc/{dataset}_%J.err\n")
        f.write("\n")
        f.write("source /hps/software/users/goldman/charwest/miniconda3/bin/activate && conda deactivate && conda activate base\n")
        f.write(f"python /hps/nobackup/goldman/charwest/omega_ai/slurm_cnn_selection/calc_auc.py --dataset_id {dataset} --model {model}\n")


# Execute
# os.system("chmod +x {0}/run_scripts_auc/run_{1}.sh".format(base_dir, dataset))
# os.system("{0}/run_scripts_auc/run_{1}.sh".format(base_dir, dataset))
for dataset, model in dataset_dict.items():
    # Make the script executable
    subprocess.run(["chmod", "+x", "{0}/run_scripts_auc/run_{1}.sh".format(base_dir, dataset)])
    # Execute the script
    subprocess.run(["sbatch", "{0}/run_scripts_auc/run_{1}.sh".format(base_dir, dataset)])