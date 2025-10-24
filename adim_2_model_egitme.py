import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import warnings
import joblib

# Olası kütüphane uyarılarını gizle (opsiyonel)
warnings.filterwarnings('ignore')

# 1. Veri Setini Yükle
try:
    df = pd.read_csv('uydu_veri_seti.csv')
except FileNotFoundError:
    print("Hata: 'uydu_veri_seti.csv' dosyası bulunamadı.")
    print("Lütfen önce 'adim_1_veri_uretme.py' dosyasını çalıştırdığınızdan emin olun.")
    exit()

print("Veri Seti Başarıyla Yüklendi.")

# 2. Veri Ön İşleme (Data Preprocessing)
# Kategorik ve sayısal özellikleri belirle
kategorik_ozellikler = ['protokol']
sayisal_ozellikler = ['kaynak_port', 'hedef_port', 'paket_boyutu', 'anomali_skoru']

# Hedef değişken (y) ve özellikler (X)
X = df.drop('etiket', axis=1)
y = df['etiket']

# Kategorik verileri (OneHotEncoder) ve sayısal verileri (StandardScaler) işlemek için bir dönüştürücü oluştur
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), sayisal_ozellikler),
        ('cat', OneHotEncoder(), kategorik_ozellikler)
    ])

# 3. Modeli Oluşturma (Random Forest)
# Random Forest, bu tür sınıflandırma problemleri için hızlı ve yüksek başarılı bir modeldir.
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 4. Pipeline Oluşturma
# Pipeline, ön işleme ve model eğitme adımlarını birleştirir
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', model)])

# 5. Veri Setini Eğitim ve Test olarak Ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Modeli Eğitme
print("Yapay zeka modeli eğitiliyor...")
clf.fit(X_train, y_train)
print("Model Eğitimi Tamamlandı.")

# 7. Modeli Test Etme ve Doğrulama
y_pred = clf.predict(X_test)

# İş Paketi 2 Hedefi: En az %90 doğruluk
accuracy = accuracy_score(y_test, y_pred)
print(f"\n--- MODEL BAŞARI ÖLÇÜTÜ ---")
print(f"Elde Edilen Doğruluk Oranı: {accuracy * 100:.2f}%")

if accuracy >= 0.90:
    print("Başarılı: Model, İş Paketi 2'deki >%90 doğruluk hedefini  karşıladı.")
else:
    print("Başarısız: Modelin doğruluğu %90 hedefinin altında kaldı. 'Risk Yönetimi' [cite: 139] adımı (model mimarisini değiştirmek) gerekebilir.")

print("\nDetaylı Sınıflama Raporu:")
print(classification_report(y_test, y_pred, target_names=['Normal (0)', 'Sızıntı (1)']))

# --- MODELİ KAYDETME ADIMI ---
# Eğitilmiş modeli (pipeline'ın tamamını) bir dosyaya kaydet
model_dosyasi = 'siber_guvenlik_modeli.joblib'
joblib.dump(clf, model_dosyasi)

print(f"\nModel başarıyla '{model_dosyasi}' dosyasına kaydedildi.")