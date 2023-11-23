import numba as nb
import numpy as np
import matplotlib.pyplot as plt
import math


@nb.jit(nopython=True)
def create_neighbor_map_euc(agents):
    num_agents = agents.shape[0]
    map = np.zeros(shape=(num_agents, num_agents))
    R = agents[0][5]  # length of attraction

    for agent_index in range(num_agents):

        x_i = agents[agent_index, 0]
        y_i = agents[agent_index, 1]
        theata_i = agents[agent_index, 2]
        Fov = agents[agent_index][19]  # field of view np.pi/2

        for neighbor_index in range(num_agents):
            if agent_index != neighbor_index:
                x_j = agents[neighbor_index, 0]
                y_j = agents[neighbor_index, 1]
                r_x = x_j - x_i
                r_y = y_j - x_j
                theata_j = math.atan2(r_y, r_x)
                theata_ij = theata_i - theata_j
                if ((x_i + R) >= x_j) and ((x_i - R) <= x_j):  # and (abs(theata_ij) <= Fov):
                    if ((y_i + R) >= y_j) and ((y_i - R) <= y_j):
                        map[agent_index, neighbor_index] = 1
        # print("map:", map)
    return map


@nb.jit(nopython=True)
def reflect_angle(angle):
    # while theata >= np.pi:
    #     theata = theata - 2 * np.pi
    # while theata <= -np.pi:
    #     theata = theata + 2 * np.pi
    # return theata
    while angle >= 2 * np.pi:
        angle = angle - 2 * np.pi
    while angle <= 0:
        angle = angle + 2 * np.pi
    return angle


@nb.jit(nopython=True)
def avoid_shepherd(agents, shepherd):
    num_agents = agents.shape[0]
    num_shepherd = shepherd.shape[0]

    num_shepherd_avoid = np.zeros(agents.shape[0])
    distance_shepherd_avoid = np.zeros(agents.shape[0])
    angle_shepherd_avoid = np.zeros(agents.shape[0])
    for agent_index in range(num_agents):
        r_x = 0
        r_y = 0
        x_i = agents[agent_index][0]
        y_i = agents[agent_index][1]
        safe_distance = agents[agent_index][17]  # safe_distance
        num_j = 0
        for shepherd_index in range(num_shepherd):
            x_j = shepherd[shepherd_index][0]
            y_j = shepherd[shepherd_index][1]
            distance = np.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)
            if distance <= safe_distance:
                num_j = num_j + 1
                r_x = r_x + (x_i - x_j)
                r_y = r_y + (y_i - y_j)
        if num_j != 0:
            r_x = r_x / num_j
            r_y = r_y / num_j
            angle = math.atan2(r_y, r_x)
            angle_shepherd_avoid[agent_index] = reflect_angle(angle)  # force_of_shepherd  agents[agent_index][8]
        num_shepherd_avoid[agent_index] = num_j
        distance_shepherd_avoid[agent_index] = np.sqrt(r_x ** 2 + r_y ** 2)
    return agents, num_shepherd_avoid, distance_shepherd_avoid, angle_shepherd_avoid


@nb.jit(nopython=True)
def avoid(update_map, agents):
    num_agents = agents.shape[0]
    num_avoid = np.zeros(agents.shape[0])
    Distance_avoid = np.zeros(agents.shape[0])
    angle_avoid = np.zeros(agents.shape[0])
    for agent_index in range(num_agents):
        neighbor_num = 0
        r_x = 0
        r_y = 0
        x_i = agents[agent_index][0]
        y_i = agents[agent_index][1]
        for neighbor_index in range(num_agents):
            if (agent_index != neighbor_index): #and (update_map[agent_index, neighbor_index] == 1):
                x_j = agents[neighbor_index][0]
                y_j = agents[neighbor_index][1]
                distance = np.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)
                if distance <= agents[0][3]:  # R_repulsion
                    neighbor_num = neighbor_num + 1
                    r_x = r_x + (x_i - x_j)
                    r_y = r_y + (y_i - y_j)
        if neighbor_num != 0:
            r_x = r_x / neighbor_num
            r_y = r_y / neighbor_num
            theata = math.atan2(r_y, r_x)
            angle_avoid[agent_index] = reflect_angle(theata)  # vector_repulsion
            num_avoid[agent_index] = neighbor_num
            Distance_avoid[agent_index] = np.sqrt(r_x ** 2 + r_y ** 2)
    return agents, num_avoid, Distance_avoid, angle_avoid


