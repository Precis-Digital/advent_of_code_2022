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
		let elapsed = self.timer.elapsed().unwrap();
		println!("------- {:?} -------", elapsed);
	}  
}

impl Drop for Timer {
	fn drop(&mut self) {
		self.print();
	}
}