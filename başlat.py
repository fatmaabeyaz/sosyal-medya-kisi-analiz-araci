from playwright.sync_api import sync_playwright #tarayıcı otomasyonu k.
from parsel import Selector #html içeriğini parse eden k.
import time
import json
import os
import sys
from openai import OpenAI
import json
#sys kütüphanesi sayesinde komut satırınadaki ek bilgileri alabiliriz.
#çalışan kodda 2. unsur varmı bakıyor
if len(sys.argv) != 2:
        #2. unsur yoksa hata mesajı veriyor
        print("Kullanım: python .\\başlat.py <kişi>")
        sys.exit(1)
#2. unsur var ise o kişi bilgilerini alıyor
#isim = sys.argv[1]
isim=sys.argv[1]
print("başlatılıyor")
# 2. unsurla veriçekme03_modül.py çalıştırılıyor 2. unsur eklenip
#
# ismi işler

def scrape_user_tweets(username: str, tweet_count: int ):
    tweets = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Kullanıcı profil sayfasına gider
        page.goto(f"https://twitter.com/" + username, timeout=60000)
        page.wait_for_selector("article[data-testid='tweet']")

        # Sayfayı kaydırarak daha fazla tweet yüklerr
        while len(tweets) < tweet_count:
            page.keyboard.press("PageDown")
            time.sleep(1)  # İçeriğin yüklenmesi için bekler
            html = page.content()
            selector = Selector(text=html)
            articles = selector.xpath("//article[@data-testid='tweet']")

            for article in articles: #Alınan veriyi filtreleme işlemi
                tweet = {
                    "text": "".join(article.xpath(".//*[@data-testid='tweetText']//text()").getall()),
                    "datetime": article.xpath(".//time/@datetime").get(),
                    "likes": article.xpath(".//*[@data-testid='like']//text()").get(),
                    "retweets": article.xpath(".//*[@data-testid='retweet']//text()").get(),
                    "replies": article.xpath(".//*[@data-testid='reply']//text()").get(),
                    "url": article.xpath(".//time/../@href").get()
                }
                if tweet not in tweets:
                    tweets.append(tweet)
                if len(tweets) >= tweet_count:
                    break

        browser.close()
    return tweets


username = isim  # Komut satırından kullanıcı adını alır
tweet_sayisi = int(input("Lütfen kaç tweet çekmek istediğinizi girin: "))
tweets = scrape_user_tweets(username , tweet_sayisi)
     # JSON verisini hazırlanır
json_data = []
    # birden fazla tweet varsa döngüye girer
for idx, tweet in enumerate(tweets, 1):# tweets her bir tiweti temsil eder
        idu=tweet['url'].split("/")[-1]  # URL'den tweet ID'sini alır
        json_data.append({#JSON yapısını oluşturur
            #yapı burdan ayarlanabilir
            "id": idu,
            "datetime": tweet['datetime'],
            "tweet": tweet['text'],
            "likes": tweet['likes'],
            "retweets": tweet['retweets'],
            "replies": tweet['replies'],
            "url": tweet['url']
        })
    #klasör oluştur
klasor_adi = "temp"# ara klasör ismi deyiştirilebilir
if not os.path.exists(klasor_adi):# dosya varmı bakar
        os.makedirs(klasor_adi)#yoksa oluşturur
yol = os.path.join(klasor_adi, f"{username}.json")# klasörün içine oluşturucak dosya yolunu oluşturur
    # Dosyaya yaz
try:
        with open(yol, "w", encoding="utf-8") as dosya:#dosyayı yazma ayrıntıları w üzerine yazar deyiştirilebilir
            json.dump(json_data, dosya, ensure_ascii=False, indent=4)#JSON verisini dosyaya yükler
        print(f"{len(json_data)} tweet başarıyla kaydedildi!")
except Exception:
        print("Hata: bir sorun oluştu!")
        

#
print("ilk adım çalıştırıldı çalıştırıldı")
print("nlp_modül.py çalıştırılıyor")

# 2. unsurla nlp_modül.py çalıştırılıyor 2. unsur eklenip
#

client = OpenAI(api_key="sk-7f12bd3e7f1343e9bb8c9a3279528017", base_url="https://api.deepseek.com")


def toku(met):
    try:
        with open(met, "r", encoding="utf-8") as f:
            veri = json.load(f)
        return [tweet["tweet"] for tweet in veri]
    except Exception as e:
        print(f"dosya okunurken hata oluştu.{e}")
        return None
#prompt ayarlayan fonksiyon
def prompt(metinler):
    return f"""
    Aşağıdaki tweet'leri analiz edip kişilik özelliklerini çıkar:
    
    {''.join([f'- {t}\\n' for t in metinler])}
    
    Çıktı formatı:
    - Ana Kişilik Özellikleri (3 kısa madde)
    - İletişim Tarzı (bir cümle)
    - Bu kişinin en hassas noktaları
    - Genel Değerlendirme (25 kelime)
    """# bu prompta talep edilen bilgiler eklenir.
#apiye yollarkenki ayarlar yapılır bu metodda
def analiz(metinler):
    try:
        response = client.chat.completions.create(
            # chat in türü
        model="deepseek-chat",
        messages=[
            {
                "role": "system", #ana yapı ne gibi davransın gibi
                "content": "Sen bir kişilik analiz uzmanısın. Twitter gönderilerine göre psikolojik profil çıkar."
            },
            {#prompt gönderilir
                "role": "user",
                "content": prompt(metinler)
            }
        ],
        # max_tokens=1000, #max token sayısı
        # temperature=0.7, #modelin ne kadar yaratıcı olacağı
        # gibi ayarlar yapılmakta
        stream=False
        )
        return response.choices[0].message.content# çıktı mesajı
    except Exception:# hata
        print("Analiz sırasında hata oluştu")
        return None



try:
        pa = os.path.dirname(os.path.abspath(__file__))# şuan bu kod dosyasının çalıştığı yolu alır
        os.chdir(f"{pa}/temp")# temp kulasörüne ulaşmak için yola /temp eklenir
except Exception:# hata mesajı
        print("dosya yok")
        sys.exit(1)
        
dosyasi = isim+".json"  # dosya adını işler
metinler = toku(dosyasi)#toku metoduna dosya adı gönderilir
if metinler:
        analiz_sonucu = analiz(metinler)
        print(analiz_sonucu)
else:
        print("Tweet bulunamadı.")




#
print("nlp_modül.py çalıştırıldı")