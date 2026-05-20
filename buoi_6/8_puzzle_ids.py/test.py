import random
import copy

class Problem:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def goal_test(self, state):
        return state == self.goal

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
    random.shuffle(nums)
    return [nums[i:i+3] for i in range(0, 9, 3)]

def tuple_matrix(matrix):
    return tuple(tuple(row) for row in matrix)

# Kiểm tra tính giải được của trạng thái
def is_solvable(matrix):
    flat_list = [num for row in matrix for num in row if num != 0]
    inversions = sum(1 for i in range(len(flat_list)) for j in range(i + 1, len(flat_list)) if flat_list[i] > flat_list[j])
    return inversions % 2 == 0

def get_actions(i, j):
    actions = []
    if i > 0: actions.append("up")
    if i < 2: actions.append("down")
    if j > 0: actions.append("left")
    if j < 2: actions.append("right")
    return actions

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
        child = Node(matrix, node, a, node.path_cost + 1)
        children.append(child)
   
    return children

def depth_limited_search(problem: Problem, l):
    node = Node(problem.start, None, None, 0)
    if problem.goal_test(node.state): 
        return node

    frontier = [node]
    reached = {tuple_matrix(problem.start)}

    res = False
    while frontier:
        node = frontier.pop()
        
        if problem.goal_test(node.state): 
            return node
            
        if node.path_cost >= l:
            res = "cutoff"
        else:
            for child in expand(problem, node):
                child_tuple = tuple_matrix(child.state)
                if child_tuple not in reached:
                    reached.add(child_tuple)
                    frontier.append(child)
                    
    return res

def eight_puzzel(problem: Problem):
    for depth in range(0, 1000):
        res = depth_limited_search(problem, depth)
        if res != "cutoff": 
            return res
    return False

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    states = []
    problem = Problem(matrix, goal)

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