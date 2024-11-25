#!/usr/local/bin/python

from audioop import avg
import os
from sys import argv
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

###########################################
#####---------- Functions ------------#####
###########################################

# Define a function to remove 'K' and convert to numbers
def convert_to_number(value):
    return int(value.replace('K', ''))

def convert_to_kilobytes(value):
    multiplier = {'G': 1024*1024, 'M': 1024, 'K': 1}
    if value[-1] in multiplier:
        return float(value[:-1]) * multiplier[value[-1]]
    elif value[-1].isdigit():
        return float(value) / 1024  # Assume value is in bytes
    else:
        return float(value)

###########################################
#####------------- Main --------------#####
###########################################

benchmark_path = "/hps/nobackup/goldman/charwest/omega_ai/data/benchmark"

###########################################
#####---------- CPU stuff ------------#####
###########################################

# Concat tfrec
tfrec_df_v4 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v4/tfrec_cpu_mem_df.csv".format(benchmark_path), header=0)
tfrec_df_v5 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v5/tfrec_cpu_mem_df.csv".format(benchmark_path), header=0)
tfrec_df_v6 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v6/tfrec_cpu_mem_df.csv".format(benchmark_path), header=0)

sum_filtered_tfrec_df_v4 = pd.DataFrame({
    'tfrec_cputime_s': [tfrec_df_v4['true_cputime_s'].sum()]
})
sum_filtered_tfrec_df_v5 = pd.DataFrame({
    'tfrec_cputime_s': [tfrec_df_v5['true_cputime_s'].sum()]
})
sum_filtered_tfrec_df_v6 = pd.DataFrame({
    'tfrec_cputime_s': [tfrec_df_v6['true_cputime_s'].sum()]
})
concat_tfrec_cpu_df = pd.concat([sum_filtered_tfrec_df_v4,sum_filtered_tfrec_df_v5,sum_filtered_tfrec_df_v6])
avg_tfrec_cpu_vals = concat_tfrec_cpu_df.mean()
avg_tfrec_cpu_df = pd.DataFrame(avg_tfrec_cpu_vals).transpose()

# Concat sim+align
sim_df_v4 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v4/cpu_mem_df.csv".format(benchmark_path), header=0)
sim_df_v5 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v5/cpu_mem_df.csv".format(benchmark_path), header=0)
sim_df_v6 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v6/cpu_mem_df.csv".format(benchmark_path), header=0)

# filtered_sim_df_v4 = sim_df_v4[["true_cputime_s", "true_clustal_s", "true_indelible_s"]]
# filtered_sim_df_v5 = sim_df_v5[["true_cputime_s", "true_clustal_s", "true_indelible_s"]]
# filtered_sim_df_v6 = sim_df_v6[["true_cputime_s", "true_clustal_s", "true_indelible_s"]]

sum_filtered_sim_df_v4 = pd.DataFrame({
    'true_cputime_s': [sim_df_v4['true_cputime_s'].sum()],
    'true_clustal_s': [sim_df_v4['true_clustal_s'].sum()],
    'true_indelible_s': [sim_df_v4['true_indelible_s'].sum()]
})
sum_filtered_sim_df_v5 = pd.DataFrame({
    'true_cputime_s': [sim_df_v5['true_cputime_s'].sum()],
    'true_clustal_s': [sim_df_v5['true_clustal_s'].sum()],
    'true_indelible_s': [sim_df_v5['true_indelible_s'].sum()]
})
sum_filtered_sim_df_v6 = pd.DataFrame({
    'true_cputime_s': [sim_df_v6['true_cputime_s'].sum()],
    'true_clustal_s': [sim_df_v6['true_clustal_s'].sum()],
    'true_indelible_s': [sim_df_v6['true_indelible_s'].sum()]
})
print(sum_filtered_sim_df_v4)
print(sum_filtered_sim_df_v5)
print(sum_filtered_sim_df_v6)

concat_sim_align_cpu_df = pd.concat([sum_filtered_sim_df_v4,sum_filtered_sim_df_v5,sum_filtered_sim_df_v6])
avg_sim_align_cpu_vals = concat_sim_align_cpu_df.mean()
avg_sim_align_cpu_df = pd.DataFrame(avg_sim_align_cpu_vals).transpose()
print(avg_sim_align_cpu_df)

