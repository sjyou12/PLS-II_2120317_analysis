from matplotlib import pyplot as plt
import numpy as np
import os

each_run_ratio = []
each_file_ratio = []

# important !! : replace file list used for SVD
object_file_list = ["210319_005", "210319_007"]

# custom setting, can change
raw_file_root = "results/single_file_all_run/"
output_file_root = "results/run_split/"

# use same value in run_info
each_file_step_size = [81, 81, 71]
each_file_run_num = [2, 1, 3]

all_data_arr = []
all_energy_arr = []
for file_idx, each_file_name in enumerate(object_file_list):
    now_file_name = raw_file_root + each_file_name + ".dat"
    now_step_size = each_file_step_size[file_idx]
    now_run_num = each_file_run_num[file_idx]
    # line step_size*run_index+2 ~ step_size*(run_index+1)+1
    for run_idx in range(now_run_num):
        output_file_name = output_file_root + each_file_name + "_run" + str(run_idx + 1) + ".dat"
        start_idx = now_step_size*run_idx + 2
        end_idx = now_step_size*(run_idx + 1) + 1
        # cat(input_file_name).dat | sed - n - e ‘1p’ - e’start, endp’ > input_file_name_run(run_index + 1).dat
        os_inst = "cat " + now_file_name + " | sed -n -e '1p' -e '" + str(start_idx) + "," + str(end_idx) + "p' > " + output_file_name
        print(os_inst)
        os.system(os_inst)

