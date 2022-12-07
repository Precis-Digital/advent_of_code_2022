use crate::{solution::Solution, input};

pub struct Day1;

impl Solution for Day1 {
	fn name(&self) -> &'static str {
		"Day 1"
	}

	fn part_1(&self) -> String {
		let input = input::load(1);
		parser(&input, 1)
	}

	fn part_2(&self) -> String {
		let input = input::load(1);
		parser(&input, 3)
	}
}

fn parser(input: &str, top: usize) -> String {
	let mut result = input
		.split("\n\n")
		.map(|elf| elf.lines().map(|kcal| kcal.parse::<i32>().unwrap()).sum())
		.collect::<Vec<i32>>();
	result.sort();
	result.reverse();
	result.into_iter().take(top).sum::<i32>().to_string()
}

#[cfg(test)]
mod test {
    use super::*;

	const SAMPLE: &str = "1000\n2000\n3000\n\n4000\n\n5000\n6000\n\n7000\n8000\n9000\n\n10000";

	#[test]
	fn part_1() {
		assert_eq!(parser(&SAMPLE, 1), "24000");
	}

	#[test]
	fn part_2() {
		assert_eq!(parser(&SAMPLE, 3), "45000");
	}
}