@nb.jit(nopython=True)
def align(map, agents):
    num_agents = agents.shape[0]
    num_align = np.zeros(agents.shape[0])
    angle_align = np.zeros(agents.shape[0])
    map_align = map
    for agent_index in range(num_agents):
        Theata_sum = 0  # theata_i
        neighbor_num = 0
        x_i = agents[agent_index][0]
        y_i = agents[agent_index][1]
        theata_i = agents[agent_index][2]
        for neighbor_index in range(num_agents):
            if (agent_index != neighbor_index) and (map_align[agent_index, neighbor_index] == 1):
                x_j = agents[neighbor_index, 0]
                y_j = agents[neighbor_index, 1]
                distance = np.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)
                if (distance < agents[0][4]) and (distance > agents[0][3]):  # R_alignment
                    neighbor_num = neighbor_num + 1
                    Theata_sum = Theata_sum + agents[neighbor_index][2]  # theata_j
        if neighbor_num != 0:
            angle = (Theata_sum + theata_i) / (neighbor_num + 1)
            angle_align[agent_index] = reflect_angle(angle)  # vector_alignment agents[agent_index][8]
        num_align[agent_index] = neighbor_num
    return agents, num_align, angle_align


@nb.jit(nopython=True)
def attract(agents):
    num_agents = agents.shape[0]
    map_att = np.zeros(shape=(num_agents, num_agents))
    num_att = np.zeros(agents.shape[0])
    distance_att = np.zeros(agents.shape[0])
    angle_att = np.zeros(agents.shape[0])
    for agent_index in range(num_agents):
        neighbor_num = 0
        r_x = 0
        r_y = 0
        x_i = agents[agent_index][0]
        y_i = agents[agent_index][1]
        for neighbor_index in range(num_agents):
            if agent_index != neighbor_index:  # and (map_att[agent_index, neighbor_index] == 1)
                x_j = agents[neighbor_index][0]
                y_j = agents[neighbor_index][1]
                distance = np.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)
                if (distance >= agents[0][3]) and (distance <= agents[0][5]):
                    neighbor_num = neighbor_num + 1
                    r_x = r_x + (x_j - x_i)
                    r_y = r_y + (y_j - y_i)
                    map_att[agent_index, neighbor_index] = 1
                if distance > agents[0][5]:
                    map_att[agent_index, neighbor_index] = 0
        if neighbor_num > 0:
            r_x = r_x / neighbor_num
            r_y = r_y / neighbor_num
            angle = math.atan2(r_y, r_x)
            angle_att[agent_index] = reflect_angle(angle)  # [0, 2*pi]
            num_att[agent_index] = neighbor_num
            distance_att[agent_index] = np.sqrt(r_x ** 2 + r_y ** 2) - agents[0][3] ## distance = 0 at the edge of repulsion range
    return agents, num_att, distance_att, angle_att, map_att


@nb.jit(nopython=True)
def update_agents_state(agents, target_x, target_y, target_size):
    num_agents = agents.shape[0]
    for agent_index in range(num_agents):
        agent_x = agents[agent_index][0]
        agent_y = agents[agent_index][1]
        distance, angle = Get_relative_distance_angle(agent_x, agent_y, target_x, target_y)
        if distance <= target_size:
            agents[agent_index][21] = 1  # agent state: 0 -> moving; 1 -> staying;
            agents[agent_index][3] = 0  # v_0 =0
        else:
            agents[agent_index][21] = 0
    return


