use std::{fs, str::Lines};

fn parse_pair(line: &str) -> ((i32, i32), (i32, i32)) {
    let assignments: Vec<&str> = line.split(",").collect();
    let a: (i32, i32) = parse_range(assignments[0]);
    let b: (i32, i32) = parse_range(assignments[1]);
    (a, b)
}

fn parse_range(assignment: &str) -> (i32, i32) {
    let range: Vec<&str> = assignment.split("-").collect();
    let low: i32 = range[0].parse::<i32>().unwrap();
    let high: i32 = range[1].parse::<i32>().unwrap();
    (low, high)
}

fn fully_contains(a: (i32, i32), b: (i32, i32)) -> bool {
    let (a_low, a_high) = a;
    let (b_low, b_high) = b;
    (a_low <= b_low && a_high  >= b_high) || (b_low <= a_low && b_high >= a_high)
}

fn overlaps(a: (i32, i32), b: (i32, i32)) -> bool {
    let (a_low, a_high) = a;
    let (b_low, b_high) = b;
    (a_low <= b_low && b_low <= a_high) || (b_low <= a_low && a_low <= b_high)
}

fn question_one(input: &str) -> i32 {
    let lines: Lines = input.lines();
    let pairs: Vec<((i32, i32), (i32, i32))> = lines.into_iter().map(|line| parse_pair(line)).collect();
    pairs.iter().filter(|&pair| fully_contains(pair.0, pair.1)).count() as i32
}

fn question_two(input: &str) -> i32 {
    let lines: Lines = input.lines();
    let pairs: Vec<((i32, i32), (i32, i32))> = lines.into_iter().map(|line| parse_pair(line)).collect();
    pairs.iter().filter(|&pair| overlaps(pair.0, pair.1)).count() as i32
}

pub fn main() {
    let input: String = fs::read_to_string("./input/day4.txt").unwrap();
    println!("Day 4 | Question 1: {}", question_one(&input));
    println!("Day 4 | Question 2: {}", question_two(&input));
}