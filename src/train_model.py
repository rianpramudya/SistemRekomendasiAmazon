import joblib
import os
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

def train_model():
    print("🚀 Memulai Training Model (K-Means Clustering Only)...")
    
    feature_path = 'data/preprocessed_features.pkl'
    if not os.path.exists(feature_path):
        print("❌ File fitur tidak ditemukan. Jalankan 'python src/preprocessing.py' terlebih dahulu!")
        return

    # 1. Load Data Hasil Preprocessing
    print("📥 Memuat Fitur SVD dari Preprocessing...")
    data = joblib.load(feature_path)
    
    matrix_reduced = data['matrix_reduced']     # Data hasil SVD (Fitur Laten)
    user_item_matrix = data['user_item_matrix'] # Data asli (sparse) untuk hitung rating
    user_item_pivot = data['user_item_pivot']   # Untuk nama kolom/produk
    svd_model = data['svd_model']               # Untuk dashboard nanti
    
    # 2. Training K-Means
    print(f"🧠 Melatih K-Means pada {matrix_reduced.shape[0]} user...")
    n_clusters = 10 
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    
    # Training hanya menggunakan data yang SUDAH di-SVD (preprocessing)
    kmeans.fit(matrix_reduced) 
    
    cluster_labels = kmeans.labels_
    
    # 3. Hitung Rekomendasi (Popularity per Cluster)
    print("⚡ Menghitung Top Items per Cluster (Popularity Based)...")
    top_items_per_cluster = {}
    
    # Helper dataframe untuk mapping User -> Cluster
    user_cluster_map = pd.DataFrame({
        'user_idx': range(len(user_item_pivot)),
        'cluster': cluster_labels
    })

    for cluster_id in range(n_clusters):
        # Ambil index user yang masuk ke dalam cluster ini
        u_indices = user_cluster_map[user_cluster_map['cluster'] == cluster_id]['user_idx'].values
        
        # Ambil data rating asli mereka (dari matrix sparse agar cepat)
        cluster_submatrix = user_item_matrix[u_indices]
        
        # Hitung Popularitas: Total Rating (SUM) per produk dalam cluster
        # Semakin tinggi jumlah rating, semakin populer barang tersebut di komunitas ini
        cluster_scores = np.array(cluster_submatrix.sum(axis=0)).flatten()
        
        # Ambil Top 50 Produk dengan skor tertinggi
        top_indices = cluster_scores.argsort()[::-1][:50]
        
        # Translate index kembali ke ID Produk (ASIN)
        top_products = [user_item_pivot.columns[i] for i in top_indices]
        
        top_items_per_cluster[cluster_id] = top_products

    # 4. Simpan Model Akhir untuk Aplikasi
    print("💾 Menyimpan Model Akhir...")
    final_artifacts = {
        'kmeans': kmeans,
        'svd': svd_model, # SVD tetap disimpan untuk memproses input user baru di Dashboard
        'user_item_pivot': user_item_pivot,
        'top_items_per_cluster': top_items_per_cluster
    }
    
    if not os.path.exists('models'):
        os.makedirs('models')
        
    joblib.dump(final_artifacts, 'models/recsys_model.pkl')
    print("✅ Model K-Means berhasil dilatih dan disimpan di 'models/recsys_model.pkl'!")

if __name__ == "__main__":
    train_model()