# Read in other CPU times
# other_cpu_dict = {"file_splits": [47,77,84], "train": [53075,53075,53075], "cnn_test": [22.493,23.890,23.766]} # subject to change
# other_mem_dict = {"file_splits": [131604,173976,164076], "train": [3961912,4084288,4093888], "cnn_test": [96,84,116]} # subject to change
other_cpu_dict = {"file_splits": [47,77,84], "train": [35392,48404,53075], "cnn_test": [22.493,23.890,23.766]} # New train data is from 61926022,61926081,60192087
other_mem_dict = {"file_splits": [131604,173976,164076], "train": [3347080,3314900,3340864], "cnn_test": [96,84,116]} # New train data is from 61926022,61926081,60192087
total_train_dict = {"elapsed_train_time": [118866,158682,172091]}
gpu_util_dict = {"gpu_util": [78,46,75]}

other_cpu_df = pd.DataFrame(other_cpu_dict)
other_mem_df = pd.DataFrame(other_mem_dict)

avg_other_cpu_vals = other_cpu_df.mean()
avg_other_cpu_df = pd.DataFrame(avg_other_cpu_vals).transpose()
avg_cpu_int_df = pd.concat([avg_sim_align_cpu_df, avg_other_cpu_df, avg_tfrec_cpu_df], axis=1)
print(avg_cpu_int_df)

# with avg_cpu_int_df make a new dataframe with new cols and only cols you want for plotting
avg_cpu_df = avg_cpu_int_df.copy()
avg_cpu_df['house_keeping_s'] = avg_cpu_df['true_cputime_s'] + avg_cpu_df['file_splits'] - avg_cpu_df['true_clustal_s'] - avg_cpu_df['true_indelible_s']
avg_cpu_df.drop(columns=['true_cputime_s', 'file_splits', 'cnn_test'], inplace=True)
print(avg_cpu_df)

# Change col order and change to cpu hours instead of seconds
avg_cpu_hours_df = pd.DataFrame({
    'setup': avg_cpu_df['house_keeping_s'] / (60 ** 2),
    'simulation': avg_cpu_df['true_indelible_s'] / (60 ** 2),
    'alignment': avg_cpu_df['true_clustal_s'] / (60 ** 2),
    'transform': avg_cpu_df['tfrec_cputime_s'] / (60 ** 2),
    'train': avg_cpu_df['train'] / (60 ** 2)
})
print(avg_cpu_hours_df)

### Plotting
# Calculate the summation of all columns except the last one
# total_sum = avg_cpu_hours_df.iloc[:, :-1].sum()

# Plot the DataFrame as a stacked bar plot without the 'Total' row
# avg_cpu_hours_df.drop('Total', errors='ignore').plot(kind='bar', stacked=True, figsize=(10, 6))


###############################################################
# # Manually add the final stacked bar for the total summation
# plt.figure()
# plt.bar(x=list(avg_cpu_hours_df.columns), height=avg_cpu_hours_df.values.flatten())

# plt.xlabel('Categories')
# plt.ylabel('CPU Hours')
# plt.title('CPU Hours')
# plt.xticks(rotation=0)
# # plt.legend(title='Columns')
# # plt.show()
# plt.savefig("{0}/cputime_res.png".format(benchmark_path))
###############################################################

###########################################
#####------- Test Time Elapsed -------#####
###########################################
paml_test_time_df_v4 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v4/paml_elapsedtime_mem_df.csv".format(benchmark_path), header=0)
paml_test_time_df_v5 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v5/paml_elapsedtime_mem_df.csv".format(benchmark_path), header=0)
paml_test_time_df_v6 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v6/paml_elapsedtime_mem_df.csv".format(benchmark_path), header=0)

other_test_dict = {"cnn_test_cpu": [149,133,130], "cnn_test_cpu_gpu": [32,32,31]} # subject to change
other_test_mem_dict = {"cnn_test_cpu": [2035692,2043424,1652604], "cnn_test_cpu_gpu": [2808948,2818976,2648388]}
other_test_df = pd.DataFrame(other_test_dict)
other_test_vals = other_test_df.mean()
avg_other_test_df = pd.DataFrame(other_test_vals).transpose()

