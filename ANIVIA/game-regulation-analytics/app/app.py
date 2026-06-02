import streamlit as st
import os
from utils import lokal_css_yukle, logo_koy

st.set_page_config(page_title="ANIVIA Game Insight", layout="wide")

# CSS ve Logo yükle
lokal_css_yukle()
logo_koy()

# Logo ve Başlıkları yan yana göster
col1, col2 = st.columns([1, 4])

with col1:
    logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
    st.image(logo_path, width=180)

with col2:
    st.markdown('<h1 class="main-title">ANIVIA GAME INSIGHT</h1>', unsafe_allow_html=True)
    st.title("Game Regulation Analytics")

st.markdown("""
<div style="background-color: #E0F2FE; border: 4px solid #D4AF37; padding: 20px; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); margin-bottom: 20px; border-radius: 8px;">
  <h3 style="text-align: center; font-family: 'Press Start 2P', cursive; font-size: 18px; color: #1E3A8A; margin: 0 0 0 0; border: none; background-color: transparent; padding: 0; box-shadow: none;">🎯 Proje Hakkında Genel Bakış</h3>
  <hr style="border: 0; border-top: 1px solid #D4AF37; margin: 12px 0;">
  <p style="font-family: 'Segoe UI', Arial, sans-serif; font-size: 16px; font-weight: 500; text-align: left; color: #1E3A8A; line-height: 1.8; margin: 0;">
    <strong>Anivia Game Insight</strong>, dijital oyun ekosistemindeki regülasyon ihtiyacını, oyuncu davranışlarını ve ebeveyn farkındalığını veri bilimi ve makine öğrenmesi metodolojileriyle ele alan kapsamlı bir <strong>Game Regulation Analytics</strong> projesidir. Projemiz, ham oyun verilerinden veli algısına kadar uzanan geniş bir yelpazeyi <strong>3 temel analitik aşamada</strong> inceler.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🧭 Sol Menü (Sidebar) ve Proje Aşamaları Kılavuzu

Sol taraftaki menüyü kullanarak projemizin şu 3 ana modülü arasında geçiş yapabilirsiniz:

1. 🔮 **Oyun Risk Radarı (Makine Öğrenmesi Tahmin Motoru)**
   - **Ne İşe Yarar?:** Geliştirdiğimiz **XGBoost** makine öğrenmesi modelini temel alır. Kullanıcı tarafından girilen platform, kategori ve yaş sınırı (PEGI) gibi parametreleri anlık olarak işleyerek oyunun çocuklar için risk durumunu dinamik olarak tahmin eder.
   - **Amacı:** Dijital marketlerdeki oyunların regülasyon standartlarına uygunluğunu yapay zeka ile denetlemek.

2. 📊 **Oyuncu Personaları (Gözetimsiz Öğrenme ve Kümeleme)**
   - **Ne İşe Yarar?:** Oyun endüstrisi datasetleri üzerinde uygulanan gelişmiş veri analitiği ve kümeleme (Clustering) algoritmalarını içerir. Oyuncuların harcama, oynama süresi ve davranış kalıplarını analiz ederek stratejik oyuncu segmentleri oluşturur.
   - **Amacı:** Kitlesel oyun verilerini anlamlandırarak sektörel tüketici profillerini (personaları) ortaya çıkarmak.

3. 👥 **Veli Algısı (Anket ve Sosyal Algı Analizi)**
   - **Ne İşe Yarar?:** Ebeveynlerin dijital oyun dünyasına bakış açılarını, çocuklarının oyun alışkanlıklarına yönelik farkındalıklarını ve endişelerini analiz eden istatistiksel veri modelidir.
   - **Amacı:** Toplumsal farkındalık düzeyini ölçerek yapay zeka modelinin tahminlerini insani ve sosyal bir perspektifle desteklemek.

---
💡 *Gezinmeye başlamak ve yapay zeka analizlerini incelemek için sol paneldeki menüden dilediğiniz aşamaya tıklayabilirsiniz.*
""")
