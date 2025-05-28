import os
from openai import OpenAI
import json

def get_client():
    dosya_adi = "api_key.txt"
    if not os.path.exists(dosya_adi):
        raise Exception("API anahtarı bulunamadı. Lütfen önce API anahtarını girin.")
    
    with open(dosya_adi, 'r') as file:
        api_key = file.read().strip()
        if not api_key:
            raise Exception("API anahtarı boş. Lütfen geçerli bir API anahtarı girin.")
    
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

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
    newline = '\n'
    return f"""
    Aşağıdaki tweet'leri analiz edip kişilik özelliklerini çıkar:
    
    {''.join([f'- {t}{newline}' for t in metinler])}
    
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
        client = get_client()
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