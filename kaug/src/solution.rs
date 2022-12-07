pub trait Solution {
	fn name(&self) -> &'static str;
	fn part_1(&self) -> String;
	fn part_2(&self) -> String;
}