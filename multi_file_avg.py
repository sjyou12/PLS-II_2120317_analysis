from matplotlib import pyplot as plt
import numpy as np

each_run_ratio = []
each_file_ratio = []

# important !! : replace file list used for SVD
# object_file_list = ["SFM_210319_00003", "SFM_210319_00004", "SFM_210319_00008"]
# G1+1a flow 25
# object_file_list = ["SFM_210319_00009", "SFM_210319_00010", "SFM_210319_00011"] + ["SFM_210320_00008"]
object_file_list = ["SFM_210321_00070"]
# object_file_list = ["SFM_210321_00070"]
# object_file_list = ["SFM_210321_00029", "SFM_210321_00030", "SFM_210321_00031"]
# object_file_list = ["SFM_210321_00018"]
# object_file_list = ["SFM_210321_00021"] # special g1


# object_file_list = ["SFM_210319_00015"]
# out_file_family_name = "dummy"
# out_file_family_name = "SFM_210321_00043_G1+1d_G1+1d_10s_L3"
out_file_family_name = "SFM_210321_00070_THF_THF_10s_L3"
# out_file_family_name = "SFM_210321_00067_THF_THF_10s_L1"
# out_file_family_name = object_file_list[0] # special g1

beforeRmPlot = True
dupDataRemove = True
# dupDataRemove = False
avgWithRmVal = True

# custom setting, can change
common_file_root = "results/single_file_all_run/"
avg_file_out_root = "results/file_run_avg/"
# avg_file_out_root = "results/g1_special_analysis/" # special g1

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
                each_energy = float(split_data[0])
                now_energy_list.append(each_energy)
                now_data = float(split_data[1])
                now_data_list.append(now_data)
        all_data_arr.append(now_data_list)
        all_energy_arr.append(now_energy_list)

if beforeRmPlot:
    for obj_idx, each_obj in enumerate(object_file_list):
        plt.plot(all_energy_arr[obj_idx], all_data_arr[obj_idx], label=str(object_file_list[obj_idx]), linestyle='--', marker='o', markersize=3)
    plt.title("each file plot")
    plt.legend()
    plt.show()

all_rm_energy_arr = []
all_rm_data_arr = []

if dupDataRemove:
    for file_idx, each_data in enumerate(all_data_arr):
        each_energy = all_energy_arr[file_idx]
        sub_arr = np.subtract(each_energy[1:] + [0], each_energy)
        same_energy_pos = np.where(sub_arr == 0)[0]
        remove_idx = []
        for each_dup_energy_pos in same_energy_pos:
            front_same_pos = each_dup_energy_pos
            back_same_pos = each_dup_energy_pos + 1
            front_val = each_data[front_same_pos]
            back_val = each_data[back_same_pos]
            before_val = each_data[front_same_pos - 1]
            after_val = each_data[back_same_pos + 1]
            print(before_val, front_val, back_val, after_val)
            front_val_dist = abs(before_val - front_val) + abs(after_val - front_val)
            back_val_dist = abs(before_val - back_val) + abs(after_val - back_val)
            remove_point = None
            if back_val_dist > front_val_dist:
                remove_point = back_same_pos
            else:
                remove_point = front_same_pos
            remove_idx.append(remove_point)

        removed_energy = [v for i, v in enumerate(all_energy_arr[file_idx]) if i not in remove_idx]
        removed_data = [v for i, v in enumerate(each_data) if i not in remove_idx]
        all_rm_energy_arr.append(removed_energy)
        all_rm_data_arr.append(removed_data)

    for obj_idx, each_obj in enumerate(object_file_list):
        plt.plot(all_rm_energy_arr[obj_idx], all_rm_data_arr[obj_idx], label=str(object_file_list[obj_idx]), linestyle='--', marker='o', markersize=3)
    plt.title("each file removed plot")
    plt.legend()
    plt.show()

if avgWithRmVal:
    avg_energy = all_rm_energy_arr[0]
    run_avg_data = np.average(all_rm_data_arr, axis=0)

    avg_out_filename = avg_file_out_root + out_file_family_name + "_run_rm_avg.dat"
    with open(avg_out_filename, 'w') as outFp:
        outFp.write("Energy(eV)\tAvg_norm_intensity\n")
        for idx, e_val in enumerate(avg_energy):
            outFp.write("{0}\t{1:0.5f}\n".format(e_val, run_avg_data[idx]))

    plt.title("run average plot" + out_file_family_name)
    plt.plot(avg_energy, run_avg_data, linestyle='-', marker='o', markersize=3)
    plt.axvline(x=avg_energy[np.argmax(run_avg_data)], linestyle=':')
    for run_idx, run_data in enumerate(all_rm_data_arr):
        plt.plot(avg_energy, run_data, label=object_file_list[run_idx], linestyle='-',
                 alpha=0.7)
    plt.legend()
    plt.show()
else:
    avg_energy = all_energy_arr[0]
    run_avg_data = np.average(all_data_arr, axis=0)

    avg_out_filename = avg_file_out_root + out_file_family_name + "_run_avg.dat"
    with open(avg_out_filename, 'w') as outFp:
        outFp.write("Energy(eV)\tAvg_norm_intensity\n")
        for idx, e_val in enumerate(avg_energy):
            outFp.write("{0}\t{1:0.5f}\n".format(e_val, run_avg_data[idx]))

    plt.title("run average plot" + out_file_family_name)
    plt.plot(avg_energy, run_avg_data, linestyle='-', marker='o', markersize=3)
    plt.axvline(x=avg_energy[np.argmax(run_avg_data)], linestyle=':')
    for run_idx, run_data in enumerate(all_data_arr):
        plt.plot(avg_energy, run_data, label=object_file_list[run_idx], linestyle='-',
                 alpha=0.7)
    plt.legend()
    plt.show()