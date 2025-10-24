import streamlit as st
import joblib
import pandas as pd
import random
import hashlib
import time
from threading import Thread

# --- Sayfa Konfigürasyonu (Tablete daha uygun) ---
st.set_page_config(
    page_title="Uydu Güvenlik Prototipi",
    page_icon="🛰️",
    layout="wide"
)

# --- Session State (Verileri saklamak için) ---
# Streamlit'te global değişkenler yerine 'session_state' kullanılır
if 'anlik_kod' not in st.session_state:
    st.session_state.anlik_kod = ""
    st.session_state.anlik_konum = ""
    st.session_state.kod_ureteci_calisiyor = False

# --- AI MODELİNİ YÜKLEME ---
@st.cache_resource  # Modeli sadece bir kez yükle, hafızada tut
def modeli_yukle():
    try:
        model = joblib.load('siber_guvenlik_modeli.joblib')
        return model
    except FileNotFoundError:
        st.error("HATA: 'siber_guvenlik_modeli.joblib' bulunamadı! Lütfen Adım 2'yi çalıştırın.")
        return None

ai_model = modeli_yukle()

# --- DİNAMİK KOD ÜRETECİ FONKSİYONLARI ---
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

    konum_string_kod = f"{enlem_derece}{enlem_yon}{enlem_dakika}{enlem_saniye}-{boylam_derece}{boylam_yon}{boylam_dakika}{boylam_saniye}"
    konum_string_goster = f"Enlem: {enlem_derece}° {enlem_dakika}' {enlem_saniye}\" {enlem_yon} | Boylam: {boylam_derece}° {boylam_dakika}' {boylam_saniye}\" {boylam_yon}"

    return konum_string_kod, konum_string_goster

def kodu_sifrele(konum_string):
    """Konum string'ini SHA-256 ile karmaşık koda dönüştürür."""
    return hashlib.sha256(konum_string.encode('utf-8')).hexdigest()

def dinamik_kod_guncelleyici():
    """[ARKA PLAN GÖREVİ] Her saniye global güvenlik kodunu yeniler."""
    while True:
        anlik_konum_kod, anlik_konum_goster = cografi_konum_uret()
        st.session_state.anlik_kod = kodu_sifrele(anlik_konum_kod)
        st.session_state.anlik_konum = anlik_konum_goster
        time.sleep(1) # Her saniye yenile

# --- PAKET ANALİZ FONKSİYONU ---
def paketi_analiz_et(paket_verisi, gelen_kod):
    """Gelen paketi analiz eder ve sonucu görsel olarak basar."""

    anlik_kod_sistem = st.session_state.anlik_kod

    # 1. KONTROL: Sonsuz Güvenlik Duvarı
    if gelen_kod != anlik_kod_sistem:
        st.error(f"**SONUÇ: ERKEN TESPİT!** 🛑\n\nPaket 'Sonsuz Güvenlik Duvarı'nı geçemedi. Kod eşleşmiyor.\n\n"
                 f"Gelen Kod: `{gelen_kod}`\n\n"
                 f"Sistem Kodu: `{anlik_kod_sistem}`")
        return

    # 2. KONTROL: Yapay Zeka Tabanlı Derin Tarama
    st.info("Güvenlik Kodu DOĞRU. Paket 'Yapay Zeka Tabanlı' derin taramaya yönlendiriliyor...")

    try:
        df = pd.DataFrame([paket_verisi])
        tahmin = ai_model.predict(df)
        tahmin_olasilik = ai_model.predict_proba(df)

        if tahmin[0] == 1: # 1 = Sızıntı
            st.warning(f"**SONUÇ: YAPAY ZEKA TESPİTİ!** ⚠️\n\n"
                       f"Model bu paketi **%{tahmin_olasilik[0][1]*100:.2f}** ihtimalle 'Sızıntı' olarak sınıflandırdı.\n\n"
                       f"DURUM: TEHDİT ENGELLENDİ.")
        else: # 0 = Normal
            st.success(f"**SONUÇ: GÜVENLİ.** ✅\n\n"
                       f"Model bu paketi **%{tahmin_olasilik[0][0]*100:.2f}** ihtimalle 'Normal' olarak sınıflandırdı.\n\n"
                       f"DURUM: İZİN VERİLDİ.")
    except Exception as e:
        st.error(f"AI Modeli analiz sırasında hata verdi: {e}")


# --- GÖRSEL ARAYÜZ (UI) ---

st.title("🛰️ Yapay Zeka Tabanlı Uydu Güvenlik Duvarı Prototipi")
st.caption(f"Ekip: Muhammed Soysal, Bedirhan Şakalar, Hilal Akçiçek, Büşra Çetinkaya | Danışman: N. Furkan Bar")

# Arka plan kod üretecini sadece bir kez başlat
if not st.session_state.kod_ureteci_calisiyor:
    kod_guncelleme_thread = Thread(target=dinamik_kod_guncelleyici, daemon=True)
    kod_guncelleme_thread.start()
    st.session_state.kod_ureteci_calisiyor = True

# Dinamik olarak güncellenecek alan
st.subheader("Sonsuz Güvenlik Duvarı (Dinamik Kod Üreteci)")
placeholder = st.empty()

st.subheader("İş Paketi 3: Test-Doğrulama Senaryoları")
st.markdown("Test etmek için bir senaryo seçin. Arka plandaki 'Anlık Güvenlik Kodu'nun her saniye değiştiğini gözlemleyin.")

col1, col2, col3 = st.columns(3)

# --- SENARYO BUTONLARI ---
with col1:
    if st.button("Senaryo 1: [GÜVENLİ] Paket Gönder", type="primary", use_container_width=True):
        paket = {'protokol': 'TCP', 'kaynak_port': 1025, 'hedef_port': 443, 'paket_boyutu': 128, 'anomali_skoru': 0.1}
        gelen_kod = st.session_state.anlik_kod # Doğru kodu kullan
        paketi_analiz_et(paket, gelen_kod)

with col2:
    if st.button("Senaryo 2: [TEHLİKELİ] Paket Gönder", use_container_width=True):
        paket = {'protokol': 'ICMP', 'kaynak_port': 45000, 'hedef_port': 666, 'paket_boyutu': 4000, 'anomali_skoru': 0.9}
        gelen_kod = st.session_state.anlik_kod # Doğru kodu kullan
        paketi_analiz_et(paket, gelen_kod)

with col3:
    if st.button("Senaryo 3: [SALDIRGAN] Paket Gönder", type="secondary", use_container_width=True):
        paket = {'protokol': 'UDP', 'kaynak_port': 12345, 'hedef_port': 1337, 'paket_boyutu': 100, 'anomali_skoru': 0.7}
        gelen_kod = "SALDIRGANIN_TAHMINI_veya_ESKI_KOD_abc123" # Yanlış kod
        paketi_analiz_et(paket, gelen_kod)


# --- DİNAMİK ALANI GÜNCELLEME DÖNGÜSÜ ---
# Bu döngü, ekranın her saniye yenilenmesini sağlar
while True:
    with placeholder.container():
        st.metric(label="Anlık Coğrafi Konum", value=st.session_state.anlik_konum)
        st.code(f"Anlık Güvenlik Kodu (Hash): {st.session_state.anlik_kod}", language="text")
        time.sleep(1) # 1 saniyede bir arayüzü yenile