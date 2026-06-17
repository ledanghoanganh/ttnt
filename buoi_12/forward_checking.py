from puzzle_core import Problem, Node
import copy
import sys

sys.setrecursionlimit(2000)

def forward_checking_search(problem: Problem, log_cb=None):
    count_obj = [0]
    VARIABLES = [(r, c) for r in range(3) for c in range(3)]
    
    def SELECT_UNASSIGNED_VARIABLE(assignment, csp):
        assigned_vars = list(assignment.keys())
        for var in VARIABLES:
            if var not in assigned_vars:
                return var
        return None
        
    def CONSISTENT(var, value, assignment, csp):
        r, c = var
        # Constraint: must match goal and AllDiff
        if csp.goal[r][c] != value:
            return False
        for v in assignment.values():
            if v == value:
                return False
        return True

    def FORWARD_CHECK(var, value, unassigned_domains):
        """
        Hàm nhìn trước (Forward Checking): 
        Loại bỏ giá trị 'value' khỏi tập domains của các biến chưa được gán 
        để đảm bảo ràng buộc khác nhau (AllDiff).
        """
        new_domains = copy.deepcopy(unassigned_domains)
        for unassigned_var in new_domains:
            if value in new_domains[unassigned_var]:
                new_domains[unassigned_var].remove(value)
            
            if len(new_domains[unassigned_var]) == 0:
                return None 
        return new_domains

    def BACKTRACK(assignment, domains, csp):
        if len(assignment) == 9:
            return assignment
            
        var = SELECT_UNASSIGNED_VARIABLE(assignment, csp)
        
        for value in domains[var]:
            state_matrix = [['?' for _ in range(3)] for _ in range(3)]
            for (vr, vc), vv in assignment.items():
                state_matrix[vr][vc] = vv
            state_matrix[var[0]][var[1]] = value
            action_str = f"x{var[0]*3 + var[1] + 1} = {value}"
            child_node = Node(state_matrix, None, action_str, len(assignment)+1, 0, 0)
            
            if CONSISTENT(var, value, assignment, csp):
                if log_cb: log_cb(child_node)
                count_obj[0] += 1
                
                assignment[var] = value
                
                unassigned_domains = {v: domains[v] for v in VARIABLES if v not in assignment}
                
                new_unassigned_domains = FORWARD_CHECK(var, value, unassigned_domains)
                
                if new_unassigned_domains is not None:
                    next_domains = copy.deepcopy(domains)
                    next_domains.update(new_unassigned_domains)
                    
                    result = BACKTRACK(assignment, next_domains, csp)
                    if result != "failure":
                        return result
                    
                del assignment[var]
            else:
                child_node.action += " (Sai)"
                if log_cb: log_cb(child_node)
                count_obj[0] += 1
                
        return "failure"
        
    def BACKTRACKING_SEARCH(csp):
        initial_domains = {var: list(range(9)) for var in VARIABLES}
        return BACKTRACK({}, initial_domains, csp)
        
    final_assignment = BACKTRACKING_SEARCH(problem)
    
    if final_assignment != "failure":
        nodes = [Node([['?' for _ in range(3)] for _ in range(3)], None, "Init", 0, 0, 0)]
        for i, var in enumerate(VARIABLES):
            val = final_assignment[var]
            ns = copy.deepcopy(nodes[-1].state)
            ns[var[0]][var[1]] = val
            n = Node(ns, nodes[-1], f"x{i+1} = {val}", i+1, 0, 0)
            nodes.append(n)
        return nodes[-1], count_obj[0]
        
    return None, count_obj[0]
