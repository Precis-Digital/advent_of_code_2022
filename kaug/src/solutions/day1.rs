use crate::{solution::Solution, input};

pub struct Day1;

impl Solution for Day1 {
	fn name(&self) -> &'static str {
		"Day 1"
	}

	fn part_1(&self) -> String {
		let input = input::load(1);
		let result = parser(&input);
		result[0].to_string()
	}

	fn part_2(&self) -> String {
		let input = input::load(1);
		let result = parser(&input);
		result.into_iter().take(3).sum::<i32>().to_string()
	}
}

fn parser(input: &str) -> Vec<i32> {
	let mut result = input
		.split("\n\n")
		.map(|elf| elf.lines().map(|kcal| kcal.parse::<i32>().unwrap()).sum())
		.collect::<Vec<i32>>();
	result.sort();
	result.reverse();
	result
}
