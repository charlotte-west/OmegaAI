#!/usr/local/bin/python
import os
import pandas as pd

###########################################
#####------------ Functions ----------#####
###########################################
# collate all different divergences corresponding to given prefix
def data_collate(basedir, dataset_prefix, indel_rate, aligners, method):
    divs = {'01':0.1, 'base':0.2, '03':0.3, '04':0.4, '05':0.5, '06':0.6, '07':0.7, '08':0.8, '09':0.9, '1':1}
    # divs = ['01', 'base', '03', '04', '05', '06', '07', '08', '09', '1']
    roc_auc_list = []
    pr_auc_list = []
    aligner_list = []
    indel_list = []
    dataset_id_list = []
    div_list = []

    for aligner in aligners:
        for div in divs.keys():
            # Construct file path
            if method == "CNN":
                roc_file_path = "{0}/{4}{1}_indistNB_indrate{2}_tips8_posprop05/{3}/roc_auc.txt".format(basedir, div, indel_rate, aligner, dataset_prefix)
                print(roc_file_path)
                pr_file_path = "{0}/{4}{1}_indistNB_indrate{2}_tips8_posprop05/{3}/pr_auc.txt".format(basedir, div, indel_rate, aligner, dataset_prefix)
            elif method == "PAML":
                roc_file_path = "{0}/{4}{1}_indistNB_indrate{2}_tips8_posprop05/{3}_roc_auc.txt".format(basedir, div, indel_rate, aligner, dataset_prefix)
                print(roc_file_path)
                pr_file_path = "{0}/{4}{1}_indistNB_indrate{2}_tips8_posprop05/{3}_pr_auc.txt".format(basedir, div, indel_rate, aligner, dataset_prefix)

            if os.path.exists(roc_file_path):
                with open(roc_file_path, "r") as f:
                    roc_auc = float(f.read().strip())
            if os.path.exists(pr_file_path):
                with open(pr_file_path, "r") as f:
                    pr_auc = float(f.read().strip())           
            
            roc_auc_list.append(roc_auc)
            pr_auc_list.append(pr_auc)
            aligner_list.append(aligner)
            indel_list.append(indel_rate)
            dataset_id_list.append("{0}{1}_indistNB_indrate{2}_tips8_posprop05".format(dataset_prefix, div, indel_rate))
            div_list.append(divs[div])
    
    df = pd.DataFrame({
        "roc_auc" : roc_auc_list,
        "pr_auc" : pr_auc_list,
        "aligner" : aligner_list,
        "divergence" : div_list,
        "indel_rate" : indel_list,
        "dataset" : dataset_id_list
    })

    return df


###########################################
#####-------------- Main -------------#####
###########################################

# Setup
cnn_res_dir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/model_test_results"
paml_res_dir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/paml_test_results"
save_dir = "/hps/nobackup/goldman/charwest/omega_ai/data/benchmark"
# aligner_list = ["clustal", "mafft", "prankaa", "prankc", "true"]
aligner_list = ["clustal", "mafft", "prankaa", "prankc"]
# aligner_list = ["true"]

# #----------- CNN indel rate 0.1 (baseline) -----------#
# cnn_ind01_df = data_collate(cnn_res_dir, "div", "01", aligner_list, "CNN")
# cnn_ind01_df.to_csv("{0}/cnn_ind01_auc.csv".format(save_dir), index=False)

# #----------- CNN indel rate 0.2 -----------#
# cnn_ind02_df = data_collate(cnn_res_dir, "div", "02", aligner_list, "CNN")
# cnn_ind02_df.to_csv("{0}/cnn_ind02_auc.csv".format(save_dir), index=False)

# #----------- CNN indel rate 0.3 -----------#
# cnn_ind03_df = data_collate(cnn_res_dir, "div", "03", aligner_list, "CNN")
# cnn_ind03_df.to_csv("{0}/cnn_ind03_auc.csv".format(save_dir), index=False)

# #----------- CNN PRANKc -----------#
# cnn_prankc_df = data_collate(cnn_res_dir, "prankc_div", "01", aligner_list, "CNN")
# cnn_prankc_df.to_csv("{0}/cnn_prankc_auc.csv".format(save_dir), index=False)

#----------- CNN true -----------#
# cnn_true_df = data_collate(cnn_res_dir, "true_div", "01", ["true"], "CNN")
# cnn_true_df.to_csv("{0}/cnn_true_auc.csv".format(save_dir), index=False)


# #----------- PAML indel rate 0.1 (baseline) -----------#
# paml_ind01_df = data_collate(paml_res_dir, "div", "01", aligner_list, "PAML")
# paml_ind01_df.to_csv("{0}/paml_ind01_auc.csv".format(save_dir), index=False)

# #----------- PAML indel rate 0.2 -----------#
# paml_ind02_df = data_collate(paml_res_dir, "div", "02", aligner_list, "PAML")
# paml_ind02_df.to_csv("{0}/paml_ind02_auc.csv".format(save_dir), index=False)

# #----------- PAML indel rate 0.3 -----------#
# paml_ind03_df = data_collate(paml_res_dir, "div", "03", aligner_list, "PAML")
# paml_ind03_df.to_csv("{0}/paml_ind03_auc.csv".format(save_dir), index=False)

#----------- PAML true -----------#
# paml_true_df = data_collate(paml_res_dir, "true_div", "01", ["true"], "PAML")
# paml_true_df.to_csv("{0}/paml_true_auc.csv".format(save_dir), index=False)

#----------- Shuffle (baseline) -----------#
# cnn_ind01_df = data_collate(cnn_res_dir, "shuffle_div", "01", aligner_list, "CNN")
# cnn_ind01_df.to_csv("{0}/cnn_shuffle_auc.csv".format(save_dir), index=False)

#----------- Modeldiv05 -----------#
# modeldiv05_cnn_ind01_df = data_collate(cnn_res_dir, "modeldiv05_div", "01", aligner_list, "CNN")
# modeldiv05_cnn_ind01_df.to_csv("{0}/modeldiv05_cnn_ind01_auc.csv".format(save_dir), index=False)

# #----------- PAMLdiv05 -----------#
pamldiv05_ind01_df = data_collate(paml_res_dir, "pamldiv05_div", "01", aligner_list, "PAML")
pamldiv05_true_ind01_df = data_collate(paml_res_dir, "pamldiv05_true_div", "01", ["true"], "PAML")
pamldiv05_df = pd.concat([pamldiv05_ind01_df, pamldiv05_true_ind01_df])

pamldiv05_df.to_csv("{0}/pamldiv05_ind01_auc.csv".format(save_dir), index=False)

