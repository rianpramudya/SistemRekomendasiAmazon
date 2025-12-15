import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
import json
import os

def evaluate_model_cv():
    print("📈 Memulai Evaluasi 5-Fold Cross Validation...")
    
    df = pd.read_csv('data/clean_ratings.csv')
    
    # Sampling user agar tidak terlalu lama (1000 user cukup untuk estimasi)
    unique_users = df['userId'].unique()
    if len(unique_users) > 1000:
        sampled_users = unique_users[:1000]
    else:
        sampled_users = unique_users
        
    df_sample = df[df['userId'].isin(sampled_users)]
    
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    fold_precision = []
    fold_recall = []
    fold_f1 = []
    
    fold_idx = 1
    
    for train_index, test_index in kf.split(df_sample):
        print(f"   🔄 Processing Fold {fold_idx}/5...")
        
        train_data = df_sample.iloc[train_index]
        test_data = df_sample.iloc[test_index]
        
        # Build Model (Train)
        pivot_train = train_data.pivot_table(index='userId', columns='productId', values='rating').fillna(0)
        matrix_train = csr_matrix(pivot_train.values)
        
        svd = TruncatedSVD(n_components=30, random_state=42)
        matrix_reduced = svd.fit_transform(matrix_train)
        
        kmeans = KMeans(n_clusters=8, random_state=42, n_init=5)
        kmeans.fit(matrix_reduced)
        
        # Evaluation Logic (Test)
        test_users_in_train = [u for u in test_data['userId'].unique() if u in pivot_train.index]
        
        precisions = []
        recalls = []
        
        for user in test_users_in_train:
            # Ground Truth: Barang yang user ini beri rating >= 4 di data Test
            actual_liked = test_data[(test_data['userId'] == user) & (test_data['rating'] >= 4)]['productId'].values
            
            if len(actual_liked) == 0: continue
            
            # 1. Tentukan Cluster User
            user_idx = pivot_train.index.get_loc(user)
            user_vector = matrix_reduced[user_idx].reshape(1, -1)
            cluster_id = kmeans.predict(user_vector)[0]
            
            # 2. Cari Top Items di Cluster (Pakai SUM/Popularity)
            cluster_users_idx = np.where(kmeans.labels_ == cluster_id)[0]
            
            # Menggunakan .sum() agar konsisten dengan train_model.py
            # Kita ambil langsung dari matrix sparse agar cepat
            cluster_submatrix = matrix_train[cluster_users_idx]
            cluster_scores = np.array(cluster_submatrix.sum(axis=0)).flatten()
            
            # Ambil Top 10 Index
            top_indices = cluster_scores.argsort()[::-1][:10]
            rec_items = [pivot_train.columns[i] for i in top_indices]
            
            # 3. Hitung Metrik
            hits = len(set(actual_liked).intersection(rec_items))
            p = hits / 10.0
            r = hits / len(actual_liked)
            
            precisions.append(p)
            recalls.append(r)
            
        if precisions:
            fold_precision.append(np.mean(precisions))
            fold_recall.append(np.mean(recalls))
            f1 = 2 * (np.mean(precisions) * np.mean(recalls)) / (np.mean(precisions) + np.mean(recalls)) if (np.mean(precisions) + np.mean(recalls)) > 0 else 0
            fold_f1.append(f1)
            
        fold_idx += 1

    final_metrics = {
        "precision": float(np.mean(fold_precision)),
        "recall": float(np.mean(fold_recall)),
        "f1_score": float(np.mean(fold_f1)),
        "n_folds": 5
    }

    with open('models/metrics.json', 'w') as f:
        json.dump(final_metrics, f)

    print("\n✅ Evaluasi Selesai & Disimpan.")
    print(f"Precision : {final_metrics['precision']:.4f}")
    print(f"Recall    : {final_metrics['recall']:.4f}")
    print(f"F1-Score  : {final_metrics['f1_score']:.4f}")

if __name__ == "__main__":
    evaluate_model_cv()