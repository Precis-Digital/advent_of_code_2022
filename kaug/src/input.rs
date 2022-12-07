use std::fs;

pub fn load(day: u32) -> String {
	let file = format!("input/day{day}.txt");
	fs::read_to_string(&file).unwrap()
}