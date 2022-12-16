use std::collections::HashSet;
use crate::{solution::Solution, input};

pub struct Day14;

impl Solution for Day14 {
	fn name(&self) -> &'static str {
		"Day 14"
	}

	fn part_1(&self) -> String {
		solution_1(input::load(14).as_str())
	}

	fn part_2(&self) -> String {
		solution_2(input::load(14).as_str())
	}
}

#[derive(Debug, Eq, Hash, PartialEq)]
struct Point {
	x: i32,
	y: i32,
}

fn solution_1(input: &str) -> String {
	let mut grid = parse(input);
	let mut count = 0;
	let max_y = grid.iter().map(|p| p.y).max().unwrap();
	let mut sand = Point {x:0, y:0};
	while sand.y <= max_y {
		sand = Point{x:500, y:0};
		while !grid.contains(&sand) && sand.y <= max_y {
			if simulate_fall(&grid, &mut sand) {
				let p = Point{x:sand.x, y: sand.y};
				grid.insert(p);
				count += 1;
			}
		}
	}
	count.to_string()
}

fn solution_2(input: &str) -> String {
	let mut grid = parse(input);
	let mut count = 0;
	let max_y = grid.iter().map(|p| p.y).max().unwrap();
	let floor = max_y + 2;
	while !grid.contains(&Point{x:500, y:0}) {
		let mut sand = Point{x:500, y:0};
		while !grid.contains(&sand) && sand.y <= floor - 1 {
			if simulate_fall(&grid, &mut sand) {
				let p = Point{x: sand.x, y: sand.y};
				grid.insert(p);
				count += 1;
			}
			if floor == sand.y + 1 {
				let p = Point{x: sand.x, y: sand.y};
				grid.insert(p);	
				count += 1;		
			}
		}
	}
	count.to_string()
}

fn simulate_fall(grid: &HashSet<Point>, sand: &mut Point) -> bool {
	if !grid.contains(&Point { x: sand.x, y: sand.y + 1 }) {
		sand.y += 1;
	} else if !grid.contains(&Point { x: sand.x - 1, y: sand.y + 1 }) {
		sand.x -= 1;
		sand.y += 1;
	} else if !grid.contains(&Point { x: sand.x + 1, y: sand.y + 1 }) {
		sand.x += 1;
		sand.y += 1;
	} else {
		return true;
	}
	false
}

fn parse(input: &str) -> HashSet<Point> {
	let mut grid = HashSet::new();
	let lines: Vec<&str> = input.split("\n").collect();

	for line in lines.iter() {
		let points: Vec<&str> = line.split(" -> ").collect();
		let mut prev_point = Point { x: 0, y: 0 };

		for (i, p) in points.iter().enumerate() {
			let coords: Vec<&str> = p.split(",").collect();
			let x = coords[0].parse().unwrap();
			let y = coords[1].parse().unwrap();
			let curr_point = Point { x, y };

			if i > 0 {
				let min_x = curr_point.x.min(prev_point.x);
				let max_x = curr_point.x.max(prev_point.x);
				let min_y = curr_point.y.min(prev_point.y);
				let max_y = curr_point.y.max(prev_point.y);

				for i in min_x..=max_x {
					grid.insert(Point { x: i, y });
				}
				for j in min_y..=max_y {
					grid.insert(Point { x, y: j });
				}
			} else {
				grid.insert(Point{ x:curr_point.x, y:curr_point.y});
			}
			prev_point = curr_point;
		}
	}
	grid
}
#[cfg(test)]
mod test {
	use super::*;

	const SAMPLE: &str = "498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9";

	#[test]
	fn part_1() {
		assert_eq!(solution_1(&SAMPLE), "24");
	}

	#[test]
	fn part_2() {
		assert_eq!(solution_2(&SAMPLE), "93");
	}
}
