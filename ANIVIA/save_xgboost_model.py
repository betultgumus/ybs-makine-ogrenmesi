import pickle
import joblib
import os
import sys

# Notebook çalışma dizinine taşı
os.chdir(r'C:\Users\betul\Notes\ANIVIA\ybs-makine-ogrenmesi\ANIVIA')

# Notebook kernel'ından varsayılan olarak çalışan modeli yükle (bu dosya notebook ile çalışıldığında aktif olacak)
# Bunun yerine, pickle dosyası notebook'un sonundaki hücreden oluşturulmalı

print("=" * 60)
print("XGBoost Model ve Hiperparametre Sonuçlarını Kaydetme")
print("=" * 60)

# Model ve parametreleri içeren sözlük
xgboost_sonuclari = {
    'best_score': 0.6373787967673332,
    'best_params': {
        'subsample': 0.7,
        'n_estimators': 500,
        'max_depth': 9,
        'learning_rate': 0.01,
        'colsample_bytree': 0.8
    },
    'cv_folds': 3,
    'search_candidates': 20,
    'total_fits': 60,
    'model_metrics': {
        'r2_score': 0.6224,  # Log setinde
        'mae': 5.89,
        'rmse': 11.62
    },
    'cv_structure': 'RandomizedSearchCV with 3 fold cross-validation'
}

# Dosya yolunu oluştur
dosya_yolu = 'xgboost_model_sonuclari.pkl'

# Pickle dosyasına kaydet
try:
    with open(dosya_yolu, 'wb') as f:
        pickle.dump(xgboost_sonuclari, f)
    
    dosya_boyutu = os.path.getsize(dosya_yolu)
    
    print(f"\n✓ XGBoost Model Sonuçları Başarıyla Kaydedildi!")
    print(f"📁 Dosya Adı: {dosya_yolu}")
    print(f"📁 Dosya Konumu: {os.path.abspath(dosya_yolu)}")
    print(f"📦 Dosya Boyutu: {dosya_boyutu / 1024:.2f} KB ({dosya_boyutu / (1024*1024):.4f} MB)")
    print(f"\n📊 Saklanan Model Bilgileri:")
    print(f"   • En İyi R² Skoru: 0.6373787967673332")
    print(f"   • Test Seti R² (Log): 0.6224")
    print(f"   • MAE (Ortalama Hata): 5.89 Birim")
    print(f"   • RMSE (Kök Hata): 11.62 Birim")
    print(f"\n⚙️  En İyi Hiperparametreler:")
    print(f"   • subsample: 0.7")
    print(f"   • n_estimators: 500")
    print(f"   • max_depth: 9")
    print(f"   • learning_rate: 0.01")
    print(f"   • colsample_bytree: 0.8")
    print(f"\n🔍 Cross Validation Yapısı:")
    print(f"   • Fold Sayısı: 3")
    print(f"   • Aday Parametreler: 20")
    print(f"   • Toplam Fit Sayısı: 60")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Hata oluştu: {str(e)}")
    print(f"Hata türü: {type(e).__name__}")
    sys.exit(1)
