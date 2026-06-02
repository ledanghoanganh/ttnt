from eight_puzzle_solver.puzzle_core import Problem, Node, random_matrix, expand, manhattan_distance


def simple_hill_climbing(problem: Problem, log_cb=None):
    """Thuật toán Simple Hill Climbing cho bài toán 8-puzzle.

    Tại mỗi bước, thuật toán sẽ chọn trạng thái con có giá trị đánh giá tốt nhất (theo hàm heuristic) để tiếp tục.
    Nếu không có trạng thái con nào tốt hơn trạng thái hiện tại, thuật toán sẽ dừng lại.
    """
    current_node = Node(problem.start, None, None, 0, 0, manhattan_distance(problem.start, problem.goal))
    count = 1
    if problem.goal_test(current_node.state):
        return current_node, count

    while True:
        # expand đã tính toán h_cost cho các node con, nên chỉ cần so sánh h_cost để chọn node con tốt nhất
        for next_node in expand(problem, current_node, log_cb):
            count += 1
            if next_node.h_cost < current_node.h_cost:
                current_node = next_node
                if problem.goal_test(current_node.state):
                    return current_node, count
                break
        else:
            break

    return False, count



if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    states = []
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, reached_len = simple_hill_climbing(problem)
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