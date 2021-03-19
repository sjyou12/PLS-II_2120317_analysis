import numpy as np
import matplotlib.pyplot as plt
import copy

# object_file_list = ["210318_023", "210318_024"]
object_file_list = ["210319_005"]
# each_run_num_of_points = [71, 81, 71]
each_run_num_of_points = [81]
excluded_idx_dict = {"210318_014": [0], "210318_016": [0], "210318_009": [1]}
# excluded_idx_dict = {}


class EachFileAnal:
    # common setting
    common_file_root = "results/single_file_all_run/"
    file_all_data = []
    file_all_energy = []
    # run_split_data = []
    run_common_energy = []
    # data_origin_name = []
    avg_data = []
    avg_file_out_root = "results/file_run_avg/"

    def __init__(self, now_file_idx, now_file_name, now_num_of_points):
        # avoid accumulated data
        self.run_split_data = []
        self.data_origin_name = []
        self.file_idx = now_file_idx
        self.file_name = now_file_name
        self.num_of_points = now_num_of_points
        self.read_data_from_file()

    def read_data_from_file(self):
        now_file_name = self.common_file_root + self.file_name + ".dat"
        with open(now_file_name, 'r') as cnt_line_f:
            now_energy_list = []
            now_data_list = []
            first_data = cnt_line_f.readlines()
            num_of_energy = len(first_data)
            print("total", num_of_energy, "line length")
            multiple_data_arr = np.zeros((num_of_energy, len(object_file_list)))
            for data_idx, each_data_line in enumerate(first_data):
                if data_idx < 1:
                    print("[successful working] {}-th file read :".format(self.file_idx), self.file_name)
                else:
                    split_data = each_data_line.split()
                    now_energy = float(split_data[0])
                    now_energy_list.append(now_energy)
                    now_data = float(split_data[1])
                    now_data_list.append(now_data)
            self.file_all_data = now_data_list
            self.file_all_energy = now_energy_list

    def run_separation(self):
        now_data_len = len(self.file_all_data)
        now_total_run_cnt = int(now_data_len / self.num_of_points)
        # self.run_common_energy = self.file_all_energy[run_idx * self.num_of_points:(run_idx + 1) * self.num_of_points]
        self.run_common_energy = self.file_all_energy[:self.num_of_points]
        for run_idx in range(now_total_run_cnt):
            self.run_split_data.append(
                self.file_all_data[run_idx * self.num_of_points:(run_idx + 1) * self.num_of_points])
            self.data_origin_name.append(object_file_list[file_idx] + "_run" + str(run_idx + 1))
            # energy value compare between all run
            if run_idx > 0:
                is_all_energy_equal = np.array_equal(self.run_common_energy, (self.file_all_energy[run_idx * self.num_of_points:(run_idx + 1) * self.num_of_points]))
                if not is_all_energy_equal:
                    error_msg = "energy value is wrong in file " + self.file_name + ", run" + str(run_idx + 1)
                    raise RuntimeError(error_msg)

    def each_run_plot(self):
        plt.title("run separate plot" + self.file_name)
        for run_idx, run_data in enumerate(self.run_split_data):
            plt.plot(self.run_common_energy, run_data, label=self.data_origin_name[run_idx], linestyle='-', marker='o', markersize=3)
            plt.axvline(x=self.run_common_energy[np.argmax(run_data)], linestyle=':')
        plt.legend()
        plt.show()

    def average_run(self, excluded_idx=[]):
        what_we_rm = []
        for each_run_idx in excluded_idx:
            what_we_rm.append(self.run_split_data[each_run_idx])

        what_we_avg = copy.deepcopy(self.run_split_data)
        for each_rm_item in what_we_rm:
            what_we_avg.remove(each_rm_item)
        self.avg_data = np.average(what_we_avg, axis=0)

        avg_out_filename = self.avg_file_out_root + self.file_name + "_run_avg.dat"
        with open(avg_out_filename, 'w') as outFp:
            outFp.write("Energy(eV)\tAvg_norm_intensity\n")
            for idx, e_val in enumerate(self.run_common_energy):
                outFp.write("{0}\t{1:0.5f}\n".format(e_val, self.avg_data[idx]))

    def avg_plot(self, cmp_each_run=False):
        plt.title("run average plot" + self.file_name)
        plt.plot(self.run_common_energy, self.avg_data, linestyle='-', marker='o', markersize=3)
        plt.axvline(x=self.run_common_energy[np.argmax(self.avg_data)], linestyle=':')
        if cmp_each_run:
            for run_idx, run_data in enumerate(self.run_split_data):
                plt.plot(self.run_common_energy, run_data, label=self.data_origin_name[run_idx], linestyle='-',
                         alpha=0.7)
        plt.legend()
        plt.show()


for file_idx, (each_file_name, each_num_points) in enumerate(zip(object_file_list, each_run_num_of_points)):
    now_anal = EachFileAnal(now_file_name=each_file_name, now_file_idx=file_idx, now_num_of_points=each_num_points)
    now_anal.run_separation()
    now_anal.each_run_plot()
    if each_file_name in excluded_idx_dict:
        now_anal.average_run(excluded_idx=excluded_idx_dict[each_file_name])
    else:
        now_anal.average_run()
    now_anal.avg_plot(cmp_each_run=True)
