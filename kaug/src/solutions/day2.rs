use crate::{solution::Solution, input};

pub struct Day2;

impl Solution for Day2 {
	fn name(&self) -> &'static str {
		"Day 2"
	}

	fn part_1(&self) -> String {
		let input = input::load(2);
		parser(&input, map_1)
	}

	fn part_2(&self) -> String {
		let input = input::load(2);
		parser(&input, map_2)
	}
}

pub fn parser(input: &str, f: fn(&Vec<&str>) -> String) -> String {
	let games: Vec<&str> = input.split("\n").collect();
	f(&games)
}

fn map_1(games: &Vec<&str>) -> String {
	let mut sum: i32 = 0;
	for game in games {
		sum += match game.to_owned() {
			"A X" => 4,
			"A Y" => 8,
			"A Z" => 3,
			"B X" => 1,
			"B Y" => 5,
			"B Z" => 9,
			"C X" => 7,
			"C Y" => 2,
			"C Z" => 6,
			_ => 0
		};
	}
	return sum.to_string();
}

fn map_2(games: &Vec<&str>) -> String {
	let mut sum: i32 = 0;
	for game in games {
		sum += match game.to_owned() {
			"A X" => 3,
			"A Y" => 4,
			"A Z" => 8,
			"B X" => 1,
			"B Y" => 5,
			"B Z" => 9,
			"C X" => 2,
			"C Y" => 6,
			"C Z" => 7,
			_ => 0
		};
	}
	return sum.to_string();
}