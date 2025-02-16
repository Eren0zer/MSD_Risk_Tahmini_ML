# -*- coding: utf-8 -*-
"""Donem_projesi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e9qQBF-hBKqbajht7iKgEspUneL5BPHe
"""
# Gerekli kütüphaneleri import ediyoruz
import pandas as pd  # Veri işleme ve analizi için kullanılan kütüphane
import matplotlib.pyplot as plt  # Grafikler ve görselleştirme için kullanılan kütüphane
import seaborn as sns  # Daha gelişmiş görselleştirme ve veri analizi için matplotlib ile entegre çalışan kütüphane
from plotnine import ggplot  # ggplot tarzı görselleştirmeler yapmak için kullanılan kütüphane
from sklearn.multioutput import MultiOutputClassifier  # Çoklu etiketli sınıflandırma için
from sklearn.ensemble import RandomForestClassifier  # Random Forest algoritması
from sklearn.linear_model import LogisticRegression  # Lojistik Regresyon algoritması
from sklearn.svm import SVC  # Destek Vektör Makineleri (SVM)
from sklearn.model_selection import train_test_split  # Eğitim ve test verilerini ayırmak için
from sklearn.preprocessing import StandardScaler  # Verileri standartlaştırmak için
from sklearn.metrics import classification_report, accuracy_score  # Sınıflandırma raporu ve doğruluk skoru için
from imblearn.over_sampling import SMOTE  # Sınıf dengesizliğini gidermek için SMOTE
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split  # Veri setini eğitim ve test olarak bölmek için
from sklearn.ensemble import RandomForestClassifier  # Random Forest algoritmasını kullanmak için
from sklearn.metrics import accuracy_score  # Modelin doğruluğunu ölçmek için

# Veri setini yüklemek için dosya yolunu tanımlıyoruz
file_path = 'msd_risk_dataset.xlsx' 

# Excel dosyasını yükleyerek incelemek için bir değişkene atıyoruz
data = pd.ExcelFile(file_path) 

# Excel dosyasındaki tüm sayfaların isimlerini görüntülüyoruz
data.sheet_names  

# İlk sayfayı (Sheet1) veri seti olarak yükleyerek yapısını incelemek için bir DataFrame'e aktarıyoruz
df = data.parse('Sheet1')  

# Veri setinin ilk birkaç satırını görüntülüyoruz
df.head() 

# Veri setindeki sayısal sütunları seçiyoruz (float64 ve int64 türündeki sütunlar)
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Genel grafik stilini ve boyutunu ayarlıyoruz
plt.style.use('ggplot')  # ggplot tarzında bir görselleştirme stili kullanılıyor
plt.figure(figsize=(20, 15))  

