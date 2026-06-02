import pandas as pd
import numpy as np
from pathlib import Path

csv_path = Path("ANIVIA/game-regulation-analytics/data/processed/veliler_temiz.csv")
df = pd.read_csv(csv_path)

mapping_onay = {
    "Kesinlikle destekliyorum": 100,
    "Destekliyorum": 75,
    "Kararsızım": 50,
    "Desteklemiyorum": 25,
}

mapping_pegi = {
    "Evet her zaman": 100,
    "Bazen": 60,
    "Hayır kontrol etmiyorum": 20,
    "PEGI nedir bilmiyorum": 10,
}

mapping_denetim = {
    "Evet, teknik ayarları (filtre, süre sınırı) aktif olarak kullanıyorum.": 100,
    "Nasıl yapılacağını biliyorum ama uygulamıyorum.": 50,
    "Bu tür ayarların nasıl yapıldığını bilmiyorum.": 20,
    "Cihazlarda böyle özelliklerin olduğundan haberdar değilim.": 10,
}

def calculate_score(row):
    scores = []
    
    if pd.notna(row.get('veli_ebeveyn_onay_gorus')):
        scores.append(mapping_onay.get(row['veli_ebeveyn_onay_gorus'], 50))
    
    if pd.notna(row.get('veli_platform_kisitlama_gorus')):
        scores.append(mapping_onay.get(row['veli_platform_kisitlama_gorus'], 50))
    
    if pd.notna(row.get('veli_pegi_kontrol')):
        scores.append(mapping_pegi.get(row['veli_pegi_kontrol'], 30))
    
    if pd.notna(row.get('veli_ebeveyn_denetimi')):
        scores.append(mapping_denetim.get(row['veli_ebeveyn_denetimi'], 40))
    
    return np.mean(scores) if scores else 50

df['ebeveyn_ilgi_skoru_100'] = df.apply(calculate_score, axis=1)

output_path = Path("ANIVIA/game-regulation-analytics/data/processed/veliler_skorlu.csv")
df.to_csv(output_path, index=False, encoding='utf-8')

print("✅ veliler_skorlu.csv oluşturuldu")
print(f"Ortalama Score: {df['ebeveyn_ilgi_skoru_100'].mean():.2f}")
print(f"Veri sayısı: {len(df)}")
