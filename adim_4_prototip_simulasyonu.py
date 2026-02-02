import joblib
import pandas as pd
import random
import hashlib
import time
import threading
import warnings
import time

# Gereksiz kütüphane uyarılarını gizleyelim
warnings.filterwarnings('ignore')

# --- Global Değişken ---
# Arka plan thread'i bu değişkeni her saniye güncelleyecek
ANLIK_GUVENLIK_KODU = ""


def cografi_konum_uret():
    """Rastgele coğrafi konum bilgisi üretir."""
    enlem = f"{random.randint(0, 90)}K{random.randint(0, 59)}{random.randint(0, 59)}"
    boylam = f"{random.randint(0, 180)}D{random.randint(0, 59)}{random.randint(0, 59)}"
    konum_string_kod = f"{enlem}-{boylam}"
    konum_string_goster = f"Enlem: {enlem} | Boylam: {boylam}"
    return konum_string_kod, konum_string_goster


def kodu_sifrele(konum_string):
    """Konum bilgisini SHA-256 ile hash'ler."""
    return hashlib.sha256(konum_string.encode('utf-8')).hexdigest()


def dinamik_kod_guncelleyici():
    """Arka planda her saniye yeni güvenlik kodu üretir."""
    global ANLIK_GUVENLIK_KODU
    while True:
        konum_kod, _ = cografi_konum_uret()
        ANLIK_GUVENLIK_KODU = kodu_sifrele(konum_kod)
        time.sleep(1)


def modeli_yukle():
    """Eğitilmiş yapay zeka modelini yükler."""
    try:
        model = joblib.load('siber_guvenlik_modeli.joblib')
        print("[Sistem]: AI Modeli başarıyla yüklendi.")
        return model
    except FileNotFoundError:
        print("[Hata]: 'siber_guvenlik_modeli.joblib' bulunamadı! Lütfen önce Adım 2'yi çalıştırın.")
        return None


def paketi_analiz_et(model, paket_verisi, gelen_kod):
    # --- ÖLÇÜM BAŞLAT ---
    start_time = time.perf_counter()

    global ANLIK_GUVENLIK_KODU
    print("\n--- Analiz Başladı ---")

    if gelen_kod != ANLIK_GUVENLIK_KODU:
        print("RESULT: 🛑 DUVAR ENGELİ!")
        return

    df = pd.DataFrame([paket_verisi])
    tahmin = model.predict(df)

    # --- ÖLÇÜM BİTİR ---
    end_time = time.perf_counter()
    gecikme_ms = (end_time - start_time) * 1000

    if tahmin[0] == 1:
        print(f"RESULT: ⚠️ AI TESPİTİ! (Süre: {gecikme_ms:.2f} ms)")
    else:
        print(f"RESULT: ✅ GÜVENLİ. (Süre: {gecikme_ms:.2f} ms)")


if __name__ == "__main__":
    ai_model = modeli_yukle()
    if ai_model is None: exit()

    # Arka plan görevini başlat
    threading.Thread(target=dinamik_kod_guncelleyici, daemon=True).start()
    print("[Sistem]: Sonsuz Güvenlik Duvarı aktif. İlk kodun üretilmesi bekleniyor...")
    time.sleep(1.5)

    while True:
        print(f"\n[Sistem Zamanı: {time.strftime('%H:%M:%S')}]")
        secim = input(
            "Test Senaryosu Seçin:\n"
            "  1: [GÜVENLİ]   Doğru Kod + Normal Paket\n"
            "  2: [SIZINTI]   Doğru Kod + Şüpheli Paket (AI Yakalamalı)\n"
            "  3: [SALDIRGAN] Yanlış Kodlu Paket (Duvar Yakalamalı)\n"
            "  q: Çıkış\n"
            "Seçiminiz: "
        )

        if secim == '1':
            # Yeni veri setine uygun: Düşük anomali skoru, normal port
            paket = {'protokol': 'TCP', 'kaynak_port': 1025, 'hedef_port': 443, 'paket_boyutu': 950,
                     'anomali_skoru': 0.28}
            paketi_analiz_et(ai_model, paket, ANLIK_GUVENLIK_KODU)
        elif secim == '2':
            # Yeni veri setine uygun: Sınırda anomali skoru, büyük paket
            paket = {'protokol': 'TCP', 'kaynak_port': 45000, 'hedef_port': 8080, 'paket_boyutu': 3800,
                     'anomali_skoru': 0.62}
            paketi_analiz_et(ai_model, paket, ANLIK_GUVENLIK_KODU)
        elif secim == '3':
            paket = {'protokol': 'UDP', 'kaynak_port': 1234, 'hedef_port': 53, 'paket_boyutu': 100,
                     'anomali_skoru': 0.50}
            paketi_analiz_et(ai_model, paket, "HATALI_GECERSIZ_HASH_123")
        elif secim.lower() == 'q':
            break
        time.sleep(1)