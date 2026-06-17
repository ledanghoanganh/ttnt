from puzzle_core import Problem, Node
import copy

def ac_3(problem: Problem, log_cb=None):
    count_obj = [0]
    VARIABLES = [(r, c) for r in range(3) for c in range(3)]
    
    DOMAIN = {var: list(range(9)) for var in VARIABLES}
    
    # Init Unary constraints
    for var in VARIABLES:
        DOMAIN[var] = [problem.goal[var[0]][var[1]]]
        
    def NEIGHBORS(X_i):
        return [v for v in VARIABLES if v != X_i]
        
    def constraint(x, y):
        return x != y # AllDiff

    def RM_INCONSISTENT_VALUES(X_i, X_j):
        removed = False
        for x in DOMAIN[X_i][:]:
            has_valid_y = False
            for y in DOMAIN[X_j]:
                if constraint(x, y):
                    has_valid_y = True
                    break
            if not has_valid_y:
                DOMAIN[X_i].remove(x)
                removed = True
                
                # Log sai
                state_matrix = [['?' for _ in range(3)] for _ in range(3)]
                for v in VARIABLES:
                    if len(DOMAIN[v]) == 1:
                        state_matrix[v[0]][v[1]] = DOMAIN[v][0]
                state_matrix[X_i[0]][X_i[1]] = x
                idx = X_i[0]*3 + X_i[1] + 1
                action_str = f"x{idx} = {x} (Sai do AC-3)"
                err_node = Node(state_matrix, None, action_str, 0, 0, 0)
                if log_cb: log_cb(err_node)
                count_obj[0] += 1
                
        return removed

    def AC_3_ALGO(csp):
        queue = []
        for X_i in VARIABLES:
            for X_j in NEIGHBORS(X_i):
                queue.append((X_i, X_j))
                
        while queue:
            X_i, X_j = queue.pop(0) # REMOVE-FIRST
            if RM_INCONSISTENT_VALUES(X_i, X_j):
                if not DOMAIN[X_i]:
                    return False
                for X_k in NEIGHBORS(X_i):
                    if (X_k, X_i) not in queue:
                        queue.append((X_k, X_i))
        return True

    success = AC_3_ALGO(problem)
    
    if success:
        nodes = [Node([['?' for _ in range(3)] for _ in range(3)], None, "Init", 0, 0, 0)]
        for i, var in enumerate(VARIABLES):
            val = DOMAIN[var][0]
            ns = copy.deepcopy(nodes[-1].state)
            ns[var[0]][var[1]] = val
            n = Node(ns, nodes[-1], f"x{i+1} = {val}", i+1, 0, 0)
            nodes.append(n)
        return nodes[-1], count_obj[0]
        
    return None, count_obj[0]