sum_paml_test_time_df_v4 = pd.DataFrame({
    'elapsed_time_s': [paml_test_time_df_v4['elapsed_time_s'].sum()]
})
sum_paml_test_time_df_v5 = pd.DataFrame({
    'elapsed_time_s': [paml_test_time_df_v5['elapsed_time_s'].sum()]
})
sum_paml_test_time_df_v6 = pd.DataFrame({
    'elapsed_time_s': [paml_test_time_df_v6['elapsed_time_s'].sum()]
})
concat_paml_time_df = pd.concat([sum_paml_test_time_df_v4,sum_paml_test_time_df_v5,sum_paml_test_time_df_v6])
avg_paml_time_vals = concat_paml_time_df.mean()
paml_test_time_df = pd.DataFrame(avg_paml_time_vals).transpose()

test_time_df = pd.concat([paml_test_time_df, avg_other_test_df], axis=1)
log_test_time_df = np.log(test_time_df)
print(log_test_time_df)


###########################################
#####--------- Memory stuff ----------#####
###########################################
# Need max memory for sim+align and file splits (the max of both of their maxs that is).
sim_align_mem_vals_4 = sim_df_v4['maxRSS'].apply(convert_to_kilobytes).values
sim_align_mem_vals_5 = sim_df_v5['maxRSS'].apply(convert_to_kilobytes).values
sim_align_mem_vals_6 = sim_df_v6['maxRSS'].apply(convert_to_kilobytes).values
sim_align_mem_vals = sim_align_mem_vals_4 + sim_align_mem_vals_5 + sim_align_mem_vals_6
maxrss_sim_align_split = max(max(sim_align_mem_vals), max(other_mem_dict['file_splits']))
print("MaxRSS for simulation, alignment and filesplits is: {0}".format(maxrss_sim_align_split))

# Max mem for transform
tfrec_mem_vals_4 = tfrec_df_v4['maxRSS'].apply(convert_to_kilobytes).values
tfrec_mem_vals_5 = tfrec_df_v5['maxRSS'].apply(convert_to_kilobytes).values
tfrec_mem_vals_6 = tfrec_df_v6['maxRSS'].apply(convert_to_kilobytes).values
tfrec_mem_vals = tfrec_mem_vals_4 + tfrec_mem_vals_5 + tfrec_mem_vals_6
maxrss_tfrec = max(tfrec_mem_vals)
print("MaxRSS for converting to tfrecord format is: {0}".format(maxrss_tfrec))

# Max mem for train
maxrss_train = max(other_mem_dict['train'])
print("MaxRSS for training is: {0}".format(maxrss_train))

# Max mem for PAML test
paml_test_mem_vals_4 = paml_test_time_df_v4['maxRSS'].apply(convert_to_kilobytes).values
paml_test_mem_vals_5 = paml_test_time_df_v5['maxRSS'].apply(convert_to_kilobytes).values
paml_test_mem_vals_6 = paml_test_time_df_v6['maxRSS'].apply(convert_to_kilobytes).values
paml_test_mem_vals = paml_test_mem_vals_4 + paml_test_mem_vals_5 + paml_test_mem_vals_6
maxrss_paml_test = max(paml_test_mem_vals)
print("MaxRSS for PAML test is: {0}".format(maxrss_paml_test))

# Max mem for CNN test CPU only
maxrss_cnn_test_cpu = max(other_test_mem_dict['cnn_test_cpu'])
print("MaxRSS for CNN test CPU only is: {0}".format(maxrss_cnn_test_cpu))

# Max mem for CNN test CPU+GPU
maxrss_cnn_test_cpu_gpu = max(other_test_mem_dict['cnn_test_cpu_gpu'])
print("MaxRSS for CNN test CPU+GPU is: {0}".format(maxrss_cnn_test_cpu_gpu))

# GPU mem for train
# train_gpu_mem = 

# GPU mem for CNN test CPU+GPU
# cnn_test_gpu_mem = 

