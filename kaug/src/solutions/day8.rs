use crate::{solution::Solution, input};

pub struct Day8;

impl Solution for Day8 {
	fn name(&self) -> &'static str {
		"Day 8"
	}

	fn part_1(&self) -> String {
		let input = input::load(8);
		parser(&input, solution_1)
	}

	fn part_2(&self) -> String {
		let input = input::load(8);
		parser(&input, solution_2)
	}
}

fn parser(input: &str, s: fn(Vec<Vec<i32>>) -> String) -> String {
	let mut trees_map = vec![];
	for line in input.split("\n") {
		trees_map.push(Vec::from_iter(line.chars().map(|x| x.to_string().parse::<i32>().unwrap())))
	}
	s(trees_map)
}

fn solution_1(trees: Vec<Vec<i32>>) -> String {
	let mut count = 0;
	for row in 0..trees.len() {
		for col in 0..trees[0].len() {
			let height = trees[row][col];
			if trees[..row].iter().all(|x| x[col] < height)
				|| trees[row][..col].iter().all(|x| x < &height)
				|| trees[row + 1..].iter().all(|x| x[col] < height)
				|| trees[row][col + 1..].iter().all(|x| x < &height)
			{
				count += 1
			}
		}
	}
	count.to_string()
}

fn solution_2(trees: Vec<Vec<i32>>) -> String {
	let mut high_score = 0;
	for row in 0..trees.len() {
		for col in 0..trees[0].len() {
			let mut ctx = (1, trees[row][col]);
			parse_score(&mut ctx, trees[..row].iter().map(|x| x[col]).rev());
			parse_score(&mut ctx, trees[row][..col].iter().rev().copied());
			parse_score(&mut ctx, trees[row + 1..].iter().map(|x| x[col]));
			parse_score(&mut ctx, trees[row][col + 1..].iter().copied());
			high_score = high_score.max(ctx.0);
		}
	}
	high_score.to_string()
}

fn parse_score((local_best, hieght): &mut (i32, i32), iter: impl Iterator<Item = i32>) {
	let mut score = 0;
	for i in iter {
		score += 1;
		if i >= *hieght {
			break;
		}
	}
	*local_best *= score;
}

#[cfg(test)]
mod test {
	use super::*;

	const SAMPLE: &str = "30373
25512
65332
33549
35390";

	#[test]
	fn part_1() {
		assert_eq!(parser(&SAMPLE, solution_1), "21");
	}

	#[test]
	fn part_2() {
		assert_eq!(parser(&SAMPLE, solution_2), "8");
	}
}
