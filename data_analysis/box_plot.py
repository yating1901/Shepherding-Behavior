import matplotlib.pyplot as plt
import numpy as np

data_Ns_50_H_1 = [tick*0.01 for tick in [49093, 42450, 45797, 46818, 42557]]
data_Ns_50_H_2 = [tick*0.01 for tick in [35042, 52262, 44731, 43289, 45470]]
data_Ns_50_H_3 = [tick*0.01 for tick in [36733, 39617, 46173, 48304, 48301]]

data_Ns_75_H_1 = [tick*0.01 for tick in [62160, 77010, 67527, 69254, 67157]]
data_Ns_75_H_2 = [tick*0.01 for tick in [74666, 77015, 55782, 60141, 66522]]
data_Ns_75_H_3 = [tick*0.01 for tick in [83042, 54495, 67615, 73988, 71292]]

data_Ns_100_H_1 = [tick*0.01 for tick in [104800, 110333, 129370, 92902, 110212]]
data_Ns_100_H_2 = [tick*0.01 for tick in [82007, 127759, 104902, 114591, 100924]]
data_Ns_100_H_3 = [tick*0.01 for tick in [72216, 75593, 90127, 95155, 86673]]

Data_50 = [data_Ns_50_H_1,  data_Ns_50_H_2, data_Ns_50_H_3]
Data_75 = [data_Ns_75_H_1, data_Ns_75_H_2, data_Ns_75_H_3]
Data_100 = [data_Ns_100_H_1, data_Ns_100_H_2, data_Ns_100_H_3]
# print(Data_50)
# figure, axes = plt.subplots()
# axes.boxplot(Data_100, vert=True, patch_artist=True)
# axes.set_xticklabels(["N = 1", "N = 2", "N = 3"])
# plt.xlabel("Number of Shepherd")
# plt.ylabel("Time (s)")
# plt.savefig("sheep=100.png")
# plt.show()

labels = ["SH = 1", "SH = 2", "SH = 3"]
colors =[(202/255., 96/255.,17/255.),(255/255., 217/255.,102/255.),(137/255., 128/255.,68/255.)]

bplot_1 = plt.boxplot(Data_50, patch_artist=True, labels=labels, positions=(1,1.4,1.8), widths=0.3)
for patch, color in zip(bplot_1['boxes'], colors):
    patch.set_facecolor(color)

bplot_2 = plt.boxplot(Data_75, patch_artist=True, labels=labels, positions=(2.5,2.9,3.3), widths=0.3)
for patch, color in zip(bplot_2['boxes'], colors):
    patch.set_facecolor(color)

bplot_3 = plt.boxplot(Data_100, patch_artist=True, labels=labels, positions=(4, 4.4, 4.8), widths=0.3)
for patch, color in zip(bplot_3['boxes'], colors):
    patch.set_facecolor(color)

x_position = [1, 2.5, 4]
x_position_fmt = ["Ns = 50", "Ns = 75", "Ns = 100"]
plt.xticks([i + 0.8 / 2 for i in x_position], x_position_fmt)

plt.xlabel("Number of Sheep")
plt.ylabel("Time (s)")
plt.grid(linestyle="--", alpha=0.3)
plt.legend(bplot_1['boxes'], labels,loc='lower right')
plt.savefig(fname='all.png')
plt.show()