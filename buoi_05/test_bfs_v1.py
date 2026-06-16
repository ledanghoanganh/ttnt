from collections import deque
from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix, is_solvable

def bfs_v1(problem: Problem, log_cb=None):
    if not is_solvable(problem.start, problem.goal):
        return False, 0

    node = Node(problem.start, None, None, 0)
    frontier = deque([node])
    frontier_states = {tuple_matrix(node.state)}
    reached = set()

    while frontier:
        node = frontier.popleft()
        
        if problem.goal_test(node.state): 
            return node, len(reached)
            
        reached.add(tuple_matrix(node.state))

        for child in expand(problem, node, log_cb):
            c = tuple_matrix(child.state)
            if c not in reached and c not in frontier_states:
                frontier.append(child)    
                frontier_states.add(c)    

    return False, len(reached)

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, count = bfs_v1(problem)
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