import copy
import utils

input_str = utils.get_input("16")


def parse_input(input_str):
    valves = {}
    max_dp = 0
    for line in input_str.split("\n"):
        valve = []
        location_pos = line.find("Valve ") + len("Valve ")
        location = line[location_pos:line.find(" ", location_pos)]
        flow_rate_pos = line.find("rate=") + len("rate=")
        valve.append(int(line[flow_rate_pos:line.find(";")]))
        tunnels_pos = line.find(" ", line.find(" to valve") + len(" to valve")) + 1
        valve.append(line[tunnels_pos:].split(", "))
        valves[location] = valve
        max_dp += valve[0]
    return valves, max_dp


def parse_neighbours(valves, steps):
    cur_depth = steps[len(steps)-1]
    next_depth = set()
    for valve in cur_depth:
        for tunnel in valves[valve][1]:
            visited = False
            for step in steps:
                if tunnel in step:
                    visited = True
            if not visited:
                next_depth.add(tunnel)
    if len(next_depth) == 0:
        return steps
    steps.append(next_depth)
    return parse_neighbours(valves, steps)


def compute_paths(valves):
    paths = {}
    for valve in valves:
        if valves[valve][0] > 0 or valve == "AA":
            pathing = {}
            for depth, step in enumerate(parse_neighbours(valves, [{valve}])):
                for end in step:
                    if end == valve or valves[end][0] == 0:
                        continue
                    pathing[end] = depth
            paths[valve] = pathing
    return paths

def solve_p1(valves, max_dp):
    paths = compute_paths(valves)
    sequences = [{"path": ["AA"],
                  "time": 30,
                  "dp": 0,
                  "pressure": 0}]
    best_pressure = 0
    while len(sequences) > 0:
        sequence = sequences.pop()
        if sequence["time"] == 0:
            if best_pressure < sequence["pressure"]:
                best_pressure = sequence["pressure"]
                # print(sequence)
            continue
        # Prune doomed sequence
        estimated_pressure = sequence["pressure"] + max_dp * (sequence["time"])
        if estimated_pressure < best_pressure:
            continue
        last_valve = sequence["path"][len(sequence["path"]) - 1]
        has_options = False
        for tunnel in paths[last_valve]:
            time = paths[last_valve][tunnel] + 1
            if tunnel in sequence["path"] or time > sequence["time"]:
                continue
            has_options = True
            path = copy.deepcopy(sequence["path"])
            path.append(tunnel)
            step = {"path": path,
                    "time": sequence["time"] - time,
                    "dp": sequence["dp"] + valves[tunnel][0],
                    "pressure": sequence["pressure"] + sequence["dp"] * time}
            sequences.append(step)
        if not has_options:
            sequence["pressure"] = sequence["pressure"] + sequence["time"] * sequence["dp"]
            sequence["time"] = 0
            if best_pressure < sequence["pressure"]:
                best_pressure = sequence["pressure"]
                # print(sequence)
    return best_pressure


valves, max_dp = parse_input(input_str)
part1 = utils.time_function(solve_p1, valves, max_dp)
print("Part 1:", part1)
