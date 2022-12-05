use std::fs;
use std::str::{self, Chars};

fn question_one(rucksacks: &Vec<&str>) -> i32 {
	let mut sum: i32 = 0;
	for rucksack in rucksacks {
		let (a, b) = rucksack.split_at(rucksack.len() / 2);
		let mut a_items: Chars = a.chars();
		let common_item: Option<char> = a_items.find(|c: &char| b.contains(*c));
		let char: char = common_item.unwrap();
		sum += score(char)
	}
	return sum;
}

fn question_two(rucksacks: &Vec<&str>) -> i32 {
	let mut sum: i32 = 0;
	for rucksack in rucksacks.chunks(3) {
		for c in rucksack[0].chars() {
			if rucksack[1].contains(c) && rucksack[2].contains(c) {
				sum += score(c);
				break;
			}
		}
	}
	return sum;
}

fn score(item: char) -> i32 {
	match item {
		'A'..='Z' => item as i32 - 'A' as i32 + 27,
		'a'..='z' => item as i32 - 'a' as i32 + 1,
		_ => 0,
	}
}

pub fn main() -> (i32, i32) {		
	let input: String = fs::read_to_string("./input/day3.txt").unwrap();
	let rucksacks: Vec<&str> = input.lines().collect();
	(question_one(&rucksacks), question_two(&rucksacks))
}