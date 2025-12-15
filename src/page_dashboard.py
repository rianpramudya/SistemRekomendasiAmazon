import streamlit as st
import pandas as pd
import time
import requests
import random
from bs4 import BeautifulSoup
import src.ui_components as ui

# --- HELPER: ROBUST LIVE SCRAPING V3 (MAXIMIZED) ---
@st.cache_data(show_spinner=False)
def fetch_product_name_live(asin):
    """
    Mengambil nama produk dari Amazon dengan 4 Lapis Strategi Anti-Bot.
    """
    url = f"https://www.amazon.com/dp/{asin}"
    
    # 1. Rotasi User-Agent yang lebih lengkap (Menyamar sebagai user asli)
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/"
    }
    
    try:
        # Timeout 4 detik agar UI tidak hang
        response = requests.get(url, headers=headers, timeout=4) 
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # --- STRATEGI 1: ID Standar Amazon ---
            title_node = soup.find("span", {"id": "productTitle"})
            
            # --- STRATEGI 2: Fallback ke H1 (Mobile View/Deal Page) ---
            if not title_node:
                title_node = soup.find("h1", {"id": "title"})
            
            # --- STRATEGI 3: Fallback ke Meta Tags ---
            if not title_node:
                meta_title = soup.find("meta", {"name": "title"})
                if meta_title:
                    return meta_title.get("content").strip()
            
            # --- STRATEGI 4: Browser Tab Title (PALING KUAT) ---
            # "Amazon.com: Nama Produk : Electronics" -> Kita ambil tengahnya
            if not title_node and soup.title:
                raw_title = soup.title.string
                clean_title = raw_title.replace("Amazon.com:", "").replace("Amazon.com :", "").split(":")[0].strip()
                if len(clean_title) > 3: # Pastikan bukan string kosong
                    return clean_title

            # Return hasil dari strategi 1 atau 2
            if title_node:
                return title_node.get_text().strip()
        
        elif response.status_code == 503:
            print(f"⚠️ Amazon 503 (Bot Detected) for {asin}")
            
    except Exception as e:
        print(f"❌ Error fetching {asin}: {str(e)}")
        pass
        
    # Fallback terakhir jika semua gagal
    return f"Product ID: {asin}"

# --- LOGIC UTAMA HALAMAN ---
def render(artifacts):
    pivot_table = artifacts['user_item_pivot']
    
    # Hero Header
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="margin-bottom: 8px;">Electronics Recommender</h1>
        <div style="display: flex; align-items: center; gap: 8px; color: #848991; font-size: 14px;">
            <i class="ph-fill ph-cpu"></i> AI-Powered Discovery Engine
            <span style="color: #2A3038;">|</span>
            <span style="color: #FF9900;">v3.2 Stable</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics Row
    c1, c2, c3 = st.columns(3)
    with c1: ui.render_metric_card("ACTIVE USERS", f"{pivot_table.shape[0]:,}", "ph-users")
    with c2: ui.render_metric_card("PRODUCT CATALOG", f"{pivot_table.shape[1]:,}", "ph-package")
    with c3: ui.render_metric_card("CLUSTERS", "10", "ph-graph")

    st.markdown("---")

    # Inputs Section
    col_input, col_param, col_opt = st.columns([2, 1, 1])
    
    with col_input:
        st.markdown("##### <i class='ph-bold ph-user-focus'></i> Target Profile", unsafe_allow_html=True)
        all_users = pivot_table.index.tolist()
        user_id = st.selectbox("Select Active User ID", all_users[:20], label_visibility="collapsed")
    
    with col_param:
        st.markdown("##### <i class='ph-bold ph-sliders'></i> Limit", unsafe_allow_html=True)
        top_n = st.number_input("Top N Items", 5, 20, 10, label_visibility="collapsed")
    
    with col_opt:
        st.markdown("##### <i class='ph-bold ph-globe'></i> Metadata", unsafe_allow_html=True)
        use_live_fetch = st.checkbox("Fetch Names (Live)", value=True, help="Enable scraping to see real product names.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("RUN ANALYSIS ENGINE", use_container_width=True):
        _run_inference(artifacts, user_id, top_n, use_live_fetch)

def _run_inference(artifacts, user_id, top_n, use_live_fetch):
    container = st.container()
    
    with container:
        start_time = time.time()
        
        progress_text = "Initializing Engine..."
        my_bar = st.progress(0, text=progress_text)
        time.sleep(0.2)
        
        my_bar.progress(20, text="Vectorizing User Profile (SVD)...")
        
        pivot_table = artifacts['user_item_pivot']
        model = artifacts['kmeans']
        svd = artifacts['svd']
        top_items_map = artifacts['top_items_per_cluster']
        
        try:
            # 1. Transform & Predict
            user_idx = pivot_table.index.get_loc(user_id)
            user_vector = svd.transform(pivot_table.iloc[user_idx].values.reshape(1, -1))
            
            my_bar.progress(50, text="Identifying User Cluster...")
            cluster_id = model.predict(user_vector)[0]
            recommendations = top_items_map[cluster_id][:top_n]
            
            # 2. Fetch Data Loop
            results = []
            score_start = 0.98
            
            total = len(recommendations)
            for i, asin in enumerate(recommendations):
                # Update progress bar
                current = 60 + int((i / total) * 35)
                
                if use_live_fetch:
                    my_bar.progress(current, text=f"Fetching [{i+1}/{total}]: {asin}...")
                    name = fetch_product_name_live(asin)
                else:
                    name = "Enable 'Fetch Names' to see details"
                
                product_url = f"https://www.amazon.com/dp/{asin}"
                
                results.append({
                    "ASIN": asin,
                    "Product Name": name,
                    "Relevance Score": score_start,
                    "Link": product_url
                })
                score_start -= 0.03

            end_time = time.time()
            execution_time = end_time - start_time

            my_bar.progress(100, text=f"Analysis Complete ({execution_time:.2f}s)")
            time.sleep(0.5)
            my_bar.empty() 

            # --- DISPLAY RESULTS ---
            # FIX: Menggunakan keyword arguments agar sesuai dengan ui_components.py terbaru
            ui.render_insight_box(
                title=f"AI Cluster Analysis (Cluster #{cluster_id})",
                content=f"User diklasifikasikan ke dalam Cluster #{cluster_id}. Rekomendasi di bawah ini disusun berdasarkan item dengan popularitas tertinggi (Top-Sum Popularity) di dalam komunitas tersebut.",
                icon="ph-users-three"
            )
            
            st.caption(f"⚡ Inference finished in **{execution_time:.3f} seconds**")
            
            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ASIN": st.column_config.TextColumn("ASIN", width="small"),
                    "Product Name": st.column_config.TextColumn("Product Name", width="large"),
                    "Relevance Score": st.column_config.ProgressColumn(
                        "Relevance", 
                        format="%.2f", 
                        min_value=0, 
                        max_value=1
                    ),
                    "Link": st.column_config.LinkColumn(
                        "Action", 
                        display_text="View on Amazon"
                    )
                }
            )
            
        except Exception as e:
            st.error(f"Inference Error: {str(e)}")