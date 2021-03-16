from SVDCalc import SVDCalc
from matplotlib import pyplot as plt
import numpy as np

# important !! : replace file list used for SVD
object_file_list = ["sample_2", "sample_3"]
singular_show_num = 2
singular_cut_num = 1

# custom setting, can change
common_svd_file_root = "results/single_run/"
svd_result_root = "results/mutli_SVD/"



multiple_data_arr = []
energy_list = []
for file_idx, each_file_name in enumerate(object_file_list):
    now_file_name = common_svd_file_root + each_file_name + ".dat"
    # for first file,
    if file_idx == 0:
        with open(now_file_name, 'r') as cnt_line_f:
            first_data = cnt_line_f.readlines()
            num_of_energy = len(first_data)
            print("total", num_of_energy, "line length")
            multiple_data_arr = np.zeros((num_of_energy, len(object_file_list)))
            for data_idx, each_data_line in enumerate(first_data):
                if data_idx < 1:
                    print("[successful working] first (0-th) file (become standard) :", each_file_name)
                else:
                    split_data = each_data_line.split()
                    now_energy = float(split_data[0])
                    energy_list.append(now_energy)
                    now_data = float(split_data[1])
                    multiple_data_arr[data_idx][file_idx] = now_data
    else:
        with open(now_file_name, 'r') as f:
            for data_idx, dataline in enumerate(f):
                if data_idx < 1:
                    print("[successful working] now " + str(file_idx) + "-th file :", each_file_name)
                else:
                    split_data = dataline.split()
                    now_data = float(split_data[1])
                    multiple_data_arr[data_idx][file_idx] = now_data


print(np.shape(multiple_data_arr))
multiple_data_arr = np.transpose(multiple_data_arr)
MultiRunSVD = SVDCalc(multiple_data_arr)
nowSingVal = MultiRunSVD.calc_svd()
print(nowSingVal)

print(nowSingVal[:singular_show_num])
singular_data_y = nowSingVal[:singular_show_num]
singular_data_y_log = np.log(singular_data_y)
singular_data_x = range(1, len(singular_data_y) + 1)


def plot_singular_value(data_x, data_y, data_y_log):
    color_r = 'tab:red'
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("index of singular value")
    ax1.set_ylabel("singular value", color=color_r)
    ax1.scatter(data_x, data_y, color=color_r)
    ax1.plot(data_x, data_y, color=color_r)
    ax1.tick_params(axis='y', labelcolor=color_r)

    ax2 = ax1.twinx()
    color_b = 'tab:blue'
    ax2.set_ylabel("log scale singular value", color=color_b)
    ax2.scatter(data_x, data_y_log, color=color_b)
    ax2.plot(data_x, data_y_log, color=color_b)
    ax2.tick_params(axis='y', labelcolor=color_b)

    fig.tight_layout()
    plt.show()


plot_singular_value(singular_data_x, singular_data_y, singular_data_y_log)

bigSingVal = nowSingVal[:singular_cut_num]
print(bigSingVal)

print("left", MultiRunSVD.leftVec.shape)
print("right", MultiRunSVD.rightVecTrans.shape)
MultiRunSVD.pick_meaningful_data(singular_cut_num)
print("left", MultiRunSVD.meanLeftVec.shape)
print("right", MultiRunSVD.meanRightVec.shape)
MultiRunSVD.plot_left_Vec()
MultiRunSVD.plot_right_Vec()