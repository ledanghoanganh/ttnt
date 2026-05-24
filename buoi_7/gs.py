import heapq
from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix, manhattan_distance

def gs(problem: Problem, log_cb=None):
    """Thuật toán Greedy-Search cho bài toán 8-puzzle.

    Sử dụng hàm đánh giá Heuristic: h(n) = khoảng cách Manhattan.
    """
    node = Node(problem.start, None, None, 0)
    h_start = manhattan_distance(node.state, problem.goal)
    
    counter = 0
    frontier = []
    heapq.heappush(frontier, (h_start, counter, node))
    
    frontier_set = {tuple_matrix(node.state)}
    
    reached = set()

    while frontier:
        h, _, node = heapq.heappop(frontier)
        
        s = tuple_matrix(node.state)
        frontier_set.discard(s)
        
        if node.state == problem.goal:
            return node, len(reached)

        reached.add(s)

        for child in expand(problem, node, log_cb):
            cs = tuple_matrix(child.state)
            
            if cs not in reached and cs not in frontier_set:
                h_child = manhattan_distance(child.state, problem.goal)
                
                counter += 1
                heapq.heappush(frontier, (h_child, counter, child))
                frontier_set.add(cs)
            

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

    res_node, reached_len = gs(problem)
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
