import csv
import matplotlib.pyplot as plt
import os, sys
import numpy as np
import h5py
import seaborn as sns
from timeit import default_timer as timer
from datetime import timedelta
from collections import defaultdict


def plot_multi_states(shepherd_state, N_sheep, Iterations):
    plt.figure(figsize=(8, 6), dpi=300)
    N_shepherd = shepherd_state.shape[0]
    x = [item * 0.01 for item in range(Iterations)]
    # subplot shepherd state
    for shepherd_index in range(N_shepherd):
        # print(shepherd_index)
        plt.subplot(N_shepherd + 1, 1, shepherd_index + 1)
        y = shepherd_state[shepherd_index, 0:Iterations]  # 1.0  drive_mode_true
        plt.plot(x, y, 'b-')
        plt.ylabel("Shepherd" + str(shepherd_index))
        if shepherd_index == 0:
            plt.title("N_shepherd=" + str(N_shepherd) + "_N_sheep=" + str(N_sheep) + "_Final_tick=" + str(Iterations))
    # subplot difference state
    difference = np.zeros(Iterations)
    for index in range(Iterations):
        if sum(shepherd_state[:, index]) != 0 and sum(shepherd_state[:, index]) != N_shepherd:
            difference[index] = 1
    print("difference:", sum(difference))
    plt.subplot(N_shepherd + 1, 1, N_shepherd + 1)
    plt.plot(x, difference, 'r-')
    plt.ylabel("difference")
    plt.xlabel("Time (s)")
    # plt.savefig("./figures/state_of_shepherd=" + str(N_shepherd)+"_N_sheep="+str(N_sheep) + ".png")
    plt.show()
    return

#calculate coordination time when shepherds are in different state;
def calculate_differ_states(shepherd_state):
    N_shepherd = shepherd_state.shape[0]
    Iterations = shepherd_state.shape[1]
    difference = np.zeros(Iterations)
    for index in range(Iterations):
        if sum(shepherd_state[:, index]) != 0 and sum(shepherd_state[:, index]) != N_shepherd:
            difference[index] = 1
    value = sum(difference)
    # print("difference:", value)
    return value


def read_hdf5_data(path):
    with h5py.File(path, "r") as f:
        # print(f.keys())
        agents = f.get("agent_data")[:]
        shepherd = f.get("shepherd_data")[:]
        agents_num = agents.shape[0]
        shepherd_num = shepherd.shape[0]
        agents_pos = agents[:, 0:2, :]
        agents_state = agents[:, 3, :]
        shepherd_pos = shepherd[:, 0:2, :]
        shepherd_state = shepherd[:, 3, :]
        # print("shepherd_state", shepherd_state.shape)
        # print("agents_state", agents_state.shape)
        f.close()
    return agents_pos, agents_state, shepherd_pos, shepherd_state


def Get_final_tick(file_name):
    file_name_string = os.path.splitext(file_name)[0].split("_")
    for item in file_name_string:
        if "tick" in item:
            tick = int(item.split("=")[1])
            # print("tick:", tick)
    return tick

################show shepherd states in one single_data########
# # # get directory for the path
# directory = os.getcwd() + "/../data/"  #"/../Data/"
# file_name = "N_sheep=200_N_shepherd=2_Final_tick=70414_Repetition=5.hdf5"
# path = directory + file_name
# agents_pos, agents_state, shepherd_pos, shepherd_state = read_hdf5_data(path)
# N_sheep = agents_pos.shape[0]
# Iterations = Get_final_tick(file_name)
# plot_multi_states(shepherd_state, N_sheep, Iterations)

################# calculate time spent in different state #######
# # get directory for the path
def calculate_time_in_different_modes(N_shepherd):
    directory = os.getcwd() + "/../Data/"
    files = os.listdir(directory)
    count = 0
    drive_mode_list = []
    collect_mode_list = []
    drive_mode = dict([])
    collect_mode = dict([])
    for sheep_index in range(100, 350, 50):
        keyword = "N_sheep=" + str(sheep_index) + "_N_shepherd=" + str(N_shepherd)
        # print(keyword)
        drive_ratio = []
        collect_ratio = []
        for file in files:
            if not os.path.isdir(file):
                if keyword in file:
                    # print(file)
                    path = directory + file
                    agents_pos, agents_state, shepherd_pos, shepherd_state = read_hdf5_data(path)
                    Iterations = Get_final_tick(file)
                    # plot_multi_states(shepherd_state, sheep_index, Iterations)
                    # print("Iterations:", Iterations)
                    drive_ratio.append(np.sum(shepherd_state) / Iterations)
                    collect_ratio.append(1 - np.sum(shepherd_state) / Iterations)
                    # print(len(drive_ratio))
                    # print(shepherd_state)
        count = count + 1
        drive_mode_list.append(drive_ratio)
        collect_mode_list.append(collect_ratio)
        drive_mode["Ns=" + str(sheep_index)] = drive_ratio
        collect_mode["Ns=" + str(sheep_index)] = collect_ratio

    drive_mode_arr = np.array(drive_mode_list)
    collect_mode_arr = np.array(collect_mode_list)
    return drive_mode_arr, collect_mode_arr
    # return drive_mode, collect_mode


