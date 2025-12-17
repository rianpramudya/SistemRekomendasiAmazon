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
    """Membuat Bar Chart Modern dengan Gradient Effects"""
    labels = ['Precision@10', 'Recall@10', 'F1-Score']
    values = [metrics['precision'], metrics['recall'], metrics['f1_score']]
    colors = ['#3b82f6', '#10b981', '#8b5cf6']
    
    fig = go.Figure()
    
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        fig.add_trace(go.Bar(
            x=[value],
            y=[label],
            orientation='h',
            text=[f"<b>{value:.4f}</b>"],
            textposition='inside',
            textfont=dict(size=16, color='white', family='Inter'),
            marker=dict(
                color=color,
                opacity=0.9,
                line=dict(color=color, width=0)
            ),
            hovertemplate=f'<b>{label}</b><br>Score: <b>{value:.4f}</b><extra></extra>',
            name=label,
            showlegend=False
        ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family="Inter", size=14),
        height=300,
        margin=dict(l=20, r=80, t=30, b=30),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#2A3038',
            gridwidth=1,
            zeroline=False,
            range=[0, max(values) * 1.2],
            showticklabels=True,
            tickfont=dict(size=12, color='#848991')
        ),
        yaxis=dict(
            showgrid=False,
            categoryorder='total ascending',
            tickfont=dict(size=14, color='white', family='Inter')
        ),
        bargap=0.3,
        hoverlabel=dict(
            bgcolor="#1A1F26",
            font_size=14,
            font_family="Inter",
            bordercolor='#FF9900'
        )
    )
    
    return fig

