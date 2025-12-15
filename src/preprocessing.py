import pandas as pd
import os

def process_data():
    print("🔄 Memuat dataset raw... (Optimized Memory)")
    
    input_path = 'data/ratings_Electronics.csv'
    output_path = 'data/clean_ratings.csv'
    
    if not os.path.exists(input_path):
        print(f"❌ Error: File {input_path} tidak ditemukan.")
        return

    # LOAD DENGAN TIPE DATA HEMAT MEMORI
    df = pd.read_csv(
        input_path, 
        names=['userId', 'productId', 'rating', 'timestamp'],
        dtype={'rating': 'float32', 'timestamp': 'int64'} # Optimasi RAM
    )
    
    df.drop('timestamp', axis=1, inplace=True)
    print(f"📊 Data Awal: {len(df):,} baris")

    # --- FILTERING ---
    # User aktif minimal 50 rating
    min_ratings = 50
    user_counts = df['userId'].value_counts()
    active_users = user_counts[user_counts >= min_ratings].index
    
    df_filtered = df[df['userId'].isin(active_users)]
    
    # Optional: Filter Produk yang minimal pernah dirating 5 kali (mengurangi noise)
    min_product_ratings = 5
    product_counts = df_filtered['productId'].value_counts()
    active_products = product_counts[product_counts >= min_product_ratings].index
    df_final = df_filtered[df_filtered['productId'].isin(active_products)]
    
    print(f"✅ Data Bersih: {len(df_final):,} baris")
    print(f"   - User Unik: {df_final['userId'].nunique()}")
    print(f"   - Produk Unik: {df_final['productId'].nunique()}")

    df_final.to_csv(output_path, index=False)
    print(f"💾 Data tersimpan di: {output_path}")

if __name__ == "__main__":
    process_data()