import copy
import utils

input_str = utils.get_input("18")
DIRECTIONS = [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]]


def hash_coordinates(x, y, z):
    return int(x) * 10000 + int(y) * 100 + int(z)


def unhash_coordinates(hash_value):
    z = hash_value % 100
    y = int((((hash_value - z) / 100) % 100))
    x = int(((hash_value - z) / 100 - y) / 100)
    return [x, y, z]


def parse_input(input_str):
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    min_z, max_z = 0, 0
    cubes = {}
    for cube_str in input_str.split("\n"):
        coords = [int(i) for i in cube_str.split(',')]
        min_x = min(min_x, coords[0])
        max_x = max(max_x, coords[0])
        min_y = min(min_y, coords[1])
        max_y = max(max_y, coords[1])
        min_z = min(min_z, coords[2])
        max_z = max(max_z, coords[2])

        coord = hash_coordinates(*coords)
        cube = {"coord": coords,
                "sides_checked": [False, False, False, False, False, False],
                "empty_sides": 0}
        cubes[coord] = cube
    return cubes, min_x, max_x, min_y, max_y, min_z, max_z


def solve_p1(cubes):
    empty_spaces = set()
    for cube_id in cubes:
        cube = cubes[cube_id]
        for idx, direction in enumerate(DIRECTIONS):
            if cube["sides_checked"][idx]:
                continue
            coord_list = copy.deepcopy(cube["coord"])
            for i in range(3):
                coord_list[i] += direction[i]
            neighbour_key = hash_coordinates(*coord_list)
            neighbour = cubes.get(neighbour_key)
            if neighbour is None:
                cube["sides_checked"][idx] = True
                cube["empty_sides"] += 1
                empty_spaces.add(neighbour_key)
            else:
                cube["sides_checked"][idx] = True
                opposite_side = (idx+1) % 2 + int(idx/2)*2
                neighbour["sides_checked"][opposite_side] = True

    area = 0
    for cube_id in cubes:
        cube = cubes[cube_id]
        area += cube["empty_sides"]
    return area, empty_spaces


def bfs(visited, queue, coord):
    cube_sides = 0
    visited.append(coord)
    queue.append(coord)

    while queue:
        next_coord = queue.pop(0)
        cur = unhash_coordinates(next_coord)
        for idx, direction in enumerate(DIRECTIONS):
            coords = copy.deepcopy(cur)
            for i in range(3):
                coords[i] += direction[i]
            neighbour_key = hash_coordinates(*coords)
            if not ((min_x <= coords[0] <= max_x) and (min_y <= coords[1] <= max_y) and (min_z <= coords[2] <= max_z)):
                return 0
            if neighbour_key in cubes:
                cube_sides += 1
                continue
            if neighbour_key in visited:
                continue
            visited.append(neighbour_key)
            queue.append(neighbour_key)
    return cube_sides


def solve_p2(area, empty_spaces):
    visited = set()
    for space_key in empty_spaces:
        if space_key in visited:
            continue
        coord_list = []
        bounded = bfs(coord_list, [], space_key)
        if bounded > 0:
            area -= bounded
            for coord in coord_list:
                visited.add(coord)
    return area


cubes, min_x, max_x, min_y, max_y, min_z, max_z = parse_input(input_str)
part1, empty_spaces = utils.time_function(solve_p1, cubes)
print(part1)
part2 = utils.time_function(solve_p2, part1, empty_spaces)
print(part2)