def render():
    # Load Phosphor Icons & Animations
    st.markdown("""
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/duotone/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/bold/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/fill/style.css">
    
    <style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 10px rgba(255, 153, 0, 0.3); }
        50% { box-shadow: 0 0 25px rgba(255, 153, 0, 0.6); }
    }
    
    .metric-card-animated {
        animation: fadeInUp 0.6s ease-out;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card-animated:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
    }
    
    .icon-pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    .glow-box {
        animation: glow 3s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 style="background: linear-gradient(90deg, #FF9900 0%, #FFB84D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 36px; margin-bottom: 8px;">Model Performance</h1>', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 30px;"><i class="ph-fill ph-chart-line-up" style="color: #FF9900; font-size: 20px;"></i><span style="color: white; font-weight: 600; font-size: 15px;">Evaluation Report</span><span style="color: #3A4556; font-size: 20px;">•</span><span style="background: rgba(255, 153, 0, 0.15); padding: 5px 12px; border-radius: 6px; color: #FF9900; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">5-Fold Cross Validation</span></div>', unsafe_allow_html=True)
    
    metrics = load_metrics()
    if not metrics:
        st.warning("⚠️ Metrics file not found. Please run `src/evaluate.py` first.")
        return

    # Main Content Split
    col_metrics, col_viz = st.columns([1.2, 1.8], gap="large")

    with col_metrics:
        st.markdown("##### <i class='ph-bold ph-faders-horizontal'></i> Performance Metrics", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Precision Card
        st.markdown(f'''
        <div class="metric-card-animated" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 30px 25px; border-radius: 12px; margin-bottom: 18px; border: 2px solid #3b82f6; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 20px; right: 20px; opacity: 0.15;">
                <i class="ph-duotone ph-target icon-pulse" style="font-size: 80px; color: #3b82f6;"></i>
            </div>
            <div style="position: relative; z-index: 1;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                    <i class="ph-fill ph-crosshair" style="color: #3b82f6; font-size: 20px;"></i>
                    <span style="color: #848991; font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">Precision@10</span>
                </div>
                <div style="color: #3b82f6; font-size: 42px; font-weight: 900; line-height: 1; font-family: 'Inter', monospace;">{metrics["precision"]:.4f}</div>
                <div style="color: #848991; font-size: 11px; margin-top: 8px;">Akurasi Rekomendasi</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Recall Card
        st.markdown(f'''
        <div class="metric-card-animated" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 30px 25px; border-radius: 12px; margin-bottom: 18px; border: 2px solid #10b981; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 20px; right: 20px; opacity: 0.15;">
                <i class="ph-duotone ph-binoculars icon-pulse" style="font-size: 80px; color: #10b981;"></i>
            </div>
            <div style="position: relative; z-index: 1;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                    <i class="ph-fill ph-magnifying-glass-plus" style="color: #10b981; font-size: 20px;"></i>
                    <span style="color: #848991; font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">Recall@10</span>
                </div>
                <div style="color: #10b981; font-size: 42px; font-weight: 900; line-height: 1; font-family: 'Inter', monospace;">{metrics["recall"]:.4f}</div>
                <div style="color: #848991; font-size: 11px; margin-top: 8px;">Cakupan Rekomendasi</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # F1 Score Card
        st.markdown(f'''
        <div class="metric-card-animated" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 30px 25px; border-radius: 12px; border: 2px solid #8b5cf6; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 20px; right: 20px; opacity: 0.15;">
                <i class="ph-duotone ph-equals icon-pulse" style="font-size: 80px; color: #8b5cf6;"></i>
            </div>
            <div style="position: relative; z-index: 1;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                    <i class="ph-fill ph-function" style="color: #8b5cf6; font-size: 20px;"></i>
                    <span style="color: #848991; font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">F1-Score</span>
                </div>
                <div style="color: #8b5cf6; font-size: 42px; font-weight: 900; line-height: 1; font-family: 'Inter', monospace;">{metrics["f1_score"]:.4f}</div>
                <div style="color: #848991; font-size: 11px; margin-top: 8px;">Harmonic Mean</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col_viz:
        st.markdown("##### <i class='ph-bold ph-chart-bar-horizontal'></i> Comparative Visualization", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Chart
        chart = render_performance_chart(metrics)
        st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Insight Box
        st.markdown('''
        <div class="glow-box" style="background: linear-gradient(135deg, #15191E 0%, #1A1F26 100%); border: 2px solid #FF9900; border-radius: 12px; padding: 25px;">
            <div style="display: flex; align-items: start; gap: 15px;">
                <i class="ph-duotone ph-lightbulb" style="color: #FF9900; font-size: 36px; margin-top: 2px;"></i>
                <div>
                    <div style="font-weight: 700; font-size: 16px; color: #FF9900; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">
                        Understanding High-Sparsity Performance
                    </div>
                    <p style="font-size: 14px; color: #ccc; line-height: 1.8; margin: 0;">
                        Dalam dataset <strong style="color: white;">High-Sparsity</strong> seperti Amazon Electronics (dimana user rata-rata hanya membeli <strong style="color: #FF9900;">&lt; 0.01%</strong> dari total katalog), angka Precision ~1-2% dianggap <strong style="color: #10b981;">wajar dan valid</strong>.
                        <br><br>
                        <i class="ph-fill ph-chart-line" style="color: #3b82f6;"></i> Grafik menunjukkan keseimbangan antara <strong style="color: #3b82f6;">akurasi</strong> (Precision) dan <strong style="color: #10b981;">cakupan</strong> (Recall) sistem rekomendasi.
                    </p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # Technical Methodology
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    with st.expander("Technical Methodology Details", expanded=False):
        st.markdown("### <i class='ph-fill ph-flask' style='color: #FF9900;'></i> Evaluation Strategy", unsafe_allow_html=True)
        st.write("Proses evaluasi dilakukan menggunakan teknik **5-Fold Cross Validation** untuk menjamin konsistensi hasil.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        with cols[0]:
            st.markdown('<div style="background: linear-gradient(135deg, #1A1F26 0%, #15191E 100%); padding: 20px; border-radius: 10px; border-left: 4px solid #3b82f6; text-align: center;"><i class="ph-duotone ph-split-horizontal" style="font-size: 36px; color: #3b82f6; display: block; margin-bottom: 10px;"></i><strong style="color: #3b82f6; font-size: 15px;">Data Splitting</strong><p style="color: #888; font-size: 12px; margin-top: 8px; line-height: 1.5;">Dataset dibagi menjadi 5 bagian (folds) secara acak</p></div>', unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown('<div style="background: linear-gradient(135deg, #1A1F26 0%, #15191E 100%); padding: 20px; border-radius: 10px; border-left: 4px solid #10b981; text-align: center;"><i class="ph-duotone ph-arrows-clockwise" style="font-size: 36px; color: #10b981; display: block; margin-bottom: 10px;"></i><strong style="color: #10b981; font-size: 15px;">Iterasi Training</strong><p style="color: #888; font-size: 12px; margin-top: 8px; line-height: 1.5;">Model dilatih 4 folds, diuji 1 fold. Diulang 5 kali</p></div>', unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown('<div style="background: linear-gradient(135deg, #1A1F26 0%, #15191E 100%); padding: 20px; border-radius: 10px; border-left: 4px solid #8b5cf6; text-align: center;"><i class="ph-duotone ph-calculator" style="font-size: 36px; color: #8b5cf6; display: block; margin-bottom: 10px;"></i><strong style="color: #8b5cf6; font-size: 15px;">Aggregasi</strong><p style="color: #888; font-size: 12px; margin-top: 8px; line-height: 1.5;">Angka final adalah rata-rata dari 5 iterasi</p></div>', unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### <i class='ph-fill ph-info' style='color: #FF9900;'></i> Metric Definitions", unsafe_allow_html=True)
        
        st.markdown("""
        - **<span style="color: #3b82f6;">Precision@10</span>:** Dari 10 barang yang direkomendasikan, berapa persen yang relevan/dibeli user?
        - **<span style="color: #10b981;">Recall@10</span>:** Dari seluruh barang yang disukai user, berapa persen yang berhasil ditemukan sistem?
        - **<span style="color: #8b5cf6;">F1-Score</span>:** Harmonic mean dari Precision dan Recall (mengukur keseimbangan keduanya).
        """, unsafe_allow_html=True)