# Her sayısal sütun için alt grafikler (subplots) oluşturuyoruz
for i, col in enumerate(numeric_columns, start=1):
    plt.subplot(len(numeric_columns) // 3 + 1, 3, i)  
    sns.histplot(df[col], kde=True, bins=20, color='blue', alpha=0.7)  
    plt.title(f"Distribution of {col}", fontsize=12)  # Histogram başlığını sütun adına göre ayarlıyoruz
    plt.xlabel(col, fontsize=10)  
    plt.ylabel("Frequency", fontsize=10) 

# Grafiklerin düzenlenmesi ve aralarındaki boşlukların ayarlanması
plt.tight_layout()

# Tüm grafikleri ekranda gösteriyoruz
plt.show()

# Veri setinin satır ve sütun sayısını öğreniyoruz
df.shape 

# Veri setindeki her bir sütunun veri tipini öğreniyoruz
df.dtypes 

# Korelasyon hesaplamak için sadece sayısal sütunları seçiyoruz
numeric_df = df.select_dtypes(include=['float64', 'int64'])  

# Sayısal sütunlar arasındaki korelasyonu hesaplar ve bir matris döndürür
correlation_matrix = numeric_df.corr()  

# Korelasyon matrisini görselleştirmek için ısı haritası (heatmap) çiziyoruz
plt.figure(figsize=(12, 8)) 
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Correlation Matrix")  # Grafik için bir başlık ekliyoruz
plt.show()

# Veri setinde eksik değerleri kontrol ediyoruz
missing_values = df.isnull().sum()

# Eksik değerlerin analiz edilmesi için ekrana yazdırıyoruz
missing_values 

# describe(): Sayısal sütunlar için özet istatistikler döner (örneğin, ortalama, standart sapma, minimum ve maksimum değerler)
basic_stats = df.describe()


basic_stats  # Her sütun için istatistiksel özet verileri gösterir

# Veri setindeki kategorik sütunları seçiyoruz
df_categorical = df.select_dtypes(include="object")
df_categorical.head(4)


# "Backpack Height" sütunundaki benzersiz (unique) değerleri görüntülüyoruz
df['Backpack Height'].unique()

# "Backpack Height" sütunundaki değerlerin frekansını (sıklığını) hesaplıyor ve yatay bir çubuk grafikle görselleştiriyoruz
df['Backpack Height'].value_counts().plot.barh(
    color=['#8b008b', '#104e8b', '#008b45']  
);

# "msd_risk" sütunundaki benzersiz (unique) değerleri görüntülüyoruz
df['msd_risk'].unique()

# "msd_risk" sütunundaki değerlerin frekansını (sıklığını) hesaplıyor ve yatay bir çubuk grafikle görselleştiriyoruz
df['msd_risk'].value_counts().plot.barh(
    color=['#8b008b', '#104e8b', '#008b45']  
);

# "Gender" sütunundaki benzersiz (unique) değerleri görüntülüyoruz
df['Gender'].unique()

# "Gender" sütunundaki cinsiyetlerin sayısını hesaplıyoruz
gender_counts = df['Gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']
# Sütun isimlerini "Gender" (Cinsiyet) ve "Count" (Sayı) olarak yeniden adlandırıyoruz

plt.figure(figsize=(5, 6)) 
# Bar grafiği oluşturuyoruz
ax = sns.barplot(
    data=gender_counts,  # Görselleştirilecek veri
    x='Gender',          # X eksenine cinsiyetleri yerleştiriyoruz
    y='Count',           # Y eksenine frekansları (sayıları) yerleştiriyoruz
    palette={"Male": "#1F77B4", "Female": "#FF69B4"}  
)

# Grafik başlığı ve eksen etiketlerini ayarlıyoruz
plt.title('Gender Distribution')  # Grafiğe bir başlık ekliyoruz
plt.xlabel('Gender')  # X eksenine "Cinsiyet" etiketi veriyoruz
plt.ylabel('Count')   # Y eksenine "Sayı" etiketi veriyoruz

# Grafiği ekranda gösteriyoruz
plt.show()  

# Sayısal sütunları seçiyoruz
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Genel stil ayarını yapıyoruz
sns.set_style("whitegrid")


# Boxplot grafikleri için bir ızgara düzeni oluşturuyoruz
n_cols = 3  # Izgara düzeninde her satırdaki sütun sayısını 3 olarak belirliyoruz
n_rows = -(-len(numerical_columns) // n_cols)  # Sayısal sütun sayısına göre toplam satır sayısını hesaplıyoruz

# Grafik boyutunu ayarlıyoruz
plt.figure(figsize=(18, n_rows * 4)) 

# Her bir sayısal sütun için bir boxplot oluşturuyoruz
for i, col in enumerate(numerical_columns, start=1):
    plt.subplot(n_rows, n_cols, i)  # Her sütun için bir alt grafik (subplot) oluşturuyoruz
    sns.boxplot(
        x=df[col],  # Boxplot grafiği için seçilen sütun
        color='#4682B4',  
        fliersize=5,  # Aykırı değerlerin (outliers) boyutunu belirliyoruz
        linewidth=2,  
        boxprops=dict(alpha=0.7)  # Kutuların saydamlığını (%70) ayarlıyoruz
    )
    plt.title(f"Boxplot of {col}", fontsize=12, fontweight='bold')  # Grafiğin başlığını sütun adına göre ayarlıyoruz
    plt.xlabel(col, fontsize=10) 
    plt.xticks(fontsize=9)  
    plt.grid(axis='y', linestyle='--', alpha=0.6) 

# Tüm grafikleri düzenli bir şekilde yerleştiriyoruz
plt.tight_layout()
plt.show()

# MSD risk seviyelerini sayısal değerlere dönüştürmek için bir eşleme (mapping) yapıyoruz
msd_risk_mapping = {'Low': 1, 'Medium': 2, 'High': 3}

df['msd_risk_encoded'] = df['msd_risk'].map(msd_risk_mapping)
# 'msd_risk' sütunundaki değerleri eşleme tablosuna göre dönüştürüp yeni bir sütuna kaydediyoruz

# MSD risk seviyelerinin her "Backpack Height" (çanta yüksekliği) kategorisi için ortalamasını hesaplıyoruz
backpack_risk_avg = df.groupby('Backpack Height')['msd_risk_encoded'].mean().sort_values()
backpack_risk_avg  # Her çanta yüksekliği kategorisi için hesaplanan ortalama MSD risk seviyelerini gösterir



# Modelleme için veri setini hazırlıyoruz
# Özellik sütunlarını ve hedef değişkeni tanımlıyoruz
features = df.drop(columns=['msd_risk', 'msd_risk_encoded', 'Gender'])
# 'msd_risk', 'msd_risk_encoded' ve 'Gender' sütunlarını özelliklerden çıkarıyoruz
target = df['msd_risk_encoded']  # Hedef değişken olarak sayısal olarak kodlanmış MSD risk seviyesini seçiyoruz

# Çanta yüksekliği için Ordinal Encoding yapıyoruz
ordinal_mapping = {'Shoulder Blades to Lower Back': 1, 'On Buttocks': 2, 'Slightly Lower': 3}
# Çanta yüksekliği kategorilerini sıralı (ordinal) değerlere dönüştürüyoruz
df['Backpack Height Ordinal'] = df['Backpack Height'].map(ordinal_mapping)
# Yeni sütun, her kategoriyi sıralı bir değerle eşler
features_ordinal = features.copy()  # Orijinal özellikleri kopyalıyoruz
features_ordinal['Backpack Height'] = df['Backpack Height Ordinal']
# Sıralı kodlanmış çanta yüksekliği sütununu ekliyoruz

# Çanta yüksekliği için One-Hot Encoding yapıyoruz
features_onehot = pd.get_dummies(features, columns=['Backpack Height'], drop_first=True)
# Çanta yüksekliği sütununu One-Hot Encoding ile dönüştürüyoruz


X_train_ord, X_test_ord, y_train, y_test = train_test_split(features_ordinal, target, test_size=0.3, random_state=42)
# Sıralı kodlanmış veriler için eğitim ve test verileri
X_train_onehot, X_test_onehot, _, _ = train_test_split(features_onehot, target, test_size=0.3, random_state=42)
# One-Hot kodlanmış veriler için eğitim ve test verileri

# Random Forest algoritması için modelleri tanımlıyoruz
rf_ord = RandomForestClassifier(random_state=42)  # Sıralı kodlama için model
rf_onehot = RandomForestClassifier(random_state=42)  # One-Hot kodlama için model

# Modelleri eğitiyoruz
rf_ord.fit(X_train_ord, y_train)  # Sıralı kodlanmış verilerle eğitme
rf_onehot.fit(X_train_onehot, y_train)  # One-Hot kodlanmış verilerle eğitme

# Test verileri üzerinde tahminler yapıyoruz
y_pred_ord = rf_ord.predict(X_test_ord)  # Sıralı kodlama ile tahminler
y_pred_onehot = rf_onehot.predict(X_test_onehot)  # One-Hot kodlama ile tahminler

# Doğruluk (accuracy) skorlarını hesaplıyoruz
accuracy_ord = accuracy_score(y_test, y_pred_ord)  # Sıralı kodlama için doğruluk
accuracy_onehot = accuracy_score(y_test, y_pred_onehot)  # One-Hot kodlama için doğruluk

# Doğruluk skorlarını görüntülüyoruz
accuracy_ord, accuracy_onehot  # Her iki yöntemin doğruluk skorları

# "Backpack Height" sütunu için One-Hot Encoding uyguluyoruz
df_cleaned = pd.get_dummies(df, columns=['Backpack Height'], drop_first=False)


# Gereksiz sütunları kaldırıyoruz (varsa)
df_cleaned = df_cleaned.drop(columns=['msd_risk_encoded'], errors='ignore')
# "msd_risk_encoded" sütunu veri setinden kaldırılır. Yoksa hata vermemesi için errors='ignore' eklenir
df_cleaned = df_cleaned.drop(columns=['Backpack Height Ordinal'], errors='ignore')
# Daha önce oluşturulmuş "Backpack Height Ordinal" sütunu kaldırılır

# Güncellenmiş veri setinin ilk birkaç satırını görüntülüyoruz
df_cleaned.head()


# "Gender" sütunu için One-Hot Encoding uyguluyoruz
df_cleaned = pd.get_dummies(df_cleaned, columns=['Gender'], drop_first=False)


# Güncellenmiş veri setinin ilk birkaç satırını görüntülüyoruz
df_cleaned.head()


# Hedef değişken (msd_risk) dağılımını analiz ediyoruz
msd_risk_distribution = df['msd_risk'].value_counts(normalize=True)


# Hedef değişkenin dağılımını ekrana yazdırıyoruz
msd_risk_distribution


# "msd_risk" sütunu için One-Hot Encoding uyguluyoruz
df_cleaned = pd.get_dummies(df_cleaned, columns=['msd_risk'], drop_first=False)

# Güncellenmiş veri setinin ilk birkaç satırını görüntülüyoruz
df_cleaned.head()

# "msd_risk" ve "Backpack Weight" arasındaki ilişkiyi görselleştirmek için bir boxplot oluşturuyoruz
sns.boxplot(x='msd_risk', y='Backpack Weight', data=df)
plt.show() 

# "msd_risk" kategorilerinin ve cinsiyetlere göre dağılımını görselleştirmek için bir countplot oluşturuyoruz
sns.countplot(x='msd_risk', hue='Gender', data=df)
plt.show()

# Sayısal sütunları seçiyoruz
numeric_columns = df_cleaned.select_dtypes(include=['float64', 'int64']).columns

# IQR yöntemiyle aykırı değerlerin tespiti ve kaldırılması
for col in numeric_columns:
    Q1 = df_cleaned[col].quantile(0.25)  # 1. Çeyrek (25. yüzdelik değer)
    Q3 = df_cleaned[col].quantile(0.75)  # 3. Çeyrek (75. yüzdelik değer)
    IQR = Q3 - Q1  # Çeyrekler arası aralık (Interquartile Range)

    # Aykırı değerler için alt ve üst sınırları tanımlıyoruz
    lower_bound = Q1 - 1.5 * IQR  # Alt sınır
    upper_bound = Q3 + 1.5 * IQR  # Üst sınır

    # Aykırı değerleri tespit ediyor ve sayıyoruz
    outliers = ((df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)).sum()
    print(f"{col}: {outliers} aykırı değer")  # Her sütundaki aykırı değerlerin sayısını yazdırıyoruz

    # Aykırı değerleri veri setinden kaldırıyoruz
    df_cleaned = df_cleaned[(df_cleaned[col] >= lower_bound) & (df_cleaned[col] <= upper_bound)]
    # Alt ve üst sınırın dışındaki değerler veri setinden çıkarılır

# Aykırı değerlerin kaldırılmasından sonra veri setinin boyutunu kontrol ediyoruz
print(f"Aykırı değerler kaldırıldıktan sonra veri setinin boyutu: {df_cleaned.shape}")
# Yeni satır ve sütun sayısını yazdırıyoruz

df_cleaned.head()



# Orijinal "msd_risk" sütununu kaldırıyoruz (varsa)
df_cleaned = df_cleaned.drop(columns=['msd_risk'], errors='ignore')
# "msd_risk" sütunu zaten One-Hot Encoded olduğu için kaldırıyoruz.

# Hedef sütunlar (One-Hot Encoding ile kodlanmış)
target_columns = ['msd_risk_High', 'msd_risk_Medium', 'msd_risk_Low']
X = df_cleaned.drop(columns=target_columns)  # Özellik sütunları
y = df_cleaned[target_columns]  # Hedef sütunlar

# Eğitim ve test verilerini bölüyoruz
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# Eğitim ve test verileri %70 - %30 oranında ayrılıyor

# SMOTE ile her hedef sütun için sınıf dengesizliğini gideriyoruz
X_train_resampled = []  # Yeniden örneklenen X verileri
y_train_resampled = []  # Yeniden örneklenen y verileri

smote = SMOTE(random_state=42)  # SMOTE nesnesini oluşturuyoruz

# SMOTE işlemini her bir hedef sütun için uyguluyoruz
for col in target_columns:
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train[col])
    X_train_resampled.append(X_resampled)
    y_train_resampled.append(y_resampled)

# Yeniden örneklenen verileri birleştiriyoruz
import numpy as np
X_train_resampled = np.concatenate(X_train_resampled, axis=0)
y_train_resampled = np.concatenate(y_train_resampled, axis=0)

# Sayısal özellikleri standartlaştırıyoruz
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train.select_dtypes(include=['float64', 'int64']))
# Eğitim verilerini standartlaştırıyoruz
X_test_scaled = scaler.transform(X_test.select_dtypes(include=['float64', 'int64']))
# Test verilerini aynı ölçekte standartlaştırıyoruz

