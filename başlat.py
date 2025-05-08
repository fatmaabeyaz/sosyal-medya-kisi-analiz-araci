import os
import sys
#sys kütüphanesi sayesinde komut satırınadaki ek bilgileri alabiliriz.
#çalışan kodda 2. unsur varmı bakıyor
if len(sys.argv) != 2:
        #2. unsur yoksa hata mesajı veriyor
        print("Kullanım: python .\\başlat.py <kişi>")
        sys.exit(1)
#2. unsur var ise o kişi bilgilerini alıyor
isim = sys.argv[1]
print("başlatılıyor")
# 2. unsurla veriçekme03_modül.py çalıştırılıyor 2. unsur eklenip
os.system(f"python veriÇekme03_modül.py {isim}")
print("veriÇekme03_modül.py çalıştırıldı")
print("nlp_modül.py çalıştırılıyor")
# 2. unsurla nlp_modül.py çalıştırılıyor 2. unsur eklenip
os.system(f"python nlp_modül.py {isim}.json")
print("nlp_modül.py çalıştırıldı")