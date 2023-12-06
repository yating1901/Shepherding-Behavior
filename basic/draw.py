import numba as nb
import numpy as np
import matplotlib.pyplot as plt
import os, sys

# import shutil
from turtle import *

@nb.jit(nopython=True)
def calculate_mass_center(agents):
    sum_x = 0
    sum_y = 0
    n = 0
    for index in range(agents.shape[0]):
        # agent state: staying -> 1; moving -> 0;
        if agents[index][21] == 0:
            n = n+1
            sum_x = sum_x + agents[index][0]
            sum_y = sum_y + agents[index][1]
    if n != 0:
        sum_x = sum_x/n
        sum_y = sum_y/n
    return sum_x, sum_y


# @nb.jit(nopython=True)
def draw_single(swarm, shepherd, Boundary_x, Boundary_y, Target_place_x, Target_place_y, Target_size):
    # draw sheep
    N = swarm.shape[0]
    for index in range(N):
        if swarm[index, 21] == 1:  # staying state radius=2.5
            circles = plt.Circle((swarm[index, 0], swarm[index, 1]), radius=2.5, facecolor='none', edgecolor='b',
                                 alpha=0.8)
        else:  # moving state radius=2.5
            circles = plt.Circle((swarm[index, 0], swarm[index, 1]), radius=2.5, facecolor='none', edgecolor='g',
                                 alpha=0.8)
            # if index == 0:
            #     plt.text(swarm[index, 0] * 1.05, swarm[index, 1] * 1.05, "agent_0", fontsize = 10)
        plt.gca().add_patch(circles)
    plt.quiver(swarm[:, 0], swarm[:, 1], np.cos(swarm[:, 2]), np.sin(swarm[:, 2]), headwidth=3, headlength=4,
               headaxislength=3.5, minshaft=4, minlength=1, color='g', scale_units='inches', scale=10)

    # #draw_network
    # N = swarm.shape[0]
    # for i in range(N):
    #     for j in range(N):
    #         if map[i,j] == 1:
    #            plt.plot([swarm[i][0], swarm[j][0]], [swarm[i][1], swarm[j][1]], linewidth = 1, color = 'g', alpha = 0.4)  #'#e6e6fa'

    # draw shepherd
    plt.plot(shepherd[:, 0], shepherd[:, 1], marker='o', color='r', markersize=5, alpha=0.2)
    plt.quiver(shepherd[:, 0], shepherd[:, 1], np.cos(shepherd[:, 2]), np.sin(shepherd[:, 2]), headwidth=3,
               headlength=3, headaxislength=3.5, minshaft=4, minlength=1, color='r', scale_units='inches', scale=10)

    N_shepherd = shepherd.shape[0]
    for i in range(N_shepherd):
        plt.plot([shepherd[i][14], shepherd[i][0]], [shepherd[i][15], shepherd[i][1]], color='cyan')
        # plt.text(shepherd[i][14] * 1.05, shepherd[i][15] * 1.05, "CP", fontsize=10)
    # draw center of mass
    # center_of_mass_x = np.mean(swarm[:, 0])
    # center_of_mass_y = np.mean(swarm[:, 1])
    center_of_mass_x, center_of_mass_y = calculate_mass_center(swarm)
    plt.plot(center_of_mass_x, center_of_mass_y, "r*", markersize=5)
    plt.plot(Target_place_x, Target_place_y, "b*")
    target_circle = plt.Circle((Target_place_x, Target_place_y), radius=Target_size, facecolor='none', edgecolor='b',
                               alpha=0.5)
    plt.gca().add_patch(target_circle)
    # plt.xlim((center_of_mass_x-Boundary_x/2, center_of_mass_x + Boundary_x/2))
    # plt.ylim((center_of_mass_y-Boundary_y/2, center_of_mass_x + Boundary_y/2))

    plt.xlim(xmin=0, xmax=Boundary_x)
    plt.ylim(ymin=0, ymax=Boundary_y)
    # plt.axis("equal")
    # plt.xlim(-Boundary_x/2, Boundary_x/2)
    # plt.ylim(-Boundary_y/2, Boundary_y/2)  


