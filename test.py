# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os, sys
import numba as nb
import numpy as np
import matplotlib.pyplot as plt
from basic.initiation import initiate, initiate_shepherd
from basic.interaction import evolve, make_preodic_boundary
from basic.save_data import save_data
from basic.draw_states import draw_state, draw_state_single
from basic.draw import draw_single, draw_dynamic, plot_snapshot
from basic.create_network import create_metric_network

N_sheep = 100
N_shepherd = 2
Space_x = 150
Space_y = 150

Target_place_x = 400
Target_place_y = 400
Target_size = 100  # radius

Boundary_x = Target_place_x + Target_size
Boundary_y = Target_place_y + Target_size

Iterations = 50000
TICK = 10000
Repetition = 3

if __name__ == '__main__':
    agents = initiate(N_sheep, Space_x, Space_y, Target_size)
    shepherd = initiate_shepherd(0, N_sheep)
    Data_agents = np.zeros((agents.shape[0], agents.shape[1], Iterations), float)
    Data_shepherds = np.zeros((shepherd.shape[0], shepherd.shape[1], Iterations), float)
    # Map_agents = np.zeros((N_sheep, N_sheep, Iterations), float)
    Max_agents_indexes = np.zeros((shepherd.shape[0], Iterations), int)
    Final_iterations = Iterations

    for tick in range(Iterations):
        if tick == TICK:
            shepherd = initiate_shepherd(N_shepherd, N_sheep)  # add shepherd at certain tick
            Data_shepherds = np.zeros((shepherd.shape[0], shepherd.shape[1], Iterations), float)
            Max_agents_indexes = np.zeros((N_shepherd, Iterations), int)

        agents_update, shepherd_update, max_agents_indexes = evolve(agents, shepherd, Target_place_x, Target_place_y, Target_size)

        agents = agents_update
        shepherd = shepherd_update
        Data_agents[:, :, tick] = agents
        Data_shepherds[:, :, tick] = shepherd
        # Map_agents[:, :, tick] = map
        Max_agents_indexes[:, tick] = max_agents_indexes    #only two dimension

        if sum(agents[:, 21]) == N_sheep:   # finish
            Final_iterations = tick
            break
    draw_dynamic(Final_iterations, Data_agents, Data_shepherds, Boundary_x, Boundary_y, Target_place_x, Target_place_y, Target_size)
    print("Repetition=", Repetition, "N_Shepherd=", N_shepherd, "N_sheep=", N_sheep, "Final_tick=", Final_iterations)
    print("L0=", shepherd[0][3], "L1=", shepherd[0][5], "L2=", shepherd[0][12], "L3=", shepherd[0][19])
    # plot_snapshot(agents, shepherd, Repetition, Boundary_x, Boundary_y, Target_place_x, Target_place_y, Target_size)

    # draw_state(Final_iterations, Data_shepherds)

    # draw_state_single(Final_iterations, Data_shepherds)

    # save_data(N_sheep, N_shepherd, Repetition, Final_iterations, Data_agents, Data_shepherds)