# Collate memory stuff into dfs:
# maxrss_df = pd.DataFrame({
#     'setup': maxrss_sim_align_split,
#     'simulation': maxrss_sim_align_split,
#     'alignment': maxrss_sim_align_split,
#     'transform': maxrss_tfrec,
#     'train': maxrss_train
# }, index=[0,1,2,3,4])
maxrss_df = pd.DataFrame({
    'setup': maxrss_sim_align_split / (1024 ** 2),
    'simulation': maxrss_sim_align_split / (1024 ** 2),
    'alignment': maxrss_sim_align_split / (1024 ** 2),
    'transform': maxrss_tfrec / (1024 ** 2),
    'train': maxrss_train / (1024 ** 2)
}, index=[0])

print(maxrss_df)

###########################################
#####------------- Plot --------------#####
###########################################

################# PLOT 1 #################
# Create figure and axis objects
fig, ax1 = plt.subplots()

# Plot bars for CPU hours
bar_width = 0.35
categories = list(avg_cpu_hours_df.columns)

# Plot all bars for CPU hours
for i, category in enumerate(categories):
    ax1.bar(i - bar_width / 2, avg_cpu_hours_df.iloc[:, i], bar_width, label=category, color='#296E85')

# Plot extra train bar
additional_value = np.mean(total_train_dict['elapsed_train_time']) / (60 ** 2)  # mean total time in hours
additional_train_bar = ax1.bar(len(categories) - 1 + bar_width / 2, additional_value, bar_width, color='#43A6C6', label='train')

# Set the labels and title for the first y-axis
# ax1.set_xlabel('Categories')
ax1.set_ylabel('Hours', color='#296E85')
ax1.tick_params(axis='y', labelcolor='#296E85')

# Create a second y-axis for maxRSS
ax2 = ax1.twinx()

# Plot bars for maxRSS
for i, category in enumerate(categories[:-1]):
    ax2.bar(i + bar_width / 2, maxrss_df.iloc[:, i], bar_width, label=category, color='#D37506')

# Plot extra maxrss train bar to accommodate
add_maxrss_train = ax2.bar(len(categories) - 1 + 1.5*bar_width , maxrss_df.iloc[:,-1], bar_width, label='train', color='#D37506')

# Set the labels and title for the second y-axis
ax2.set_ylabel('Memory (GB)', color='#D37506')
ax2.tick_params(axis='y', labelcolor='#D37506')

# Set x-axis ticks and labels
ax1.set_xticks(range(len(categories)))
ax1.set_xticklabels(categories)

# Add legend
# lines, labels = ax1.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()
# ax1.legend(lines + lines2, labels + labels2, loc='upper left')
leg_colours = ['#296E85', '#43A6C6', '#D37506']
leg_labels = ['CPU hours', 'Elapsed hours (with GPU)', 'Memory']

# Create the custom legend handles
legend_handles = [mpatches.Patch(color=color, label=label) for color, label in zip(leg_colours, leg_labels)]
plt.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.0, 1.15), ncol=2)

# Save the plot
plt.savefig("{0}/cputime_maxrss_res.png".format(benchmark_path))

################# PLOT 2 #################
# Construct dataframes
elapsed_test_df = pd.DataFrame({
    'CODEML': test_time_df.values.flatten()[0],
    'OmegaAI CPU only': test_time_df.values.flatten()[1],
    'OmegaAI CPU+GPU': test_time_df.values.flatten()[2]
}, index=[0])
print(elapsed_test_df)
# elapsed_test_df.to_csv("{0}/elapsed_test_time.csv".format(benchmark_path), index=False)

maxrss_test_df = pd.DataFrame({
    'CODEML': maxrss_paml_test / (1024 ** 2),
    'OmegaAI CPU only': maxrss_cnn_test_cpu / (1024 ** 2),
    'OmegaAI CPU+GPU': maxrss_cnn_test_cpu_gpu / (1024 ** 2)
}, index=[0])
# maxrss_test_df.to_csv("{0}/test_memory.csv".format(benchmark_path), index=False)

fig2, ax3 = plt.subplots()

# Plot bars for CPU hours
bar_width = 0.4
categories = list(elapsed_test_df.columns)

