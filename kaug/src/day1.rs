use std::{fs, str::Lines};

pub fn main() -> (String, String) {
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
	let ans1: String = sums[0].to_string();
	let ans2_sum: i32 = sums[0..3].iter().sum();
	let ans2: String = ans2_sum.to_string();
	
	return (ans1, ans2);
}

