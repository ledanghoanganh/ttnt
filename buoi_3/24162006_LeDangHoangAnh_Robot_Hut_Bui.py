import random

def random_matrix():
    num = 3
    matrix = [[0 for _ in range(3)] for _ in range(3)]
    index2d = [(i, j) for i in range(3) for j in range(3)]
    
    while num > 0:
        i, j = random.choice(index2d)
        matrix[i][j] = 1
        num -= 1
        index2d.remove((i, j))
    return matrix

def cap_nhat_state(state, action, percept):
    moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
    if action in moves:
        di, dj = moves[action]
        state["pos"] = (state["pos"][0] + di, state["pos"][1] + dj)
        
    state["visited"].add(state["pos"])
    
    state["has_trash"] = (percept == 1)
    
    if action == "suck":
        state["cleaned_count"] += 1
        state["has_trash"] = False
        
    return state

def khop_luat(state, bando_model):
    if state["has_trash"]:
        return "suck"
        
    valid_moves = bando_model[state["pos"]]
    moves_dict = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
    unvisited_moves = []
    
    for move in valid_moves:
        di, dj = moves_dict[move]
        next_pos = (state["pos"][0] + di, state["pos"][1] + dj)
        
        if next_pos not in state["visited"]:
            unvisited_moves.append(move)
            
    if len(unvisited_moves) > 0:
        return random.choice(unvisited_moves)
    else:
        return random.choice(valid_moves)

def hanh_dong(matrix, real_pos, action):
    if action == "suck":
        i, j = real_pos
        matrix[i][j] = 0
        
    elif action in ["up", "down", "left", "right"]:
        moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        di, dj = moves[action]
        real_pos = (real_pos[0] + di, real_pos[1] + dj)
        
    return matrix, real_pos

def robot_hut_bui(matrix):
    bando_model = {
        (0, 0): ["down", "right"],
        (0, 1): ["down", "left", "right"],
        (0, 2): ["down", "left"],
        (1, 0): ["up", "down", "right"],
        (1, 1): ["up", "down", "left", "right"],
        (1, 2): ["up", "down", "left"],
        (2, 0): ["up", "right"],
        (2, 1): ["up", "left", "right"],
        (2, 2): ["up", "left"]
    }

    state = {
        "pos": (0, 0),             
        "visited": set([(0, 0)]),  
        "has_trash": False,
        "cleaned_count": 0        
    }
    
    real_pos = (0, 0)  
    last_action = None  
    res = []           
    
    max_steps = 50 
    step = 0
    
    while state["cleaned_count"] < 3 and step < max_steps:
        
        i, j = real_pos
        percept = matrix[i][j]
        
        state = cap_nhat_state(state, last_action, percept)
        
        action = khop_luat(state, bando_model)
        
        matrix, real_pos = hanh_dong(matrix, real_pos, action)
        
        res.append(action)
        last_action = action
        step += 1
        
    return res, matrix

if __name__ == "__main__":
    matrix = random_matrix()
    
    for row in matrix:
        print(row)
        
    hanh_trinh, matrix_sau_don = robot_hut_bui(matrix)
    
    print('->'.join(hanh_trinh))
    
    for row in matrix_sau_don:
        print(row)