@nb.jit(nopython=True)
def update(agents, shepherd):  # map,
    num_agents = agents.shape[0]
    agents, num_att, distance_att, angle_att, updated_map = attract(agents)  # update the map as well
    agents, num_avoid, distance_avoid, angle_avoid = avoid(updated_map, agents)
    agents, num_align, angle_align = align(updated_map, agents)
    agents, num_shepherd, distance_shepherd, angle_shepherd_avoid = avoid_shepherd(agents, shepherd)
    v0 = agents[0][6]
    K_repulsion_agent = agents[0][10]  # K_repulsion_agent
    K_attraction_agent = agents[0][11]  # K_attraction_agent
    K_repulsion_shepherd = agents[0][12]  # K_repulsion_shepherd
    K_Dr = agents[0][13]  # noise_strength
    tick_time = agents[0][14]  # tick_time
    alpha = agents[0][15]  # alpha: acceleration rate
    beta = agents[0][16]  # beta: turning rate
    dis_repulsion = agents[0][3]
    max_turning_angle = agents[0][18]  # np.pi*2/3

    for agent_index in range(num_agents):
        agent_state = agents[agent_index][21]
        # if agent_state == 0:  # moving
        f_avoid_agent_x = 0
        f_avoid_agent_y = 0
        f_att_agent_x = 0
        f_att_agent_y = 0
        f_avoid_shepherd_x = 0
        f_avoid_shepherd_y = 0
        if num_avoid[agent_index] != 0:  # repulsion_force_of_agents, highest priority
            f_avoid_agent_x = ((dis_repulsion - distance_avoid[agent_index])**3) * np.cos(angle_avoid[agent_index]) #(1 / distance_avoid[agent_index])
            f_avoid_agent_y = ((dis_repulsion - distance_avoid[agent_index])**3) * np.sin(angle_avoid[agent_index]) #(1 / distance_avoid[agent_index])

        if num_att[agent_index] != 0:  # attraction_force_of_agents
            f_att_agent_x = (distance_att[agent_index]) * np.cos(angle_att[agent_index])
            f_att_agent_y = (distance_att[agent_index]) * np.sin(angle_att[agent_index])

        if num_shepherd[agent_index] != 0:  # avoid shepherd
            f_avoid_shepherd_x = distance_shepherd[agent_index] * np.cos(angle_shepherd_avoid[agent_index])
            f_avoid_shepherd_y = distance_shepherd[agent_index] * np.sin(angle_shepherd_avoid[agent_index])

        if num_avoid[agent_index] != 0:   #### first priority!!!
            f_x = f_avoid_agent_x * K_repulsion_agent
            f_y = f_avoid_agent_y * K_repulsion_agent
        else:
            f_x = f_att_agent_x * K_attraction_agent + f_avoid_shepherd_x * K_repulsion_shepherd
            f_y = f_att_agent_y * K_attraction_agent + f_avoid_shepherd_y * K_repulsion_shepherd

        # f_x = f_avoid_agent_x * K_repulsion_agent + f_att_agent_x * K_attraction_agent + f_avoid_shepherd_x * K_repulsion_shepherd
        # f_y = f_avoid_agent_y * K_repulsion_agent + f_att_agent_y * K_attraction_agent + f_avoid_shepherd_y * K_repulsion_shepherd

        v_dot = f_x * np.cos(agents[agent_index][2]) + f_y * np.sin(agents[agent_index][2])
        w_dot = (-f_x * np.sin(agents[agent_index][2]) + f_y * np.cos(agents[agent_index][2]))  # inertia (1 / v0) *

        if w_dot > max_turning_angle:
            w_dot = max_turning_angle
        if w_dot <= -max_turning_angle:
            w_dot = -max_turning_angle
        Dr = np.sqrt(2 * K_Dr) / (tick_time ** 0.5) * np.random.normal(0, 1)
        agents[agent_index][0] = agents[agent_index][0] + (v0 + v_dot * alpha) * np.cos(
            agents[agent_index][2]) * tick_time  # alpha = 1 acceleration
        agents[agent_index][1] = agents[agent_index][1] + (v0 + v_dot * alpha) * np.sin(
            agents[agent_index][2]) * tick_time  # beta = 1 turning rate
        agents[agent_index][2] = reflect_angle(agents[agent_index][2] + (w_dot * beta + Dr) * tick_time)
    return agents, updated_map


