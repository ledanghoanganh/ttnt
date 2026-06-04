from puzzle_core import Problem, random_matrix, expand, manhattan_distance, Node
import random

def local_beam_search(problem: Problem, log_cb=None, k=2):
    """Thuật toán Local Beam Search cho bài toán 8-puzzle.
    """
    node = Node(problem.start, None, None, 0, 0, manhattan_distance(problem.start, problem.goal))
    if problem.goal_test(node.state):
        return node, 0
        
    current_states = expand(problem, node, log_cb)
    count = len(current_states)
    
    for state in current_states:
        if problem.goal_test(state.state):
            return state, count
            
    k_actual = min(k, len(current_states))
    if k_actual > 0:
        current_states = random.sample(current_states, k=k_actual)

    while True:
        neighbor_states = []
        for state in current_states:
            new_neighbors = expand(problem, state, log_cb)
            count += len(new_neighbors)
            neighbor_states.extend(new_neighbors)
        
        if len(neighbor_states) == 0:
            return False, count
        
        for neighbor in neighbor_states:
            if problem.goal_test(neighbor.state):
                return neighbor, count
        
        neighbor_states = sorted(neighbor_states, key=lambda x: x.h_cost)
        best_current = min(current_states, key=lambda x: x.h_cost)
        
        if neighbor_states[0].h_cost >= best_current.h_cost:
            return False, count
            
        current_states = neighbor_states[:k]
    

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    states = []
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, reached_len = local_beam_search(problem)
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