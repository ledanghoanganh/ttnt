from collections import deque
from puzzle_core import Node, Problem, tuple_matrix, child_node, random_matrix, is_solvable

def bfs_v2(problem: Problem, log_cb=None):
    if not is_solvable(problem.start, problem.goal):
        return False, 0

    node = Node(problem.start, None, None, 0)
    if problem.goal_test(node.state):
        return node, 0

    frontier = deque([node])
    frontier_set = {tuple_matrix(node.state)}
    explored = set()

    while frontier:
        node = frontier.popleft()
        explored.add(tuple_matrix(node.state))

        for action in problem.get_actions(node.state):
            child = child_node(problem, node, action, log_cb)
            if tuple_matrix(child.state) not in explored and tuple_matrix(child.state) not in frontier_set:
                if problem.goal_test(child.state):
                    return child, len(explored)
                frontier.append(child)
                frontier_set.add(tuple_matrix(child.state))

    return False, len(explored)

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, count = bfs_v2(problem)
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