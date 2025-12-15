import streamlit as st

def inject_custom_css():
    st.markdown("""
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
    /* --- 1. GLOBAL THEME VARIABLES --- */
    :root {
        --primary: #FF9900;
        --primary-dim: rgba(255, 153, 0, 0.15);
        --bg-dark: #0F1111;
        --sidebar-bg: #111418;
        --card-bg: #1A1F26;
        --text-white: #FFFFFF;
        --text-muted: #848991;
        --border-color: #2A3038;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-white);
        background-color: var(--bg-dark);
    }
    
    .stApp { background-color: var(--bg-dark); }

    /* --- 2. SIDEBAR NAVIGATION --- */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
    }

    /* Hide Radio Circles */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none;
    }

    /* Base Menu Item */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 6px;
        border: 1px solid transparent;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        color: var(--text-muted);
        background: transparent;
        display: flex;
        align-items: center;
    }

    /* Hover State */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-white);
        transform: translateX(4px);
    }

    /* Active/Selected State */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] {
        background: var(--primary-dim);
        border: 1px solid rgba(255, 153, 0, 0.3);
        color: var(--primary) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] p {
        color: var(--primary) !important;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* --- 3. COMPONENTS --- */
    
    /* Metric Card */
    .metric-card {
        background: linear-gradient(180deg, #1E232B 0%, #15181E 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        transition: transform 0.3s ease, border-color 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        border-color: var(--primary);
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .metric-value { font-size: 32px; font-weight: 800; color: white; margin-top: 10px; line-height: 1; }
    .metric-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1.2px; display: flex; align-items: center; gap: 8px; font-weight: 600; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF9900 0%, #FFB84D 100%);
        color: #000000 !important;
        font-weight: 700 !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 0.5px;
    }
    .stButton > button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(255, 153, 0, 0.4); 
    }
    
    /* Info Box (Dynamic Insight) */
    .info-box {
        background: rgba(255, 153, 0, 0.05);
        border-left: 4px solid var(--primary);
        padding: 20px;
        border-radius: 0 8px 8px 0;
        display: flex;
        gap: 16px;
        align-items: start;
        margin-top: 24px;
        backdrop-filter: blur(10px);
    }
    
    /* System Status Footer */
    .status-container {
        background: rgba(255,255,255,0.03);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-top: auto;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render Sidebar Modern dengan Status & Navigasi"""
    with st.sidebar:
        # Header Area
        st.markdown("""
        <div style="padding: 10px 0 30px 0; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span style="font-weight: 800; font-size: 20px; color: white; letter-spacing: -0.5px;">
                    <i class="ph-fill ph-circles-three-plus" style="color: #FF9900; margin-right: 8px;"></i>
                    RecSys
                </span>
                <span style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; font-size: 10px; color: #888; font-weight: 700; vertical-align: middle; margin-left: 6px;">ADMIN</span>
            </div>
            <div style="width: 8px; height: 8px; background: #10B981; border-radius: 50%; box-shadow: 0 0 8px #10B981;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p style="font-size: 11px; color: #555; font-weight: 700; margin-bottom: 12px; letter-spacing: 1px;">MAIN MODULES</p>', unsafe_allow_html=True)
        
        # Navigation Menu
        page = st.radio(
            "Navigation", 
            ["   Dashboard Engine", "   Model Performance", "   Dataset Information"], 
            label_visibility="collapsed"
        )
        
        # Spacer agar status turun ke bawah
        st.markdown("<div style='height: 35vh'></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # System Health Footer
        st.markdown("""
        <div class="status-container">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <i class="ph-fill ph-cpu" style="color: #848991; font-size: 18px; margin-right: 10px;"></i>
                <span style="font-size: 12px; color: white; font-weight: 600;">System Health</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #848991; margin-bottom: 6px;">
                <span>Algorithm</span>
                <span style="color: #FF9900; font-weight: 600;">K-Means v2</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #848991;">
                <span>Latency</span>
                <span style="color: #10B981; font-family: monospace;">~24ms</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return page.strip()

def render_metric_card(label, value, icon):
    """Render Kartu Metrik Statistik"""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">
            <i class="ph-fill {icon}" style="color: #FF9900;"></i> {label}
        </div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_insight_box(title, content, icon="ph-sparkle"):
    """
    Render Insight Box yang Dinamis (Bisa custom title & content).
    Digunakan untuk menampilkan hasil analisis cluster.
    """
    st.markdown(f"""
    <div class="info-box">
        <i class="ph-duotone {icon}" style="font-size: 28px; color: #FF9900; margin-top: 2px;"></i>
        <div>
            <strong style="color: #FF9900; font-size: 15px; display: block; margin-bottom: 4px;">{title}</strong>
            <p style="margin: 0; font-size: 13px; color: #ccc; line-height: 1.5;">
                {content}
            </p>
        </div>
    </div>
    <br>
    """, unsafe_allow_html=True)