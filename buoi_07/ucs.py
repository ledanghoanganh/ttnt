import heapq
from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix

def ucs(problem: Problem, log_cb=None):
    node = Node(problem.start, None, None, 0)
    frontier = []
    heapq.heappush(frontier, (node.path_cost, node))
    frontier_set = {tuple_matrix(node.state)}
    reached = set()

    while frontier:
        node = heapq.heappop(frontier)[1]
        s = tuple_matrix(node.state)

        if s in reached:
            continue

        if node.state == problem.goal:
            return node, len(reached)

        reached.add(s)

        for child in expand(problem, node, log_cb):
            cs = tuple_matrix(child.state)
            if cs not in reached and cs not in frontier_set:
                heapq.heappush(frontier, (child.path_cost, child))
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
