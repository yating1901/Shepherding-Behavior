import csv
import matplotlib.pyplot as plt
import os, sys
import numpy as np
import h5py
import seaborn as sns
from timeit import default_timer as timer
from datetime import timedelta
from collections import defaultdict


def read_hdf5_data(file_path):
    with h5py.File(file_path, "r") as f:
        # print(f.keys())
        agents = f.get("agent_data")[:]
        shepherd = f.get("shepherd_data")[:]
        agents_pos = agents[:, 0:2, :]
        agents_state = agents[:, 3, :]
        shepherd_pos = shepherd[:, 0:2, :]
        shepherd_state = shepherd[:, 3, :]
        f.close()
    return agents_pos, agents_state, shepherd_pos, shepherd_state


def Get_final_tick(file_name):
    file_name_string = os.path.splitext(file_name)[0].split("_")
    for item in file_name_string:
        if "tick" in item:
            tick = int(item.split("=")[1])
    return tick

def calculate_differ_states(shepherd_states_data, Iterations):
    N_shepherd = shepherd_states_data.shape[0]
    iterations = Iterations
    difference = np.zeros(iterations)
    for index in range(iterations):
        if sum(shepherd_states_data[:, index]) != 0 and sum(shepherd_states_data[:, index]) != N_shepherd:
            difference[index] = 1
    value = sum(difference)
    print("N_shepherd:", N_shepherd, "difference:", value, "iterations", iterations)
    return value


def calculate_pairwise_differ_states(shepherd_states_data, Iterations):
    N_shepherd = shepherd_states_data.shape[0]
    iterations = Iterations
    difference = np.zeros(iterations)
    for tick in range(iterations):
        count = 0
        for start_index in range(N_shepherd - 1):
            for end_index in range(start_index + 1, N_shepherd):
                count = count + 1
                if shepherd_states_data[start_index, tick] != shepherd_states_data[end_index, tick]:
                    difference[tick] = difference[tick] + 1
        # print("count:", count)
        difference[tick] = difference[tick] #/ count
    value = sum(difference)
    print("N_shepherd:", N_shepherd, "count:", count, "difference:", sum(difference), "iterations", iterations)
    return value


##########calculate difference value for multiple data#######
def calculate_multi_difference(List_of_L3, List_of_N_sheep, List_of_N_shepherd, Directory):

    count = 0
    matrix = np.zeros(len(List_of_N_shepherd), dtype=float)
    for L3 in List_of_L3:
        for N_sheep in List_of_N_sheep:
            data_folder = Directory + "/L3=" + str(L3) + "/N_sheep=" + str(N_sheep) + "/"
            files = os.listdir(data_folder)
            for N_shepherd in List_of_N_shepherd:
                keyword = "N_sheep=" + str(N_sheep) + "_N_shepherd=" + str(N_shepherd) + "_L3=" + str(L3)
                # print(keyword)
                states = []
                for file in files:
                    if not os.path.isdir(file):
                        if keyword in file: #and "Repetition=0" in file:
                            # print(file)
                            file_path = data_folder + file
                            agents_pos, agents_state, shepherd_pos, shepherd_state = read_hdf5_data(file_path)
                            Iterations = Get_final_tick(file)
                            # print("Iterations:", Iterations)
                            # value = calculate_pairwise_differ_states(shepherd_state, Iterations) / Iterations
                            value = calculate_differ_states(shepherd_state, Iterations) / Iterations
                            states.append(value)
                            # print("value:", value)
                    else:
                        print("Please enter a file path!")
                mean_value = np.mean(np.array(states))  # ratio over repetitions
                print(keyword, "repetitions=", np.array(states).shape[0], "mean_different_state_value", mean_value)
                matrix[count] = mean_value
                count = count + 1
    return matrix


def plot_coordination_ratio(list_of_L3, list_of_N_sheep, list_of_N_shepherd, path):
    for L3 in list_of_L3:
        plt.figure(figsize=(8, 6), dpi=300)
        x = list_of_N_shepherd
        labels = ["N = " + str(n_shepherd) for n_shepherd in list_of_N_shepherd]
        for N_sheep in list_of_N_sheep:
            coordinate_ratio = calculate_multi_difference(list_of_L3, list_of_N_sheep, list_of_N_shepherd, path)
            plt.plot(x, coordinate_ratio, '^-', color='orange', label="N_sheep = " + str(N_sheep))
        plt.xticks(x, labels)
        plt.title("L3 = " + str(L3))
        plt.xlabel("Shepherd number")
        plt.ylabel("Coordination Ratio")
        plt.legend(loc="best")
        plt.savefig("./figures/Coordination_Ratio_L3=" + str(L3) + ".png")
        plt.show()
        plt.clf()


# L3 = 0
path = directory = os.getcwd() + "/../Data_Metric_Model"
list_of_L3 = [0]

# L3 = 20
# path = "/media/yateng/Extreme SSD/"
# list_of_L3 = [20]

list_of_N_sheep = [100] #[i for i in range(100, 350, 50)]  ##[100]
list_of_N_shepherd = [2] #[i for i in range(2, 6)]

# plot time as a function of the number of shepherds
Matrix = calculate_multi_difference(list_of_L3, list_of_N_sheep, list_of_N_shepherd, path)
print(Matrix)
# plot_coordination_ratio(list_of_L3, list_of_N_sheep, list_of_N_shepherd, path)