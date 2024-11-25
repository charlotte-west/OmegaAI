#!/usr/local/bin/python

import argparse
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy.stats import gaussian_kde

# Define the dimensions
indel_rates = [0.1, 0.2, 0.3]
tree_divergences = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
aligner_types = ['clustal', 'mafft', 'prankaa', 'prankc']
column_scores = 2004
# string vecs
indel_vec = ['01', '02', '03']
tree_div_vec = ['01', 'base', '03', '04', '05', '06', '07', '08', '09', '1']

aligner_colors = {
    'clustal': '#0072B2',
    'mafft': '#E69F00',
    'prankaa': '#CC79A7',
    'prankc': '#009E73'
}

aligner_names = {
    'clustal': 'Clustal',
    'mafft': 'MAFFT',
    'prankaa': 'PRANKaa',
    'prankc': 'PRANKc'
}

# Create the multidimensional array
scores_array = np.zeros((len(indel_rates), len(tree_divergences), len(aligner_types), column_scores))
# scores_array = np.load("/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/alignment_scores_array.npy")
# scores_array = np.load("/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/alignment_scores_array_SPS.npy")
# scores_array = np.nan_to_num(scores_array)
# scores_array = np.load("/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/fastsp_alignment_scores_array_CS.npy")
scores_array = np.load("/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/fastsp_alignment_scores_array_SPS.npy")


# Create subplot grid
fig, axs = plt.subplots(len(tree_divergences), len(indel_rates), figsize=(12, 10), sharex=True, sharey=True)

# # fill array
# for i, divergence in enumerate(tree_divergences):
#     for j, indel_rate in enumerate(indel_rates):
#         ax = axs[i, j]
#         for k, aligner_type in enumerate(aligner_types):
#             for x in range(column_scores):
#                 if x <= 500:
#                     group = "group_0"
#                 elif (x > 500) & (x < 1002):
#                     group = "group_501"
#                 elif (x >= 1002) & (x <= 1502):
#                     group = "group_1002"
#                 else:
#                     group = "group_1503"
#                 # Get file
#                 file_path = f"/hps/nobackup/goldman/charwest/omega_ai/data/simulations/fastsp_alignment_scores/div{tree_div_vec[i]}_indistNB_indrate{indel_vec[j]}_tips8_posprop05/{group}/CS/{aligner_types[k]}/{x}_score.txt"      
#                 if os.path.exists(file_path):
#                     with open(file_path, 'r') as file:
#                         for line in file:
#                             score_now = float(line.strip())
#                 else:
#                     score_now = np.nan
#                     print(f"empty file detected for /hps/nobackup/goldman/charwest/omega_ai/data/simulations/fastsp_alignment_scores/div{tree_div_vec[i]}_indistNB_indrate{indel_vec[j]}_tips8_posprop05/{group}/CS/{aligner_types[k]}/{x}_score.txt")

#                 scores_array[j,i,k,x] = score_now

#             # Plot
#             scores_for_aligner = scores_array[j, i, k, :]
#             ax.bar(aligner_type, np.mean(scores_for_aligner), yerr=np.std(scores_for_aligner), label=aligner_type)
#         # ax.set_title(f"Indel Rate: {indel_rate}, Divergence: {divergence}")
#         if j == 0:
#             ax.set_ylabel(f"Div: {divergence}")
#         if i == len(tree_divergences) - 1:
#             ax.set_xlabel(f"Indel Rate: {indel_rate}")

##################################
# # Title for the entire plot
# fig.suptitle('Frequency', x=0.5, y=0.95, fontsize=16)

# # Single label for the bottom
# fig.text(0.5, 0.05, 'Score', ha='center', fontsize=14)

# # Move divergence labels to the right side
# for i, divergence in enumerate(tree_divergences):
#     axs[i, -1].set_ylabel(f"Div: {divergence}", rotation=-90, ha='left', va='center')

# # Move indel rate labels to the top
# for j, indel_rate in enumerate(indel_rates):
#     axs[0, j].set_title(f"Indel Rate: {indel_rate}")

# # Simultaneously plot in loop
# for i, divergence in enumerate(tree_divergences):
#     for j, indel_rate in enumerate(indel_rates):
#         ax = axs[i, j]
#         for k, aligner_type in enumerate(aligner_types):
#             scores_for_aligner = scores_array[j, i, k, :]

