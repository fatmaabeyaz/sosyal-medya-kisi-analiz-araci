# sosyal-medya-kisi-analiz-araci
Bu proje, sosyal medya paylaşımlarını analiz ederek bireylerin biyolojik ritmi, ruh hali, ilgi alanları ve sosyal etkileşimleri hakkında bilgi çıkarmayı hedefliyor. Ayrıca, sosyal medya verilerinin kötü niyetli kişilere nasıl kullanılabileceğine dair farkındalık yaratmayı amaçlar.  

## Veri Kazıma (Scraping)  

X (Twitter) API fiyatları ve yüksek dolar kuru nedeniyle veri kazıma yöntemini kullanmak zorunda kaldık. X'in anti-bot sistemlerine takılmamak için projemize **sleeper** (bekleme süreleri) ekledik, bu da işlem hızını bir miktar yavaşlattı.  

Veri kazıma yöntemi olarak, [Scrapfly](https://scrapfly.io/blog/how-to-scrape-twitter/)'ın blogunda öğrendiğimiz teknikleri uyguladık.  

## Veritabanı (MongoDB)
Projede toplanan tüm sosyal medya verileri, güvenli ve bulut tabanlı bir çözüm olan MongoDB Atlas veritabanında saklanmaktadır. MongoDB, esnek yapısı sayesinde farklı sosyal medya verilerini kolayca depolamamıza ve analiz etmemize imkân tanır.

Veritabanı bağlantısı ve işlemleri için db_connection.py dosyasını kullandık. Bağlantı bilgisi güvenlik amacıyla .env dosyasında saklanmalıdır:

bash
MONGODB_URI=mongodb+srv://kullaniciadi:sifre@cluster0.xxx.mongodb.net/veritabani_adi
Veri aktarımları, projemize entegre ettiğimiz otomatik iş akışı (workflow) yardımıyla MongoDB'ye anında yapılmaktadır.
