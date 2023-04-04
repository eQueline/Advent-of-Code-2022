import requests
import main

#input_str = "Sabqponm\n\abcryxxl\naccszExk\nacctuvwj\nabdefghi\n"
input_str = requests.get('https://adventofcode.com/2022/day/12/input', cookies={"session": main.SESSION_ID}).text

grid = []
start = []
end = []
for idy, y in enumerate(input_str.split("\n")[:-1]):
    row = []
    for idx, x in enumerate(y):
        val = x
        if val == "S":
            start = [idx, idy]
            val = 'a'
        if val == 'E':
            end = [idx, idy]
            val = 'z'
        row.append(ord(val) - ord('a'))
    grid.append(row)
cnt_steps = 0


def hash_coordinates(coord):
    return coord[0] * 1000 + coord[1]


# Part 1
visited = {}
to_visit = []
visited[hash_coordinates(start)] = 0
to_visit.append((start, 0))
while True:
    cnt_steps += 1
    if len(to_visit) == 0:
        break
    position, steps = to_visit.pop()
    if hash_coordinates(position) == hash_coordinates(end):
        continue
    valid_locations = []
    for step in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
        if position[0] + step[0] < 0 \
                or position[0] + step[0] >= len(grid[0]) \
                or position[1] + step[1] < 0 \
                or position[1] + step[1] >= len(grid):
            continue
        location = [position[0] + step[0], position[1] + step[1]]
        if grid[location[1]][location[0]] - grid[position[1]][position[0]] > 1:
            continue
        valid_locations.append(location)
    for location in valid_locations:
        h_loc = hash_coordinates(location)
        if h_loc not in visited.keys() or visited[h_loc] > steps + 1:
            visited[h_loc] = steps + 1
            to_visit.append([location, steps+1])
print("Min steps to finish:", visited[hash_coordinates(end)])
print("Total steps:", cnt_steps)

# Part 2
visited = {}
to_visit = []
visited[hash_coordinates(end)] = 0
to_visit.append((end, 0))
min_steps = 999999
while True:
    cnt_steps += 1
    if len(to_visit) == 0:
        break
    position, steps = to_visit.pop()
    if grid[position[1]][position[0]] == 0:
        if min_steps > steps:
            min_steps = steps
        continue
    valid_locations = []
    for step in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
        if position[0] + step[0] < 0 \
                or position[0] + step[0] >= len(grid[0]) \
                or position[1] + step[1] < 0 \
                or position[1] + step[1] >= len(grid):
            continue
        location = [position[0] + step[0], position[1] + step[1]]
        if grid[position[1]][position[0]] - grid[location[1]][location[0]] > 1:
            continue
        valid_locations.append(location)
    for location in valid_locations:
        h_loc = hash_coordinates(location)
        if h_loc not in visited.keys() or visited[h_loc] > steps + 1:
            visited[h_loc] = steps + 1
            to_visit.append([location, steps+1])
print("Min steps to finish:", min_steps)
print("Total steps:", cnt_steps)
