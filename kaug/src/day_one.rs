use std::fs;

pub fn main() {
  	let day_one_content = fs::read_to_string("./input/day1.txt")
		.expect("Should be able to read file");

	let elves = day_one_content.split("\n\n");
	
	let mut sums = Vec::new();

	for elf in elves {
		let kcal = elf.split("\n");
		let mut sum : i32 = 0;
		for item in kcal {
			sum = sum + item.parse::<i32>().unwrap();
		}
		sums.push(sum)
	}

	sums.sort();
	sums.reverse();

	let question_one_answer = sums[0];
	let question_two_anwser : i32 = sums[0..3].iter().sum();

	println!("Day 1 | Question 1: {}", question_one_answer);
	println!("Day 1 | Question 2: {}", question_two_anwser);
}

