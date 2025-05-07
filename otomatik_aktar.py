from dotenv import load_dotenv
load_dotenv()

import os
import json
import pymongo

def get_db():
    uri = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(uri)
    db = client["sosyalmedya"]
    return db

def jsondan_mongo_ya_aktar(json_dosyasi, koleksiyon_adi, benzersiz_alan="id"):
    db = get_db()
    if not os.path.exists(json_dosyasi):
        print(f"{json_dosyasi} bulunamadı!")
        return
    
    with open(json_dosyasi, encoding="utf-8") as f:
        data = json.load(f)

    def upsert_one(item):
        if benzersiz_alan not in item:
            print(f"Benzersiz alan ({benzersiz_alan}) yok: {item}")
            return
        result = db[koleksiyon_adi].update_one(
            {benzersiz_alan: item[benzersiz_alan]},  # Sorgu
            {"$set": item},                          # Yeni değerler
            upsert=True                              # Yoksa ekle
        )
        if result.matched_count:
            print(f"Güncellendi: {item[benzersiz_alan]}")
        else:
            print(f"Eklendi: {item[benzersiz_alan]}")

    if isinstance(data, list):
        for item in data:
            upsert_one(item)
    elif isinstance(data, dict):
        upsert_one(data)
    else:
        print(f"{json_dosyasi} beklenmeyen formatta.")

if __name__ == "__main__":
    temp_klasoru = "temp"
    for dosya_adi in os.listdir(temp_klasoru):
        if dosya_adi.endswith(".json"):
            dosya_yolu = os.path.join(temp_klasoru, dosya_adi)
            koleksiyon_adi = os.path.splitext(dosya_adi)[0]
<<<<<<< HEAD
            jsondan_mongo_ya_aktar(dosya_yolu, koleksiyon_adi, benzersiz_alan="id")
=======
            jsondan_mongo_ya_aktar(dosya_yolu, koleksiyon_adi, benzersiz_alan="id")
>>>>>>> 26fb9f788492c84f0589003b97952579f1cf9959
