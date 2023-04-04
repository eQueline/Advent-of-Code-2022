import requests
import main

input_str = "498,4 -> 498,6 -> 496,6\n503,4 -> 502,4 -> 502,9 -> 494,9\n"
input_str = requests.get('https://adventofcode.com/2022/day/14/input', cookies={"session": main.SESSION_ID}).text


def hash_coord(x, y):
    return x * 1000 + y


def drop_sand():
    coord = [500, 0]
    moved = True
    while moved:
        moved = False
        for path in [[0, 1], [-1, 1], [1, 1]]:
            new_coord = [coord[0] + path[0], coord[1] + path[1]]
            new_hash = hash_coord(*new_coord)
            if new_hash not in solids.keys():
                moved = True
                coord = new_coord
                break
    solids[hash_coord(*coord)] = 1
    return coord[1] > max_y - 2


def print_sand():
    for y in range(0, max_y+2):
        row = ""
        for x in range(min_x-1, max_x+1):
            coord = hash_coord(x, y)
            if coord in solids.keys():
                row += "#" if solids[coord] == 0 else "o"
            else:
                row += "."
        print(row)


max_y = 0
min_x, max_x = 1000, 0
solids = dict()
for trace in input_str[:-1].split('\n'):
    prev_point = None
    for point in trace.split(' -> '):
        pair = point.split(',')
        cur_point = [int(pair[0]), int(pair[1])]
        if prev_point is not None:
            if prev_point[0] == cur_point[0]:
                x = cur_point[0]
                for y in range(min(prev_point[1], cur_point[1]), max(prev_point[1], cur_point[1]) + 1):
                    solids[hash_coord(x, y)] = 0
                    if max_y < y:
                        max_y = y
                    if min_x > x:
                        min_x = x
                    if max_x < x:
                        max_x = x
            else:
                y = cur_point[1]
                for x in range(min(prev_point[0], cur_point[0]), max(prev_point[0], cur_point[0]) + 1):
                    solids[hash_coord(x, y)] = 0
                    if max_y < y:
                        max_y = y
                    if min_x > x:
                        min_x = x
                    if max_x < x:
                        max_x = x
        prev_point = cur_point
max_y = max_y + 2
for x in range(min_x-10, max_x+10):
    solids[hash_coord(x, max_y)] = 0

# Part 1
cnt = 0

while not drop_sand():
    cnt += 1
print(cnt)
#print_sand()


# Part 2
cnt = 0
row = 0
for y in range(0, max_y+1):
    for x in range(500-row, 500+row+1):
        coord = hash_coord(x, y)
        can_fill = y == 0
        if coord not in solids.keys() or coord in solids.keys() and solids[coord] == 1:
            for path in [[0, -1], [-1, -1], [1, -1]]:
                above = hash_coord(x + path[0], y + path[1])
                if above in solids.keys() and solids[above] == 1:
                    can_fill = True
        if can_fill:
            if min_x > x:
                min_x = x
            if max_x < x:
                max_x = x
            if y == max_y:
                solids[coord] = 0
                continue
            cnt += 1
            if coord not in solids.keys():
                solids[coord] = 1
    row += 1
print(cnt)
#print_sand()
