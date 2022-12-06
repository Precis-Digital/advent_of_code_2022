use std::collections::HashSet;

use crate::{solution::Solution, input};

pub struct Day6;

impl Solution for Day6 {
	fn name(&self) -> &'static str {
		"Day 1"
	}

	fn part_1(&self) -> String {
		let input = input::load(6);
		let result = parser(&input, 3);
		result.to_string()
	}

	fn part_2(&self) -> String {
		let input = input::load(6);
		let result = parser(&input, 13);
		result.to_string()
	}
}

fn has_unique_values(iter: &Vec<char>) -> bool {
    let mut uniq = HashSet::new();
    iter.into_iter().all(move |x| uniq.insert(x))
}

fn parser(input: &str, num_char: i32) -> i32 {
	let (a, b) = input.split_at(num_char as usize);
	let mut last_three: Vec<char> = a.chars().collect();
	let start_from: Vec<char> = b.chars().collect();
	let mut pos = num_char;
	for c in start_from {
		pos += 1;
		if last_three.contains(&c) || !has_unique_values(&last_three) {
			last_three.remove(0);
			last_three.push(c);
		} else {
			return pos
		}
	}
	pos
}
