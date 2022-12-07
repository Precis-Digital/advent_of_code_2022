use std::str::Chars;

use crate::{solution::Solution, input};

pub struct Day3;

impl Solution for Day3 {
	fn name(&self) -> &'static str {
		"Day 3"
	}

	fn part_1(&self) -> String {
		let input = input::load(3);
		parser_1(&input)
	}

	fn part_2(&self) -> String {
		let input = input::load(3);
		parser_2(&input)
	}
}

fn parser_1(input: &str) -> String {
	let rucksacks: Vec<&str>  = input.split("\n").collect();
	let mut sum: i32 = 0;
	for rucksack in rucksacks {
		let (a, b) = rucksack.split_at(rucksack.len() / 2);
		let mut a_items: Chars = a.chars();
		let common_item: Option<char> = a_items.find(|c: &char| b.contains(*c));
		let char: char = common_item.unwrap();
		sum += score(char)
	}
	sum.to_string()
}

fn parser_2(input: &str) -> String {
	let rucksacks: Vec<&str> = input.split("\n").collect();
	let mut sum: i32 = 0;
	for rucksack in rucksacks.chunks(3) {
		for c in rucksack[0].chars() {
			if rucksack[1].contains(c) && rucksack[2].contains(c) {
				sum += score(c);
				break;
			}
		}
	}
	sum.to_string()
}

fn score(item: char) -> i32 {
	match item {
		'A'..='Z' => item as i32 - 'A' as i32 + 27,
		'a'..='z' => item as i32 - 'a' as i32 + 1,
		_ => 0,
	}
}

#[cfg(test)]
mod test {
    use super::*;

	const SAMPLE: &str = "vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw";

	#[test]
	fn part_1() {
		assert_eq!(parser_1(&SAMPLE), "157");
	}

	#[test]
	fn part_2() {
		assert_eq!(parser_2(&SAMPLE), "70");
	}
}