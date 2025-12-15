import streamlit as st
import joblib
import src.ui_components as ui

# Import Halaman-Halaman Baru
import src.page_dashboard as page_dashboard
import src.page_performance as page_performance
import src.page_dataset as page_dataset

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Amazon RecSys | Enterprise",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
ui.inject_custom_css()

# --- 2. GLOBAL RESOURCE LOADER ---
@st.cache_resource
def load_resources():
    try:
        return joblib.load('models/recsys_model.pkl')
    except FileNotFoundError:
        return None

# --- 3. MAIN CONTROLLER ---
def main():
    # Load Model Sekali Saja di Awal
    artifacts = load_resources()
    
    if not artifacts:
        st.error("⚠️ Model artifacts not found. Please run `python src/train_model.py` first.")
        st.stop()

    # Render Sidebar & Dapatkan Pilihan User
    selected_page = ui.render_sidebar()

    # Routing Logic (Pengarah Halaman)
    if "Dashboard" in selected_page:
        page_dashboard.render(artifacts)
        
    elif "Performance" in selected_page:
        page_performance.render()
        
    elif "Dataset" in selected_page:
        page_dataset.render(artifacts)

if __name__ == "__main__":
    main()