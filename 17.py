import copy

import requests
import main

input_str = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
input_str = requests.get('https://adventofcode.com/2022/day/17/input', cookies={"session": main.SESSION_ID}).text
shapes_height = [1, 3, 3, 4, 2]
shapes = [[[0, 0], [1, 0], [2, 0], [3, 0]],
          [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]],
          [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]],
          [[0, 0], [0, 1], [0, 2], [0, 3]],
          [[0, 0], [0, 1], [1, 0], [1, 1]]]
shape_index = 0
jet = input_str
jet_index = 0
rocks = []
height = 0
falling = False


def create_rock(shape, height):
    rock = []
    for part in shape:
        rock.append([part[0] + 2, part[1] + height + 3])
    return [rock, False]


def print_cave():
    global height
    pic = []
    for y in range(height + 8):
        row = "|"
        for x in range(7):
            row += "."
        row += "|"
        pic.append(row)
    for rock in rocks:
        for coord in rock[0]:
            row = pic[coord[1]]
            row = row[:coord[0] + 1] + ("#" if rock[1] else "@") + row[coord[0] + 2:]
            pic[coord[1]] = row
    pic.reverse()
    for row in pic:
        print(row)
    print("+-------+")


def move(fall):
    global jet_index
    rock = rocks.pop()
    new_rock = []
    if fall:
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
        if fall:
            rock[1] = True
            max_height = 0
            for coord in rock[0]:
                max_height = max(max_height, coord[1] + 1)
            rock.append(max_height)
    else:
        rock[0] = new_rock
    rocks.append(rock)


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
    hash = ""
    for y in grid:
        for x in y:
            hash += x
    return hash


def step():
    global height
    global shapes
    global shape_index
    global falling
    if len(rocks) == 0 or rocks[-1][1]:
        if len(rocks) > 0:
            last_rock = rocks[-1]
            for coord in last_rock[0]:
                height = max(height, coord[1] + 1)
        rocks.append(create_rock(shapes[shape_index], height))
        shape_index = (shape_index + 1) % len(shapes)
        return True
    else:
        move(falling)
        falling = not falling
        return False


# Part 1
while len(rocks) < 23:
    step()
print(height)


# Part 2
shape_index = 0
jet_index = 0
rocks = []
height = 0
falling = False
hash_list = dict()
cycle_start, cycle_end = [], []


while True:
    finished = step()
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
    finished = step()
    if finished:
        cnt += 1
total_height = height + cycle_height * cycles
print(total_height)

