import os
from openai import OpenAI
import json

#Burası api_key.txt dosyasının varlığını kontrol ediyor
dosya_adi = "api_key.txt"
# Dosya mevcut mu kontrol et
if not os.path.exists(dosya_adi):
    # Kullanıcıdan API anahtarı al
    api_key = input("Lütfen DeepSeek API anahtarınızı girin: ")
    with open(dosya_adi, "w") as f:# Dosyaya yaz
        f.write(api_key)

# api_key.txt dosyasından API anahtarını oku
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

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
    - Ana Kişilik Özellikleri (3 madde)
    - İletişim Tarzı
    - Olası psikolojik açıkları
    - Dikkat Çeken Kelime Kalıpları
    - Genel Değerlendirme (100 kelime)
    """

#apiye yollarkenki ayarlar yapılır bu metodda
def analiz(metinler):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "Sen bir kişilik analiz uzmanısın. Twitter gönderilerine göre psikolojik profil çıkar."
                },
                {
                    "role": "user",
                    "content": prompt(metinler)
                }
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Analiz sırasında hata oluştu: {str(e)}")
        return None

if __name__ == "__main__":
    metinler = toku("elonmusk.json")  # dosya adı
    # dosya adı değiştirilebilir
    if metinler:
        analiz_sonucu = analiz(metinler)
        print(analiz_sonucu)
    else:
        print("Tweet bulunamadı.")