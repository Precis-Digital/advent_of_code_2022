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
		parser(&input, contains)
	}
}

fn parser(input: &str, asserter : fn(i32, i32, i32, i32) -> bool) -> String {
	let lines: Vec<&str> = input.split("\n").collect();
	let mut count = 0;
	for line in lines {
		let (a, b, c, d) = sscanf!(line, "{i32}-{i32},{i32}-{i32}").unwrap();
		if asserter(a, b, c, d) {
			count += 1;
		}
	}
	count.to_string()
}

fn overlaps(a:i32, b: i32, c: i32, d: i32) -> bool {
	(a <= c && b >= d) || (c <= a && d >= b)
}

fn contains(a:i32, b: i32, c: i32, d: i32) -> bool {
	!(b < c || d < a)
}

#[cfg(test)]
mod test {
    use super::*;

	const SAMPLE: &str = "2-4,6-8\n2-3,4-5\n5-7,7-9\n2-8,3-7\n6-6,4-6\n2-6,4-8";

	#[test]
	fn part_1() {
		assert_eq!(parser(&SAMPLE, overlaps), "2");
	}

	#[test]
	fn part_2() {
		assert_eq!(parser(&SAMPLE, contains), "4");
	}
}