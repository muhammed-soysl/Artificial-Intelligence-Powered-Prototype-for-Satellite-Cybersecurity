import joblib
import pandas as pd
import random
import hashlib
import time
import threading
import warnings

# Uyarıları gizle
warnings.filterwarnings('ignore')

# --- Global Değişken ---
# Arka plan thread'i bu değişkeni her saniye güncelleyecek
ANLIK_GUVENLIK_KODU = ""
# -------------------------

# --- Adım 3'teki Dinamik Kod Üreteci Fonksiyonları ---
def cografi_konum_uret():
    """Rastgele coğrafi konum bilgisi (derece, dakika, saniye, yön) üretir."""
    enlem_derece = random.randint(0, 90)
    enlem_dakika = random.randint(0, 59)
    enlem_saniye = random.randint(0, 59)
    enlem_yon = random.choice(['K', 'G'])
    boylam_derece = random.randint(0, 180)
    boylam_dakika = random.randint(0, 59)
    boylam_saniye = random.randint(0, 59)
    boylam_yon = random.choice(['D', 'B'])

    # Koda dönüştürülecek string (Proje önerisindeki mantık)
    konum_string_kod = f"{enlem_derece}{enlem_yon}{enlem_dakika}{enlem_saniye}-{boylam_derece}{boylam_yon}{boylam_dakika}{boylam_saniye}"

    # Ekranda gösterilecek format
    konum_string_goster = f"Enlem: {enlem_derece}° {enlem_dakika}' {enlem_saniye}\" {enlem_yon} | Boylam: {boylam_derece}° {boylam_dakika}' {boylam_saniye}\" {boylam_yon}"

    return konum_string_kod, konum_string_goster

def kodu_sifrele(konum_string):
    """Konum string'ini SHA-256 ile karmaşık koda dönüştürür."""
    konum_bytes = konum_string.encode('utf-8')
    hash_objesi = hashlib.sha256(konum_bytes)
    karmasik_kod = hash_objesi.hexdigest()
    return karmasik_kod

def dinamik_kod_guncelleyici():
    """
    [ARKA PLAN GÖREVİ]
    Proje önerisindeki "Sonsuz Güvenlik Duvarı"nı simüle eder.
    Her saniye global güvenlik kodunu yeniler.
    """
    global ANLIK_GUVENLIK_KODU
    print("[Arka Plan]: Sonsuz Duvar kod üreteci çalıştı.")

    while True:
        anlik_konum_kod, anlik_konum_goster = cografi_konum_uret()
        ANLIK_GUVENLIK_KODU = kodu_sifrele(anlik_konum_kod)

        print(f"\n[Arka Plan DUYURU] - Zaman: {time.strftime('%H:%M:%S')}")
        print(f"  Yeni Konum: {anlik_konum_goster}")
        print(f"  YENİ GÜVENLİK KODU: {ANLIK_GUVENLIK_KODU[:20]}...")

        time.sleep(1) # Her saniye yenile [cite: 35]

# --- Adım 2'deki AI Modelini Yükleme ---
def modeli_yukle():
    """Eğitilmiş .joblib modelini yükler."""
    try:
        model = joblib.load('siber_guvenlik_modeli.joblib')
        print("[Sistem]: Yapay zeka modeli 'siber_guvenlik_modeli.joblib' başarıyla yüklendi.")
        return model
    except FileNotFoundError:
        print("[Hata]: 'siber_guvenlik_modeli.joblib' bulunamadı!")
        print("Lütfen önce 'adim_2_model_egitme.py' (ve Görev 3'teki kaydetme adımını) çalıştırın.")
        return None

