import copy
from collections import deque

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

class PuzzleModel:
    def __init__(self):
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.reached_count = 0
        self.solution_nodes = []

    def tuple_matrix(self, matrix):
        return tuple(tuple(row) for row in matrix)

    def get_actions(self, i, j):
        actions = []
        if i > 0: actions.append("up")
        if i < 2: actions.append("down")
        if j > 0: actions.append("left")
        if j < 2: actions.append("right")
        return actions

    def expand(self, node):
        i, j = node.get_index()
        actions = self.get_actions(i, j)
        moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        children = []
        for a in actions:
            matrix = copy.deepcopy(node.state)
            di, dj = moves[a]
            matrix[i][j], matrix[i + di][j + dj] = matrix[i + di][j + dj], matrix[i][j]
            child = Node(matrix, node, a, node.path_cost + 1)
            children.append(child)
        return children

    def eight_puzzel(self, start_matrix):
        node = Node(start_matrix, None, None, 0)
        frontier = deque(); frontier.append(node)
        frontier_states = set(); frontier_states.add(self.tuple_matrix(node.state))
        reached = set()

        while frontier:
            node = frontier.popleft() 
            if node.state == self.goal: return node
            
            reached.add(self.tuple_matrix(node.state))
            self.reached_count = len(reached)

            for child in self.expand(node):
                c = self.tuple_matrix(child.state)
                if c not in reached and c not in frontier_states:
                    frontier.append(child)    
                    frontier_states.add(c)    

        return False
    
    def get_solution(self, node):
        res = []
        while node.parent is not None:
            res.append(node)
            node = node.parent
        res.reverse()
        self.solution_nodes = res
