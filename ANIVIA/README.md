# ANIVIA - Cross-Platform Oyun Fiyat Tahminleme ve Veri Madenciliği

![ANIVIA](https://img.shields.io/badge/Project-ANIVIA-blue) ![Python](https://img.shields.io/badge/Python-3.8%2B-green) ![DataScience](https://img.shields.io/badge/DataScience-ML-orange)

---

## 📋 Proje Özeti (Executive Summary)

**ANIVIA**, çok platformlu video oyunlarının fiyatlarını tahmin etmek için makine öğrenmesi ve veri madenciliği tekniklerini kullanan kapsamlı bir veri analizi projesidir. 

Proje, **Steam**, **Epic Games**, **PlayStation Store**, **Nintendo Store** ve **Xbox Store** gibi 5 farklı dijital oyun dağıtım platformundan toplanan ve standardize edilen ~20,000 oyun verisiyle çalışır. 

### 🎯 Proje Hedefleri:
- ✅ Oyun fiyatları üzerinde etkili olan faktörleri tanımlamak
- ✅ Platform ve cihaz türüne göre fiyat dalgalanmalarını analiz etmek
- ✅ Makine öğrenmesi modeli ile fiyat tahmini yapmak
- ✅ Oyun geliştirici ve yayınlayıcılar için fiyatlandırma stratejileri sunmak

### 📊 Veri Seti Özellikleri:
| Özellik | Değer |
|---------|-------|
| **Toplam Kayıt** | ~19,936 oyun |
| **Aktif Kolon** | 11 değişken |
| **Platform Sayısı** | 5 (Steam, Epic, PlayStation, Nintendo, Xbox) |
| **Hedef Değişken** | Fiyat (USD) |
| **Veri Kalitesi** | %92+ eksiksiz |

---

## 1. Veri Toplama Metodolojisi (Data Acquisition)

### 📡 Kaynaklar ve Yöntemler

Veriler, aşağıdaki platformlardan **Web Scraping** teknikleri kullanılarak dinamik olarak toplanmıştır:

#### **Web Scraping Teknolojileri:**
- **BeautifulSoup**: Statik HTML sayfaların parse edilmesi
- **Selenium**: JavaScript ile dinamik yüklenen sayfaların otomasyonu
- **Requests**: HTTP istek gönderimleri

#### **Platform Özellikleri:**

| Platform | Veri Kaynağı | Öğe Sayısı | Para Birimi | Not |
|----------|--------------|-----------|------------|-----|
| **Steam** | store.steampowered.com | 9,847 | TRY | PC oyunları |
| **Epic Games** | epicgames.com/store | 2,156 | TRY | PC oyunları |
| **PlayStation** | store.playstation.com | 5,432 | TRY | PS4/PS5 |
| **Nintendo** | eshop.nintendo.com | 2,301 | USD | Switch |
| **Xbox** | microsoft.com/store | 200 (kısmi) | USD | Xbox One/Series |

### 🔧 Veri Filtreleme Kriterleri:

1. **Kampanya Hariçtir**: Sadece **liste fiyatları** (indirim yapılmamış) alınmıştır
2. **Güncel Veriler**: Web scraping tarihi itibariyle aktif ürünler

---

## 2. Veri Hazırlama ve Ön İşleme (Data Preprocessing)

### 📐 Normalizasyon ve Standardizasyon

#### **Para Birimi Dönüşümü:**
```
Dönüşüm Kuru (Global Rate): 1 USD = 44.52 TRY (Proje tarihi itibariyle)

Örnek:
- PlayStation (TRY): 299 ₺  → 299 ÷ 44.52 = 6.71 USD ✓
- Nintendo (USD): 49.99 USD → 49.99 USD ✓
```

#### **Sütun Adlarının Standardizasyonu:**
```python
# Farklı platformlardan gelen sütun adları
Steam:       'oyun_adı', 'oyun_turu', 'fiyat', 'puan'
Epic:        'Oyun Adı', 'Oyun Türü', 'Fiyat', 'Puan'
PlayStation: 'oyun_adi', 'oyun_turu', 'Fiyat', 'Puan'
Nintendo:    'Oyun Adı', 'Türler', 'Fiyat_Sayisal', 'Metacritic'

# Sonuç: Tek standart DataFrame yapısında birleştirildi
Ortak Sütunlar: 
  ['oyun_adi', 'oyun_turu', 'gelistirici', 'puan', 
   'turkce_destegi', 'fiyat', 'yas', 'dil', 
   'ingilizce_destegi', 'dil_sayisi', 'platform']
```

### 🏗️ Özellik Mühendisliği (Feature Engineering)

Modelin açıklayıcılık gücünü artırmak için yeni değişkenler türetilmiştir:

| Yeni Özellik | Türetilme Yöntemi | Örnek |
|--------------|------------------|-------|
| **cihaz_turu** | Platform analizi | PC, Konsol, PC+Konsol |
| **dil_sayisi** | Dil listesi parsing | "English, Turkish, German" → 3 |
| **turkce_destegi** | String matching | Dil listesinde "Türkçe" varsa → 1 |
| **ingilizce_destegi** | String matching | Dil listesinde "English" varsa → 1 |
| **oyun_turu_sayisi** | Tag/kategori hesaplama | "Action, Adventure" → 2 |
| **puan_durumu** | Kategorisizasyon | Düşük/Orta/Yüksek/Değerlendirmeme |

---

## 3. Veri Kalitesi Raporu ve Eksik Veri Stratejisi

### 📊 Eksik Veri Analizi

Veri seti 19,936 kayıt ve 11 sütundan oluşmaktadır. Eksik veriler strategik olarak ele alınmıştır:

| Sütun | Eksik (%) | Strateji | Sonuç |
|-------|-----------|----------|-------|
| **oyun_adi** | 0.03% | Satır sil | Konu yok |
| **oyun_turu** | 1.34% | "Bilinmiyor" yaz | Kapsülle |
| **gelistirici** | 35.3% | Platform bazlı impute | Bilinmiyor_PC/Konsol |
| **puan** | 47.9% | Yeni kategori oluştur | "Değerlendirilmemiş/Yeni" |
| **fiyat** | 7.1% | Platform medyanı ile impute | Güvenilir tahmin |
| **yas** | 5.3% | Oyun türü mod'u ile impute | Yaş kategorisi tahmin |
| **dil** | 31.4% | "English" (global default) | Sektörün ana dili |
| **dil_sayisi** | 0.6% | Dilden hesapla | Sayısal |

---

## 4. Keşifçi Veri Analizi (EDA) ve Görselleştirmeler

### 📈 Tekli Değişken Analizi

#### **Fiyat Dağılımı**
- **İstatistikler:** Min: $0 | Q1: $4.99 | Medyan: $9.99 | Q3: $19.99 | Max: $99.99
- **Şekli:** Sağa çarpık (right-skewed) - çoğunluk düşük fiyatlıdır
- **Aykırı Değerler:** IQR yöntemiyle 324 aykırı değer tespit edildi

#### **Dil Sayısı Dağılımı**
- **Ortalama:** 2.3 dil/oyun
- **Medyan:** 2 dil
- **Sınırlar:** Minimum 1, Maksimum 40+

#### **Platform Dağılımı**
- PlayStation: 5,432 oyun (27.8%)
- Steam: 9,847 oyun (50.3%)
- Epic Games: 2,156 oyun (11.0%)
- Nintendo: 2,301 oyun (11.8%)
- Xbox: 200 oyun (1.0%, kısmi veri)

### 🔗 İkili Değişken Analizi

#### **Platform - Fiyat İlişkisi**

**Bulgular:**
- **Nintendo** oyunları en pahalı (Medyan: $39.99)
- **PlayStation** oyunları orta segment (Medyan: $14.99)
- **Steam & Epic** oyunları daha ucuz (Medyan: $9.99-$12.99)

#### **Yaş Grubu - Fiyat İlişkisi**

| Yaş Grubu | Medyan Fiyat | Oyun Sayısı |
|-----------|-------------|------------|
| **3** | $4.99 | 3,200 |
| **10** | $14.99 | 2,100 |
| **12** | $19.99 | 3,450 |
| **18** | $12.99 | 8,829 |

**Anahtar Bulgu:** Yaş grubu arttıkça fiyat da artmakta (korelasyon: 0.27)

#### **Dil Desteği Analizi**

- **Türkçe Desteği:** Negatif korelasyon (-0.13) - Türkçe oyunlar daha düşük fiyatlı
- **İngilizce Desteği:** Pozitif korelasyon (0.14) - İngilizce oyunlar daha pahalı
- **Dil Sayısı:** Pozitif korelasyon (0.18) - Çok dilli oyunlar daha pahalı

#### **Korelasyon Analizi**

| Değişken Çifti | Korelasyon | Yorum |
|----------------|-----------|-------|
| **fiyat ↔ puan** | 0.31 | Kalite arttıkça fiyat artar |
| **fiyat ↔ yas** | 0.27 | Yaş grubu yükseldikçe fiyat artar |
| **fiyat ↔ oyun_turu_sayisi** | -0.22 | Çok türlü oyunlar daha ucuz |
| **fiyat ↔ ingilizce_destegi** | 0.14 | Global oyunlar daha pahalı |

---

## 5. Model Başarı Değerlendirmesi

### 🤖 Kullanılan Algoritmalar

#### **Şampiyon Model: XGBoost Regressor (Hiperparametre Optimizasyonu)**

**En İyi Parametreler:**
```python
n_estimators: 500
max_depth: 9
learning_rate: 0.01
subsample: 0.7
colsample_bytree: 0.8
```

### 📊 Model Performans Metrikleri

| Metrik | Train | Test | Açıklama |
|--------|-------|------|----------|
| **R² Skoru** | 0.62 | 0.58 | Model, varyansın %62'sini açıklıyor |


### 🎯 Özellik Önemi (Feature Importance - Top 10)

| Sıra | Özellik | 
|-----|---------|
| 1 | **platform_nintendo** | 
| 2 | **platform_ps** | 
| 3 | **cihaz_turu_pc** | 
| 4 | **tek_oyunculu** | 
| 5 | **platform_steam** | 
| 6 | **ingilizce_destegi** | 

---

## 6. Sonuç ve İş Bulguları

### 🎯 İş Stratejileri Önerileri

#### **Geliştiriciler için:**
1. **Platformları Seçici Kullan**: Nintendo exclusive'leri premium fiyatlandırsın
2. **Kaliteyi Vurgula**: Puanlanan oyunlarda daha yüksek.
3. **Dil Desteği Dengele**: Daha fazla dil = daha geniş pazaar ama fiyat düşme riski
4. **Yaş Grubu Odaklı**: +18 gibi oyunlarda sunulan fiyat daha yüksek.

#### **Yayınlayıcılar için:**
1. **Portföy Risk Yönetimi**: Konsol yarışması daha kârlı ama riskli
2. **Indie Aksesibilitesi**: Steam indie'ler büyük hacim ancak düşük margin
3. **Segmentasyon**: Her tür için farklı fiyatlandırma stratejisi gerekli

---
---

**© 2026 ANIVIA Projesi | Tüm Hakları Saklıdır**


