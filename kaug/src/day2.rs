use std::{fs, str::Split};

fn question_one(input: &str) -> i32 {
	let mut sum: i32 = 0;
	let games: Split<&str> = input.split("\n");
	for game in games {
		sum += match game {
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
	return sum;
}

fn question_two(input: &str) -> i32 {
	let mut sum: i32 = 0;
	let games: Split<&str> = input.split("\n");
	for game in games {
		sum += match game {
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
	return sum;
}

pub fn main() {
	let day_two_content: String = fs::read_to_string("./input/day2.txt").unwrap();
	println!("Day 2 | Question 1: {}", question_one(&day_two_content));
	println!("Day 2 | Question 2: {}", question_two(&day_two_content));
}