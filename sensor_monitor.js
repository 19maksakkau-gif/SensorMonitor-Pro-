// sensor_monitor.js — монитор датчиков (акселерометр, гироскоп, компас) на JavaScript (Node.js)

const readline = require('readline');

// ANSI-цвета
const colors = {
    cyan: '\x1b[96m',
    reset: '\x1b[0m',
    green: '\x1b[92m',
    yellow: '\x1b[93m',
    magenta: '\x1b[95m',
    blue: '\x1b[94m'
};

function clearScreen() {
    console.clear();
}

function updateData() {
    const t = Date.now() / 1000;
    return {
        accel: [
            0.2 * Math.sin(t * 0.5) + (Math.random() - 0.5) * 0.1,
            0.3 * Math.cos(t * 0.7) + (Math.random() - 0.5) * 0.1,
            9.81 + 0.1 * Math.sin(t * 0.3) + (Math.random() - 0.5) * 0.1
        ],
        gyro: [
            0.02 * Math.sin(t * 0.8) + (Math.random() - 0.5) * 0.02,
            0.03 * Math.cos(t * 0.6) + (Math.random() - 0.5) * 0.02,
            0.01 * Math.sin(t * 0.9) + (Math.random() - 0.5) * 0.02
        ],
        mag: [
            15.0 + 2.0 * Math.sin(t * 0.4) + (Math.random() - 0.5) * 1.0,
            -10.0 + 3.0 * Math.cos(t * 0.5) + (Math.random() - 0.5) * 1.0,
            40.0 + 4.0 * Math.sin(t * 0.6) + (Math.random() - 0.5) * 1.0
        ],
        angles: [
            2.0 * Math.sin(t * 0.2),
            1.5 * Math.cos(t * 0.25),
            45.0 + 10.0 * Math.sin(t * 0.1)
        ]
    };
}

function display(data) {
    clearScreen();
    console.log(`${colors.cyan}📡 SensorMonitor Pro — JavaScript Edition${colors.reset}`);
    console.log(`Акселерометр (м/с²):  X: ${data.accel[0].toFixed(2)}  Y: ${data.accel[1].toFixed(2)}  Z: ${data.accel[2].toFixed(2)}`);
    console.log(`Гироскоп (рад/с):     X: ${data.gyro[0].toFixed(2)}  Y: ${data.gyro[1].toFixed(2)}  Z: ${data.gyro[2].toFixed(2)}`);
    console.log(`Компас (мкТл):        X: ${data.mag[0].toFixed(2)}  Y: ${data.mag[1].toFixed(2)}  Z: ${data.mag[2].toFixed(2)}`);
    console.log(`Углы:  Roll: ${data.angles[0].toFixed(1)}°  Pitch: ${data.angles[1].toFixed(1)}°  Yaw: ${data.angles[2].toFixed(1)}°`);
    console.log(`\nНажмите Ctrl+C для выхода`);
}

function main() {
    const freq = 10;
    const interval = 1000 / freq;

    // Обработка Ctrl+C
    process.on('SIGINT', () => {
        console.log('\nВыход...');
        process.exit(0);
    });

    setInterval(() => {
        const data = updateData();
        display(data);
    }, interval);
}

main();
