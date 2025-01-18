# Veri Analizi ve Makine Öğrenmesi Projesi

Bu proje, öğrencilerde kas-iskelet sistemi bozuklukları riskini tahmin etmeyi amaçlamaktadır. Kullanılan veri seti, Kaggle'da [Musculoskeletal Disorders Risk in Students](https://www.kaggle.com/datasets/mrhmnshu/musculoskeletal-disorders-risk-in-students) başlığı altında erişilebilir.

---

## İçindekiler

1. [Proje Hedefi](#1-proje-hedefi)
2. [Veri Yükleme ve Görüntüleme](#2-veri-yükleme-ve-görüntüleme)
3. [Histogramlarla Veriyi Görselleştirme](#3-histogramlarla-veriyi-görselleştirme)
4. [Veri Setinin Yapısını Anlama](#4-veri-setinin-yapısını-anlama)
5. [Korelasyon Matrisi](#5-korelasyon-matrisi)
6. [Eksik Değer Analizi ve Özet İstatistikler](#6-eksik-değer-analizi-ve-özet-istatistikler)
7. [Kategorik Değişkenlerin İncelenmesi](#7-kategorik-değişkenlerin-incelenmesi)
8. [MSD Riskinin İncelenmesi](#8-msd-riskinin-incelenmesi)
9. [Cinsiyet Dağılımı](#9-cinsiyet-dağılımı)
10. [Box Plot ile Değişkenlerin İncelenmesi](#10-box-plot-ile-değişkenlerin-incelenmesi)
11. [Çanta Yüksekliği ve MSD Risk Analizi](#11-canta-yuksekligi-ve-msd-risk-analizi)
12. [Gender ve MSD Risk için One-Hot Encoding](#12-gender-ve-msd-risk-icin-one-hot-encoding)
13. [MSD Risk ve Grafiksel Analizler](#13-msd-risk-ve-grafiksel-analizler)
14. [Aykırı Değer Analizi](#14-aykiri-deger-analizi)
15. [SMOTE ile Veri Dengesizliğini Giderme](#15-smote-ile-veri-dengesizligini-giderme)
16. [Makine Öğrenmesi Modellerinin Eğitimi ve Değerlendirilmesi](#16-makine-ogrenmesi-modellerinin-egitimi-ve-degerlendirilmesi)
17. [Accuracyyi Artırma Yöntemleri](#17-accuracyyi-artirma-yontemleri)
18. [Web Scraping ile Veri Elde Etme Denemesi](#18-web-scraping-ile-veri-elde-etme-denemesi)
19. [Proje ve Kodun İşleyişi](#19-proje-ve-kodun-işleyişi)
    
---

## 1. Proje Hedefi

Bu projenin amacı:

- Öğrencilerde **kas-iskelet sistemi bozuklukları riskini** (MSD riski) tahmin etmek,
- Veri temizleme, görselleştirme ve analizi gerçekleştirmek,
- Sınıf dengesizliği problemini çözmek,
- Çoklu etiketli sınıflandırma algoritmalarını kullanarak doğruluk skorlarını karşılaştırmaktır.

---

## 2. Veri Yükleme ve Görüntüleme

### Kod:
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veri setini yükleme
file_path = 'msd_risk_dataset.xlsx'
data = pd.ExcelFile(file_path)

# Sayfa isimlerini kontrol etme
data.sheet_names

# Verinin ilk sayfasını okuma
df = data.parse('Sheet1')

# Veri setinin ilk 5 satırını görüntüleme
df.head()
```

### Açıklama:

1. Veri seti, **Excel** formatında yüklenir.
2. **Sayfa isimleri** kontrol edilir ve ilk sayfa projeye dahil edilir.
3. Veri setinin ilk 5 satırı görüntülenerek içeriğin genel yapısı incelenir.

### Ekran Görüntüsü Ekleyin:
Bu bölümde, **veri setinin ilk 5 satırını gösteren ekran görüntüsünü** ekleyebilirsiniz. Bu görüntü, veri setinin yapısını görsel olarak sunmayı kolaylaştırır.

---

## 3. Histogramlarla Veriyi Görselleştirme

### Kod:
```python
# Sayısal sütunları seçiyoruz
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Grafik stilini ayarlıyoruz
plt.style.use('ggplot')
plt.figure(figsize=(20, 15))

# Her bir sayısal sütun için histogram çizimi
for i, col in enumerate(numeric_columns, start=1):
    plt.subplot(len(numeric_columns) // 3 + 1, 3, i)  # Alt grafik düzeni
    sns.histplot(df[col], kde=True, bins=20, color='blue', alpha=0.7)
    plt.title(f"Distribution of {col}", fontsize=12)
    plt.xlabel(col, fontsize=10)
    plt.ylabel("Frequency", fontsize=10)

plt.tight_layout()
plt.show()
```

### Açıklama:

1. Veri setindeki **sayısal sütunlar** seçilir.
2. Her bir sayısal değişkenin dağılımını göstermek için histogramlar oluşturulur.
3. Histogramlara **kernel density estimate (KDE)** eklenerek verinin yoğunluk dağılımı görselleştirilir.

### Analizin Amacı:
- Sayısal sütunların veri dağılımını incelemek ve olası aykırı değerleri tespit etmek.
- Verinin genel yapısını daha iyi anlamak.

### Ekran Görüntüsü Ekleyin:
- Bu bölümde, **her bir sayısal sütun için oluşturulan histogramların ekran görüntülerini** ekleyebilirsiniz.

---

## 4. Veri Setinin Yapısını Anlama

### Kod:
```python
# Satır ve sütun sayısını görüntülüyoruz
df_shape = df.shape
print(f"Veri setinde {df_shape[0]} satır ve {df_shape[1]} sütun bulunmaktadır.")

# Değişken türlerini görüntülüyoruz
df_types = df.dtypes
print(df_types)
```

### Açıklama:
1. Veri setinin satır ve sütun sayısı hesaplanarak genel boyut hakkında bilgi sağlanır.
2. Her bir sütunun veri türü incelenir (örneğin, float, int, object).

### Analizin Amacı:
- Veri setinin genel yapısını anlamak ve hangi türde veriler içerdiğini belirlemek.

### Ekran Görüntüsü Ekleyin:
- **Satır ve sütun sayısını gösteren konsol çıktısı**.
- **Değişken türlerini gösteren tablo veya çıktı**.

---

## 5. Korelasyon Matrisi

### Kod:
```python
# Sayısal sütunlar için korelasyon matrisi hesaplama
correlation_matrix = df.select_dtypes(include=['float64', 'int64']).corr()

# Korelasyon matrisi görselleştirme
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Correlation Matrix")
plt.show()
```

### Açıklama:
1. Sayısal sütunlar arasındaki korelasyon ilişkisi hesaplanır.
2. **Isı haritası** kullanılarak bu ilişkiler görselleştirilir.

### Analizin Amacı:
- Değişkenler arasındaki doğrusal ilişkileri incelemek.
- Birbirine yüksek oranda bağlı değişkenleri tespit etmek.

### Ekran Görüntüsü Ekleyin:
- **Korelasyon matrisi ısı haritasının ekran görüntüsü**.

---

## 6. Eksik Değer Analizi ve Özet İstatistikler

### Kod:
```python
# Eksik değerlerin kontrol edilmesi
missing_values = df.isnull().sum()
print("Eksik Değerler:")
print(missing_values)

# Özet istatistiklerin hesaplanması
basic_stats = df.describe()
print("Özet İstatistikler:")
print(basic_stats)
```

### Açıklama:
1. Her sütunda eksik değerlerin olup olmadığı kontrol edilir ve eksik değer sayısı hesaplanır.
2. Özet istatistikler (ortalama, standart sapma, minimum, maksimum vb.) hesaplanarak veri setinin temel özellikleri özetlenir.

### Analizin Amacı:
- Eksik değerlerin tespit edilmesi, eksik veri işleme adımlarına yön verir.
- Özet istatistikler, verinin genel özelliklerini ve dağılımını anlamak için önemlidir.

### Ekran Görüntüsü Ekleyin:
- **Eksik değerlerin listesi**.
- **Özet istatistiklerin gösterimi**.

---

## 7. Kategorik Değişkenlerin İncelenmesi

### Kod:
```python
# Kategorik değişkenlerin incelenmesi
df_categorical = df.select_dtypes(include="object")
print("Kategorik Değişkenler:")
print(df_categorical.head())

# Çanta Ağırlığının Benzersiz Değerleri
df['Backpack Weight'].unique()

# Çanta Ağırlığı Dağılımı
sns.countplot(data=df, x='Backpack Weight', palette="muted")
plt.title("Backpack Weight Distribution")
plt.xlabel("Backpack Weight")
plt.ylabel("Count")
plt.show()
```

### Açıklama:
- Kategorik değişkenlerin başlıca benzersiz değerleri ve dağılımları incelenir.
- Özellikle **Çanta Ağırlığı** dağılımı analiz edilerek görselleştirilir.

### Analizin Amacı:
- Kategorik değişkenlerin sınıf yapısını ve hangi kategorilere sahip olduğunu anlamak.
- Dağılımın dengesiz olup olmadığını kontrol etmek.

### Ekran Görüntüsü Ekleyin:
- **Kategorik değişkenlerin başlıca benzersiz değerlerini gösteren ekran görüntüsü**.
- **Çanta ağırlığı dağılım grafiği**.

---

## 8. MSD Riskinin İncelenmesi

### Kod:
```python
# MSD Riskinin Benzersiz Değerleri
df['msd_risk'].unique()

# MSD Risk Dağılımı
sns.countplot(data=df, x='msd_risk', palette="coolwarm")
plt.title("MSD Risk Distribution")
plt.xlabel("MSD Risk")
plt.ylabel("Count")
plt.show()
```

### Açıklama:
- **MSD Riskinin** (Low, Medium, High) benzersiz değerleri ve dağılımı incelenir.
- Bu dağılımın dengesiz olup olmadığı görselleştirilir.

### Analizin Amacı:
- Hedef değişkenin sınıf yapısını anlamak.
- Sınıf dengesizliği olup olmadığını tespit etmek.

### Ekran Görüntüsü Ekleyin:
- **MSD Riskinin benzersiz değerlerini ve dağılım grafiğini içeren ekran görüntüsü**.

---

## 9. Cinsiyet Dağılımı

### Kod:
```python
# Cinsiyet Dağılımı
sns.countplot(data=df, x='Gender', palette="pastel")
plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()
```

### Açıklama:
- Veri setindeki cinsiyet değişkeninin dağılımı analiz edilir ve görselleştirilir.

### Analizin Amacı:
- Cinsiyet değişkeninin veri setindeki temsil oranını anlamak.

### Ekran Görüntüsü Ekleyin:
- **Cinsiyet dağılımını gösteren grafik**.

---

## 10. Box Plot ile Değişkenlerin İncelenmesi

### Kod:
```python
# Box Plot Çizimi
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
plt.figure(figsize=(15, 10))

for i, col in enumerate(numeric_columns, start=1):
    plt.subplot(len(numeric_columns) // 3 + 1, 3, i)
    sns.boxplot(data=df, y=col, palette="cool")
    plt.title(f"Box Plot of {col}")
    plt.ylabel(col)

plt.tight_layout()
plt.show()
```

### Açıklama:
- Her bir sayısal değişken için **Box Plot** çizilir ve olası aykırı değerler incelenir.

### Analizin Amacı:
- Sayısal değişkenlerdeki aykırı değerleri tespit etmek ve genel dağılımı görselleştirmek.

### Ekran Görüntüsü Ekleyin:
-

---

## 11. Çanta Yüksekliği ve MSD Risk Analizi

### Kod:
```python
# MSD risk seviyesini sayısal olarak kodlama
msd_risk_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
df['msd_risk_encoded'] = df['msd_risk'].map(msd_risk_mapping)

# Her çanta yüksekliği kategorisi için ortalama MSD risk seviyesini hesaplama
backpack_risk_avg = df.groupby('Backpack Height')['msd_risk_encoded'].mean().sort_values()
print(backpack_risk_avg)

# Çanta yüksekliği için sıralı kodlama ve One-Hot Encoding yöntemlerini test etme
ordinal_mapping = {'Shoulder Blades to Lower Back': 1, 'On Buttocks': 2, 'Slightly Lower': 3}
df['Backpack Height Ordinal'] = df['Backpack Height'].map(ordinal_mapping)

# One-Hot Encoding
df_onehot = pd.get_dummies(df, columns=['Backpack Height'], drop_first=True)

# Sonuç: One-Hot Encoding daha iyi bir performans gösterdiği için uygulanır
# Gereksiz sütunları temizleme
df_cleaned = df_onehot.drop(columns=['Backpack Height Ordinal', 'msd_risk_encoded'], errors='ignore')

# Güncellenmiş veri setinin ilk satırlarını görüntüleme
print(df_cleaned.head())
```

### Açıklama:
1. **MSD Risk Seviyesi:** Çanta yüksekliği kategorilerine göre ortalama MSD risk seviyeleri hesaplanır.
2. **Sıralı Kodlama vs. One-Hot Encoding:** Çanta yüksekliği için iki farklı kodlama yöntemi test edilerek One-Hot Encoding’in daha iyi sonuç verdiği gözlemlenir.
3. **Son İşlem:** Gereksiz sütunlar temizlenir ve veri seti analiz için hazır hale getirilir.

### Analizin Amacı:
- Çanta yüksekliği ile MSD risk seviyesi arasındaki ilişkiyi anlamak.
- Farklı kodlama yöntemlerini test ederek en uygun yöntemi seçmek.

### Ekran Görüntüsü Ekleyin:
- **Ortalama MSD risk seviyelerini gösteren tablo**.
- **One-Hot Encoding sonrası güncellenmiş veri setinin ekran görüntüsü**.

---

## 12. Gender ve MSD Risk için One-Hot Encoding

### Kod:
```python
# Gender ve MSD Risk için One-Hot Encoding uygulama
df_cleaned = pd.get_dummies(df_cleaned, columns=['Gender', 'msd_risk'], drop_first=False)

# Güncellenmiş veri setinin ilk birkaç satırını görüntüleme
print(df_cleaned.head())
```

### Açıklama:
- **Gender** ve **msd_risk** kategorik değişkenleri için One-Hot Encoding uygulanarak sayısal formatta temsili sağlanır.
- Bu işlem, modelin kategorik değişkenlerle daha iyi çalışmasını sağlar.

### Analizin Amacı:
- Cinsiyet ve MSD risk değişkenlerini modellerde kullanılabilir formata dönüştürmek.

### Ekran Görüntüsü Ekleyin:
- **Gender ve MSD Risk için One-Hot Encoding sonrası veri seti görüntüsü**.

---

## 13. MSD Risk ve Grafiksel Analizler

### Kod:
```python
# MSD Risk dağılımını analiz etme
sns.countplot(x='msd_risk', data=df)
plt.title("MSD Risk Distribution")
plt.xlabel("MSD Risk")
plt.ylabel("Count")
plt.show()

# MSD Risk - Çanta Ağırlığı Boxplot Grafiği
sns.boxplot(x='msd_risk', y='Backpack Weight', data=df)
plt.title("MSD Risk by Backpack Weight")
plt.xlabel("MSD Risk")
plt.ylabel("Backpack Weight")
plt.show()

# MSD Risk - Gender Grafiği
sns.countplot(x='msd_risk', hue='Gender', data=df)
plt.title("MSD Risk by Gender")
plt.xlabel("MSD Risk")
plt.ylabel("Count")
plt.legend(title="Gender")
plt.show()
```

### Açıklama:
1. **MSD Risk Dağılımı:** Her MSD risk seviyesindeki gözlem sayıları görselleştirilir.
2. **Boxplot Analizi:** MSD risk seviyelerine göre çanta ağırlığının dağılımı incelenir.
3. **Gender Karşılaştırması:** MSD risk seviyeleri, cinsiyete göre karşılaştırılır.

### Analizin Amacı:
- Hedef değişken olan MSD risk seviyelerinin dağılımını anlamak.
- Çanta ağırlığı ve cinsiyetin MSD risk üzerindeki etkilerini görselleştirmek.

### Ekran Görüntüsü Ekleyin:
- **MSD Risk dağılım grafiği**.
- **MSD Risk - Çanta Ağırlığı boxplot grafiği**.
- **MSD Risk - Gender karşılaştırma grafiği**.

---

## 14. Aykırı Değer Analizi

### Kod:
```python
# Numeric sütunlar için aykırı değer analizi
numeric_columns = df_cleaned.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_columns:
    Q1 = df_cleaned[col].quantile(0.25)
    Q3 = df_cleaned[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Aykırı değerleri kaldırma
    df_cleaned = df_cleaned[(df_cleaned[col] >= lower_bound) & (df_cleaned[col] <= upper_bound)]

print(f"Aykırı değerler kaldırıldı. Güncel veri seti boyutu: {df_cleaned.shape}")
```

### Açıklama:
- **IQR Yöntemi:** Her sayısal sütun için aykırı değerler alt ve üst sınırlarla belirlenir.
- Aykırı değerler, model performansını iyileştirmek için kaldırılır.

### Analizin Amacı:
- Veri setindeki uç değerlere bağlı hatalı model sonuçlarının önüne geçmek.

### Ekran Görüntüsü Ekleyin:
- **Aykırı değerlerin kaldırılmasından önce ve sonra veri seti boyutları**.

---

## 15. SMOTE ile Veri Dengesizliğini Giderme

### Kod:
```python
from imblearn.over_sampling import SMOTE

# SMOTE uygulama
X = df_cleaned.drop(columns=['msd_risk_High', 'msd_risk_Medium', 'msd_risk_Low'])
y = df_cleaned[['msd_risk_High', 'msd_risk_Medium', 'msd_risk_Low']]

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

print(f"Veri dengesizliği giderildi. Yeni veri seti boyutu: {X_resampled.shape}")
```

### Açıklama:
- **SMOTE:** Veri setindeki sınıf dengesizliğini gidererek, azınlık sınıflarının model üzerindeki etkisini artırır.

### Analizin Amacı:
- Modelin sınıf dengesizliğinden kaynaklanan yanlılıklarını ortadan kaldırmak.

### Ekran Görüntüsü Ekleyin:
- **SMOTE öncesi ve sonrası veri seti boyutları**.

---

## 16. Makine Öğrenmesi Modellerinin Eğitimi ve Değerlendirilmesi

### Kod:
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

# Modellerin tanımlanması
rf_model = RandomForestClassifier(random_state=42)
log_reg_model = LogisticRegression(max_iter=1000, random_state=42)
svm_model = SVC(random_state=42, probability=True)

# Modellerin saklanması
models = {
    'Random Forest': rf_model,
    'Logistic Regression': log_reg_model,
    'SVM': svm_model
}

# Sonuçları saklamak için bir dictionary
evaluation_results = {}

# Modelleri eğitme ve değerlendirme
for name, model in models.items():
    model.fit(X_resampled, y_resampled)
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y, y_pred, average='weighted')

    # Sonuçları saklama
    evaluation_results[name] = {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1
    }

    print(f"{name} için sınıflandırma raporu:")
    print(classification_report(y, y_pred, zero_division=0))

# Sonuçları yazdırma
print("\nModellerin Değerlendirme Sonuçları:")
for model, scores in evaluation_results.items():
    print(f"{model}:")
    for metric, value in scores.items():
        print(f"  {metric}: {value:.4f}")
```

### Açıklama:
1. **Modellerin Eğitimi:** Random Forest, Logistic Regression ve SVM algoritmaları kullanılarak veri seti üzerinde modeller eğitildi.
2. **Değerlendirme Metriği:** Her model için doğruluk (accuracy), kesinlik (precision), geri çağırma (recall) ve F1 skoru hesaplandı.
3. **Sonuçların Analizi:** Her model için sınıflandırma raporu ve metriğe dayalı performans sonuçları yazdırıldı.

### Analizin Amacı:
- Farklı makine öğrenmesi algoritmalarının performansını karşılaştırarak en iyi sonuç veren modeli belirlemek.
- Model performanslarını doğruluk, kesinlik, geri çağırma ve F1 skoru üzerinden değerlendirmek.

### Ekran Görüntüsü Ekleyin:
- **Sınıflandırma raporları ve metrik sonuçlarının yer aldığı ekran görüntüleri.**

---

## 17. Accuracyyi Artırma Yöntemleri

Makine öğrenmesi model performansını artırmak için aşağıdaki adımlar uygulanabilir:

1. **Özellik Mühendisliği:**
   - Daha anlamlı özellikler oluşturmak veya mevcut özellikleri yeniden işlemek.
   - Örneğin, çanta ağırlığı ve öğrencinin boyu gibi özelliklerden yeni oranlar hesaplanabilir.

2. **Aykırı Değerlerin Daha Detaylı İncelenmesi:**
   - Aykırı değerler model performansını düşürebilir. Bu nedenle, daha hassas yöntemlerle tespit edilip uygun şekilde işlenebilir.

3. **Hyperparameter Tuning:**
   - Modellerin hiperparametrelerini optimize ederek daha iyi sonuçlar elde edilebilir. Bunun için **GridSearchCV** veya **RandomizedSearchCV** gibi araçlar kullanılabilir.

4. **Daha Fazla Veri:**
   - Eğitim verisinin artırılması modelin genel başarısını yükseltebilir. Veri artırma (data augmentation) teknikleri veya yeni veri toplama seçenekleri değerlendirilebilir.

5. **Farklı Algoritmalar:**
   - Kullanılan algoritmalar dışında Gradient Boosting (XGBoost, LightGBM) gibi modeller denenebilir.

6. **Özellik Seçimi:**
   - Gereksiz özellikleri kaldırmak ve en anlamlı özellikleri seçmek için **Recursive Feature Elimination (RFE)** veya **Feature Importance** gibi yöntemler uygulanabilir.

7. **Daha Dengeli Sınıflar:**
   - SMOTE veya ADASYN gibi yöntemlerin etkinliği test edilebilir. Alternatif olarak, sınıf ağırlıklarını dengeleyen modeller kullanılabilir.

8. **Ensemble Modeller:**
   - Birden fazla modelin sonuçlarını birleştiren Ensemble yöntemleri (örneğin, Bagging, Boosting) ile daha iyi doğruluk elde edilebilir.

---

## 18. Web Scraping ile Veri Elde Etme Denemesi

### Açıklama:
Bu projede kullanılan veri setinden önce, kendi veri setimizi oluşturmayı denedik. Bunun için **Ebay Teknoloji Kategorisi** üzerinden ürün bilgilerini toplamak amacıyla web scraping teknikleri kullandık. Elde edilen veriye ulaşmak için : [Web Scraping ile elde edilen veri](https://docs.google.com/spreadsheets/d/1_RGWBIPvF_kEPm4sgnAMkHdoS0TmS7gD/edit?usp=drive_link&ouid=110655962960934133918&rtpof=true&sd=true)

- **Elde Edilen Veri:**
  - Ürün adı
  - Fiyat
  - Kargo Bilgisi 
  - Ürün açıklamaları
  - Yorum Sayısı ve Değerlendirme
  - Satıcı Puanı 

- **Karşılaşılan Zorluklar:**
  - Elde edilen veri, MSD risk tahmini gibi bir sınıflandırma problemi için uygun değildi.
  - Toplanan veri, eğitim verisi olarak kullanılamayacak kadar sınırlı ve dağınıktı.

### Neden Kullanılmadı?
- Elde edilen veri, bu projenin hedefleriyle doğrudan ilişkili değildi.
- Veri seti, makine öğrenmesi modellerinin ihtiyaç duyduğu çeşitlilik ve kalite standartlarını karşılamadı.

### Gelecekteki Kullanım:
Web scraping ile elde edilen veri, farklı projeler (örneğin, ürün fiyatlandırma veya kullanıcı davranışı analizi) için kullanılabilir.

---

## 19. Proje ve Kodun İşleyişi

### Açıklama:
Bu bölümde, proje boyunca kullanılan kodun ve adımların nasıl çalıştığını detaylı şekilde açıkladım. Ayrıca, bu açıklamalara bir video ekleyerek kullanıcıların projeyi daha iyi anlamasını sağlamayı planlıyorum.

### Video İçeriği:
- Veri yükleme ve ön işleme adımları.
- Grafiksel analizlerin nasıl yapıldığı ve sonuçların yorumlanması.
- Aykırı değer analizi ve sınıf dengesizliğinin giderilmesi.
- Makine öğrenmesi modellerinin eğitimi ve değerlendirilmesi.
- Accuracy, recall, precision, ve F1 score sonuçlarının karşılaştırılması.

### Video Ekleme:
Bu bölüme bir YouTube veya diğer platform üzerinden erişilebilecek bir video bağlantısı eklenebilir. Video, projenin kodlama adımlarını ve genel mantığını izleyicilere açıklamak için etkili bir araç olacaktır.

---




