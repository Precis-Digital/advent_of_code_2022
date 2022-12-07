use std::collections::HashSet;

use crate::{solution::Solution, input};

pub struct Day6;

impl Solution for Day6 {
	fn name(&self) -> &'static str {
		"Day 6"
	}

	fn part_1(&self) -> String {
		let input = input::load(6);
		parser(&input, 4)
	}

	fn part_2(&self) -> String {
		let input = input::load(6);
		parser(&input, 14)
	}
}

fn parser(input: &str, num_char: usize) -> String {
	for i in num_char..input.len() + 1 {
		let hashmap: HashSet<char> = input[i-num_char..i].chars().collect();
		if hashmap.len() == num_char {
		  return i.to_string();
		}
	  }
	return 0.to_string();
}

#[cfg(test)]
mod test {
    use super::*;

	#[test]
	fn part_1() {
		assert_eq!(parser("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4), "7");
		assert_eq!(parser("bvwbjplbgvbhsrlpgdmjqwftvncz", 4), "5");
		assert_eq!(parser("nppdvjthqldpwncqszvftbrmjlhg", 4), "6");
		assert_eq!(parser("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4), "10");
		assert_eq!(parser("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4), "11");
	}

	#[test]
	fn part_2() {
		assert_eq!(parser("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14), "19");
		assert_eq!(parser("bvwbjplbgvbhsrlpgdmjqwftvncz", 14), "23");
		assert_eq!(parser("nppdvjthqldpwncqszvftbrmjlhg", 14), "23");
		assert_eq!(parser("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14), "29");
		assert_eq!(parser("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14), "26");
	}
}
