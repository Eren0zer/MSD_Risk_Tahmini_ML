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