def draw_dynamic(Iterations, Data_agents, Data_shepherds, Space_x, Space_y, Target_place_x, Target_place_y,
                 Target_size):
    plt.figure(figsize=(8, 6), dpi=300)
    plt.ion()
    folder_path = os.getcwd() + "/images/"
    # print(folder_path)
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file_path)[1]
            if file_ext.lower() in ['.png', '.mp4']:
                os.remove(file_path)

    for index in range(0, Iterations, 100):
        # print(index)
        plt.cla()
        draw_single(Data_agents[:, :, index], Data_shepherds[:, :, index], Space_x, Space_y, Target_place_x,
                    Target_place_y, Target_size)
        plt.title("tick = " + str(index))
        plt.savefig(folder_path + str(int(index / 100)) + ".png")
        # plt.pause(0.01)
    plt.ioff()
    # plt.show()
    return


def plot_snapshot(Final_tick, swarm, shepherd, repetition, Boundary_x, Boundary_y, Target_place_x, Target_place_y, Target_size):
    # create folder
    folder_path = os.getcwd() + "/snapshot"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    # create figure
    plt.figure(figsize=(8, 6), dpi=300)
    N_sheep = swarm.shape[0]
    N_shepherd = shepherd.shape[0]
    # plot sheep
    for index in range(N_sheep):
        if swarm[index, 21] == 1:
            # staying state
            circles = plt.Circle((swarm[index, 0], swarm[index, 1]), radius=2.5, facecolor='none', edgecolor='b',
                                 alpha=0.8)
        else:
            # moving state
            circles = plt.Circle((swarm[index, 0], swarm[index, 1]), radius=2.5, facecolor='none', edgecolor='g',
                                 alpha=0.8)
        plt.gca().add_patch(circles)
    # add arrow
    plt.quiver(swarm[:, 0], swarm[:, 1], np.cos(swarm[:, 2]), np.sin(swarm[:, 2]), headwidth=3, headlength=4,
               headaxislength=3.5, minshaft=4, minlength=1, color='g', scale_units='inches', scale=10)
    # plot shepherd
    plt.plot(shepherd[:, 0], shepherd[:, 1], marker='o', color='r', markersize=5, alpha=0.2)
    plt.quiver(shepherd[:, 0], shepherd[:, 1], np.cos(shepherd[:, 2]), np.sin(shepherd[:, 2]), headwidth=3,
               headlength=3, headaxislength=3.5, minshaft=4, minlength=1, color='r', scale_units='inches', scale=10)
    # draw direct line between shepherd
    for i in range(N_shepherd):
        plt.plot([shepherd[i][14], shepherd[i][0]], [shepherd[i][15], shepherd[i][1]], color='cyan')
    # draw center of mass ---------------> to be updated: ignore those inside the target place...
    # center_of_mass_x = np.mean(swarm[:, 0])
    # center_of_mass_y = np.mean(swarm[:, 1])
    center_of_mass_x, center_of_mass_y = calculate_mass_center(swarm)

    plt.plot(center_of_mass_x, center_of_mass_y, "r*", markersize=5)
    plt.plot(Target_place_x, Target_place_y, "b*")
    target_circle = plt.Circle((Target_place_x, Target_place_y), radius=Target_size, facecolor='none', edgecolor='b',
                               alpha=0.5)
    plt.gca().add_patch(target_circle)

    plt.xlim(xmin=0, xmax=Boundary_x)
    plt.ylim(ymin=0, ymax=Boundary_y)

    plt.title("Ns = " + str(N_sheep) + "N = " + str(N_shepherd) + "tick =" + str(Final_tick))
    plt.savefig(folder_path + "/" + "N_sheep=" + str(N_sheep) + "_N_shepherd=" + str(N_shepherd)
                + "_repetition=" + str(repetition) + ".png")

    return

# ffmpeg -framerate 10 -start_number 0 -i %d.png -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4
## ffplay output.mp4
