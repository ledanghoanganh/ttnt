from puzzle_core import Node, Problem, tuple_matrix, expand


def _depth_limited_search(problem: Problem, limit, log_cb=None):
    node = Node(problem.start, None, None, 0)
    if problem.goal_test(node.state):
        return node, {tuple_matrix(problem.start)}

    frontier = [node]
    reached = {tuple_matrix(problem.start)}
    cutoff_occurred = False

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node, reached
        if node.path_cost >= limit:
            cutoff_occurred = True
        else:
            for child in expand(problem, node, log_cb):
                cs = tuple_matrix(child.state)
                if cs not in reached:
                    reached.add(cs)
                    frontier.append(child)

    return ("cutoff" if cutoff_occurred else False), reached


def ids(problem: Problem, log_cb=None):
    total_visited = set()
    for depth in range(1000):
        result, visited = _depth_limited_search(problem, depth, log_cb)
        total_visited.update(visited)
        if result != "cutoff":
            return result, len(total_visited)
    return False, len(total_visited)
