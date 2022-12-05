use std::fs;

fn parse_pair(line: &str) -> ((i32, i32), (i32, i32)) {
	let assignments: Vec<&str> = line.split(",").collect();
	(parse_range(assignments[0]), parse_range(assignments[1]))
}

fn parse_range(assignment: &str) -> (i32, i32) {
	let range: Vec<&str> = assignment.split("-").collect();
	(range[0].parse::<i32>().unwrap(), range[1].parse::<i32>().unwrap())
}

fn fully_contains(a: (i32, i32), b: (i32, i32)) -> bool {
	(a.0 <= b.0 && a.1  >= b.1) || (b.0 <= a.0 && b.1 >= a.1)
}

fn overlaps(a: (i32, i32), b: (i32, i32)) -> bool {
	(a.0 <= b.0 && b.0 <= a.1) || (b.0 <= a.0 && a.0 <= b.1)
}

fn question_one(pairs: Vec<((i32, i32), (i32, i32))>) -> i32 {
	pairs.iter().filter(|&pair| fully_contains(pair.0, pair.1)).count() as i32
}

fn question_two(pairs: Vec<((i32, i32), (i32, i32))>) -> i32 {
	pairs.iter().filter(|&pair| overlaps(pair.0, pair.1)).count() as i32
}

pub fn main() -> (i32, i32) {
	let input: String = fs::read_to_string("./input/day4.txt").unwrap();
	let lines: Vec<&str> = input.lines().collect();
	let pairs: Vec<((i32, i32), (i32, i32))> = lines.iter().map(|line| parse_pair(line)).collect();
	(question_one(pairs.clone()), question_two(pairs))
}