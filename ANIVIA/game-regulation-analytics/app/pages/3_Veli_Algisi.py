import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from utils import lokal_css_yukle, logo_koy

st.set_page_config(page_title="Veli Algısı", layout="wide")

# CSS ve Logo yükle
lokal_css_yukle()
logo_koy()

# CSS Renkler
COLOR_LIGHT_BLUE = "#E0F2FE"
COLOR_DARK_BLUE = "#1E3A8A"
COLOR_GOLD = "#D4AF37"
COLOR_DARK_GOLD = "#B8860B"
COLOR_VERY_LIGHT_BLUE = "#EBF3FA"
COLOR_TEXT_DARK = "#0a0f2c"

st.markdown("""
<div style="text-align: center; margin-bottom: 30px; border-bottom: 5px solid #D4AF37; padding-bottom: 15px;">
    <h1 style="color: #1E3A8A; font-size: 3em; margin: 0;">VELİ ALGISI</h1>
</div>
""", unsafe_allow_html=True)

# Veri Yukleme
@st.cache_data
def veri_yukle():
    data_path = Path(__file__).parent.parent.parent / "data" / "processed" / "veliler_skorlu.csv"
    if data_path.exists():
        df = pd.read_csv(data_path)
        return df
    else:
        st.error(f"Veri dosyası bulunamadı: {data_path}")
        return None

df = veri_yukle()

