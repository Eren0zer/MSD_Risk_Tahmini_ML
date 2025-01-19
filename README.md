# Veri Analizi ve Makine Öğrenmesi Projesi

Bu proje, öğrencilerde kas-iskelet sistemi bozuklukları riskini tahmin etmeyi amaçlamaktadır. Kullanılan veri seti, Kaggle'da [Musculoskeletal Disorders Risk in Students](https://www.kaggle.com/datasets/mrhmnshu/musculoskeletal-disorders-risk-in-students) başlığı altında erişilebilir.
> "Bu bölümde yer alan kodlar, projeyi genel olarak açıklamak için sembolik olarak sunulmuştur. Asıl kodlar ve detaylı uygulama dosya içerisinde bulunmaktadır. README'deki açıklama sırası, dosyada bulunan kodların sırasıyla birebir uyumludur. Proje adımlarını takip etmek için README ile kod dosyalarını kolayca eşleştirebilirsiniz."
---

## İçindekiler

1. [Proje Hedefi](#1-proje-hedefi)
2. [Veri Seti Özeti](#2-veri-seti-özeti)
3. [Veri Yükleme ve Görüntüleme](#3-veri-yükleme-ve-görüntüleme)
4. [Histogramlarla Veriyi Görselleştirme](#4-histogramlarla-veriyi-görselleştirme)
5. [Veri Setinin Yapısını Anlama](#5-veri-setinin-yapısını-anlama)
6. [Korelasyon Matrisi](#6-korelasyon-matrisi)
7. [Eksik Değer Analizi ve Özet İstatistikler](#7-eksik-değer-analizi-ve-özet-istatistikler)
8. [Kategorik Değişkenlerin İncelenmesi](#8-kategorik-değişkenlerin-incelenmesi)
9. [MSD Riskinin İncelenmesi](#9-msd-riskinin-incelenmesi)
10. [Cinsiyet Dağılımı](#10-cinsiyet-dağılımı)
11. [Box Plot ile Değişkenlerin İncelenmesi](#11-box-plot-ile-değişkenlerin-incelenmesi)
12. [Çanta Yüksekliği ve MSD Risk Analizi](#12-çanta-yüksekliği-ve-msd-risk-analizi)
13. [Gender ve MSD Risk için One-Hot Encoding](#13-gender-ve-msd-risk-için-one-hot-encoding)
14. [MSD Risk ve Grafiksel Analizler](#14-msd-risk-ve-grafiksel-analizler)
15. [Aykırı Değer Analizi](#15-aykırı-değer-analizi)
16. [SMOTE ile Veri Dengesizliğini Giderme](#16-smote-ile-veri-dengesizliğini-giderme)
17. [Makine Öğrenmesi Modellerinin Eğitimi ve Değerlendirilmesi](#17-makine-öğrenmesi-modellerinin-eğitimi-ve-değerlendirilmesi)
18. [Accuracyyi Artırma Yöntemleri](#18-accuracyyi-artirma-yöntemleri)
19. [Web Scraping ile Veri Elde Etme Denemesi](#19-web-scraping-ile-veri-elde-etme-denemesi)
20. [Proje ve Kodun İşleyişi Hakkında Video](#20-proje-ve-kodun-işleyişi-hakkında-video)
    
---

## 1. Proje Hedefi

Bu projenin amacı:

- Öğrencilerde **kas-iskelet sistemi bozuklukları riskini** (MSD riski) tahmin etmek,
- Veri temizleme, görselleştirme ve analizi gerçekleştirmek,
- Sınıf dengesizliği problemini çözmek,
- Çoklu etiketli sınıflandırma algoritmalarını kullanarak doğruluk skorlarını karşılaştırmaktır.

---

## 2. Veri Seti Özeti

Veri setimiz, öğrencilerde kas-iskelet sistemi bozuklukları riskini analiz etmek için kullanılmıştır. Aşağıda veri setindeki sütunlar ve bu sütunların açıklamaları bulunmaktadır:

| **Sütun Adı**         | **Veri Tipi** | **Açıklama**                                                                               |
|------------------------|---------------|-------------------------------------------------------------------------------------------|
| `Gender`              | Kategorik     | Öğrencinin cinsiyeti (`Male`, `Female`).                                                  |
| `Age`                 | Sayısal       | Öğrencinin yaşı.                                                                          |
| `Height`              | Sayısal       | Öğrencinin boyu (santimetre cinsinden).                                                   |
| `Weight`              | Sayısal       | Öğrencinin kilosu (kilogram cinsinden).                                                   |
| `Backpack Weight`     | Sayısal       | Öğrencinin taşıdığı çantanın ağırlığı (kilogram cinsinden).                               |
| `Backpack Height`     | Kategorik     | Çantanın öğrencinin vücudundaki konumu (`Shoulder Blades to Lower Back`, `On Buttocks`). |
| `Sitting Hours`       | Sayısal       | Öğrencinin gün içerisinde oturarak geçirdiği saat miktarı.                                |
| `Physical Activity`   | Kategorik     | Öğrencinin fiziksel aktivite seviyesi (`Low`, `Medium`, `High`).                         |
| `msd_risk`            | Kategorik     | Öğrencideki kas-iskelet sistemi bozuklukları riski (`Low`, `Medium`, `High`).            |

### Açıklama:
1. **Gender:** Cinsiyet bilgisi, model için kategorik bir değişkendir.
2. **Age, Height, Weight:** Öğrencilerin fiziksel özelliklerini yansıtan sayısal değişkenlerdir.
3. **Backpack Weight ve Backpack Height:** Çantanın ağırlığı ve vücuttaki konumu, MSD riskini etkileyebilecek önemli faktörlerdir.
4. **Sitting Hours:** Uzun süreli oturma, kas-iskelet sistemi bozuklukları riskini artırabileceği için bu sütun önemlidir.
5. **Physical Activity:** Fiziksel aktivite seviyesi, MSD riskini azaltabilecek önemli bir etkendir.
6. **msd_risk:** Bu veri setindeki hedef değişken, öğrencinin MSD riski sınıfını temsil eder (`Low`, `Medium`, `High`).

---

## 3. Veri Yükleme ve Görüntüleme

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

### Ekran Görüntüsü: 

![Veri seti](https://github.com/user-attachments/assets/15075ecc-0a25-4fc1-a9b4-71db6568cc80)

---

## 4. Histogramlarla Veriyi Görselleştirme

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

### Ekran Görüntüsü:
| ![Image 1](https://github.com/user-attachments/assets/d9467630-1605-4b24-9a2c-b8b03dd0b391) | ![Image 2](https://github.com/user-attachments/assets/081ef6e3-0a8b-448b-bef9-82d086272a8b) | ![Image 3](https://github.com/user-attachments/assets/22135065-1441-47ac-b38f-c69c067c4662) |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|

| ![Image 4](https://github.com/user-attachments/assets/a2c23bc3-c4e3-4fa2-8fa8-421c35e6da1b) | ![Image 5](https://github.com/user-attachments/assets/37ce5f40-782a-4aee-b50d-13947ca7d834) | ![Image 6](https://github.com/user-attachments/assets/93c9ec42-f4d1-4846-9315-2503cd5f35e5) |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|

| ![Image 7](https://github.com/user-attachments/assets/9972aa7d-13ac-4cf1-8d9e-d3bbee716042) | ![Image 8](https://github.com/user-attachments/assets/7516020f-0358-4643-91fd-8172f7762dcb) | ![Image 9](https://github.com/user-attachments/assets/4e03e874-555d-4efe-9480-4dcae1da12c2) |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|

| ![Image 10](https://github.com/user-attachments/assets/083d1643-f9dd-4ed2-8401-3eda534c39e2) |
|:-------------------------------------------------------------------------------------------:|



---

## 5. Veri Setinin Yapısını Anlama

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
1. Veri setinin satır ve sütun sayısı hesaplanarak genel boyut hakkında bilgi sağlanır. Bu veri setimizin 10000 satır 13 sutün olduğunu görüyoruz.
2. Her bir sütunun veri türü incelenir (örneğin, float, int, object).

### Analizin Amacı:
- Veri setinin genel yapısını anlamak ve hangi türde veriler içerdiğini belirlemek.

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/06a7bcf2-88fb-4201-b6b7-e70d958d2d60) |
|:-------------------------------------------------------------------------------------------:|
---

## 6. Korelasyon Matrisi

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

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/dd036c01-5c5d-4ac5-a8f9-b3f26922d281) |
|:-------------------------------------------------------------------------------------------:|

---

## 7. Eksik Değer Analizi ve Özet İstatistikler

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

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/ed6611e4-0ed8-49ea-ab3b-6b1919e226a8) | ![Image](https://github.com/user-attachments/assets/ece9ebbe-1a15-4cc0-9dbb-d0332d2ea599) |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|



---

## 8. Kategorik Değişkenlerin İncelenmesi

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

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/c2fe851e-4deb-4b12-a7be-5ec03836a098) | ![Image](https://github.com/user-attachments/assets/4a315439-e9cd-4b94-af8f-c8e80319f634) |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|

---

## 9. MSD Riskinin İncelenmesi

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

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/d620f018-9b35-4076-a82c-55e769a1a740) |
|:-------------------------------------------------------------------------------------------:|

---

## 10. Cinsiyet Dağılımı

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

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/cd13cfec-5247-459f-923d-2d1c5ac45af9) |
|:-------------------------------------------------------------------------------------------:|

---

## 11. Box Plot ile Değişkenlerin İncelenmesi

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

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/8030234f-026b-4a36-97a6-2d50f534b195) | ![Image](https://github.com/user-attachments/assets/48b6b0d7-6011-42f5-bbc2-5e9ab8641b90) | ![Image](https://github.com/user-attachments/assets/a58eb618-6a39-47d6-8f3b-023e6c654919) |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|
| ![Image](https://github.com/user-attachments/assets/80db05df-5f46-40bc-afff-5527c16689bf) | ![Image](https://github.com/user-attachments/assets/8ed4de1e-6d38-4821-8b08-abd7255a01ae) | ![Image](https://github.com/user-attachments/assets/65bf5fd6-c049-4862-88ac-5276a109039f) |
| ![Image](https://github.com/user-attachments/assets/c35440fa-6156-45f4-8f4f-50630edf7d84) | ![Image](https://github.com/user-attachments/assets/c7c31755-e881-4eae-8285-fea99607f5cc) | ![Image](https://github.com/user-attachments/assets/5bc32b3f-8a59-4a61-b197-3d10fdeb4385) |
| ![Image](https://github.com/user-attachments/assets/0547636c-ce2f-4462-9504-0b09c01ba323) |                                                                                           |                                                                                           |
### Analiz:
- Thoracic Deviation ve Lumbar Deviation değişkenlerinde aykırı değerler tespit edilmiştir. Bu aykırı değerlerin etkisi, veri analizi sırasında incelenmeli ve gerektiğinde çıkarılmalıdır.
- Diğer değişkenler normal bir dağılım sergilemektedir ve medyan değerler genel dağılımın ortasında yer almaktadır.
- Çocuk yaşı ve boyu gibi değişkenlerin dar bir aralığı kapsadığı görülüyor. Bu, veri setinin odaklandığı yaş grubuyla uyumludur.
- Aykırı değerlerin modellenmesi ve sınıflandırma işlemleri üzerindeki etkisi SMOTE ve diğer veri işleme teknikleriyle dengelenebilir.

---

## 12. Çanta Yüksekliği ve MSD Risk Analizi

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
2. **Sıralı Kodlama vs. One-Hot Encoding:** Çanta yüksekliği için iki farklı kodlama yöntemi test edilir. Sıralı kodlama 0.354 değerini verirken, One-Hot Encoding 0.367 değerini verir. One-Hot Encoding daha iyi sonuç verdiği gözlemlenir.
3. **Son İşlem:** Gereksiz sütunlar temizlenir ve veri seti analiz için hazır hale getirilir.

### Analizin Amacı:
- Çanta yüksekliği ile MSD risk seviyesi arasındaki ilişkiyi anlamak.
- Farklı kodlama yöntemlerini test ederek en uygun yöntemi seçmek.

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/7bb5b136-edd2-46b7-949b-73ac0794007e) | ![Image](https://github.com/user-attachments/assets/45d46ac5-5c81-4381-bc9c-bfade54686f1) |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|


---

## 13. Gender ve MSD Risk için One-Hot Encoding

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

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/78e04765-08d2-4281-9cc3-91d2a9894696) | ![Image](https://github.com/user-attachments/assets/212788b0-0814-48ff-916a-b0589f3741a5) |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|


---

## 14. MSD Risk ve Grafiksel Analizler

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

### Ekran Görüntüsü:
| ![Image](https://github.com/user-attachments/assets/8d5a9259-b7aa-45c0-a1e8-d92877bf93ca) | ![Image](https://github.com/user-attachments/assets/43111ca7-3556-4e05-9023-152e79e0630c) | ![Image](https://github.com/user-attachments/assets/e0505b58-52af-488b-be10-f7383de07d24) |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|

### Analiz:
- Veri setinde düşük risk seviyesi baskındır, ancak risk seviyeleri arasında çok büyük bir dengesizlik görülmemektedir. Bu durum, modelin sınıflandırma sırasında her sınıfa eşit önem verebilmesi için bir avantajdır.
- Çanta ağırlığının, MSD risk seviyeleri üzerinde önemli bir ayrıştırıcı özellik olmadığını söyleyebiliriz.
- Grafikler, cinsiyet değişkeninin farklı risk seviyelerinde belirleyici bir rol oynayabileceğini göstermektedir. Bu nedenle, cinsiyet özelliği modellerde mutlaka kullanılmalıdır.
---

## 15. Aykırı Değer Analizi

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

### Ekran Görüntüsü:

| ![Image](https://github.com/user-attachments/assets/6dab06e8-4bf7-4287-9547-1bb200b7ce5c) |
|:-------------------------------------------------------------------------------------------:|

---

## 16. SMOTE ile Veri Dengesizliğini Giderme

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

---

## 17. Makine Öğrenmesi Modellerinin Eğitimi ve Değerlendirilmesi

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

### Ekran Görüntüsü:
| ![Image](https://github.com/user-attachments/assets/5dfeb486-a7d1-4894-b317-c148e3fdbf7f) | ![Image](https://github.com/user-attachments/assets/1982024f-be3b-4be1-b9eb-8e735675d8ba) | ![Image](https://github.com/user-attachments/assets/69e3cbf3-77d1-48c6-b437-976760a52ee6) |
|:------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------:|
| **Support Vector Machine (SVM)**                                                                           | **Random Forest**                                                                    | **Logistic Regression**                                                          |

### 1. Random Forest

#### Avantajlar:
- **Dengeli Performans**: Random Forest, tüm etiketler için dengeli bir performans göstermektedir.
- **Düşük Risk Doğruluğu**: Özellikle düşük MSD risk seviyelerinde daha iyi bir doğruluk oranı sunar.

#### Dezavantajlar:
- **Orta Risk Hataları**: Medium risk seviyesi için hatalı tahmin oranı görece yüksektir.

---

### 2. Lojistik Regresyon

#### Avantajlar:
- **Hızlı Performans**: Basit yapısı sayesinde veri setinde hızlı çalışmaktadır.
- **Orta Risk İçin Yüksek Geri Çağırma**: Medium risk seviyesi için geri çağırma oranı yüksektir.

#### Dezavantajlar:
- **Precision Düşüklüğü**: High ve Low risk seviyeleri için precision düşüktür.
- **Dengesiz Performans**: Etiketler arası performans farklılıkları bulunmaktadır.

---

### 3. SVM

#### Avantajlar:
- **Low Risk İçin En Yüksek Precision**: Low risk seviyesi için en iyi precision değerini sağlar.
- **Ayrım Yeteneği**: Farklı sınıfların ayrıcı çizgisini belirlemede başarılıdır.

#### Dezavantajlar:
- **Orta Risk F1 Skoru**: Medium risk seviyesi için düşük bir F1 skoru bulunmaktadır.
- **Hesaplama Maliyeti**: Diğer algoritmalara göre hesaplama süresi daha uzun olabilir.

---

### 4. Karşılaştırmalı Sonuçlar

#### Doğruluk (Accuracy):
- Random Forest en yüksek doğruluk oranına sahiptir (0.685).
- Lojistik Regresyon ve SVM, doğruluk açısından benzer sonuçlar göstermiştir (0.667).

#### F1-Score:
- Random Forest, F1-Score açısından en iyi sonuçları vermektedir. Bu, dengesiz veri setlerinde daha güvenilir tahminler yaptığını gösterir.

#### Sınıf Dengesizliği:
- Tüm algoritmalar, düşük risk seviyelerinde daha iyi sonuçlar verirken, Medium risk seviyesinde genellikle düşük performans sergilemiştir. Bu, veri setindeki sınıf dengesizliğinden kaynaklanıyor olabilir.

#### Uygun Algoritma Seçimi:
- Eğer Medium risk seviyesi için tahminler daha kritikse, Lojistik Regresyon tercih edilebilir.
- Daha dengeli bir performans için Random Forest önerilir.
- Sınıf ayrımı daha belirgin olan veri setlerinde SVM daha iyi performans gösterebilir.

---

## 18. Accuracyyi Artırma Yöntemleri

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

## 19. Web Scraping ile Veri Elde Etme Denemesi

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

## 20. Proje ve Kodun İşleyişi Hakkında Video

### Açıklama:
Bu bölümde, proje boyunca kullanılan kodun ve adımların nasıl çalıştığını detaylı şekilde açıkladım. Ayrıca, bu açıklamalara bir video ekleyerek kullanıcıların projeyi daha iyi anlamasını sağlamayı planlıyorum.

### Video İçeriği:
- Veri yükleme ve ön işleme adımları.
- Grafiksel analizlerin nasıl yapıldığı ve sonuçların yorumlanması.
- Aykırı değer analizi ve sınıf dengesizliğinin giderilmesi.
- Makine öğrenmesi modellerinin eğitimi ve değerlendirilmesi.
- Accuracy, recall, precision, ve F1 score sonuçlarının karşılaştırılması.

### Video:
Bu bölüme bir YouTube veya diğer platform üzerinden erişilebilecek bir video bağlantısı eklenebilir. Video, projenin kodlama adımlarını ve genel mantığını izleyicilere açıklamak için etkili bir araç olacaktır.

---




