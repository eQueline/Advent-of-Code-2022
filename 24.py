import main
import requests
from queue import PriorityQueue

DIR_LIST = [
    (0, 0),
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
]
DIR_MAP = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1),
    '.': False
}
DIR_BACKMAP = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): 'v',
    (0, -1): '^'
}


def parse_input(input_str) -> (dict, int, int):
    blizzards = dict()
    field = input_str[:-1].split('\n')[1:-1]
    height = len(field)
    width = len(field[0]) - 2
    for x in range(width):
        for y in range(height):
            blizzard = DIR_MAP[field[y][x + 1]]
            if blizzard:
                blizzards[(x, y)] = [blizzard]
    return blizzards, width, height


def advance_blizzards(blizzards: dict, w, h) -> (set, dict):
    empty_tiles = set()
    next_blizzards = {}
    for blizzard_key in blizzards:
        for blizzard in blizzards[blizzard_key]:
            dx, dy = blizzard_key[0] + blizzard[0], blizzard_key[1] + blizzard[1]
            if dx < 0: dx = w - 1
            if dx >= w: dx = 0
            if dy < 0: dy = h - 1
            if dy >= h: dy = 0
            next_blizzards[(dx, dy)] = next_blizzards.get((dx, dy), []) + [blizzard]
    for x in range(w):
        for y in range(h):
            if (x, y) not in next_blizzards:
                empty_tiles.add((x, y))
    return empty_tiles, next_blizzards


def generate_steps(loc, tiles: set, w, h, start, end) -> list:
    directions = []
    for direction in DIR_LIST:
        x, y = loc[0] + direction[0], loc[1] + direction[1]
        if (x, y) == end:
            directions.append((x, y))
            break
        if (x, y) == start:
            directions.append((x, y))
            continue
        if (x, y) != start and (x < 0 or x >= w or y < 0 or y >= h):
            continue
        if (x, y) in tiles:
            directions.append((x, y))
    return directions


def can_purge(moves, loc, w, h, min_finish, end):
    return moves + (abs(end[0] - loc[0]) + abs(end[1] - loc[1])) >= min_finish


def solve(blizzards, w, h, empty_tiles, start, end, total_moves=0) -> (int, list):
    min_moves = total_moves + w * h + 2
    options = PriorityQueue()
    options.put([total_moves, start])
    visited = set()
    while not options.empty():
        moves, loc = options.get()
        if (loc, moves) in visited:
            continue
        visited.add((loc, moves))
        if min_moves <= moves:
            continue
        if moves >= len(empty_tiles):
            tiles, blizzards = advance_blizzards(blizzards, w, h)
            empty_tiles.append(tiles)
        tiles = empty_tiles[moves]
        next_steps = generate_steps(loc, tiles, w, h, start, end)
        moves += 1
        for step in next_steps:
            if step == end:
                if min_moves > moves:
                    min_moves = moves
            if can_purge(moves, loc, w, h, min_moves, end):
                continue
            options.put([moves, step])
    return min_moves, blizzards, empty_tiles, w, h


def solve_p1(input_str):
    blizzards, w, h = parse_input(input_str)
    start, end = (0, -1), (w - 1, h)
    min_moves, blizzards, empty_tiles, w, h = solve(blizzards, w, h, [], start, end)
    return min_moves, blizzards, empty_tiles, w, h


def solve_p2(blizzards, empty_tiles, w, h, total_moves):
    start, end = (0, -1), (w - 1, h)
    total_moves, blizzards, empty_tiles, w, h = solve(blizzards, w, h, empty_tiles, end, start, total_moves)
    total_moves, blizzards, empty_tiles, w, h = solve(blizzards, w, h, empty_tiles, start, end, total_moves)
    return total_moves


input_str = "#.#####\n#.....#\n#>....#\n#.....#\n#...v.#\n#.....#\n#####.#\n"
input_str = "#.######\n#>>.<^<#\n#.<..<<#\n#>v.><>#\n#<^v^^>#\n######.#\n"
input_str = requests.get('https://adventofcode.com/2022/day/24/input', cookies={"session": main.SESSION_ID}).text
print("Start")
moves, blizzards, empty_tiles, width, height = main.time_function(solve_p1, input_str)
print(moves)
print(main.time_function(solve_p2, blizzards, empty_tiles, width, height, moves))
