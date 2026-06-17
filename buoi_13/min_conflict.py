from puzzle_core import Problem, Node
import copy
import random

def min_conflict(problem: Problem, log_cb=None, max_steps=1000):
    count_obj = [0]
    VARIABLES = [(r, c) for r in range(3) for c in range(3)]
    
    def state_from_assignment(assignment):
        s = [[0]*3 for _ in range(3)]
        for var, v in assignment.items():
            s[var[0]][var[1]] = v
        return s
        
    def is_solution(assignment):
        for var, val in assignment.items():
            if problem.goal[var[0]][var[1]] != val: return False
        vals = list(assignment.values())
        if len(set(vals)) != 9: return False
        return True

    def CONFLICTS(var, v, assignment, csp):
        c_count = 0
        if problem.goal[var[0]][var[1]] != v:
            c_count += 1
        for other_var, other_val in assignment.items():
            if other_var != var and other_val == v:
                c_count += 1
        return c_count

    def MIN_CONFLICTS(csp, max_steps):
        nums = list(range(9))
        random.shuffle(nums)
        current = {var: nums[i] for i, var in enumerate(VARIABLES)}
        
        current_node = Node(state_from_assignment(current), None, "Khởi tạo ngẫu nhiên", 0, 0, 0)
        if log_cb: log_cb(current_node)
        
        for step in range(1, max_steps + 1):
            if is_solution(current):
                return current_node
                
            conflicted_vars = []
            for var, val in current.items():
                if CONFLICTS(var, val, current, csp) > 0:
                    conflicted_vars.append(var)
                    
            if not conflicted_vars:
                return current_node
                
            var = random.choice(conflicted_vars)
            
            min_c = float('inf')
            best_vals = []
            for v in range(9):
                c_val = CONFLICTS(var, v, current, csp)
                if c_val < min_c:
                    min_c = c_val
                    best_vals = [v]
                elif c_val == min_c:
                    best_vals.append(v)
            value = random.choice(best_vals)
            
            current[var] = value
            
            action_str = f"x{var[0]*3 + var[1] + 1} = {value}"
            current_node = Node(state_from_assignment(current), current_node, action_str, current_node.path_cost + 1, 0, 0)
            if log_cb: log_cb(current_node)
            count_obj[0] += 1
            
        return "failure"
        
    res = MIN_CONFLICTS(problem, max_steps)
    if res != "failure":
        return res, count_obj[0]
    return None, count_obj[0]
