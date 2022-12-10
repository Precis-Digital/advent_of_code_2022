use std::{collections::HashSet, ops::{AddAssign, Sub}};

use crate::{solution::Solution, input};

pub struct Day9;

impl Solution for Day9 {
	fn name(&self) -> &'static str {
		"Day 9"
	}

	fn part_1(&self) -> String {
		let input = input::load(9);
		parser(&input, 2)
	}

	fn part_2(&self) -> String {
		let input = input::load(9);
		parser(&input, 10)
	}
}

fn parser(input: &str, n: usize) -> String {
	let movements = input.lines().map(Pos::parse_input).collect::<Vec<(Pos, i32)>>();
	let mut tail_map = HashSet::new();
	let mut knots = vec![Pos::init(0, 0); n];

    tail_map.insert(*knots.last().unwrap());
    for (dir, count) in movements {
        for _ in 0..count {
            knots[0] += dir;
            for i in 1..knots.len() {
                let diff = knots[i - 1] - knots[i];
                if diff.abs().max() <= 1 {
                    continue;
                }
                knots[i] += diff.signum();
            }
            tail_map.insert(*knots.last().unwrap());
        }
    }
	tail_map.len().to_string()
}

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
struct Pos {
	x: i32,
	y: i32
}

impl AddAssign for Pos {
	fn add_assign(&mut self, other: Self) {
		*self = Self {
			x: self.x + other.x,
			y: self.y + other.y
		}
	}
}

impl Sub for Pos {
	type Output = Self;

	fn sub(self, other: Self) -> Self::Output {
		Self {
			x: self.x - other.x,
			y: self.y - other.y,
		}
	}
}

impl Pos {
	fn init(x: i32, y: i32) -> Self {
		Self { x, y }
	}
	fn signum(&self) -> Self {
		Self { 
			x: self.x.signum(),
			y: self.y.signum()
		}
	}
	fn abs(&self) -> Self {
		Self { 
			x: self.x.abs(),
			y: self.y.abs() 
		}
	}
	fn max(&self) -> i32 {
		self.x.max(self.y)
	}
	fn parse_input(imp: &str) -> (Self, i32) {
		let (dir, count) = imp.split_once(" ").unwrap();
		let count = count.parse::<i32>().unwrap();

		let pos = match dir {
			"R" => Self::init(1, 0),
			"D" => Self::init(0, 1),
			"L" => Self::init(-1, 0),
			"U" => Self::init(0, -1),
			_ => panic!("Movement parsing error")
		};

		(pos, count)
	}
}

#[cfg(test)]
mod test {
	use super::*;

	const SAMPLE: &str = "R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2";

	const SAMPLE_2: &str ="R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20";

	#[test]
	fn part_1() {
		assert_eq!(parser(&SAMPLE, 2), "13");
	}

	#[test]
	fn part_2() {
		assert_eq!(parser(&SAMPLE_2, 10), "36");
	}
}
