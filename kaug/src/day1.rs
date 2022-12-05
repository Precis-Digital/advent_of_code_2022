use std::{fs, str::Lines};

pub fn main() {
	let day_one_content: String = fs::read_to_string("./input/day1.txt").unwrap();
	let lines: Lines = day_one_content.lines();
	let mut sums: Vec<i32> = Vec::new();
	let mut sum: i32 = 0;
	for kcal in lines {
		if kcal != "" {
			sum += kcal.parse::<i32>().unwrap();
		} else {
			sums.push(sum);
			sum = 0;
		}
	}
	sums.sort();
	sums.reverse();
	let ans1: i32 = sums[0];
	let ans2: i32 = sums[0..3].iter().sum();
	println!("Day 1 | Question 1: {}", ans1);
	println!("Day 1 | Question 2: {}", ans2);
}

