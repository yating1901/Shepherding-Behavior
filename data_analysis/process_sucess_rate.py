import matplotlib.pyplot as plt
import os, sys
import numpy as np
import h5py
from collections import defaultdict
from timeit import default_timer as timer
from datetime import timedelta
import glob


def plot_multi_states(shepherd_state):
    plt.figure(figsize=(8, 6), dpi=300)
    N_shepherd = shepherd_state.shape[0]
    # print("N_shepherd", N_shepherd)
    Iterations = shepherd_state.shape[1]
    x = [item * 0.01 for item in range(Iterations)]
    # subplot shepherd state
    for shepherd_index in range(N_shepherd):
        # print(shepherd_index)
        plt.subplot(N_shepherd + 1, 1, shepherd_index + 1)
        y = shepherd_state[shepherd_index, :]  # 1.0  drive_mode_true
        plt.plot(x, y, 'b-')
        plt.ylabel("Shepherd" + str(shepherd_index))
        if shepherd_index == 0:
            plt.title("Shepherd states")
    # subplot difference state
    difference = np.zeros(Iterations)
    for index in range(Iterations):
        if sum(shepherd_state[:, index]) != 0 and sum(shepherd_state[:, index]) != N_shepherd:
            difference[index] = 1
    print("difference:", sum(difference))
    plt.subplot(N_shepherd + 1, 1, N_shepherd + 1)
    plt.plot(x, difference, 'r-')
    plt.ylabel("difference")
    plt.savefig("./figures/state_of_shepherd.png")
    plt.xlabel("Time (s)")
    plt.show()
    return


def read_hdf5_data(path):
    # get directory for the path
    # directory = os.getcwd() + "/../data/"
    # file_name = "N_sheep=400_N_shepherd=3_Final_tick=200000_Repetition=0.hdf5"
    # path = directory + file_name
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
    return agents_pos, agents_state, shepherd_pos, shepherd_state


def data_plot(data, N_sheep):
    N_shepherd = len(data)
    # repetition = len(data[0])
    X = np.arange(N_shepherd) + 1
    Time = [np.mean(data[item]) * 0.01 for item in range(N_shepherd)]
    plt.plot(X, Time, 's-', label="N_sheep = " + str(N_sheep))
    plt.xticks(X, ["N = 1", "N = 2", "N = 3", "N = 4", "N = 5"])
    return


def Get_dict_of_data(N_sheep):
    directory = os.getcwd() + "/../Data"
    files = os.listdir(directory)
    dic = defaultdict(list)
    # matrix = np.zeros(len(data + 1))
    for N_shepherd in range(1, 6):
        count = 0
        for file in files:
            if not os.path.isdir(file):
                keyword = "N_sheep=" + str(N_sheep) + "_N_shepherd=" + str(N_shepherd)
                if keyword in file:
                    count = count + 1
                    file_name_string = os.path.splitext(file)[0].split("_")
                    for item in file_name_string:
                        if "tick" in item:    #get final ticks from the file name "tick = ..."
                            dic[keyword].append(int(item.split("=")[1]))
        # print(keyword)
        # print(count)
    return dic


# plot time as a function of the number of shepherds
def plot_time_shepherd():
    plt.figure(figsize=(8, 6), dpi=300)
    for N_sheep in range(100, 350, 50):
        dic = Get_dict_of_data(N_sheep)
        data = list(dic.values())
        repetition = len(data[0])
        # print(repetition)
        data_plot(data, N_sheep)

    plt.xlabel("Shepherd number")
    plt.ylabel("Time (s)")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.13),
               ncol=3, fancybox=True, shadow=True)
    plt.savefig("./figures/Time_and_N_shepherd.png")
    plt.show()
    return


# plot_time_shepherd()

def sucess_rate_plot(mean_success_rate, N_sheep):
    N_shepherd = len(mean_success_rate)
    # repetition = len(data[0])
    X = np.arange(N_shepherd) + 1
    plt.plot(X, mean_success_rate, 's-', label="N_sheep = " + str(N_sheep))
    plt.xticks(X, ["N = 1", "N = 2", "N = 3", "N = 4", "N = 5"])
    return


def get_success_rate(N_sheep):
    dic = Get_dict_of_data(N_sheep)
    data = list(dic.values())
    Data = np.array(data, dtype=float)
    Data = 1 / (Data * 0.01)
    mean_success_rate = np.mean(Data, axis=1)  # calculate the mean value according to lines;
    # print(mean_success_rate)
    return mean_success_rate


def draw_success_rate():
    plt.figure(figsize=(8, 6), dpi=300)
    for N_sheep in range(100, 350, 50):
        mean_success_rate = get_success_rate(N_sheep)
        sucess_rate_plot(mean_success_rate, N_sheep)
    plt.xlabel("Shepherd number")
    plt.ylabel("Success rate")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.13),
               ncol=3, fancybox=True, shadow=True)
    plt.savefig("./figures/Mean_success_rate.png")
    plt.show()

    return


draw_success_rate()
