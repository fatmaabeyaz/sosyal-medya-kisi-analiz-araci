from playwright.sync_api import sync_playwright #tarayıcı otomasyonu k.
from parsel import Selector #html içeriğini parse eden k.
import time
import json

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

if __name__ == "__main__":
    username = input("lütfen kullanıcı adını girin(@ veya x.com olmadan): ")  # Örnek kullanıcı adı
    tweet_sayisi = int(input("Lütfen kaç tweet çekmek istediğinizi girin: "))
    tweets = scrape_user_tweets(username , tweet_sayisi)
     # JSON verisini hazırla
    json_data = []
    for idx, tweet in enumerate(tweets, 1):
        json_data.append({
            "id": idx,
            "datetime": tweet['datetime'],
            "tweet": tweet['text'],
            "likes": tweet['likes'],
            "retweets": tweet['retweets'],
            "replies": tweet['replies'],
            "url": tweet['url']
        })
    
    # Dosyaya yaz
    try:
        with open(f"{username}.json", "w", encoding="utf-8") as dosya:
            json.dump(json_data, dosya, ensure_ascii=False, indent=4)
        print(f"{len(json_data)} tweet başarıyla kaydedildi!")
    except FileExistsError:
        print("Hata: Dosya zaten var!")
        print("Lütfen var olan dosyayı silin.")
