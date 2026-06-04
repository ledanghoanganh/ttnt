from eight_puzzle_solver.puzzle_core import Problem, random_matrix
from stochastic_hill_climbing import stochastic_hill_climbing


def random_restart_hill_climbing(problem: Problem, log_cb=None):
    """Thuật toán Random Restart Hill Climbing cho bài toán 8-puzzle.
    """
    MAX_RESTART = 1000
    res, count = False, 0
    for _ in range(MAX_RESTART):
        if res != False:
            break
        res, count = stochastic_hill_climbing(problem)
    return res, count

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    states = []
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, reached_len = random_restart_hill_climbing(problem)
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