# Algoritma 1: Random Forest ile Multi-Label Sınıflandırma
multi_rf = MultiOutputClassifier(RandomForestClassifier(random_state=42))
multi_rf.fit(X_train_scaled, y_train)  # Modeli eğitiyoruz
y_pred_rf = multi_rf.predict(X_test_scaled)  # Tahminler yapıyoruz

# Random Forest için sınıflandırma raporu
print("Random Forest Çoklu Etiketli Sınıflandırma Raporu:")
for i, col in enumerate(target_columns):
    # Her etiket için sınıflandırma raporunu yazdırıyoruz
    print(f"Etiket: {col}")
    print(classification_report(y_test.iloc[:, i], y_pred_rf[:, i], zero_division=0))

# Random Forest için doğruluk skorları
rf_accuracy = [accuracy_score(y_test.iloc[:, i], y_pred_rf[:, i]) for i in range(len(target_columns))]
print(f"Random Forest Her Etiket İçin Doğruluk: {rf_accuracy}")
print(f"Random Forest Genel Doğruluk: {sum(rf_accuracy) / len(target_columns)}\n")

# Algoritma 2: Logistic Regression ile Multi-Label Sınıflandırma
multi_log_reg = MultiOutputClassifier(LogisticRegression(max_iter=1000, random_state=42))
multi_log_reg.fit(X_train_scaled, y_train)  # Modeli eğitiyoruz
y_pred_log = multi_log_reg.predict(X_test_scaled)  # Tahminler yapıyoruz

