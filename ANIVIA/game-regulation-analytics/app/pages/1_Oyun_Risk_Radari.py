import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import joblib
import plotly.graph_objects as go
import plotly.express as px
from utils import lokal_css_yukle, logo_koy
from pathlib import Path

st.set_page_config(page_title="Oyun Risk Radarı", layout="wide")

# CSS ve Logo yükle
lokal_css_yukle()
logo_koy()

# CSS renkleri tanımla
COLOR_LIGHT_BLUE = "#E0F2FE"
COLOR_DARK_BLUE = "#1E3A8A"
COLOR_GOLD = "#D4AF37"
COLOR_LIGHT_GOLD = "#B8860B"

# =====================================================================
# Model ve Scaler Yükleme
# =====================================================================
model_path = Path(__file__).parent.parent.parent / "models" / "anivia_risk_radari_xgb.pkl"
scaler_path = Path(__file__).parent.parent.parent / "models" / "anivia_scaler.pkl"

model_loaded = False
scaler_loaded = False

# Model Yükleme (Joblib ile denesin, başarısızsa XGBoost native yükleme)
try:
    if not model_path.exists():
        st.error(f"❌ Model dosyası bulunamadı!")
        st.error(f"📍 Arama yolu: {model_path}")
        st.error(f"📁 Parent klasör var mı: {model_path.parent.exists()}")
        if model_path.parent.exists():
            pkl_files = list(model_path.parent.glob('*.pkl'))
            st.error(f"📄 Mevcut .pkl dosyaları: {[f.name for f in pkl_files]}")
        model_loaded = False
    else:
        # Plan A: Joblib ile yüklemeyi denesin
        try:
            risk_model = joblib.load(model_path)
            model_loaded = True
            # st.success(f"✅ Model yüklendi (Joblib): {model_path.name}")
        except Exception as joblib_error:
            # Eğer "unsupported persistent id" hatası alırsa
            if "unsupported persistent id" in str(joblib_error):
                # st.warning(f"⚠️ Joblib yükleme başarısız, XGBoost native yükleme deneniyor...")
                
                # Plan B: XGBoost native yükleme
                try:
                    import xgboost as xgb
                    risk_model = xgb.XGBClassifier()
                    risk_model.load_model(str(model_path))
                    model_loaded = True
                    # st.success(f"✅ Model yüklendi (XGBoost Native): {model_path.name}")
                except Exception as xgb_error:
                    st.error(f"❌ XGBoost native yükleme de başarısız: {str(xgb_error)}")
                    model_loaded = False
            else:
                st.error(f"❌ Model yükleme hatası: {str(joblib_error)}")
                st.error(f"📍 Denenen yol: {model_path}")
                model_loaded = False
except Exception as e:
    st.error(f"❌ Model yükleme kritik hatası: {str(e)}")
    st.error(f"📍 Denenen yol: {model_path}")
    model_loaded = False

# Scaler Yükleme (Joblib ile denesin, başarısızsa bilgilendirin)
try:
    if not scaler_path.exists():
        st.error(f"❌ Scaler dosyası bulunamadı!")
        st.error(f"📍 Arama yolu: {scaler_path}")
        scaler_loaded = False
    else:
        scaler = joblib.load(scaler_path)
        scaler_loaded = True
        # st.success(f"✅ Scaler yüklendi: {scaler_path.name}")
except Exception as e:
    st.error(f"❌ Scaler yükleme hatası: {str(e)}")
    st.error(f"📍 Denenen yol: {scaler_path}")
    scaler_loaded = False

