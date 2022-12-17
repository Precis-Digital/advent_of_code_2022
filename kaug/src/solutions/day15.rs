use sscanf::sscanf;
use crate::{solution::Solution, input};

pub struct Day15;

impl Solution for Day15 {
	fn name(&self) -> &'static str {
		"Day 15"
	}

	fn part_1(&self) -> String {
		solution_1(input::load(15).as_str(), 2000000)
	}

	fn part_2(&self) -> String {
		solution_2(input::load(15).as_str(), 4000000)
	}
}

struct Point {
	x: i64,
	y: i64
}

impl Point {
	fn equal(&self, b: &Point) -> bool {
		self.x == b.x && self.y == b.y
	}
}

struct Sensor {
	pos: Point,
	beacon: Point,
	distance: i64
}


impl Sensor {
	fn contains(&self, b: &Point) -> bool {
		self.distance >= manhattan(&self.pos, b)
	}

	fn new() -> Self {
		Self {
			pos: Point { x: 0, y: 0 },
			beacon: Point { x: 0, y: 0 },
			distance: 0
		}
	}
}

fn solution_1(input: &str, row: i64) -> String {
	let sensors = parser(&input);
	let (x_min, x_max) = x_min_x_max(&sensors);

	let mut count = 0;

	for x in x_min..=x_max {
		let test_point = Point {x, y: row};
		for sensor in &sensors {
			if sensor.contains(&test_point)
			&& !sensor.pos.equal(&test_point)
			&& !sensor.beacon.equal(&test_point) {
				count += 1;
				break;
			}
		}
	}

	count.to_string()
}

fn solution_2(input: &str, coord_max: i64) -> String {
	let sensors = parser(&input);
	let mut possible_beacon_location = Point {x: 0, y: 0};
	// Found inspiration from this visual https://www.reddit.com/r/adventofcode/comments/zmfwg1/2022_day_15_part_2_seekin_for_the_beacon/
	// So bascially just iterate around the perimiter of each sensor
	// breaks the loop if we have found the possible beacon location
	for sensor in &sensors {
		if possible_beacon_location.x > 0 {
			break;
		}

		let min_y = sensor.pos.y - sensor.distance + 1;
		let max_y = sensor.pos.y + sensor.distance + 1;

		for y in min_y..=max_y {
			
			if 0 > y || y > coord_max {
				continue;
			}

			let left_x = sensor.pos.x - (sensor.distance - (sensor.pos.y - y).abs() + 1);
			let right_x = sensor.pos.x + (sensor.distance - (sensor.pos.y - y).abs() + 1);
			let left_possible = Point{x: left_x, y};
			let right_possible = Point{x: right_x, y};

			if !is_covered(&left_possible, &sensors) && left_x < coord_max {
				possible_beacon_location = left_possible;
				break;
			}

			if !is_covered(&right_possible, &sensors) && right_x < coord_max {
				possible_beacon_location = right_possible;
				break;
			}

		}
	}

	(possible_beacon_location.x  * 4000000 + possible_beacon_location.y).to_string()

}

fn is_covered(possible_beacon_location: &Point, sensors: &Vec<Sensor>) -> bool{
	let mut covered = false;
	for sensor in sensors {
		if sensor.contains(&possible_beacon_location) {
			covered = true;
		}
	}
	covered
}

fn x_min_x_max(sensors: &Vec<Sensor>) -> (i64, i64) {
	let mut x_min = 99999999;
	let mut x_max = 0;

	for sensor in sensors {
		if sensor.pos.x - sensor.distance < x_min {
			x_min = sensor.pos.x - sensor.distance;
		}
		if sensor.pos.x + sensor.distance > x_max {
			x_max = sensor.pos.x + sensor.distance;
		}
	}

	(x_min, x_max)
}

fn manhattan(a: &Point, b: &Point) -> i64 {
	(a.x - b.x).abs() + (a.y - b.y).abs()
}

fn parser(input: &str) -> Vec<Sensor> {
	let mut sensors = Vec::new();
	for line in input.lines() {
		let (
			sensor_x,
			sensor_y,
			beacon_x,
			beacon_y
		) = sscanf!(line, "Sensor at x={i64}, y={i64}: closest beacon is at x={i64}, y={i64}").unwrap();
		let sensor_pos = Point { x: sensor_x, y: sensor_y };
		let beacon_pos = Point { x: beacon_x, y: beacon_y };
		sensors.push(Sensor {
			distance: manhattan(&sensor_pos, &beacon_pos),
			pos: sensor_pos,
			beacon: beacon_pos
		});
	}
	sensors
}

#[cfg(test)]
mod test {
	use super::*;

	const SAMPLE: &str = "Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3";

	// 5292496 to high
	#[test]
	fn part_1() {
		assert_eq!(solution_1(&SAMPLE, 10), "26");
	}

	#[test]
	fn part_2() {
		assert_eq!(solution_2(&SAMPLE, 20), "56000011");
	}
}
