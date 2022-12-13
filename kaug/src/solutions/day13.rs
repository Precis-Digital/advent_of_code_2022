use std::{str::Lines, cmp::Ordering};
use serde_json::Value;
use crate::{solution::Solution, input};

pub struct Day13;

impl Solution for Day13 {
	fn name(&self) -> &'static str {
		"Day 13"
	}

	fn part_1(&self) -> String {
		solution_1(input::load(13).as_str())
	}

	fn part_2(&self) -> String {
		solution_2(input::load(13).as_str())
	}
}

fn solution_1(input: &str) -> String {
	let packets = PacketsParser{ lines: input.lines() };
	let mut sum = 0;
	for (i, (p1, p2)) in packets.enumerate() {
		match compare_pair(&p1, &p2) {
			Some(Ordering::Less) | Some(Ordering::Equal) => {
				sum += i + 1
			},
			Some(Ordering::Greater) => {},
			None => panic!("Error ordering pair")
		}
	}
	sum.to_string()
}

fn solution_2(input: &str) -> String {
	let mut packets: Vec<Value> = input.lines()
		.filter(|l| l.len() > 0)
		.map(|l| serde_json::from_str(l).unwrap())
		.collect();
	
	let divider_1 = serde_json::to_value(vec![vec![2]]).unwrap();
	let divider_2 = serde_json::to_value(vec![vec![6]]).unwrap();
	packets.push(divider_1.clone());
	packets.push(divider_2.clone());
	packets.sort_by(|p1, p2| compare_pair(p1, p2).unwrap())
	
	let pos_1 = packets.iter().position(|e|compare_pair(e, &divider_1) == Some(Ordering::Equal)).unwrap();
	let pos_2 = packets.iter().position(|e|compare_pair(e, &divider_2) == Some(Ordering::Equal)).unwrap();
	
	((pos_1 + 1) * (pos_2 + 1)).to_string()
}

struct PacketsParser<'a> {
	lines: Lines<'a>,
}

impl<'a> Iterator for PacketsParser<'a> {
	type Item = (serde_json::Value, serde_json::Value);

	fn next(&mut self) -> Option<Self::Item> {
		let p1 = self.lines.next()?;
		let p2 = self.lines.next()?;
		let _empty = self.lines.next()?;
		Some((serde_json::from_str(p1).ok()?,
			serde_json::from_str(p2).ok()?))
	}
}

fn compare_pair(p1: &Value, p2: &Value) -> Option<Ordering> {
	match(p1, p2) {
		(Value::Array(a1), Value::Array(a2)) => {
			compare_vec(a1, a2)
		},
		(Value::Number(n1), Value::Number(n2)) => {
			n1.as_i64().unwrap().partial_cmp(&n2.as_i64().unwrap())
		},
		(Value::Array(a), Value::Number(_)) => {
			compare_vec(a, &vec![p2.clone()])
		},
		(Value::Number(_), Value::Array(b)) => {
			compare_vec(&vec![p1.clone()], b)
		},
		_ => panic!("Error comparing pair")
	}
}

fn compare_vec(v1: &Vec<Value>, v2: &Vec<Value>) -> Option<Ordering> {
	for(p1, p2) in v1.iter().zip(v2) {
		let cmp = compare_pair(p1, p2);
		if cmp != Some(Ordering::Equal) {
			return cmp;
		}
	}
	v1.len().partial_cmp(&v2.len())
}

#[cfg(test)]
mod test {
	use super::*;

	const SAMPLE: &str = "[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]";

	#[test]
	fn part_1() {
		assert_eq!(solution_1(&SAMPLE), "13");
	}

	#[test]
	fn part_2() {
		assert_eq!(solution_2(&SAMPLE), "140");
	}
}
