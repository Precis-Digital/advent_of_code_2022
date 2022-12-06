use regex::Regex;

use crate::{input, solution::Solution};

struct Input {
	crates: Vec<Vec<char>>,
	moves: Vec<(usize, usize, usize)>
}

pub struct Day5;

impl Solution for Day5 {
	fn name(&self) -> &'static str {
		"Day 5"
	}

	fn part_1(&self) -> String {
		let file_input = input::load(5);
		let input = parse_input(&file_input);
		let mut crates: Vec<Vec<char>> = input.crates.clone();
		let moves: Vec<(usize, usize, usize)> = input.moves.clone();
		for(m, f, t) in moves {
			for _ in 0..m {
				let top: char = crates[f - 1].pop().unwrap();
				crates[t - 1].push(top)
			}
		}
		crates.iter().map(|c| c.last().copied().unwrap()).collect()
	}

	fn part_2(&self) -> String {
		let file_input = input::load(5);
		let input = parse_input(&file_input);
		let mut crates: Vec<Vec<char>> = input.crates.clone();
		let moves: Vec<(usize, usize, usize)> = input.moves.clone();
		for(m, f, t) in moves {
			let split: usize = crates[f - 1].len() - m;
			let mut top: Vec<char> = crates[f - 1].split_off(split);
			crates[t - 1].append(&mut top);
		}
		crates.iter().map(|c| c.last().copied().unwrap()).collect()
	}
}

fn parse_input(input: &str) -> Input {
	let (a, b) = input.split_once("\n\n").unwrap();
	let mut crate_input = a.lines().collect::<Vec<_>>();
	crate_input.pop();
	let num_crates: usize = (crate_input[0].len() + 1) / 4;
	let mut crates: Vec<Vec<char>> = vec![vec![]; num_crates];
	for line in crate_input {
		for(i, s) in crates.iter_mut().enumerate() {
			let c = line.as_bytes()[1 + 4 * i];
			if (b'A'..=b'Z').contains(&c) {
				s.push(c as char)
			}
		}
	}
	crates.iter_mut().for_each(|v| v.reverse());
	let re: Regex = Regex::new(r"^move (\d+) from (\d+) to (\d+)$").unwrap();
	let moves: Vec<(usize, usize, usize)> = b.
		lines()
		.map(|l| {
			let m = re.captures(l).unwrap();
			Ok((m[1].parse()?, m[2].parse()?, m[3].parse()?))
		})
		.collect::<Result<_, std::num::ParseIntError>>().unwrap();
	Input { crates, moves }
}