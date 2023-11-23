import matplotlib.pyplot as plt
import os, sys
import numpy as np

directory = os.getcwd() + "/../data/"

file_name = "N_sheep=50_N_shepherd=1_Final_tick=100_Repetition=1.npy"

data = np.load(directory+file_name)
print(data.shape)
