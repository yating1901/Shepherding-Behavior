
import numpy as np

def initate(agent_num, space_x, space_y, Target_size):
    
    swarm = np.zeros(shape=(agent_num, 22))
    # swarm
    swarm[:, 0] = np.random.uniform(50, space_x, agent_num)
    swarm[:, 1] = np.random.uniform(50, space_y, agent_num)
    swarm[:, 2] = np.random.uniform(0, 2*np.pi, agent_num)
    swarm[:, 3] = 7.5    # repulsion_distance 10  #12.5  #10 #7 #6.5 #7.5
    swarm[:, 4] = 0      # alignment_distance no use
    swarm[:, 5] = 30     # attraction_distance  30 # 20 # 25
    swarm[:, 6] = 1.5    # v0 # 0.4 # 0.1 # 1
    swarm[:, 7] = 0
    swarm[:, 8] = 0
    swarm[:, 9] = 0
    swarm[:, 10] = 2             # K_repulsion_agent  0.4 1 0.6 1
    swarm[:, 11] = 0.8           # K_attraction  0.04 0.08 0.7 0.6 0.8
    swarm[:, 12] = 1.8           # K_repulsion avoid shepherd  2.8 0.5 0.8
    swarm[:, 13] = 0.1           # K_Dr: noise strength
    swarm[:, 14] = 0.01          # tick_time 0.001
    swarm[:, 15] = 1             # alpha: acceleration 1   1
    swarm[:, 16] = 1             # beta: turning rate  1
    swarm[:, 17] = 65             #### safe_distance  45
    swarm[:, 18] = np.pi*2/3      # maximum turning rate
    swarm[:, 19] = np.pi          # field of view np.pi * 4 / 3  #240 degree
    swarm[:, 20] = Target_size
    swarm[:, 21] = 0              # agent state: moving -> 0; staying -> 1;
    return swarm

def initate_shepherd(N_shepherd):
    shepherd_swarm = np.zeros(shape=(N_shepherd, 22), dtype=float)
    # parameter
    shepherd_swarm[:, 0] = np.random.uniform(0, 50, N_shepherd)
    shepherd_swarm[:, 1] = np.random.uniform(0, 50, N_shepherd)
    shepherd_swarm[:, 2] = np.random.uniform(-np.pi, np.pi, N_shepherd)
    shepherd_swarm[:, 3] = 20     ### l0: Equlibrum distance from the furthest agent to collect point
    shepherd_swarm[:, 4] = 5      ### K: elastic force # 2
    shepherd_swarm[:, 5] = 50     ### l1: drive distance from the center of mass to the drive point (30 Ns = 50) (30 N = 75)(35 N=100)_## related to safe_distance = 45
    shepherd_swarm[:, 6] = 4               # v0
    shepherd_swarm[:, 7] = 3               # alpha #4
    shepherd_swarm[:, 8] = 0.5             # beta  #2
    shepherd_swarm[:, 9] = 0.1             # Dr: noise
    shepherd_swarm[:, 10] = 0.01           # tick_time/ seconds
    shepherd_swarm[:, 11] = np.pi*1/3      # maximum turning rate
    shepherd_swarm[:, 12] = 60             ### maximum distance of furthest agent to mass (35 Ns = 50) (60 Ns=100) ### switch to collect mode
    shepherd_swarm[:, 13] = 1.0            # drive_mode_true
    shepherd_swarm[:, 14] = 0              # collect_x
    shepherd_swarm[:, 15] = 0              # collect_y
    shepherd_swarm[:, 16] = 0              # collect_agent_index
    shepherd_swarm[:, 17] = np.pi*2        # half field of view ??
    shepherd_swarm[:, 18] = 0.01           ### K_attraction_target
    shepherd_swarm[:, 19] = 10             ### L3 Equilibrium distance from other shepherd 8
    shepherd_swarm[:, 20] = 0              ##############
    shepherd_swarm[:, 21] = 0              ##############

    return shepherd_swarm
