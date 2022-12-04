use std::{fs, str::Split};

pub fn main() {
	let day_one_content: String = fs::read_to_string("./input/day1.txt").unwrap();
	let elves: Split<&str> = day_one_content.split("\n\n");
	let mut sums: Vec<i32> = Vec::new();
	for elf in elves {
		let kcal: Split<&str> = elf.split("\n");
		let mut sum: i32 = 0;
		for item in kcal {
			sum = sum + item.parse::<i32>().unwrap();
		}
		sums.push(sum)
	}
	sums.sort();
	sums.reverse();
	let ans1: i32 = sums[0];
	let ans2: i32 = sums[0..3].iter().sum();
	println!("Day 1 | Question 1: {}", ans1);
	println!("Day 1 | Question 2: {}", ans2);
}

