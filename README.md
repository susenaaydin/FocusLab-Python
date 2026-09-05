# FocusLab-Python
# FocusLab

Python ve CustomTkinter kullanılarak geliştirilmiş, çalışma süresini takip etmeye ve günlük görevleri düzenlemeye yardımcı olan masaüstü odaklanma uygulaması.

## Özellikler

* Kronometre ile çalışma süresi takibi
* Zamanlayıcı ile belirli süreli çalışma
* 10, 25 ve 45 dakikalık hazır zamanlayıcı seçenekleri
* Özel süre belirleyebilme
* Günlük görev ekleme ve silme
* Görev kategorileri oluşturma
* Çalışma sürelerini kategorilere göre kaydetme
* Günlük çalışma geçmişini görüntüleme
* Günlük çalışma istatistiklerini görüntüleme
* Takvim üzerinden geçmiş çalışma sürelerini inceleme
* 9 farklı tema seçeneği
* Verilerin `JSON` dosyasında kalıcı olarak saklanması

## Kullanılan Teknolojiler

* Python
* CustomTkinter
* JSON
* Threading
* Tkinter
* PyInstaller

## Uygulama Bölümleri

### Kronometre

Çalışma süresini saniye bazında takip eder. Kronometre çalışırken toplam süre günlük çalışma geçmişine kaydedilir.

### Zamanlayıcı

Hazır süre seçenekleri:

* 10 dakika
* 25 dakika
* 45 dakika

Bunların yanında kullanıcı kendi çalışma süresini dakika cinsinden belirleyebilir.

### Günlük Planlayıcı

Kullanıcı kendi görevlerini ve görev kategorilerini oluşturabilir.

Görevler tamamlanma durumları ve çalışma süreleriyle birlikte saklanır.

### Takvim

Geçmiş günlerde gerçekleştirilen toplam çalışma sürelerini görüntüler.

### İstatistik

Bugünkü toplam çalışma süresini saat ve dakika olarak gösterir.

### Tema Seçimi

Uygulama içerisinde farklı renk temaları kullanılabilir:

* Pink
* Dark Pink
* Metal
* Purple
* Blue
* Midnight
* Lilac
* Mint
* Sunset Orange

## Veri Saklama

Uygulama içerisindeki görevler, kategoriler, tema seçimi ve çalışma geçmişi `data.json` dosyasında saklanır.

Örnek veri yapısı:

```json
{
    "theme": "Pink",
    "categories": [],
    "tasks": [],
    "history": {}
}
```

## Çalıştırma

Python ile çalıştırmak için gerekli kütüphaneyi yükleyin:

```bash
pip install customtkinter
```

Ardından:

```bash
python FocusLab.py
```

## Windows EXE Sürümü

FocusLab'ın Windows üzerinde Python kurulumu gerektirmeden çalıştırılabilen `.exe` sürümü de bulunmaktadır.

Hazır sürümü GitHub Releases bölümünden indirerek doğrudan çalıştırabilirsiniz.

## Proje Yapısı

```text
FocusLab/
│
├── FocusLab.py
├── data.json
├── README.md
└── ...
```

## Proje Amacı

FocusLab; çalışma süresini takip etmek, görevleri düzenlemek ve günlük çalışma verilerini saklamak amacıyla geliştirilmiş bir masaüstü uygulamasıdır.

Proje kapsamında Python ile masaüstü arayüz geliştirme, JSON tabanlı veri saklama, zaman yönetimi, çoklu iş parçacığı kullanımı ve uygulamanın `.exe` formatına dönüştürülmesi üzerine çalışılmıştır.

## Durum

Tamamlandı.

## Geliştirilebilecek Özellikler

* Grafik tabanlı istatistikler
* Görev düzenleme
* Bildirim sistemi
* Pomodoro modu
* Haftalık ve aylık raporlar
* Çalışma hedefleri
* Daha gelişmiş takvim görünümü

## Geliştirici

Sude Sena Aydın

```

**GitHub'da EXE'yi normal dosya olarak repo içine koymak yerine** mümkünse `Releases` bölümüne koymanı öneririm. README'deki “Windows EXE Sürümü” kısmı da kullanıcıyı oraya yönlendirir.

İstersen sonraki adımda sana **FocusLab için GitHub Description kısmına yazacağın tek cümleyi** de hazırlayabilirim.
```
