import pandas as pd
import joblib
import os
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans

def train_and_eval():
    print("🚀 Memulai Training Model-Based (Clustering K-Means)...")
    
    file_path = 'data/clean_ratings.csv'
    if not os.path.exists(file_path):
        print("❌ Data tidak ditemukan.")
        return

    df = pd.read_csv(file_path)
    
    # 1. Pivot Table
    print("🔄 Membuat Matrix User-Item...")
    user_item_pivot = df.pivot_table(index='userId', columns='productId', values='rating').fillna(0)
    user_item_matrix = csr_matrix(user_item_pivot.values)
    
    # 2. SVD (Dimensionality Reduction)
    print("📉 Melakukan Reduksi Dimensi (SVD)...")
    svd = TruncatedSVD(n_components=50, random_state=42)
    matrix_reduced = svd.fit_transform(user_item_matrix)
    
    # 3. K-Means Clustering
    print("🧠 Melatih Model K-Means...")
    n_clusters = 10 
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(matrix_reduced)
    
    cluster_labels = kmeans.labels_
    
    # 4. Pre-compute Recommendations (IMPROVED LOGIC: SUM instead of MEAN)
    print("⚡ Menghitung Top Items per Cluster (Popularity Based)...")
    top_items_per_cluster = {}
    
    # Mapping User Index -> Cluster
    user_cluster_map = pd.DataFrame({
        'user_idx': range(len(user_item_pivot)),
        'cluster': cluster_labels
    })

    for cluster_id in range(n_clusters):
        # Ambil index user di cluster ini
        u_indices = user_cluster_map[user_cluster_map['cluster'] == cluster_id]['user_idx'].values
        
        # Ambil subset matriks (Sparse operation = Cepat)
        cluster_submatrix = user_item_matrix[u_indices]
        
        # Hitung Total Rating per produk (Summing Axis 0)
        # Logic: Barang populer di komunitas ini = Sum Rating Tinggi
        cluster_scores = np.array(cluster_submatrix.sum(axis=0)).flatten()
        
        # Ambil Top 50 Index Produk
        top_indices = cluster_scores.argsort()[::-1][:50]
        
        # Translate ke ASIN
        top_products = [user_item_pivot.columns[i] for i in top_indices]
        top_items_per_cluster[cluster_id] = top_products

    # 5. Simpan Model
    print("💾 Menyimpan Model...")
    artifacts = {
        'svd': svd,
        'kmeans': kmeans,
        'user_item_pivot': user_item_pivot, 
        'top_items_per_cluster': top_items_per_cluster
    }
    
    if not os.path.exists('models'):
        os.makedirs('models')

    joblib.dump(artifacts, 'models/recsys_model.pkl')
    print("✅ Model Clustering berhasil disimpan!")

if __name__ == "__main__":
    train_and_eval()