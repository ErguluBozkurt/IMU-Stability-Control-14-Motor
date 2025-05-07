import time
import RPi.GPIO as GPIO
import BNO055

# PID Kontrolörü
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, setpoint, measured_value):
        error = setpoint - measured_value
        self.integral += error
        derivative = error - self.prev_error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output

# GPIO ve Servo Ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)  # Servo 1 PWM sinyali
GPIO.setup(15, GPIO.OUT)  # Servo 2 PWM sinyali

# 50 Hz PWM frekansı ile servoları başlat
pwm_servo1 = GPIO.PWM(14, 50)
pwm_servo2 = GPIO.PWM(15, 50)

pwm_servo1.start(0)
pwm_servo2.start(0)

# PID parametreleri (sadece pitch için). Deneme yanılma ile değiştirilecek.
pid_pitch = PIDController(kp=1.5, ki=0.03, kd=0.08)

# Hedef pitch açısı (dengede kalmak için 0 derece)
target_pitch = 0.0

# Servo açılarını sınırla (örneğin, 0-180 derece arası)
def constrain_angle(angle):
    return max(0, min(180, angle))

try:
    while True:
        # Sensör verilerini güvenli bir şekilde oku
        with BNO055.data_lock:
            current_pitch = BNO055.pitch

        # PID çıktısını hesapla (sadece pitch için)
        pitch_output = pid_pitch.compute(target_pitch, current_pitch)

        # Servo açılarını hesapla
        servo1_angle = 90 + pitch_output  # 90: merkez konumu
        servo2_angle = 90 - pitch_output

        # Servo açılarını sınırla
        servo1_angle = constrain_angle(servo1_angle)
        servo2_angle = constrain_angle(servo2_angle)

        # Servo açılarını PWM duty cycle'a dönüştür (0-100 arası)
        # Servo PWM duty cycle genellikle 2.5% (0 derece) ile 12.5% (180 derece) arasındadır.
        # Bu nedenle, açıyı duty cycle'a dönüştürmek için:
        duty_cycle_servo1 = 2.5 + (servo1_angle / 180.0) * 10.0
        duty_cycle_servo2 = 2.5 + (servo2_angle / 180.0) * 10.0

        # PWM sinyallerini güncelle
        pwm_servo1.ChangeDutyCycle(duty_cycle_servo1)
        pwm_servo2.ChangeDutyCycle(duty_cycle_servo2)

        time.sleep(0.01)  # 10 ms'de bir güncelle

except KeyboardInterrupt:
    # Program sonlandırıldığında servoları durdur
    pwm_servo1.stop()
    pwm_servo2.stop()
    GPIO.cleanup()