import os
import sys
if len(sys.argv) != 2:
        print("Kullanım: python .\\başlat.py <kişi>")
        sys.exit(1)

isim = sys.argv[1]
print("başlatılıyor")
os.system(f"python veriÇekme03_modül.py {isim}")
print("veriÇekme03_modül.py çalıştırıldı")
print("nlp_modül.py çalıştırılıyor")
os.system(f"python nlp_modül.py {isim}.json")
print("nlp_modül.py çalıştırıldı")