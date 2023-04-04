import copy
import re
import requests
import main

input_str = "        ...#\n\
        .#..\n\
        #...\n\
        ....\n\
...#.......#\n\
........#...\n\
..#....#....\n\
..........#.\n\
        ...#....\n\
        .....#..\n\
        .#......\n\
        ......#.\n\
\n\
10R5L5R10L4R5L5\n"
input_str = requests.get('https://adventofcode.com/2022/day/22/input', cookies={"session": main.SESSION_ID}).text


path = ""
map = []
for line in input_str[:-1].split('\n'):
    if line == '':
        continue
    if line.find("L") > 0:
        path = line
        continue

    start = 0
    end = 0
    row = []
    for c in line:
        if c == ' ':
            start += 1
            end = start
            continue
        end += 1
        if c == '.':
            row.append(True)
        else:
            row.append(False)
    map.append({"start": start, "end": end, "tiles": row})


# print(*map, sep="\n")


def move(start, steps):
    x, y, direction = start
    dir = directions[direction]
    for i in range(steps):
        dx, dy = x + dir[0], (y + dir[1]) % len(map)
        row = map[dy]
        while x > row["end"] or x < row["start"]:
            dy = (dy + dir[1]) % len(map)
            row = map[dy]
        width = row["end"] - row["start"]
        dx_coord = (dx - row["start"])
        if dx_coord == width:
            dx_coord = 0
            dx = row["start"]
        if dx_coord == -1:
            dx_coord = width - 1
            dx = row["end"]

        tile = row["tiles"][dx_coord]
        if not tile:
            return x, y, direction
        x, y = dx, dy
    return x, y, direction


directions = [*zip((1, 0, -1, 0), (0, 1, 0, -1))]
loc = [map[0]["start"], 0, 0]
steps = 0
for c in path:
    if c == "R":
        loc[:] = move(loc, steps)
        loc[2] = (loc[2] + 1) % 4
        steps = 0
    elif c == "L":
        loc[:] = move(loc, steps)
        loc[2] = (loc[2] + 3) % 4
        steps = 0
    else:
        steps = steps * 10 + int(c)
print(1000 * (loc[1] + 1) + 4 * (loc[0] + 1) + loc[2])

# a = [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 1, 1]]
# side = (a[0].index(1), 0)
# a[side[1]][side[0]] = 0
# cube = {"front": [side, 0]}
# while len(cube) < 6:
