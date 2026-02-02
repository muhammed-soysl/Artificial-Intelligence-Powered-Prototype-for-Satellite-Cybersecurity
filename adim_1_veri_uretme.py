import pandas as pd
import numpy as np
import random

# --- KONFİGÜRASYON ---
# İş Paketi 1: Veri seti büyüklüğü ve sızıntı oranı
VERI_SAYISI = 3000
SIZINTI_ORANI = 0.20  # Veri setinin %20'si sızıntı/tehdit senaryosu

data = []

# Port Gruplarız
normal_ports = [80, 443, 22, 53]
supheli_ports = [1337, 8080, 666, 9001]

print(f"--- Veri Üretim Süreci Başladı ({VERI_SAYISI} kayıt) ---")

for _ in range(VERI_SAYISI):
    # Rastgele seçimle paketin tipine karar ver
    is_sizinti = np.random.rand() < SIZINTI_ORANI

    if not is_sizinti:
        # --- NORMAL TRAFİK SENARYOSU ---
        protokol = random.choice(['TCP', 'UDP'])

        # Hedef Port: %90 normal portlar, %10 rastgele (gürültü için)
        if np.random.rand() < 0.9:
            hedef_port = random.choice(normal_ports)
        else:
            hedef_port = random.randint(1, 65535)

        # Paket Boyutu: Standart veri akış aralığı
        paket_boyutu = random.randint(100, 2500)

        # Anomali Skoru: Ortalama 0.25, Standart Sapma 0.15
        # (Sızıntı trafiği ile çakışma yaratarak modelin zorlanmasını sağlar)
        anomali_skoru = np.clip(np.random.normal(0.25, 0.15), 0, 1)
        etiket = 0

    else:
        # --- SIZINTI (ATTACK) TRAFİK SENARYOSU ---
        protokol = random.choice(['TCP', 'ICMP', 'UDP'])

        # Hedef Port: %40 normal portlarda saklanmaya çalış (Stealth Attack)
        # %60 bilinen şüpheli portları kullan
        if np.random.rand() < 0.4:
            hedef_port = random.choice(normal_ports)
        else:
            hedef_port = random.choice(supheli_ports)

        # Paket Boyutu: Çok küçük (kontrol) veya çok büyük (veri sızdırma) paketler
        paket_boyutu = random.randint(40, 4500)

        # Anomali Skoru: Ortalama 0.55, Standart Sapma 0.20
        # (0.4 - 0.6 arası değerler normal trafikle karışacaktır)
        anomali_skoru = np.clip(np.random.normal(0.55, 0.20), 0, 1)
        etiket = 1

    # Ortak Özellik: Kaynak Port
    kaynak_port = random.randint(1024, 65535)

    data.append({
        'protokol': protokol,
        'kaynak_port': kaynak_port,
        'hedef_port': hedef_port,
        'paket_boyutu': paket_boyutu,
        'anomali_skoru': anomali_skoru,
        'etiket': etiket
    })

# --- VERİ KAYIT VE ÖZET ---
# DataFrame oluştur
df = pd.DataFrame(data)

# CSV olarak kaydet
df.to_csv('uydu_veri_seti.csv', index=False)

print("\n[TAMAMLANDI]: 'uydu_veri_seti.csv' başarıyla oluşturuldu.")
print("-" * 30)
print("Veri Seti Özeti:")
print(f"Toplam Kayıt: {len(df)}")
print(f"Normal Paket (0): {df['etiket'].value_counts()[0]}")
print(f"Sızıntı Paketi (1): {df['etiket'].value_counts()[1]}")
print("-" * 30)
print("Önemli: Veri seti artık daha karmaşık (çakışan değerler var).")
print("Şimdi 'adim_2_model_egitme.py' dosyasını çalıştırarak modeli güncelleyebilirsiniz.")