# sensor_monitor_python.py — монитор датчиков (акселерометр, гироскоп, компас) на Python

import math
import random
import time
import threading
import argparse
from datetime import datetime

# Попробуем импортировать matplotlib для графиков (если доступно)
try:
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    HAS_MATPLOTLIB = True
except:
    HAS_MATPLOTLIB = False

class SensorSimulator:
    def __init__(self, freq=10):
        self.freq = freq
        self.running = True
        self.accel = [0.0, 0.0, 0.0]   # X, Y, Z (м/с²)
        self.gyro = [0.0, 0.0, 0.0]    # X, Y, Z (рад/с)
        self.mag = [0.0, 0.0, 0.0]     # X, Y, Z (мкТл)
        self.angles = [0.0, 0.0, 0.0]  # roll, pitch, yaw (градусы)
        self.timestamp = time.time()
        self.lock = threading.Lock()
        self.history = {'accel': [], 'gyro': [], 'mag': [], 'time': []}

    def update(self):
        # Генерация плавных изменений с помощью синусоид
        t = time.time()
        # Акселерометр: добавляем небольшие колебания вокруг 9.81 по Z
        self.accel[0] = 0.2 * math.sin(t * 0.5) + random.uniform(-0.05, 0.05)
        self.accel[1] = 0.3 * math.cos(t * 0.7) + random.uniform(-0.05, 0.05)
        self.accel[2] = 9.81 + 0.1 * math.sin(t * 0.3) + random.uniform(-0.05, 0.05)

        # Гироскоп: небольшие вращения
        self.gyro[0] = 0.02 * math.sin(t * 0.8) + random.uniform(-0.01, 0.01)
        self.gyro[1] = 0.03 * math.cos(t * 0.6) + random.uniform(-0.01, 0.01)
        self.gyro[2] = 0.01 * math.sin(t * 0.9) + random.uniform(-0.01, 0.01)

        # Магнитометр: изменчивое поле
        self.mag[0] = 15.0 + 2.0 * math.sin(t * 0.4) + random.uniform(-0.5, 0.5)
        self.mag[1] = -10.0 + 3.0 * math.cos(t * 0.5) + random.uniform(-0.5, 0.5)
        self.mag[2] = 40.0 + 4.0 * math.sin(t * 0.6) + random.uniform(-0.5, 0.5)

        # Углы (из гироскопа или акселерометра) — простая симуляция
        self.angles[0] = 2.0 * math.sin(t * 0.2)  # roll
        self.angles[1] = 1.5 * math.cos(t * 0.25) # pitch
        self.angles[2] = 45.0 + 10.0 * math.sin(t * 0.1) # yaw (азимут)

        self.timestamp = time.time()
        # Сохраняем историю для графиков
        if HAS_MATPLOTLIB:
            with self.lock:
                self.history['time'].append(self.timestamp)
                self.history['accel'].append(self.accel.copy())
                self.history['gyro'].append(self.gyro.copy())
                self.history['mag'].append(self.mag.copy())
                # Ограничиваем историю до 100 точек
                if len(self.history['time']) > 100:
                    for key in self.history:
                        self.history[key].pop(0)

    def run(self):
        while self.running:
            self.update()
            time.sleep(1.0 / self.freq)

    def stop(self):
        self.running = False

def main():
    parser = argparse.ArgumentParser(description="Монитор датчиков")
    parser.add_argument('--freq', type=int, default=10, help='Частота обновления (Гц)')
    parser.add_argument('--plot', action='store_true', help='Показать графики (требуется matplotlib)')
    args = parser.parse_args()

    sim = SensorSimulator(freq=args.freq)

    # Запускаем поток для обновления датчиков
    thread = threading.Thread(target=sim.run, daemon=True)
    thread.start()

    if args.plot and HAS_MATPLOTLIB:
        # Создаём три графика для акселерометра, гироскопа и компаса
        fig, axes = plt.subplots(3, 1, figsize=(10, 8))
        ax1, ax2, ax3 = axes
        ax1.set_title('Акселерометр (м/с²)')
        ax2.set_title('Гироскоп (рад/с)')
        ax3.set_title('Магнитометр (мкТл)')

        lines1 = [ax1.plot([], [], label=f'{axis}')[0] for axis in ['X', 'Y', 'Z']]
        lines2 = [ax2.plot([], [], label=f'{axis}')[0] for axis in ['X', 'Y', 'Z']]
        lines3 = [ax3.plot([], [], label=f'{axis}')[0] for axis in ['X', 'Y', 'Z']]

        for ax in axes:
            ax.legend()
            ax.grid(True)

        def update_plot(frame):
            with sim.lock:
                times = sim.history['time']
                accel_data = sim.history['accel']
                gyro_data = sim.history['gyro']
                mag_data = sim.history['mag']
                if not times:
                    return lines1 + lines2 + lines3
                t = times
                # Акселерометр
                for i in range(3):
                    y = [d[i] for d in accel_data]
                    lines1[i].set_data(t, y)
                # Гироскоп
                for i in range(3):
                    y = [d[i] for d in gyro_data]
                    lines2[i].set_data(t, y)
                # Магнитометр
                for i in range(3):
                    y = [d[i] for d in mag_data]
                    lines3[i].set_data(t, y)
                for ax in axes:
                    ax.relim()
                    ax.autoscale_view()
                return lines1 + lines2 + lines3

        ani = FuncAnimation(fig, update_plot, interval=100, blit=False)
        plt.tight_layout()
        plt.show()
    else:
        # Консольный режим
        try:
            while True:
                with sim.lock:
                    acc = sim.accel
                    gyr = sim.gyro
                    mag = sim.mag
                    ang = sim.angles
                print(f"\033[2J\033[H")  # clear screen
                print("📡 SensorMonitor Pro — Python Edition")
                print(f"Частота: {args.freq} Гц\n")
                print(f"Акселерометр (м/с²):  X: {acc[0]:6.2f}  Y: {acc[1]:6.2f}  Z: {acc[2]:6.2f}")
                print(f"Гироскоп (рад/с):     X: {gyr[0]:6.2f}  Y: {gyr[1]:6.2f}  Z: {gyr[2]:6.2f}")
                print(f"Компас (мкТл):        X: {mag[0]:6.2f}  Y: {mag[1]:6.2f}  Z: {mag[2]:6.2f}")
                print(f"Углы:  Roll: {ang[0]:6.1f}°  Pitch: {ang[1]:6.1f}°  Yaw: {ang[2]:6.1f}°")
                print("\nНажмите Ctrl+C для выхода")
                time.sleep(1.0 / args.freq)
        except KeyboardInterrupt:
            sim.stop()
            print("\nВыход...")

if __name__ == "__main__":
    main()
