import os, sys
import numpy as np
import pandas as pd


def save_data(N_sheep, N_shepherd, Repetition, Final_tick, Data_agents, Data_shepherds):
    # get directory for the path
    directory = os.getcwd() + "/data"

    if not os.path.exists(directory):
        os.mkdir(directory)
    file_name = ("N_sheep=" + str(N_sheep) + "_N_shepherd=" + str(N_shepherd)
                 + "_Final_tick=" + str(Final_tick) + "_Repetition=" + str(Repetition))

    Data = np.vstack((Data_agents, Data_shepherds))
    # save agents to .npy file
    np.save(file=directory + "/"+ file_name + ".npy", arr=Data)
    return

def save_file(N_sheep, N_shepherd, Repetition, Final_tick):
    # write simple data to txt file
    directory = os.getcwd() + "/data/"
    file_name = ("N_sheep=" + str(N_sheep) + "_N_shepherd=" + str(N_shepherd)
                 + "_Final_tick=" + str(Final_tick))  # + "_Repetition=" + str(Repetition)
    file_txt = directory + file_name + ".txt"
    print(file_txt)
    if not os.path.exists(file_txt):
        f = open(file_txt, "w")
    else:
        f = open(file_txt, "a")
    # f.write("Repetition=%d_Final=tick=%d\n" % int(Repetition) % int(Final_tick))
    f.write("Repetition=%d\n" % int(Repetition))
    f.write("Final=tick=%d\n" % int(Final_tick))
    f.close()
    return