# N_shepherd = 1
# drive_mode_arr, collect_mode_arr = calculate_time_in_different_modes(N_shepherd)

# def dict_write_to_csv(dic, file):
#     with open(file, "wb") as fp:
#         # create a writer object
#         writer = csv.DictWriter(fp, fieldnames=dic.keys())
#
#         # write the header row
#         writer.writeheader()
#
#         # write the data rows
#         writer.writerow(dic)
#     return
#
#
# def dict_read_from_csv(file):
#     with open(file, "r") as infile:
#         # create a reader object:
#         reader = csv.DictReader(infile)
#
#         # iterate through the rows
#         for row in reader:
#             print(row)
#     return
###########not used ############
# N_shepherd = 1
# drive_mode, collect_mode = calculate_time_in_different_modes(N_shepherd)
# file1 = os.getcwd() + "/../result/drive_mode.csv"
# file2 = os.getcwd() + "/../result/collect_mode.csv"
# dict_write_to_csv(drive_mode, file1)
# dict_write_to_csv(collect_mode, file2)
# print("dict_drive:", list(drive_mode.items()))


# print("keys:", list(drive_mode.values()))
def save_file(file, data):
    with open(file, "wb") as f:
        np.save(f, data)
    f.close()
    return

N_shepherd = 1
drive_mode_arr, collect_mode_arr = calculate_time_in_different_modes(N_shepherd)
file1 = os.getcwd() + "/mediate_result/drive_mode.npy"
file2 = os.getcwd() + "/mediate_result/collect_mode.npy"
save_file(file1, drive_mode_arr)
save_file(file2, collect_mode_arr)

#####used in box_plot_new file############
# def read_mode_data(file):
#     with open(file, "rb") as f:
#         data = np.load(f)
#         f.close()
#         # print("data:", data)
#     return data
# drive_data = read_mode_data(file1)
# collect_data = read_mode_data(file2)


##########calculate difference value for multiple data#######
def calculate_multi_difference(N_sheep):
    directory = os.getcwd() + "/../data_tick=200000/"  #+ "/../Data/"    #
    files = os.listdir(directory)
    count = 0
    matrix = np.zeros(4, dtype=float)
    for N_shepherd in range(2, 6):
        keyword = "N_sheep=" + str(N_sheep) + "_N_shepherd=" + str(N_shepherd)
        states = []
        for file in files:
            if not os.path.isdir(file):
                if keyword in file:
                    # print(file)
                    path = directory + file
                    agents_pos, agents_state, shepherd_pos, shepherd_state = read_hdf5_data(path)
                    # Iterations = shepherd_state.shape[1]
                    Iterations = Get_final_tick(file)
                    print("Iterations:", Iterations)
                    value = calculate_differ_states(shepherd_state) / Iterations  # ratio over running time
                    states.append(value)
                    # print("value:", value)
            else:
                print("Please enter a file path!")
        mean_value = np.mean(np.array(states))  #ratio over repetitions
        # matrix[index][count] = np.mean(np.array(state))
        print(keyword, "repetitions=", np.array(states).shape[0], "mean_differnt_state_value", np.mean(np.array(states)))
        matrix[count] = mean_value
        count = count + 1
    return matrix

# matrix = calculate_multi_difference(500)
# print(matrix)
##########################################
# [0.27566821, 0.41870727, 0.43268498, 0.39779931] #100
# [0.19009225, 0.30122245, 0.34001382, 0.32961186] #150
# [0.12916332, 0.2203914,  0.19322434, 0.1768058 ] #200
# [0.13176278, 0.22539609, 0.20774006, 0.19836793] #250
# [0.10728878, 0.15610854, 0.20185862, 0.20313016] #300
#  [0.101035, 0.186179, 0.217867, 0.213464] #400
# [0.064301, 0.151275, 0.156486, 0.261062] #500

