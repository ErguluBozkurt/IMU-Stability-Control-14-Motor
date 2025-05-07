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

# GPIO ve PWM Ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)  # Motor 1 PWM sinyali
GPIO.setup(15, GPIO.OUT)  # Motor 2 PWM sinyali

pwm_motor1 = GPIO.PWM(14, 50)  # 50 Hz PWM frekansı
pwm_motor2 = GPIO.PWM(15, 50)

pwm_motor1.start(5)  # Minimum sinyal (duty cycle = 5)
pwm_motor2.start(5)  # Minimum sinyal (duty cycle = 5)

# PID parametreleri (sadece roll için). Deneme yanılma ile değiştirilecek.
pid_roll = PIDController(kp=1.3, ki=0.001, kd=0.01)

# Hedef roll açısı (dengede kalmak için 0 derece)
target_roll = 0.0

# Tolerans değeri (örneğin, -0.1 ile +0.1 arasındaki değerlerde motorlar çalışmayacak)
tolerance = 0.5

# Temel hız (duty cycle = 5.5) - Daha düşük temel hız
base_speed = 6.0
time.sleep(5)
def map_value(value, in_min, in_max, out_min, out_max):
    """
    Bir değeri bir aralıktan başka bir aralığa dönüştürür.
    Örneğin, -50 ile +50 arasındaki değeri 5-10 arasına dönüştürür.
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

try:
    while True:
        # Sensör verilerini güvenli bir şekilde oku
        with BNO055.data_lock:
            current_roll = BNO055.roll

        # Eğer açı tolerans aralığında ise motorları durdur
        if -tolerance <= current_roll <= tolerance:
            pwm_motor1.ChangeDutyCycle(5)  # Minimum sinyal
            pwm_motor2.ChangeDutyCycle(5)
            time.sleep(0.01)
            continue

        # PID çıktısını hesapla (sadece roll için)
        roll_output = pid_roll.compute(target_roll, current_roll)

        # Temel hız ve PID çıktısını ekleyerek motor hızlarını hesapla
        motor1_speed = base_speed - roll_output
        motor2_speed = base_speed + roll_output

        # Motor hızlarını 5-10 aralığına sınırla
        motor1_speed = max(5, min(10, motor1_speed))
        motor2_speed = max(5, min(10, motor2_speed))

        # PWM sinyallerini güncelle
        pwm_motor1.ChangeDutyCycle(motor1_speed)
        pwm_motor2.ChangeDutyCycle(motor2_speed)

        time.sleep(0.01)  # 10 ms'de bir güncelle

except KeyboardInterrupt:
    # Program sonlandırıldığında motorları durdur
    pwm_motor1.ChangeDutyCycle(5)  # Minimum sinyal
    pwm_motor2.ChangeDutyCycle(5)
    time.sleep(1)
    pwm_motor1.stop()
    pwm_motor2.stop()
    GPIO.cleanup()
    