# Lojistik Regresyon için sınıflandırma raporu
print("Lojistik Regresyon Çoklu Etiketli Sınıflandırma Raporu:")
for i, col in enumerate(target_columns):
    # Her etiket için sınıflandırma raporunu yazdırıyoruz
    print(f"Etiket: {col}")
    print(classification_report(y_test.iloc[:, i], y_pred_log[:, i], zero_division=0))

# Lojistik Regresyon için doğruluk skorları
log_reg_accuracy = [accuracy_score(y_test.iloc[:, i], y_pred_log[:, i]) for i in range(len(target_columns))]
print(f"Lojistik Regresyon Her Etiket İçin Doğruluk: {log_reg_accuracy}")
print(f"Lojistik Regresyon Genel Doğruluk: {sum(log_reg_accuracy) / len(target_columns)}\n")

# Algoritma 3: SVM ile Multi-Label Sınıflandırma
multi_svc = MultiOutputClassifier(SVC(random_state=42))
multi_svc.fit(X_train_scaled, y_train)  # Modeli eğitiyoruz
y_pred_svm = multi_svc.predict(X_test_scaled)  # Tahminler yapıyoruz

# SVM için sınıflandırma raporu
print("SVM Çoklu Etiketli Sınıflandırma Raporu:")
for i, col in enumerate(target_columns):
    # Her etiket için sınıflandırma raporunu yazdırıyoruz
    print(f"Etiket: {col}")
    print(classification_report(y_test.iloc[:, i], y_pred_svm[:, i], zero_division=0))

