import numpy as np
import argparse
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser(description='give file name to process and plot')
parser.add_argument('-f', '--file', nargs=1, dest='anal_filename',
                    help='enter only file name, path and extension is automatically set')
args = parser.parse_args()

# important !! : replace file save root
common_raw_file_root = "raw_data/"

# custom setting, can change.
cut_file_root = "cut_data/"
default_name = "sample_clear"
result_out_root = "results/single_run/"

raw_data_file = None
processed_data_file = None
default_original_name = "raw_data/" + default_name + ".dat"
default_cut_name = cut_file_root + default_name + "_cut.dat"
outfile_name = None

if args.anal_filename is None:
    print('there is no argument, use default file name : ' + default_name)
    raw_data_file = default_original_name
    processed_data_file = default_cut_name
    outfile_name = default_name
else:
    arg_filename = args.anal_filename[0]
    raw_data_file = common_raw_file_root + arg_filename + '.dat'
    processed_data_file = cut_file_root + arg_filename + '_cut.dat'
    print('read file : ' + raw_data_file)
    outfile_name = arg_filename

os_inst = 'cat ' + raw_data_file + ' | grep -v "#" | grep -v -e "^$" >> ' + processed_data_file
print(os_inst)
os.system(os_inst)

whole_data_arr = []

with open(processed_data_file, 'r') as f:
    for dataline in f:
        split_data = np.fromstring(dataline, dtype=np.float64, sep=' ')
        whole_data_arr.append(split_data)
whole_data_arr = tuple(whole_data_arr)
data_arr_2d = np.vstack(whole_data_arr)

# please use zero-based index
energy_line_idx = 0
I0_line_idx = 4
intensity_line_idx = 7

energy_val_arr = data_arr_2d[:, energy_line_idx]
norm_int = np.divide(data_arr_2d[:, intensity_line_idx], data_arr_2d[:, I0_line_idx])

plt.scatter(energy_val_arr, norm_int)
plt.show()

file_out = True
if file_out:
    outfile_fullname = result_out_root + outfile_name + ".dat"
    outFp = open(outfile_fullname, 'w')
    print("file out at :", outfile_fullname)
    outFp.write("Energy(eV)\tNormalized_intensity\n")
    for idx, e_val in enumerate(energy_val_arr):
        outFp.write("{0}\t{1:0.5f}\n".format(e_val, norm_int[idx]))
