import heapq
from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix, number_of_wrong

def ucs(problem: Problem, log_cb=None):
    """Thuật toán Uniformed-Cost Search cho bài toán 8-puzzle.

    Với hàm chi phí là g(n) = số ô sai
    """
    from puzzle_core import is_solvable
    if not is_solvable(problem.start, problem.goal):
        return False, 0

    node = Node(problem.start, None, None, 0, 0, 0)
    frontier = []
    heapq.heappush(frontier, (node.g_cost, node))
    frontier_set = {tuple_matrix(node.state)}
    reached = set()

    while frontier:
        parent_g_cost, node = heapq.heappop(frontier)
        s = tuple_matrix(node.state)

        if s in reached:
            continue

        if node.state == problem.goal:
            return node, len(reached)

        reached.add(s)

        for child in expand(problem, node, log_cb):
            cs = tuple_matrix(child.state)
            if cs not in reached and cs not in frontier_set:
                heapq.heappush(frontier, (child.g_cost, child))
                frontier_set.add(cs)

    return False, len(reached)

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    states = []
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, reached_len = ucs(problem)
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
