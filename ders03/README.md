
# Telco Customer Churn — Müşteri Kayıp Analizi

Bir telekomünikasyon şirketinin 7.043 müşterisine ait verinin keşifsel veri analizi (EDA) ile incelenmesi. Müşteri kaybı (Churn) olgusunun ~%26.5 oranında görülmesi temelinde risk faktörlerinin tanımlanması.

---

## İçerik Özeti

### **Adım 1: Kütüphaneleri İçe Aktarma**
- Temel araçlar: pandas, numpy, matplotlib, seaborn, plotly
- Görselleştirme ve veri manipülasyonu için gerekli yapılandırmalar

### **Adım 2: Veriyi Yükleme ve İlk İnceleme**
- CSV dosyasından 7.043 müşteri kaydını pandas DataFrame'e yükleme
- `head()`, `tail()`, `sample()` ile ilk bakış
- Veri seti: 21 değişken, ~26.5% churn oranı

### **Adım 3: Veri Yapısı ve Temel Bilgiler**
- Veri tipleri inceleme (int64, float64, object)
- `df.info()` ve `df.describe()` ile istatistiksel özet
- TotalCharges sütununun veri tipi anomalisi tespiti

### **Adım 4: Değişken Sözlüğü ve Sınıflandırma**
- Demografik değişkenler (yaş, cinsiyet, hane halkı)
- Hizmet değişkenleri (internet, güvenlik, destek)
- Finansal değişkenler (aylık ücreti, toplam ücret)
- Hedef değişken (Churn)

### **Adım 5-10: Derinlemesine Analiz**
- Eksik değerlerin tespiti ve yönetimi
- Aykırı değer (outlier) analizi ve görselleştirmesi
- Kategorik ve sayısal değişkenlerin dağılımları
- Churn ile değişken ilişkileri
- Korelasyon matrisi ve ısı haritası
- İstatistiksel testler (chi-square, t-test vb.)

---

## Ana Bulgular

- **Müşteri Segmentasyonu**: Yaş, cinsiyet, sözleşme türüne göre churn farklılaşmaktadır
- **Finansal İlişki**: Aylık ücret ve sözleşme süresi churn'ü etkilemektedir
- **Hizmet Etkisi**: İnternet türü ve ek hizmetler (güvenlik, destek) müşteri tutumunda rol oynamaktadır
- **Sözleşme Türü**: Aylık sözleşmelerde yıllık sözleşmelere kıyasla daha yüksek churn görülmektedir

---

## Kullanılan Araçlar
- **Kütüphaneler**: pandas, numpy, matplotlib, seaborn, plotly
- **Yöntemler**: Tanımlayıcı istatistik, görselleştirme, korelasyon, t-test, chi-square testi

---

## Dosya
- `telco-workshop.ipynb`
- `Telco-Customer-Churn.csv`

