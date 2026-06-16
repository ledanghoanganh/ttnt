from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix, is_solvable

def depth_limited_search(problem: Problem, l: int, log_cb=None):
    node = Node(problem.start, None, None, 0)
    if problem.goal_test(node.state):
        return node, 0

    frontier = [node]
    reached = {tuple_matrix(node.state)}
    res = False
    
    while frontier:
        reached_count = len(reached)
        node = frontier.pop()

        if problem.goal_test(node.state):
            return node, reached_count

        if node.path_cost >= l:
            res = "cutoff"
        else:
            for child in expand(problem, node, log_cb):
                child_tuple = tuple_matrix(child.state)
                if child_tuple not in reached:
                    reached.add(child_tuple)
                    frontier.append(child)

    return res, len(reached)

def ids(problem: Problem, log_cb=None):
    if not is_solvable(problem.start, problem.goal):
        return False, 0

    for depth in range(0, 1000):
        res, count = depth_limited_search(problem, depth, log_cb)
        if res != "cutoff":
            return res, count
    return False, 0

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, count = ids(problem)
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