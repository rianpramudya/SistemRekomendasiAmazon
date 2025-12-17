import pandas as pd
import numpy as np
import os
import joblib
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

def process_data():
    print("🔄 [1/2] Memuat dataset raw...")
    input_path = 'data/ratings_Electronics.csv'
    
    # Cek folder data dan models
    if not os.path.exists('data'): os.makedirs('data')
    if not os.path.exists('models'): os.makedirs('models')

    if not os.path.exists(input_path):
        print(f"❌ Error: File {input_path} tidak ditemukan. Pastikan file ada di folder data/.")
        return

    # 1. Load Data
    # Menggunakan tipe data hemat memori
    df = pd.read_csv(
        input_path, 
        names=['userId', 'productId', 'rating', 'timestamp'],
        dtype={'rating': 'float32', 'timestamp': 'int64'}
    )
    df.drop('timestamp', axis=1, inplace=True)

    # 2. Filtering (Data Cleaning)
    print("🧹 [2/2] Filtering Active Users & Products...")
    
    # Filter User (Minimal 50 interaksi)
    min_ratings = 50
    user_counts = df['userId'].value_counts()
    active_users = user_counts[user_counts >= min_ratings].index
    df_filtered = df[df['userId'].isin(active_users)]
    
    # Filter Produk (Minimal 5 interaksi)
    min_product_ratings = 5
    product_counts = df_filtered['productId'].value_counts()
    active_products = product_counts[product_counts >= min_product_ratings].index
    df_final = df_filtered[df_filtered['productId'].isin(active_products)]
    
    # Simpan CSV bersih (untuk keperluan Evaluate nanti)
    df_final.to_csv('data/clean_ratings.csv', index=False)
    print(f"✅ Data Bersih: {len(df_final):,} baris tersimpan di data/clean_ratings.csv")
    
    # 3. Pivot Table & Sparse Matrix
    print("📊 Membuat Matrix User-Item...")
    user_item_pivot = df_final.pivot_table(index='userId', columns='productId', values='rating').fillna(0)
    user_item_matrix = csr_matrix(user_item_pivot.values)
    
    # 4. SVD (DIMENSIONALITY REDUCTION) - Dipindah ke sini sebagai preprocessing
    print("📉 Menjalankan SVD (Feature Extraction)...")
    svd = TruncatedSVD(n_components=50, random_state=42)
    matrix_reduced = svd.fit_transform(user_item_matrix)
    
    # 5. Simpan Hasil Preprocessing (Fitur Siap Pakai)
    print("💾 Menyimpan Fitur SVD & Matrix...")
    preprocessed_data = {
        'user_item_pivot': user_item_pivot,
        'user_item_matrix': user_item_matrix, # Disimpan untuk hitung popularity nanti
        'matrix_reduced': matrix_reduced,     # Ini input untuk K-Means
        'svd_model': svd                      # Disimpan untuk inferensi di Dashboard
    }
    
    joblib.dump(preprocessed_data, 'data/preprocessed_features.pkl')
    print("✅ Preprocessing & SVD Selesai! File tersimpan di 'data/preprocessed_features.pkl'")

if __name__ == "__main__":
    process_data()