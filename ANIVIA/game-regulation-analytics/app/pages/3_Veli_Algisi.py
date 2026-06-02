import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils import lokal_css_yukle, logo_koy

st.set_page_config(page_title="Veli Algısı", layout="wide")

# CSS ve Logo yükle
lokal_css_yukle()
logo_koy()

st.header("Veli Algısı")

# Veri Yukleme
@st.cache_data
def veri_yukle():
    # Dosya yolunu dinamik olarak belirle
    data_path = Path(__file__).parent.parent.parent / "data" / "processed" / "veliler_skorlu.csv"
    if data_path.exists():
        df = pd.read_csv(data_path)
        return df
    else:
        st.error(f"Veri dosyası bulunamadı: {data_path}")
        return None

df = veri_yukle()

if df is not None:
    # Sidebar Filtreleri
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtreleme")
    
    selected_gender = st.sidebar.multiselect(
        "Veli Cinsiyeti", 
        options=df["veli_cinsiyet"].unique(), 
        default=df["veli_cinsiyet"].unique()
    )
    
    selected_child_age = st.sidebar.multiselect(
        "Çocuk Yaş Grubu", 
        options=df["cocuk_yas"].unique(), 
        default=df["cocuk_yas"].unique()
    )
    
    # Filtreleme Uygula
    filtered_df = df[
        (df["veli_cinsiyet"].isin(selected_gender)) & 
        (df["cocuk_yas"].isin(selected_child_age))
    ]
    
    # Metrikler
    st.subheader("📊 Temiz Performans Göstergeleri (KPI)")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        avg_score = filtered_df["ebeveyn_ilgi_skoru_100"].mean()
        st.metric("Ortalama İlgi Skoru", f"{avg_score:.1f} / 100")
        
    with m2:
        total_resp = len(filtered_df)
        st.metric("Analiz Edilen Veli Sayısı", total_resp)
        
    with m3:
        high_interest = (filtered_df["ebeveyn_ilgi_skoru_100"] > 70).sum()
        ratio = (high_interest / total_resp * 100) if total_resp > 0 else 0
        st.metric("Yüksek İlgi Oranı", f"%{ratio:.1f}")

    st.markdown("---")
    
    # Görselleştirmeler
    st.subheader("📈 Çapraz Analizler")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### Harcama Etkisi vs İlgi Skoru")
        # Harcama güven etkisine göre ortalama skor
        harcama_skor = filtered_df.groupby("veli_harcama_guven_etkisi")["ebeveyn_ilgi_skoru_100"].mean().reset_index()
        fig_harcama = px.bar(
            harcama_skor, 
            x="ebeveyn_ilgi_skoru_100", 
            y="veli_harcama_guven_etkisi",
            orientation='h',
            labels={"ebeveyn_ilgi_skoru_100": "Ort. İlgi Skoru", "veli_harcama_guven_etkisi": "Harcama Güven Etkisi"},
            color="ebeveyn_ilgi_skoru_100",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_harcama, use_container_width=True)

    with c2:
        st.markdown("#### Ruh Hali Gözlemi vs İlgi Skoru")
        fig_box = px.box(
            filtered_df, 
            x="cocuk_ruh_hali_gozlemi", 
            y="ebeveyn_ilgi_skoru_100",
            labels={"cocuk_ruh_hali_gozlemi": "Ruh Hali Gözlemi", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"},
            color="cocuk_ruh_hali_gozlemi"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("#### Çocuk Yaş Grubuna Göre İlgi Skoru Dağılımı")
    fig_age = px.violin(
        filtered_df, 
        x="cocuk_yas", 
        y="ebeveyn_ilgi_skoru_100", 
        color="cocuk_yas",
        box=True, 
        points="all",
        labels={"cocuk_yas": "Yaş Grubu", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"}
    )
    st.plotly_chart(fig_age, use_container_width=True)
else:
    st.warning("Veriler yüklenemediği için analiz gösterilemiyor.")