# SVM için doğruluk skorları
svc_accuracy = [accuracy_score(y_test.iloc[:, i], y_pred_svm[:, i]) for i in range(len(target_columns))]
print(f"SVM Her Etiket İçin Doğruluk: {svc_accuracy}")
print(f"SVM Genel Doğruluk: {sum(svc_accuracy) / len(target_columns)}\n")

# Algoritma 4: KNN ile Multi-Label Sınıflandırma
multi_knn = MultiOutputClassifier(KNeighborsClassifier(n_neighbors=5))
multi_knn.fit(X_train_scaled, y_train)
y_pred_knn = multi_knn.predict(X_test_scaled)

# KNN için sınıflandırma raporu
print("KNN Çoklu Etiketli Sınıflandırma Raporu:")
for i, col in enumerate(target_columns):
    print(f"Etiket: {col}")
    print(classification_report(y_test.iloc[:, i], y_pred_knn[:, i], zero_division=0))

# KNN doğruluk skorları
knn_accuracy = [accuracy_score(y_test.iloc[:, i], y_pred_knn[:, i]) for i in range(len(target_columns))]
print(f"KNN Her Etiket İçin Doğruluk: {knn_accuracy}")
print(f"KNN Genel Doğruluk: {sum(knn_accuracy) / len(target_columns)}\n")

