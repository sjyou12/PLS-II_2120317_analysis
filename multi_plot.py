from matplotlib import pyplot as plt
import numpy as np

# important !! : replace file list used for SVD
# L1_object_file_list = ["210317_012", "210317_015", "210317_017", "210317_019", "210317_021", "210318_002",
#                        "210318_004", "210318_006", "210318_012", "210318_015", "210318_017", "210318_019",
#                        "210318_022", "210318_024"]  # for all L1
# L3_object_file_list = ["210317_010", "210317_011", "210317_014", "210317_016", "210317_018", "210317_020",
#                        "210318_001", "210318_003", "210318_011", "210318_014", "210318_016",
#                        "210318_018", "210318_021", "210318_023", "210319_001"]  # for all L3
L1_object_file_list = ["210318_019",  "210318_022", "210318_024", "210319_003", "210319_005"]  # for all L1

# L1_object_file_list = ["210318_012", "210318_015", "210318_017", "210318_019",
#                        "210318_022", "210318_024", "210319_003", "210319_005"]  # for L1
L3_object_file_list = ["210317_010", "210318_011", "210318_014", "210318_016", "210318_018",
                       "210318_021", "210318_023", "210319_001", "210319_002", "210319_004"]  # for L3

L3_object_file_list = ["210317_010", "210318_018", "210319_004"]  # for only G1 L3
# L1_object_file_list = ["210318_019", "210319_005"]  # for only G1 L1


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

# custom setting, can change
common_file_root = "results/file_run_avg/"
result_out_root = "results/norm_run_avg/"

