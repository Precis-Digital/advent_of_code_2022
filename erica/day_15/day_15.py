
def get_sensor_and_beacon():
    with open('erica/day_15/input_data.txt') as f:
        rows = [line.strip().split(":") for line in f.readlines()]
        cord_list = []
        for row in rows:
            row_list = []
            for cord in row:
                cord = cord.replace("Sensor at ", "").replace(" closest beacon is at ", "").replace("x=", "").replace(" y=","").split(",")
                cord = tuple(map(int, cord))
                row_list.append(cord)
            cord_list.append(row_list)

        return cord_list


def manhattan_distance_between_sensor_and_beacon(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def can_be_reached_from_sensor(sensor, pos, distance):
    return manhattan_distance_between_sensor_and_beacon(sensor, pos) <= distance


class Sensor:

    def __init__(self, sensor, beacon):
        self.sensor = sensor
        self.beacon = beacon
        self.x = sensor[0]
        self.y = sensor[1]
        self.distance = manhattan_distance_between_sensor_and_beacon(sensor, beacon)


def part_1():

    goal_y = 2000000
    cords = get_sensor_and_beacon()

    sensors = [Sensor(sensor=cord[0], beacon=cord[1]) for cord in cords]
    beacons = [cord[1] for cord in cords]

    spot = []
    for s in sensors:
        for x in range(s.x - s.distance, s.x + (s.distance + 1)):
            if can_be_reached_from_sensor(s.sensor, (x, goal_y), s.distance) and (x, goal_y) not in beacons:
                spot.append((x, goal_y))

    print(f"Part 1: {len(list(set(spot)))}")  # part 1: 4811413


if __name__ == "__main__":
    part_1()






