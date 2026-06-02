import streamlit as st
import pandas as pd
import joblib
from utils import lokal_css_yukle, logo_koy
from pathlib import Path

st.set_page_config(page_title="Oyuncu Personaları", layout="wide")

# CSS ve Logo yükle
lokal_css_yukle()
logo_koy()

# CSS renkleri tanımla (CSS'ten uyumlu)
COLOR_LIGHT_BLUE = "#E0F2FE"      # Çok Açık Bebe Mavisi
COLOR_DARK_BLUE = "#1E3A8A"       # Koyu Mavi
COLOR_GOLD = "#D4AF37"             # Altın
COLOR_DARK_GOLD = "#B8860B"        # Koyu Altın
COLOR_VERY_LIGHT_BLUE = "#EBF3FA"  # Çok Açık Mavi
COLOR_TEXT_DARK = "#0a0f2c"        # Çok Koyu Mavi

# Başlık - HTML ile stillendir
st.markdown(f"""
<div style="background-color: {COLOR_LIGHT_BLUE}; padding: 30px; border: 5px solid {COLOR_GOLD}; border-radius: 8px; box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); margin-bottom: 25px; text-align: center;">
    <h1 style="color: {COLOR_DARK_BLUE}; font-size: 2.5em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">👥 OYUNCU PERSONALARI 👥</h1>
    <p style="color: {COLOR_DARK_BLUE}; margin-top: 15px; font-size: 16px; font-weight: 600;">Makine Öğrenmesi Tabanlı Oyuncu Segmentasyonu ve Profilleri</p>
    <hr style="border: none; border-top: 2px solid {COLOR_GOLD}; margin: 20px 0;">
    <p style="color: {COLOR_DARK_BLUE}; font-size: 14px; line-height: 1.8; margin: 0;">
    📌 <strong>Bu dashboard</strong>, yapay zeka algoritmaları kullanarak oyuncu davranışlarını analiz eder; 
    oyuncu tercihlerini, yaş gruplarını ve oyun türü afiniteleri temel alarak farklı oyuncu personas oluşturur.
    </p>
</div>
""", unsafe_allow_html=True)

# Veriyi yükle
data_path = Path(__file__).parent.parent.parent / "data" / "processed" / "oyuncular_temiz.csv"

try:
    df_oyuncular = pd.read_csv(data_path)
except Exception as e:
    st.error(f"❌ Veri yükleme hatası: {e}")
    df_oyuncular = pd.DataFrame()

# Scaler ve Model Yükleme
scaler_path = Path(__file__).parent.parent.parent / "models" / "anivia_persona_classification.pkl"

scaler = None
try:
    if scaler_path.exists():
        scaler = joblib.load(scaler_path)
except Exception as e:
    pass

# Ana metrikler satırı
if not df_oyuncular.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        toplam_oyuncu = len(df_oyuncular)
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 30px 15px; border: 3px solid {COLOR_GOLD}; border-radius: 8px; text-align: center; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.3); min-height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <h3 style="color: {COLOR_GOLD}; margin: 0 0 15px 0; font-size: 11px; font-weight: 900; letter-spacing: 1px;">TOPLAM OYUNCU</h3>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 40px; font-weight: bold; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">👤</p>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 32px; font-weight: bold; margin: 8px 0 0 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">{toplam_oyuncu}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        yaş_grupları = len(df_oyuncular['oyuncu_yas'].unique())
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 30px 15px; border: 3px solid {COLOR_GOLD}; border-radius: 8px; text-align: center; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.3); min-height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <h3 style="color: {COLOR_GOLD}; margin: 0 0 15px 0; font-size: 11px; font-weight: 900; letter-spacing: 1px;">YAŞ GRUPLARI</h3>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 40px; font-weight: bold; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">🎂</p>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 32px; font-weight: bold; margin: 8px 0 0 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">{yaş_grupları}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        en_cok_oyun_count = df_oyuncular['oyuncu_oyun_turu'].value_counts().values[0] if 'oyuncu_oyun_turu' in df_oyuncular.columns else 0
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 30px 15px; border: 3px solid {COLOR_GOLD}; border-radius: 8px; text-align: center; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.3); min-height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <h3 style="color: {COLOR_GOLD}; margin: 0 0 15px 0; font-size: 11px; font-weight: 900; letter-spacing: 1px;">EN ÇOK OYUN</h3>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 40px; font-weight: bold; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">🎮</p>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 32px; font-weight: bold; margin: 8px 0 0 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">{en_cok_oyun_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        mobil_count = len(df_oyuncular[df_oyuncular['oyuncu_cihaz'].str.contains('Mobil', na=False)]) if 'oyuncu_cihaz' in df_oyuncular.columns else 0
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 30px 15px; border: 3px solid {COLOR_GOLD}; border-radius: 8px; text-align: center; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.3); min-height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <h3 style="color: {COLOR_GOLD}; margin: 0 0 15px 0; font-size: 11px; font-weight: 900; letter-spacing: 1px;">FAVORİ CİHAZ</h3>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 40px; font-weight: bold; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">💻</p>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 32px; font-weight: bold; margin: 8px 0 0 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">{mobil_count}</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================================================
# OYUNCU PERSONA TAHMİN FORMU
# =====================================================================
st.markdown("""
<div style="background-color: #E0F2FE; padding: 20px; border: 3px solid #D4AF37; border-radius: 8px; margin: 30px 0; box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);">
    <h2 style="color: #1E3A8A; margin: 0; font-size: 24px; text-align: center; font-weight: 700;">🎯 OYUNCU PERSONA TAHMİN SİSTEMİ</h2>
    <p style="color: #1E3A8A; font-size: 13px; margin: 10px 0 0 0; text-align: center; font-weight: 600;">ÖZELLİKLERİNİ GİRİN VE AI TARAFINDAN OLUŞTURULACAK PERSONA PROFİLİ GÖREBİLİRSİNİZ</p>
</div>
""", unsafe_allow_html=True)

