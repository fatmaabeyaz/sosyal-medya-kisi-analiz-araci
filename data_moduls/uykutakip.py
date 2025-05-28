import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# 👤 Kullanıcı adını komut satırından al
if len(sys.argv) != 2:
    print("Kullanım: python uykutakip.py kisiadi")
    sys.exit(1)
    
kisi_adi = sys.argv[1]
dosya_yolu = f"temp/{kisi_adi}.json"  # JSON dosyası yolu

# 📁 Dosyanın varlığını kontrol et
if not os.path.exists(dosya_yolu):
    print(f"Hata: {dosya_yolu} dosyası bulunamadı!")
    sys.exit(1)

# 🧾 Veriyi dosyadan oku
try:
    tweets_df = pd.read_json(dosya_yolu)
except Exception as e:
    print(f"Hata: Dosya okunurken bir sorun oluştu: {str(e)}")
    sys.exit(1)

# 🧠 Uyku durumu tahmini ve saat analizi
def analyze_tweets(tweets_df):
    tweets_df["datetime"] = pd.to_datetime(tweets_df["datetime"])
    tweets_df["Hour"] = tweets_df["datetime"].dt.hour
    tweets_df["Sleep Status"] = tweets_df["Hour"].apply(lambda x: "Asleep" if x < 6 else "Awake")

    # Kullanıcı adını URL'den çıkar
    tweets_df["Username"] = tweets_df["url"].apply(lambda url: url.split("/")[1] if "/" in url else "Bilinmiyor")

    sleep_df = tweets_df[["id", "Username", "tweet", "datetime", "Sleep Status", "Hour"]]
    sleep_df.columns = ['Tweet ID', 'Username', 'Tweet Text', 'Tweet Time', 'Sleep Status', 'Hour']

    hourly_counts = sleep_df['Hour'].value_counts().sort_index()
    least_active_hours = hourly_counts[hourly_counts == hourly_counts.min()].index.tolist()
    least_active_users = sleep_df[sleep_df['Hour'].isin(least_active_hours)]

    return sleep_df, hourly_counts, least_active_hours, least_active_users

# 🔍 Analiz
analysis_results, hourly_counts, least_active_hours, least_active_users = analyze_tweets(tweets_df)

# 🖨 Sonuçları yazdır
print("\nUyku Durumu Analizi Sonuçları:")
print(analysis_results)

print("\nEn Az Tweet Atılan Saatler:")
print(least_active_hours)

print("\nBu Saatlerde Tweet Atan Kullanıcılar ve Sayıları:")
for hour in least_active_hours:
    users = least_active_users[least_active_users['Hour'] == hour]
    print(f"Saat {hour}: {users['Username'].unique()} (Toplam Tweet: {len(users)})")

# 📊 Görselleştirme
plt.figure(figsize=(10, 6))
hourly_counts.plot(kind='bar', color='skyblue')
plt.title('Tweet Sayılarına Göre Saat Analizi')
plt.xlabel('Saat')
plt.ylabel('Tweet Sayısı')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.axhline(y=hourly_counts.min(), color='r', linestyle='--', label='En Az Tweet Atılan Saat')
plt.legend()
plt.tight_layout()
plt.show()