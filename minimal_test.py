"""
MINIMAL TEST - Letakkan di root folder dan jalankan: streamlit run minimal_test.py
Ini akan membantu kita isolate masalahnya
"""

import streamlit as st

st.set_page_config(page_title="Minimal Test", layout="wide")

st.title("🔬 Minimal Rendering Test")

# Test 1: Paling sederhana
st.markdown("---")
st.subheader("Test 1: Simplest HTML")
st.markdown("<h2 style='color: red;'>RED TEXT</h2>", unsafe_allow_html=True)

# Test 2: Apakah st.markdown berfungsi?
st.markdown("---")
st.subheader("Test 2: Check if unsafe_allow_html parameter works")

# Tanpa unsafe_allow_html
st.write("**Without unsafe_allow_html:**")
st.markdown("<p style='color: green;'>This should show as CODE</p>")

# Dengan unsafe_allow_html
st.write("**With unsafe_allow_html=True:**")
st.markdown("<p style='color: green;'>This should be GREEN</p>", unsafe_allow_html=True)

# Test 3: Pipeline sederhana
st.markdown("---")
st.subheader("Test 3: Simple Pipeline (No Icons)")

pipeline_html = """
<div style="display: flex; gap: 20px; padding: 20px; background: #2a2a2a; border-radius: 8px;">
    <div style="background: #3a3a3a; padding: 20px; border-radius: 8px; color: white;">
        Step 1
    </div>
    <div style="color: white; font-size: 24px;">→</div>
    <div style="background: #3a3a3a; padding: 20px; border-radius: 8px; color: white;">
        Step 2
    </div>
</div>
"""

st.markdown(pipeline_html, unsafe_allow_html=True)

# Test 4: Cek apakah ada konflik dengan multiline string
st.markdown("---")
st.subheader("Test 4: Single Line HTML")
st.markdown("<div style='padding: 20px; background: orange; color: black; border-radius: 8px;'>Orange Box</div>", unsafe_allow_html=True)

st.markdown("---")
st.info("""
**Interpretasi:**
- Jika Test 1 menampilkan "RED TEXT" dalam warna merah → HTML rendering OK
- Jika Test 1 menampilkan code HTML → Ada masalah serius dengan Streamlit setup
- Jika Test 3 menampilkan 2 kotak abu-abu dengan arrow → Flexbox OK
- Jika Test 3 menampilkan code HTML → Ada masalah dengan multiline strings
""")