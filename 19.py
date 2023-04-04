import copy
import re
import math

import requests
import main

input_str = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore " \
            "and 14 clay. Each geode robot costs 2 ore and 7 obsidian.\nBlueprint 2: Each ore robot costs 2 ore. Each " \
            "clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 " \
            "obsidian.\n"
input_str = requests.get('https://adventofcode.com/2022/day/19/input', cookies={"session": main.SESSION_ID}).text

blueprints = []
for line in input_str[:-1].split("\n"):
    m = re.findall(r'(\d+)', line)
    m = [int(i) for i in m]
    blueprint = {"ore": {"ore": m[1]},
                 "clay": {"ore": m[2]},
                 "obsidian": {"ore": m[3], "clay": m[4]},
                 "geode": {"ore": m[5], "obsidian": m[6]}}
    blueprints.append(blueprint)


def get_build_time(blueprint, robot, state):
    time = 0
    for req_key in blueprint[robot]:
        if state["robots"][req_key] == 0:
            return None
        time = max(time, math.ceil((blueprint[robot][req_key] - state["res"][req_key]) / state["robots"][req_key]))
    return time + 1


def can_prune(blueprint, state, best_geode):
    # If build only geodes from now on, can it beat the best?
    geode_robots = state["robots"]["geode"]
    time_left = state["time"] + 1
    total_geode = state["res"]["geode"] + time_left * (time_left - 1) / 2 + geode_robots * time_left
    if total_geode <= best_geode:
        return True
    # If robots > any single robot cost except geode
    for res in ROBOTS:
        if res == 'geode':
            continue
        max_res = 0
        for robot in ROBOTS:
            max_res = max(max_res, blueprint[robot].get(res, 0))
        if max_res < state["robots"][res]:
            return True
    return False


def hash_state(state):
    hash_ar = []
    for robot in state["robots"]:
        hash_ar.append(state["robots"][robot])
    for res in state["res"]:
        hash_ar.append(state["res"][res])
    return hash(tuple(hash_ar))


quality_sum = 0
ROBOTS = ["ore", "clay", "obsidian", "geode"]
START_STATE = {"time": 24,
               "robots": {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0},
               "res": {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}}
for idx, bp in enumerate(blueprints):
    best_geode = 0
    visited = dict()
    states = [copy.deepcopy(START_STATE)]
    while states:
        state = states.pop()
        state_hash = hash_state(state)
        pruned = can_prune(bp, state, best_geode)
        visited[state_hash] = max(visited.get(state_hash, 0), -1 if pruned else state["time"])
        if pruned:
            continue
        can_build = False
        if state["time"] == 0:
            geode = state["res"]["geode"]
            if geode > best_geode:
                best_geode = geode
            continue
        for robot in reversed(ROBOTS):
            build_time = get_build_time(bp, robot, state)
            if build_time is None or build_time > state["time"]:
                continue
            new_state = copy.deepcopy(state)
            # Wait for res
            for res in new_state["robots"]:
                new_state["res"][res] += new_state["robots"][res] * build_time
            # Spend res
            for req_key in bp[robot]:
                new_state["res"][req_key] -= bp[robot][req_key]
            # Spend time
            new_state["time"] -= build_time
            # Add robot
            new_state["robots"][robot] += 1
            if new_state["time"] > visited.get(hash_state(new_state), -1):
                states.append(new_state)
                can_build = True
        if not can_build:
            geode = state["res"]["geode"] + state["robots"]["geode"] * state["time"]
            if geode > best_geode:
                best_geode = geode
    quality_sum += (idx + 1) * best_geode
print(quality_sum)


# Part 2
quality_mul = 1
START_STATE = {"time": 32,
               "robots": {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0},
               "res": {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}}
for bp in blueprints[0:3]:
    best_geode = 0
    visited = dict()
    states = [copy.deepcopy(START_STATE)]
    while states:
        state = states.pop()
        state_hash = hash_state(state)
        pruned = can_prune(bp, state, best_geode)
        visited[state_hash] = max(visited.get(state_hash, 0), -1 if pruned else state["time"])
        if pruned:
            continue
        can_build = False
        if state["time"] == 0:
            geode = state["res"]["geode"]
            if geode > best_geode:
                best_geode = geode
            continue
        for robot in reversed(ROBOTS):
            build_time = get_build_time(bp, robot, state)
            if build_time is None or build_time > state["time"]:
                continue
            new_state = copy.deepcopy(state)
            # Wait for res
            for res in new_state["robots"]:
                new_state["res"][res] += new_state["robots"][res] * build_time
            # Spend res
            for req_key in bp[robot]:
                new_state["res"][req_key] -= bp[robot][req_key]
            # Spend time
            new_state["time"] -= build_time
            # Add robot
            new_state["robots"][robot] += 1
            if new_state["time"] > visited.get(hash_state(new_state), -1):
                states.append(new_state)
                can_build = True
        if not can_build:
            geode = state["res"]["geode"] + state["robots"]["geode"] * state["time"]
            if geode > best_geode:
                best_geode = geode
    quality_mul *= best_geode
print(quality_mul)
