# Veritabanı İşlemleri

## Giriş
Bu belgedeki bilgiler, projedeki MongoDB veritabanıyla ilgili temel işlemleri açıklamaktadır.

## Kullanılan Teknolojiler
- **Veritabanı Yönetim Sistemi**: MongoDB
- **ORM**: Mongoose

## Veritabanı Yapısı
- **Kullanıcılar Koleksiyonu**: Kullanıcı bilgilerini saklar.
- **Saglikbakanligi Koleksiyonu**: Sağlık ile ilgili bilgileri saklar.

### Saglikbakanligi Koleksiyonu Yapısı
- **_id**: MongoDB'nin otomatik olarak oluşturduğu belge kimliği.
- **datetime**: Tweetin tarih ve saat bilgisi.
- **likes**: Tweetin aldığı beğeni sayısı.
- **replies**: Tweetin aldığı yanıt sayısı.
- **retweets**: Tweetin paylaşıldığı sayısı.
- **tweet**: Tweet içeriği.
- **url**: Tweetin bağlantısı.

## Temel İşlemler
### Kullanıcı Ekleme
```javascript  
db.kullanicilar.insertOne({  
  isim: "Fatma",  
  email: "fatma@example.com"  
});  
