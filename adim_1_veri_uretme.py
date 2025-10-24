import pandas as pd
import numpy as np
import random

# İş Paketi 1 Hedefi: En az 3000 veri [cite: 68]
VERI_SAYISI = 3000
SIZINTI_ORANI = 0.15 # Veri setimizin %15'i sızıntı olsun

data = []

# Popüler portlar (normal trafik için)
normal_ports = [80, 443, 22, 53]
# Şüpheli portlar (sızıntı için)
supheli_ports = [1337, 8080, 666, 9001]

for _ in range(VERI_SAYISI):
    is_sizinti = np.random.rand() < SIZINTI_ORANI

    if not is_sizinti:
        # --- Normal Trafik Verisi Üret ---
        protokol = random.choice(['TCP', 'UDP'])
        kaynak_port = random.randint(1024, 65535)
        hedef_port = random.choice(normal_ports)
        # Normal paketler genellikle belirli bir boyut aralığındadır
        paket_boyutu = random.randint(64, 1500)
        # Normal trafiğin anomali skoru düşük olur
        anomali_skoru = max(0, np.random.normal(0.1, 0.05))
        etiket = 0
    else:
        # --- Sızıntı Trafik Verisi Üret ---
        protokol = random.choice(['TCP', 'ICMP'])
        kaynak_port = random.randint(40000, 65535)
        hedef_port = random.choice(supheli_ports)
        # Sızıntı (data exfiltration) genellikle büyük veya çok küçük (kontrol) paketler kullanır
        paket_boyutu = random.choice([random.randint(20, 40), random.randint(4000, 8000)])
        # Sızıntı trafiğinin anomali skoru yüksek olur
        anomali_skoru = min(1, np.random.normal(0.8, 0.1))
        etiket = 1

    data.append({
        'protokol': protokol,
        'kaynak_port': kaynak_port,
        'hedef_port': hedef_port,
        'paket_boyutu': paket_boyutu,
        'anomali_skoru': anomali_skoru,
        'etiket': etiket
    })

# DataFrame oluştur ve CSV olarak kaydet
df = pd.DataFrame(data)
df.to_csv('uydu_veri_seti.csv', index=False)

print(f"{VERI_SAYISI} adet yapay veri seti 'uydu_veri_seti.csv' dosyasına kaydedildi.")
print("Veri setindeki etiket dağılımı:")
print(df['etiket'].value_counts())