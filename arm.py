import time
import RPi.GPIO as GPIO

# GPIO Ayarları
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
    pwm.start(0)  # Başlangıçta 0 duty cycle

def arm_esc(pwm_motor, motor_name):
    print(f"{motor_name} silahlanma işlemi başlatılıyor...")
    
    # Minimum sinyal gönder (duty cycle = 5)
    print(f"{motor_name} için minimum sinyal gönderiliyor (duty cycle = 5)...")
    pwm_motor.ChangeDutyCycle(5)
    time.sleep(5)  # ESC'nin arm için bekleyin

    print(f"{motor_name} silahlanma işlemi tamamlandı.")

try:
    # Sağdaki motorları silahlandır
    for i, pwm_motor in enumerate(pwm_motor_right):
        arm_esc(pwm_motor, f"Sağ Motor {i+1}")

    # Soldaki motorları silahlandır
    for i, pwm_motor in enumerate(pwm_motor_left):
        arm_esc(pwm_motor, f"Sol Motor {i+1}")

except KeyboardInterrupt:
    print("Silahlanma işlemi durduruldu.")

finally:
    # PWM ve GPIO temizleme
    for pwm in pwm_motor_right + pwm_motor_left:
        pwm.stop()
    GPIO.cleanup()