# Algoritma 5: XGBoost ile Multi-Label Sınıflandırma
multi_xgb = MultiOutputClassifier(XGBClassifier(random_state=42, eval_metric='mlogloss'))
multi_xgb.fit(X_train_scaled, y_train)  # Modeli eğitiyoruz
y_pred_xgb = multi_xgb.predict(X_test_scaled)  # Tahmin yapıyoruz

# XGBoost için sınıflandırma raporu ve doğruluk hesaplama
print("XGBoost Çoklu Etiketli Sınıflandırma Raporu:")
xgb_accuracies = []  # Her etiket için doğrulukları saklamak için bir liste
for i, col in enumerate(target_columns):
    print(f"Etiket: {col}")
    print(classification_report(y_test.iloc[:, i], y_pred_xgb[:, i], zero_division=0))
    acc = accuracy_score(y_test.iloc[:, i], y_pred_xgb[:, i])  # Her etiket için doğruluk skoru
    xgb_accuracies.append(acc)
    print(f"{col} için doğruluk: {acc:.4f}")

# Genel doğruluk
overall_accuracy = sum(xgb_accuracies) / len(target_columns)
print(f"XGBoost Her Etiket İçin Doğruluk: {xgb_accuracies}")
print(f"XGBoost Genel Doğruluk: {overall_accuracy:.4f}")