# Başlık - HTML ile stillendir
st.markdown(f"""
<div style="background-color: {COLOR_LIGHT_BLUE}; padding: 25px; border: 4px solid {COLOR_GOLD}; border-radius: 5px; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); margin-bottom: 20px;">
    <h1 style="color: {COLOR_DARK_BLUE}; text-align: center; font-size: 32px; margin: 0;">🎮 OYUN RİSK RADARI 🎮</h1>
    <p style="color: {COLOR_DARK_BLUE}; text-align: center; margin-top: 10px; font-size: 14px;">Çocukların Oyun Seçimi İçin Akıllı Analiz Sistemi</p>
    <hr style="border: 0; border-top: 1px solid {COLOR_GOLD}; margin: 15px 0;">
    <p style="color: {COLOR_DARK_BLUE}; font-size: 13px; line-height: 1.6; margin: 0; text-align: center;">
    📌 <strong>Bu analitik dashboard</strong>, yapay zeka ve makine öğrenmesi (XGBoost) algoritmalarını kullanarak oyunların platform, kategori ve yaş sınırı (PEGI) gibi parametrelerini analiz eder; 
    çocukların dijital güvenliğini tehdit edebilecek olası risk durumlarını dinamik olarak tahmin eder.
    </p>
</div>
""", unsafe_allow_html=True)

# Veriyi yükle
data_path = Path(__file__).parent.parent.parent / "data" / "processed" / "oyunlar_temiz.csv"

try:
    df_oyunlar = pd.read_csv(data_path)
except Exception as e:
    st.error(f"❌ Veri yükleme hatası: {e}")
    df_oyunlar = pd.DataFrame()

