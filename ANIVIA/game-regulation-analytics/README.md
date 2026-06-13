# Game Regulation Analytics

# ANIVIA: Dijital Oyun Ekosistemi Regülasyon ve Karar Destek Sistemi

Bu proje; dijital oyun ekosistemindeki psikososyal, finansal ve davranışsal riskleri yönetmek, yasal regülasyon süreçlerine ve ebeveyn denetim mekanizmalarına veri temelli bir analitik altyapı kazandırmak amacıyla geliştirilmiştir.

**Canlı Uygulama:** [ANIVIA Streamlit Arayüzü](https://anivia-game-regulation.streamlit.app/Oyuncu_Personalari)

---

## Projenin Amacı ve Kapsamı

Projenin temel amacı, oyun içeriklerindeki yapısal risk unsurlarını ve kullanıcı eğilimlerini gelişmiş makine öğrenmesi algoritmalarıyla modelleyerek karar vericiler (yasal otoriteler) ve ebeveynler için doğrulanmış bir rehber sunmaktır. Proje mimarisi üç temel analitik eksen üzerinde kurgulanmıştır:

* **Oyun Ekseni (Oyun Risk Radarı):** Steam, Epic Games gibi platformlardan derlenen oyunların tematik içerikleri (şiddet, korku, suç, yetişkin içerik vb.) **XGBoost Sınıflandırma Algoritması** ile taranarak güvenlik seviyelerine göre (Düşük, Orta, Yüksek Risk) ayrıştırılmaktadır. Bu eksendeki kısıtlama, yasaklama ve güvenlik seviyesi (Düşük, Orta, Yüksek Risk) kararları doğrudan Türkiye 7578 Sayılı Yeni Oyun Yasası yasal mevzuatına göre belirlenmektedir. Model tehlikeli oyunlar %85 (recall) oranında tahmin edebilir. 

* **Oyuncu Ekseni (Hibrit Model):** Kullanıcıların dürüst beyanları; niyet, finansal hacim ve psikososyal yıkım boyutlarına göre **K-Means Kümeleme** algoritmasıyla işlenerek 4 ana oyuncu personası keşfedilmiştir. Yeni kullanıcı girdileri, **Random Forest** modeliyle gerçek zamanlı olarak bu personalara sınıflandırılmaktadır.

* **Veli Ekseni (Skorlama ve Segmentasyon):** Ebeveynlerin arabuluculuk yaklaşımları, akademik literatürdeki faktör yükleriyle ağırlıklandırılarak 100 üzerinden bir *Ebeveyn Denetim Skoru* üretmekte ve dijital okuryazarlık seviyelerini segmentlere ayırmaktadır.

---

## Kurulum ve Çalıştırma

```bash
# Projeyi yerel ortamınıza klonlayın
git clone https://github.com/betultgumus/ybs-makine-ogrenmesi.git

# Proje dizinine geçiş yapın
cd ybs-makine-ogrenmesi/ANIVIA/game-regulation-analytics

# Gerekli bağımlılıkları yükleyin
pip install -r requirements.txt

# Streamlit uygulamasını yerelde başlatın
streamlit run app.py

```
