import utils

input_str = utils.get_input("15")

ROW = 2000000  # 2000000 for input "15"
# ROW = 10  # 10 for input "15e"
THRESHOLD = 4000000


def parse_input(input_str):
    sensors = []
    beacons = set()
    for line in input_str.split("\n"):
        sensor = []
        sensor_x_pos = line.find("r at x=") + len("r at x=")
        sensor.append(int(line[sensor_x_pos:line.find(",")]))
        sensor_y_pos = line.find(", y=") + len(", y=")
        sensor.append(int(line[sensor_y_pos:line.find(":")]))
        beacon_x_pos = line.find("is at x=") + len("is at x=")
        sensor.append(int(line[beacon_x_pos:line.find(",", beacon_x_pos)]))
        beacon_y_pos = line.find(", y=", beacon_x_pos) + len(", y=")
        sensor.append(int(line[beacon_y_pos:]))
        sensor.append(abs(sensor[0] - sensor[2]) + abs(sensor[1] - sensor[3]))
        sensors.append(sensor)
        if sensor[3] == ROW:
            beacons.add(sensor[2])
    return sensors, beacons


def solve_p1(sensors, beacons):
    lines = []
    for sensor in sensors:
        dist = abs(ROW - sensor[1])
        if sensor[4] >= dist:
            width = sensor[4] - dist
            lines.append([sensor[0] - width, sensor[0] + width])
    u_lines = []
    while len(lines) > 0:
        line = lines.pop()
        reduced = False
        for o_line in lines:
            if line[0] <= o_line[1] and line[1] >= o_line[0]:
                new_line = [min(line[0], o_line[0]), max(line[1], o_line[1])]
                lines.remove(o_line)
                lines.append(new_line)
                reduced = True
                break
        if not reduced:
            u_lines.append(line)

    coords = 0
    for line in u_lines:
        coords += abs(line[1] - line[0] + 1)
        for beacon in beacons:
            if line[0] <= beacon <= line[1]:
                coords -= 1
    return coords


def check_for_beacon(x, y):
    for sensor in sensors:
        if abs(x-sensor[0]) + abs(y-sensor[1]) <= sensor[4]:
            return False
    return True


def solve_p2(sensors):
    for sensor in sensors:
        strip_dist = sensor[4] + 1
        for x in range(sensor[0], sensor[0] + strip_dist + 1):
            if x < 0 or x > THRESHOLD:
                continue
            y = sensor[1] - strip_dist + x - sensor[0]
            if y < 0 or y > THRESHOLD:
                continue
            if check_for_beacon(x, y):
                return x * THRESHOLD + y


sensors, beacons = parse_input(input_str)
part1 = utils.time_function(solve_p1, sensors, beacons)
print("Part 1:", part1)
part2 = utils.time_function(solve_p2, sensors)
print("Part 2:", part2)


