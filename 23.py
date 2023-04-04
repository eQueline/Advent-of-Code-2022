import itertools
import requests
import time
import main


def calculate_empty_tiles(grid: set) -> int:
    min_x, min_y = 1000000, 1000000
    max_x, max_y = 0, 0
    for x, y in grid:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(grid)


def have_neighbours(grid: set, x, y) -> bool:
    for dx, dy in itertools.product((-1, 0, 1), (-1, 0, 1)):
        if dx == 0 and dy == 0:
            continue
        if (x + dx, y + dy) in grid:
            return True
    return False


def get_proposed_moves(grid: set, dir_order) -> dict:
    moves = {}
    for x, y in grid:
        if not have_neighbours(grid, x, y):
            continue
        for direction_index in range(len(DIRECTIONS)):
            direction = DIRECTIONS[(dir_order + direction_index) % len(DIRECTIONS)]
            dx, dy = direction[1]
            can_step = True
            check: tuple
            for check in direction[0]:
                cx, cy = x + check[0], y + check[1]
                if (cx, cy) in grid:
                    can_step = False
                    break
            if can_step:
                move = moves.get((x + dx, y + dy), [(x, y), 0])
                move[1] += 1
                moves[(x + dx, y + dy)] = move
                break
    return moves


def perform_moves(grid: set, moves: dict):
    for cx, cy in moves:
        move = moves[(cx, cy)]
        if move[1] != 1:
            continue
        elf = moves[(cx, cy)][0]
        grid.remove(elf)
        grid.add((cx, cy))


def step(grid: set, dir_order) -> int:
    moves = get_proposed_moves(grid, dir_order)
    perform_moves(grid, moves)
    return len(moves)


def parse_input(input_str) -> set:
    grid = set()
    for y, line in enumerate(input_str[:-1].split('\n')):
        for x, char in enumerate(line):
            if char == '#':
                grid.add((x, y))
    return grid


def solve_p1(input_str) -> int:
    grid = parse_input(input_str)
    dir_order = 0
    for i in range(10):
        step(grid, dir_order)
        dir_order = (dir_order + 1) % len(DIRECTIONS)
    return calculate_empty_tiles(grid)


def solve_p2(input_str) -> int:
    grid = parse_input(input_str)
    dir_order = 0
    cnt = 1
    while step(grid, dir_order) > 0:
        cnt += 1
        dir_order = (dir_order + 1) % len(DIRECTIONS)
    return cnt


input_str = "..............\n..............\n.......#......\n.....###.#....\n...#...#.#....\n....#...##....\n...#.###......\n...##.#.##....\n....#..#......\n..............\n..............\n..............\n"
DIRECTIONS = [
    [[*zip((-1, 0, 1), (-1, -1, -1))], (0, -1)],
    [[*zip((-1, 0, 1), (1, 1, 1))], (0, 1)],
    [[*zip((-1, -1, -1), (-1, 0, 1))], (-1, 0)],
    [[*zip((1, 1, 1), (-1, 0, 1))], (1, 0)]
]
input_str = requests.get('https://adventofcode.com/2022/day/23/input', cookies={"session": main.SESSION_ID}).text
# print(*DIRECTIONS, sep='\n')
print("Start")
print(main.time_function(solve_p1, input_str))
print(main.time_function(solve_p2, input_str))
