import streamlit as st

def inject_custom_css():
    st.markdown("""
    <!-- Phosphor Icons CSS -->
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/regular/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/bold/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/fill/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/duotone/style.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

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
    
    .stApp { 
        background-color: var(--bg-dark);
    }

    /* --- 2. ANIMATIONS --- */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideIn {
        from { 
            opacity: 0;
            transform: translateY(20px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse-glow {
        0%, 100% { 
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
        }
        50% { 
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
        }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* --- 3. SIDEBAR NAVIGATION --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111418 0%, #0a0d10 100%);
        border-right: 1px solid var(--border-color);
        animation: fadeIn 0.5s ease-out;
    }

    /* Hide Radio Circles */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none;
    }

    /* Base Menu Item */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 8px;
        border: 1px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: var(--text-muted);
        background: transparent;
        display: flex;
        align-items: center;
        font-weight: 500;
    }

    /* Hover State */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.08);
        color: var(--text-white);
        transform: translateX(6px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Active/Selected State */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(135deg, var(--primary-dim) 0%, rgba(255, 153, 0, 0.05) 100%);
        border: 1px solid rgba(255, 153, 0, 0.4);
        color: var(--primary) !important;
        box-shadow: 0 4px 15px rgba(255, 153, 0, 0.2);
        transform: translateX(8px);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] p {
        color: var(--primary) !important;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    /* --- 4. ENHANCED METRIC CARD --- */
    .metric-card {
        background: linear-gradient(135deg, #1E232B 0%, #15181E 100%);
        border: 2px solid var(--border-color);
        border-radius: 14px;
        padding: 28px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: slideIn 0.6s ease-out;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 153, 0, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        border-color: var(--primary);
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 30px rgba(255, 153, 0, 0.2);
    }
    
    .metric-value { 
        font-size: 36px; 
        font-weight: 900; 
        color: white; 
        margin-top: 12px; 
        line-height: 1;
        font-family: 'Inter', monospace;
    }
    
    .metric-label { 
        font-size: 11px; 
        color: var(--text-muted); 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
        display: flex; 
        align-items: center; 
        gap: 8px; 
        font-weight: 700;
    }

    /* --- 5. PREMIUM BUTTONS --- */
    .stButton > button {
        background: linear-gradient(135deg, #FF9900 0%, #FFB84D 100%);
        color: #000000 !important;
        font-weight: 800 !important;
        border: none;
        border-radius: 10px;
        padding: 0.9rem 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(255, 153, 0, 0.3);
    }
    
    .stButton > button:hover { 
        transform: translateY(-3px) scale(1.05); 
        box-shadow: 0 8px 25px rgba(255, 153, 0, 0.5);
        background: linear-gradient(135deg, #FFB84D 0%, #FF9900 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* --- 6. ENHANCED INFO BOX --- */
    .info-box {
        background: linear-gradient(135deg, rgba(255, 153, 0, 0.08) 0%, rgba(255, 153, 0, 0.03) 100%);
        border-left: 4px solid var(--primary);
        padding: 24px;
        border-radius: 0 12px 12px 0;
        display: flex;
        gap: 18px;
        align-items: start;
        margin-top: 24px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 153, 0, 0.2);
        transition: all 0.3s ease;
        animation: slideIn 0.6s ease-out;
    }
    
    .info-box:hover {
        transform: translateX(4px);
        box-shadow: 0 8px 20px rgba(255, 153, 0, 0.15);
    }
    
    /* --- 7. SYSTEM STATUS FOOTER --- */
    .status-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-top: auto;
        transition: all 0.3s ease;
    }
    
    .status-container:hover {
        border-color: rgba(255, 153, 0, 0.3);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .status-pulse {
        animation: pulse-glow 2s ease-in-out infinite;
    }
    
    /* --- 8. LOADING & PROGRESS --- */
    .stProgress > div > div {
        background: linear-gradient(90deg, #FF9900 0%, #FFD700 100%);
    }
    
    /* --- 9. DATAFRAME ENHANCEMENTS --- */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    
    /* --- 10. SELECT & INPUT STYLING --- */
    .stSelectbox > div > div {
        background-color: #1A1F26;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary);
    }
    
    .stNumberInput > div > div > input {
        background-color: #1A1F26;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: white;
    }
    
    /* --- 11. CHECKBOX STYLING --- */
    .stCheckbox {
        transition: all 0.2s ease;
    }
    
    .stCheckbox:hover {
        transform: translateX(2px);
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render Ultra Premium Sidebar dengan Enhanced Styling"""
    with st.sidebar:
        # Premium Header Area
        st.markdown("""
        <div style="padding: 12px 0 35px 0; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <i class="ph-duotone ph-circles-three-plus" style="color: #FF9900; font-size: 26px;"></i>
                <div>
                    <span style="font-weight: 900; font-size: 22px; color: white; letter-spacing: -0.5px;">
                        RecSys
                    </span>
                    <div style="font-size: 9px; color: #555; font-weight: 600; letter-spacing: 1px; margin-top: 2px;">RECOMMENDATION SYSTEM</div>
                </div>
            </div>
            <div class="status-pulse" style="width: 10px; height: 10px; background: #10B981; border-radius: 50%; box-shadow: 0 0 10px #10B981;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p style="font-size: 10px; color: #555; font-weight: 800; margin-bottom: 15px; letter-spacing: 1.5px; text-transform: uppercase;"><i class="ph-fill ph-squares-four" style="margin-right: 6px; color: #FF9900;"></i>Main Modules</p>', unsafe_allow_html=True)
        
        # Navigation Menu
        page = st.radio(
            "Navigation", 
            ["   Dashboard Engine", "   Model Performance", "   Dataset Information"], 
            label_visibility="collapsed"
        )
        
        # Spacer
        st.markdown("<div style='height: 35vh'></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Enhanced System Health Footer
        st.markdown("""
        <div class="status-container">
            <div style="display: flex; align-items: center; margin-bottom: 14px; gap: 10px;">
                <i class="ph-duotone ph-cpu" style="color: #FF9900; font-size: 22px;"></i>
                <span style="font-size: 13px; color: white; font-weight: 700;">System Health</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #848991; margin-bottom: 8px; padding: 8px; background: rgba(0,0,0,0.2); border-radius: 6px;">
                <span style="display: flex; align-items: center; gap: 6px;">
                    <i class="ph-fill ph-git-branch" style="color: #3b82f6;"></i>
                    Algorithm
                </span>
                <span style="color: #FF9900; font-weight: 700; font-family: monospace;">K-Means v2</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #848991; padding: 8px; background: rgba(0,0,0,0.2); border-radius: 6px;">
                <span style="display: flex; align-items: center; gap: 6px;">
                    <i class="ph-fill ph-lightning" style="color: #10B981;"></i>
                    Latency
                </span>
                <span style="color: #10B981; font-family: monospace; font-weight: 700;">~24ms</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return page.strip()

def render_metric_card(label, value, icon):
    """Render Enhanced Premium Metric Card"""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">
            <i class="ph-duotone {icon}" style="color: #FF9900; font-size: 18px;"></i>
            <span>{label}</span>
        </div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_insight_box(title, content, icon="ph-sparkle"):
    """
    Render Ultra Premium Insight Box dengan Enhanced Styling
    Digunakan untuk menampilkan hasil analisis cluster.
    """
    st.markdown(f"""
    <div class="info-box">
        <i class="ph-duotone {icon}" style="font-size: 32px; color: #FF9900; margin-top: 2px;"></i>
        <div style="flex: 1;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <strong style="color: #FF9900; font-size: 16px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">{title}</strong>
                <i class="ph-fill ph-seal-check" style="color: #10B981; font-size: 18px;"></i>
            </div>
            <p style="margin: 0; font-size: 14px; color: #ccc; line-height: 1.7;">
                {content}
            </p>
        </div>
    </div>
    <br>
    """, unsafe_allow_html=True)