from eight_puzzle_solver.puzzle_core import Problem, Node, random_matrix, expand, manhattan_distance
import random, math


def simulated_annealing(problem: Problem, log_cb=None):
    """Thuật toán Simul Annealing cho bài toán 8-puzzle.
    """
    current_node = Node(problem.start, None, None, 0, 0, manhattan_distance(problem.start, problem.goal))
    count = 1

    T = 10
    T_min = 0.01
    alpha = 0.95
    while T > T_min:
        if problem.goal_test(current_node):
            return current_node, count
        
        next_nodes = expand(problem, current_node)
        count += len(next_nodes)
        next_node = random.choice(next_nodes)

        delta = next_node.h_cost - current_node.h_cost
        if delta < 0:
            current_node = next_node
        else:
            p = math.exp(-delta/T)
            if random.random() < p:
                current_node = next_node

        T = alpha*T

    return current_node, count

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    states = []
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, reached_len = simulated_annealing(problem)
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