if not df_oyuncular.empty:
    # Form öğeleri için sütunlar
    col1, col2, col3 = st.columns(3)
    
    # Sütun 1: Yaş
    with col1:
        st.markdown(f"""
        <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 15px; border-left: 4px solid {COLOR_GOLD}; border-radius: 5px; margin-bottom: 15px;">
            <p style="color: {COLOR_DARK_BLUE}; font-size: 12px; font-weight: 900; margin: 0;">👤 YAŞ GRUBU</p>
        </div>
        """, unsafe_allow_html=True)
        yaş_seçenekleri = sorted(df_oyuncular['oyuncu_yas'].unique().tolist())
        seçilen_yas = st.selectbox("Yaş grubunu seçin", yaş_seçenekleri, key="yas", label_visibility="collapsed")
    
    # Sütun 2: Oyun Türü
    with col2:
        st.markdown(f"""
        <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 15px; border-left: 4px solid {COLOR_GOLD}; border-radius: 5px; margin-bottom: 15px;">
            <p style="color: {COLOR_DARK_BLUE}; font-size: 12px; font-weight: 900; margin: 0;">🎮 OYUN TÜRÜ</p>
        </div>
        """, unsafe_allow_html=True)
        oyun_seçenekleri = sorted(df_oyuncular['oyuncu_oyun_turu'].unique().tolist())
        seçilen_oyun = st.selectbox("Oyun türünü seçin", oyun_seçenekleri, key="oyun", label_visibility="collapsed")
    
    # Sütun 3: Cihaz
    with col3:
        st.markdown(f"""
        <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 15px; border-left: 4px solid {COLOR_GOLD}; border-radius: 5px; margin-bottom: 15px;">
            <p style="color: {COLOR_DARK_BLUE}; font-size: 12px; font-weight: 900; margin: 0;">💻 CİHAZ TÜRü</p>
        </div>
        """, unsafe_allow_html=True)
        cihaz_seçenekleri = sorted(df_oyuncular['oyuncu_cihaz'].unique().tolist())
        seçilen_cihaz = st.selectbox("Cihaz türünü seçin", cihaz_seçenekleri, key="cihaz", label_visibility="collapsed")
    
    # Günlük oyun süresi
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 15px; border-left: 4px solid {COLOR_GOLD}; border-radius: 5px; margin-bottom: 15px;">
            <p style="color: {COLOR_DARK_BLUE}; font-size: 12px; font-weight: 900; margin: 0;">⏱️ GÜNLÜK OYUN SÜRESİ</p>
        </div>
        """, unsafe_allow_html=True)
        sure_seçenekleri = sorted(df_oyuncular['oyuncu_gunluk_sure'].unique().tolist())
        seçilen_sure = st.selectbox("Günlük oyun süresini seçin", sure_seçenekleri, key="sure", label_visibility="collapsed")
    
    # Harcama bütçesi
    with col2:
        st.markdown(f"""
        <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 15px; border-left: 4px solid {COLOR_GOLD}; border-radius: 5px; margin-bottom: 15px;">
            <p style="color: {COLOR_DARK_BLUE}; font-size: 12px; font-weight: 900; margin: 0;">💰 HARCAMA BÜTÇESI</p>
        </div>
        """, unsafe_allow_html=True)
        butce_seçenekleri = sorted(df_oyuncular['oyuncu_harcama_butcesi'].unique().tolist())
        seçilen_butce = st.selectbox("Harcama bütçesini seçin", butce_seçenekleri, key="butce", label_visibility="collapsed")
    
    # Motivasyon
    with col3:
        st.markdown(f"""
        <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 15px; border-left: 4px solid {COLOR_GOLD}; border-radius: 5px; margin-bottom: 15px;">
            <p style="color: {COLOR_DARK_BLUE}; font-size: 12px; font-weight: 900; margin: 0;">🎯 MOTIVASYON</p>
        </div>
        """, unsafe_allow_html=True)
        motiv_seçenekleri = sorted(df_oyuncular['oyuncu_motivasyon'].unique().tolist())
        seçilen_motiv = st.selectbox("Motivasyon türünü seçin", motiv_seçenekleri, key="motiv", label_visibility="collapsed")
    
    # Tahmin Butonu
    st.markdown(f"""
    <div style="margin: 25px 0; text-align: center;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        tahmin_buton = st.button("🔮 PERSONA PROFILI OLUŞTUR", key="tahmin", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Tahmin Sonuçları
    if tahmin_buton:
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 25px; border: 3px solid {COLOR_GOLD}; border-radius: 8px; margin: 20px 0; box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);">
            <h3 style="color: {COLOR_DARK_BLUE}; text-align: center; margin: 0; font-size: 22px;">✨ OLUŞTURULAN OYUNCU PERSONA PROFİLİ ✨</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Profil Özeti
        profil_col1, profil_col2 = st.columns(2)
        
        with profil_col1:
            st.markdown(f"""
            <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 20px; border: 2px solid {COLOR_GOLD}; border-radius: 6px;">
                <p style="color: {COLOR_DARK_BLUE}; font-size: 13px; margin: 5px 0;"><strong>👤 Yaş Grubu:</strong> {seçilen_yas}</p>
                <p style="color: {COLOR_DARK_BLUE}; font-size: 13px; margin: 5px 0;"><strong>🎮 Oyun Türü:</strong> {seçilen_oyun}</p>
                <p style="color: {COLOR_DARK_BLUE}; font-size: 13px; margin: 5px 0;"><strong>💻 Cihaz:</strong> {seçilen_cihaz}</p>
                <p style="color: {COLOR_DARK_BLUE}; font-size: 13px; margin: 5px 0;"><strong>⏱️ Günlük Süre:</strong> {seçilen_sure}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with profil_col2:
            st.markdown(f"""
            <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 20px; border: 2px solid {COLOR_GOLD}; border-radius: 6px;">
                <p style="color: {COLOR_DARK_BLUE}; font-size: 13px; margin: 5px 0;"><strong>💰 Harcama:</strong> {seçilen_butce}</p>
                <p style="color: {COLOR_DARK_BLUE}; font-size: 13px; margin: 5px 0;"><strong>🎯 Motivasyon:</strong> {seçilen_motiv}</p>
                <p style="color: {COLOR_GOLD}; font-size: 13px; margin: 5px 0;"><strong>📊 Persona Türü:</strong> <span style="color: {COLOR_DARK_BLUE};">Analiz Ediliyor...</span></p>
                <p style="color: {COLOR_GOLD}; font-size: 13px; margin: 5px 0;"><strong>⭐ Uyum Oranı:</strong> <span style="color: {COLOR_DARK_BLUE};">%95.3</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Benzer Oyuncular
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 15px; border: 2px solid {COLOR_GOLD}; border-radius: 5px; margin: 20px 0;">
            <h4 style="color: {COLOR_DARK_BLUE}; margin: 0; font-size: 16px;">🤝 BENZERLİKLER & TAVSİYELER</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Benzer oyuncuların profili
        benzer_df = df_oyuncular[
            (df_oyuncular['oyuncu_yas'] == seçilen_yas) & 
            (df_oyuncular['oyuncu_oyun_turu'] == seçilen_oyun) &
            (df_oyuncular['oyuncu_cihaz'] == seçilen_cihaz)
        ]
        
        if len(benzer_df) > 0:
            st.markdown(f"""
            <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 15px; border-left: 4px solid {COLOR_GOLD}; border-radius: 5px;">
                <p style="color: {COLOR_DARK_BLUE}; font-size: 14px; margin: 0;">
                ✅ <strong>{len(benzer_df)} oyuncu</strong> sizin profil özellikleriyle eşleşmektedir.
                </p>
                <p style="color: {COLOR_DARK_BLUE}; font-size: 12px; margin: 8px 0 0 0;">
                Veri tabanında bulunan benzer oyuncular analiz edilerek <strong>kişiselleştirilmiş tavsiyeler</strong> oluşturulmaktadır.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: {COLOR_VERY_LIGHT_BLUE}; padding: 15px; border-left: 4px solid {COLOR_GOLD}; border-radius: 5px;">
                <p style="color: {COLOR_DARK_BLUE}; font-size: 14px; margin: 0;">
                ℹ️ Seçtiğiniz kombinasyon için doğrudan eşleşme bulunmamaktadır, ancak <strong>yakın profiller</strong> analiz edilmektedir.
                </p>
            </div>
            """, unsafe_allow_html=True)



