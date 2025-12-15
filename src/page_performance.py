import streamlit as st
import json
import plotly.graph_objects as go
import src.ui_components as ui

def load_metrics():
    try:
        with open('models/metrics.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def render_performance_chart(metrics):
    """Membuat Bar Chart Horizontal Modern menggunakan Plotly"""
    
    # Data Setup
    labels = ['Precision@10', 'Recall@10', 'F1-Score']
    values = [metrics['precision'], metrics['recall'], metrics['f1_score']]
    colors = ['#3b82f6', '#10b981', '#8b5cf6'] # Biru, Hijau, Ungu
    
    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        text=[f"{v:.4f}" for v in values], # Tampilkan angka di bar
        textposition='auto',
        marker_color=colors,
        opacity=0.9
    ))

    # Styling Chart agar menyatu dengan Dark Mode
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family="Inter"),
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#333', 
            zeroline=False,
            showticklabels=False # Sembunyikan angka axis bawah agar bersih
        ),
        yaxis=dict(
            showgrid=False,
            categoryorder='total ascending'
        ),
        bargap=0.4
    )
    
    return fig

def render():
    # --- 1. HERO SECTION ---
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="margin-bottom: 8px;">Model Performance</h1>
        <div style="display: flex; align-items: center; gap: 8px; color: #848991; font-size: 14px;">
            <i class="ph-fill ph-chart-line-up"></i> Evaluation Report
            <span style="color: #2A3038;">|</span>
            <span style="color: #FF9900;">5-Fold Cross Validation</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    metrics = load_metrics()
    if not metrics:
        st.warning("⚠️ Metrics file not found. Please run `src/evaluate.py` first.")
        return

    # --- 2. MAIN CONTENT (Split Layout) ---
    # Kolom Kiri: Kartu Angka | Kolom Kanan: Visualisasi Grafik
    col_metrics, col_viz = st.columns([1, 1.5], gap="large")

    with col_metrics:
        st.markdown("##### <i class='ph-bold ph-faders'></i> Key Metrics", unsafe_allow_html=True)
        # Precision
        ui.render_metric_card("PRECISION@10", f"{metrics['precision']:.4f}", "ph-crosshair")
        st.markdown("<div style='margin-bottom: 12px'></div>", unsafe_allow_html=True)
        
        # Recall
        ui.render_metric_card("RECALL@10", f"{metrics['recall']:.4f}", "ph-magnifying-glass-plus")
        st.markdown("<div style='margin-bottom: 12px'></div>", unsafe_allow_html=True)
        
        # F1 Score
        ui.render_metric_card("F1-SCORE", f"{metrics['f1_score']:.4f}", "ph-function")

    with col_viz:
        st.markdown("##### <i class='ph-bold ph-chart-bar'></i> Performance Visualization", unsafe_allow_html=True)
        
        # Render Plotly Chart
        chart = render_performance_chart(metrics)
        st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
        
        # Insight Box Modern
        st.markdown("""
        <div style="background: #15191E; border: 1px solid #2A3038; border-radius: 12px; padding: 20px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <i class="ph-fill ph-info" style="color: #FF9900; font-size: 20px;"></i>
                <span style="font-weight: 600; font-size: 14px;">Understanding the Numbers</span>
            </div>
            <p style="font-size: 13px; color: #848991; line-height: 1.6; margin: 0;">
                Dalam dataset <strong>High-Sparsity</strong> seperti Amazon Electronics (dimana user rata-rata hanya membeli < 0.01% dari total katalog), angka Precision ~1-2% dianggap <strong>wajar dan valid</strong>.
                <br><br>
                Grafik di atas menunjukkan keseimbangan antara kemampuan model memberikan rekomendasi akurat (Precision) dan kelengkapan rekomendasi (Recall).
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- 3. TECHNICAL FOOTER ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🛠️ Technical Methodology Details"):
        st.markdown("""
        ### Evaluation Strategy
        Proses evaluasi dilakukan menggunakan teknik **5-Fold Cross Validation** untuk menjamin konsistensi hasil.
        
        1.  **Data Splitting:** Dataset dibagi menjadi 5 bagian (folds) secara acak.
        2.  **Iterasi:** Model dilatih pada 4 bagian dan diuji pada 1 bagian yang tersisa. Proses ini diulang 5 kali.
        3.  **Aggregasi:** Angka yang ditampilkan di atas adalah rata-rata (mean) dari ke-5 iterasi tersebut.
        
        ### Metric Definitions
        * **Precision@10:** Dari 10 barang yang direkomendasikan, berapa persen yang relevan/dibeli user?
        * **Recall@10:** Dari seluruh barang yang disukai user, berapa persen yang berhasil ditemukan oleh sistem?
        """)