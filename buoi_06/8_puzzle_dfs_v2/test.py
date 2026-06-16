import random
import copy
from collections import deque


class Problem:
    def __init__(self, start, goal, states, actions):
        self.start = start
        self.goal = goal
        self.states = states
        self.actions = actions


class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost


    def get_index(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return None


def random_matrix():
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    matrix = [[0 for _ in range(3)] for _ in range(3)]
    
    for i in range(3):
        for j in range(3):
            num = random.choice(nums)
            matrix[i][j] = num
            nums.remove(num)

    return matrix


def get_actions(i, j):
    actions = []

    if i > 0: actions.append("up")
    if i < 2: actions.append("down")
    if j > 0: actions.append("left")
    if j < 2: actions.append("right")

    return actions


def tuple_matrix(matrix):
    return tuple(tuple(row) for row in matrix)


def expand(problem: Problem, node: Node):
    (i, j) = node.get_index()
    actions = get_actions(i, j)
    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    children = []
    for a in actions:
        matrix = copy.deepcopy(node.state)
        di, dj = moves[a]
        matrix[i][j], matrix[i + di][j + dj] = matrix[i + di][j + dj], matrix[i][j]
        child = Node(matrix, node, a, node.path_cost+1)
        children.append(child)
   
    return children


def eight_puzzel(problem: Problem):
    node = Node(problem.start, None, None, 0)
    if node.state == problem.goal: return node

    frontier = []; frontier.append(node)
    frontier_states = set(); frontier_states.add(tuple_matrix(node.state))
    reached = set(); reached.add(tuple_matrix(problem.start))

    while frontier:
        node = frontier.pop()
        for child in expand(problem, node):
            s = child.state
            if s == problem.goal: return child
            if tuple_matrix(s) not in reached and tuple_matrix(s) not in frontier_states:
                reached.add(tuple_matrix(s))
                frontier.append(child)
                frontier_states.add(tuple_matrix(s))
            
    return False


if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    states = []
    problem = Problem(matrix, goal, None, None)

    for row in matrix:
        print(row)

    res_node = eight_puzzel(problem)
    if res_node == False:
        print("Không giải được")
    else:
        res = []
        while res_node.parent != None:
            res.append(res_node)
            res_node = res_node.parent

        res.reverse()
        for node in res:
            print(node.action)
            for row in node.state:
                print(row)