import streamlit as st
import joblib
import pandas as pd
import random
import hashlib
import time
from threading import Thread

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Uydu Güvenlik Prototipi", page_icon="🛰️", layout="wide")

# --- Durum Yönetimi (Session State) ---
if 'anlik_kod' not in st.session_state:
    st.session_state.anlik_kod = ""
    st.session_state.anlik_konum = ""
    st.session_state.kod_ureteci_calisiyor = False


# --- Model Yükleme ---
@st.cache_resource
def modeli_yukle():
    try:
        return joblib.load('siber_guvenlik_modeli.joblib')
    except:
        return None


ai_model = modeli_yukle()


# --- Dinamik Kod Mantığı ---
def dinamik_kod_guncelleyici():
    while True:
        enlem = f"{random.randint(0, 90)}K{random.randint(0, 59)}D"
        boylam = f"{random.randint(0, 180)}D{random.randint(0, 59)}D"
        st.session_state.anlik_konum = f"Konum: {enlem} | {boylam}"
        st.session_state.anlik_kod = hashlib.sha256(f"{enlem}-{boylam}".encode()).hexdigest()
        time.sleep(1)


if not st.session_state.kod_ureteci_calisiyor:
    Thread(target=dinamik_kod_guncelleyici, daemon=True).start()
    st.session_state.kod_ureteci_calisiyor = True


# --- Analiz Fonksiyonu ---
def paketi_analiz_et(paket_verisi, gelen_kod):
    # --- ÖLÇÜM BAŞLAT ---
    start_time = time.perf_counter()

    if gelen_kod != st.session_state.anlik_kod:
        st.error("🛑 ERKEN TESPİT! Kod Uyuşmuyor.")
        return

    df = pd.DataFrame([paket_verisi])
    tahmin = ai_model.predict(df)

    # --- ÖLÇÜM BİTİR ---
    end_time = time.perf_counter()
    gecikme_ms = (end_time - start_time) * 1000

    if tahmin[0] == 1:
        st.warning(f"⚠️ AI TESPİTİ! (Analiz Süresi: {gecikme_ms:.2f} ms)")
    else:
        st.success(f"✅ GÜVENLİ. (Analiz Süresi: {gecikme_ms:.2f} ms)")


# --- Arayüz Tasarımı ---
st.title("🛰️ Yapay Zeka Tabanlı Uydu Güvenlik Prototipi")
st.markdown("Bu prototip, Dinamik Şifreleme ve Yapay Zeka katmanlarını birleştirerek uydu verilerini korur.")

# Dinamik Veri Gösterge Paneli
placeholder = st.empty()

# Test Senaryoları
st.subheader("Simülasyon Senaryoları")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Senaryo 1: [GÜVENLİ]", type="primary", use_container_width=True):
        # Normal port, düşük anomali skoru (0.25)
        paket = {'protokol': 'TCP', 'kaynak_port': 1024, 'hedef_port': 443, 'paket_boyutu': 800, 'anomali_skoru': 0.25}
        paketi_analiz_et(paket, st.session_state.anlik_kod)

with col2:
    if st.button("Senaryo 2: [SIZINTI]", use_container_width=True):
        # Şüpheli port, yüksek paket boyutu ve anomali skoru (0.65)
        paket = {'protokol': 'TCP', 'kaynak_port': 5000, 'hedef_port': 8080, 'paket_boyutu': 4200,
                 'anomali_skoru': 0.65}
        paketi_analiz_et(paket, st.session_state.anlik_kod)

with col3:
    if st.button("Senaryo 3: [SALDIRGAN]", type="secondary", use_container_width=True):
        # Kodun uyuşmadığı durum testi
        paket = {'protokol': 'UDP', 'kaynak_port': 9999, 'hedef_port': 666, 'paket_boyutu': 50, 'anomali_skoru': 0.90}
        paketi_analiz_et(paket, "GECERSIZ_VEYA_ESKI_ANAHTAR")

# Ekranı saniyede bir güncelle
while True:
    with placeholder.container():
        c1, c2 = st.columns(2)
        c1.metric("Anlık Uydu Konumu", st.session_state.anlik_konum)
        c2.metric("Aktif Güvenlik Anahtarı", st.session_state.anlik_kod[:12] + "...")
        time.sleep(1)