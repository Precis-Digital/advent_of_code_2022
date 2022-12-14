use std::{collections::HashSet, cmp::{min, max}};
use crate::{solution::Solution, input};

pub struct Day14;

impl Solution for Day14 {
	fn name(&self) -> &'static str {
		"Day 14"
	}

	fn part_1(&self) -> String {
		solution_1(input::load(14).as_str())
		//String::from("")
	}

	fn part_2(&self) -> String {
		solution_2(input::load(14).as_str())
	}
}

fn solution_1(input: &str) -> String {
	let rocks = parse(input);
	let mut sand: HashSet<(i32, i32)> = HashSet::new();

	loop {
		let obstacles: HashSet<(i32, i32)> = rocks.union(&sand).copied().collect();
		let mut current = (500, 0);
		loop {
			let down = (current.0, current.1 + 1);
			if down.1 > 2000 {
				return sand.len().to_string()
			}
			if obstacles.contains(&down) {
				let left = (current.0 - 1, current.1 + 1);
				if !obstacles.contains(&left) {
					current = left;
					continue;
				}
				let right = (current.0 + 1, current.1 + 1);
				if !obstacles.contains(&right) {
					current = right;
					continue;
				}
				sand.insert(current);
			} else {
				current = down;
				continue;
			}
			break;
		}
	}
}

fn solution_2(input: &str) -> String {
	let rocks = parse(input);
	let mut sand: HashSet<(i32, i32)> = HashSet::new();
	let end = rocks.iter().map(|(_, y)| y).max().unwrap();
	loop {
		let obstacles: HashSet<(i32, i32)> = rocks.union(&sand).copied().collect();
		let mut current = (500,0);
		if obstacles.contains(&current) {
			return sand.len().to_string();
		}
		loop {
			let down = (current.0, current.1 + 1);
			if down.1 == end + 2 {
				sand.insert(current);
				break;
			}
			if obstacles.contains(&down) {
				let left = (current.0 - 1, current.1 + 1);
				if !obstacles.contains(&left) {
					current = left;
					continue;
				}
				let right = (current.0 + 1, current.1 + 1);
				if !obstacles.contains(&right) {
					current = right;
					continue;
				}
				sand.insert(current);
			} else {
				current = down;
				continue;
			}
			break;
		}
	}
}

fn parse(input: &str) -> HashSet<(i32, i32)> {
	let mut set = HashSet::new();
	for line in input.lines() {
		let points: Vec<(i32, i32)> = line
			.split(" -> ")
			.map(|pair| {
				let parts: Vec<&str> = pair.split(",").collect();
				(parts[0].parse().unwrap(), parts[1].parse().unwrap())
			})
			.collect();

		for window in points.windows(2) {
			let a = window[0];
			let b = window[1];

			if a.0 == b.0 {
				let y1 = min(a.1, b.1);
				let y2 = max(a.1, b.1);
				for y in y1..=y2 {
					set.insert((a.0, y));
				}
			} else {
				let x1 = min(a.0, b.0);
				let x2 = max(a.0, b.0);
				for x in x1..=x2 {
					set.insert((x, a.1));
				}
			}
		}
	}

	set
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
