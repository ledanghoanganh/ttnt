from puzzle_core import Node, Problem, tuple_matrix, expand, random_matrix, is_solvable

def dfs_v2(problem: Problem, log_cb=None):
    if not is_solvable(problem.start, problem.goal):
        return False, 0

    node = Node(problem.start, None, None, 0)
    if problem.goal_test(node.state): 
        return node, 0

    frontier = [node]
    frontier_states = {tuple_matrix(node.state)}
    reached = {tuple_matrix(node.state)}
    reached_count = 0

    while frontier:
        node = frontier.pop()
        reached_count = len(reached)
        
        for child in expand(problem, node, log_cb):
            s = child.state
            if problem.goal_test(s): 
                return child, reached_count
            
            if tuple_matrix(s) not in reached and tuple_matrix(s) not in frontier_states:
                reached.add(tuple_matrix(s))
                frontier.append(child)    
                frontier_states.add(tuple_matrix(s))    

    return False, reached_count

if __name__ == "__main__":
    matrix = random_matrix()
    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]
    problem = Problem(matrix, goal)

    for row in matrix:
        print(row)

    res_node, count = dfs_v2(problem)
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