from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix

def _depth_limited_search(problem: Problem, limit, log_cb=None):
    """Thuật toán Depth-First Search phiên bản Depth-Limit Test cho bài toán 8-puzzle.
    """
    node = Node(problem.start, None, None, 0, 0, 0)

    if problem.goal_test(node.state):
        return node, {tuple_matrix(problem.start)}

    frontier = [node]
    reached = {tuple_matrix(problem.start)}
    cutoff = False

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node, reached
        if node.path_cost >= limit:
            cutoff = True
        else:
            for child in expand(problem, node, log_cb):
                cs = tuple_matrix(child.state)
                if cs not in reached:
                    reached.add(cs)
                    frontier.append(child)

    return ("cutoff" if cutoff else False), reached

def ids(problem: Problem, log_cb=None):
    """Thuật toán Interative-Deepening Search cho bài toán 8-puzzle.
    """
    from puzzle_core import is_solvable
    if not is_solvable(problem.start, problem.goal):
        return False, 0

    total_visited = set()
    for depth in range(1000):
        result, visited = _depth_limited_search(problem, depth, log_cb)
        total_visited.update(visited)
        if result != "cutoff":
            return result, len(total_visited)
    return False, len(total_visited)

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    problem = Problem(matrix, goal)

    print("Ma trận bắt đầu:")
    for row in matrix:
        print(row)

    res_node, reached_len = ids(problem)
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
