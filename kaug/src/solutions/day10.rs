use crate::{solution::Solution, input};

pub struct Day10;

impl Solution for Day10 {
	fn name(&self) -> &'static str {
		"Day 9"
	}

	fn part_1(&self) -> String {
		let input = input::load(10);
		parser(&input, solution_1)
	}

	fn part_2(&self) -> String {
		let input = input::load(10);
		parser(&input, solution_2)
	}
}

fn solution_1(lines: Vec<(&str, i32)>) -> String {
	let mut cycle = 1;
	let cycles = [20, 60, 100, 140, 180, 220];
	let mut x = 1;
	let mut signal_strength = 0;

	for row in lines {
		let mut iterations = 1;
		if row.0 == "addx" {
			iterations = 2;
		}
		for _ in 0..iterations {
			if cycles.contains(&cycle) {
				signal_strength += x * cycle;
			}
			cycle+=1;
		}
		x += row.1;
	}
	signal_strength.to_string()
}

fn solution_2(lines: Vec<(&str, i32)>) -> String {
	let mut x = 1;
	let mut rows = vec![String::new();6];
	let mut col = 0;
	let mut row = 0;
	for line in lines {
		let mut iterations = 1;
		if line.0 == "addx" {
			iterations = 2;
		}
		for _ in 0..iterations {
			let mut pixel = ".";
			if col == x || col == x-1 || col == x+1 {
				pixel = "#";
			}
			rows[row] = format!("{}{}", rows[row], pixel);
			col += 1;
			if col == 40 {
				col = 0;
				row += 1;
			}
		}
		x += line.1;
	}

	let mut result = String::from("\n");
	for r in rows {
		result = format!("{}{}\n", result, r)
	}
	result
}

fn parser(input: &str, f: fn (Vec<(&str, i32)>) -> String) -> String {
	let lines = input.lines()
		.map(|x| x.split_once(" ")
		.map(|y| (y.0, y.1.parse::<i32>().unwrap()))
		.unwrap_or(("noop", 0))).collect::<Vec<(&str, i32)>>();
	f(lines)
}

#[cfg(test)]
mod test {
	use std::fs;

use super::*;

	const OUTPUT_PART_2: &str = "
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
";

	#[test]
	fn part_1() {
		let input = fs::read_to_string("input/day10_sample.txt").unwrap();
		assert_eq!(parser(&input, solution_1), "13140");
	}

	#[test]
	fn part_2() {
		let input = fs::read_to_string("input/day10_sample.txt").unwrap();
		assert_eq!(parser(&input, solution_2), OUTPUT_PART_2);
	}
}