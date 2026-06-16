from puzzle_core import Problem, Node, expand, manhattan_distance, random_matrix
import sys

sys.setrecursionlimit(2000)

def and_or_search(problem: Problem, log_cb=None):
    """
    Thuật toán AND-OR Graph Search.
    """
    count_obj = [0]
    
    def OR_SEARCH(state, path):
        current_node = Node(state, None, None, 0, 0, 0)
        if log_cb:
            log_cb(current_node)
        count_obj[0] += 1
            
        if problem.goal_test(state):
            return []
            
        state_tuple = tuple(map(tuple, state))
        if state_tuple in path:
            return "failure"
            
        # Giới hạn độ sâu phòng trường hợp tràn bộ nhớ do 8-puzzle quá lớn
        if len(path) >= 50:
            return "failure"
            
        for child_node in expand(problem, current_node, None):
            action = child_node.action
            
            result_states = [child_node.state]
            
            plan = AND_SEARCH(result_states, path + [state_tuple])
            
            if plan != "failure":
                return [action, plan]
                
        return "failure"

    def AND_SEARCH(states, path):
        plans = {}
        
        for s in states:
            plan_s = OR_SEARCH(s, path)
            
            if plan_s == "failure":
                return "failure"
                
            s_tuple = tuple(map(tuple, s))
            plans[s_tuple] = plan_s
            
        return plans


    plan = OR_SEARCH(problem.start, [])
    
    # Do GUI cần một node cuối cùng (kèm thông tin parent) để vẽ quá trình di chuyển,
    # ta phải chuyển đổi "plan" (danh sách lồng nhau) trở lại thành Node chain.
    if plan == "failure":
        return None, count_obj[0]
        
    def build_node_chain(state, current_plan, parent_node):
        if current_plan == []:
            return parent_node
            
        action = current_plan[0]
        sub_plans = current_plan[1]
        
        temp_node = Node(state, None, None, 0, 0, 0)
        for child in expand(problem, temp_node, None):
            if child.action == action:
                child.parent = parent_node
                child_state_tuple = tuple(map(tuple, child.state))
                next_plan = sub_plans[child_state_tuple]
                return build_node_chain(child.state, next_plan, child)
                
    start_node = Node(problem.start, None, None, 0, 0, manhattan_distance(problem.start, problem.goal))
    final_node = build_node_chain(problem.start, plan, start_node)
    
    return final_node, count_obj[0]


if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    states = []
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, reached_len = and_or_search(problem)
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