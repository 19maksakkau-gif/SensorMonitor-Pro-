// SensorMonitorJava.java — монитор датчиков (акселерометр, гироскоп, компас) на Java

import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

public class SensorMonitorJava {
    private static class SensorData {
        double[] accel = new double[3];
        double[] gyro = new double[3];
        double[] mag = new double[3];
        double[] angles = new double[3];
    }

    private static SensorData data = new SensorData();
    private static Random rand = new Random();
    private static boolean running = true;

    public static void main(String[] args) {
        int freq = 10;
        if (args.length > 0) {
            try { freq = Integer.parseInt(args[0]); } catch (NumberFormatException e) {}
        }
        if (freq < 1) freq = 1;
        if (freq > 100) freq = 100;

        System.out.println("📡 SensorMonitor Pro — Java Edition");
        System.out.println("Частота: " + freq + " Гц");
        System.out.println("Нажмите Ctrl+C для выхода");

        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                updateData();
                displayData();
            }
        }, 0, 1000 / freq);

        // Ждём прерывания
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            running = false;
            timer.cancel();
            System.out.println("\nВыход...");
        }));

        try {
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException e) {}
    }

    private static void updateData() {
        double t = System.currentTimeMillis() / 1000.0;
        // Акселерометр
        data.accel[0] = 0.2 * Math.sin(t * 0.5) + (rand.nextDouble() - 0.5) * 0.1;
        data.accel[1] = 0.3 * Math.cos(t * 0.7) + (rand.nextDouble() - 0.5) * 0.1;
        data.accel[2] = 9.81 + 0.1 * Math.sin(t * 0.3) + (rand.nextDouble() - 0.5) * 0.1;

        // Гироскоп
        data.gyro[0] = 0.02 * Math.sin(t * 0.8) + (rand.nextDouble() - 0.5) * 0.02;
        data.gyro[1] = 0.03 * Math.cos(t * 0.6) + (rand.nextDouble() - 0.5) * 0.02;
        data.gyro[2] = 0.01 * Math.sin(t * 0.9) + (rand.nextDouble() - 0.5) * 0.02;

        // Магнитометр
        data.mag[0] = 15.0 + 2.0 * Math.sin(t * 0.4) + (rand.nextDouble() - 0.5) * 1.0;
        data.mag[1] = -10.0 + 3.0 * Math.cos(t * 0.5) + (rand.nextDouble() - 0.5) * 1.0;
        data.mag[2] = 40.0 + 4.0 * Math.sin(t * 0.6) + (rand.nextDouble() - 0.5) * 1.0;

        // Углы
        data.angles[0] = 2.0 * Math.sin(t * 0.2);
        data.angles[1] = 1.5 * Math.cos(t * 0.25);
        data.angles[2] = 45.0 + 10.0 * Math.sin(t * 0.1);
    }

    private static void displayData() {
        // Очистка консоли (ANSI)
        System.out.print("\033[H\033[2J");
        System.out.flush();
        System.out.println("📡 SensorMonitor Pro — Java Edition");
        System.out.printf("Акселерометр (м/с²):  X: %6.2f  Y: %6.2f  Z: %6.2f%n",
                data.accel[0], data.accel[1], data.accel[2]);
        System.out.printf("Гироскоп (рад/с):     X: %6.2f  Y: %6.2f  Z: %6.2f%n",
                data.gyro[0], data.gyro[1], data.gyro[2]);
        System.out.printf("Компас (мкТл):        X: %6.2f  Y: %6.2f  Z: %6.2f%n",
                data.mag[0], data.mag[1], data.mag[2]);
        System.out.printf("Углы:  Roll: %6.1f°  Pitch: %6.1f°  Yaw: %6.1f°%n",
                data.angles[0], data.angles[1], data.angles[2]);
        System.out.println("\nНажмите Ctrl+C для выхода");
    }
}
