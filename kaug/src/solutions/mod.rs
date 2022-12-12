use crate::solution::Solution;

mod day1;
mod day2;
mod day3;
mod day4;
mod day5;
mod day6;
mod day7;
mod day8;
mod day9;
mod day10;
mod day11;
mod day12;


pub fn get(day: &str) -> &dyn Solution {
	match day {
		"day1" => &day1::Day1,
		"day2" => &day2::Day2,
		"day3" => &day3::Day3,
		"day4" => &day4::Day4,
		"day5" => &day5::Day5,
		"day6" => &day6::Day6,
		"day7" => &day7::Day7,
		"day8" => &day8::Day8,
		"day9" => &day9::Day9,
		"day10" => &day10::Day10,
		"day11" => &day11::Day11,
		"day12" => &day12::Day12,
		_=> panic!("Invalid day")
	}
}
