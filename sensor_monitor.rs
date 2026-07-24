// sensor_monitor.rs — монитор датчиков (акселерометр, гироскоп, компас) на Rust

use std::f64::consts::PI;
use std::time::{Duration, Instant};
use std::thread;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use rand::Rng;
use termion::{clear, cursor, color, style};

struct SensorData {
    accel: [f64; 3],
    gyro: [f64; 3],
    mag: [f64; 3],
    angles: [f64; 3],
}

fn update_data() -> SensorData {
    let t = Instant::now().elapsed().as_secs_f64();
    let mut rng = rand::thread_rng();
    SensorData {
        accel: [
            0.2 * (t * 0.5).sin() + (rng.gen::<f64>() - 0.5) * 0.1,
            0.3 * (t * 0.7).cos() + (rng.gen::<f64>() - 0.5) * 0.1,
            9.81 + 0.1 * (t * 0.3).sin() + (rng.gen::<f64>() - 0.5) * 0.1,
        ],
        gyro: [
            0.02 * (t * 0.8).sin() + (rng.gen::<f64>() - 0.5) * 0.02,
            0.03 * (t * 0.6).cos() + (rng.gen::<f64>() - 0.5) * 0.02,
            0.01 * (t * 0.9).sin() + (rng.gen::<f64>() - 0.5) * 0.02,
        ],
        mag: [
            15.0 + 2.0 * (t * 0.4).sin() + (rng.gen::<f64>() - 0.5) * 1.0,
            -10.0 + 3.0 * (t * 0.5).cos() + (rng.gen::<f64>() - 0.5) * 1.0,
            40.0 + 4.0 * (t * 0.6).sin() + (rng.gen::<f64>() - 0.5) * 1.0,
        ],
        angles: [
            2.0 * (t * 0.2).sin(),
            1.5 * (t * 0.25).cos(),
            45.0 + 10.0 * (t * 0.1).sin(),
        ],
    }
}

fn display(data: &SensorData) {
    print!("{}{}", clear::All, cursor::Goto(1, 1));
    println!("{}📡 SensorMonitor Pro — Rust Edition{}", color::Fg(color::Cyan), style::Reset);
    println!("Акселерометр (м/с²):  X: {:6.2}  Y: {:6.2}  Z: {:6.2}",
             data.accel[0], data.accel[1], data.accel[2]);
    println!("Гироскоп (рад/с):     X: {:6.2}  Y: {:6.2}  Z: {:6.2}",
             data.gyro[0], data.gyro[1], data.gyro[2]);
    println!("Компас (мкТл):        X: {:6.2}  Y: {:6.2}  Z: {:6.2}",
             data.mag[0], data.mag[1], data.mag[2]);
    println!("Углы:  Roll: {:6.1}°  Pitch: {:6.1}°  Yaw: {:6.1}°",
             data.angles[0], data.angles[1], data.angles[2]);
    println!("\n{}Нажмите Ctrl+C для выхода{}", color::Fg(color::White), style::Reset);
}

fn main() {
    let running = Arc::new(AtomicBool::new(true));
    let r = running.clone();
    ctrlc::set_handler(move || {
        r.store(false, Ordering::SeqCst);
        println!("\nВыход...");
    }).expect("Ошибка установки обработчика Ctrl+C");

    let freq = 10; // Гц
    let interval = Duration::from_secs_f64(1.0 / freq as f64);

    while running.load(Ordering::SeqCst) {
        let data = update_data();
        display(&data);
        thread::sleep(interval);
    }
}
