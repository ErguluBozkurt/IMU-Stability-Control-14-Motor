import board
import busio
import adafruit_bno055
import threading

# I2C arayüzünü başlat
i2c = busio.I2C(board.SCL, board.SDA)

# BNO055 sensörünü belirtilen I2C adresiyle başlat (0x28 veya 0x29 olabilir)
sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x28)

print("BNO055 Sensörü Başlatıldı...")

# Sensör verilerini tutacak global değişkenler
yaw = 0.0
pitch = 0.0
roll = 0.0

# Thread güvenliği için lock
data_lock = threading.Lock()

# Sensör verilerini sürekli güncelleyen fonksiyon
def update_sensor_data():
    global yaw, pitch, roll
    while True:
        try:
            # Euler açılarını oku
            euler_angles = sensor.euler
            if euler_angles is not None:
                with data_lock:
                    yaw, pitch, roll = euler_angles
        except Exception as e:
            print(f"Sensör verisi okunurken hata oluştu: {e}")

# Sensör verilerini güncelleme thread'i başlat
sensor_thread = threading.Thread(target=update_sensor_data)
sensor_thread.daemon = True
sensor_thread.start()