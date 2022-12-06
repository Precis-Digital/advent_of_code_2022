use crate::solution::Solution;

mod day1;
mod day2;
mod day3;
mod day4;
mod day5;
mod day6;


pub fn get(day: &str) -> &dyn Solution {
  match day {
      "day1" => &day1::Day1,
      "day2" => &day2::Day2,
      "day3" => &day3::Day3,
      "day4" => &day4::Day4,
      "day5" => &day5::Day5,
      "day6" => &day6::Day6,
      _=> panic!("Invalid day")
  }
}
