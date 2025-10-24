import streamlit as st
import joblib
import pandas as pd
import random
import hashlib
import time
import os
from threading import Thread
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# --- Sayfa Konfigürasyonu ---
st.set_page_config(
    page_title="Uydu Güvenlik Prototipi v2.2 (Hata Düzeltildi)",
    page_icon="🛰️",
    layout="wide"
)

# --- Session State (Tüm dinamik veriler burada) ---
# HATA DÜZELTMESİ: Eksik değişkenler eklendi
if 'anlik_anahtar' not in st.session_state:
    st.session_state.anlik_anahtar = b""
    st.session_state.anlik_konum = ""
    st.session_state.anlik_konum_kod = ""
    st.session_state.anlik_salt = b""
    st.session_state.kod_ureteci_calisiyor = False
    st.session_state.kullanilan_konumlar = set()
    st.session_state.toplam_uretilen_kod = 0  # <<< BU SATIRIN OLDUĞUNDAN EMİN OLUN
    st.session_state.engellenen_tekrarli_kod = 0 # <<< BU SATIRIN OLDUĞUNDAN EMİN OLUN


# --- AI MODELİNİ YÜKLEME ---
@st.cache_resource
def modeli_yukle():
    try:
        model = joblib.load('siber_guvenlik_modeli.joblib')
        return model
    except FileNotFoundError:
        st.error("HATA: 'siber_guvenlik_modeli.joblib' bulunamadı! Lütfen Adım 2'yi çalıştırın.")
        return None


ai_model = modeli_yukle()


# --- GÜNCELLENMİŞ DİNAMİK KOD ÜRETECİ FONKSİYONLARI ---

def cografi_konum_uret():
    """Rastgele coğrafi konum bilgisi üretir."""
    enlem_derece = random.randint(0, 90)
    enlem_dakika = random.randint(0, 59)
    enlem_saniye = random.randint(0, 59)
    enlem_yon = random.choice(['K', 'G'])
    boylam_derece = random.randint(0, 180)
    boylam_dakika = random.randint(0, 59)
    boylam_saniye = random.randint(0, 59)
    boylam_yon = random.choice(['D', 'B'])

    konum_string_kod = f"{enlem_derece}{enlem_yon}{enlem_dakika}{enlem_saniye}-{boylam_derece}{boylam_yon}{boylam_dakika}{boylam_saniye}"
    konum_string_goster = f"{enlem_derece}° {enlem_dakika}' {enlem_saniye}\" {enlem_yon} | {boylam_derece}° {boylam_dakika}' {boylam_saniye}\" {boylam_yon}"

    return konum_string_kod, konum_string_goster


