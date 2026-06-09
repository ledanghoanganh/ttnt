from puzzle_core import Problem, random_matrix, expand, manhattan_distance, Node
import random

def local_beam_search(problem: Problem, log_cb=None, k=2, max_count=10000):
    """Thuật toán Local Beam Search cho bài toán 8-puzzle.
    """
    node = Node(problem.start, None, None, 0, 0, manhattan_distance(problem.start, problem.goal))
    current_states = expand(problem, node, log_cb)
    
    if k < len(current_states):
        current_states = random.sample(current_states, k=k)
        
    count = len(current_states)

    while count < max_count:
        neighbor_states = []
        for state in current_states:
            new_neighbors = expand(problem, state, log_cb)
            neighbor_states.extend(new_neighbors)
            count += len(new_neighbors)
            
            if count >= max_count:
                break
        
        if len(neighbor_states) == 0:
            current_states = sorted(current_states, key=lambda x: x.h_cost)
            return current_states[0], count
        
        for neighbor in neighbor_states:
            if problem.goal_test(neighbor.state):
                return neighbor, count
        
        neighbor_states = sorted(neighbor_states, key=lambda x: x.h_cost)
        current_states = neighbor_states[:k]
        
    # Nếu vượt quá max_count, trả về trạng thái tốt nhất tìm được tới thời điểm hiện tại
    current_states = sorted(current_states, key=lambda x: x.h_cost)
    return current_states[0], count


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
    if res_node is None:
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




