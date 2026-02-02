import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import warnings
import joblib

# Gereksiz uyarıları gizle
warnings.filterwarnings('ignore')

# 1. Veri Setini Yükle
try:
    df = pd.read_csv('uydu_veri_seti.csv')
    print("[Sistem]: 'uydu_veri_seti.csv' başarıyla yüklendi.")
except FileNotFoundError:
    print("[Hata]: Veri seti bulunamadı! Lütfen önce Adım 1'i çalıştırın.")
    exit()

# 2. Veri Ön İşleme (Feature Engineering)
# KRİTİK: 'anomali_skoru' özelliğini modelin "kopya çekmesini" engellemek için çıkardık.
# Model artık sadece ham ağ trafiği parametrelerini analiz edecek.
kategorik_ozellikler = ['protokol']
sayisal_ozellikler = ['kaynak_port', 'hedef_port', 'paket_boyutu']

# Özellikler (X) ve Hedef (y)
X = df[kategorik_ozellikler + sayisal_ozellikler]
y = df['etiket']

# Dönüştürücü (Preprocessing) Tanımlama
# Sayısal veriler için standartlaştırma, kategorik veriler için One-Hot encoding uyguluyoruz.
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), sayisal_ozellikler),
        ('cat', OneHotEncoder(handle_unknown='ignore'), kategorik_ozellikler)
    ])

# 3. Model ve Pipeline Oluşturma
# RandomForest, siber güvenlik verilerindeki karmaşık ilişkileri yakalamak için idealdir.
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Pipeline: Ön işleme ve modelleme adımlarını tek bir çatı altında birleştirir.
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', model)])

# 4. Eğitim ve Test Verisini Ayırma
# Verinin %80'i ile eğitiyor, %20'si ile performansını ölçüyoruz.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Modeli Eğitme
print("Yapay zeka modeli gerçekçi senaryolara göre eğitiliyor...")
clf.fit(X_train, y_train)
print("Eğitim Süreci Başarıyla Tamamlandı.")

# 6. Performans Analizi
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n" + "="*40)
print(f"--- GERÇEKÇİ MODEL BAŞARI RAPORU ---")
print(f"Doğruluk Oranı (Accuracy): {accuracy * 100:.2f}%")
print("="*40)

print("\nDetaylı Sınıflandırma Analizi:")
print(classification_report(y_test, y_pred))

# 7. Modeli Kaydetme
# Bu dosya Adım 4 ve Adım 5 tarafından kullanılacaktır.
joblib.dump(clf, 'siber_guvenlik_modeli.joblib')
print("\n[BİLGİ]: Güncel model 'siber_guvenlik_modeli.joblib' adıyla kaydedildi.")