# Ana metrikler satırı
if not df_oyunlar.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 20px; border-left: 5px solid {COLOR_GOLD}; border-radius: 3px; text-align: center;">
            <h3 style="color: {COLOR_GOLD}; margin: 0; font-size: 14px;">TOPLAM OYUN</h3>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 28px; font-weight: bold; margin: 10px 0;">📊 {len(df_oyunlar)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        guvenli = (df_oyunlar['tehlikeli_oyun'] == 0).sum()
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 20px; border-left: 5px solid {COLOR_GOLD}; border-radius: 3px; text-align: center;">
            <h3 style="color: {COLOR_GOLD}; margin: 0; font-size: 14px;">GÜVENLI OYUN</h3>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 28px; font-weight: bold; margin: 10px 0;">✅ {guvenli}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        tehlikeli = (df_oyunlar['tehlikeli_oyun'] == 1).sum()
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 20px; border-left: 5px solid {COLOR_GOLD}; border-radius: 3px; text-align: center;">
            <h3 style="color: {COLOR_GOLD}; margin: 0; font-size: 14px;">TEHLİKELİ OYUN</h3>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 28px; font-weight: bold; margin: 10px 0;">⚠️ {tehlikeli}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        platform_cesitleri = df_oyunlar['platform'].nunique()
        st.markdown(f"""
        <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 20px; border-left: 5px solid {COLOR_GOLD}; border-radius: 3px; text-align: center;">
            <h3 style="color: {COLOR_GOLD}; margin: 0; font-size: 14px;">PLATFORM SAYISI</h3>
            <p style="color: {COLOR_DARK_BLUE}; font-size: 28px; font-weight: bold; margin: 10px 0;">🖥️ {platform_cesitleri}</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================================================
# YAPAY ZEKA İLE OYUN RİSKİ HESAPLA - TAHMIN FORMU (METRIKLERIN HEMEN ALTINDA)
# =====================================================================
st.markdown(f"""
<div style="background-color: {COLOR_LIGHT_BLUE}; padding: 40px 30px 0 30px; border: 3px solid {COLOR_GOLD}; border-radius: 5px 5px 0 0; margin-top: 50px; margin-bottom: 0; text-align: center; width: 100%; box-sizing: border-box; display: block;">
    <h2 style="color: {COLOR_DARK_BLUE}; margin: 0 0 15px 0; padding: 0; font-weight: bold; letter-spacing: 2px; font-size: 26px; line-height: 1.3;">🤖 YAPAY ZEKA İLE OYUN RİSKİ HESAPLA</h2>
    <div style="border-top: 2px solid {COLOR_GOLD}; margin: 15px 0 20px 0; width: 85%; margin-left: auto; margin-right: auto;"></div>
    <p style="color: {COLOR_DARK_BLUE}; margin: 0 0 30px 0; padding: 0; font-size: 16px; font-weight: 500; line-height: 1.5;">XGBoost modelimiz size yardımcı olacak</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background-color: {COLOR_LIGHT_BLUE}; padding: 20px 30px 30px 30px; border-left: 3px solid {COLOR_GOLD}; border-right: 3px solid {COLOR_GOLD}; border-bottom: 3px solid {COLOR_GOLD}; border-radius: 0 0 5px 5px; margin-top: -3px; width: 100%; box-sizing: border-box; display: block;">
""", unsafe_allow_html=True)

if model_loaded and scaler_loaded and not df_oyunlar.empty:
    col_pred1, col_pred2, col_pred3 = st.columns(3)
    
    with col_pred1:
        pred_fiyat = st.number_input("💰 Fiyat (USD):", 
                                     min_value=0.0, 
                                     max_value=1000.0, 
                                     value=0.0, 
                                     step=0.01,
                                     key="pred_fiyat")
    
    with col_pred2:
        pred_platform = st.selectbox("📱 Platform Seç:", 
                                     ["Seçiniz", "Appstore", "Playstore", "Steam", "Epic Games", "Nintendo", "PlayStation", "Xbox"],
                                     key="pred_platform")
    
    with col_pred3:
        pred_cihaz = st.selectbox("🖥️ Cihaz Türü Seç:", 
                                  ["Seçiniz", "Mobil Cihaz", "Kişisel Bilgisayar", "Konsol"],
                                  key="pred_cihaz")
    
    # Tahmin Butonu
    if st.button("🔍 Riski Analiz Et", use_container_width=True):
        # ===== DOĞRULAMA =====
        if pred_platform == "Seçiniz":
            st.warning("⚠️ Lütfen Platform seçiniz!")
        elif pred_cihaz == "Seçiniz":
            st.warning("⚠️ Lütfen Cihaz Türü seçiniz!")
        elif pred_fiyat < 0:
            st.warning("⚠️ Fiyat negatif olamaz! (0 = Ücretsiz oyun)")
        else:
            try:
                # ===== VERİ HAZIRLANMA =====
                
                # Kullanıcının seçtiği girdilerden ham bir DataFrame oluştur
                girdi_df = pd.DataFrame([{
                    'fiyat': pred_fiyat,
                    'platform': pred_platform,
                    'cihaz_turu': pred_cihaz
                }])
                
                # One-Hot Encoding uygula
                girdi_encoded = pd.get_dummies(girdi_df)
                
                # SCALER HİZALAMA (Kesin Çözüm)
                scaler_cols = scaler.feature_names_in_
                
                # Eksik sütunları 0 ile oluştur
                for col in scaler_cols:
                    if col not in girdi_encoded.columns:
                        girdi_encoded[col] = 0
                
                # Sütunların sırasını TAM OLARAK scaler'ın beklediği sıraya getir
                girdi_encoded = girdi_encoded[scaler_cols]
                
                # Transform
                X_scaled = scaler.transform(girdi_encoded)
                
                # Tahmin
                prediction = risk_model.predict(X_scaled)[0]
                probability = risk_model.predict_proba(X_scaled)[0]
                
                guvenli_olasiligi = probability[0] * 100
                tehlikeli_olasiligi = probability[1] * 100
                
                # ===== SONUÇ GÖSTER =====
                if prediction == 1:
                    # TEHLİKELİ
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #DC2626 0%, {COLOR_GOLD} 100%); 
                                padding: 30px; border-radius: 10px; border: 3px solid {COLOR_GOLD};
                                box-shadow: 0 0 20px rgba(220, 38, 38, 0.5); margin-top: 20px;">
                        <h3 style="color: white; text-align: center; margin-top: 0;">⚠️ TEHLİKELİ OYUN</h3>
                        <p style="color: white; text-align: center; font-size: 16px; margin: 10px 0;">
                            <strong>Fiyat:</strong> ${pred_fiyat:.2f}<br>
                            <strong>Platform:</strong> {pred_platform}<br>
                            <strong>Cihaz Türü:</strong> {pred_cihaz}
                        </p>
                        <div style="background-color: rgba(255, 255, 255, 0.2); padding: 15px; border-radius: 5px; margin-top: 15px;">
                            <p style="color: white; text-align: center; font-size: 14px; margin: 0;">
                                <strong>Güvenli Olma Olasılığı:</strong> {guvenli_olasiligi:.1f}%<br>
                                <strong>Tehlikeli Olma Olasılığı:</strong> {tehlikeli_olasiligi:.1f}%
                            </p>
                        </div>
                        <p style="color: white; text-align: center; font-size: 12px; margin-top: 15px; margin-bottom: 0;">
                            ⚠️ Bu oyun, çocuklar için potansiyel risk taşıyabilir. Velilerin dikkatli incelemesi önerilir.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # GÜVENLI
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {COLOR_DARK_BLUE} 0%, {COLOR_LIGHT_BLUE} 100%); 
                                padding: 30px; border-radius: 10px; border: 3px solid {COLOR_GOLD};
                                box-shadow: 0 0 20px rgba(30, 58, 138, 0.5); margin-top: 20px;">
                        <h3 style="color: white; text-align: center; margin-top: 0;">✅ GÜVENLI OYUN</h3>
                        <p style="color: white; text-align: center; font-size: 16px; margin: 10px 0;">
                            <strong>Fiyat:</strong> ${pred_fiyat:.2f}<br>
                            <strong>Platform:</strong> {pred_platform}<br>
                            <strong>Cihaz Türü:</strong> {pred_cihaz}
                        </p>
                        <div style="background-color: rgba(255, 255, 255, 0.2); padding: 15px; border-radius: 5px; margin-top: 15px;">
                            <p style="color: white; text-align: center; font-size: 14px; margin: 0;">
                                <strong>Güvenli Olma Olasılığı:</strong> {guvenli_olasiligi:.1f}%<br>
                                <strong>Tehlikeli Olma Olasılığı:</strong> {tehlikeli_olasiligi:.1f}%
                            </p>
                        </div>
                        <p style="color: white; text-align: center; font-size: 12px; margin-top: 15px; margin-bottom: 0;">
                            ✨ Bu oyun, çocuklara yönelik güvenli bir seçim gibi görünüyor!
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"❌ HATA OLUŞTU:")
                st.exception(e)

else:
    if not model_loaded or not scaler_loaded:
        st.warning("⚠️ Model veya Scaler yüklenemedi. Lütfen '03_game_ml_models.ipynb' notebook'unu çalıştırarak modelleri eğitin.")

st.markdown("</div>", unsafe_allow_html=True)  # Tahmin Motoru container'ını kapat

# =====================================================================
# FİLTRELEME SEÇENEKLERİ (ALT BÖLÜM) - ORTAK FILTERED_DF OLUŞTUR
# =====================================================================
st.markdown(f"""
<div style="background-color: {COLOR_LIGHT_BLUE}; padding: 15px; border: 2px solid {COLOR_GOLD}; border-radius: 5px; margin: 40px 0 20px 0;">
    <h3 style="color: {COLOR_DARK_BLUE}; margin-top: 0;">🔍 FİLTRELEME SEÇENEKLERI</h3>
</div>
""", unsafe_allow_html=True)

if not df_oyunlar.empty:
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        platforms = ["Hepsi"] + sorted(df_oyunlar['platform'].unique().tolist())
        selected_platform_display = st.selectbox("📱 Platform Seç:", platforms, key="filter_platform")
        selected_platform = None if selected_platform_display == "Hepsi" else selected_platform_display
    
    with col_filter2:
        ages = ["Hepsi"] + sorted([str(int(x)) for x in df_oyunlar['yas_siniri'].dropna().unique()], key=int)
        selected_age_display = st.selectbox("👶 Yaş Sınırı Seç:", ages, key="filter_age")
        selected_age = None if selected_age_display == "Hepsi" else int(selected_age_display)
    
    with col_filter3:
        risk_filter = st.radio("⚠️ Risk Durumu:", ["Tümü", "Güvenli", "Tehlikeli"], key="filter_risk")
    
    # ===== ORTAK FİLTRELENMİŞ DATAFRAME'İ OLUŞTUR (PLATFORM + YAŞ + RISK SADECE) =====
    filtered_df = df_oyunlar.copy()
    
    # Platform filtresi
    if selected_platform is not None:
        filtered_df = filtered_df[filtered_df['platform'] == selected_platform]
    
    # Yaş sınırı filtresi (0 değeri olduğu için "is not None" kullan!)
    if selected_age is not None:
        filtered_df = filtered_df[filtered_df['yas_siniri'] == selected_age]
    
    # Risk durumu filtresi
    if risk_filter == "Güvenli":
        filtered_df = filtered_df[filtered_df['tehlikeli_oyun'] == 0]
    elif risk_filter == "Tehlikeli":
        filtered_df = filtered_df[filtered_df['tehlikeli_oyun'] == 1]
    
    # ===== SONUÇLAR BAŞLIĞI (SENKRONIZE SAYILI) =====
    st.markdown(f"""
    <div style="background-color: {COLOR_LIGHT_BLUE}; padding: 15px; border: 2px solid {COLOR_GOLD}; border-radius: 5px; margin: 20px 0;">
        <h3 style="color: {COLOR_DARK_BLUE}; margin-top: 0;">📋 SONUÇLAR ({len(filtered_df)} oyun bulundu)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== KATEGORİ DAĞILIMI (FILTERED_DF'DEN) =====
    st.subheader("📊 Kategori Dağılımı")
    
    if not filtered_df['kategori'].dropna().empty:
        # Kategorileri virgülle ayırıp aç (explode) - Top 40 kategorisi
        cat_series = filtered_df['kategori'].dropna().astype(str).str.split(', ').explode()
        cat_counts = cat_series.value_counts().reset_index()
        cat_counts.columns = ['Kategori', 'Oyun Sayısı']
        cat_counts = cat_counts.head(40)  # Sadece en büyük 40 kategori
        
        # Dikey Plotly bar grafik
        fig_kategori = px.bar(cat_counts, x='Kategori', y='Oyun Sayısı', 
                              color_discrete_sequence=[COLOR_GOLD])
        fig_kategori.update_layout(
            title="Kategori Başına Oyun Sayısı (Top 40)",
            plot_bgcolor=COLOR_LIGHT_BLUE,
            paper_bgcolor=COLOR_LIGHT_BLUE,
            font=dict(color=COLOR_DARK_BLUE),
            height=450,
            showlegend=False,
            xaxis_tickangle=-45,  # Kategoriler 45 derece eğik
            margin=dict(b=100)  # Alt yazılar için yer
        )
        st.plotly_chart(fig_kategori, use_container_width=True)
    else:
        st.info("📊 Seçili filtreler için veri bulunmuyor.")
    
    # ===== OYUN LİSTESİ (FILTERED_DF'DEN) =====
    st.subheader("🎮 Oyun Listesi")
    display_cols = ['oyun_adi', 'platform', 'kategori', 'yas_siniri', 'tehlikeli_oyun']
    
    # Sadece mevcut sütunları göster
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    
    if not filtered_df.empty:
        st.dataframe(filtered_df[available_cols], use_container_width=True)
    else:
        st.info("🎮 Seçili filtreler için oyun bulunmuyor.")
