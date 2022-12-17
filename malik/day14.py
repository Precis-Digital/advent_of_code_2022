from typing import Optional
from dataclasses import dataclass

@dataclass
class Particle:
    x: int
    y: int
    at_rest: bool = False
    fell_off: bool = False

    def move(self,
             coordinates_of_rocks_and_particles: set[tuple[int, int]],
             min_x: int,
             max_x: int,
             min_y: int,
             max_y: int,
             height_map: dict[int, int],
             floor: Optional[int] = None,
             ) -> None:

        # print(height_map)
        # move the floor down if it's not at the bottom
        # if self.x in height_map:
        #     if self.y < height_map[self.x]:
        #         self.y = height_map[self.x] - 2


        if floor and (self.y + 1) == floor:
            self.at_rest = True
            return

        # first try to move down in y direction
        if self.at_rest:
            return
        if (self.x, self.y + 1) not in coordinates_of_rocks_and_particles:
            self.y += 1
        elif (self.x - 1, self.y + 1) not in coordinates_of_rocks_and_particles:
            self.x -= 1
            self.y += 1
        elif (self.x + 1, self.y+1) not in coordinates_of_rocks_and_particles:
            self.x += 1
            self.y += 1
        else:
            self.at_rest = True
            return

        # check if the particle fell off the map
        if floor is None and (self.y > max_y or self.x < min_x or self.x > max_x):
            self.fell_off = True
            return

    def coordinates(self) -> tuple[int, int]:
        return (self.x, self.y)


def get_data(fname: str) -> set[tuple[int, int]]:
    with open(fname, "r") as f:
        all_rocks = set()
        for line in f.readlines():
            line = line.strip()
            coordinates = line.split(" ->")
            coordinate_tuples = []
            for coordinate_string in coordinates:
                coordinate = coordinate_string.split(",")
                coordinate_tuples.append((int(coordinate[0]), int(coordinate[1])))
            for i in range(len(coordinate_tuples) - 1):
                # print(i)
                x1, y1 = coordinate_tuples[i]
                x2, y2 = coordinate_tuples[i + 1]
                dx, dy = x2 - x1, y2 - y1
                dx = dx // abs(dx) if dx != 0 else 0
                dy = dy // abs(dy) if dy != 0 else 0
                newx, newy = x1, y1
                all_rocks.add((newx, newy))
                while (newx, newy) != (x2, y2):
                    # print(newx, newy, dx, dy)
                    newx += dx
                    newy += dy
                    all_rocks.add((newx, newy))
        return all_rocks


def get_min_max(all_rocks: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    x = [rock[0] for rock in all_rocks]
    y = [rock[1] for rock in all_rocks]
    return min(x), 0, max(x), max(y)


def print_grid(rocks: set[tuple[int, int]], particles_coordinates: set[tuple[int, int]], simulate_floor: bool = False) -> None:
    minx, miny, maxx, maxy = get_min_max(rocks)
    for y in range(miny-3, maxy + 3):
        for x in range(minx-3, maxx + 3):
            if simulate_floor and y == maxy + 2:
                print("#", end="")
            elif (x, y) in rocks:
                print("#", end="")
            elif (x, y) in particles_coordinates:
                print("O", end="")
            else:
                print(".", end="")

        print()


def get_particle_coordinates(particles: list[Particle]) -> set[tuple[int, int]]:
    return {(particle.x, particle.y) for particle in particles}

def simulate_sand(rocks: set[tuple[int, int]], simulate_floor: bool = False, max_iterations: int=1000, visualize: bool=False) -> int:
    init_y = -1
    init_x = 500
    minx, miny, maxx, maxy = get_min_max(rocks)
    floor = maxy + 2 if simulate_floor else None

    particles = [Particle(x=init_x, y=init_y)]
    particles_at_rest: set[tuple[int, int]] = set()

    objects = rocks | particles_at_rest

    height_map = {}
    for x, y in rocks:
        height_map[x] = max(height_map.get(x, 0), y)

    stop_simulation = False
    i = 0
    while particles and not stop_simulation and i < max_iterations:
        particle = particles.pop()
        particle.move(objects, minx, maxx, miny, maxy, floor=floor, height_map=height_map)
        # height_map[particle.x] = min(height_map.get(particle.x, 0), particle.y)
        # print(particle, particle.at_rest, particle.fell_off, particle.coordinates())
        if particle.at_rest:
            particles_at_rest.add(particle.coordinates())
            objects.add(particle.coordinates())
            if particle.coordinates() == (init_x, 0):
                stop_simulation = True
            # append a new partticle to the list
            particles.append(Particle(x=init_x, y=init_y))
        elif particle.fell_off:
            # if the particle falls off stop the simulation
            stop_simulation = True
        else:
            particles.append(particle)

        particle_coordinates = get_particle_coordinates(particles)
        if visualize and i % 100000 == 0:
            print(i)
            print_grid(rocks, particles_at_rest.union(particle_coordinates), simulate_floor=simulate_floor)
        i += 1

    return len(particles_at_rest)

def solution1(rocks):
    return simulate_sand(rocks=rocks, max_iterations=1000000, visualize=True)

def solution2(rocks):
    return simulate_sand(rocks=rocks, max_iterations=10000000, simulate_floor=True, visualize=True)

if __name__ == "__main__":
    rocks = get_data("inputs/day-14-sample.txt")
    assert solution1(rocks) == 24
    assert solution2(rocks) == 93

    rocks = get_data("inputs/day-14-input.txt")
    assert solution1(rocks) == 1001
    assert solution2(rocks) == 27976