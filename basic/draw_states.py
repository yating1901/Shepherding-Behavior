import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import os


def draw_state(Iterations, Data_shepherds):
    plt.figure(figsize=(8, 6), dpi=300)
    N_shepherd = Data_shepherds[:, :, 0].shape[0]
    x = [item*0.01 for item in range(Iterations-5000)]
    difference = np.zeros(Iterations)
    # print(x)
    for shepherd_index in range(N_shepherd):
        plt.subplot(N_shepherd+1, 1, (1+shepherd_index))
        # y = Data_shepherds[shepherd_index, 13, 5000: 5000+Iterations]  # 1.0  drive_mode_true
        y = Data_shepherds[shepherd_index, 13, 5000:Iterations]  # 1.0  drive_mode_true
        plt.plot(x, y, 'b-')
        plt.xlabel("Time (s)")
        plt.ylabel("State of Shepherd " + str(shepherd_index))
        if shepherd_index == 0:
            difference = y
        else:
            difference = abs(y-difference)
    print("mean difference:", mean(difference))
    plt.subplot(3, 1, 3)
    plt.plot(x, difference, 'r-')
    # plt.plot(x, difference, 'r-')
    plt.xlabel("Time (s)")
    plt.ylabel("Difference of state")
    plt.savefig("States_of_shepherd.png")
    plt.show()
    return

def draw_state_single(Iterations, Data_shepherds):
    plt.figure(figsize=(8, 6), dpi=300)
    x = [item*0.01 for item in range(Iterations-5000)]
    y = Data_shepherds[0, 13, 5000: Iterations]  # 1.0  drive_mode_true
    plt.plot(x, y, 'b-')
    plt.xlabel("Time (s)")
    plt.ylabel("State of Shepherd ")
    plt.savefig("States_of_shepherd.png")
    plt.show()
    return