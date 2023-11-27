import numba as nb
import numpy as np
import matplotlib.pyplot as plt
import math

@nb.jit(nopython=True)
def create_metric_network(agents):
    # get number of agents
    num_agents = agents.shape[0]
    # create a metric with N * N dimension
    metric_network = np.zeros(shape=(num_agents, num_agents))
    # length of attraction: maximum interaction range for agent
    R = agents[0][5]
    # loop agents
    for agent_index in range(num_agents):
        x_i = agents[agent_index, 0]
        y_i = agents[agent_index, 1]
        angle_i = agents[agent_index, 2]
        # field of view np.pi/2 -- to be used
        Fov = agents[agent_index][19]
        for neighbor_index in range(num_agents):
            if agent_index != neighbor_index:
                x_j = agents[neighbor_index, 0]
                y_j = agents[neighbor_index, 1]
                # distance between agent i and agent j
                r_ij = np.sqrt((x_j - x_i)**2 + (y_i - y_j)**2)
                # vector from agent j position to agent i position
                angle_ij = math.atan2((y_j - y_i), (x_j - x_i))
                # vectory from the heading direction of agent i to vector_ij
                difference_ij = angle_i - angle_ij
                if r_ij <= R:  # and (abs(angle_ij) <= Fov):
                    metric_network[agent_index, neighbor_index] = 1
    return metric_network

def create_topological_network(agents, N):
    Nearest_neighbour = N
    # get number of agents
    num_agents = agents.shape[0]
    # create a metric with N * N dimension
    topological_network = np.zeros(shape=(num_agents, num_agents))

    return topological_network