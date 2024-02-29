import matplotlib.pyplot as plt
import numpy as np
import os


def read_mode_data(file):
    with open(file, "rb") as f:
        data = np.load(f)
        f.close()
        # print("data:", data)
    return data


file1 = os.getcwd() + "/mediate_result/drive_mode.npy"
file2 = os.getcwd() + "/mediate_result/collect_mode.npy"
drive_data = read_mode_data(file1)
collect_data = read_mode_data(file2)
# print(drive_data)
# print(len(drive_data))

plt.figure(figsize=(8, 6), dpi=300)

# labels = ["Ns = 100", "Ns = 150", "Ns = 200", "Ns = 250", "Ns = 300"]
labels = ["Ns = 100", "Ns = 200", "Ns = 300", "Ns = 400"]
# print(len(labels))
colors = [(202 / 255., 96 / 255., 17 / 255.), (255 / 255., 217 / 255., 102 / 255.),'pink', 'lightblue', 'lightgreen']
pos = np.array(np.arange(len(drive_data))*3.0+0.35)
# print(pos)
#
drive_plot = plt.boxplot(drive_data.T, vert=True, showmeans=True, patch_artist=True, meanline=True, labels=labels, positions=pos, widths=0.3)
plt.setp(drive_plot["boxes"], facecolor="pink")
# for patch, color in zip(drive_plot['boxes'], colors):
#     patch.set_facecolor(color)
#
collect_plot = plt.boxplot(collect_data.T, vert=True, patch_artist=True, showmeans=True, meanline=True, labels=labels, positions=pos-0.7, widths=0.3)
plt.setp(collect_plot["boxes"], facecolor="lightblue")
# for patch, color in zip(collect_plot['boxes'], colors):
#     patch.set_facecolor(color)

# #
x_position = np.array(np.arange(len(drive_data))*3.0)
x_position_fmt = ["Ns = 100", "Ns = 200", "Ns = 300", "Ns = 400"]
plt.xticks([i + 0.8 / 2 for i in x_position], x_position_fmt)
#
plt.xlabel("Number of Sheep")
plt.ylabel("Ratio of shepherd mode")
plt.title("Shepherd = 1")
plt.grid(linestyle="--", alpha=0.3)
# plt.legend(["drive mode", "collect mode"])
plt.legend([drive_plot['boxes'][0], collect_plot['boxes'][0]], ["drive mode", "collect mode"], loc='upper left')
# plt.legend(drive_plot['boxes'],  collect_plot['boxes'], ["drive mode", "collect mode"], loc='lower right')
plt.savefig(os.getcwd()+"/figures/Modes_of_Shepherd_box_plot.png")
plt.show()
