import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import src.ui_components as ui

def render_sparsity_chart(n_ratings, matrix_size):
    """Membuat Donut Chart untuk memvisualisasikan Kekosongan Data"""
    n_empty = matrix_size - n_ratings
    sparsity_pct = (n_empty / matrix_size) * 100
    density_pct = (n_ratings / matrix_size) * 100
    
    # Warna: Gelap untuk Empty, Orange Cerah untuk Interaction
    colors = ['#1A1F26', '#FF9900'] 
    
    fig = go.Figure(data=[go.Pie(
        labels=['Empty Space', 'User Interactions'],
        values=[n_empty, n_ratings],
        hole=.7, # Donut style
        marker=dict(colors=colors, line=dict(color='#0F1111', width=2)),
        textinfo='none', # Bersih tanpa teks di dalam slice
        hoverinfo='label+value+percent'
    )])

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        height=200,
        annotations=[dict(text=f'{density_pct:.2f}%<br>Density', x=0.5, y=0.5, font_size=14, showarrow=False, font_color='white')]
    )
    return fig

def render(artifacts):
    pivot_table = artifacts['user_item_pivot']
    
    # --- 1. HERO HEADER ---
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="margin-bottom: 8px;">Dataset Overview</h1>
        <div style="display: flex; align-items: center; gap: 8px; color: #848991; font-size: 14px;">
            <i class="ph-fill ph-database"></i> Amazon Electronics
            <span style="color: #2A3038;">|</span>
            <span style="color: #FF9900;">Filtered & Processed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hitung Statistik
    n_users = pivot_table.shape[0]
    n_items = pivot_table.shape[1]
    n_ratings = pivot_table.astype(bool).sum().sum()
    matrix_size = n_users * n_items
    sparsity = 100 * (1 - (n_ratings / matrix_size))
    
    # --- 2. KEY METRICS ROW ---
    c1, c2, c3, c4 = st.columns(4)
    with c1: ui.render_metric_card("TOTAL USERS", f"{n_users:,}", "ph-users")
    with c2: ui.render_metric_card("TOTAL ITEMS", f"{n_items:,}", "ph-package")
    with c3: ui.render_metric_card("INTERACTIONS", f"{n_ratings:,}", "ph-star")
    with c4: ui.render_metric_card("SPARSITY", f"{sparsity:.2f}%", "ph-circles-three")
    
    st.markdown("---")
    
    # --- 3. ANALYTICAL SECTION (Split Layout) ---
    col_viz, col_data = st.columns([1, 2], gap="large")
    
    with col_viz:
        st.markdown("##### <i class='ph-bold ph-chart-pie-slice'></i> Matrix Density", unsafe_allow_html=True)
        # Render Chart
        fig = render_sparsity_chart(n_ratings, matrix_size)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Insight Kecil
        st.markdown("""
        <div style="background: #15191E; padding: 15px; border-radius: 8px; border: 1px solid #2A3038; font-size: 12px; color: #888; line-height: 1.5;">
            <strong style="color: #FF9900;">Why SVD?</strong><br>
            Grafik ini menunjukkan bahwa 99.8% data matriks adalah "kosong". 
            Teknik reduksi dimensi (SVD) mutlak diperlukan untuk memadatkan informasi ini agar Clustering bisa bekerja.
        </div>
        """, unsafe_allow_html=True)

    with col_data:
        st.markdown("##### <i class='ph-bold ph-table'></i> Data Snapshot (Pivot)", unsafe_allow_html=True)
        st.markdown("<p style='color:#848991; font-size:13px; margin-bottom: 10px;'>Sample slice of the User-Item interaction matrix (First 10x10).</p>", unsafe_allow_html=True)
        
        # Tampilkan Dataframe
        st.dataframe(
            pivot_table.iloc[:10, :10],
            use_container_width=True,
            height=300
        )

    st.markdown("---")

    # --- 4. PIPELINE VISUALIZATION ---
    st.markdown("##### <i class='ph-bold ph-git-merge'></i> Preprocessing Pipeline", unsafe_allow_html=True)
    
    # Custom HTML Flowchart
    st.markdown("""
    <div style="display: flex; justify-content: space-between; gap: 10px; margin-top: 15px;">
        <div style="flex: 1; background: #1A1F26; padding: 15px; border-radius: 8px; border: 1px solid #3A4556; text-align: center;">
            <i class="ph-duotone ph-file-csv" style="font-size: 24px; color: #FF9900; margin-bottom: 8px;"></i>
            <div style="color: white; font-weight: 600; font-size: 13px;">Raw Data</div>
            <div style="color: #888; font-size: 11px;">7.8M Ratings</div>
        </div>
        
        <div style="display: flex; align-items: center; color: #555;"><i class="ph-bold ph-arrow-right"></i></div>
        
        <div style="flex: 1; background: #1A1F26; padding: 15px; border-radius: 8px; border: 1px solid #3A4556; text-align: center;">
            <i class="ph-duotone ph-funnel" style="font-size: 24px; color: #10B981; margin-bottom: 8px;"></i>
            <div style="color: white; font-weight: 600; font-size: 13px;">Filtering</div>
            <div style="color: #888; font-size: 11px;">Active Users (>50)</div>
        </div>

        <div style="display: flex; align-items: center; color: #555;"><i class="ph-bold ph-arrow-right"></i></div>

        <div style="flex: 1; background: #1A1F26; padding: 15px; border-radius: 8px; border: 1px solid #3A4556; text-align: center;">
            <i class="ph-duotone ph-table" style="font-size: 24px; color: #3b82f6; margin-bottom: 8px;"></i>
            <div style="color: white; font-weight: 600; font-size: 13px;">Pivot</div>
            <div style="color: #888; font-size: 11px;">User-Item Matrix</div>
        </div>

        <div style="display: flex; align-items: center; color: #555;"><i class="ph-bold ph-arrow-right"></i></div>

        <div style="flex: 1; background: #1A1F26; padding: 15px; border-radius: 8px; border: 1px solid #3A4556; text-align: center;">
            <i class="ph-duotone ph-projector-screen-chart" style="font-size: 24px; color: #8b5cf6; margin-bottom: 8px;"></i>
            <div style="color: white; font-weight: 600; font-size: 13px;">SVD Reduction</div>
            <div style="color: #888; font-size: 11px;">50 Latent Features</div>
        </div>
    </div>
    """, unsafe_allow_html=True)