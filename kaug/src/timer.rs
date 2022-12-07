use core::f32;
use std::time::SystemTime;

pub struct Timer {
	timer : SystemTime
}

impl Timer {
	pub fn new() -> Timer {
		Timer {
			timer : SystemTime::now()
		}
	}

	fn print(&self) {
		let elapsed = 0.001*(self.timer.elapsed().unwrap().as_millis() as f32);
		println!("------- {}s -------", elapsed);
	}  
}

impl Drop for Timer {
	fn drop(&mut self) {
		self.print();
	}
}