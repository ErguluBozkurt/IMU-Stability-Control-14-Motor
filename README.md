# ESC Kontrol Sistemi (Raspberry Pi + BNO055)

Bu proje, Raspberry Pi ve BNO055 sensörü kullanarak 14 motoru dengelemek için PID kontrolü uygulayan, ESC kalibrasyonu ve silahlandırma (arming) işlemlerini içeren bir sistemdir. Proje dört ana Python dosyasından oluşmaktadır:

- `controller.py`: PID kontrolü ile motorları dengede tutar.
- `calibrate.py`: ESC'leri kalibre etmek için kullanılır.
- `arm.py`: ESC'leri silahlandırmak (arm) için kullanılır.
- `BNO055.py`: BNO055 IMU sensöründen sürekli veri toplar (roll, pitch, yaw).

## 🛠️ Gereksinimler

- Raspberry Pi (GPIO pinlerine erişim)
- 14 adet ESC ve motor
- BNO055 IMU sensörü (I2C bağlantılı)
- Python 3

## 📦 Kurulum

1. Gerekli Python kütüphanelerini yükleyin:

```bash
pip install -r requirements.txt
