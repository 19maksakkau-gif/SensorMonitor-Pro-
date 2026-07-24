// SensorMonitorCSharp.cs — монитор датчиков (акселерометр, гироскоп, компас) на C#

using System;
using System.Threading;
using System.Threading.Tasks;

class SensorMonitorCSharp
{
    private static class SensorData
    {
        public static double[] Accel = new double[3];
        public static double[] Gyro = new double[3];
        public static double[] Mag = new double[3];
        public static double[] Angles = new double[3];
    }

    private static readonly Random rand = new Random();
    private static bool running = true;

    static void Main(string[] args)
    {
        int freq = 10;
        if (args.Length > 0 && int.TryParse(args[0], out int f))
            freq = f;
        if (freq < 1) freq = 1;
        if (freq > 100) freq = 100;

        Console.WriteLine("📡 SensorMonitor Pro — C# Edition");
        Console.WriteLine($"Частота: {freq} Гц");
        Console.WriteLine("Нажмите Ctrl+C для выхода");

        CancellationTokenSource cts = new CancellationTokenSource();
        Console.CancelKeyPress += (s, e) => {
            e.Cancel = true;
            running = false;
            cts.Cancel();
            Console.WriteLine("\nВыход...");
        };

        var timer = new Timer(_ => {
            UpdateData();
            DisplayData();
        }, null, 0, 1000 / freq);

        Task.Delay(-1, cts.Token).Wait();
        timer.Dispose();
    }

    private static void UpdateData()
    {
        double t = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
        // Акселерометр
        SensorData.Accel[0] = 0.2 * Math.Sin(t * 0.5) + (rand.NextDouble() - 0.5) * 0.1;
        SensorData.Accel[1] = 0.3 * Math.Cos(t * 0.7) + (rand.NextDouble() - 0.5) * 0.1;
        SensorData.Accel[2] = 9.81 + 0.1 * Math.Sin(t * 0.3) + (rand.NextDouble() - 0.5) * 0.1;

        // Гироскоп
        SensorData.Gyro[0] = 0.02 * Math.Sin(t * 0.8) + (rand.NextDouble() - 0.5) * 0.02;
        SensorData.Gyro[1] = 0.03 * Math.Cos(t * 0.6) + (rand.NextDouble() - 0.5) * 0.02;
        SensorData.Gyro[2] = 0.01 * Math.Sin(t * 0.9) + (rand.NextDouble() - 0.5) * 0.02;

        // Магнитометр
        SensorData.Mag[0] = 15.0 + 2.0 * Math.Sin(t * 0.4) + (rand.NextDouble() - 0.5) * 1.0;
        SensorData.Mag[1] = -10.0 + 3.0 * Math.Cos(t * 0.5) + (rand.NextDouble() - 0.5) * 1.0;
        SensorData.Mag[2] = 40.0 + 4.0 * Math.Sin(t * 0.6) + (rand.NextDouble() - 0.5) * 1.0;

        // Углы
        SensorData.Angles[0] = 2.0 * Math.Sin(t * 0.2);
        SensorData.Angles[1] = 1.5 * Math.Cos(t * 0.25);
        SensorData.Angles[2] = 45.0 + 10.0 * Math.Sin(t * 0.1);
    }

    private static void DisplayData()
    {
        Console.Clear();
        Console.WriteLine("📡 SensorMonitor Pro — C# Edition");
        Console.WriteLine($"Акселерометр (м/с²):  X: {SensorData.Accel[0],6:F2}  Y: {SensorData.Accel[1],6:F2}  Z: {SensorData.Accel[2],6:F2}");
        Console.WriteLine($"Гироскоп (рад/с):     X: {SensorData.Gyro[0],6:F2}  Y: {SensorData.Gyro[1],6:F2}  Z: {SensorData.Gyro[2],6:F2}");
        Console.WriteLine($"Компас (мкТл):        X: {SensorData.Mag[0],6:F2}  Y: {SensorData.Mag[1],6:F2}  Z: {SensorData.Mag[2],6:F2}");
        Console.WriteLine($"Углы:  Roll: {SensorData.Angles[0],6:F1}°  Pitch: {SensorData.Angles[1],6:F1}°  Yaw: {SensorData.Angles[2],6:F1}°");
        Console.WriteLine("\nНажмите Ctrl+C для выхода");
    }
}
