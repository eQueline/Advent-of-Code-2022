import utils

input_str = utils.get_input("22")
DIRECTIONS = [*zip((1, 0, -1, 0), (0, 1, 0, -1))]


def parse_input(input_str):
    path = ""
    map = []
    for line in input_str.split('\n'):
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
    return map, path


def move(map, start, steps):
    x, y, direction = start
    dir = DIRECTIONS[direction]
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


def solve_p1(input_str):
    map, path = parse_input(input_str)
    loc = [map[0]["start"], 0, 0]
    steps = 0
    for c in path:
        if c == "R":
            loc[:] = move(map, loc, steps)
            loc[2] = (loc[2] + 1) % 4
            steps = 0
        elif c == "L":
            loc[:] = move(map, loc, steps)
            loc[2] = (loc[2] + 3) % 4
            steps = 0
        else:
            steps = steps * 10 + int(c)
    return 1000 * (loc[1] + 1) + 4 * (loc[0] + 1) + loc[2]


part1 = utils.time_function(solve_p1, input_str)
print("Part 1:", part1)
