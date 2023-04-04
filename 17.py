import utils

input_str = utils.get_input("17")
SHAPE_HEIGHTS = [1, 3, 3, 4, 2]
SHAPES = [[[0, 0], [1, 0], [2, 0], [3, 0]],
          [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]],
          [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]],
          [[0, 0], [0, 1], [0, 2], [0, 3]],
          [[0, 0], [0, 1], [1, 0], [1, 1]]]


def create_rock(shape, height):
    rock = []
    for part in shape:
        rock.append([part[0] + 2, part[1] + height + 3])
    return [rock, False]


def move(rocks, falling, jet, jet_index):
    rock = rocks.pop()
    new_rock = []
    if falling:
        for part in rock[0]:
            new_rock.append([part[0], part[1] - 1])
    else:
        jet_dir = (1 if jet[jet_index] == ">" else -1)
        jet_index = (jet_index + 1) % len(jet)
        new_rock = []
        for part in rock[0]:
            new_rock.append([part[0] + jet_dir, part[1]])
    collision = False
    for c1 in new_rock:
        if c1[0] < 0 or c1[0] >= 7 or c1[1] < 0:
            collision = True
            break
    new_rock_height = 0
    for coord in new_rock:
        new_rock_height = max(new_rock_height, coord[1] + 1)
    for rock2 in reversed(rocks):
        for c2 in rock2[0]:
            if new_rock_height - rock2[2] > 4:
                continue
            for c1 in new_rock:
                if c1[0] == c2[0] and c1[1] == c2[1]:
                    collision = True
                    break
            if collision:
                break
        if collision:
            break
    if collision:
        if falling:
            rock[1] = True
            max_height = 0
            for coord in rock[0]:
                max_height = max(max_height, coord[1] + 1)
            rock.append(max_height)
    else:
        rock[0] = new_rock
    rocks.append(rock)
    return jet_index


def hash_state(last_rocks):
    grid = []
    for y in range(60):
        row = []
        for x in range(7):
            row.append("0")
        grid.append(row)
    max_y = 0
    for rock in last_rocks:
        for coord in rock[0]:
            max_y = max(max_y, coord[1])
    for rock in last_rocks:
        for coord in rock[0]:
            grid[max_y-coord[1]][coord[0]] = "1"
    hash_str = ""
    for y in grid:
        for x in y:
            hash_str += x
    return hash_str


def step(rocks, height, shape_index, falling, jet, jet_index):
    if len(rocks) == 0 or rocks[-1][1]:
        if len(rocks) > 0:
            last_rock = rocks[-1]
            for coord in last_rock[0]:
                height = max(height, coord[1] + 1)
        rocks.append(create_rock(SHAPES[shape_index], height))
        shape_index = (shape_index + 1) % len(SHAPES)
        return True, height, shape_index, falling, jet_index
    else:
        jet_index = move(rocks, falling, jet, jet_index)
        return False, height, shape_index, not falling, jet_index


def solve_p1(jet):
    falling = False
    height = 0
    shape_index = 0
    jet_index = 0
    rocks = []
    while len(rocks) < 2023:
        finished, height, shape_index, falling, jet_index = step(rocks, height, shape_index, falling, jet, jet_index)
    return height


def solve_p2(jet):
    shape_index = 0
    jet_index = 0
    rocks = []
    height = 0
    falling = False
    hash_list = dict()
    cycle_start, cycle_end = [], []

    while True:
        finished, height, shape_index, falling, jet_index = step(rocks, height, shape_index, falling, jet, jet_index)
        if finished:
            state = hash_state(rocks[-10:])
            if state in hash_list.keys():
                cycle_start = hash_list[state]
                cycle_end = [len(rocks), height]
                break
            hash_list[state] = [len(rocks), height]
    cycles = int((1000000000000 - cycle_start[0]) / (cycle_end[0] - cycle_start[0])) - 1
    remainder = (1000000000000 - cycle_start[0]) % (cycle_end[0] - cycle_start[0])
    cycle_height = cycle_end[1] - cycle_start[1]
    cnt = 0
    while cnt <= remainder:
        finished, height, shape_index, falling, jet_index = step(rocks, height, shape_index, falling, jet, jet_index)
        if finished:
            cnt += 1
    total_height = height + cycle_height * cycles
    return total_height


part1 = utils.time_function(solve_p1, input_str)
print(part1)
part2 = utils.time_function(solve_p2, input_str)
print(part2)
