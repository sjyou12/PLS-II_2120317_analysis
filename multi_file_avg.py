from matplotlib import pyplot as plt
import numpy as np

each_run_ratio = []
each_file_ratio = []

# important !! : replace file list used for SVD
# object_file_list = ["210317_010", "210318_018", "210319_004"]
object_file_list = ["macrotest_00001"]
out_file_family_name = "macrotest"

# custom setting, can change
common_file_root = "results/single_file_all_run/"
avg_file_out_root = "results/file_run_avg/"

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

for obj_idx, each_obj in enumerate(object_file_list):
    plt.plot(all_energy_arr[obj_idx], all_data_arr[obj_idx], label=str(object_file_list[obj_idx]), linestyle='--', marker='o', markersize=3)
plt.title("each file plot")
plt.legend()
plt.show()

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