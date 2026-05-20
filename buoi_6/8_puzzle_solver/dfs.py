from puzzle_core import Node, Problem, tuple_matrix, expand


def dfs(problem: Problem, log_cb=None):
    node = Node(problem.start, None, None, 0)
    if node.state == problem.goal:
        return node, 0

    frontier = [node]
    frontier_set = {tuple_matrix(node.state)}
    reached = {tuple_matrix(problem.start)}

    while frontier:
        node = frontier.pop()
        for child in expand(problem, node, log_cb):
            s = tuple_matrix(child.state)
            if child.state == problem.goal:
                return child, len(reached)
            if s not in reached and s not in frontier_set:
                reached.add(s)
                frontier.append(child)
                frontier_set.add(s)

    return False, len(reached)
