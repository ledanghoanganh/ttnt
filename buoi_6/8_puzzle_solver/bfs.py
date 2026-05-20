from collections import deque
from puzzle_core import Node, Problem, tuple_matrix, expand, child_node


def bfs(problem: Problem, log_cb=None):
    node = Node(problem.start, None, None, 0)
    frontier = deque([node])
    frontier_set = {tuple_matrix(node.state)}
    reached = set()

    while frontier:
        node = frontier.popleft()
        if node.state == problem.goal:
            return node, len(reached)
        reached.add(tuple_matrix(node.state))
        for child in expand(problem, node, log_cb):
            s = tuple_matrix(child.state)
            if s not in reached and s not in frontier_set:
                frontier.append(child)
                frontier_set.add(s)

    return False, len(reached)


def bfs_v2(problem: Problem, log_cb=None):
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
            cs = tuple_matrix(child.state)
            if cs not in explored and cs not in frontier_set:
                if problem.goal_test(child.state):
                    return child, len(explored)
                frontier.append(child)
                frontier_set.add(cs)

    return False, len(explored)
