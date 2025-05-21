import os
import json
import pymongo
from dotenv import load_dotenv

# Ortam değişkenlerini yükle (.env için)
load_dotenv()

def get_db():
    uri = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(uri)
    db = client["sosyalmedya"]
    return db

def jsondan_mongo_ya_aktar(json_dosyasi, koleksiyon_adi):
    db = get_db()
    if not os.path.exists(json_dosyasi):
        print(f"{json_dosyasi} bulunamadı!")
        return

    with open(json_dosyasi, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        if data:
            db[koleksiyon_adi].insert_many(data)
            print(f"{json_dosyasi} → '{koleksiyon_adi}' koleksiyonuna {len(data)} adet veri eklendi.")
        else:
            print(f"{json_dosyasi} içinde veri yok.")
    elif isinstance(data, dict):
        db[koleksiyon_adi].insert_one(data)
        print(f"{json_dosyasi} → '{koleksiyon_adi}' koleksiyonuna 1 adet veri eklendi.")
    else:
        print(f"{json_dosyasi} beklenmeyen formatta.")

if __name__ == "__main__":
    temp_klasoru = "./temp"

    if not os.path.exists(temp_klasoru):
        print(f"{temp_klasoru} klasörü bulunamadı.")
        exit()

    for dosya_adi in os.listdir(temp_klasoru):
        if dosya_adi.endswith(".json"):
            json_yolu = os.path.join(temp_klasoru, dosya_adi)
            koleksiyon_adi = os.path.splitext(dosya_adi)[0]  # dosyaadı.json → dosyaadı
            jsondan_mongo_ya_aktar(json_yolu, koleksiyon_adi)