# Plot all bars for elapsed time seconds (log)
for i, category in enumerate(categories):
    ax3.bar(i - bar_width / 2, elapsed_test_df.iloc[:, i], bar_width, label=category, color='#43A6C6')

# Set the labels and title for the first y-axis
# ax3.set_xlabel('Categories')
ax3.set_ylabel('Elapsed Time (s)', color='#43A6C6')
ax3.tick_params(axis='y', labelcolor='#43A6C6')
ax3.set_yscale('log')

# Create a second y-axis for maxRSS
ax4 = ax3.twinx()

# Plot bars for maxRSS
for i, category in enumerate(categories):
    ax4.bar(i + bar_width / 2, maxrss_test_df.iloc[:, i], bar_width, label=category, color='#D37506')

# Set the labels and title for the second y-axis
ax4.set_ylabel('Memory (GB)', color='#D37506')
ax4.tick_params(axis='y', labelcolor='#D37506')

# Set x-axis ticks and labels
ax3.set_xticks(range(len(categories)))
ax3.set_xticklabels(categories)

leg_colours = ['#43A6C6', '#D37506']
leg_labels = ['Elapsed time', 'Memory']

# Create the custom legend handles
legend_handles = [mpatches.Patch(color=color, label=label) for color, label in zip(leg_colours, leg_labels)]
plt.legend(handles=legend_handles, loc='upper center')

# Save the plot
plt.savefig("{0}/log_test_elapsed_time.png".format(benchmark_path))



###########################################
# # Create figure and axis objects
# fig, ax = plt.subplots()

# # Plot bars
# bar_width = 0.35
# categories = list(avg_cpu_hours_df.columns)

# # Plot all bars except the 'train' and 'additional' bars
# for i, category in enumerate(categories[:-1]):
#     ax.bar(i, avg_cpu_hours_df.iloc[:, i], bar_width, color='blue')#, label=category)

# # Plot the 'train' bar
# train_bar = ax.bar(len(categories) - 1, avg_cpu_hours_df.iloc[:, -1], bar_width, color='blue')#, label='train')

# # Add a bar to the right side of the 'train' bar
# additional_value = np.mean(total_train_dict['elapsed_train_time']) / (60 ** 2)  # mean total time in hours
# additional_bar = ax.bar(len(categories) - 1 + bar_width, additional_value, bar_width, color='red', label='additional')

# # Set labels and title
# ax.set_xlabel('Categories')
# ax.set_ylabel('CPU Hours')
# ax.set_title('CPU Hours')
# ax.set_xticks(range(len(categories)))
# ax.set_xticklabels(categories)

# # Save the plot
# plt.savefig("{0}/cputime_res_withtraintime.png".format(benchmark_path))

###########################################
#####------------ Archive ------------#####
###########################################

# plt.figure()
# plt.bar(x=["PAML", "OmegaAI CPU only", "OmegaAI CPU+GPU"], height=log_test_time_df.values.flatten())

# plt.xlabel('Test Methods')
# plt.ylabel('Elapsed Timed (log(s))')
# plt.title('Methods at Test Time')
# plt.xticks(rotation=0)
# # plt.legend(title='Columns')
# # plt.show()
# plt.savefig("{0}/log_test_elapsed_time.png".format(benchmark_path))



# avg_other_mum_vals = other_mem_df.mean()
# avg_other_mem_df = pd.DataFrame(avg_other_mum_vals).transpose()

# # Concat paml test
# paml_test_df_v4 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v4/paml_cpu_mem_df.csv".format(benchmark_path), header=0)
# paml_test_df_v5 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v5/paml_cpu_mem_df.csv".format(benchmark_path), header=0)
# paml_test_df_v6 = pd.read_csv("{0}/bm_divbase_indistNB_indrate01_tips8_posprop05_v6/paml_cpu_mem_df.csv".format(benchmark_path), header=0)

## Separate CPU and memory dfs, combine with other data
# Dataframe with housekeeping, sim, align, tfrec and train CPU
# Dataframe with housekeeping, sim, align, tfrec and train memory
# Dataframe with omegaAI and PAML test CPU
# Dataframe with omegaAI and PAML test memory