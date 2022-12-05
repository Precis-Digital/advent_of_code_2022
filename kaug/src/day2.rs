use std::fs;

fn question_one(games: &Vec<&str>) -> String {
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

fn question_two(games: &Vec<&str>) -> String {
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

pub fn main() -> (String, String) {
	let input: String = fs::read_to_string("./input/day2.txt").unwrap();
	let games: Vec<&str> = input.lines().collect();
	(question_one(&games), question_two(&games))
}