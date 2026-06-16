import copy
import random

class Node:

    def __init__(self, state, parent, action, path_cost=0, g_cost=0, h_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.g_cost = g_cost
        self.h_cost = h_cost

    def __lt__(self, other):
        return (self.g_cost + self.h_cost) < (other.g_cost + other.h_cost)

class Problem:
    MOVES = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def goal_test(self, state):
        return state == self.goal

    def get_actions(self, state):
        i, j = get_index(state)
        actions = []
        if i > 0: actions.append("up")
        if i < 2: actions.append("down")
        if j > 0: actions.append("left")
        if j < 2: actions.append("right")
        return actions

def get_index(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return (i, j)
    return None

def tuple_matrix(m):
    return tuple(tuple(r) for r in m)

def random_matrix():
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    matrix = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            num = random.choice(nums)
            matrix[i][j] = num
            nums.remove(num)
    return matrix

def expand(problem: Problem, node: Node, log_cb=None):
    i, j = get_index(node.state)
    children = []
    for action in problem.get_actions(node.state):
        matrix = copy.deepcopy(node.state)
        di, dj = Problem.MOVES[action]
        matrix[i][j], matrix[i + di][j + dj] = matrix[i + di][j + dj], matrix[i][j]
        child = Node(matrix, node, action, node.path_cost + 1, node.g_cost + number_of_wrong(matrix, problem.goal), manhattan_distance(matrix, problem.goal))
        children.append(child)
        if log_cb:
            log_cb(child)
    return children

def child_node(problem: Problem, node: Node, action, log_cb=None):
    i, j = get_index(node.state)
    matrix = copy.deepcopy(node.state)
    di, dj = Problem.MOVES[action]
    matrix[i][j], matrix[i + di][j + dj] = matrix[i + di][j + dj], matrix[i][j]
    child = Node(matrix, node, action, node.path_cost + 1, node.g_cost + number_of_wrong(matrix, problem.goal), manhattan_distance(matrix, problem.goal))
    if log_cb:
        log_cb(child)
    return child

def number_of_wrong(state, goal):
    count = 0
    
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j]:
                count += 1

    return count

def manhattan_distance(state, goal):
    distance = 0
    goal_positions = {}

    for i in range(3):
        for j in range(3):
            val = goal[i][j]
            if val != 0:
                goal_positions[val] = (i, j)
                
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                goal_i, goal_j = goal_positions[val]
                distance += (abs(i - goal_i) + abs(j - goal_j))

    return distance

def count_inversions(state):
    flat_list = []
    for row in state:
        for val in row:
            if val != 0:
                flat_list.append(val)
                
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
                
    return inversions

def is_solvable(start, goal):
    start_inv = count_inversions(start)
    goal_inv = count_inversions(goal)
    # Trạng thái giải được nếu số cặp nghịch thế của start và goal có cùng tính chẵn lẻ
    return (start_inv % 2) == (goal_inv % 2)