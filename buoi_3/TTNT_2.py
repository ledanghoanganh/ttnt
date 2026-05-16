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


def get_actions(i, j):
    actions = []

    if i > 0:
        actions.append("up")
    if i < 2:
        actions.append("down")
    if j > 0:
        actions.append("left")
    if j < 2:
        actions.append("right")

    return actions


def rule_match(state, rules):
    return rules(state)


def robot_hut_bui(percept):

    def rules(state):
        i, j, trash = state
        actions = []
        if trash == 1:
            actions.append("suck")
        actions.append(random.choice(get_actions(i, j)))

        return actions

    state = percept
    rule = rule_match(state, rules)
    action = rule

    return action


def actuator(matrix, pos, actions):

    for a in actions:
        if a == "suck":
            matrix[pos[0]][pos[1]] = 0
        else:
            moves = {
                "up": (-1, 0),
                "down": (1, 0),
                "left": (0, -1),
                "right": (0, 1)
            }
            di, dj = moves[a]
            pos = (pos[0] + di, pos[1] + dj)

    return matrix, pos



matrix = random_matrix()

for row in matrix:
    print(row)

pos = (0, 0)

history = set()

path = []

while True:

    state = (
        pos,
        tuple(tuple(row) for row in matrix)
    )

    if state in history:
        print("Robot bị kẹt trong vòng lặp!")
        print("Không thể quét hết rác.")
        break

    history.add(state)

    percept = (pos[0], pos[1], matrix[pos[0]][pos[1]])

    actions = robot_hut_bui(percept)

    path.append("+".join(actions))

    matrix, pos = actuator(matrix, pos, actions)

    tong_rac = sum(sum(row) for row in matrix)

    if tong_rac == 0:
        print("Đã dọn sạch toàn bộ rác!")
        break


print(" -> ".join(path))

for row in matrix:
    print(row)