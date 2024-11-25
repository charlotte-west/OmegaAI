#!/usr/local/bin/python

import os
from sys import argv
import pandas as pd
import re

###########################################
#####----------- Functions -----------#####
###########################################
def parse_time(time_str):
    # Regular expression to match time formats
    time_regex = re.compile(r'((?P<days>\d+)-)?((?P<hours>\d+):)?(?P<minutes>\d+):(?P<seconds>\d+(\.\d+)?)')
    match = time_regex.match(time_str)
    
    if match:
        days = int(match.group('days')) if match.group('days') else 0
        hours = int(match.group('hours')) if match.group('hours') else 0
        minutes = int(match.group('minutes'))
        seconds = float(match.group('seconds'))
        
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
        return total_seconds
    else:
        raise ValueError("Invalid time format")

def format_seconds(total_seconds):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

def multiply_time(time_str, x):
    total_seconds = parse_time(time_str)
    new_total_seconds = total_seconds * x
    new_time_str = format_seconds(new_total_seconds)
    return new_time_str, new_total_seconds

def extract_and_sum(file_path, pattern):
    total_sum = 0.0
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                decimal_number = float(match.group(1))
                total_sum += decimal_number
    return total_sum

###########################################
#####------------- Main --------------#####
###########################################

###### Read in jobIDs ######
mother_id = argv[1]
if len(argv) > 2 and argv[2]:
    cores = int(argv[2])
else:
    cores = 1

benchmark_path = "/hps/nobackup/goldman/charwest/omega_ai/data/benchmark/{0}".format(mother_id)
# jobid_file_path = "{0}/sim_align_job_ids.txt".format(benchmark_path)
# jobid_file_path = "{0}/tfrec_jobids.txt".format(benchmark_path)
jobid_file_path = "{0}/{1}_paml_jobids.txt".format(benchmark_path, mother_id)
jobids = []
with open(jobid_file_path, "r") as file:
    # Skip the first line
    # next(file)
    # Loop through each line in the file
    for line in file:
        words = line.strip().split()
        jobid = words[-1]
        jobids.append(jobid)

# print(jobids)

###### Run sacct command for each job ID ######
cputimes = []
maxrss_vals = []
for jobid in jobids:
    os.system('sacct --format="Elapsed,MaxRSS,TotalCPU" -j {0} > {1}/{0}_cpu_mem.txt'.format(jobid, benchmark_path))
    # Read job data
    with open('{1}/{0}_cpu_mem.txt'.format(jobid, benchmark_path), "r") as file:
        for line_number, line in enumerate(file):
            # Check if it's the third line
            if line_number == 2:
                components = line.strip().split()
                cputime = components[0]
                cputimes.append(cputime)
                
            if line_number == 3:
                components = line.strip().split()
                maxrss = components[1]
                maxrss_vals.append(maxrss)
                break

###### Remove tmp files ######
os.system("rm {0}/*_cpu_mem.txt".format(benchmark_path))

# ###### Extract INDELible and Clustal times ######
# sim_out_path = "/hps/nobackup/goldman/charwest/omega_ai/sim_out"
# indelible_pattern = r'indelible runtime: (\d+\.\d+)'
# clustal_pattern = r'Clustal runtime: (\d+\.\d+)'
# indelible_times = []
# clustal_times = []

# for jobid in jobids:
#     file = "{0}/{1}_{2}.out".format(sim_out_path, mother_id, jobid)
#     clustal_time = extract_and_sum(file, clustal_pattern)
#     indelible_time = extract_and_sum(file, indelible_pattern)
#     clustal_times.append(clustal_time)
#     indelible_times.append(indelible_time)

###### Get true CPU time ######
# Given CPU multiplied by the number of cores
true_cputime_str = []
true_cputime_s = []
# true_indelible_cpu_s =  [x * cores for x in indelible_times]
# true_clustal_cpu_s = [x * cores for x in clustal_times]

for cputime in cputimes:
    time_str, time_s = multiply_time(cputime, cores)
    true_cputime_str.append(time_str)
    true_cputime_s.append(time_s)

###### Construct and save dataframe ######
# bm_dict = {'jobid': jobids, 'cputime': cputimes, 'true_cputime': true_cputime_str, 'true_cputime_s': true_cputime_s, 'maxRSS': maxrss_vals, 'indelible_s': indelible_times, 'clustal_s': clustal_times, 'true_indelible_s': true_indelible_cpu_s, 'true_clustal_s': true_clustal_cpu_s}
# bm_dict = {'jobid': jobids, 'cputime': cputimes, 'true_cputime': true_cputime_str, 'true_cputime_s': true_cputime_s, 'maxRSS': maxrss_vals}
bm_dict = {'jobid': jobids, 'elapsed_time': cputimes, 'elapsed_time_s': true_cputime_s, 'maxRSS': maxrss_vals}
bm_df = pd.DataFrame(bm_dict)
print(bm_df)
bm_df.to_csv("{0}/paml_elapsedtime_mem_df.csv".format(benchmark_path), index=False)

### Check true cpu vals
# filtered_df = bm_df[(bm_df['true_indelible_s'] + bm_df['true_clustal_s']) > bm_df['true_cputime_s']]

# # Print the filtered DataFrame
# print("non-coherent rows:")
# print(filtered_df)

###### Construct and save dataframe of final totals ######

