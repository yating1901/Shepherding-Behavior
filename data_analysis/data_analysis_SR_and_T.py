import matplotlib.pyplot as plt
import os, sys
import numpy as np
import h5py
from collections import defaultdict
from timeit import default_timer as timer
from datetime import timedelta
import glob


def Get_dict_of_data(l3, N_sheep, N_shepherd, data_folder):
    files = os.listdir(data_folder)
    dic = defaultdict(list)
    count = 0  # count repetitions
    for file in files:
        if not os.path.isdir(file):
            keyword = "N_sheep=" + str(N_sheep) + "_N_shepherd=" + str(N_shepherd) + "_L3=" + str(l3)
            if keyword in file:
                count = count + 1
                file_name_string = os.path.splitext(file)[0].split("_")
                for item in file_name_string:
                    if "tick" in item:  # get final ticks from the file name "tick = ..."
                        dic[keyword].append(int(item.split("=")[1]))
    # print(keyword)
    # print(count)
    # print(dic)
    data = list(dic.values())[0]  #
    return data


def plot_time_shepherd_force(list_of_L3, list_of_N_sheep, list_of_N_shepherd, path, SR):
    for l3 in list_of_L3:
        # plt.figure(figsize=(8, 6), dpi=300)
        plt.figure()
        for N_sheep in list_of_N_sheep:
            data_folder = path + "/L3=" + str(l3) + "/N_sheep=" + str(N_sheep) + "/"
            Success_Rate = []
            Std_Success_Rate = []
            Time = []
            Std_Time = []
            # print("N_sheep:", N_sheep)
            for N_shepherd in list_of_N_shepherd:
                # print("N_shepherd:", N_shepherd)
                data = Get_dict_of_data(l3, N_sheep, N_shepherd, data_folder)
                # repetition = len(data[0])
                # print(data)
                data_time = [t * 0.01 for t in data]  # seconds
                success_rate = [1.0 / (t * 0.01) for t in data]

                # print(data_time)
                Time.append(np.mean(data_time))
                Std_Time.append(np.std(data_time))
                Success_Rate.append(np.mean(success_rate))
                Std_Success_Rate.append(np.std(success_rate))
            # print(Time)
            # print(success_rate)
            X = list_of_N_shepherd
            labels = ["N = " + str(n_shepherd) for n_shepherd in list_of_N_shepherd]
            if SR == False:
                plt.errorbar(X, Time, yerr=Std_Time, fmt="-o", label="N_sheep = " + str(N_sheep))
            else:
                plt.errorbar(X, Success_Rate, yerr=Std_Success_Rate, fmt="-o", label="N_sheep = " + str(N_sheep))
            plt.xticks(X, labels)
        plt.title("L3 = " + str(l3))
        plt.xlabel("Number of Shepherds")
        plt.legend()
        if SR == False:
            plt.ylabel("Time (s)")
            plt.savefig("./figures/Time_and_N_shepherd_L3=" + str(l3) + ".png")
        else:
            plt.ylabel("Success Rate")
            plt.savefig("./figures/SR_and_N_shepherd_L3=" + str(l3) + ".png")
        plt.show()
        plt.clf()
    return


# L3 = 0
path = directory = os.getcwd() + "/../Data_Metric_Model"
list_of_L3 = [0]

# L3 = 20
# path = "/media/yateng/Extreme SSD/"
# list_of_L3 = [20]

list_of_N_sheep = [i for i in range(100, 350, 50)]  ##[100]
list_of_N_shepherd = [i for i in range(1, 6)]
SR = False  # success rate
# plot time as a function of the number of shepherds
plot_time_shepherd_force(list_of_L3, list_of_N_sheep, list_of_N_shepherd, path, SR)
