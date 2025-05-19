# Sosyal-medya-kisi-analiz-araci
Bu proje, sosyal medya paylaşımlarını analiz ederek bireylerin biyolojik ritmi, ruh hali, ilgi alanları ve sosyal etkileşimleri hakkında bilgi çıkarmayı hedefliyor. Ayrıca, sosyal medya verilerinin kötü niyetli kişilere nasıl kullanılabileceğine dair farkındalık yaratmayı amaçlar.  

## 🏗️ Mimari Karar: Mikroservis Mimarisi

Projemizde mikroservis mimarisini tercih ettik çünkü:
```
📌 Birden fazla bağımsız modülün uyum içinde çalışması gereken bir sistem tasarlıyoruz
📌 Her bir bileşenin kendi yaşam döngüsüne ve teknoloji stack'ine sahip olması gerekiyor
📌 Sistemin farklı parçalarının bağımsız olarak ölçeklenebilir olması kritik önem taşıyor
```

## 🧩 Modüller ve Mimari Uyum

Projemizdeki modüller ve mikroservis mimarisine uygunlukları:

### 1. **Veri Çekme Servisi**
X (Twitter) API fiyatları ve yüksek dolar kuru nedeniyle veri kazıma yöntemini kullanmak zorunda kaldık. X'in anti-bot sistemlerine takılmamak için projemize **sleeper** (bekleme süreleri) ekledik, bu da işlem hızını bir miktar yavaşlattı.  

Veri kazıma yöntemi olarak, [Scrapfly](https://scrapfly.io/blog/how-to-scrape-twitter/)'ın blogunda öğrendiğimiz teknikleri uyguladık.  

### 2. **Veri İşleme Servisi**
enes burayı doldur

### 3. **LLM API Bağlantı Servisi**
enes burayı da doldur

### 4. **Kullanıcı Arayüzü Servisi**
henüz tamamlanmadı

### 5. **Veritabanı Bağlantı Servisi**

Projede toplanan tüm sosyal medya verileri, güvenli ve bulut tabanlı bir çözüm olan MongoDB Atlas veritabanında saklanmaktadır. MongoDB, esnek yapısı sayesinde farklı sosyal medya verilerini kolayca depolamamıza ve analiz etmemize imkân tanır.

Veritabanı bağlantısı ve işlemleri için db_connection.py dosyasını kullandık. Bağlantı bilgisi güvenlik amacıyla .env dosyasında saklanmalıdır:

bash
MONGODB_URI=mongodb+srv://kullaniciadi:sifre@cluster0.xxx.mongodb.net/veritabani_adi
Veri aktarımları, projemize entegre ettiğimiz otomatik iş akışı (workflow) yardımıyla MongoDB'ye anında yapılmaktadır.


## ✅ Avantajlar

Mikroservis mimarisinin projemize sağladığı avantajlar:

| Avantaj | Projemize Katkısı |
|---------|------------------|
| **Modülerlik** | Her bir işlevsellik bağımsız geliştirilebilir |
| **Ölçeklenebilirlik** | Yük altındaki modüller bağımsız ölçeklenebilir |
| **Teknoloji Esnekliği** | Her modül için uygun teknoloji seçilebilir |
| **Güncelleme ve geliştirme desteği** | Modüller bağımsız olarak güncellenebilir |
| **Hata İzolasyonu** | Bir modüldeki hata tüm sistemi çökertmez |
