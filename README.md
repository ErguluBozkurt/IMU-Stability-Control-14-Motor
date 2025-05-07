# ESC Kontrol Sistemi (Raspberry Pi + BNO055 Sensörü)

Bu proje, **Raspberry Pi** ve **BNO055 IMU sensörü** kullanarak 14 motor ile hava aracını dengeli bir şekilde hareket etmek için **PID kontrolü** uygulayan, ESC kalibrasyonu ve silahlandırma (arming) işlemlerini içeren bir sistemdir. Proje, motorları dengede tutmayı, ESC'leri kalibre etmeyi ve silahlandırmayı amaçlayan dört ana Python dosyasından oluşmaktadır:

- **`controller.py`**
- **`calibrate.py`**
- **`arm.py`**
- **`BNO055.py`**

Bu proje, özellikle **robotik sistemler** ve **dengeleme uygulamaları** için uygundur.

## 🚀 Proje Yapısı

Proje şu dosyalardan oluşur:

- **`controller.py`**: PID kontrol algoritması ile motorların hızını ayarlar ve motorları dengede tutar.
- **`calibrate.py`**: ESC'lerin kalibrasyonunu yapar. ESC'ler doğru bir şekilde çalışabilmesi için önce kalibre edilmelidir.
- **`arm.py`**: Motorların ESC'lerini silahlandırmak (arm) için kullanılır. Bu işlem, motorların çalışmaya başlamadan önce yapılması gerekir.
- **`BNO055.py`**: BNO055 sensöründen sürekli olarak Euler açılarını (roll, pitch, yaw) alır ve güvenli bir şekilde günceller.

## 🛠️ Gereksinimler

Bu projeyi çalıştırabilmek için aşağıdaki donanım ve yazılım gereksinimlerine ihtiyacınız vardır:

### Donanım Gereksinimleri:
- **Raspberry Pi** (GPIO pinlerine erişimi olan bir model)
- **14 adet ESC (Elektronik Hız Kontrolcüsü)**
- **14 adet Motor**
- **BNO055 IMU Sensörü** (I2C ile bağlanacak)
- **Bağlantı kabloları ve güç kaynakları**

### Yazılım Gereksinimleri:
- **Python 3.x** yüklü olmalı

## 📦 Kurulum

1. **Python ve pip'in yüklü olduğundan emin olun**:
   - Raspberry Pi üzerinde terminal açarak aşağıdaki komutları çalıştırarak Python ve pip'i kontrol edin:

   ```bash
   python3 --version
   pip3 --version
   ```
   - Gerekli kütüphaneleri kurun.
    ```bash
   pip install -r requirements.txt
