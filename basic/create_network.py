import numba as nb
import numpy as np
import matplotlib.pyplot as plt
import math


def Get_relative_distance_angle(target_x, target_y, focal_agent_x, focal_agent_y):
    r_x = target_x - focal_agent_x
    r_y = target_y - focal_agent_y
    r_length = np.sqrt(r_x ** 2 + r_y ** 2)
    r_angle = np.arctan2(r_y, r_x)  # [-pi, pi]
    return r_length, r_angle

@nb.jit(nopython=True)
def transform_angle(theta):
    while theta >= np.pi:
        theta = theta - 2 * np.pi
    while theta <= -np.pi:
        theta = theta + 2 * np.pi
    return theta

@nb.jit(nopython=True)
def create_metric_network(agents, R, Fov):
    # R: length of attraction: maximum interaction range for agent
    # FOV: field of view [0, pi]---- agents[agent_index][19] = np.pi/2
    # get number of agents
    num_agents = agents.shape[0]
    # create a metric with N * N dimension
    metric_network = np.zeros(shape=(num_agents, num_agents))
    # loop agents
    for agent_index in range(num_agents):
        theta_i = agents[agent_index, 2]
        for neighbor_index in range(num_agents):
            if agent_index != neighbor_index:
                r_ij, theta_ij = Get_relative_distance_angle(agents[agent_index][0], agents[agent_index][1],
                                                             agents[neighbor_index][0], agents[neighbor_index][1])
                turning_angle = transform_angle(theta_i - theta_ij)  # theta_i, theta_ij<-- [-pi, pi];
                if r_ij <= R and (abs(turning_angle) <= Fov):
                    metric_network[agent_index, neighbor_index] = 1
                    metric_network[neighbor_index, agent_index] = 1
    return metric_network


def create_topological_network(agents):
    # get number of agents
    num_agents = agents.shape[0]
    # create a metric with N * N dimension
    distance_matrix = np.zeros(shape=(num_agents, num_agents))

    # create matrix with distance
    for agent_index in range(num_agents):
        for neighbor_index in range(num_agents):
            if neighbor_index != agent_index:
                distance, r_angle = Get_relative_distance_angle(agents[agent_index][0], agents[agent_index][1],
                                                                agents[neighbor_index][0], agents[neighbor_index][1])
                distance_matrix[agent_index][neighbor_index] = distance
                distance_matrix[neighbor_index][agent_index] = distance
    # rank neighbor by distance
    topological_network = np.argsort(distance_matrix)  #! including agent itsself
    return topological_network
