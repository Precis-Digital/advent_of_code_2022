use std::{collections::BinaryHeap, iter};

use crate::{solution::Solution, input};

pub struct Day11;

impl Solution for Day11 {
	fn name(&self) -> &'static str {
		"Day 11"
	}

	fn part_1(&self) -> String {
		solution(input::load(11).as_str(), 20, 3)
	}

	fn part_2(&self) -> String {
		solution(input::load(11).as_str(), 10000, 1)
	}
}

fn solution(input: &str, rounds: usize, relief: u64) -> String {
	iter::once(parser(input))
		.map(|m| (m.iter().map(|m| m.divisible_by).product(), m))
		.fold(0, |_, (modn, mut monkeys)| {
			for _ in 0..rounds {
				for m in 0..monkeys.len() {
					monkeys[m].inspect(modn, relief)
						.into_iter()
						.for_each(|(t, w)| monkeys[t].items.push(w))
				}
			}
			monkeys.iter()
				.map(|m| m.inspected_items)
				.collect::<BinaryHeap<_>>()
				.into_sorted_vec()
				.iter()
				.rev()
				.take(2)
				.product()
		}).to_string()
}

#[derive(Debug)]
struct Monkey {
	items: Vec<u64>,
	inspected_items: usize,
	operation: Operation,
	divisible_by: u64,
	yes: usize,
	no: usize,
}

impl Monkey {
	fn inspect(&mut self, modn: u64, relief: u64) -> Vec<(usize, u64)> {
		self.items.drain(..)
			.inspect(|_| self.inspected_items += 1)
			.map(|w| (self.operation.apply(w) % modn) / relief)
			.map(|w| (match w % self.divisible_by == 0 {
				true => self.yes,
				_ => self.no
			}, w))
			.collect()
	}
}

#[derive(Debug)]
enum Operation {
    Add(u64),
    Multiply(u64),
    Square,
}

impl Operation {
    fn apply(&self, b: u64) -> u64 {
        match self {
            Operation::Add(a) => a + b,
            Operation::Multiply(a) => a * b,
            Operation::Square => b * b,
        }
    }
}

fn parser(input: &str) -> Vec<Monkey> {
	input.split("\n\n")
		.flat_map(|m| <Vec<_> as TryInto<[_; 5]>>::try_into(m.lines()
			.skip(1)
			.map(str::trim)
			.map(|l| l.trim_start_matches("Starting items: ")
				.trim_start_matches("Operation: new = old ")
				.trim_start_matches("Test: divisible by ")
				.trim_start_matches("If true: throw to monkey ")
				.trim_start_matches("If false: throw to monkey "))
			.collect()).ok())
		.flat_map(|m| Some(Monkey {
			items: m[0].split(", ").flat_map(|i| i.parse().ok()).collect(),
			inspected_items: 0,
			operation: match m[1].split_once(" ")? {
				("+", n) => Operation::Add(n.parse().ok()?),
				("*", "old") => Operation::Square,
				(_, n) => Operation::Multiply(n.parse().ok()?)
			},
			divisible_by: m[2].parse().ok()?,
			yes: m[3].parse().ok()?,
			no: m[4].parse().ok()?,
		}))
		.collect()
}


#[cfg(test)]
mod test {
	use super::*;

	const SAMPLE: &str = "Monkey 0:
Starting items: 79, 98
Operation: new = old * 19
Test: divisible by 23
	If true: throw to monkey 2
	If false: throw to monkey 3

Monkey 1:
Starting items: 54, 65, 75, 74
Operation: new = old + 6
Test: divisible by 19
	If true: throw to monkey 2
	If false: throw to monkey 0

Monkey 2:
Starting items: 79, 60, 97
Operation: new = old * old
Test: divisible by 13
	If true: throw to monkey 1
	If false: throw to monkey 3

Monkey 3:
Starting items: 74
Operation: new = old + 3
Test: divisible by 17
	If true: throw to monkey 0
	If false: throw to monkey 1";

	#[test]
	fn part_1() {
		assert_eq!(solution(&SAMPLE, 20, 3), "10605");
	}

	#[test]
	fn part_2() {
		assert_eq!(solution(&SAMPLE, 10000, 1), "36");
	}
}