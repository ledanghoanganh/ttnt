from puzzle_core import Problem, Node, expand, manhattan_distance, random_matrix
import sys

# Tăng recursion limit cho backtracking
sys.setrecursionlimit(2000)

def backtracking_search(problem: Problem, log_cb=None):
    """
    Thuật toán Backtracking Search áp dụng cho 8-puzzle.
    """
    count_obj = [0]
    start_node = Node(problem.start, None, None, 0, 0, manhattan_distance(problem.start, problem.goal))
    
    def BACKTRACK(assignment):
        current_node = assignment[-1]
        
        if log_cb:
            log_cb(current_node)
        count_obj[0] += 1
            
        if problem.goal_test(current_node.state):
            return assignment
            
        # Giới hạn độ sâu phòng trường hợp tràn bộ nhớ do 8-puzzle quá lớn
        if len(assignment) >= 50:
            return "failure"
            

        var = current_node
        
        for value in expand(problem, var, None):
            
            state_tuple = tuple(map(tuple, value.state))
            is_consistent = True
            for node in assignment:
                if tuple(map(tuple, node.state)) == state_tuple:
                    is_consistent = False
                    break
                    
            if is_consistent:
                assignment.append(value)
                
                result = BACKTRACK(assignment)
                
                if result != "failure":
                    return result
                    
                assignment.pop()
                
        return "failure"

    initial_assignment = [start_node]
    result = BACKTRACK(initial_assignment)
    
    if result != "failure":
        for i in range(1, len(result)):
            result[i].parent = result[i-1]
        return result[-1], count_obj[0]
    else:
        return None, count_obj[0]
        
if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    states = []
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, reached_len = backtracking_search(problem)
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