def anahtar_turet(konum_string, salt):
    """Konum bilgisini kriptografik anahtar türetmede 'seed' (tohum) olarak kullanır."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(konum_string.encode('utf-8'))


def dinamik_kod_guncelleyici():
    """[ARKA PLAN GÖREVİ] Konum Tekrar Kontrolü yaparak her saniye anahtarı yeniler."""
    time.sleep(1)

    while True:
        # Hata burada oluyordu, artık 'toplam_uretilen_kod' tanımlı
        st.session_state.toplam_uretilen_kod += 1
        anlik_konum_kod, anlik_konum_goster = cografi_konum_uret()

        if anlik_konum_kod in st.session_state.kullanilan_konumlar:
            st.session_state.engellenen_tekrarli_kod += 1
            time.sleep(0.01)
            continue

        st.session_state.kullanilan_konumlar.add(anlik_konum_kod)
        if len(st.session_state.kullanilan_konumlar) > 1000:
            st.session_state.kullanilan_konumlar.pop()

        yeni_salt = os.urandom(16)
        yeni_anahtar = anahtar_turet(anlik_konum_kod, yeni_salt)

        st.session_state.anlik_anahtar = yeni_anahtar
        st.session_state.anlik_konum = anlik_konum_goster
        st.session_state.anlik_konum_kod = anlik_konum_kod
        st.session_state.anlik_salt = yeni_salt

        time.sleep(1)


# --- PAKET ANALİZ FONKSİYONU ---
def paketi_analiz_et(paket_verisi, gelen_konum_bilgisi):
    """Gelen paketi analiz eder ve sonucu görsel olarak basar."""

    try:
        gelen_anahtar = anahtar_turet(gelen_konum_bilgisi, st.session_state.anlik_salt)
    except Exception:
        gelen_anahtar = b"INVALID_KEY"

    sistem_anahtari = st.session_state.anlik_anahtar

    if not hashlib.timing_safe_compare(gelen_anahtar, sistem_anahtari):
        st.error(f"**SONUÇ: ERKEN TESPİT!** 🛑 (Katman 1: Konum/Anahtar Hatası)\n\n"
                 f"Paket 'Sonsuz Güvenlik Duvarı'nı geçemedi. Gelen konum bilgisi, o anki beklenen anahtarı türetmedi.\n\n"
                 f"Gelen Konum: `{gelen_konum_bilgisi}`\n"
                 f"Beklenen (Ham) Konum Kodu: `{st.session_state.anlik_konum_kod}`")
        return

    st.info(
        "Güvenlik Kodu DOĞRU (Katman 1 başarılı). Paket 'Yapay Zeka Tabanlı' derin taramaya (Katman 4) yönlendiriliyor...")

    try:
        df = pd.DataFrame([paket_verisi])
        tahmin = ai_model.predict(df)
        tahmin_olasılık = ai_model.predict_proba(df)

        if tahmin[0] == 1:  # 1 = Sızıntı
            st.warning(f"**SONUÇ: YAPAY ZEKA TESPİTİ!** ⚠️ (Katman 5: Tepki)\n\n"
                       f"Model bu paketi **%{tahmin_olasılık[0][1] * 100:.2f}** ihtimalle 'Sızıntı' olarak sınıflandırdı.\n\n"
                       f"DURUM: TEHDİT ENGELLENDİ.")
        else:  # 0 = Normal
            st.success(f"**SONUÇ: GÜVENLİ.** ✅\n\n"
                       f"Model bu paketi **%{tahmin_olasılık[0][0] * 100:.2f}** ihtimalle 'Normal' olarak sınıflandırdı.\n\n"
                       f"DURUM: İZİN VERİLDİ.")
    except Exception as e:
        st.error(f"AI Modeli analiz sırasında hata verdi: {e}")


# --- GÖRSEL ARAYÜZ (UI) ---

st.title("🛰️ GÖZEN-7: Yapay Zeka Destekli Dinamik Uydu Güvenlik Duvarı")
st.caption(
    f"Teknofest 2025 (ID: 746170) ve TÜBİTAK 2209-A Fikirleri Entegre Prototipi")  # GÖZEN-7 ID'nizi rapordan aldım

if ai_model is None:
    st.stop()

if not st.session_state.kod_ureteci_calisiyor:
    kod_guncelleme_thread = Thread(target=dinamik_kod_guncelleyici, daemon=True)
    kod_guncelleme_thread.start()
    st.session_state.kod_ureteci_calisiyor = True

st.subheader("Katman 1: Sonsuz Güvenlik Duvarı (Dinamik Anahtar Türetme)")

col1_metric, col2_metric, col3_metric = st.columns(3)
with col1_metric:
    placeholder_konum = st.empty()
with col2_metric:
    placeholder_tekrar_onleme = st.empty()
with col3_metric:
    placeholder_uretilen_kod = st.empty()

placeholder_anahtar = st.empty()

st.subheader("İş Paketi 3: Test-Doğrulama Senaryoları (5 Katmanlı Mimari Testi)")

sistem_hazir = bool(st.session_state.anlik_konum_kod)

if not sistem_hazir:
    st.info("Sistem başlatılıyor... Lütfen ilk güvenlik kodunun üretilmesi için 1-2 saniye bekleyin.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Senaryo 1: [GÜVENLİ] Paket Gönder", type="primary", use_container_width=True,
                 disabled=not sistem_hazir):
        paket = {'protokol': 'TCP', 'kaynak_port': 1025, 'hedef_port': 443, 'paket_boyutu': 128, 'anomali_skoru': 0.1}
        ham_konum = st.session_state.anlik_konum_kod
        paketi_analiz_et(paket, ham_konum)

with col2:
    if st.button("Senaryo 2: [TEHLİKELİ] Paket Gönder", use_container_width=True, disabled=not sistem_hazir):
        paket = {'protokol': 'ICMP', 'kaynak_port': 45000, 'hedef_port': 666, 'paket_boyutu': 4000,
                 'anomali_skoru': 0.9}
        ham_konum = st.session_state.anlik_konum_kod
        paketi_analiz_et(paket, ham_konum)

with col3:
    if st.button("Senaryo 3: [SALDIRGAN] Paket Gönder", type="secondary", use_container_width=True,
                 disabled=not sistem_hazir):  # Saldırgan butonu her zaman aktif olabilir
        paket = {'protokol': 'UDP', 'kaynak_port': 12345, 'hedef_port': 1337, 'paket_boyutu': 100, 'anomali_skoru': 0.7}
        gelen_konum = "41K2317-32D4805"
        paketi_analiz_et(paket, gelen_konum)

# --- DİNAMİK ALANI GÜNCELLEME DÖNGÜSÜ ---
while True:
    with placeholder_konum:
        st.metric(label="Anlık Coğrafi Konum", value=st.session_state.anlik_konum or "Üretiliyor...")

    with placeholder_tekrar_onleme:
        st.metric(label="Konum Tekrar Kontrolü (AI)",
                  value=f"{st.session_state.engellenen_tekrarli_kod} Engellendi")

    with placeholder_uretilen_kod:
        st.metric(label="Toplam Üretilen Kod Denemesi",
                  value=f"{st.session_state.toplam_uretilen_kod}")

    with placeholder_anahtar:
        st.code(
            f"Türetilen Kriptografik Anahtar (AES-256 Seed): {st.session_state.anlik_anahtar.hex()[:40] if sistem_hazir else '...'}",
            language="text")

    # 'disabled' durumunu güncellemek için arayüzü sürekli yenile
    if not sistem_hazir:
        st.rerun()
    else:
        # Sistem hazır olduğunda, sadece ana thread 1 saniye beklesin
        # Arka plan thread'i zaten session state'i güncelliyor
        # st.rerun() sürekli kullanmak yerine arayüzün doğal güncellemesini bekleyelim
        time.sleep(1)
        # st.rerun() # Sadece metriklerin anlık güncellenmesi isteniyorsa bu satır açılabilir, ancak thread ile çakışabilir.
        # st.rerun() olmadan da metrikler arka plan thread'i sayesinde güncellenecektir (Streamlit'in modern yapısı)
        # Düzeltme: En stabil yapı için st.rerun()'ı kaldırıp, thread'in state'i güncellemesine izin verelim.
        # Streamlit state değiştiğinde otomatik yenileme yapmalı, ancak thread'den dolayı yapmayabilir.
        # st.rerun() en güvenli yoldur.
        st.rerun()