@nb.jit(nopython=True)
def Get_relative_distance_angle(target_x, target_y, focal_agent_x, focal_agent_y):
    r_x = target_x - focal_agent_x
    r_y = target_y - focal_agent_y
    r_length = np.sqrt(r_x ** 2 + r_y ** 2)
    r_angle = np.arctan2(r_y, r_x)  # range[-pi, pi]
    return r_length, r_angle


@nb.jit(nopython=True)
def Get_furthest_agent(agents, shepherd_x, shepherd_y, target_place_x, target_place_y):
    num_agents = agents.shape[0]
    angle_herd_agents = np.zeros(agents.shape[0])
    distance_herd_agents = np.zeros(agents.shape[0])
    dirt_angles_of_target_to_agent = np.zeros(agents.shape[0])

    r_target, angle_target_herd = Get_relative_distance_angle(target_place_x, target_place_y, shepherd_x, shepherd_y)
    for agent_index in range(num_agents):
        if agents[agent_index][21] == 0:  # in the moving state
            agent_x = agents[agent_index][0]
            agent_y = agents[agent_index][1]
            r_agent_herd, angle_agent_herd = Get_relative_distance_angle(agent_x, agent_y, shepherd_x, shepherd_y)
            angle_herd_agents[agent_index] = angle_agent_herd  # [-pi, pi]
            dirt_angle_from_target_to_herd = angle_target_herd - angle_agent_herd  # original: [-2*pi,2*pi]
            while angle_agent_herd >= np.pi:
                angle_agent_herd = angle_agent_herd - 2 * np.pi
            while angle_agent_herd <= -np.pi:
                angle_agent_herd = angle_agent_herd + 2 * np.pi
            dirt_angles_of_target_to_agent[agent_index] = dirt_angle_from_target_to_herd  # angle between two vector: [-np.pi, np.pi]

            distance_herd_agents[agent_index] = r_agent_herd
            # dirt_angles_of_target_to_agent[agent_index] = reflect_angle(angle_target_herd - angle_agent_herd)  # original: [-pi,2*pi]

    max_agent_index = int(np.argmax(np.absolute(angle_herd_agents)))  # +: clockwise, -: anti-clockwise

    return max_agent_index, distance_herd_agents[max_agent_index]


@nb.jit(nopython=True)
def collect_furthest_agent(agent_x, agent_y, shepherd_x, shepherd_y, target_place_x, target_place_y, l0):
    # collect_point_1
    distance_agent_target, angle_agent_target = Get_relative_distance_angle(agent_x, agent_y, target_place_x,
                                                                            target_place_y)
    collect_point_x = agent_x + l0 * np.cos(angle_agent_target)
    collect_point_y = agent_y + l0 * np.sin(angle_agent_target)
    distance_cp_herd, angle_cp_herd = Get_relative_distance_angle(collect_point_x, collect_point_y, shepherd_x,
                                                                  shepherd_y)
    force_x = distance_cp_herd * np.cos(angle_cp_herd)  #
    force_y = distance_cp_herd * np.sin(angle_cp_herd)  #
    return collect_point_x, collect_point_y, force_x, force_y


@nb.jit(nopython=True)
def drive_the_herd(agents, shepherd_x, shepherd_y, shepherd_angle, target_place_x, target_place_y, l1, k):
    center_of_mass_x = np.mean(agents[:, 0])
    center_of_mass_y = np.mean(agents[:, 1])

    distance_mass_target, angle_mass_target = Get_relative_distance_angle(center_of_mass_x, center_of_mass_y,
                                                                          target_place_x, target_place_y)
    drive_point_x = center_of_mass_x + l1 * np.cos(angle_mass_target)
    drive_point_y = center_of_mass_y + l1 * np.sin(angle_mass_target)
    distance_drive_herd, angle_drive_herd = Get_relative_distance_angle(drive_point_x, drive_point_y,
                                                                        shepherd_x, shepherd_y)
    force_x = distance_drive_herd * np.cos(angle_drive_herd)  #
    force_y = distance_drive_herd * np.sin(angle_drive_herd)  #
    return force_x, force_y


