use clap::Parser;

use crate::timer::Timer;

mod solutions;
mod solution;
mod input;
mod timer;

/// Runs the solution for the 2022 Advent of Code
#[derive(Parser)]
struct Cli {
    /// the day to run
    day: String
}


fn main() {
	let args: Cli = Cli::parse();

	let _timer = Timer::new();
	let solution = solutions::get(&args.day);

	println!("----- 2022 {} -----", solution.name());
	println!("part_1: {}", solution.part_1());
	println!("part_2: {}", solution.part_2());
}