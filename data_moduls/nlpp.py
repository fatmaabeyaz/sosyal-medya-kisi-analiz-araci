import os
from openai import OpenAI
import json

# API istemcisi oluşturur
def get_client():
    api_key = "xxxxxxxx"  # API anahtarını buraya yazın 
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# Tweet verilerini yükler
def toku(met):
    try:
        with open(met, "r", encoding="utf-8") as f:
            veri = json.load(f)
        return [tweet["tweet"] for tweet in veri]
    except Exception as e:
        print(f"dosya okunurken hata oluştu.{e}")
        return None

# Çıktı formatını nlp.py içinden dinamik olarak alır
def get_output_format():
    try:
        with open("nlp.py", "r", encoding="utf-8") as f:
            lines = f.readlines()

        start = end = None
        for i, line in enumerate(lines):
            if '"""' in line and "Çıktı formatı" in line:
                start = i
                break

        if start is not None:
            for j in range(start + 1, len(lines)):
                if '"""' in lines[j]:
                    end = j
                    break

        if start is not None and end is not None:
            return "".join(lines[start:end + 1])
        else:
            return '''"""
Çıktı formatı:
- Ana Kişilik Özellikleri (3 madde)
- İletişim Tarzı
- Olası psikolojik açıkları
- Dikkat Çeken Kelime Kalıpları
- Genel Değerlendirme (100 kelime)
"""'''
    except Exception as e:
        print(f"Çıktı formatı alınamadı: {e}")
        return '''"""
Çıktı formatı:
- Ana Kişilik Özellikleri (3 madde)
- İletişim Tarzı
- Olası psikolojik açıkları
- Dikkat Çeken Kelime Kalıpları
- Genel Değerlendirme (100 kelime)
"""'''

# Prompt oluşturur
def prompt(metinler):
    cikti_formati = get_output_format()
    return f"""
Aşağıdaki tweet'leri analiz edip kişilik özelliklerini çıkar:

{''.join([f'- {t}\n' for t in metinler])}

{cikti_formati}
"""

# Analizi API üzerinden yapar
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
        print("API Response (tam):", response)  # Tüm cevabı görmek için
        return response.choices[0].message.content
    except Exception as e:
        print(f"Analiz sırasında hata oluştu: {str(e)}")
        return None

# Uygulama başlangıcı
if __name__ == "__main__":
    metinler = toku("elonmusk.json")  # Tweet dosyası
    if metinler:
        analiz_sonucu = analiz(metinler)
        print("Analiz Sonucu:\n", analiz_sonucu)
    else:
        print("Tweet bulunamadı.")
