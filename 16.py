import copy

import requests
import main

input_str = "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB\nValve BB has flow rate=13; tunnels lead to " \
            "valves CC, AA\nValve CC has flow rate=2; tunnels lead to valves DD, BB\nValve DD has flow rate=20; " \
            "tunnels lead to valves CC, AA, EE\nValve EE has flow rate=3; tunnels lead to valves FF, DD\nValve FF has " \
            "flow rate=0; tunnels lead to valves EE, GG\nValve GG has flow rate=0; tunnels lead to valves FF, " \
            "HH\nValve HH has flow rate=22; tunnel leads to valve GG\nValve II has flow rate=0; tunnels lead to " \
            "valves AA, JJ\nValve JJ has flow rate=21; tunnel leads to valve II\n"
input_str = requests.get('https://adventofcode.com/2022/day/16/input', cookies={"session": main.SESSION_ID}).text

valves = {}
max_dp = 0
for line in input_str[:-1].split("\n"):
    valve = []
    location_pos = line.find("Valve ") + len("Valve ")
    location = line[location_pos:line.find(" ", location_pos)]
    flow_rate_pos = line.find("rate=") + len("rate=")
    valve.append(int(line[flow_rate_pos:line.find(";")]))
    tunnels_pos = line.find(" ", line.find(" to valve") + len(" to valve")) + 1
    valve.append(line[tunnels_pos:].split(", "))
    valves[location] = valve
    max_dp += valve[0]


def parse_neighbours(steps):
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
    return parse_neighbours(steps)


paths = {}
for valve in valves:
    if valves[valve][0] > 0 or valve == "AA":
        pathing = {}
        for depth, step in enumerate(parse_neighbours([{valve}])):
            for end in step:
                if end == valve or valves[end][0] == 0:
                    continue
                pathing[end] = depth
        paths[valve] = pathing
print(paths)


# Part 1
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
            print(sequence)
        continue
    # Purge doomed sequence
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
            print(sequence)
print(best_pressure)