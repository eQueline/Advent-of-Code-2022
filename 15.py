import requests
import main

input_str = "Sensor at x=2, y=18: closest beacon is at x=-2, y=15\nSensor at x=9, y=16: closest beacon is at x=10, " \
            "y=16\nSensor at x=13, y=2: closest beacon is at x=15, y=3\nSensor at x=12, y=14: closest beacon is at " \
            "x=10, y=16\nSensor at x=10, y=20: closest beacon is at x=10, y=16\nSensor at x=14, y=17: closest beacon " \
            "is at x=10, y=16\nSensor at x=8, y=7: closest beacon is at x=2, y=10\nSensor at x=2, y=0: closest beacon " \
            "is at x=2, y=10\nSensor at x=0, y=11: closest beacon is at x=2, y=10\nSensor at x=20, y=14: closest " \
            "beacon is at x=25, y=17\nSensor at x=17, y=20: closest beacon is at x=21, y=22\nSensor at x=16, " \
            "y=7: closest beacon is at x=15, y=3\nSensor at x=14, y=3: closest beacon is at x=15, y=3\nSensor at " \
            "x=20, y=1: closest beacon is at x=15, y=3\n"
input_str = requests.get('https://adventofcode.com/2022/day/15/input', cookies={"session": main.SESSION_ID}).text

y = 2000000
threshold = 4000000
sensors = []
beacons = set()
for line in input_str[:-1].split("\n"):
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
    if sensor[3] == y:
        beacons.add(sensor[2])


# Part 1
lines = []
for sensor in sensors:
    dist = abs(y - sensor[1])
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
print(coords)


# Part 2
def check_for_beacon(x, y):
    for sensor in sensors:
        if abs(x-sensor[0]) + abs(y-sensor[1]) <= sensor[4]:
            return False
    return True


for sensor in sensors:
    strip_dist = sensor[4] + 1
    for x in range(sensor[0], sensor[0] + strip_dist + 1):
        if x < 0 or x > threshold:
            continue
        y = sensor[1] - strip_dist + x - sensor[0]
        if y < 0 or y > threshold:
            continue
        if check_for_beacon(x, y):
            print(x*threshold + y)
            exit()

