from playwright.sync_api import sync_playwright #tarayıcı otomasyonu k.
from parsel import Selector #html içeriğini parse eden k.
import time
import json
import os

def scrape_user_tweets(username: str, tweet_count: int):
    tweets = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # Kaydedilmiş cookie'leri yükle
        cookie_path = os.path.join(os.path.dirname(__file__), "xCookie.json")
        print(f"Cookie'ler şuradan yükleniyor: {cookie_path}")
        
        if os.path.exists(cookie_path):
            try:
                with open(cookie_path, 'r') as f:
                    storage_state = json.load(f)
                context = browser.new_context(storage_state=storage_state)
                print("Cookie'ler başarıyla yüklendi.")
            except Exception as e:
                print(f"Cookie'ler yüklenirken hata oluştu: {str(e)}")
        else:
            print(f"Cookie dosyası bulunamadı: {cookie_path}")

        try:
            page = context.new_page()
            
            # Kullanıcı profil sayfasına git
            page.goto(f"https://twitter.com/" + username, timeout=60000)
            page.wait_for_selector("article[data-testid='tweet']")

            # Sayfayı kaydırarak daha fazla tweet yükler
            while len(tweets) < tweet_count:
                page.keyboard.press("PageDown")
                time.sleep(1)  # İçeriğin yüklenmesi için bekler
                html = page.content()
                selector = Selector(text=html)
                articles = selector.xpath("//article[@data-testid='tweet']")

                for article in articles:
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

        except Exception as e:
            print(f"Veri çekme sırasında hata oluştu: {str(e)}")
            return None
        finally:
            context.close()
            browser.close()

    return tweets

if __name__ == "__main__":
    username = input("lütfen kullanıcı adını girin(@ veya x.com olmadan): ")
    tweet_sayisi = int(input("Lütfen kaç tweet çekmek istediğinizi girin: "))
    tweets = scrape_user_tweets(username, tweet_sayisi)
    
    if tweets:
        # JSON verisini hazırla
        json_data = []
        for idx, tweet in enumerate(tweets, 1):
            idu = tweet['url'].split("/")[-1]
            json_data.append({
                "id": idu,
                "datetime": tweet['datetime'],
                "tweet": tweet['text'],
                "likes": tweet['likes'],
                "retweets": tweet['retweets'],
                "replies": tweet['replies'],
                "url": tweet['url']
            })
        
        # Klasör oluştur
        klasor_adi = "temp"
        if not os.path.exists(klasor_adi):
            os.makedirs(klasor_adi)
        
        yol = os.path.join(klasor_adi, f"{username}.json")
        
        # Dosyaya yaz
        try:
            with open(yol, "w", encoding="utf-8") as dosya:
                json.dump(json_data, dosya, ensure_ascii=False, indent=4)
            print(f"{len(json_data)} tweet başarıyla kaydedildi!")
        except Exception as e:
            print(f"Hata: {str(e)}")
    else:
        print("Tweet'ler çekilemedi!")
