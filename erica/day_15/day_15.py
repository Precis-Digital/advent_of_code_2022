
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


def part_2():
    cords = get_sensor_and_beacon()

    sensors = [Sensor(sensor=cord[0], beacon=cord[1]) for cord in cords]

    a_coff = set()
    b_coff = set()
    for s in sensors:
        a_coff.add(s.y-s.x+s.distance+1)
        a_coff.add(s.y-s.x-s.distance-1)
        b_coff.add(s.x+s.y+s.distance+1)
        b_coff.add(s.x+s.y-s.distance-1)

    bound = 4000000
    for a in a_coff:
        for b in b_coff:
            p = ((b-a)//2, (a+b)//2)
            if all(0 < c < bound for c in p):
                if all(manhattan_distance_between_sensor_and_beacon(p, s.sensor) > s.distance for s in sensors):
                    print(f"Part 2: {bound*p[0] + p[1]} ") # part 2: 13171855019123


if __name__ == "__main__":
    part_1()
    part_2()






