import os
import sys
import json            
import pymongo         

print("Çalışılan dizin:", os.getcwd())
print("Dizin içeriği:", os.listdir())

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
            print(f"{json_dosyasi} koleksiyonuna {len(data)} adet veri eklendi.")
        else:
            print(f"{json_dosyasi} içinde veri yok.")
    elif isinstance(data, dict):
        db[koleksiyon_adi].insert_one(data)
        print(f"{json_dosyasi} koleksiyonuna 1 adet veri eklendi.")
    else:
        print(f"{json_dosyasi} beklenmeyen formatta.")

if __name__ == "__main__":
    aktarilacaklar = [
        ("elonmusk.json", "elonmusk"),
        ("saglikbakanligi.json", "saglikbakanligi")
    ]

    for json_dosyasi, koleksiyon_adi in aktarilacaklar:
        jsondan_mongo_ya_aktar(json_dosyasi, koleksiyon_adi)
