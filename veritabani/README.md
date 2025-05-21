# 🧠 Sosyal Medya Uyku Takip ve Veri Analiz Sistemi

Bu proje, sosyal medya üzerinden toplanan verilerle kullanıcıların olası uyku/uyanıklık zamanlarını tahmin etmek ve MongoDB üzerinde veri analizi yapmak üzere geliştirilmiştir.

---

## 🔧 Kullanılan Teknolojiler

- **Veritabanı**: MongoDB Atlas
- **Veri İşleme**: Python, pandas, matplotlib
- **Veri Aktarımı**: pymongo
- **Ortam Değişkeni Yönetimi**: python-dotenv

---

## 🗃️ Veritabanı Yapısı

### Koleksiyonlar

- `kullanicilar`  
- `saglikbakanligi`  


---

### `saglikbakanligi` Koleksiyonu Yapısı

| Alan        | Açıklama                           |
|-------------|------------------------------------|
| `_id`       | MongoDB tarafından otomatik atanır |
| `datetime`  | Tweet zaman bilgisi (ISO format)   |
| `likes`     | Beğeni sayısı                      |
| `replies`   | Yanıt sayısı                       |
| `retweets`  | Retweet sayısı                     |
| `tweet`     | Tweet metni                        |
| `url`       | Tweet bağlantısı                   |

---

## 📥 Veri Aktarımı 

 `temp/` klasörüne `.json` dosyası eklendikten sonra aşağıdaki komut  çalıştırılmalıdır:

```bash
python veritabani/otomatik_aktar.py