# --- İş Paketi 3: Test ve Doğrulama Simülasyonu ---
def paketi_analiz_et(model, paket_verisi, gelen_kod):
    """
    [PROTOTİP ANA MANTIĞI]
    Gelen paketi önce 'Sonsuz Duvar' ile, sonra 'AI Model' ile kontrol eder.
    """
    print("\n--- Paket Analizi Başladı ---")
    global ANLIK_GUVENLIK_KODU

    # 1. KONTROL: Sonsuz Güvenlik Duvarı (Dinamik Kod Kontrolü)
    print(f"  Sistemin O Anki Kodu: {ANLIK_GUVENLIK_KODU[:20]}...")
    print(f"  Paketten Gelen Kod:   {gelen_kod[:20]}...")

    if gelen_kod != ANLIK_GUVENLIK_KODU:
        print("\n  SONUÇ: ERKEN TESPİT! ")
        print("  Paket 'Sonsuz Güvenlik Duvarı'nı geçemedi. Kod eşleşmiyor.")
        print("  DURUM: TEHDİT ENGELLENDİ (AI Taramasına Gerek Kalmadı).")
        print("--- Analiz Bitti ---")
        return

    # 2. KONTROL: Yapay Zeka Tabanlı Derin Tarama
    print("\n  Güvenlik Kodu DOĞRU. Paket 'Yapay Zeka Tabanlı' derin taramaya yönlendiriliyor... [cite: 19]")

    # Gelen paket verisini (dict) AI modelinin anlayacağı DataFrame'e çevir
    try:
        df = pd.DataFrame([paket_verisi])

        # Modeli kullanarak tahmin yap
        tahmin = model.predict(df)
        tahmin_olasilik = model.predict_proba(df)

        if tahmin[0] == 1: # 1 = Sızıntı
            print("\n  SONUÇ: YAPAY ZEKA TESPİTİ!")
            print(f"  Model bu paketi %{tahmin_olasilik[0][1]*100:.2f} ihtimalle 'Sızıntı' olarak sınıflandırdı.")
            print("  DURUM: TEHDİT ENGELLENDİ.")
        else: # 0 = Normal
            print("\n  SONUÇ: GÜVENLİ.")
            print(f"  Model bu paketi %{tahmin_olasilik[0][0]*100:.2f} ihtimalle 'Normal' olarak sınıflandırdı.")
            print("  DURUM: İZİN VERİLDİ.")

    except Exception as e:
        print(f"[Hata] AI Modeli analiz sırasında hata verdi: {e}")

    print("--- Analiz Bitti ---")


# --- ANA PROGRAM: Simülasyon Arayüzü ---
if __name__ == "__main__":
    # 1. AI Modelini yükle
    ai_model = modeli_yukle()
    if ai_model is None:
        exit()

    # 2. Arka planda "Sonsuz Duvar"ı (Dinamik Kod Üreteci) başlat
    # 'daemon=True' ana program kapanınca arka plan görevinin de kapanmasını sağlar
    kod_guncelleme_thread = threading.Thread(target=dinamik_kod_guncelleyici, daemon=True)
    kod_guncelleme_thread.start()

    print("\n[Sistem]: Arka planda 'Sonsuz Güvenlik Duvarı' kod üreteci başlatılıyor...")
    # Kod üretecinin ilk kodu üretmesi için kısa bir süre bekle
    time.sleep(1.5)

    print("\n" + "="*50)
    print(" UYDU SİBER GÜVENLİK PROTOTİP SİMÜLASYONU BAŞLADI ")
    print(" Arka planda her saniye güvenlik kodu değişiyor... ")
    print("="*50)

    # 3. Ana Simülasyon Menüsü (İş Paketi 3: Test Senaryoları)
    while True:
        print("\n--- Yeni Bir Paket Simülasyonu Oluştur ---")
        print(" (Arka plandaki kod değişimlerini izleyin)")

        secim = input(
            "Test Senaryosu Seçin:\n"
            "  1: [GÜVENLİ]   Doğru Kodlu NORMAL Paket\n"
            "  2: [TEHLİKELİ] Doğru Kodlu SIZINTI Paketi (AI Yakalamalı)\n"
            "  3: [SALDIRGAN] YANLIŞ Kodlu Paket (Duvar Yakalamalı)\n"
            "  q: Çıkış\n"
            "Seçiminiz: "
        )

        if secim == '1':
            # Bu veri, 'adim_1'deki 'Normal (0)' verilere benziyor
            paket = {'protokol': 'TCP', 'kaynak_port': 1025, 'hedef_port': 443, 'paket_boyutu': 128, 'anomali_skoru': 0.1}
            gelen_kod = ANLIK_GUVENLIK_KODU # Doğru kodu kullan
            paketi_analiz_et(ai_model, paket, gelen_kod)

        elif secim == '2':
            # Bu veri, 'adim_1'deki 'Sızıntı (1)' verilere benziyor
            paket = {'protokol': 'ICMP', 'kaynak_port': 45000, 'hedef_port': 666, 'paket_boyutu': 4000, 'anomali_skoru': 0.9}
            gelen_kod = ANLIK_GUVENLIK_KODU # Doğru kodu kullan (örn: şifreyi çalan içeriden biri)
            paketi_analiz_et(ai_model, paket, gelen_kod)

        elif secim == '3':
            # Bu veri önemli değil, çünkü koda takılacak
            paket = {'protokol': 'UDP', 'kaynak_port': 12345, 'hedef_port': 1337, 'paket_boyutu': 100, 'anomali_skoru': 0.7}
            gelen_kod = "SALDIRGANIN_TAHMINI_veya_ESKI_KOD_abc123" # Yanlış kod
            paketi_analiz_et(ai_model, paket, gelen_kod)

        elif secim.lower() == 'q':
            break

        else:
            print("Geçersiz seçim. Lütfen 1, 2, 3 veya 'q' girin.")

        time.sleep(1) # Menünün tekrar gelmesi için kısa bir bekleme

    print("\n[Sistem]: Prototip simülasyonu sonlandırıldı.")