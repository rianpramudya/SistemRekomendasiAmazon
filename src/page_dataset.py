import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import src.ui_components as ui

def render_sparsity_chart(n_ratings, matrix_size):
    """Membuat Donut Chart untuk memvisualisasikan Kekosongan Data"""
    n_empty = matrix_size - n_ratings
    density_pct = (n_ratings / matrix_size) * 100
    
    colors = ['#1A1F26', '#FF9900'] 
    
    fig = go.Figure(data=[go.Pie(
        labels=['Empty Space', 'User Interactions'],
        values=[n_empty, n_ratings],
        hole=.7,
        marker=dict(colors=colors, line=dict(color='#0F1111', width=2)),
        textinfo='none',
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
    # Load Phosphor Icons CSS
    st.markdown("""
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/duotone/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/bold/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/fill/style.css">
    
    <style>
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    .pipeline-card {
        animation: fadeInUp 0.6s ease-out;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .pipeline-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
    }
    
    .pipeline-icon {
        animation: pulse 2s ease-in-out infinite;
    }
    
    .arrow-flow {
        animation: flowRight 2s ease-in-out infinite;
    }
    
    @keyframes flowRight {
        0%, 100% {
            opacity: 0.3;
            transform: translateX(-5px);
        }
        50% {
            opacity: 1;
            transform: translateX(5px);
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    pivot_table = artifacts['user_item_pivot']
    
    # Header
    st.markdown("<h1>Dataset Overview</h1>", unsafe_allow_html=True)
    
    # Hitung Statistik
    n_users = pivot_table.shape[0]
    n_items = pivot_table.shape[1]
    n_ratings = pivot_table.astype(bool).sum().sum()
    matrix_size = n_users * n_items
    sparsity = 100 * (1 - (n_ratings / matrix_size))
    
    # Key Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        ui.render_metric_card("TOTAL USERS", f"{n_users:,}", "ph-users")
    with c2: 
        ui.render_metric_card("TOTAL ITEMS", f"{n_items:,}", "ph-package")
    with c3: 
        ui.render_metric_card("INTERACTIONS", f"{n_ratings:,}", "ph-star")
    with c4: 
        ui.render_metric_card("SPARSITY", f"{sparsity:.2f}%", "ph-circles-three")
    
    st.markdown("---")
    
    # Analytical Section
    col_viz, col_data = st.columns([1, 2], gap="large")
    
    with col_viz:
        st.markdown("**Matrix Density**")
        fig = render_sparsity_chart(n_ratings, matrix_size)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.info("Grafik ini menunjukkan bahwa >99% data matriks adalah kosong. SVD mutlak diperlukan.")

    with col_data:
        st.markdown("**Data Snapshot (Pivot)**")
        st.dataframe(pivot_table.iloc[:10, :10], use_container_width=True, height=300)

    st.markdown("---")
    st.markdown("### Preprocessing Pipeline")
    
    # PREMIUM PIPELINE dengan Phosphor Icons
    cols = st.columns([2, 0.5, 2, 0.5, 2, 0.5, 2])
    
    # Step 1: Raw Data (Phosphor Icon: file-csv)
    with cols[0]:
        st.markdown('''
        <div class="pipeline-card" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #FF9900; box-shadow: 0 4px 12px rgba(255, 153, 0, 0.2);">
            <i class="ph-duotone ph-file-csv pipeline-icon" style="font-size: 48px; color: #FF9900; display: block; margin-bottom: 15px;"></i>
            <div style="color: #FF9900; font-weight: 700; font-size: 16px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Raw Data</div>
            <div style="color: #888; font-size: 12px;">Load CSV File</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Arrow 1
    with cols[1]:
        st.markdown('<div class="arrow-flow" style="text-align: center; padding-top: 60px;"><i class="ph-bold ph-arrow-right" style="font-size: 28px; color: #FF9900;"></i></div>', unsafe_allow_html=True)
    
    # Step 2: Filtering (Phosphor Icon: funnel)
    with cols[2]:
        st.markdown('''
        <div class="pipeline-card" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #10B981; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);">
            <i class="ph-duotone ph-funnel pipeline-icon" style="font-size: 48px; color: #10B981; display: block; margin-bottom: 15px;"></i>
            <div style="color: #10B981; font-weight: 700; font-size: 16px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Filtering</div>
            <div style="color: #888; font-size: 12px;">Active Users (>50)</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Arrow 2
    with cols[3]:
        st.markdown('<div class="arrow-flow" style="text-align: center; padding-top: 60px;"><i class="ph-bold ph-arrow-right" style="font-size: 28px; color: #10B981;"></i></div>', unsafe_allow_html=True)
    
    # Step 3: Pivot (Phosphor Icon: table)
    with cols[4]:
        st.markdown('''
        <div class="pipeline-card" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #3b82f6; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);">
            <i class="ph-duotone ph-table pipeline-icon" style="font-size: 48px; color: #3b82f6; display: block; margin-bottom: 15px;"></i>
            <div style="color: #3b82f6; font-weight: 700; font-size: 16px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Pivot</div>
            <div style="color: #888; font-size: 12px;">User-Item Matrix</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Arrow 3
    with cols[5]:
        st.markdown('<div class="arrow-flow" style="text-align: center; padding-top: 60px;"><i class="ph-bold ph-arrow-right" style="font-size: 28px; color: #3b82f6;"></i></div>', unsafe_allow_html=True)
    
    # Step 4: SVD (Phosphor Icon: chart-line)
    with cols[6]:
        st.markdown('''
        <div class="pipeline-card" style="background: linear-gradient(135deg, #2a3038 0%, #1f2630 100%); padding: 25px; border-radius: 12px; text-align: center; border: 2px solid #8b5cf6; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);">
            <i class="ph-duotone ph-chart-line pipeline-icon" style="font-size: 48px; color: #8b5cf6; display: block; margin-bottom: 15px;"></i>
            <div style="color: #8b5cf6; font-weight: 700; font-size: 16px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">SVD</div>
            <div style="color: #888; font-size: 12px;">50 Latent Features</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)