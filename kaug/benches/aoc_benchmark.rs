use criterion::{criterion_group, criterion_main, Criterion};
use kaug::*;

fn criterion_benchmark(c: &mut Criterion) {
	let days = vec![
		//"day1", "day2", "day3", "day4", "day5",
		//"day6", "day7", "day8", "day9", "day10",
		//"day11", "day12", "day13", "day14"
		"day15"
	];
	for day in days {
		c.bench_function(format!("{}_part_1", &day).as_str(), |b| b.iter(|| {
			solutions::get(day).part_1()
		}));
		c.bench_function(format!("{}_part_2", &day).as_str(), |b| b.iter(|| {
			solutions::get(day).part_2()
		}));	
	}

}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);