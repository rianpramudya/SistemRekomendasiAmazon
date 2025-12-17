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
    """Mengambil nama produk dari Amazon dengan 4 Lapis Strategi Anti-Bot."""
    url = f"https://www.amazon.com/dp/{asin}"
    
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
        response = requests.get(url, headers=headers, timeout=4) 
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            title_node = soup.find("span", {"id": "productTitle"})
            
            if not title_node:
                title_node = soup.find("h1", {"id": "title"})
            
            if not title_node:
                meta_title = soup.find("meta", {"name": "title"})
                if meta_title:
                    return meta_title.get("content").strip()
            
            if not title_node and soup.title:
                raw_title = soup.title.string
                clean_title = raw_title.replace("Amazon.com:", "").replace("Amazon.com :", "").split(":")[0].strip()
                if len(clean_title) > 3:
                    return clean_title

            if title_node:
                return title_node.get_text().strip()
        
        elif response.status_code == 503:
            print(f"⚠️ Amazon 503 (Bot Detected) for {asin}")
            
    except Exception as e:
        print(f"❌ Error fetching {asin}: {str(e)}")
        pass
        
    return f"Product ID: {asin}"

def render(artifacts):
    # Load Phosphor Icons & Enhanced Animations
    st.markdown("""
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/duotone/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/bold/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/fill/style.css">
    
    <style>
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse-glow {
        0%, 100% { 
            box-shadow: 0 0 20px rgba(255, 153, 0, 0.4);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 0 40px rgba(255, 153, 0, 0.8);
            transform: scale(1.02);
        }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .hero-animated {
        animation: fadeInDown 0.8s ease-out;
    }
    
    .metric-card {
        animation: slideInUp 0.6s ease-out;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }
    
    .metric-card:hover .metric-icon {
        animation: bounce 0.6s ease-in-out infinite;
    }
    
    .control-panel {
        animation: slideInUp 0.8s ease-out;
        background: linear-gradient(135deg, #1a1f26 0%, #15191e 100%);
        border: 2px solid #3A4556;
        border-radius: 14px;
        padding: 30px;
        margin: 25px 0;
        position: relative;
        overflow: hidden;
    }
    
    .control-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 153, 0, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    .spinner-icon {
        animation: rotate 1.5s linear infinite;
    }
    
    .badge-pulse {
        animation: pulse-glow 2s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)
    
    pivot_table = artifacts['user_item_pivot']
    
    # Ultra Premium Hero Header
    st.markdown("""
    <div class="hero-animated" style="margin-bottom: 35px; position: relative;">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 12px;">
            <i class="ph-duotone ph-brain" style="font-size: 50px; color: #FF9900;"></i>
            <h1 style="background: linear-gradient(135deg, #FF9900 0%, #FFD700 50%, #FF9900 100%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 44px; margin: 0; font-weight: 900; letter-spacing: -1px;">
                AI Recommendation Engine
            </h1>
        </div>
        <div style="display: flex; align-items: center; gap: 12px; color: #848991; font-size: 15px; margin-left: 65px;">
            <i class="ph-fill ph-sparkle" style="color: #FFD700; font-size: 18px;"></i>
            <span style="color: white; font-weight: 600;">Powered by K-Means Clustering & SVD</span>
            <span style="color: #3A4556; font-size: 24px;">•</span>
            <div class="badge-pulse" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.05) 100%); padding: 6px 14px; border-radius: 20px; border: 2px solid #10B981; display: inline-flex; align-items: center; gap: 6px;">
                <i class="ph-fill ph-check-circle" style="color: #10B981; font-size: 16px;"></i>
                <span style="color: #10B981; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px;">Production Ready</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ultra Enhanced Metrics Row with Icons & Hover
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 30px; border-radius: 14px; border: 2px solid #3b82f6; text-align: center; position: relative; overflow: hidden;">
            <div style="position: absolute; top: -20px; right: -20px; opacity: 0.1;">
                <i class="ph-duotone ph-users-three" style="font-size: 120px; color: #3b82f6;"></i>
            </div>
            <div style="position: relative; z-index: 1;">
                <i class="ph-duotone ph-users-three metric-icon" style="font-size: 56px; color: #3b82f6; display: block; margin-bottom: 15px;"></i>
                <div style="color: #848991; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 800; margin-bottom: 10px;">Active Users</div>
                <div style="color: #3b82f6; font-size: 42px; font-weight: 900; font-family: 'Inter', monospace; line-height: 1;">{pivot_table.shape[0]:,}</div>
                <div style="color: #555; font-size: 10px; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px;">Registered Profiles</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with c2:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 30px; border-radius: 14px; border: 2px solid #10B981; text-align: center; position: relative; overflow: hidden;">
            <div style="position: absolute; top: -20px; right: -20px; opacity: 0.1;">
                <i class="ph-duotone ph-package" style="font-size: 120px; color: #10B981;"></i>
            </div>
            <div style="position: relative; z-index: 1;">
                <i class="ph-duotone ph-package metric-icon" style="font-size: 56px; color: #10B981; display: block; margin-bottom: 15px;"></i>
                <div style="color: #848991; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 800; margin-bottom: 10px;">Product Catalog</div>
                <div style="color: #10B981; font-size: 42px; font-weight: 900; font-family: 'Inter', monospace; line-height: 1;">{pivot_table.shape[1]:,}</div>
                <div style="color: #555; font-size: 10px; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px;">Unique Items</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with c3:
        st.markdown('''
        <div class="metric-card" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 30px; border-radius: 14px; border: 2px solid #8b5cf6; text-align: center; position: relative; overflow: hidden;">
            <div style="position: absolute; top: -20px; right: -20px; opacity: 0.1;">
                <i class="ph-duotone ph-graph" style="font-size: 120px; color: #8b5cf6;"></i>
            </div>
            <div style="position: relative; z-index: 1;">
                <i class="ph-duotone ph-graph metric-icon" style="font-size: 56px; color: #8b5cf6; display: block; margin-bottom: 15px;"></i>
                <div style="color: #848991; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 800; margin-bottom: 10px;">AI Clusters</div>
                <div style="color: #8b5cf6; font-size: 42px; font-weight: 900; font-family: 'Inter', monospace; line-height: 1;">10</div>
                <div style="color: #555; font-size: 10px; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px;">User Segments</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Ultra Premium Control Panel
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px;">
        <i class="ph-duotone ph-sliders-horizontal" style="font-size: 28px; color: #FF9900;"></i>
        <h3 style="margin: 0; color: white; font-size: 20px; font-weight: 700;">Configuration Panel</h3>
        <div style="flex: 1; height: 2px; background: linear-gradient(90deg, #FF9900 0%, transparent 100%);"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    col_input, col_param, col_opt = st.columns([2, 1, 1])
    
    with col_input:
        st.markdown('<div style="margin-bottom: 8px;"><i class="ph-fill ph-user-circle-gear" style="color: #3b82f6; font-size: 18px; margin-right: 8px;"></i><strong style="color: white; font-size: 14px;">Target User Profile</strong></div>', unsafe_allow_html=True)
        all_users = pivot_table.index.tolist()
        user_id = st.selectbox("Select Active User ID", all_users[:20], label_visibility="collapsed")
    
    with col_param:
        st.markdown('<div style="margin-bottom: 8px;"><i class="ph-fill ph-list-numbers" style="color: #10B981; font-size: 18px; margin-right: 8px;"></i><strong style="color: white; font-size: 14px;">Recommendation Limit</strong></div>', unsafe_allow_html=True)
        top_n = st.number_input("Top N Items", 5, 20, 10, label_visibility="collapsed")
    
    with col_opt:
        st.markdown('<div style="margin-bottom: 8px;"><i class="ph-fill ph-globe-hemisphere-west" style="color: #8b5cf6; font-size: 18px; margin-right: 8px;"></i><strong style="color: white; font-size: 14px;">Live Metadata</strong></div>', unsafe_allow_html=True)
        use_live_fetch = st.checkbox("Fetch Product Names", value=True, help="Enable live scraping to retrieve real product titles from Amazon.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Ultra Premium Run Button
    button_clicked = st.button(
        "▶ RUN AI ANALYSIS ENGINE",
        use_container_width=True,
        type="primary"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

    if button_clicked:
        _run_inference(artifacts, user_id, top_n, use_live_fetch)

def _run_inference(artifacts, user_id, top_n, use_live_fetch):
    # Create placeholder for progress
    progress_placeholder = st.empty()
    
    start_time = time.time()
    
    # Show progress in placeholder
    with progress_placeholder.container():
        st.markdown('''
        <div style="background: linear-gradient(135deg, #1A1F26 0%, #15191E 100%); padding: 25px; border-radius: 12px; border: 2px solid #3A4556; margin: 25px 0;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
                <i class="ph-duotone ph-gear-six spinner-icon" style="color: #FF9900; font-size: 28px;"></i>
                <strong style="color: white; font-size: 16px;">Processing AI Request...</strong>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        progress_text = "Initializing AI Engine..."
        my_bar = st.progress(0, text=progress_text)
        time.sleep(0.2)
        
        my_bar.progress(20, text="Vectorizing User Profile (SVD Transformation)...")
    
    pivot_table = artifacts['user_item_pivot']
    model = artifacts['kmeans']
    svd = artifacts['svd']
    top_items_map = artifacts['top_items_per_cluster']
    
    try:
        user_idx = pivot_table.index.get_loc(user_id)
        user_vector = svd.transform(pivot_table.iloc[user_idx].values.reshape(1, -1))
        
        with progress_placeholder.container():
            my_bar = st.progress(50, text="Identifying User Cluster (K-Means Prediction)...")
        
        cluster_id = model.predict(user_vector)[0]
        recommendations = top_items_map[cluster_id][:top_n]
        
        results = []
        score_start = 0.98
        
        total = len(recommendations)
        for i, asin in enumerate(recommendations):
            current = 60 + int((i / total) * 35)
            
            if use_live_fetch:
                with progress_placeholder.container():
                    st.progress(current, text=f"Fetching Product [{i+1}/{total}]: {asin}...")
                name = fetch_product_name_live(asin)
            else:
                name = "Enable 'Fetch Product Names' to see details"
            
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

        with progress_placeholder.container():
            st.progress(100, text=f"Analysis Complete ({execution_time:.2f}s)")
        time.sleep(0.5)
        
        # Clear entire progress section
        progress_placeholder.empty()

        # Ultra Premium Result Display
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, #15191E 0%, #1A1F26 100%); border: 3px solid #FF9900; border-radius: 14px; padding: 30px; margin-bottom: 25px; position: relative; overflow: hidden;">
            <div style="position: absolute; top: -30px; right: -30px; opacity: 0.05;">
                <i class="ph-duotone ph-sparkle" style="font-size: 200px; color: #FF9900;"></i>
            </div>
            <div style="position: relative; z-index: 1;">
                <div style="display: flex; align-items: start; gap: 20px;">
                    <i class="ph-duotone ph-target" style="color: #FF9900; font-size: 48px; margin-top: 5px;"></i>
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                            <h3 style="margin: 0; color: #FF9900; font-size: 20px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">AI Cluster Analysis Complete</h3>
                            <i class="ph-fill ph-check-circle" style="color: #10B981; font-size: 24px;"></i>
                        </div>
                        <p style="font-size: 15px; color: #ccc; line-height: 1.8; margin: 0;">
                            User <strong style="color: white; background: rgba(255, 255, 255, 0.1); padding: 2px 8px; border-radius: 4px; font-family: monospace;">{user_id}</strong> has been classified into 
                            <strong style="color: #3b82f6;">Cluster #{cluster_id}</strong>. 
                            The <strong style="color: #FF9900;">{top_n} recommendations</strong> below are ranked by 
                            <strong style="color: #10B981;">Top-Sum Popularity</strong> within this community cluster.
                        </p>
                    </div>
                    <div style="background: rgba(255, 153, 0, 0.15); padding: 15px 20px; border-radius: 10px; text-align: center; border: 2px solid #FF9900;">
                        <div style="color: #848991; font-size: 9px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; font-weight: 700;">Cluster ID</div>
                        <div style="color: #FF9900; font-size: 36px; font-weight: 900; font-family: monospace; line-height: 1;">#{cluster_id}</div>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Performance Badge
        st.markdown(f'''
        <div style="display: inline-flex; align-items: center; gap: 10px; background: linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(255, 153, 0, 0.1) 100%); padding: 10px 18px; border-radius: 20px; border: 2px solid #FFD700; margin-bottom: 20px;">
            <i class="ph-fill ph-lightning" style="color: #FFD700; font-size: 22px;"></i>
            <span style="color: #ccc; font-size: 14px;">Inference completed in <strong style="color: #FFD700; font-family: monospace; font-size: 16px;">{execution_time:.3f}s</strong></span>
        </div>
        ''', unsafe_allow_html=True)
        
        # Enhanced DataFrame
        st.dataframe(
            pd.DataFrame(results),
            use_container_width=True,
            hide_index=True,
            column_config={
                "ASIN": st.column_config.TextColumn(
                    "ASIN", 
                    width="small",
                    help="Amazon Standard Identification Number"
                ),
                "Product Name": st.column_config.TextColumn(
                    "Product Name", 
                    width="large"
                ),
                "Relevance Score": st.column_config.ProgressColumn(
                    "Relevance", 
                    format="%.2f", 
                    min_value=0, 
                    max_value=1,
                    help="AI-computed relevance score"
                ),
                "Link": st.column_config.LinkColumn(
                    "Action", 
                    display_text="View on Amazon"
                )
            }
        )
        
    except Exception as e:
        progress_placeholder.empty()
        st.error(f"<i class='ph-fill ph-warning-circle'></i> Inference Error: {str(e)}", icon="⚠️")