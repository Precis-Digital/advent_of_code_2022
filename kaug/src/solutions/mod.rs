use crate::solution::Solution;

mod day1;


pub fn get(day: &str) -> &dyn Solution {
  match day {
      "day1" => &day1::Day1,
      _=> panic!("Invalid day")
  }
}
