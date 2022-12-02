use std::{fs, str::Split, time::Instant};

pub fn main() {
	// start exec timer
	let start = Instant::now();
	
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

	let question_one_answer: i32 = sums[0];
	let question_two_anwser: i32 = sums[0..3].iter().sum();
	println!("Day 1 | Question 1: {}", question_one_answer);
	println!("Day 1 | Question 2: {}", question_two_anwser);
	
	// end exec timer
	let duration = start.elapsed();
	println!("Day 1 | Duration: {:?}", duration);
}

