import random
import hashlib
import time

def cografi_konum_uret():
    """
    Proje önerisindeki gibi rastgele coğrafi konum bilgisi üretir.
    (Derece, Dakika, Saniye, Yön)
    """
    # Enlem (Latitude) üret
    enlem_derece = random.randint(0, 90)
    enlem_dakika = random.randint(0, 59)
    enlem_saniye = random.randint(0, 59)
    enlem_yon = random.choice(['K', 'G']) # Kuzey / Güney

    # Boylam (Longitude) üret
    boylam_derece = random.randint(0, 180)
    boylam_dakika = random.randint(0, 59)
    boylam_saniye = random.randint(0, 59)
    boylam_yon = random.choice(['D', 'B']) # Doğu / Batı

    # Koda dönüştürülecek string (boşluksuz, ham veri)
    # Proje önerisi "bu konum bilgilerini kodlara dönüştürmesidir"
    konum_string_kod = f"{enlem_derece}{enlem_yon}{enlem_dakika}{enlem_saniye}-{boylam_derece}{boylam_yon}{boylam_dakika}{boylam_saniye}"

    # Ekranda gösterilecek format (kullanıcının isteği)
    konum_string_goster = f"Enlem: {enlem_derece}° {enlem_dakika}' {enlem_saniye}\" {enlem_yon} | Boylam: {boylam_derece}° {boylam_dakika}' {boylam_saniye}\" {boylam_yon}"

    # (1) Kodlama için ham veri, (2) Ekranda göstermek için formatlı veri
    return konum_string_kod, konum_string_goster

def kodu_sifrele(konum_string):
    """
    Proje önerisindeki gibi verileri şifreler/karmaşık koda dönüştürür.
    Burada prototip için hızlı olan SHA-256 hash kullanılır.
    """
    # String'i byte'a çevir
    konum_bytes = konum_string.encode('utf-8')

    # SHA-256 hash'ini oluştur
    hash_objesi = hashlib.sha256(konum_bytes)

    # Karmaşık kodu (hex formatında) al
    karmasikk_kod = hash_objesi.hexdigest()
    return karmasikk_kod

def sonsuz_guvenlik_duvari_baslat():
    """
    Proje önerisindeki gibi her saniye yeni kod üreten
    "Sonsuz Güvenlik Duvarı" döngüsü.
    """
    print("--- Sonsuz Güvenlik Duvarı Prototipi Başlatıldı ---")
    print("Her saniye rastgele coğrafi konuma dayalı yeni bir GÜVENLİK KODU üretiliyor...")
    print("Durdurmak için (Ctrl+C) tuşlarına basın.\n")

    global anlik_guvenlik_kodu
    anlik_guvenlik_kodu = ""

    try:
        while True:
            # 1. Coğrafi Konum Belirle
            # (kodlanacak_veri, gosterilecek_veri)
            anlik_konum_kod, anlik_konum_goster = cografi_konum_uret()

            # 2. Şifreleme ve Kod Üretimi
            anlik_guvenlik_kodu = kodu_sifrele(anlik_konum_kod)

            # 3. Dinamik Güvenlik Duvarı Oluşumu
            # Bu kodun "her saniye yenilendiğini" simüle et
            print(f"Zaman: {time.strftime('%H:%M:%S')}")
            print(f"  Konum Bilgisi: {anlik_konum_goster}")
            print(f"  Üretilen Kod:   {anlik_guvenlik_kodu[:20]}...")
            print("-" * 30) # Ayıraç

            # 1 saniye bekle
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n--- Güvenlik Duvarı Döngüsü Durduruldu ---")

if __name__ == "__main__":
    sonsuz_guvenlik_duvari_baslat()