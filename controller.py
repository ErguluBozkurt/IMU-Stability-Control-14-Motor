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

# Sağdaki motorlar için PWM pinleri
motor_pwm_right = [14, 15, 18, 23, 24, 25, 8]  # Sağda 7 motor için pinler

# Soldaki motorlar için PWM pinleri
motor_pwm_left = [7, 9, 10, 11, 12, 13, 16]  # Solda 7 motor için pinler

# Motorlar için PWM nesneleri
pwm_motor_right = [GPIO.PWM(pin, 50) for pin in motor_pwm_right]
pwm_motor_left = [GPIO.PWM(pin, 50) for pin in motor_pwm_left]

# PWM motorları başlat
for pwm in pwm_motor_right + pwm_motor_left:
    pwm.start(5)  # Minimum sinyal (duty cycle = 5)

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
            for pwm in pwm_motor_right + pwm_motor_left:
                pwm.ChangeDutyCycle(5)  # Minimum sinyal
            time.sleep(0.01)
            continue

        # PID çıktısını hesapla (sadece roll için)
        roll_output = pid_roll.compute(target_roll, current_roll)

        # Temel hız ve PID çıktısını ekleyerek motor hızlarını hesapla
        motor_speed_right = [base_speed + roll_output for _ in motor_pwm_right]
        motor_speed_left = [base_speed - roll_output for _ in motor_pwm_left]

        # Motor hızlarını 5-10 aralığına sınırla
        motor_speed_right = [max(5, min(10, speed)) for speed in motor_speed_right]
        motor_speed_left = [max(5, min(10, speed)) for speed in motor_speed_left]

        # PWM sinyallerini güncelle
        for pwm, speed in zip(pwm_motor_right, motor_speed_right):
            pwm.ChangeDutyCycle(speed)
        for pwm, speed in zip(pwm_motor_left, motor_speed_left):
            pwm.ChangeDutyCycle(speed)

        time.sleep(0.01)  # 10 ms'de bir güncelle

except KeyboardInterrupt:
    # Program sonlandırıldığında motorları durdur
    for pwm in pwm_motor_right + pwm_motor_left:
        pwm.ChangeDutyCycle(5)  # Minimum sinyal
    time.sleep(1)
    for pwm in pwm_motor_right + pwm_motor_left:
        pwm.stop()
    GPIO.cleanup()
