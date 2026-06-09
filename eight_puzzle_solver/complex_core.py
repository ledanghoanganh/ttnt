import itertools
import copy
from puzzle_core import Node, Problem, tuple_matrix

def expand_partial_state(matrix):
    missing_positions = []
    seen = set()
    for i in range(3):
        for j in range(3):
            val = matrix[i][j]
            if val == '?':
                missing_positions.append((i, j))
            else:
                seen.add(int(val))
    
    missing_nums = set(range(9)) - seen
    if len(missing_nums) != len(missing_positions):
        return
    
    for perm in itertools.permutations(missing_nums):
        new_mat = [list(row) for row in matrix]
        for (i, j), num in zip(missing_positions, perm):
            new_mat[i][j] = num
        yield new_mat

def get_first_two_states(states_list):
    if not states_list:
        return None
        
    if len(states_list) >= 2:
        gen1 = expand_partial_state(states_list[0])
        gen2 = expand_partial_state(states_list[1])
        s1 = next(gen1, None)
        s2 = next(gen2, None)
        
        if s1 and s2:
            return (tuple_matrix(s1), tuple_matrix(s2))
        elif s1:
            return (tuple_matrix(s1), tuple_matrix(s1))
        elif s2:
            return (tuple_matrix(s2), tuple_matrix(s2))
        else:
            return None
    else:
        gen = expand_partial_state(states_list[0])
        s1 = next(gen, None)
        s2 = next(gen, None)
        if s1 and s2:
            return (tuple_matrix(s1), tuple_matrix(s2))
        elif s1:
            return (tuple_matrix(s1), tuple_matrix(s1))
        else:
            return None

def get_initial_belief_state(starts):
    return get_first_two_states(starts)

def get_target_goal_states(goals):
    return get_first_two_states(goals)

class ComplexNode:
    def __init__(self, belief_state, parent, action, path_cost=0, g_cost=0, h_cost=0):
        self.state = belief_state
        self.belief_state = belief_state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.g_cost = g_cost
        self.h_cost = h_cost

    def __lt__(self, other):
        return (self.g_cost + self.h_cost) < (other.g_cost + other.h_cost)

def get_applicable_actions(belief_state):
    return ["up", "down", "left", "right"]

def apply_action(belief_state, action):
    moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
    new_belief = []
    di, dj = moves[action]
    
    for state in belief_state:
        i, j = None, None
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    i, j = r, c
                    break
                    
        if 0 <= i + di < 3 and 0 <= j + dj < 3:
            new_state = [list(row) for row in state]
            new_state[i][j], new_state[i + di][j + dj] = new_state[i + di][j + dj], new_state[i][j]
            new_belief.append(tuple_matrix(new_state))
        else:
            new_belief.append(state)
            
    return tuple(new_belief)

def is_goal(belief_state, target_goals):
    for state in belief_state:
        if state not in target_goals:
            return False
    return True

def manhattan_distance_tuple(state, target):
    distance = 0
    goal_positions = {}

    for i in range(3):
        for j in range(3):
            val = target[i][j]
            if val != 0:
                goal_positions[val] = (i, j)
                
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                goal_i, goal_j = goal_positions[val]
                distance += (abs(i - goal_i) + abs(j - goal_j))

    return distance

def complex_h_cost(belief_state, target_goals):
    dist_s1 = min(manhattan_distance_tuple(belief_state[0], g) for g in target_goals)
    dist_s2 = min(manhattan_distance_tuple(belief_state[1], g) for g in target_goals)
    return min(dist_s1, dist_s2)
