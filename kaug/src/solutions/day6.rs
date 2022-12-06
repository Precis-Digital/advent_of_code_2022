use std::collections::HashSet;

use crate::{solution::Solution, input};

pub struct Day6;

impl Solution for Day6 {
	fn name(&self) -> &'static str {
		"Day 6"
	}

	fn part_1(&self) -> String {
		let input = input::load(6);
		let result = parser(&input, 4);
		result.to_string()
	}

	fn part_2(&self) -> String {
		let input = input::load(6);
		let result = parser(&input, 14);
		result.to_string()
	}
}

fn parser(input: &str, num_char: usize) -> usize {
	for i in num_char..input.len() + 1 {
		let hashmap: HashSet<char> = input[i-num_char..i].chars().collect();
		if hashmap.len() == num_char {
		  return i;
		}
	  }
	return 0;
}
