from complex_core import get_initial_belief_state, get_target_goal_states, ComplexNode, get_applicable_actions, apply_action, is_goal, complex_h_cost
import heapq

def complex_a_star_missing_both(problem, log_cb=None):
    # Khuyết Input & Goal: Chỉ lấy State 1 và Goal 1
    starts = [problem.start[0]] if problem.start else []
    goals = [problem.goal[0]] if problem.goal else []
    
    belief_state = get_initial_belief_state(starts)
    target_goals = get_target_goal_states(goals)
    
    if not belief_state or not target_goals:
        return None, 0
        
    h_start = complex_h_cost(belief_state, target_goals)
    start_node = ComplexNode(belief_state, None, "", 0, 0, h_start)
    if log_cb:
        log_cb(start_node)
        
    if is_goal(belief_state, target_goals):
        return start_node, 1
        
    frontier = []
    heapq.heappush(frontier, (start_node.g_cost + start_node.h_cost, id(start_node), start_node))
    explored = {belief_state: start_node.g_cost}
    count = 1
    
    while frontier:
        f_cost, _, node = heapq.heappop(frontier)
        
        if is_goal(node.belief_state, target_goals):
            return node, count
            
        if node.g_cost > explored.get(node.belief_state, float('inf')):
            continue
            
        actions = get_applicable_actions(node.belief_state)
        for action in actions:
            new_belief = apply_action(node.belief_state, action)
            new_g = node.g_cost + 1 
            
            if new_belief not in explored or new_g < explored[new_belief]:
                explored[new_belief] = new_g
                h_cost = complex_h_cost(new_belief, target_goals)
                child = ComplexNode(new_belief, node, action, node.path_cost + 1, new_g, h_cost)
                count += 1
                if log_cb:
                    log_cb(child)
                    
                heapq.heappush(frontier, (new_g + h_cost, id(child), child))
                
    return None, count
