use crate::solution::Solution;

mod day1;
mod day6;


pub fn get(day: &str) -> &dyn Solution {
  match day {
      "day1" => &day1::Day1,
      "day6" => &day6::Day6,
      _=> panic!("Invalid day")
  }
}
