
import numpy as np

def initiate(agent_num, space_x, space_y, Target_size):
    
    swarm = np.zeros(shape=(agent_num, 22))
    swarm[:, 0] = np.random.uniform(50, space_x, agent_num)
    swarm[:, 1] = np.random.uniform(50, space_y, agent_num)
    swarm[:, 2] = np.random.uniform(-np.pi, np.pi, agent_num)
    swarm[:, 3] = 7.5    # repulsion_distance 10  #12.5  #10 #7 #6.5 #7.5
    swarm[:, 4] = 0      # alignment_distance no use
    swarm[:, 5] = 25     # attraction_distance #25  #30
    swarm[:, 6] = 1      # v0 # 0.4 # 0.1 # 1 # 1.5
    swarm[:, 7] = 0
    swarm[:, 8] = 0
    swarm[:, 9] = 0
    swarm[:, 10] = 2             # K_repulsion_agent  0.4 1 0.6 1 #2
    swarm[:, 11] = 0.8           # K_attraction  0.04 0.08 0.7 0.6 #0.8
    swarm[:, 12] = 1.5           # K_repulsion avoid shepherd  5 #1.8 #2.5
    swarm[:, 13] = 0.1           # K_Dr: noise strength
    swarm[:, 14] = 0.01          # tick_time 0.001
    swarm[:, 15] = 1             # alpha: acceleration 1   1
    swarm[:, 16] = 1             # beta: turning rate  1
    swarm[:, 17] = 65            # safe_distance from shepherd # 45
    swarm[:, 18] = np.pi*2/3     # maximum turning rate
    swarm[:, 19] = np.pi         # FOV field of view np.pi * 4 / 3  #240 degree
    swarm[:, 20] = Target_size
    swarm[:, 21] = 0.0             ### agent state: moving -> 0; staying -> 1;
    return swarm

def initiate_shepherd(N_shepherd, agent_num, L3):
    shepherd_swarm = np.zeros(shape=(N_shepherd, 22), dtype=float)
    # parameter
    shepherd_swarm[:, 0] = np.random.uniform(0, 50, N_shepherd)
    shepherd_swarm[:, 1] = np.random.uniform(0, 50, N_shepherd)
    shepherd_swarm[:, 2] = np.random.uniform(-np.pi, np.pi, N_shepherd)
    shepherd_swarm[:, 3] = 15              # L0: collect point: from shepherd to the collect agent
    shepherd_swarm[:, 4] = 5               # K: elastic force # 2
    shepherd_swarm[:, 5] = 7.5*(np.sqrt(agent_num))*2/3    # L1: drive point: from shepherd to mass center(40 Ns = 50)(50 N=100)(75 N = 200)#59 N = 250
    shepherd_swarm[:, 6] = 4               # v0    #4 #2 2 is too small to catch up the sheep
    shepherd_swarm[:, 7] = 3.5               # alpha #4 #3 #1 #2
    shepherd_swarm[:, 8] = 0.5             # beta  #2 #0.5 #1
    shepherd_swarm[:, 9] = 0.1             # Dr: noise
    shepherd_swarm[:, 10] = 0.01           # tick_time/ seconds
    shepherd_swarm[:, 11] = np.pi*1/3      # maximum turning rate
    shepherd_swarm[:, 12] = 7.5*(np.sqrt(agent_num))*2/3    # L2: collect mode: Furthest agent to mass (35 Ns = 50) (60 Ns=100)(75 Ns = 200)# 59 N = 250
    shepherd_swarm[:, 13] = 1.0            # shepherd state: drive_mode = true
    shepherd_swarm[:, 14] = 0              # collect_x/drive_x
    shepherd_swarm[:, 15] = 0              # collect_y/drive_y
    shepherd_swarm[:, 16] = 0              # collect_agent_index
    shepherd_swarm[:, 17] = np.pi*2        # half field of view ??
    shepherd_swarm[:, 18] = 0.01           # K_attraction_target   0.01
    shepherd_swarm[:, 19] = L3  # L3: distance to avoid other shepherd #10 ((np.sqrt(agent_num))*7.5)/3/(N_shepherd+1)
    shepherd_swarm[:, 20] = 0              #
    shepherd_swarm[:, 21] = 0              #

    return shepherd_swarm