if df is not None:
    
    # ============================================================
    # ÜST KIŞIM: GENEL ANALIZ (SABİT - HER ZAMAN VİZİBL)
    # ============================================================
    
    st.subheader("📊 Genel Veli Algısı Tablosu")
    st.markdown("*Tüm veliler için temel analiz ve istatistikler*")
    
    # ===== METRİK KARTLARI (Genel) =====
    m1, m2, m3, m4 = st.columns(4)
    
    avg_score = df["ebeveyn_ilgi_skoru_100"].mean()
    total_resp = len(df)
    high_interest = (df["ebeveyn_ilgi_skoru_100"] > 70).sum()
    high_ratio = (high_interest / total_resp * 100) if total_resp > 0 else 0
    low_interest = (df["ebeveyn_ilgi_skoru_100"] < 40).sum()
    low_ratio = (low_interest / total_resp * 100) if total_resp > 0 else 0
    
    with m1:
        st.metric("📈 Ort. İlgi Skoru", f"{avg_score:.1f}/100")
    
    with m2:
        st.metric("👥 Toplam Veli", total_resp)
    
    with m3:
        st.metric("⬆️ Yüksek İlgi", f"{high_ratio:.1f}%")
    
    with m4:
        st.metric("⬇️ Düşük İlgi", f"{low_ratio:.1f}%")
    
    st.markdown("---")
    
    # ===== DONUT GRAFİĞİ (Genel) =====
    st.subheader("🎯 İlgi Skoru Kategorilerinin Dağılımı (Genel)")
    
    high = (df["ebeveyn_ilgi_skoru_100"] >= 70).sum()
    medium = ((df["ebeveyn_ilgi_skoru_100"] >= 40) & (df["ebeveyn_ilgi_skoru_100"] < 70)).sum()
    low = (df["ebeveyn_ilgi_skoru_100"] < 40).sum()
    
    donut_data = {
        "Kategori": ["Yüksek İlgi (70+)", "Orta İlgi (40-69)", "Düşük İlgi (<40)"],
        "Sayı": [high, medium, low],
        "Yüzde": [
            (high / total_resp * 100) if total_resp > 0 else 0,
            (medium / total_resp * 100) if total_resp > 0 else 0,
            (low / total_resp * 100) if total_resp > 0 else 0
        ]
    }
    donut_df = pd.DataFrame(donut_data)
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=donut_df["Kategori"],
        values=donut_df["Sayı"],
        hole=0.4,
        marker=dict(colors=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE]),
        text=[f"{x:.1f}%" for x in donut_df["Yüzde"]],
        textposition="inside",
        hovertemplate="<b>%{label}</b><br>Sayı: %{value}<br>Yüzde: %{customdata:.1f}%<extra></extra>",
        customdata=donut_df["Yüzde"]
    )])
    
    fig_donut.update_layout(
        font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
        paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
        plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
        height=450
    )
    
    st.plotly_chart(fig_donut, use_container_width=True)
    
    dominant_category = donut_df.loc[donut_df["Sayı"].idxmax(), "Kategori"]
    dominant_percent = donut_df.loc[donut_df["Sayı"].idxmax(), "Yüzde"]
    high_score_veli = df[df["ebeveyn_ilgi_skoru_100"] > 80]
    
    if len(high_score_veli) > 0:
        gender_counts = high_score_veli["veli_cinsiyet"].value_counts()
        if len(gender_counts) > 0:
            dominant_gender_in_high = gender_counts.index[0]
            high_gender_count = gender_counts.iloc[0]
            high_gender_percent = (high_gender_count / len(high_score_veli) * 100)
            pct_high_overall = (len(high_score_veli) / total_resp * 100)
            st.info(f"📌 **Derinlemesine Kategori Analizi:** Ebeveynlerin %{dominant_percent:.1f}'ini oluşturan {dominant_category} kategorisinin baskın konumu, örneklem içinde oyun güvenliğine yönelik tutumların orta-yüksek düzeyde yoğunlaştığını göstermektedir. Skoru 80 puanın üzerine çıkan {len(high_score_veli)} ebeveyn (%{pct_high_overall:.1f}), tüm popülasyonun en bilinçli ve aktif segment'ini temsil etmektedir; bu grup içerisinde **{dominant_gender_in_high}** ebeveynler %{high_gender_percent:.1f} oranında ön plana çıkmaktadır. Yüksek farkındalık skorunun cinsiyet boyutunda bu şekilde dağılması, belirli demografik grupların dijital oyun eko-sistemindeki çocuk güvenliği konularında daha etkin bir denetim mekanizması oluşturduğunu işaret etmektedir. Söz konusu dinamik, ebeveyn eğitimi ve bilinçlendirme kampanyalarının hangi hedef kitleye odaklanması gerektiğinin önemli bir göstergesidir. Dolayısıyla, oyun güvenliği politikaları ve koruyucu tedbirlerin tasarlanmasında, bu yüksek-farkındalık grubunun deneyim ve yaklaşımları model alınabilir.")
    
    st.markdown("---")
    
    # ===== HİSTOGRAM (Genel) =====
    st.subheader("📊 İlgi Skoru Dağılımı (Genel)")
    
    try:
        fig_hist = go.Figure(data=[go.Histogram(
            x=df["ebeveyn_ilgi_skoru_100"],
            nbinsx=15,
            marker=dict(color=COLOR_DARK_BLUE, line=dict(color=COLOR_GOLD, width=2))
        )])
        
        fig_hist.update_layout(
            xaxis_title="İlgi Skoru",
            yaxis_title="Veli Sayısı",
            font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
            paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
            plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
    except:
        # Fallback: Bar grafiğe çevir
        score_dist = df["ebeveyn_ilgi_skoru_100"].value_counts().sort_index()
        fig_bar = go.Figure(data=[go.Bar(
            x=score_dist.index,
            y=score_dist.values,
            marker=dict(color=COLOR_DARK_BLUE)
        )])
        fig_bar.update_layout(
            xaxis_title="İlgi Skoru",
            yaxis_title="Sayı",
            font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
            paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
            plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    median_score = df["ebeveyn_ilgi_skoru_100"].median()
    mean_score = df["ebeveyn_ilgi_skoru_100"].mean()
    std_score = df["ebeveyn_ilgi_skoru_100"].std()
    q1 = df["ebeveyn_ilgi_skoru_100"].quantile(0.25)
    q3 = df["ebeveyn_ilgi_skoru_100"].quantile(0.75)
    
    skewness = "sağa" if mean_score > median_score else "sola"
    iqr = q3 - q1
    outlier_upper = q3 + 1.5 * iqr
    outlier_lower = q1 - 1.5 * iqr
    outliers = ((df["ebeveyn_ilgi_skoru_100"] > outlier_upper) | (df["ebeveyn_ilgi_skoru_100"] < outlier_lower)).sum()
    median_diff = abs(mean_score - median_score)
    st.success(f"📊 **İstatistiksel Dağılım Analizi:** Ebeveyn ilgi skorlarının dağılımı {skewness} yönde çarpıklık göstermekte (Ort: {mean_score:.2f}, Medyan: {median_score:.2f}, Fark: {median_diff:.2f}), bu da veri setindeki sistematik eğilimi yansıtmaktadır. Çeyrek aralık analizi (Q1: {q1:.1f}, Q3: {q3:.1f}, İQR: {iqr:.1f}), temel veri grubunun belirli skorların etrafında yoğunlaştığını göstermektedir. Standart sapma ({std_score:.2f}) değeri, ebeveynlik yaklaşımlarının heterojenliğinin ölçüsü olup, bu değişkenlik demografik ve sosyoekonomik faktörlere atfedilebilir. Uç değerler ({outliers} veli), istisnai durumları temsil eden ve oyun güvenliğine ilişkin tutum spektrumunun genişliğini göstermektedir. Söz konusu dağılım karakteristikleri, ebeveyn eğitim ve müdahale programlarının farklılaştırılmış yaklaşımlar gerektirdiğini, özellikle de düşük skorlu gruplar için yoğunlaştırılmış bilinçlendirme çalışmalarının kritik öneme sahip olduğunu göstermektedir.")
    
    st.markdown("---")
    
    # ===== BOXPLOT: CİNSİYET (Genel) =====
    st.subheader("👥 Cinsiyet Açısından İlgi Skoru Analizi (Genel)")
    
    if "veli_cinsiyet" in df.columns and len(df) > 0:
        try:
            fig_box_gender = px.box(
                df,
                x="veli_cinsiyet",
                y="ebeveyn_ilgi_skoru_100",
                title="",
                labels={"veli_cinsiyet": "Veli Cinsiyeti", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"},
                color="veli_cinsiyet",
                color_discrete_sequence=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE]
            )
            
            fig_box_gender.update_layout(
                font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_box_gender, use_container_width=True)
        except:
            # Fallback: Scatter grafiğe çevir
            fig_scatter_gender = px.scatter(
                df,
                x="veli_cinsiyet",
                y="ebeveyn_ilgi_skoru_100",
                title="",
                labels={"veli_cinsiyet": "Veli Cinsiyeti", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"},
                color="veli_cinsiyet",
                color_discrete_sequence=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE],
                size_max=15
            )
            
            fig_scatter_gender.update_layout(
                font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_scatter_gender, use_container_width=True)
    
    gender_stats = df.groupby("veli_cinsiyet")["ebeveyn_ilgi_skoru_100"].agg(['mean', 'median', 'std', 'min', 'max', 'count'])
    if len(gender_stats) > 0:
        gender_sorted = gender_stats.sort_values('mean', ascending=False)
        top_gender = gender_sorted.index[0]
        top_mean = gender_sorted.iloc[0]['mean']
        top_std = gender_sorted.iloc[0]['std']
        top_count = int(gender_sorted.iloc[0]['count'])
        if len(gender_sorted) > 1:
            bottom_gender = gender_sorted.index[-1]
            bottom_mean = gender_sorted.iloc[-1]['mean']
            bottom_std = gender_sorted.iloc[-1]['std']
            gender_diff = top_mean - bottom_mean
            st.info(f"💡 **Cinsiyet Boyutunda Ebeveyn Farkındalığı:** {top_gender} ebeveynlerin oyun güvenliğine yönelik ilgi skoru ortalaması {top_mean:.2f} (/100) olup, standart sapması {top_std:.2f} seviyesindedir (n={top_count}). Karşılaştırmalı olarak, {bottom_gender} ebeveynler {bottom_mean:.2f} ortalama skor elde etmiş olup, iki grup arasında {gender_diff:.2f} puantlık bir fark gözlenmektedir. Bu fark, oyun güvenliği konularında cinsiyet-bazlı tutum farklılıklarının önemli bir göstergesidir. Standart sapma değerleri ({top_std:.2f} vs {bottom_std:.2f}), her iki grup içindeki homojenlik derecesini ortaya koymakta, düşük standart sapma daha tutarlı tutumlar gösterirken, yüksek sapma grup içi görüş ayrılıklarını işaret etmektedir. Dijital oyunlarda çocuk güvenliği bağlamında, ebeveynlerin cinsiyet-bazlı farklı denetim ve bilinçlendirme ihtiyaçlarının olabileceği bu veriler tarafından desteklenmektedir.")
        else:
            st.info(f"💡 **Cinsiyet Analizi:** Örneklemde {top_gender} ebeveynler yer almakta, ortalama skoru {top_mean:.2f} (Std: {top_std:.2f}, n={top_count})'dir. Cinsiyet dağılımının tek gruba yoğunlaşması nedeniyle karşılaştırmalı analiz yapılamamış olup, sonuç tüm nüfusu temsil etme kapasitesi sınırlıdır.")
    
    st.markdown("---")
    
    # ===== BOXPLOT: RUH HALI (Genel) =====
    st.subheader("😊 Ruh Hali Gözlemi ile İlgi Skoru Bağlantısı (Genel)")
    
    if "cocuk_ruh_hali_gozlemi" in df.columns and len(df) > 0:
        try:
            fig_box_mood = px.box(
                df,
                x="cocuk_ruh_hali_gozlemi",
                y="ebeveyn_ilgi_skoru_100",
                title="",
                labels={"cocuk_ruh_hali_gozlemi": "Çocuk Ruh Hali", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"},
                color="cocuk_ruh_hali_gozlemi",
                color_discrete_sequence=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE]
            )
            
            fig_box_mood.update_layout(
                font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_box_mood, use_container_width=True)
        except:
            # Fallback: Scatter grafiğe çevir
            fig_scatter_mood = px.scatter(
                df,
                x="cocuk_ruh_hali_gozlemi",
                y="ebeveyn_ilgi_skoru_100",
                title="",
                labels={"cocuk_ruh_hali_gozlemi": "Çocuk Ruh Hali", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"},
                color="cocuk_ruh_hali_gozlemi",
                color_discrete_sequence=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE],
                size_max=15
            )
            
            fig_scatter_mood.update_layout(
                font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_scatter_mood, use_container_width=True)
    
    mood_stats = df.groupby("cocuk_ruh_hali_gozlemi")["ebeveyn_ilgi_skoru_100"].agg(['mean', 'median', 'std', 'min', 'max', 'count']).sort_values('mean', ascending=False)
    if len(mood_stats) > 0:
        best_mood = mood_stats.index[0]
        best_mean = mood_stats.iloc[0]['mean']
        best_std = mood_stats.iloc[0]['std']
        best_count = int(mood_stats.iloc[0]['count'])
        worst_mood = mood_stats.index[-1]
        worst_mean = mood_stats.iloc[-1]['mean']
        worst_std = mood_stats.iloc[-1]['std']
        worst_count = int(mood_stats.iloc[-1]['count'])
        mood_diff = best_mean - worst_mean
        correlation_strength = "güçlü" if mood_diff > 15 else "orta" if mood_diff > 8 else "zayıf"
        st.success(f"🎯 **Çocuk Ruh Hali ve Ebeveyn Farkındalığı Korelasyonu:** Çocuğun ruh hali gözlemi {best_mood} olan ebeveynlerin ilgi skoru ortalaması {best_mean:.2f} ile en yüksek değeri almış olup, bu grup içindeki standart sapma {best_std:.2f}'dir (n={best_count}). Diğer taraftan, {worst_mood} ruh hali gözlemi yapan ebeveynlerin skoru {worst_mean:.2f} ile minimum seviyede yer almakta, {worst_std:.2f} standart sapması ile grup içi tutum değişkenliği göstermektedir (n={worst_count}). İki grup arasında {mood_diff:.2f} puantlık fark, çocuğun psikolojik ve duygusal durumunun, ebeveyn bilinçlendirme düzeyinin kritik bir yordayıcısı olduğunu göstermektedir. Bu {correlation_strength} korelasyon, stabil ve dengeli ruh halindeki çocuklara sahip ebeveynlerin, dijital oyun eko-sistemindeki güvenlik risklerine karşı daha etkin bir denetim mekanizması oluşturabildikleri şeklinde yorumlanabilir. Sonuç olarak, çocuğun duygusal ve psikolojik sağlığının iyileştirilmesi, ebeveyn oyun güvenliği farkındalığının artırılmasında kritik bir ara değişken görevini görmektedir.")
    
    # ============================================================
    # AYIRICI
    # ============================================================
    
    st.divider()
    
    # ============================================================
    # ALT KIŞIM: DETAYLI FİLTRELEME (DİNAMİK)
    # ============================================================
    
    st.subheader("🔍 Detaylı Filtreleme")
    st.markdown("*Belirli demografik gruplara göre analiz yapın*")
    
    # Session state'i başlat
    if "filter_applied" not in st.session_state:
        st.session_state.filter_applied = False
    
    f1, f2, f3 = st.columns([2, 2, 1])
    
    with f1:
        selected_gender = st.multiselect(
            "Veli Cinsiyeti", 
            options=sorted(df["veli_cinsiyet"].unique()), 
            default=[],
            key="gender_filter"
        )
    
    with f2:
        selected_child_age = st.multiselect(
            "Çocuk Yaş Grubu", 
            options=sorted(df["cocuk_yas"].unique()), 
            default=[],
            key="age_filter"
        )
    
    with f3:
        filter_button = st.button("🔍 Filtrele", key="apply_filter", use_container_width=True)
        if filter_button:
            st.session_state.filter_applied = True
            st.session_state.selected_gender = selected_gender
            st.session_state.selected_child_age = selected_child_age
    
    st.markdown("---")
    
    # Filtreleme Uygula
    if st.session_state.filter_applied:
        selected_gender = st.session_state.get("selected_gender", [])
        selected_child_age = st.session_state.get("selected_child_age", [])
        
        # Başlangıç: tüm veri
        filtered_df = df.copy()
        
        # Eğer cinsiyet seçildiyse filtrele
        if len(selected_gender) > 0:
            filtered_df = filtered_df[filtered_df["veli_cinsiyet"].isin(selected_gender)]
        
        # Eğer yaş grubu seçildiyse filtrele
        if len(selected_child_age) > 0:
            filtered_df = filtered_df[filtered_df["cocuk_yas"].isin(selected_child_age)]
    else:
        filtered_df = None
    
    # ALT KIŞIM ANALİZLERİ
    if not st.session_state.filter_applied:
        st.info("📋 **Lütfen filtreleri seçiniz ve 'Filtrele' butonuna basınız.**")
    
    elif st.session_state.filter_applied and filtered_df is not None and filtered_df.empty:
        st.warning("📭 **Bu filtreleme kriterlerine uygun veri bulunamadı.**")
    
    elif st.session_state.filter_applied and filtered_df is not None and not filtered_df.empty:
        st.success(f"✅ **Filtreleme Uygulandı:** {len(filtered_df)} veli seçildi")
        
        # ===== FİLTRELENMİŞ METRİK KARTLARI =====
        st.subheader("📊 Seçili Grup İçin Göstergeler")
        
        m1, m2, m3, m4 = st.columns(4)
        
        avg_score_f = filtered_df["ebeveyn_ilgi_skoru_100"].mean()
        total_resp_f = len(filtered_df)
        high_interest_f = (filtered_df["ebeveyn_ilgi_skoru_100"] > 70).sum()
        high_ratio_f = (high_interest_f / total_resp_f * 100) if total_resp_f > 0 else 0
        low_interest_f = (filtered_df["ebeveyn_ilgi_skoru_100"] < 40).sum()
        low_ratio_f = (low_interest_f / total_resp_f * 100) if total_resp_f > 0 else 0
        
        with m1:
            st.metric("📈 Ort. İlgi Skoru", f"{avg_score_f:.1f}/100")
        
        with m2:
            st.metric("👥 Veli Sayısı", total_resp_f)
        
        with m3:
            st.metric("⬆️ Yüksek İlgi", f"{high_ratio_f:.1f}%")
        
        with m4:
            st.metric("⬇️ Düşük İlgi", f"{low_ratio_f:.1f}%")
        
        st.markdown("---")
        
        # ===== FİLTRELENMİŞ DONUT =====
        st.subheader("🎯 İlgi Skoru Kategorilerinin Dağılımı (Filtrelenmiş)")
        
        high_f = (filtered_df["ebeveyn_ilgi_skoru_100"] >= 70).sum()
        medium_f = ((filtered_df["ebeveyn_ilgi_skoru_100"] >= 40) & (filtered_df["ebeveyn_ilgi_skoru_100"] < 70)).sum()
        low_f = (filtered_df["ebeveyn_ilgi_skoru_100"] < 40).sum()
        
        donut_data_f = {
            "Kategori": ["Yüksek İlgi (70+)", "Orta İlgi (40-69)", "Düşük İlgi (<40)"],
            "Sayı": [high_f, medium_f, low_f],
            "Yüzde": [
                (high_f / total_resp_f * 100) if total_resp_f > 0 else 0,
                (medium_f / total_resp_f * 100) if total_resp_f > 0 else 0,
                (low_f / total_resp_f * 100) if total_resp_f > 0 else 0
            ]
        }
        donut_df_f = pd.DataFrame(donut_data_f)
        
        fig_donut_f = go.Figure(data=[go.Pie(
            labels=donut_df_f["Kategori"],
            values=donut_df_f["Sayı"],
            hole=0.4,
            marker=dict(colors=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE]),
            text=[f"{x:.1f}%" for x in donut_df_f["Yüzde"]],
            textposition="inside",
            hovertemplate="<b>%{label}</b><br>Sayı: %{value}<br>Yüzde: %{customdata:.1f}%<extra></extra>",
            customdata=donut_df_f["Yüzde"]
        )])
        
        fig_donut_f.update_layout(
            font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
            paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
            plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
            height=450
        )
        
        st.plotly_chart(fig_donut_f, use_container_width=True)
        
        high_f_pct = (high_f / total_resp_f * 100) if total_resp_f > 0 else 0
        high_f_all = (high_f / total_resp * 100) if total_resp > 0 else 0
        st.info(f"📌 **Filtrelenmiş Grup - Kategori Dağılımı Analizi:** Seçili demografik grup içerisinde, ilgi skoru 70+ olan (Yüksek İlgi) ebeveynler %{high_f_pct:.1f} oranında yer almakta, orta ilgi grubu (%{donut_df_f.iloc[1]['Yüzde']:.1f}) ile düşük ilgi grubu (%{donut_df_f.iloc[2]['Yüzde']:.1f})'nun dağılımını oluşturmaktadır. Filtreleme öncesi genel popülasyon içerisinde yüksek ilgi oranı %{high_f_all:.1f} olurken, mevcut seçimde bu oran, filtreleme kriterlerinin bilinçli ebeveyn profilini ne kadar iyi hedeflediğinin göstergesidir. Kategori içi yoğunluk analizi, belirli demografik özelliklerin oyun güvenliği konusundaki farkındalık düzeyini ne ölçüde etkilediğini ortaya koymaktadır. Söz konusu dağılım, hedeflenmiş ebeveyn bilinçlendirme kampanyalarının tasarlanması ve uygulanması için kritik bir veri kaynağı oluşturmaktadır. Diğer taraftan, bu filtrelenmiş grup ve genel populasyon arasındaki fark, hangi demografik kombinasyonların en etkin eğitim müdahaleleri için öncelik alması gerektiğini belirlemede yardımcı olmaktadır.")
        
        st.markdown("---")
        
        # ===== FİLTRELENMİŞ HİSTOGRAM =====
        st.subheader("📊 İlgi Skoru Dağılımı (Filtrelenmiş)")
        
        try:
            fig_hist_f = go.Figure(data=[go.Histogram(
                x=filtered_df["ebeveyn_ilgi_skoru_100"],
                nbinsx=10,
                marker=dict(color=COLOR_DARK_BLUE, line=dict(color=COLOR_GOLD, width=2))
            )])
            
            fig_hist_f.update_layout(
                xaxis_title="İlgi Skoru",
                yaxis_title="Veli Sayısı",
                font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_hist_f, use_container_width=True)
        except:
            # Fallback: Bar grafiğe çevir
            score_dist_f = filtered_df["ebeveyn_ilgi_skoru_100"].value_counts().sort_index()
            fig_bar_f = go.Figure(data=[go.Bar(
                x=score_dist_f.index,
                y=score_dist_f.values,
                marker=dict(color=COLOR_DARK_BLUE)
            )])
            fig_bar_f.update_layout(
                xaxis_title="İlgi Skoru",
                yaxis_title="Sayı",
                font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig_bar_f, use_container_width=True)
        
        median_score_f = filtered_df["ebeveyn_ilgi_skoru_100"].median()
        mean_score_f = filtered_df["ebeveyn_ilgi_skoru_100"].mean()
        std_score_f = filtered_df["ebeveyn_ilgi_skoru_100"].std()
        q1_f = filtered_df["ebeveyn_ilgi_skoru_100"].quantile(0.25)
        q3_f = filtered_df["ebeveyn_ilgi_skoru_100"].quantile(0.75)
        iqr_f = q3_f - q1_f
        range_f = filtered_df["ebeveyn_ilgi_skoru_100"].max() - filtered_df["ebeveyn_ilgi_skoru_100"].min()
        skewness_f = "sağa" if mean_score_f > median_score_f else "sola"
        
        st.success(f"📊 **Filtrelenmiş Grup - İstatistiksel Profili:** Seçili ebeveyn grubu içerisinde ilgi skoru dağılımı, ortalama {mean_score_f:.2f} ve medyan {median_score_f:.2f} değerleriyle {skewness_f} yönde çarpıklık göstermektedir. Standart sapma {std_score_f:.2f} seviyesinde tespit edilerek, grup içindeki tutum heterojenliğinin derecesini aydınlatmaktadır. Çeyrek aralık analizi (Q1: {q1_f:.1f}, Q3: {q3_f:.1f}, İQR: {iqr_f:.1f}), temel veri kümesinin yerişimini ve konsantrasyonunu göstermekte, toplam skör aralığı ({range_f:.1f} puan) ise eşik değerleri ortaya koymaktadır. Bu filtrelenmiş grup profili, genel populasyonla karşılaştırıldığında, demografik faktörlerin ebeveyn bilinçlendirme düzeyini ne ölçüde diferensiye ettiğini ortaya koymaktadır. Dolayısıyla, bu istatistiksel profil, çocuk güvenliği perspektifinden, mezkur demografik gruba yönelik özelçı tasarlanmış müdahalelerin gerekliliğini desteklemektedir.")
        
        st.markdown("---")
        
        # ===== FİLTRELENMİŞ BOXPLOT: CİNSİYET =====
        st.subheader("👥 Cinsiyet Açısından İlgi Skoru (Filtrelenmiş)")
        
        if "veli_cinsiyet" in filtered_df.columns and len(filtered_df) > 0:
            try:
                fig_box_gender_f = px.box(
                    filtered_df,
                    x="veli_cinsiyet",
                    y="ebeveyn_ilgi_skoru_100",
                    title="",
                    labels={"veli_cinsiyet": "Veli Cinsiyeti", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"},
                    color="veli_cinsiyet",
                    color_discrete_sequence=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE]
                )
                
                fig_box_gender_f.update_layout(
                    font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                    paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                    plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_box_gender_f, use_container_width=True)
            except:
                # Fallback: Scatter grafiğe çevir
                fig_scatter_gender_f = px.scatter(
                    filtered_df,
                    x="veli_cinsiyet",
                    y="ebeveyn_ilgi_skoru_100",
                    title="",
                    labels={"veli_cinsiyet": "Veli Cinsiyeti", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"},
                    color="veli_cinsiyet",
                    color_discrete_sequence=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE],
                    size_max=15
                )
                
                fig_scatter_gender_f.update_layout(
                    font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                    paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                    plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_scatter_gender_f, use_container_width=True)
        
        gender_stats_f = filtered_df.groupby("veli_cinsiyet")["ebeveyn_ilgi_skoru_100"].agg(['mean', 'median', 'std', 'min', 'max', 'count'])
        if len(gender_stats_f) > 0:
            gender_f_sorted = gender_stats_f.sort_values('mean', ascending=False)
            top_g_f = gender_f_sorted.index[0]
            top_mean_f = gender_f_sorted.iloc[0]['mean']
            top_std_f = gender_f_sorted.iloc[0]['std']
            top_count_f = int(gender_f_sorted.iloc[0]['count'])
            if len(gender_f_sorted) > 1:
                bottom_g_f = gender_f_sorted.index[-1]
                bottom_mean_f = gender_f_sorted.iloc[-1]['mean']
                gender_diff_f = top_mean_f - bottom_mean_f
                st.info(f"💡 **Filtrelenmiş Grup - Cinsiyet Bazlı Farkındalık:** {top_g_f} ebeveynlerin bu filtrelenmiş segment içerisindeki ortalama skoru {top_mean_f:.2f} olup, {bottom_g_f} ebeveynlerin skoru {bottom_mean_f:.2f}'dir; fark {gender_diff_f:.2f} puandır (n={top_count_f} vs n={int(gender_f_sorted.iloc[-1]['count'])}). Genel popülasyon içindeki cinsiyet farkı ile bu filtrelenmiş grup içindeki farkın karşılaştırılması, demografik interaksiyon etkilerinin nasıl çalıştığını aydınlatmaktadır. Standart sapmaların farklılığı ({top_std_f:.2f} vs {gender_f_sorted.iloc[-1]['std']:.2f}), belirli cinsiyet grupları içinde daha veya daha az tutarlı tutumların olduğunu göstermektedir. Bu bulgu, oyun güvenliği politikalarının belirlenmesi aşamasında, çok katmanlı demografik bileşenler düşünülmesi gerektiğini ortaya koymaktadır.")
            else:
                st.info(f"💡 **Filtrelenmiş Grup - Cinsiyet Profili:** Bu örneklemde {top_g_f} ebeveynler baskın olup (n={top_count_f}), ortalama skoru {top_mean_f:.2f}, standart sapması {top_std_f:.2f}'dir. Cinsiyet dağılımının tek gruba yoğunlaşması, karşılaştırmalı analiz kapasitesini sınırlandırmakta, dolaysıyla cinsiyet-bazlı müdahalelerin içeriğinin bu spesifik segment için contextualize edilmesi gerektiğini ortaya koymaktadır.")
        
        st.markdown("---")
        
        # ===== FİLTRELENMİŞ BOXPLOT: RUH HALI =====
        st.subheader("😊 Ruh Hali Gözlemi ile İlgi Skoru (Filtrelenmiş)")
        
        if "cocuk_ruh_hali_gozlemi" in filtered_df.columns and len(filtered_df) > 0:
            try:
                fig_box_mood_f = px.box(
                    filtered_df,
                    x="cocuk_ruh_hali_gozlemi",
                    y="ebeveyn_ilgi_skoru_100",
                    title="",
                    labels={"cocuk_ruh_hali_gozlemi": "Çocuk Ruh Hali", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"},
                    color="cocuk_ruh_hali_gozlemi",
                    color_discrete_sequence=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE]
                )
                
                fig_box_mood_f.update_layout(
                    font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                    paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                    plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_box_mood_f, use_container_width=True)
            except:
                # Fallback: Scatter grafiğe çevir
                fig_scatter_mood_f = px.scatter(
                    filtered_df,
                    x="cocuk_ruh_hali_gozlemi",
                    y="ebeveyn_ilgi_skoru_100",
                    title="",
                    labels={"cocuk_ruh_hali_gozlemi": "Çocuk Ruh Hali", "ebeveyn_ilgi_skoru_100": "İlgi Skoru"},
                    color="cocuk_ruh_hali_gozlemi",
                    color_discrete_sequence=[COLOR_DARK_BLUE, COLOR_GOLD, COLOR_VERY_LIGHT_BLUE],
                    size_max=15
                )
                
                fig_scatter_mood_f.update_layout(
                    font=dict(family="Arial, sans-serif", size=12, color=COLOR_TEXT_DARK),
                    paper_bgcolor=COLOR_VERY_LIGHT_BLUE,
                    plot_bgcolor=COLOR_VERY_LIGHT_BLUE,
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_scatter_mood_f, use_container_width=True)
        
        mood_stats_f = filtered_df.groupby("cocuk_ruh_hali_gozlemi")["ebeveyn_ilgi_skoru_100"].agg(['mean', 'median', 'std', 'min', 'max', 'count']).sort_values('mean', ascending=False)
        if len(mood_stats_f) > 0:
            best_mood_f = mood_stats_f.index[0]
            best_mean_f = mood_stats_f.iloc[0]['mean']
            best_std_f = mood_stats_f.iloc[0]['std']
            best_count_f = int(mood_stats_f.iloc[0]['count'])
            worst_mood_f = mood_stats_f.index[-1]
            worst_mean_f = mood_stats_f.iloc[-1]['mean']
            worst_count_f = int(mood_stats_f.iloc[-1]['count'])
            mood_diff_f = best_mean_f - worst_mean_f
            st.success(f"🎯 **Filtrelenmiş Grup - Ruh Hali ve İlgi İlişkisi:** Bu demografik segment içerisinde, {best_mood_f} ruh haline sahip çocuklara başlayan ebeveynler ortalama {best_mean_f:.2f} skor almakta (Std: {best_std_f:.2f}, n={best_count_f}), diğer taraftan {worst_mood_f} ruh halini gözleyen ebeveynler {worst_mean_f:.2f} skor elde etmektedirler (n={worst_count_f}). Aralarındaki {mood_diff_f:.2f} puantlık fark, bu spesifik demografik grubun içerisinde çocuğun psikososyal durumunun, ebeveyn oyun güvenliği farkındalığının ne kadar kritik bir belirleyicisi olduğunu göstermektedir. Söz konusu korelasyon, genel popülasyonla karşılaştırıldığında, hangi demografik kombinasyonun bu ilişkiyi daha güçlü hale getirdiğini ortaya koymaktadır. Dolayısıyla, oyun güvenliği perspektifinden, bu gruba yönelik müdahalelerin çocuğun psikolojik refaha odaklanması bağlamında tasarlanması, stratejik önem taşımaktadır.")

else:
    st.warning("Veriler yüklenemediği için analiz gösterilemiyor.")
