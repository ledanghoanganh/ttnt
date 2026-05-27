from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix, manhattan_distance

def _cost_limited_search(problem: Problem, limit, log_cb=None):
    """Thuật toán A* phiên bản Cost-Limit Test cho bài toán 8-puzzle.

    Sử dụng g(n) là hàm tính số ô sai so với đích, h(n) là hàm tính khoảng cách Manhattan từ các ô sai đến vị trí đích của chúng.
    """
    node = Node(problem.start, None, None, 0, 0, manhattan_distance(problem.start, problem.goal))

    if problem.goal_test(node.state):
        return node, limit, {tuple_matrix(problem.start)}

    frontier = [node]
    reached = {tuple_matrix(problem.start): 0}
    
    min_exceeded_f = float('inf')
    visited_states = set()

    while frontier:
        current = frontier.pop()
        cs = tuple_matrix(current.state)
        visited_states.add(cs)

        if problem.goal_test(current.state):
            return current, limit, visited_states

        for child in expand(problem, current, log_cb):
            child_state_tuple = tuple_matrix(child.state)
            child_f = child.g_cost + child.h_cost
            
            if child_f > limit:
                if child_f < min_exceeded_f:
                    min_exceeded_f = child_f
            else:
                if child_state_tuple not in reached or child.g_cost < reached[child_state_tuple]:
                    reached[child_state_tuple] = child.g_cost
                    frontier.append(child)

    return False, min_exceeded_f, visited_states

def ida_star(problem: Problem, log_cb=None):
    """Thuật toán Iterative-Deepening A* cho bài toán 8-puzzle.
    """
    limit = manhattan_distance(problem.start, problem.goal)
    total_visited = set()
    
    while True:
        result, next_limit, visited = _cost_limited_search(problem, limit, log_cb)
        total_visited.update(visited)
        
        if result is not False:
            return result, len(total_visited)
            
        if next_limit == float('inf'):
            return False, len(total_visited)
            
        limit = next_limit

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    problem = Problem(matrix, goal)

    print("Ma trận bắt đầu:")
    for row in matrix:
        print(row)

    res_node, reached_len = ida_star(problem)
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
