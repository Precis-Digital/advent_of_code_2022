use crate::{solution::Solution, input};

pub struct Day7;

impl Solution for Day7 {
	fn name(&self) -> &'static str {
		"Day 7"
	}

	fn part_1(&self) -> String {
		let input = input::load(7);
		parser(&input, solution_1)
	}

	fn part_2(&self) -> String {
		let input = input::load(7);
		parser(&input, solution_2)
	}
}

fn parser(input: &str, s: fn(Vec<i32>) -> String) -> String {
	let lines: Vec<&str> = input.split("\n").collect();

	let mut dir: Vec<i32> = Vec::new();
	let mut directories: Vec<i32> = Vec::new();

	for line in lines {
		if line.starts_with("$ cd") {
			if line.contains("..") {
				directories.push(dir.pop().unwrap());
			} else {
				dir.push(0);
			}
		}
		if !line.starts_with("$") && !line.starts_with("dir") {
			let size = line.split(" ").nth(0).map(|s| s.parse::<i32>().unwrap()).unwrap();
			for i in &mut dir {
				*i += size
			}
		}
	}
	directories.extend(&dir);
	s(directories)
}

fn solution_1(directories: Vec<i32>) -> String {
	directories.iter().filter(|size| **size <= 100000).sum::<i32>().to_string()
}

fn solution_2(directories: Vec<i32>) -> String {
	let max = directories.iter().max().unwrap();
	let req = 30000000 - (70000000-max);
	directories.iter().filter(|size| **size >= req).min().unwrap().to_string()
}

#[cfg(test)]
mod test {
	use super::*;

	const SAMPLE: &str = "$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k";

	#[test]
	fn part_1() {
		assert_eq!(parser(&SAMPLE, solution_1), "95437");
	}

	#[test]
	fn part_2() {
		assert_eq!(parser(&SAMPLE, solution_2), "24933642");
	}
}
