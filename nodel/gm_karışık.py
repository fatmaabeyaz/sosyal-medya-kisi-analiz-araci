from simpletransformers.classification import ClassificationModel
import pandas as pd
import matplotlib.pyplot as plt
import json
isim=""
def main():
    # Modeli yükle
    model = ClassificationModel(
        "bert",
        "nodel/bert_model",
        use_cuda=False,
        num_labels=2,
        args={"local_files_only": True}
    )

    # JSON dosyasını oku
    with open(f"temp/{isim}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # DataFrame oluştur
    df = pd.DataFrame(data)
    df = df[df["tweet"].str.strip() != ""]  # Boş tweetleri çıkar

    # Tahmin yap
    tweets = df["tweet"].tolist()
    predictions, _ = model.predict(tweets)
    df["olumluluk"] = ["eksi" if p == 0 else "artı" for p in predictions]

    # zamanı türünü ayarlar
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Grafiği çiz
    summary = df.groupby([df["datetime"].dt.date, "olumluluk"]).size().unstack(fill_value=0)
    summary.plot(kind="bar", stacked=True, figsize=(12, 6))
    plt.title(f"{isim} Tweet Duygu Dağılımı")#tablo başlığı
    plt.xlabel("Tarih")#x eksenindeki başlık
    plt.ylabel("Tweet Sayısı")#y eksenindeki başlık
    plt.legend(title="Duygu")#türler yazılmakta
    plt.tight_layout()#grafik boyutunu deyerlerin kösterildiği yere uygun boyut ayarlar
    plt.show()#gösterir

    # grafiği oluşturulmuş set yazdırılır
    print(df[["datetime", "tweet", "olumluluk"]])

if __name__ == "__main__":
    isim = input("Lütfen kullanıcı adını girin (örn: elonmusk): ")
    main()
