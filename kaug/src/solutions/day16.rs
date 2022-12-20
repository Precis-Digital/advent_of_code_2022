use std::{collections::HashMap, cell::RefCell, cmp};
use regex::Regex;
use crate::{solution::Solution, input};

pub struct Day16;

impl Solution for Day16 {
	fn name(&self) -> &'static str {
		"Day 16"
	}

	fn part_1(&self) -> String {
		solution_1(input::load(16).as_str())
	}

	fn part_2(&self) -> String {
		solution_2(input::load(16).as_str())
	}
}

fn solution_1(input: &str) -> String {
	let valves = parser(&input);
	let distances = floyd_warshall(&valves);
	let mut answers = HashMap::new();
	let run = goto(String::from("AA"), &valves, &distances, 30, 0, 0, &mut answers);
	run.values().max().unwrap().to_string()
}

fn solution_2(input: &str) -> String {
	let valves = parser(&input);
	let distances = floyd_warshall(&valves);
	let mut answers = HashMap::new();
	let run = goto(String::from("AA"), &valves, &distances, 26, 0, 0, &mut answers);
	let mut total= 0;
	for (player_state, player_total) in run.iter() {
		for (elephant_state, elephant_total) in run.iter() {
			// Only care for states with no bits in common, i.e. 
			// player and the elephant hasn't opened the same valves.
			if (player_state & elephant_state) == 0 {
				if player_total + elephant_total > total {
					total = player_total + elephant_total;
				}
			}
		}
	}
	total.to_string()
}

#[derive(Debug)]
struct Valve {
	flow_rate: i64,
	mask: i64,
	neighbours: Vec<String>,
}

fn floyd_warshall(valves: &HashMap<String, Valve>) -> HashMap<(String, String), RefCell<i64>> {
	let mut distances = HashMap::new();
	for x in valves.keys() {
		for y in valves.keys() {
			if valves[x].neighbours.contains(y) {
				distances.entry((x.clone(), y.clone())).or_insert(RefCell::new(1));
			} else {
				distances.entry((x.clone(), y.clone())).or_insert(RefCell::new(999999));
			}
		}
	}
	for k in valves.keys() {
		for i in valves.keys() {
			for j in valves.keys() {
				let ij = distances[&(i.clone(), j.clone())].clone().take();
				let ik = distances[&(i.clone(), k.clone())].clone().take();
				let kj = distances[&(k.clone(), j.clone())].clone().take();
				distances.insert((i.clone(), j.clone()), RefCell::new(cmp::min(ij, ik + kj)));
			}
		}
	}
	distances
}

/// Recursively check all paths to find all possible outputs.
/// 
/// # Arguments
/// 
/// * `valve` - Valve that we're going to
/// * `valves`- HashMap containg all Valves
/// * `distances` HashMap of distances between all valves
/// * `time_left` - Time remaining
/// * `sate` Int/mask of valves that are turned on
/// * `total_flow` Flow calculated as total from each vavle when it's turned on
/// * `answers` HashMap containing all possible outputs. Key is state, value is max flow from that state
fn goto<'a>
(
	valve: String,
	valves: &HashMap<String, Valve>,
	distances: &HashMap<(String, String), RefCell<i64>>,
	time_left: i64,
	state: i64,
	total_flow: i64,	
	answers: &'a mut HashMap<i64, i64>
)
-> &'a mut HashMap<i64, i64> 
{
	let mut n = 0;
	
	if answers.contains_key(&state) {
		n = answers[&state].clone();
	}

	answers.insert(state, cmp::max(n, total_flow));
	// Iterate all valves, don't care about those with a flow rate of 0 
	// as it doesn't affect the results anymore since we have the distance.
	for name in valves.iter().filter(|(_, v)| v.flow_rate > 0).map(|(name, _)| name) {
		// Distance from valve we're at to the current valve in the iteration
		let dist = distances[&(valve.clone(), name.clone())].clone().take();
		let new_time_left = time_left - dist - 1;
		let mask = valves[name].mask;
		// Don't go to same Valve twice or don't go to a valve if we run out of time
		if (state & mask) != 0 || new_time_left < 0 {
			continue;
		} else {
			let flow_here = valves[name].flow_rate;
			// Go to new valve, update state (LSB) so that valve is turned on, add it's total flow, rinse and repeat
			let _ = goto(name.clone(), &valves, &distances, new_time_left, state | mask, total_flow + (new_time_left * flow_here), answers);
		}
	}
	answers
}

fn parser(input: &str) -> HashMap<String, Valve> {
	let re = Regex::new(r"Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnels? leads? to valves? (.+)").unwrap();
	let mut valves = HashMap::<String, Valve>::new();
	let mut i = 0;
	for line in input.lines() {
		let captures = re.captures(line).unwrap();
		let name = captures[1].to_string();
		let flow_rate = captures[2].parse().unwrap();
		let neighbours = captures[3].split(", ").map(|s| s.to_string()).collect();
		let valve = Valve {
			flow_rate,
			mask: 1 << i,
			neighbours
		};
		valves.insert(name, valve);
		i += 1;
	}
	valves
}



#[cfg(test)]
mod test {
	use super::*;

	const SAMPLE: &str = "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II";

	#[test]
	fn part_1() {
		assert_eq!(solution_1(&SAMPLE), "1651");
	}

	#[test]
	fn part_2() {
		assert_eq!(solution_2(&SAMPLE), "1707");
	}
}