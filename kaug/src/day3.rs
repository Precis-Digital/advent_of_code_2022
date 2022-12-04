use std::{fs, str::Lines};
use std::str::{self, Chars};

fn question_one(input: &str) -> i32 {
	let rucksacks: Lines = input.lines();
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

fn question_two(input: &str) -> i32 {
	let rucksacks: Vec<&str> = input.lines().collect();
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

pub fn main() {		
	let day_two_content: String = fs::read_to_string("./input/day3.txt").unwrap();
	println!("Day 3 | Question 1: {}", question_one(&day_two_content));
	println!("Day 3 | Question 2: {}", question_two(&day_two_content));
}