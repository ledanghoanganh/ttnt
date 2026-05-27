import heapq
from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix, number_of_wrong, manhattan_distance

def a_star(problem: Problem, log_cb=None):
    """Thuật toán A* cho bài toán 8-puzzle.

    Sử dụng hàm đánh giá f(n) = g(n) + h(n).
    Với g(n) là chi phí đường đi từ Start tới state hiện tại (số bước di chuyển),
    và h(n) là khoảng cách Manhattan từ state hiện tại đến đích.
    """
    from puzzle_core import is_solvable
    if not is_solvable(problem.start, problem.goal):
        return False, 0

    start_node = Node(problem.start, None, None, 0, 0, manhattan_distance(problem.start, problem.goal))
    f = start_node.g_cost + start_node.h_cost

    frontier = []
    heapq.heappush(frontier, (f, start_node))

    frontier_costs = {tuple_matrix(start_node.state): start_node.g_cost}
    reached_costs = {}

    while frontier:
        f, node = heapq.heappop(frontier)
        s = tuple_matrix(node.state)

        if s in reached_costs and node.g_cost > reached_costs[s]:
            continue

        if node.state == problem.goal:
            return node, len(reached_costs)

        reached_costs[s] = node.g_cost

        for child in expand(problem, node, log_cb):
            cs = tuple_matrix(child.state)
            g = node.g_cost + number_of_wrong(child.state, problem.goal)
            h = manhattan_distance(child.state, problem.goal)
            f = g + h

            if cs in reached_costs and g >= reached_costs[cs]:
                continue

            if cs not in frontier_costs or g < frontier_costs[cs]:
                if cs in reached_costs:
                    del reached_costs[cs]
                frontier_costs[cs] = g
                heapq.heappush(frontier, (f, child))

    return False, len(reached_costs)

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    problem = Problem(matrix, goal)

    print("Ma trận bắt đầu:")
    for row in matrix:
        print(row)

    res_node, reached_len = a_star(problem)
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