class AvgCmp:
    l3_standard_idx = 0
    l1_standard_idx = 0

    def __init__(self, l1_list, l3_list):
        self.l1_file_list = l1_list
        self.l3_file_list = l3_list
        self.l1_energy_arr, self.l1_data_arr = self.read_data_from_file(l1_list)
        self.l3_energy_arr, self.l3_data_arr = self.read_data_from_file(l3_list)
        self.each_run_l3_baseline = []
        self.each_run_l1_baseline = []
        self.corrected_l3_data_arr = []
        self.corrected_l1_data_arr = []
        self.norm_l3_data_arr = []
        self.norm_l1_data_arr = []
        self.l3_diff_data_arr = []
        self.l1_diff_data_arr = []

    @staticmethod
    def read_data_from_file(object_file_list):
        all_data_arr = []
        all_energy_arr = []
        for file_idx, each_file_name in enumerate(object_file_list):
            now_file_name = common_file_root + each_file_name + "_run_avg.dat"
            with open(now_file_name, 'r') as cnt_line_f:
                now_energy_list = []
                now_data_list = []
                first_data = cnt_line_f.readlines()
                num_of_energy = len(first_data)
                # print("total", num_of_energy, "line length")
                multiple_data_arr = np.zeros((num_of_energy, len(object_file_list)))
                for data_idx, each_data_line in enumerate(first_data):
                    if data_idx < 1:
                        print("[success] {}-th file read :".format(file_idx), each_file_name)
                    else:
                        split_data = each_data_line.split()
                        now_energy = float(split_data[0])
                        now_energy_list.append(now_energy)
                        now_data = float(split_data[1])
                        now_data_list.append(now_data)
                all_data_arr.append(now_data_list)
                all_energy_arr.append(now_energy_list)
        return all_energy_arr, all_data_arr

    def plot_raw_l1_data(self):
        global graph_label
        for obj_idx, each_obj in enumerate(self.l1_file_list):
            if each_obj in graph_label:
                plt.plot(self.l1_energy_arr[obj_idx], self.l1_data_arr[obj_idx], label=str(graph_label[each_obj]),
                         linestyle='-')
        plt.title("each file plot")
        plt.legend()
        plt.show()

    def plot_raw_l3_data(self):
        global graph_label
        for obj_idx, each_obj in enumerate(self.l3_file_list):
            if each_obj in graph_label:
                plt.plot(self.l3_energy_arr[obj_idx], self.l3_data_arr[obj_idx], label=str(graph_label[each_obj]),
                         linestyle='-')
        plt.title("each file plot")
        plt.legend()
        plt.show()

    def l3_baseline_correction(self):
        baseline_range = [(2.834, 2.836), (2.846, 2.848)]
        # baseline value calculation
        for data_idx, each_data in enumerate(self.l3_data_arr):
            each_range_avg = []
            for range_start, range_end in baseline_range:
                now_energy = self.l3_energy_arr[data_idx]
                now_range_avg = np.average(each_data[now_energy.index(range_start):now_energy.index(range_end)])
                each_range_avg.append(now_range_avg)
            now_baseline = np.average(each_range_avg)
            self.each_run_l3_baseline.append(now_baseline)
            now_corrected = np.subtract(each_data, now_baseline)
            self.corrected_l3_data_arr.append(now_corrected)
        # self.plot_crt_l3_data()

        norm_range_start, norm_range_end = (2.838, 2.844)
        for data_idx, each_data in enumerate(self.corrected_l3_data_arr):
            now_energy = self.l3_energy_arr[data_idx]
            now_norm_val = np.sum(each_data[now_energy.index(norm_range_start):now_energy.index(norm_range_end)])
            now_normalized = np.divide(each_data, now_norm_val)
            self.norm_l3_data_arr.append(now_normalized)
        # self.plot_norm_l3_data()

    def plot_crt_l3_data(self):
        global graph_label
        for obj_idx, each_obj in enumerate(self.l3_file_list):
            if each_obj in graph_label:
                plt.plot(self.l3_energy_arr[obj_idx], self.corrected_l3_data_arr[obj_idx], label=str(graph_label[each_obj]),
                         linestyle='-')
        plt.title("baseline corrected plot")
        plt.legend()
        plt.show()

    def plot_norm_l3_data(self):
        global graph_label
        for obj_idx, each_obj in enumerate(self.l3_file_list):
            if each_obj in graph_label:
                plt.plot(self.l3_energy_arr[obj_idx], self.norm_l3_data_arr[obj_idx], label=str(graph_label[each_obj]),
                         linestyle='-')
        plt.title("normalized plot")
        plt.legend()
        plt.show()

    def file_out_l3_data(self):
        global graph_label
        for obj_idx, each_obj in enumerate(self.l3_file_list):
            outfile_fullname = result_out_root + each_obj + "_" + graph_label[each_obj] + "_norm_avg.dat"
            print("file out at :", outfile_fullname)
            with open(outfile_fullname, 'w') as outFp:
                outFp.write("Energy(eV)\tNorm_avg_intensity\n")
                for idx, int_val in enumerate(self.norm_l3_data_arr[obj_idx]):
                    outFp.write("{0}\t{1:0.5f}\n".format(self.l3_energy_arr[obj_idx][idx], int_val))

    def l1_baseline_correction(self):
        baseline_range = [(3.2, 3.202)]
        # baseline value calculation
        for data_idx, each_data in enumerate(self.l1_data_arr):
            each_range_avg = []
            for range_start, range_end in baseline_range:
                now_energy = self.l1_energy_arr[data_idx]
                now_range_avg = np.average(each_data[now_energy.index(range_start):now_energy.index(range_end)])
                each_range_avg.append(now_range_avg)
            now_baseline = np.average(each_range_avg)
            self.each_run_l1_baseline.append(now_baseline)
            now_corrected = np.subtract(each_data, now_baseline)
            self.corrected_l1_data_arr.append(now_corrected)
        # self.plot_crt_l1_data()

        norm_range_start, norm_range_end = (3.2035, 3.205)
        for data_idx, each_data in enumerate(self.corrected_l1_data_arr):
            now_energy = self.l1_energy_arr[data_idx]
            try:
                now_norm_val = np.sum(each_data[now_energy.index(norm_range_start):now_energy.index(norm_range_end)])
                # norm_start_idx = np.argmin(np.abs(np.subtract(now_energy, norm_range_start)))
                # norm_end_idx = np.argmin(np.abs(np.subtract(now_energy, norm_range_end)))
                # now_norm_val = np.sum(each_data[norm_start_idx:norm_end_idx])
                now_normalized = np.divide(each_data, now_norm_val)
                self.norm_l1_data_arr.append(now_normalized)
            except:
                print("normalization failed in " + graph_label[self.l1_file_list[data_idx]])
        # self.plot_norm_l1_data()

    def plot_crt_l1_data(self):
        global graph_label
        for obj_idx, each_obj in enumerate(self.l1_file_list):
            if each_obj in graph_label:
                plt.plot(self.l1_energy_arr[obj_idx], self.corrected_l1_data_arr[obj_idx], label=str(graph_label[each_obj]))
        plt.title("baseline corrected plot")
        plt.legend()
        plt.show()

    def plot_norm_l1_data(self):
        global graph_label
        for obj_idx, each_obj in enumerate(self.l1_file_list):
            if each_obj in graph_label:
                try:
                    plt.plot(self.l1_energy_arr[obj_idx], self.norm_l1_data_arr[obj_idx], label=str(graph_label[each_obj]))
                except:
                    pass
        plt.title("normalized plot")
        plt.legend()
        plt.show()

    def file_out_l1_data(self):
        for obj_idx, each_obj in enumerate(self.l1_file_list):
            outfile_fullname = result_out_root + each_obj + "_" + graph_label[each_obj] + "_norm_avg.dat"
            print("file out at :", outfile_fullname)
            with open(outfile_fullname, 'w') as outFp:
                outFp.write("Energy(eV)\tNorm_avg_intensity\n")
                for idx, int_val in enumerate(self.norm_l1_data_arr[obj_idx]):
                    outFp.write("{0}\t{1:0.5f}\n".format(self.l1_energy_arr[obj_idx][idx], int_val))

    def diff_with_g1_L3(self):
        standard_g1_L3 = "210317_010"
        self.l3_standard_idx = self.l3_file_list.index(standard_g1_L3)
        print(self.l3_standard_idx)
        standard_data = self.norm_l3_data_arr[self.l3_standard_idx]
        for data_idx, each_data in enumerate(self.norm_l3_data_arr):
            now_diff = np.subtract(each_data, standard_data)
            self.l3_diff_data_arr.append(now_diff)

    def plot_diff_l3_data(self):
        global graph_label
        for obj_idx, each_obj in enumerate(self.l3_file_list):
            if obj_idx == self.l3_standard_idx:
                continue
            if each_obj in graph_label:
                plt.plot(self.l3_energy_arr[obj_idx], self.l3_diff_data_arr[obj_idx], label=str(graph_label[each_obj]))
        plt.title("difference with G1 plot")
        plt.legend()
        plt.show()

    def diff_with_g1_L1(self):
        standard_g1_L1 = "210319_005"
        self.l1_standard_idx = self.l1_file_list.index(standard_g1_L1)
        print(self.l1_standard_idx)
        standard_data = self.norm_l1_data_arr[self.l1_standard_idx]
        for data_idx, each_data in enumerate(self.norm_l1_data_arr):
            now_diff = np.subtract(each_data, standard_data)
            self.l1_diff_data_arr.append(now_diff)

    def plot_diff_l1_data(self):
        global graph_label
        for obj_idx, each_obj in enumerate(self.l1_file_list):
            if obj_idx == self.l1_standard_idx:
                continue
            if each_obj in graph_label:
                plt.plot(self.l1_energy_arr[obj_idx], self.l1_diff_data_arr[obj_idx], label=str(graph_label[each_obj]))
        plt.title("difference with G1 plot")
        plt.legend()
        plt.show()

GrubbsAvgCmp = AvgCmp(l1_list=L1_object_file_list, l3_list=L3_object_file_list)
# GrubbsAvgCmp.plot_raw_l3_data()
GrubbsAvgCmp.plot_raw_l1_data()
# GrubbsAvgCmp.l3_baseline_correction()
GrubbsAvgCmp.l1_baseline_correction()
# GrubbsAvgCmp.plot_norm_l3_data()
# GrubbsAvgCmp.file_out_l3_data()
GrubbsAvgCmp.plot_norm_l1_data()
# GrubbsAvgCmp.file_out_l1_data()
# GrubbsAvgCmp.diff_with_g1_L3()
# GrubbsAvgCmp.plot_diff_l3_data()
GrubbsAvgCmp.diff_with_g1_L1()
GrubbsAvgCmp.plot_diff_l1_data()