use std::env;
use kaug::Solution;


fn main() {
	let args: Vec<String> = env::args().collect();

	let s: Solution = Solution::build(&args).unwrap();

	println!("Day {} | Question 1: {} | Question 2: {}", s.day, s.answer.0, s.answer.1)
}