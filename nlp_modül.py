from openai import OpenAI
import json
import sys
import os
client = OpenAI(api_key="sk-7f12bd3e7f1343e9bb8c9a3279528017", base_url="https://api.deepseek.com")


def toku(met):
    try:
        with open(met, "r", encoding="utf-8") as f:
            veri = json.load(f)
        return [tweet["tweet"] for tweet in veri]
    except Exception as e:
        print(f"dosya okunurken hata oluştu.{e}")
        return None
def prompt(metinler):
    return f"""
    Aşağıdaki tweet'leri analiz edip kişilik özelliklerini çıkar:
    
    {''.join([f'- {t}\\n' for t in metinler])}
    
    Çıktı formatı:
        Çıktı formatı:
    - Ana Kişilik Özellikleri (3 madde)
    - İletişim Tarzı
    - Olası psikolojik açıkları
    - Dikkat Çeken Kelime Kalıpları
    - Genel Değerlendirme (100 kelime)
    """
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
    except Exception:
        print("Analiz sırasında hata oluştu")
        return None

if __name__ == "__main__":
    try:
        pa = os.path.dirname(os.path.abspath(__file__))
        os.chdir(f"{pa}/temp")
    except Exception:
        print("dosya yok")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Kullanım: python nlp.py <json_dosyasi>")
        sys.exit(1)
    
    
    dosyasi = sys.argv[1]  # Komut satırından dosya adını alır
    metinler = toku(dosyasi)
    if metinler:
        analiz_sonucu = analiz(metinler)
        print(analiz_sonucu)
    else:
        print("Tweet bulunamadı.")