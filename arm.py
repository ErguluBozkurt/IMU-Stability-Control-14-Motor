import time
import RPi.GPIO as GPIO

# GPIO Ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)  # Motor 1 PWM sinyali
GPIO.setup(15, GPIO.OUT)  # Motor 2 PWM sinyali

# PWM Ayarları
pwm_motor1 = GPIO.PWM(14, 50)  # 50 Hz PWM frekansı
pwm_motor2 = GPIO.PWM(15, 50)

pwm_motor1.start(0)
pwm_motor2.start(0)

def arm_esc(pwm_motor, motor_name):
    print(f"{motor_name} silahlanma işlemi başlatılıyor...")
    
    # Minimum sinyal gönder (duty cycle = 5)
    print(f"{motor_name} için minimum sinyal gönderiliyor (duty cycle = 5)...")
    pwm_motor.ChangeDutyCycle(5)
    time.sleep(5)  # ESC'nin arm için bekleyin

    print(f"{motor_name} silahlanma işlemi tamamlandı.")

try:
    # Motor 1'i silahlandır
    arm_esc(pwm_motor1, "Motor 1")
    
    # Motor 2'yi silahlandır
    arm_esc(pwm_motor2, "Motor 2")

except KeyboardInterrupt:
    print("Silahlanma işlemi durduruldu.")

finally:
    # PWM ve GPIO temizleme
    pwm_motor1.stop()
    pwm_motor2.stop()
    GPIO.cleanup()
