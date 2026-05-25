from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix

def dfs(problem: Problem, log_cb=None):
    """Thuật toán Depth-First Search phiên bản Early-Goal Test cho bài toán 8-puzzle.
    """
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

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    problem = Problem(matrix, goal)

    print("Ma trận bắt đầu:")
    for row in matrix:
        print(row)

    res_node, reached_len = dfs(problem)
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