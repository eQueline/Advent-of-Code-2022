from copy import copy
import re
import math
from queue import PriorityQueue
import utils

input_str = utils.get_input("19")
RESOURCES = ["ore", "clay", "obsidian", "geode"]


class Resources:
    def __init__(self, ore=0, clay=0, obsidian=0, geode=0):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def __copy__(self):
        return Resources(self.ore, self.clay, self.obsidian, self.geode)


class State:
    def __init__(self, time):
        self.time = time
        self.robots = Resources()
        self.res = Resources()

    def __copy__(self):
        state_copy = State(self.time)
        state_copy.robots = copy(self.robots)
        state_copy.res = copy(self.res)
        return state_copy

    def __hash__(self):
        hash_tuple = (self.time,
                      self.robots.ore, self.robots.clay, self.robots.obsidian, self.robots.geode,
                      self.res.ore, self.res.clay, self.res.obsidian, self.res.geode)
        return hash(hash_tuple)

    def __gt__(self, other):
        return self.time > other.time


class Blueprint:
    def __init__(self):
        self.ore = Resources()
        self.clay = Resources()
        self.obsidian = Resources()
        self.geode = Resources()


def parse_input(input_str):
    blueprints = []
    for line in input_str.split("\n"):
        m = re.findall(r'(\d+)', line)
        m = [int(i) for i in m]
        blueprint = Blueprint()
        blueprint.ore = Resources(ore=m[1])
        blueprint.clay = Resources(ore=m[2])
        blueprint.obsidian = Resources(ore=m[3], clay=m[4])
        blueprint.geode = Resources(ore=m[5], obsidian=m[6])
        blueprints.append(blueprint)
    return blueprints


def get_build_time(cost: Resources, state: State):
    time = 0
    for req_key in RESOURCES:
        if getattr(cost, req_key) == 0:
            continue
        if getattr(state.robots, req_key) == 0:
            return None
        time = max(time, math.ceil((getattr(cost, req_key) - getattr(state.res, req_key)) /
                                   getattr(state.robots, req_key)))
    return time + 1


def can_prune(blueprint: Blueprint, state, best_geode):
    # If build only geodes from now on, can it beat the best?
    time_left = state.time + 1
    total_geode = state.res.geode + state.robots.geode * time_left + time_left * (time_left - 1) / 2
    if total_geode <= best_geode:
        return True
    # If robot amount > max robot cost except geode
    for res in RESOURCES:
        if res == "geode":
            continue
        max_res = 0
        for robot in RESOURCES:
            max_res = max(max_res, getattr(getattr(blueprint, robot), res))
        if max_res < getattr(state.robots, res):
            return True
    return False


def get_blueprint_best_geodes(blueprint, start_time):
    best_geodes = 0
    visited = set()
    states = PriorityQueue()
    start_state = State(start_time)
    start_state.robots.ore = 1
    states.put(start_state)
    while not states.empty():
        state = states.get()

        can_build = False
        if state.time == 0:
            if state.res.geode > best_geodes:
                best_geodes = state.res.geode
            continue
        for robot in RESOURCES:
            robot_costs = getattr(blueprint, robot)
            build_time = get_build_time(robot_costs, state)
            if build_time is None or build_time > state.time:
                continue
            new_state = copy(state)
            # Add income and deduct cost
            for res in RESOURCES:
                old_value = getattr(new_state.res, res)
                setattr(new_state.res, res,
                        old_value + getattr(new_state.robots, res) * build_time - getattr(robot_costs, res))
            # Spend time
            new_state.time -= build_time
            # Add robot
            setattr(new_state.robots, robot, getattr(new_state.robots, robot) + 1)

            state_hash = hash(new_state)
            if state_hash in visited:
                continue
            visited.add(state_hash)
            if not can_prune(blueprint, new_state, best_geodes):
                states.put(new_state)
                can_build = True
        if not can_build:
            geode = state.res.geode + state.robots.geode * state.time
            if geode > best_geodes:
                best_geodes = geode
    return best_geodes


def solve_p1(blueprints):
    quality_sum = 0
    for idx, bp in enumerate(blueprints):
        best_geodes = get_blueprint_best_geodes(bp, 24)
        quality_sum += (idx + 1) * best_geodes
    return quality_sum


def solve_p2(blueprints):
    quality_mul = 1
    for bp in blueprints:
        best_geodes = get_blueprint_best_geodes(bp, 32)
        quality_mul *= best_geodes
    return quality_mul


blueprints = parse_input(input_str)
part1 = utils.time_function(solve_p1, blueprints)
print(part1)
part2 = utils.time_function(solve_p2, blueprints[0:3])
print(part2)
