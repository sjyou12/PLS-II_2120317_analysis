from SVDCalc import SVDCalc
from matplotlib import pyplot as plt
import numpy as np
import re

# important !! : replace file list used for SVD
# object_file_list = ["210317_010", "210319_002", "210317_014", "210317_016", "210317_018", "210317_020", "210318_001", "210318_003", "210319_001", "210318_023", "210318_021", "210318_011", "210318_014", "210318_016"]  # for L3 SVD
object_file_list = ["210319_005", "210319_003", "210317_015", "210317_017", "210317_019", "210317_021", "210318_002", "210318_004", "210318_006", "210318_024", "210318_022", "210318_012", "210318_015", "210318_017"]  # for L1 SVD
singular_show_num = 10
singular_cut_num = 3
# output_file_name = "L3_SVD"
output_file_name = "L1_SVD"

# custom setting, can change
common_svd_file_root = "results/norm_run_avg/"
svd_result_root = "results/svd/"

graph_label = {"210317_009": "G1_L1-0317", "210317_010": "G1_L3-0317", "210317_011": "G1+1a_L3", "210317_012": "G1+1a_L1",
               "210317_014": "G1+1b_L3", "210317_015": "G1+1b_L1", "210317_016": "G1+1c_L3", "210317_017": "G1+1c_L1",
               "210317_018": "G1+1d_L3", "210317_019": "G1+1d_L1", "210317_020": "G1+1e_L3", "210317_021": "G1+1e_L1",
               "210318_001": "G1+1f_L3", "210318_002": "G1+1f_L1", "210318_003": "G1+1g_L3", "210318_004": "G1+1g_L1",
               "210318_005": "G1+1h_L3", "210318_006": "G1+1h_L1", "210318_008": "G1+1i_L3",
               "210318_011": "G1+ethylene_L3", "210318_012": "G1+ethylene_L3",
               "210318_014": "G1+2a_L3", "210318_015": "G1+2a_L1", "210318_016": "G1+2b_L3", "210318_017": "G1+2b_L1",
               "210318_018": "G1_L3-0318", "210318_019": "G1_L1-0318", "210318_021": "G1+1j_L3", "210318_022": "G1+1j_L1",
               "210318_023": "G1+1i_L3", "210318_024": "G1+1i_L1", "210319_001": "G1+1h_L3",
               "210319_002": "G1+1a_L3", "210319_003": "G1+1a_L1", "210319_004": "G1_L3-0319",
               "210319_005": "G1_L1-0319", "210319_007": "G1_L1-0319-7"}

multiple_data_arr = []
energy_list = []
label_list = []
for file_idx, each_file_name in enumerate(object_file_list):
    now_label = graph_label[each_file_name]
    label_list.append(now_label)
    now_read_file_name = each_file_name + "_" + now_label + "_norm_avg.dat"
    now_file_name = common_svd_file_root + now_read_file_name
    # for first file,
    if file_idx == 0:
        with open(now_file_name, 'r') as cnt_line_f:
            first_data = cnt_line_f.readlines()
            num_of_energy = len(first_data) - 1
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
                    multiple_data_arr[data_idx - 1][file_idx] = now_data
    else:
        with open(now_file_name, 'r') as f:
            for data_idx, dataline in enumerate(f):
                if data_idx < 1:
                    print("[successful working] now " + str(file_idx) + "-th file :", each_file_name)
                else:
                    split_data = dataline.split()
                    now_data = float(split_data[1])
                    multiple_data_arr[data_idx - 1][file_idx] = now_data


print(np.shape(multiple_data_arr))
# multiple_data_arr = np.transpose(multiple_data_arr)
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

shot_label_list = []
for each_label in label_list:
    regex_search = re.findall(r"\+.*_", each_label)
    if regex_search:
        now_important = regex_search[0][1:-1]
    else:
        now_important = "G1"
    shot_label_list.append(now_important)
print(shot_label_list)

# MultiRunSVD.plot_left_vec_with_x_val(graph_title="L3 LSV plot", x_val=energy_list)
# MultiRunSVD.plot_right_vec_with_x_text(graph_title="L3 RSV plot", x_text=shot_label_list)
MultiRunSVD.plot_left_vec_with_x_val(graph_title="L1 LSV plot", x_val=energy_list)
MultiRunSVD.plot_right_vec_with_x_text(graph_title="L1 RSV plot", x_text=shot_label_list)

# sVal_file_name = "L3_210319_static_SingVal.dat"
# rsv_file_name = "L3_210319_static_RSV.dat"
# lsv_file_name = "L3_210319_static_LSV.dat"
sVal_file_name = "L1_210319_static_SingVal.dat"
rsv_file_name = "L1_210319_static_RSV.dat"
lsv_file_name = "L1_210319_static_LSV.dat"

sValOutFp = open((svd_result_root + sVal_file_name), 'w')
rsvOutFp = open((svd_result_root + rsv_file_name), 'w')
lsvOutFp = open((svd_result_root + lsv_file_name), 'w')

MultiRunSVD.file_output_singular_value(sValOutFp)
MultiRunSVD.file_output_singular_vectors_with_label(lsvOutFp, rsvOutFp, leftLableName="energy", leftLabel=energy_list, rightLabelName="substrate", rightLabel=shot_label_list)

sValOutFp.close()
rsvOutFp.close()
lsvOutFp.close()