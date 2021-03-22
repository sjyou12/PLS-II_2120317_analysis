from matplotlib import pyplot as plt
import numpy as np


each_run_ratio = []
each_file_ratio = []

# important !! : replace file list used for SVD
object_file_list = ["SFM_210321_00002"]
# object_file_list = ["SFM_210319_G1_L3_f25_run_avg", "SFM_210319_G1_1a_L3_f25_run_avg", "SFM_210319_G1_1b_L3_f25_run_avg", "SFM_210319_G1_1c_L3_f25_run_avg"]
# object_file_list = ["210317_021", "210317_019", "210317_017", "210317_015", "210317_012", "210317_009"]
    # L3 ["210317_020", "210317_018", "210317_016", "210317_014", "210317_011", "210317_010"]
    # L1 ["210317_019", "210317_017", "210317_015", "210317_012", "210317_009"]
# each_file_plot = False
each_file_plot = True
each_run_plot = True
# hand_control_ratio = True
hand_control_ratio = False

if hand_control_ratio:
    # each_run_ratio = [1, 1, 14, 14, 14]
    # each_run_ratio = [1, 1.03, 1.05, 1.095, 1.085, 1.085]
    # each_run_ratio = [1,1,1,1,1,1,1,1,1,1,1,1]
    each_run_ratio = [1,1]
    # each_run_ratio = [1.2,1.2,1.2,1.17,1.17,1.17,1.05,1.06,1.06,1,1,1,1.37,1.42,1.8,1.15,1.18,1.22]
    # L3 [1.15,1.15,1.15,1.15,1.13,1.13,1.13,1.06,1.06,1.06,1,1,1,1.5,1.5,1.5,1.48,1.53,1.54]
    # L1 [1.2,1.2,1.2,1.17,1.17,1.17,1.05,1.06,1.06,1,1,1,1.37,1.42,1.8,1.15,1.18,1.22]


else:
    # each_file_ratio = [1, 15]
    # each_file_ratio = [1,1,1,1,1,1,1,1,1]
    each_file_ratio = [1, 1]

step_num_in_command = 71

# custom setting, can change
common_file_root = "results/file_run_avg/" #"results/single_file_all_run/" #change

all_data_arr = []
all_energy_arr = []
for file_idx, each_file_name in enumerate(object_file_list):
    now_file_name = common_file_root + each_file_name + ".dat"
    with open(now_file_name, 'r') as cnt_line_f:
        now_energy_list = []
        now_data_list = []
        first_data = cnt_line_f.readlines()
        num_of_energy = len(first_data)
        print("total", num_of_energy, "line length")
        multiple_data_arr = np.zeros((num_of_energy, len(object_file_list)))
        for data_idx, each_data_line in enumerate(first_data):
            if data_idx < 1:
                print("[successful working] {}-th file read :".format(file_idx), each_file_name)
            else:
                split_data = each_data_line.split()
                now_energy = float(split_data[0])
                now_energy_list.append(now_energy)
                now_data = float(split_data[1])
                now_data_list.append(now_data)
        all_data_arr.append(now_data_list)
        all_energy_arr.append(now_energy_list)

if each_file_plot:
    for obj_idx, each_obj in enumerate(object_file_list):
        plt.plot(all_energy_arr[obj_idx], all_data_arr[obj_idx], label=str(object_file_list[obj_idx]), linestyle='--', marker='o', markersize=3)
    plt.title("each file plot")
    plt.legend()
    plt.show()

each_run_num_of_point = step_num_in_command + 1

run_split_energy = []
run_split_data = []
data_origin_name = []
for file_idx, (each_data, each_energy) in enumerate(zip(all_data_arr, all_energy_arr)):
    now_data_len = len(each_data)
    now_total_run_cnt = int(now_data_len / each_run_num_of_point)
    for run_idx in range(now_total_run_cnt):
        run_split_data.append(all_data_arr[file_idx][run_idx*each_run_num_of_point:(run_idx + 1)*each_run_num_of_point])
        run_split_energy.append(all_energy_arr[file_idx][run_idx * each_run_num_of_point:(run_idx + 1) * each_run_num_of_point])
        data_origin_name.append(object_file_list[file_idx] + "_run" + str(run_idx))
        if not hand_control_ratio:
            each_run_ratio.append(each_file_ratio[file_idx])

if each_run_plot:
    for run_idx, run_data in enumerate(run_split_data):
        # plt.plot(run_split_energy[run_idx], np.multiply(run_data, each_run_ratio[run_idx]), label=data_origin_name[run_idx])
        plt.plot(run_split_energy[run_idx], np.multiply(run_data, each_run_ratio[run_idx]), label=data_origin_name[run_idx], linestyle='-', marker='o', markersize=3)
    plt.title("run separate plot")
    plt.axvline(x=run_split_energy[0][np.argmax(run_split_data[0])], linestyle=':', color='b')
    plt.axvline(x=run_split_energy[-1][np.argmax(run_split_data[-1])], linestyle=':', color='r')
#   plt.axhline(y=0.013, linestyle=':', color='g')
    plt.legend()
    plt.show()

# run_split_data_array = np.array(run_split_data)
# each_run_ratio_arry = np.array(each_run_ratio)
# w_data=run_split_data_array
# for run_idx, run_data in enumerate(run_split_data):
#     w_data[run_idx:] = np.multiply(run_split_data_array[run_idx:], each_run_ratio_arry[run_idx])
#     plt.plot(run_split_energy[run_idx], np.multiply(run_data, each_run_ratio[run_idx]), label=data_origin_name[run_idx], linestyle='-', marker='o', markersize=3)
# run_num=each_run_ratio_arry.size
# w_data=np.sum(w_data, axis=0)
# w_data=np.divide(w_data, run_num)
# plt.plot(run_split_energy[0], w_data, label='average', linestyle='-', marker='o', markersize=3)
# plt.legend()
# plt.show()