@nb.jit(nopython=True)
def keep_distance_from_other_shepherd(shepherd):
    angle_other_shepherd = np.zeros(shepherd.shape[0])
    distance_other_shepherd = np.zeros(shepherd.shape[0])
    l3 = shepherd[0][19]  # L3 Equilibrium distance from other shepherd
    for shepherd_index in range(shepherd.shape[0]):
        x_i = shepherd[shepherd_index][0]
        y_i = shepherd[shepherd_index][1]
        neighbor_num = 0
        r_x = 0
        r_y = 0
        for neighbor_index in range(shepherd.shape[0]):
            if shepherd_index != neighbor_index:
                x_j = shepherd[neighbor_index][0]
                y_j = shepherd[neighbor_index][1]
                distance = np.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)
                if distance <= l3:  # Distance_from_other_shepherd
                    neighbor_num = neighbor_num + 1
                    r_x = r_x + (x_i - x_j)
                    r_y = r_y + (y_i - y_j)
        if neighbor_num != 0:
            r_x = r_x / neighbor_num
            r_y = r_y / neighbor_num
            angle = math.atan2(r_y, r_x)
            angle_other_shepherd[shepherd_index] = reflect_angle(angle)  # Angle of the repulsion vector
            distance_other_shepherd[shepherd_index] = np.sqrt(r_x ** 2 + r_y ** 2)  # Distance of the repulsion vector

    return distance_other_shepherd, angle_other_shepherd

