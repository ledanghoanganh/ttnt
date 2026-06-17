from puzzle_core import Problem, Node
import copy
import sys

sys.setrecursionlimit(2000)

def and_or_search(problem: Problem, log_cb=None):
    count_obj = [0]
    VARIABLES = [(r, c) for r in range(3) for c in range(3)]
    
    def OR_SEARCH(state, problem, path):
        # goal_test
        def is_goal(s):
            for r in range(3):
                for c in range(3):
                    if s[r][c] == '?': return False
                    if s[r][c] != problem.goal[r][c]: return False
            return True
            
        if is_goal(state):
            return []
            
        state_tuple = tuple(map(tuple, state))
        if state_tuple in path:
            return "failure"
            
        # Tìm biến chưa gán
        var_idx = -1
        for i in range(9):
            r, c = VARIABLES[i]
            if state[r][c] == '?':
                var_idx = i
                break
        if var_idx == -1: return "failure"
        r, c = VARIABLES[var_idx]
        
        # problem.actions(state)
        actions = []
        for val in range(9):
            consistent = True
            if problem.goal[r][c] != val: consistent = False
            for i in range(3):
                for j in range(3):
                    if state[i][j] == val: consistent = False
            
            action_str = f"x{var_idx+1} = {val}"
            err_s = copy.deepcopy(state)
            err_s[r][c] = val
            err_node = Node(err_s, None, action_str, len(path)+1, 0, 0)
                
            if consistent:
                actions.append((val, action_str, err_node))
                if log_cb: log_cb(err_node)
                count_obj[0] += 1
            else:
                err_node.action += " (Sai)"
                if log_cb: log_cb(err_node)
                count_obj[0] += 1
                
        for val, action_str, node in actions:
            # result_states = problem.results(state, action)
            new_state = copy.deepcopy(state)
            new_state[r][c] = val
            result_states = [new_state]
            
            plan = AND_SEARCH(result_states, problem, path + [state_tuple])
            if plan != "failure":
                return [action_str, plan]
                
        return "failure"

    def AND_SEARCH(states, problem, path):
        plans = {}
        for s in states:
            plan_s = OR_SEARCH(s, problem, path)
            if plan_s == "failure":
                return "failure"
            plans[tuple(map(tuple, s))] = plan_s
        return plans

    def AND_OR_GRAPH_SEARCH(problem):
        initial_state = [['?' for _ in range(3)] for _ in range(3)]
        return OR_SEARCH(initial_state, problem, [])
        
    plan = AND_OR_GRAPH_SEARCH(problem)
    
    if plan != "failure":
        nodes = [Node([['?' for _ in range(3)] for _ in range(3)], None, "Init", 0, 0, 0)]
        curr_plan = plan
        for i in range(9):
            if not curr_plan: break
            action_str = curr_plan[0]
            val = int(action_str.split("=")[1].strip())
            r, c = VARIABLES[i]
            ns = copy.deepcopy(nodes[-1].state)
            ns[r][c] = val
            n = Node(ns, nodes[-1], action_str, i+1, 0, 0)
            nodes.append(n)
            
            # lấy plan con
            sub_plans = curr_plan[1]
            ns_tuple = tuple(map(tuple, ns))
            curr_plan = sub_plans.get(ns_tuple, [])
            
        return nodes[-1], count_obj[0]
        
    return None, count_obj[0]
