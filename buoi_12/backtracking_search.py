from eight_puzzle_solver.puzzle_core import Problem, Node, expand, manhattan_distance, random_matrix
import sys

# Tăng recursion limit cho backtracking
sys.setrecursionlimit(2000)

def backtracking_search(problem: Problem, log_cb=None):
    """
    Thuật toán Backtracking Search áp dụng cho 8-puzzle.
    """
    count_obj = [0]
    start_node = Node(problem.start, None, None, 0, 0, manhattan_distance(problem.start, problem.goal))
    
    # function BACKTRACK(assignment, csp) returns a solution or failure
    def BACKTRACK(assignment):
        current_node = assignment[-1]
        
        if log_cb:
            log_cb(current_node)
        count_obj[0] += 1
            
        # if assignment is complete then return assignment
        if problem.goal_test(current_node.state):
            return assignment
            
        # Giới hạn độ sâu để tránh đệ quy vô hạn (đặc thù đồ thị vòng của 8-puzzle)
        if len(assignment) >= 40:
            return "failure"
            
        # var <- SELECT-UNASSIGNED-VARIABLE(assignment, csp)
        # Trong 8-puzzle, "biến" tiếp theo chính là trạng thái hiện tại cần được mở rộng
        var = current_node
        
        # for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
        # "value" ở đây là các node con (kết quả của các action hợp lệ)
        for value in expand(problem, var, None):
            
            # if CONSISTENT(var, value, assignment, csp) then
            # Hợp lệ (consistent) ở đây là không đi vào trạng thái đã có trong đường đi (tránh chu trình)
            state_tuple = tuple(map(tuple, value.state))
            is_consistent = True
            for node in assignment:
                if tuple(map(tuple, node.state)) == state_tuple:
                    is_consistent = False
                    break
                    
            if is_consistent:
                # add {var = value} to assignment
                assignment.append(value)
                
                # result <- BACKTRACK(assignment, csp)
                result = BACKTRACK(assignment)
                
                # if result != failure then return result
                if result != "failure":
                    return result
                    
                # remove {var = value} from assignment
                assignment.pop()
                
        # return failure
        return "failure"

    # return BACKTRACK({}, csp) 
    # Khởi tạo assignment rỗng (ở đây là mảng chứa trạng thái bắt đầu)
    initial_assignment = [start_node]
    result = BACKTRACK(initial_assignment)
    
    # Phục hồi cấu trúc Node chain cho UI
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