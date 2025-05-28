from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

# MongoDB bağlantı dizesi
password = "xxxxx"  # Buraya şifrenizi yazın
client = MongoClient(f"mongodb+srv://{kullanciadi:şifre}@sosyalmedya.bvcdmdf.mongodb.net/sosyalmedya?retryWrites=true&w=majority")

# Başarılı Bağlantı Kontrolü
try:
    client.admin.command('ping')
    print("MongoDB bağlantısı başarılı!")
except Exception as e:
    print("Bağlantı hatası:", e)

# Sosyalmedya veritabanını tanımlayın
db = client['sosyalmedya']

# Mevcut koleksiyonları listeleme ve veri çekme
def fetch_tweets():
    collections = db.list_collection_names()
    tweets = []

    for collection_name in collections:
        tweet_collection = db[collection_name]
        tweets.extend(list(tweet_collection.find()))

    return tweets

# Uyku durumu tahmini ve saat analizi
def analyze_tweets(tweets):
    sleep_data = []
    tweet_times = []

    for tweet in tweets:
        tweet_time = tweet['datetime']
        tweet_time = pd.to_datetime(tweet_time)
        tweet_times.append(tweet_time)

        sleep_status = "Asleep" if tweet_time.hour < 6 else "Awake"
        url = tweet['url']
        username = url.split('/')[1] if '/' in url else 'Bilinmiyor'
        tweet_text = tweet['tweet']

        sleep_data.append({
            'Tweet ID': tweet['id'],
            'Username': username,
            'Tweet Text': tweet_text,
            'Tweet Time': tweet_time,
            'Sleep Status': sleep_status,
            'Hour': tweet_time.hour
        })

    sleep_df = pd.DataFrame(sleep_data)
    
    # Saat bazında tweet sayıları
    hourly_counts = sleep_df['Hour'].value_counts().sort_index()
    
    # En az tweet atılan saatler
    least_active_hours = hourly_counts[hourly_counts == hourly_counts.min()].index.tolist()

    # Kullanıcı adlarını filtreleme
    least_active_users = sleep_df[sleep_df['Hour'].isin(least_active_hours)]

    return sleep_df, hourly_counts, least_active_hours, least_active_users

# Tweetleri çek ve analiz et
tweets = fetch_tweets()
analysis_results, hourly_counts, least_active_hours, least_active_users = analyze_tweets(tweets)

# Sonuçları yazdırma
print("\nUyku Durumu Analizi Sonuçları:")
print(analysis_results)

print("\nEn Az Tweet Atılan Saatler:")
print(least_active_hours)

print("\nBu Saatlerde Tweet Atan Kullanıcılar ve Sayıları:")
for hour in least_active_hours:
    users = least_active_users[least_active_users['Hour'] == hour]
    print(f"Saat {hour}: {users['Username'].unique()} (Toplam Tweet: {len(users)})")

# Tweet sayılarını görselleştirme
plt.figure(figsize=(10, 6))
hourly_counts.plot(kind='bar', color='skyblue')
plt.title('Tweet Sayılarına Göre Saat Analizi')
plt.xlabel('Saat')
plt.ylabel('Tweet Sayısı')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.axhline(y=hourly_counts.min(), color='r', linestyle='--', label='En Az Tweet Atılan Saat')
plt.legend()
plt.show()

