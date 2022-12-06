use sscanf::sscanf;
use crate::{solution::Solution, input};

pub struct Day4;

impl Solution for Day4 {
	fn name(&self) -> &'static str {
		"Day 4"
	}

	fn part_1(&self) -> String {
		let input = input::load(4);
		parser(&input, overlaps)
	}

	fn part_2(&self) -> String {
		let input = input::load(4);
		parser(&input, fully_contains)
	}
}

fn parser(input: &str, f : fn(i32, i32, i32, i32) -> bool) -> String {
	let lines: Vec<&str> = input.split("\n").collect();
	let mut count = 0;
	for line in lines {
		let (a, b, c, d) = sscanf!(line, "{i32}-{i32},{i32}-{i32}").unwrap();
		if f(a, b, c, d) {
			count += 1;
		}
	}
	count.to_string()
}

fn fully_contains(a:i32, b: i32, c: i32, d: i32) -> bool {
	(a <= c && b >= d) || (c <= a && d >= b)
}

fn overlaps(a:i32, b: i32, c: i32, d: i32) -> bool {
	!(b < c || d < a)
}