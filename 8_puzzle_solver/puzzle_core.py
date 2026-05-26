import copy
import random

class Node:
    __slots__ = ("state", "parent", "action", "path_cost")

    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

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
        child = Node(matrix, node, action, node.path_cost + 1)
        children.append(child)
        if log_cb:
            log_cb(child)
    return children

def child_node(problem: Problem, node: Node, action, log_cb=None):
    i, j = get_index(node.state)
    matrix = copy.deepcopy(node.state)
    di, dj = Problem.MOVES[action]
    matrix[i][j], matrix[i + di][j + dj] = matrix[i + di][j + dj], matrix[i][j]
    child = Node(matrix, node, action, node.path_cost + 1)
    if log_cb:
        log_cb(child)
    return child

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
                distance += abs(i - goal_i) + abs(j - goal_j)
                
    return distance