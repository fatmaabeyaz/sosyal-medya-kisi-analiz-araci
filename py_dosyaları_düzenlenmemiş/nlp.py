from openai import OpenAI
import json
# api key gibi ince ayarlar yapılır
client = OpenAI(api_key="sk-7f12bd3e7f1343e9bb8c9a3279528017", base_url="https://api.deepseek.com")


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
        Çıktı formatı:
    - Ana Kişilik Özellikleri (3 madde)
    - İletişim Tarzı
    - Olası psikolojik açıkları
    - Dikkat Çeken Kelime Kalıpları
    - Genel Değerlendirme (100 kelime)
    """# bu prompta talep edilen bilgiler eklenir.
#apiye yollarkenki ayarlar yapılır bu metodda
def analiz(metinler):
    try:
        response = client.chat.completions.create(
            # chat in türü
        model="deepseek-chat",
        messages=[
            {
                "role": "system", #ana yapı ne gibi davransın gibi
                "content": "Sen bir kişilik analiz uzmanısın. Twitter gönderilerine göre psikolojik profil çıkar."
            },
            {#prompt gönderilir
                "role": "user",
                "content": prompt(metinler)
            }
        ],
        # max_tokens=1000, #max token sayısı
        # temperature=0.7, #modelin ne kadar yaratıcı olacağı
        # gibi ayarlar yapılmakta
        stream=False
        )
        return response.choices[0].message.content# çıktı mesajı
    except Exception:# hata
        print("Analiz sırasında hata oluştu")
        return None

if __name__ == "__main__":
    metinler = toku("elonmusk.json")# dosya adı
    # dosya adı değiştirilebilir
    if metinler:
        analiz_sonucu = analiz(metinler)
        print(analiz_sonucu)
    else:
        print("Tweet bulunamadı.")