import random
import copy
from collections import deque


def get_index(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return (i, j)
    return None


class Problem:
    def __init__(self, start, goal, states, actions):
        self.start = start
        self.goal = goal
        self.states = states
        self.actions = actions
    
    def goal_test(self, state):
        return state == self.goal
    
    def get_actions(self, state):
        (i, j) = get_index(state)
        actions = []

        if i > 0: actions.append("up")
        if i < 2: actions.append("down")
        if j > 0: actions.append("left")
        if j < 2: actions.append("right")

        return actions

class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

def random_matrix():
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    matrix = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            num = random.choice(nums)
            matrix[i][j] = num
            nums.remove(num)
    return matrix

def tuple_matrix(matrix):
    return tuple(tuple(row) for row in matrix)

def child_node(problem: Problem, node: Node, action):
    (i, j) = get_index(node.state)
    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    matrix = copy.deepcopy(node.state)
    di, dj = moves[action]
    matrix[i][j], matrix[i + di][j + dj] = matrix[i + di][j + dj], matrix[i][j]
    
    return Node(matrix, node, action, node.path_cost+1)

def eight_puzzel(problem: Problem):
    node = Node(problem.start, None, None, 0)
    
    if problem.goal_test(node.state): return node 
    
    frontier = deque()
    frontier.append(node)
    frontier_states = set()
    frontier_states.add(tuple_matrix(node.state))
    
    explored = set()

    while frontier:
        node = frontier.popleft()
        
        explored.add(tuple_matrix(node.state))
        
        for action in problem.get_actions(node.state):
            child = child_node(problem, node, action)
                        
            if tuple_matrix(child.state) not in explored and tuple_matrix(child.state) not in frontier_states:
                if problem.goal_test(child.state): 
                    return child
                
                frontier.append(child)
                frontier_states.add(tuple_matrix(child.state)) 

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