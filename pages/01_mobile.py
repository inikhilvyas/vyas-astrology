import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="VYAS ASTRA • Sovereign Mobile App",
    page_icon="static/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit Chrome & Headers for pure app feel
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stApp { margin: 0 !important; padding: 0 !important; background: #060913 !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    div.block-container { padding: 0 !important; max-width: 100% !important; }
    iframe { border: none !important; width: 100% !important; height: 100vh !important; }
</style>
""", unsafe_allow_html=True)

html_path = os.path.join(os.path.dirname(__file__), "..", "mobile", "src", "index.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Fix relative paths to work inside Streamlit
    css_path = os.path.join(os.path.dirname(__file__), "..", "mobile", "src", "css", "mobile-elite.css")
    js_path = os.path.join(os.path.dirname(__file__), "..", "mobile", "src", "js", "app-core.js")
    
    css_content = open(css_path, "r", encoding="utf-8").read() if os.path.exists(css_path) else ""
    js_content = open(js_path, "r", encoding="utf-8").read() if os.path.exists(js_path) else ""
    
    # Inline CSS and JS so it loads 100% offline and standalone with zero 404s
    html_code = html_code.replace('<link rel="stylesheet" href="css/mobile-elite.css">', f'<style>{css_content}</style>')
    html_code = html_code.replace('<script src="js/app-core.js"></script>', f'<script>{js_content}</script>')
    html_code = html_code.replace('src="assets/logo_icon.png"', 'src="/app/static/logo_icon.png"')
    
    components.html(html_code, height=920, scrolling=True)
else:
    st.error("Mobile interface assets loading...")
