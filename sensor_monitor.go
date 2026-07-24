// sensor_monitor.go — монитор датчиков (акселерометр, гироскоп, компас) на Go

package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
	"os/signal"
	"syscall"
	"time"
)

type SensorData struct {
	Accel  [3]float64
	Gyro   [3]float64
	Mag    [3]float64
	Angles [3]float64
}

var data SensorData
var running bool = true

func updateData() {
	t := float64(time.Now().UnixNano()) / 1e9
	// Акселерометр
	data.Accel[0] = 0.2*math.Sin(t*0.5) + (rand.Float64()-0.5)*0.1
	data.Accel[1] = 0.3*math.Cos(t*0.7) + (rand.Float64()-0.5)*0.1
	data.Accel[2] = 9.81 + 0.1*math.Sin(t*0.3) + (rand.Float64()-0.5)*0.1

	// Гироскоп
	data.Gyro[0] = 0.02*math.Sin(t*0.8) + (rand.Float64()-0.5)*0.02
	data.Gyro[1] = 0.03*math.Cos(t*0.6) + (rand.Float64()-0.5)*0.02
	data.Gyro[2] = 0.01*math.Sin(t*0.9) + (rand.Float64()-0.5)*0.02

	// Магнитометр
	data.Mag[0] = 15.0 + 2.0*math.Sin(t*0.4) + (rand.Float64()-0.5)*1.0
	data.Mag[1] = -10.0 + 3.0*math.Cos(t*0.5) + (rand.Float64()-0.5)*1.0
	data.Mag[2] = 40.0 + 4.0*math.Sin(t*0.6) + (rand.Float64()-0.5)*1.0

	// Углы
	data.Angles[0] = 2.0 * math.Sin(t*0.2)
	data.Angles[1] = 1.5 * math.Cos(t*0.25)
	data.Angles[2] = 45.0 + 10.0*math.Sin(t*0.1)
}

func displayData() {
	fmt.Print("\033[H\033[2J")
	fmt.Println("📡 SensorMonitor Pro — Go Edition")
	fmt.Printf("Акселерометр (м/с²):  X: %6.2f  Y: %6.2f  Z: %6.2f\n", data.Accel[0], data.Accel[1], data.Accel[2])
	fmt.Printf("Гироскоп (рад/с):     X: %6.2f  Y: %6.2f  Z: %6.2f\n", data.Gyro[0], data.Gyro[1], data.Gyro[2])
	fmt.Printf("Компас (мкТл):        X: %6.2f  Y: %6.2f  Z: %6.2f\n", data.Mag[0], data.Mag[1], data.Mag[2])
	fmt.Printf("Углы:  Roll: %6.1f°  Pitch: %6.1f°  Yaw: %6.1f°\n", data.Angles[0], data.Angles[1], data.Angles[2])
	fmt.Println("\nНажмите Ctrl+C для выхода")
}

func main() {
	rand.Seed(time.Now().UnixNano())
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	ticker := time.NewTicker(100 * time.Millisecond) // 10 Гц
	defer ticker.Stop()

	go func() {
		for {
			select {
			case <-ticker.C:
				updateData()
				displayData()
			}
		}
	}()

	<-sigChan
	running = false
	fmt.Println("\nВыход...")
}