#             # Check if there are enough non-zero data points
#             if np.count_nonzero(scores_for_aligner) > 1:
#                 density = gaussian_kde(scores_for_aligner)
#                 xs = np.linspace(np.min(scores_for_aligner), np.max(scores_for_aligner), 100)
#                 scaled_density = density(xs) / np.max(density(xs))  # Scale to range [0, 1]
#                 ax.plot(xs, scaled_density, label=aligner_type, color=aligner_colors.get(aligner_type, 'black'))  # Plot the density curve
                
#                 # Fill the area under the density curve
#                 ax.fill_between(xs, 0, scaled_density, color=aligner_colors.get(aligner_type, 'black'), alpha=0.3)
#             else:
#                 # Plot histogram if there are too few data points
#                 hist, bins = np.histogram(scores_for_aligner, bins=20, density=True)
#                 bin_centers = (bins[:-1] + bins[1:]) / 2
#                 ax.plot(bin_centers, hist, label=aligner_type, color=aligner_colors.get(aligner_type, 'black'), alpha=0.8)  # Plot histogram

#         # Hide x-axis labels for all but the bottom row
#         if i != len(tree_divergences) - 1:
#             ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
#         # Set y-axis limits to [0, 1]
#         ax.set_ylim(0, 1)
#         ax.set_xlim(0,1)

# # Adjust layout
# plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.9])
# plt.show()

##################################

# Plot in loop
for i, divergence in enumerate(tree_divergences):
    for j, indel_rate in enumerate(indel_rates):
        ax = axs[i, j]
        for k, aligner_type in enumerate(aligner_types):
            scores_for_aligner = scores_array[j, i, k, :]

            # Check if there are enough non-zero data points
            if np.count_nonzero(scores_for_aligner) > 1:
                density = gaussian_kde(scores_for_aligner)
                xs = np.linspace(np.min(scores_for_aligner), np.max(scores_for_aligner), 100)
                scaled_density = density(xs) / np.max(density(xs))  # Scale to range [0, 1]
                ax.plot(xs, scaled_density, color=aligner_colors.get(aligner_type, 'black'))  # Plot the density curve
                
                # Fill the area under the density curve
                ax.fill_between(xs, 0, scaled_density, label=aligner_names.get(aligner_type, aligner_type), color=aligner_colors.get(aligner_type, 'black'), alpha=0.3)
            else:
                # Plot histogram if there are too few data points
                hist, bins = np.histogram(scores_for_aligner, bins=20, density=True)
                bin_centers = (bins[:-1] + bins[1:]) / 2
                ax.plot(bin_centers, hist, label=aligner_type, color=aligner_colors.get(aligner_type, 'black'), alpha=0.8)  # Plot histogram

        # ax.set_title(f"Indel Rate: {indel_rate}, Divergence: {divergence}")
        if j == 0:
            ax.set_ylabel(f"Div: {divergence}")
        if i == 0:
            ax.set_title(f"Indel Rate: {indel_rate}")
        if i == len(tree_divergences) - 1:
            ax.set_xlabel("Sum of Pairs Score")
        ax.set_ylim(0, 1)  # Set y-axis limits to [0, 1]
        ax.set_xlim(0,1)

# Add legend outside the subplots
# plt.legend(loc='upper center', bbox_to_anchor=(-0.5, -0.1), fancybox=True, shadow=True, ncol=4)
# Create a legend subplot
legend_ax = fig.add_subplot(1, 1, 1)
legend_ax.axis('off')  # Hide the axes of the legend subplot

# Create the legend
handles, labels = axs[0, 0].get_legend_handles_labels()
legend_ax.legend(handles, labels, loc='center', bbox_to_anchor=(0.92, 0.08), fontsize='large', framealpha=1)


plt.tight_layout()
# plt.savefig("/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/alignment_score_gridplot.png")
plt.savefig("/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/fastsp_alignment_score_gridplot_SPS_density_fill_legend_axesnameredo.png")
# plt.savefig("/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/fastsp_alignment_score_gridplot_CS_density_fill_legend_axesnameredo.png")

# Save numpy array
# np.save("/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/fastsp_alignment_scores_array_CS.npy", scores_array)