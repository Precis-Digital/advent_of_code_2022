mod day1;
mod day2;
mod day3;
mod day4;
mod day5;

pub struct Solution {
	pub day: String,
	pub answer: (String, String)
}

impl Solution {
	pub fn build(args: &[String]) -> Result<Solution, &'static str> {
		if args.len() < 2 {
            return Err("not enough arguments");
        }
		let day: String = args[1].clone();
		let answer: (String, String) = match day.as_str() {
			"1" => day1::main(),
			"2" => day2::main(),
			"3" => day3::main(),
			"4" => day4::main(),
			"5" => day5::main(),
			_ => panic!("Invalid day")
		};
		Ok(Solution { day, answer })
	}
}