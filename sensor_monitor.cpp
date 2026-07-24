// sensor_monitor.cpp — монитор датчиков (акселерометр, гироскоп, компас) на C++

#include <iostream>
#include <cmath>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <vector>

using namespace std;

// ANSI-цвета для красивого вывода
#define RESET   "\033[0m"
#define RED     "\033[91m"
#define GREEN   "\033[92m"
#define YELLOW  "\033[93m"
#define BLUE    "\033[94m"
#define MAGENTA "\033[95m"
#define CYAN    "\033[96m"

struct SensorData {
    double accel[3];
    double gyro[3];
    double mag[3];
    double angles[3];
};

class SensorSimulator {
private:
    SensorData data;
    double freq;
    bool running;

public:
    SensorSimulator(double f = 10.0) : freq(f), running(true) {
        srand(time(nullptr));
    }

    void update() {
        double t = time(nullptr);
        // Акселерометр
        data.accel[0] = 0.2 * sin(t * 0.5) + (rand() % 100 - 50) / 1000.0;
        data.accel[1] = 0.3 * cos(t * 0.7) + (rand() % 100 - 50) / 1000.0;
        data.accel[2] = 9.81 + 0.1 * sin(t * 0.3) + (rand() % 100 - 50) / 1000.0;

        // Гироскоп
        data.gyro[0] = 0.02 * sin(t * 0.8) + (rand() % 100 - 50) / 5000.0;
        data.gyro[1] = 0.03 * cos(t * 0.6) + (rand() % 100 - 50) / 5000.0;
        data.gyro[2] = 0.01 * sin(t * 0.9) + (rand() % 100 - 50) / 5000.0;

        // Магнитометр
        data.mag[0] = 15.0 + 2.0 * sin(t * 0.4) + (rand() % 100 - 50) / 100.0;
        data.mag[1] = -10.0 + 3.0 * cos(t * 0.5) + (rand() % 100 - 50) / 100.0;
        data.mag[2] = 40.0 + 4.0 * sin(t * 0.6) + (rand() % 100 - 50) / 100.0;

        // Углы
        data.angles[0] = 2.0 * sin(t * 0.2);   // roll
        data.angles[1] = 1.5 * cos(t * 0.25);  // pitch
        data.angles[2] = 45.0 + 10.0 * sin(t * 0.1); // yaw
    }

    void run() {
        while (running) {
            update();
            display();
            this_thread::sleep_for(chrono::milliseconds((int)(1000.0 / freq)));
        }
    }

    void stop() { running = false; }

    void display() {
        // Очистка экрана (ANSI)
        cout << "\033[2J\033[H";
        cout << CYAN << "📡 SensorMonitor Pro — C++ Edition" << RESET << endl;
        cout << "Частота: " << freq << " Гц\n" << endl;
        cout << "Акселерометр (м/с²):  X: " << fixed << setprecision(2) << setw(6) << data.accel[0]
             << "  Y: " << setw(6) << data.accel[1] << "  Z: " << setw(6) << data.accel[2] << endl;
        cout << "Гироскоп (рад/с):     X: " << setw(6) << data.gyro[0]
             << "  Y: " << setw(6) << data.gyro[1] << "  Z: " << setw(6) << data.gyro[2] << endl;
        cout << "Компас (мкТл):        X: " << setw(6) << data.mag[0]
             << "  Y: " << setw(6) << data.mag[1] << "  Z: " << setw(6) << data.mag[2] << endl;
        cout << "Углы:  Roll: " << setw(6) << data.angles[0] << "°  Pitch: " << setw(6) << data.angles[1]
             << "°  Yaw: " << setw(6) << data.angles[2] << "°" << endl;
        cout << RESET << "\nНажмите Ctrl+C для выхода" << endl;
    }

    SensorData getData() const { return data; }
};

int main(int argc, char* argv[]) {
    double freq = 10.0;
    if (argc > 1) freq = atof(argv[1]);
    if (freq < 1) freq = 1;
    if (freq > 100) freq = 100;

    SensorSimulator sim(freq);
    // Запускаем в отдельном потоке (для возможности остановки по Ctrl+C)
    thread t(&SensorSimulator::run, &sim);

    // Ждём сигнала Ctrl+C
    cin.get();
    sim.stop();
    t.join();
    return 0;
}