@nb.jit(nopython=True)
def herd(agents, shepherd, target_place_x, target_place_y):
    max_agents_indexes = np.zeros(shepherd.shape[0])  # record the furthest agent index
    l0 = shepherd[0][3]
    k = shepherd[0][4]
    l1 = shepherd[0][5]  # distance from the center of mass to the drive point
    v0 = shepherd[0][6]
    alpha = shepherd[0][7]
    beta = shepherd[0][8]
    Dr = shepherd[0][9]
    tick_time = shepherd[0][10]
    max_turning_rate = shepherd[0][11]
    d_furthest = shepherd[0][12]
    K_attraction_target = shepherd[0][18]
    center_of_mass_x = np.mean(agents[:, 0])
    center_of_mass_y = np.mean(agents[:, 1])

    distance_other_shepherd, angle_other_shepherd = keep_distance_from_other_shepherd(shepherd)

    for shepherd_index in range(shepherd.shape[0]):
        shepherd_x = shepherd[shepherd_index][0]
        shepherd_y = shepherd[shepherd_index][1]
        shepherd_angle = shepherd[shepherd_index][2]

        # repulsion from other shepherd
        f_x_other_shepherd = distance_other_shepherd[shepherd_index] * np.cos(angle_other_shepherd[shepherd_index])
        f_y_other_shepherd = distance_other_shepherd[shepherd_index] * np.sin(angle_other_shepherd[shepherd_index])

        if shepherd[shepherd_index][13] == 1.0:
            # drive_mode: attract by the mass and the target + repulsion from other shepherd
            force_x, force_y = drive_the_herd(agents, shepherd_x, shepherd_y, shepherd_angle,
                                              target_place_x, target_place_y, l1, k)
            distance_shepherd_target, angle_shepherd_target = Get_relative_distance_angle(target_place_x,
                                                                                          target_place_y,
                                                                                          shepherd_x, shepherd_y)
            f_att_target_x = np.cos(angle_shepherd_target) * distance_shepherd_target * K_attraction_target
            f_att_target_y = np.sin(angle_shepherd_target) * distance_shepherd_target * K_attraction_target

            F_x = f_x_other_shepherd + f_att_target_x + force_x
            F_y = f_y_other_shepherd + f_att_target_y + force_y
            shepherd[shepherd_index][14] = np.mean(agents[:, 0])   # collect_x
            shepherd[shepherd_index][15] = np.mean(agents[:, 1])   # collect_y

            max_agent_index, r_agent = Get_furthest_agent(agents, shepherd_x, shepherd_y, target_place_x, target_place_y)

            agent_x = agents[int(max_agent_index)][0]
            agent_y = agents[int(max_agent_index)][1]
            max_agents_indexes[shepherd_index] = int(max_agent_index)
            distance_agent_mass, angle_agent_mass = Get_relative_distance_angle(agent_x, agent_y,
                                                                                center_of_mass_x, center_of_mass_y, )
            if distance_agent_mass > d_furthest:
                shepherd[shepherd_index][13] = 0.0  # collect_mode = true
                shepherd[shepherd_index][16] = int(max_agent_index)
        else:
            # collect mode: attract by the furthest agent and repulsion from other shepherd
            agent_x = agents[int(shepherd[shepherd_index][16])][0]
            agent_y = agents[int(shepherd[shepherd_index][16])][1]
            collect_point_x, collect_point_y, force_x, force_y = collect_furthest_agent(agent_x, agent_y,
                                                                                        shepherd_x, shepherd_y,
                                                                                        center_of_mass_x,
                                                                                        center_of_mass_y,
                                                                                        l0)
            F_x = f_x_other_shepherd + force_x
            F_y = f_y_other_shepherd + force_y
            shepherd[shepherd_index][14] = collect_point_x
            shepherd[shepherd_index][15] = collect_point_y
            distance_agent_mass, angle_agent_mass = Get_relative_distance_angle(collect_point_x, collect_point_y,
                                                                                center_of_mass_x, center_of_mass_y)
            if distance_agent_mass <= d_furthest:
                shepherd[shepherd_index][13] = 1.0  # drive_mode_true

        v_dot = F_x * np.cos(shepherd_angle) + F_y * np.sin(shepherd_angle)  # heading_direction_acceleration
        w_dot = -F_x * np.sin(shepherd_angle) + F_y * np.cos(shepherd_angle)  # angular_acceleration

        noise = np.sqrt(2 * Dr) / (tick_time ** 0.5) * np.random.normal(0, 1)
        shepherd[shepherd_index][0] = shepherd_x + ((v0 + v_dot * alpha) * np.cos(shepherd_angle)) * tick_time
        shepherd[shepherd_index][1] = shepherd_y + ((v0 + v_dot * alpha) * np.sin(shepherd_angle)) * tick_time
        shepherd[shepherd_index][2] = reflect_angle(shepherd_angle + (w_dot / v0 * beta + noise) * tick_time)
    return shepherd, max_agents_indexes


def make_preodic_boundary(agents, space_x, space_y):
    # how to calculate preodic distance?
    num_agents = agents.shape[0]
    for agent_index in range(num_agents):
        agent_x = agents[agent_index][0]
        agent_y = agents[agent_index][1]
        if agent_x < -space_x / 2:
            agent_x += space_x
        elif agent_x >= space_x / 2:
            agent_x -= space_x
        if agent_y < -space_y / 2:
            agent_y += space_y
        elif agent_y >= space_y / 2:
            agent_y -= space_y
        agents[agent_index][0] = agent_x
        agents[agent_index][1] = agent_y
    return agents


@nb.jit(nopython=True)
def evolve(agents, shepherd, Target_place_x, Target_place_y, Target_size):
    # map = create_neighbor_map_euc(agents)
    # agents_update, updated_map = update(map, agents, shepherd)
    agents_update, updated_map = update(agents, shepherd)
    shepherd_update, max_agents_indexes = herd(agents, shepherd, Target_place_x, Target_place_y)
    update_agents_state(agents, Target_place_x, Target_place_y, Target_size)
    return updated_map, agents_update, shepherd_update, max_agents_indexes
