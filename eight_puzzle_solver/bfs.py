from collections import deque
from puzzle_core import Node, Problem, tuple_matrix, expand, child_node, random_matrix

def bfs(problem: Problem, log_cb=None):
    """Thuật toán Breadth-First Search cho bài toán 8-puzzle.
    """
    from puzzle_core import is_solvable
    if not is_solvable(problem.start, problem.goal):
        return False, 0

    node = Node(problem.start, None, None, 0, 0, 0)
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
    """Thuật toán Breadth-First Search phiên bản Early-Goal Test cho bài toán 8-puzzle.
    """
    from puzzle_core import is_solvable
    if not is_solvable(problem.start, problem.goal):
        return False, 0

    node = Node(problem.start, None, None, 0, 0, 0)

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

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    problem = Problem(matrix, goal)

    print("Ma trận bắt đầu:")
    for row in matrix:
        print(row)

    print("Giải bằng BFS")

    res_node, reached_len = bfs(problem)
    if res_node == False:
        print("Không giải được")
    else:
        res = []
        while res_node.parent != None:
            res.append(res_node)
            res_node = res_node.parent

        res.reverse()
        print(f"Đã duyệt {reached_len} trạng thái.")
        print(f"Số bước giải: {len(res)}")
        for node in res:
            print(node.action)
            for row in node.state:
                print(row)

    print("Giải bằng BFS_V2")

    res_node, reached_len = bfs_v2(problem)
    if res_node == False:
        print("Không giải được")
    else:
        res = []
        while res_node.parent != None:
            res.append(res_node)
            res_node = res_node.parent

        res.reverse()
        print(f"Đã duyệt {reached_len} trạng thái.")
        print(f"Số bước giải: {len(res)}")
        for node in res:
            print(node.action)
            for row in node.state:
                print(row)
