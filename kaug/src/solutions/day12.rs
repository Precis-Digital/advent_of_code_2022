use pathfinding::prelude::{bfs, Matrix};

use crate::{solution::Solution, input};
pub struct Day12;

impl Solution for Day12 {
	fn name(&self) -> &'static str {
		"Day 12"
	}

	fn part_1(&self) -> String {
		solution_1(input::load(12).as_str())
	}

	fn part_2(&self) -> String {
		solution_2(input::load(12).as_str())
	}
}

fn solution_1 (input: &str) -> String {
	let (map, start, end) = &parser(input);
	(bfs(
		start,
		|&p| map.neighbours(p, false).filter(move |&q| map[q] <= map[p] +1),
		|&p| p == *end,
	)
	.unwrap()
	.len() - 1).to_string()
}

fn solution_2 (input: &str) -> String {
	let (map, _, end) = &parser(input);
	(bfs(
		end,
		|&p| map.neighbours(p, false).filter(move |&q| map[p] <= map[q] +1),
		|&p| map[p] == b'a',
	)
	.unwrap()
	.len() - 1).to_string()
}

fn parser(input: &str) -> (Matrix<u8>, (usize, usize), (usize, usize)) {
	let mut map = Matrix::from_rows(input.lines().map(str::bytes)).unwrap();
	let start = map.indices().find(|p| map[*p] == b'S').unwrap();
	let end = map.indices().find(|p| map[*p] == b'E').unwrap();
	map[start] = b'a';
	map[end] = b'z';
	(map, start, end)
}


#[cfg(test)]
mod test {
	use super::*;

	const SAMPLE: &str = "Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi";

	#[test]
	fn part_1() {
		assert_eq!(solution_1(&SAMPLE), "31");
	}

	#[test]
	fn part_2() {
		assert_eq!(solution_2(&SAMPLE), "29");
	}
}