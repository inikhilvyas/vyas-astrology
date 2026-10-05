import streamlit as st
from datetime import datetime, timezone, timedelta, time as d_time
import sys
import os
import re
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import base64

# Ensure the vyas module is in the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from vyas.ephem import planet_positions, ascendant_sidereal
from vyas.chart import Chart, PlanetState
from vyas.varga import calculate_vargas_detailed, get_all_vargas_matrix, format_dms as format_varga_dms, SIGNS as VARGA_SIGNS
from vyas import constants
from vyas.svg_chart import get_north_indian_chart_svg, get_south_indian_chart_svg
from vyas.kp import (
    calculate_placidus_cusps_sidereal,
    calculate_sub_lords,
    compute_kp_significators,
    get_ruling_planets,
    KPCusp,
    calculate_planet_kp_lords,
    compute_kp_4fold_house_significators,
    evaluate_kp_house_promises,
    evaluate_active_houses_by_dasha
)
from vyas.dasha import VimshottariDasha
from vyas import ephem as vyas_ephem
from vyas import panchang as vyas_panchang
from vyas import gochar as vyas_gochar
from vyas.predictive_engine import synthesize_prediction
from vyas import chakras as vyas_chakras
from vyas import nadi as vyas_nadi
from vyas import sutra_bank as vyas_sutra_bank
from vyas import ashtakavarga as vyas_ashtaka
from vyas import shadbala as vyas_shadbala
from vyas import chalit as vyas_chalit
from vyas import jaimini as vyas_jaimini
from vyas import forensic_predictor
from vyas import publication_engine
from vyas import auth_vault
from vyas import lalkitab as vyas_lalkitab
from vyas import daily_horoscope as vyas_daily
from vyas import btr as vyas_btr
from vyas import varga_predictions as vyas_vp
from vyas import match as vyas_match

def render_kundli(svg_str: str):
    """Render astrological SVG cleanly via base64 data URI to prevent DOMPurify stripping."""
    clean = re.sub(r'<!--.*?-->', '', svg_str, flags=re.DOTALL)
    clean = re.sub(r'\s+', ' ', clean).strip()
    b64 = base64.b64encode(clean.encode('utf-8')).decode('utf-8')
    st.html(f'<div class="kundli-container"><img src="data:image/svg+xml;base64,{b64}" style="max-width: 100%; height: auto; display: block; margin: 0 auto;" /></div>')

st.set_page_config(page_title="VYAS • Vedic Yield Astrology Systems", page_icon="☸️", layout="wide", initial_sidebar_state="expanded")

# Global Luxury Vedic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Tiro+Devanagari+Sanskrit&family=Noto+Sans+Devanagari:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');

    :root {
        --gold-primary: #f0c05a;
        --gold-light: #fef0cd;
        --bg-deep: #070b16;
        --card-bg: rgba(14, 23, 47, 0.82);
        --card-border: rgba(240, 192, 90, 0.3);
        --accent-ruby: #e63946;
        --accent-emerald: #2a9d8f;
    }

    @keyframes cosmicShimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes goldPulse {
        0%, 100% { box-shadow: 0 10px 35px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(240, 192, 90, 0.3); border-color: rgba(240, 192, 90, 0.35); }
        50% { box-shadow: 0 14px 45px rgba(240, 192, 90, 0.25), inset 0 1px 0 rgba(240, 192, 90, 0.6); border-color: rgba(240, 192, 90, 0.65); }
    }
    @keyframes badgeFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-2px); }
    }
    @keyframes textGlow {
        0%, 100% { text-shadow: 0 0 15px rgba(240, 192, 90, 0.3); }
        50% { text-shadow: 0 0 28px rgba(240, 192, 90, 0.65); }
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #111e3b 0%, #070b16 70%, #03050a 100%) !important;
        font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', sans-serif !important;
        color: #e2e8f0 !important;
    }

    /* Top Executive Header */
    .vyas-banner {
        background: linear-gradient(180deg, rgba(22, 34, 66, 0.95) 0%, rgba(10, 16, 33, 0.98) 100%);
        border: 1px solid rgba(240, 192, 90, 0.35);
        border-radius: 16px;
        padding: 24px 28px;
        text-align: center;
        animation: goldPulse 5s infinite ease-in-out;
        margin-bottom: 22px;
        position: relative;
    }
    .vyas-banner::before {
        content: "";
        position: absolute;
        top: 0; left: 10%; right: 10%; height: 2px;
        background: linear-gradient(90deg, transparent, #f0c05a, transparent);
    }
    .vyas-title {
        font-family: 'Cinzel', serif;
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: 2.5px;
        background: linear-gradient(135deg, #fff2cc 0%, #f0c05a 50%, #d49429 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        animation: textGlow 4s infinite ease-in-out;
    }
    .vyas-subtitle {
        font-family: 'Tiro Devanagari Sanskrit', serif;
        font-size: 1.18rem;
        font-weight: 600;
        color: #eedc9a;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .vyas-badge-bar {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 10px;
    }
    .vyas-badge {
        background: rgba(240, 192, 90, 0.12);
        border: 1px solid rgba(240, 192, 90, 0.35);
        border-radius: 20px;
        padding: 5px 16px;
        font-size: 0.85rem;
        color: #f7d584;
        font-weight: 600;
        transition: all 0.3s ease;
        animation: badgeFloat 4s infinite ease-in-out;
    }
    .vyas-badge:hover {
        background: rgba(240, 192, 90, 0.25);
        border-color: #f0c05a;
        box-shadow: 0 4px 15px rgba(240, 192, 90, 0.3);
    }

    /* Cards with Glassmorphism & Micro-animations */
    .glass-card {
        background: rgba(14, 23, 47, 0.78);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(240, 192, 90, 0.28);
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.5);
        transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.35s;
    }
    .glass-card:hover {
        border-color: rgba(240, 192, 90, 0.6);
        box-shadow: 0 12px 36px rgba(240, 192, 90, 0.22);
        transform: translateY(-3px);
    }

    .section-title {
        font-family: 'Cinzel', 'Noto Sans Devanagari', serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #f0c05a;
        letter-spacing: 1px;
        border-bottom: 1px solid rgba(240, 192, 90, 0.3);
        padding-bottom: 10px;
        margin-top: 8px;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Domain Suite Pills (Segmented Selector) */
    div[data-testid="stRadio"] > div {
        flex-wrap: wrap;
        gap: 10px;
    }
    div[data-testid="stRadio"] label {
        background: rgba(14, 23, 47, 0.88) !important;
        border: 1px solid rgba(240, 192, 90, 0.3) !important;
        border-radius: 12px !important;
        padding: 11px 20px !important;
        color: #d1d5db !important;
        font-weight: 600 !important;
        font-size: 0.94rem !important;
        transition: all 0.28s ease !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] label:hover {
        border-color: #f0c05a !important;
        color: #fef0cd !important;
        background: rgba(240, 192, 90, 0.16) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(229, 169, 60, 0.38) 0%, rgba(14, 23, 47, 0.95) 100%) !important;
        border-color: #f0c05a !important;
        color: #ffd97d !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 18px rgba(240, 192, 90, 0.3) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"], .stTabs [role="tablist"] {
        gap: 10px;
        background-color: rgba(9, 15, 30, 0.88);
        padding: 8px 14px;
        border-radius: 14px;
        border: 1px solid rgba(240, 192, 90, 0.25);
    }
    .stTabs [data-baseweb="tab"], .stTabs button[role="tab"] {
        height: 44px;
        background-color: transparent;
        border-radius: 10px;
        color: #b0bac9;
        font-size: 0.92rem;
        font-weight: 600;
        padding: 8px 18px;
        transition: all 0.25s ease;
        border: none;
    }
    .stTabs [data-baseweb="tab"]:hover, .stTabs button[role="tab"]:hover {
        color: #f7d584;
        background: rgba(240, 192, 90, 0.12);
    }
    .stTabs [aria-selected="true"], .stTabs button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(229, 169, 60, 0.32) 0%, rgba(14, 23, 47, 0.95) 100%) !important;
        color: #f7d584 !important;
        border: 1px solid rgba(240, 192, 90, 0.55) !important;
        font-weight: 700 !important;
    }

    /* Kundli Container */
    .kundli-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 16px;
        background: radial-gradient(circle at 50% 50%, rgba(20, 32, 60, 0.65) 0%, rgba(7, 11, 22, 0.92) 100%);
        border: 1px solid rgba(240, 192, 90, 0.35);
        border-radius: 16px;
        box-shadow: 0 10px 36px rgba(0, 0, 0, 0.65), inset 0 0 25px rgba(240, 192, 90, 0.08);
        margin-bottom: 22px;
        transition: transform 0.3s ease;
    }
    .kundli-container:hover {
        transform: scale(1.01);
    }

    /* Predictive Alert Cards */
    .predict-card {
        background: rgba(15, 23, 42, 0.88);
        border-left: 4px solid #f0c05a;
        border-top: 1px solid rgba(240, 192, 90, 0.22);
        border-right: 1px solid rgba(240, 192, 90, 0.22);
        border-bottom: 1px solid rgba(240, 192, 90, 0.22);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-left-color 0.3s ease;
    }
    .predict-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(240, 192, 90, 0.16);
        border-left-color: #ffd97d;
    }
    .predict-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f0c05a;
        margin-bottom: 8px;
    }

    /* -------------------------------------------------------------
       CRITICAL FIXES: DARK GLASSMORPHISM SIDEBAR & DEVANAGARI FONTS
       ------------------------------------------------------------- */
    /* Force complete dark background on Streamlit Sidebar */
    section[data-testid="stSidebar"] {
        background: #090e1a !important;
        background-color: #090e1a !important;
        border-right: 1px solid rgba(240, 192, 90, 0.22) !important;
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        background: #090e1a !important;
        background-color: #090e1a !important;
    }
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #e2e8f0 !important;
        font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #f0c05a !important;
        font-family: 'Cinzel', 'Noto Sans Devanagari', serif !important;
    }

    /* Streamlit Input Fields in Sidebar */
    section[data-testid="stSidebar"] div[data-baseweb="input"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border: 1px solid rgba(240, 192, 90, 0.35) !important;
        color: #f7d584 !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] input {
        color: #fef0cd !important;
        font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', sans-serif !important;
    }

    /* -------------------------------------------------------------
       PRIORITY 2: ROYAL GOLD CTA BUTTON WITH DEEP BLACK HIGH-CONTRAST TEXT
       ------------------------------------------------------------- */
    div.stButton > button[kind="primary"], 
    div.stButton > button,
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(135deg, #e5a93c 0%, #fcd375 50%, #c98822 100%) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.5px !important;
        border: 2px solid #ffd97d !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 20px rgba(212, 148, 41, 0.45) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 12px 24px !important;
        text-shadow: none !important;
    }
    div.stButton > button *,
    section[data-testid="stSidebar"] div.stButton > button * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 900 !important;
    }
    div.stButton > button:hover,
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, #fcd375 0%, #fff2cc 50%, #e5a93c 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(247, 213, 132, 0.65) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* Expander styling in dark mode */
    .streamlit-expanderHeader,
    details summary {
        background: rgba(14, 23, 47, 0.85) !important;
        border: 1px solid rgba(240, 192, 90, 0.25) !important;
        border-radius: 8px !important;
        color: #f0c05a !important;
    }

    /* -------------------------------------------------------------
       CRITICAL ICON BUG FIX: PRESERVE GOOGLE MATERIAL SYMBOLS
       Prevents 'keyboard_double_arrow_left' and 'arrow_right' raw ligature leaks
       ------------------------------------------------------------- */
    span[data-testid="stIconMaterial"],
    span[data-testid*="stIcon"],
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stExpandSidebarButton"] span,
    [data-testid="stExpanderToggleIcon"] span,
    button[data-testid="stSidebarCollapseButton"] *,
    button[data-testid="stExpandSidebarButton"] *,
    details summary svg,
    details summary span {
        font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
        font-feature-settings: 'liga' 1 !important;
        -webkit-font-feature-settings: 'liga' 1 !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* Target typography cleanly WITHOUT overriding Streamlit internal icon SVGs & spans */
    body, p, label, .stMarkdown:not([data-testid*="stIcon"]), .stText, h1, h2, h3, h4, h5, h6, input, select, textarea, button:not([data-testid*="Sidebar"]):not([data-testid*="stExpander"]) {
        font-family: 'Noto Sans Devanagari', 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# Master Header with Interactive 60fps Cosmic Particle Canvas
st.components.v1.html("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Tiro+Devanagari+Sanskrit&family=Plus+Jakarta+Sans:wght@500;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: transparent; overflow: hidden; font-family: 'Plus Jakarta Sans', sans-serif; }
        #canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; }
        .vyas-banner {
            position: relative;
            z-index: 2;
            background: linear-gradient(180deg, rgba(16, 26, 52, 0.88) 0%, rgba(7, 12, 26, 0.96) 100%);
            border: 1px solid rgba(240, 192, 90, 0.4);
            border-radius: 16px;
            padding: 20px 24px;
            text-align: center;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(240, 192, 90, 0.3);
        }
        .vyas-title {
            font-family: 'Cinzel', serif;
            font-size: 2.5rem;
            font-weight: 900;
            letter-spacing: 3px;
            background: linear-gradient(135deg, #fff2cc 0%, #f0c05a 50%, #d49429 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2px;
            text-shadow: 0 0 25px rgba(240, 192, 90, 0.4);
        }
        .vyas-subtitle {
            font-family: 'Tiro Devanagari Sanskrit', serif;
            font-size: 1.15rem;
            font-weight: 600;
            color: #eedc9a;
            letter-spacing: 0.8px;
            margin-bottom: 8px;
        }
        .vyas-badge-bar {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 6px;
        }
        .vyas-badge {
            background: rgba(240, 192, 90, 0.12);
            border: 1px solid rgba(240, 192, 90, 0.35);
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 0.82rem;
            color: #f7d584;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <div class="vyas-banner">
        <div style="font-family: 'Tiro Devanagari Sanskrit', serif; font-size: 1.1rem; color: #f0c05a; letter-spacing: 2px;">|| श्री गणेशाय नमः ||</div>
        <div class="vyas-title">VYAS ASTRA</div>
        <div class="vyas-subtitle">Vedic Yield Astrology Systems • बहु-पद्धति शोध-स्तरीय ज्योतिष शोध प्रबंध</div>
        <div class="vyas-badge-bar">
            <span class="vyas-badge">👤 निखिल व्यास (एम.ए. ज्योतिष - स्नातकोत्तर / M.A. Jyotish)</span>
            <span class="vyas-badge">📞 +91-9414121172</span>
            <span class="vyas-badge">✉️ inikhilvyas@gmail.com</span>
            <span class="vyas-badge">🪐 JPL Ephemeris DE440s</span>
            <span class="vyas-badge">⚡ Sub-Arcsec Precision</span>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        const stars = [];
        for (let i = 0; i < 45; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.6 + 0.4,
                alpha: Math.random() * 0.8 + 0.2,
                speed: Math.random() * 0.03 + 0.01,
                dx: (Math.random() - 0.5) * 0.3,
                dy: (Math.random() - 0.5) * 0.3
            });
        }

        function animate() {
            ctx.clearRect(0, 0, width, height);
            stars.forEach(s => {
                s.alpha += s.speed;
                if (s.alpha > 1 || s.alpha < 0.2) s.speed = -s.speed;
                s.x += s.dx;
                s.y += s.dy;
                if (s.x < 0) s.x = width;
                if (s.x > width) s.x = 0;
                if (s.y < 0) s.y = height;
                if (s.y > height) s.y = 0;

                ctx.beginPath();
                ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(240, 192, 90, ' + Math.abs(s.alpha) + ')';
                ctx.shadowBlur = 6;
                ctx.shadowColor = '#f0c05a';
                ctx.fill();
            });
            requestAnimationFrame(animate);
        }
        animate();
    </script>
</body>
</html>
""", height=185)

# Sidebar Native Setup
with st.sidebar:
    # Use transparent PNG logo with cosmic gold halo
    logo_file = "logo.png" if os.path.exists(os.path.join(os.path.dirname(__file__), "logo.png")) else "logo.jpg"
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 10px;">
        <img src="data:image/png;base64,{base64.b64encode(open(os.path.join(os.path.dirname(__file__), logo_file), 'rb').read()).decode()}" 
             style="max-width: 170px; height: auto; filter: drop-shadow(0 0 16px rgba(240, 192, 90, 0.45));" />
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><small style='color: #eedc9a;'><b>System Architect:</b> Nikhil Vyas (M.A. Jyotish / PG in Astrology)</small></div><hr style='border-color: rgba(240,192,90,0.2);'>", unsafe_allow_html=True)
    
    # ---------------- MOBILE 1-CLICK PWA APP INSTALLATION (NATIVE PROMPT) ----------------
    st.components.v1.html("""
    <div id="pwa-install-container" style="display: none; background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(14, 23, 47, 0.95) 100%);
                border: 1px solid rgba(96, 165, 250, 0.5); border-radius: 12px; padding: 12px 14px; margin-bottom: 12px; text-align: center;">
        <div style="font-size: 0.9rem; font-weight: 800; color: #93c5fd; font-family: sans-serif;">📲 VYAS ASTRA ऐप इंस्टॉल करें</div>
        <div style="font-size: 0.76rem; color: #cbd5e1; margin: 4px 0 10px 0; font-family: sans-serif;">अपने फोन की होम स्क्रीन पर सीधे 1-क्लिक में ऐप जोड़ें।</div>
        <button id="pwa-install-btn" style="background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: 1px solid #60a5fa; border-radius: 8px; padding: 8px 18px; font-weight: 700; font-size: 0.85rem; cursor: pointer; width: 100%; box-shadow: 0 4px 12px rgba(37,99,235,0.4);">
            ⚡ अभी इंस्टॉल करें (Install Now)
        </button>
    </div>

    <script>
        let deferredPrompt;
        const container = document.getElementById('pwa-install-container');
        const installBtn = document.getElementById('pwa-install-btn');

        // Automatically trigger when browser detects installable PWA
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            container.style.display = 'block';
        });

        // Always show button on mobile devices so user can trigger it
        if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
            container.style.display = 'block';
        }

        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                if (outcome === 'accepted') {
                    container.style.display = 'none';
                }
                deferredPrompt = null;
            } else {
                alert("मोबाइल पर इंस्टॉल करने के लिए ब्राउज़र के शीर्ष मेनू (⋮ या शेयर आइकन) पर टैप करके 'Add to Home screen' चुनें।");
            }
        });
    </script>
    """, height=125)
    
    # ---------------- USER AUTH & 30-DAY VIP TRIAL VAULT ----------------
    if "user" not in st.session_state:
        st.session_state["user"] = {
            "id": 1,
            "name": "नया जातक (Seeker)",
            "email": "seeker@vyasastro.com",
            "tier": "VIP_TRIAL",
            "days_left": 30,
            "is_vip": True
        }

    u = st.session_state["user"]
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(240, 192, 90, 0.25) 0%, rgba(14, 23, 47, 0.95) 100%);
                border: 1px solid rgba(240, 192, 90, 0.6); border-radius: 10px; padding: 10px 14px; text-align: center; margin-bottom: 8px;">
        <div style="color: #f7d584; font-weight: 800; font-size: 0.95rem;">👑 VIP PRO TRIAL ACTIVE</div>
        <div style="color: #eedc9a; font-size: 0.8rem; margin-top: 2px;">{u['name']} • <b>{u['days_left']} Days Left</b> (30-Day Free Trial)</div>
    </div>
    """, unsafe_allow_html=True)

    # Hybrid Payment & Upgrade VIP Modal
    with st.expander("💳 Upgrade VIP / प्रीमियम सदस्यता लें", expanded=False):
        st.markdown("""
        <div style="font-size: 0.85rem; color: #eedc9a; margin-bottom: 8px;">
            <b>VIP Pro प्लान्स:</b> असीमित कुंडलियां, 30+ पेज PDF, D60 देवता, लाल किताब व BTR का पूर्ण एक्सेस।
        </div>
        """, unsafe_allow_html=True)
        plan_sel = st.selectbox("चुनें प्लान (Select Plan)", [
            "🥈 वार्षिक प्रो (Annual VIP Pro) - ₹999 / वर्ष",
            "🥉 मासिक (Monthly Starter) - ₹199 / माह",
            "🥇 लाइफटाइम एलीट (Lifetime Elite) - ₹2,499"
        ])
        
        plan_key = "annual"
        amount = 999
        if "मासिक" in plan_sel:
            plan_key = "monthly"
            amount = 199
        elif "लाइफटाइम" in plan_sel:
            plan_key = "lifetime"
            amount = 2499

        # Dynamic UPI Link & Exact Amount QR Code
        upi_id = "inikhilvyas@ybl"
        payee_name = "Nikhil Vyas"
        import urllib.parse
        upi_uri = f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(payee_name)}&am={amount}.00&cu=INR&tn={urllib.parse.quote('VYAS VIP Subscription')}"
        encoded_uri = urllib.parse.quote(upi_uri)
        # Generate online QR code image URL with exact payment amount embedded
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded_uri}"

        st.markdown(f"""
        <div style="text-align: center; background: rgba(10, 16, 32, 0.9); border: 1px solid #f0c05a; border-radius: 12px; padding: 14px; margin-top: 8px;">
            <div style="color: #f0c05a; font-weight: 800; font-size: 0.95rem;">📲 Scan & Pay ₹{amount} (Exact Amount QR)</div>
            <div style="color: #eedc9a; font-size: 0.8rem;">(PhonePe, GPay, Paytm, BHIM - स्कैन करते ही ₹{amount} अपने आप आ जाएगा)</div>
            <div style="margin: 12px 0;">
                <img src="{qr_url}" width="180" height="180" style="border-radius: 10px; border: 2px solid #eedc9a; background: white; padding: 6px;"/>
            </div>
            <div style="font-size: 0.85rem; color: #f7d584;"><b>UPI ID:</b> <code>{upi_id}</code></div>
            <div style="font-size: 0.95rem; color: #48cae4; font-weight: 800; margin-top: 5px;">कुल देय राशि: ₹{amount}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<small style='color: #eedc9a;'><b>भुगतान के बाद पुष्टि करें (Verification):</b></small>", unsafe_allow_html=True)
        txn_input = st.text_input("UPI Reference / UTR No.", placeholder="e.g. 428192849120", key="txn_field")
        
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            if st.button("✅ Confirm Payment", use_container_width=True):
                if txn_input and len(txn_input) >= 6:
                    ok, up_msg = auth_vault.upgrade_vip(u["id"], plan_key, txn_input)
                    if ok:
                        st.session_state["user"]["tier"] = "VIP_PAID"
                        st.session_state["user"]["is_vip"] = True
                        st.success(up_msg)
                        st.rerun()
                    else:
                        st.error(up_msg)
                else:
                    st.warning("कृपया मान्य UTR / ट्रांजैक्शन नंबर दर्ज करें।")
        with col_pay2:
            wa_text = f"Namaste Nikhil Ji, I have paid INR {amount} for VYAS VIP ({plan_key}). UTR: {txn_input}"
            wa_url = f"https://wa.me/919414121172?text={wa_text.replace(' ', '%20')}"
            st.markdown(f"""
            <a href="{wa_url}" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; background: #25D366; color: white; border: none; border-radius: 6px; padding: 7px; font-weight: 700; font-size: 0.85rem; cursor: pointer;">
                    💬 WhatsApp Help
                </button>
            </a>
            """, unsafe_allow_html=True)

    with st.expander("👤 User Account / Login / Register", expanded=False):
        auth_mode = st.radio("Account Action", ["Quick Register (New User)", "Login (Existing)"], horizontal=True)
        if "Register" in auth_mode:
            reg_name = st.text_input("Full Name", "New Seeker")
            reg_email = st.text_input("Email", "seeker@example.com")
            reg_pwd = st.text_input("Password", type="password")
            if st.button("Activate 30-Day Free VIP Trial", use_container_width=True):
                ok, msg, u_data = auth_vault.register_user(reg_email, reg_name, reg_pwd)
                if ok and u_data:
                    st.session_state["user"] = u_data
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            log_email = st.text_input("Registered Email", "inikhilvyas@gmail.com")
            log_pwd = st.text_input("Password", type="password", key="log_pwd")
            if st.button("Login", use_container_width=True):
                ok, msg, u_data = auth_vault.login_user(log_email, log_pwd)
                if ok and u_data:
                    st.session_state["user"] = u_data
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    # Saved Kundlis Vault
    saved_list = auth_vault.get_saved_kundlis(u["id"])
    if saved_list:
        with st.expander(f"📁 My Kundli Vault ({len(saved_list)} Saved)", expanded=False):
            k_names = [f"{k['name']} ({k['dob']})" for k in saved_list]
            selected_k_idx = st.selectbox("Load Saved Kundli", range(len(saved_list)), format_func=lambda i: k_names[i])
            if st.button("⚡ Load Profile into Workspace", use_container_width=True):
                sk = saved_list[selected_k_idx]
                st.session_state['loaded_profile'] = sk
                st.rerun()

    ui_lang = st.radio("🌐 भाषा / Language", ["हिन्दी (Hindi)", "English"], horizontal=True)
    is_hi = "हिन्दी" in ui_lang
    
    st.header("Native Details / जातक विवरण" if is_hi else "Native Details")
    mode = st.radio("Mode / प्रकार" if is_hi else "Mode", ["Natal Kundli (जन्म कुण्डली)", "Prashna (प्रश्न कुण्डली)"] if is_hi else ["Natal Kundli", "Prashna (Horary)"], horizontal=True)
    
    lp = st.session_state.get('loaded_profile', {})
    default_name = lp.get('name', 'जातक / Seeker')
    default_city = lp.get('city', 'New Delhi, India')
    default_lat = float(lp.get('lat', 28.6139))
    default_lon = float(lp.get('lon', 77.2090))
    
    if "Natal" in mode:
        name = st.text_input("Name / नाम" if is_hi else "Name", default_name)
        date_val = st.date_input("Date of Birth / जन्म तिथि" if is_hi else "Date of Birth", value=datetime(1995, 1, 1).date(), min_value=datetime(1900, 1, 1).date(), max_value=datetime(2100, 12, 31).date(), format="DD/MM/YYYY")
        
        # Exact HH:MM:SS input for ultra micro-precision
        st.markdown("<small style='color: #f0c05a;'><b>Time of Birth (Hours : Mins : Secs) / जन्म समय</b></small>", unsafe_allow_html=True)
        t_col1, t_col2, t_col3 = st.columns(3)
        tob_hour = t_col1.number_input("Hour (घंटा)", min_value=0, max_value=23, value=12)
        tob_min = t_col2.number_input("Min (मिनट)", min_value=0, max_value=59, value=0)
        tob_sec = t_col3.number_input("Sec (सेकंड)", min_value=0, max_value=59, value=0)
        time_val = d_time(int(tob_hour), int(tob_min), int(tob_sec))
    else:
        name = st.text_input("Querent Name / प्रच्छक का नाम" if is_hi else "Querent Name", "Querent")
        st.info("Prashna uses exact current time / प्रश्न कुण्डली में तात्कालिक समय प्रयुक्त होगा।")
        now = datetime.now()
        date_val = now.date()
        time_val = now.time()

    st.subheader("Birth Place / जन्म स्थान" if is_hi else "Birth Place")
    city_name = st.text_input("City Name / नगर" if is_hi else "City Name", default_city)
    
    if st.button("🔍 Search City / नगर खोजें" if is_hi else "🔍 Search City", use_container_width=True):
        if city_name:
            geolocator = Nominatim(user_agent="vyas_astro_software_v4")
            try:
                location = geolocator.geocode(city_name, timeout=5)
                if location:
                    st.session_state['lat'] = round(location.latitude, 4)
                    st.session_state['lon'] = round(location.longitude, 4)
                    st.success(f"Found: {location.address}")
                else:
                    st.warning("City not found. You can adjust Latitude/Longitude directly below.")
            except Exception as e:
                st.warning(f"Online city search unavailable ({e}). You can enter Latitude/Longitude directly below.")
        else:
            st.error("Please enter a city name.")
            
    coord_col1, coord_col2 = st.columns(2)
    lat = coord_col1.number_input("Latitude (°N) / अक्षांश" if is_hi else "Latitude (°N)", value=float(st.session_state.get('lat', default_lat)), format="%.4f", step=0.01)
    lon = coord_col2.number_input("Longitude (°E) / रेखांश" if is_hi else "Longitude (°E)", value=float(st.session_state.get('lon', default_lon)), format="%.4f", step=0.01)
    st.session_state['lat'] = lat
    st.session_state['lon'] = lon
    
    tz_offset = st.number_input("Timezone Offset (Hours) / समय क्षेत्र", value=5.5, step=0.5)
    
    col_ay1, col_ay2 = st.columns(2)
    with col_ay1:
        ayan_choice = st.selectbox("Ayanamsa (अयनांश)", ["Lahiri", "KP", "Raman"], index=0)
    with col_ay2:
        node_choice = st.selectbox("राहु-केतु नोड (Rahu Node)", ["Mean (औसत)", "True (स्पष्ट)"], index=0)

    # Save to vault button
    if st.button("💾 Save Profile to Vault / वॉल्ट में सेव करें", use_container_width=True):
        k_payload = {
            "name": name,
            "dob": date_val.strftime("%Y-%m-%d"),
            "tob": time_val.strftime("%H:%M:%S"),
            "city": city_name,
            "lat": lat,
            "lon": lon,
            "tz": tz_offset,
            "ayanamsa": ayan_choice
        }
        ok, s_msg = auth_vault.save_kundli(u["id"], k_payload)
        if ok:
            st.success(s_msg)
        else:
            st.warning(s_msg)
    
    btn_lbl = "☸️ कुण्डली बनाएं एवं फलादेश देखें (Generate Kundli)" if is_hi else "☸️ Generate Kundli & Astrological Analysis"
    generate = st.button(btn_lbl, type="primary", use_container_width=True)

# Calculate Core Structures
if generate or 'data_generated' not in st.session_state:
    dt = datetime.combine(date_val, time_val)
    dt_utc = dt - timedelta(hours=tz_offset)
    dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    vyas_ephem.set_ayanamsa(ayan_choice)
    vyas_ephem.set_node_model("true" if "True" in node_choice else "mean")
    with st.spinner("Executing Micro-Degree Ephemeris, D60 & KP Cuspal Mathematics..."):
        try:
            raw_pos = planet_positions(dt_utc)
            asc_lon = ascendant_sidereal(dt_utc, lat, lon)
            
            planets = {n: PlanetState(n, p.longitude, p.speed) for n, p in raw_pos.items()}
            chart = Chart(asc_lon, planets)
            
            # Placidus cusps
            kp_cusps = calculate_placidus_cusps_sidereal(dt_utc, lat, lon)
            
            # Vimshottari Dasha Engine
            dasha_eng = VimshottariDasha(chart.planets["Moon"].longitude, dt)
            vargas_matrix = get_all_vargas_matrix(chart)
            
            st.session_state['birth'] = {'local': dt, 'lat': lat, 'lon': lon, 'tz': tz_offset, 'name': name, 'city': city_name}
            st.session_state['chart'] = chart
            st.session_state['kp_cusps'] = kp_cusps
            st.session_state['dasha_engine'] = dasha_eng
            st.session_state['vargas_matrix'] = vargas_matrix
            st.session_state['data_generated'] = True
            for k in ('panchang', 'gochar', 'predictions'):
                st.session_state.pop(k, None)
        except Exception as e:
            st.error(f"Error calculating: {e}")

if st.session_state.get('data_generated'):
    chart = st.session_state['chart']
    birth = st.session_state['birth']
    kp_cusps = st.session_state['kp_cusps']
    dasha_engine = st.session_state['dasha_engine']
    vargas_matrix = st.session_state['vargas_matrix']
    asc_sign_idx = chart.ascendant_sign

    # Global predictive and astrological precomputations
    dignities = forensic_predictor.analyze_all_planetary_dignities(chart, vargas_matrix)
    bhavas = forensic_predictor.analyze_all_12_bhavas(chart, dignities)
    p_signs = {n: p.sign_index for n, p in chart.planets.items()}
    av_res = vyas_ashtaka.compute_ashtakavarga(p_signs, asc_sign_idx)
    sav = av_res["sav"]
    cur_dasha = dasha_engine.get_running_dasha(datetime.now()) if hasattr(dasha_engine, 'get_running_dasha') else dasha_engine.get_dasha_at(datetime.now())

    d1_houses = {h: [] for h in range(1, 13)}
    for h in range(1, 13):
        sign = (asc_sign_idx + h - 1) % 12
        d1_houses[h].append(str(sign + 1))
        
    for p_name, p in chart.planets.items():
        house_num = (p.sign_index - asc_sign_idx + 12) % 12 + 1
        p_hi_abbr = constants.PLANETS_HI.get(p_name, p_name)[:2] if is_hi else p_name[:2]
        abbr = f"{p_hi_abbr} {int(p.longitude % 30)}°{int((p.longitude % 1)*60):02d}'"
        if p.is_retrograde:
            abbr += " (R)" if not is_hi else " (व)"
        d1_houses[house_num].append(abbr)

    # -------------------------------------------------------------------------
    # DOMAIN SUITE NAVIGATION (Pure Astrology & Research Suites)
    # -------------------------------------------------------------------------
    suite_options = [
        "🌞 व्यक्तिगत दैनिक राशिफल" if is_hi else "🌞 Personalised Daily Horoscope",
        "🌟 कुण्डली एवं षोडशवर्ग" if is_hi else "🌟 Charts & 16 Vargas",
        "💍 अष्टकूट मिलान एवं दोष परिहार" if is_hi else "💍 Ashtakoota Match & Dosha Parihara",
        "📕 लाल किताब सम्पूर्ण" if is_hi else "📕 Lal Kitab System & Remedies",
        "🔮 दशा, गोचर एवं वर्षफल" if is_hi else "🔮 Dasha, Transits & Varshphal",
        "⏳ जन्म समय शुद्धि (BTR)" if is_hi else "⏳ Birth Time Rectification (BTR)",
        "⚖️ अष्टकवर्ग, षड्बल एवं मैत्री" if is_hi else "⚖️ Ashtakavarga & Strengths",
        "👑 केपी, जैमिनी, नाड़ी एवं चक्र" if is_hi else "👑 KP, Jaimini, Nadi & Chakras",
        "📄 35+ पेज शोध प्रबंध PDF" if is_hi else "📄 35+ Page Publication PDF"
    ]
    
    selected_suite = st.radio("चयनित ज्योतिषीय अनुसंधान प्रभाग (Select Domain Suite):", suite_options, horizontal=True)

    # =========================================================================
    # SUITE 0: 🌞 HYPER-PERSONALISED DAILY HOROSCOPE
    # =========================================================================
    if "दैनिक" in selected_suite or "Daily" in selected_suite:
        st.markdown(f'<div class="section-title">{"🌞 जातक का व्यक्तिगत दैनिक राशिफल (नवतारा चक्र + गोचर + चालू दशा)" if is_hi else "🌞 Personalised Daily Horoscope (Navatara + Transit + Active Dasha)"}</div>', unsafe_allow_html=True)
        
        # Calculate daily horoscope using current UTC time
        now_dt = datetime.now()
        # Transit moon longitude using current time
        try:
            cur_raw_pos = planet_positions(now_dt.replace(tzinfo=timezone.utc))
            transit_moon_lon = cur_raw_pos["Moon"].longitude
        except Exception:
            transit_moon_lon = (chart.planets["Moon"].longitude + 13.2) % 360.0
        
        cur_dasha_str = cur_dasha.get("full_path", "Jupiter-Saturn") if isinstance(cur_dasha, dict) else str(cur_dasha)
        daily_res = vyas_daily.generate_daily_horoscope(
            chart.planets["Moon"].longitude,
            chart.ascendant_longitude,
            cur_dasha_str,
            transit_moon_lon,
            now_dt
        )

        # Render Top Score Cards
        score = daily_res["overall_score"]
        score_color = "#2a9d8f" if score >= 75 else ("#e9c46a" if score >= 55 else "#e63946")
        
        col_s1, col_s2, col_s3 = st.columns([1, 1.8, 1.2])
        with col_s1:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; border: 2px solid {score_color}; padding: 22px;">
                <div style="font-size: 0.85rem; color: #eedc9a; font-weight: 700;">आज का समग्र प्रभाव</div>
                <div style="font-size: 3rem; font-weight: 900; color: {score_color}; font-family: 'Cinzel', serif;">{score}%</div>
                <div style="font-size: 0.82rem; color: #f7d584; font-weight: 600;">{daily_res['today_str']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_s2:
            st.markdown(f"""
            <div class="glass-card" style="padding: 18px 22px;">
                <div style="font-size: 1.15rem; font-weight: 700; color: #f0c05a;">☸️ {daily_res['tara_name']}</div>
                <div style="font-size: 0.95rem; color: #e2e8f0; margin-top: 6px;">{daily_res['tara_desc']}</div>
                <hr style="border-color: rgba(240, 192, 90, 0.2); margin: 10px 0;">
                <div style="font-size: 0.85rem; color: #eedc9a;">
                    <b>जन्म नक्षत्र:</b> {daily_res['natal_nakshatra']} &nbsp;|&nbsp; 
                    <b>आज का गोचर नक्षत्र:</b> {daily_res['transit_nakshatra']} &nbsp;|&nbsp; 
                    <b>सक्रिय दशा:</b> {daily_res['running_dasha']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_s3:
            st.markdown(f"""
            <div class="glass-card" style="padding: 16px 20px;">
                <div style="font-size: 0.85rem; color: #f7d584;"><b>⏰ अमृत वेला (शुभ समय):</b><br><span style="color: #48cae4; font-weight: 700;">{daily_res['amrit_vela']}</span></div>
                <div style="font-size: 0.85rem; color: #f7d584; margin-top: 8px;"><b>⚠️ राहुकाल (सावधानी समय):</b><br><span style="color: #ff858d; font-weight: 700;">{daily_res['rahu_kalam']}</span></div>
                <div style="font-size: 0.85rem; color: #eedc9a; margin-top: 8px;"><b>🎨 लकी रंग:</b> {daily_res['lucky_color']}</div>
            </div>
            """, unsafe_allow_html=True)

        # 4 Area Meters
        st.markdown("#### 📊 जीवन के 4 प्रमुख क्षेत्रों का दैनिक मीटर")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("💼 आजीविका व करियर", f"{daily_res['scores']['career']}%")
        m_col2.metric("💰 धन व वित्त", f"{daily_res['scores']['wealth']}%")
        m_col3.metric("❤️ संबंध व दांपत्य", f"{daily_res['scores']['love']}%")
        m_col4.metric("🧘 स्वास्थ्य व मानसिक शांति", f"{daily_res['scores']['health']}%")

        # Daily Remedy Card
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #2a9d8f; background: rgba(42, 157, 143, 0.12); padding: 16px 20px;">
            <div style="color: #2a9d8f; font-weight: 800; font-size: 1.05rem;">🛡️ आज का विशेष अचूक उपाय (Daily Astro Remedy)</div>
            <div style="color: #fdf5e6; font-size: 0.95rem; margin-top: 4px;">{daily_res['remedy']}</div>
        </div>
        """, unsafe_allow_html=True)

    # =========================================================================
    # SUITE: 📕 LAL KITAB SYSTEM & REMEDIES
    # =========================================================================
    if "लाल किताब" in selected_suite or "Lal Kitab" in selected_suite:
        st.markdown(f'<div class="section-title">{"📕 लाल किताब संपूर्ण विश्लेषण एवं अचूक घरेलू उपाय (पं. रूपचंद जोशी व जी.डी. वशिष्ठ)" if is_hi else "📕 Lal Kitab System & Authentic Remedies"}</div>', unsafe_allow_html=True)
        
        planets_dict = {n: {"sign_index": p.sign_index, "longitude": p.longitude} for n, p in chart.planets.items()}
        lk_res = vyas_lalkitab.analyze_lalkitab(planets_dict, asc_sign_idx)

        # Badges for Dharmi and Andhi Kundli
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.markdown(f"""
            <div class="glass-card" style="padding: 14px 18px; border-left: 4px solid #f0c05a;">
                <div style="font-weight: 700; color: #f0c05a;">तेवा प्रकृति (Tewa Type):</div>
                <div style="color: #fef0cd; font-size: 0.95rem;">{lk_res['summary']['dharmi_status']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_l2:
            st.markdown(f"""
            <div class="glass-card" style="padding: 14px 18px; border-left: 4px solid #e63946;">
                <div style="font-weight: 700; color: #e63946;">दृष्टि स्थिति (Sight Status):</div>
                <div style="color: #fef0cd; font-size: 0.95rem;">{lk_res['summary']['andhi_status']}</div>
            </div>
            """, unsafe_allow_html=True)

        if lk_res['sleeping_houses']:
            st.info(f"😴 **सोए हुए घर (Sleeping Houses):** भाव {', '.join(str(h) for h in lk_res['sleeping_houses'])} — इन भावों के फलों को जाग्रत करने हेतु संबंधित उपायों की आवश्यकता है।")
        if lk_res['sleeping_planets']:
            st.warning(f"🌙 **सोए हुए ग्रह (Sleeping Planets):** {', '.join(lk_res['sleeping_planets'])} — यह ग्रह अपनी पूर्ण क्षमता से फल देने में असमर्थ हैं।")

        st.markdown("#### 🪐 9 ग्रहों की भाव स्थिति एवं अचूक लाल किताब उपाय")
        st.dataframe(pd.DataFrame(lk_res["planet_details"]), use_container_width=True, hide_index=True)

    # =========================================================================
    # SUITE: ⏳ BIRTH TIME RECTIFICATION (BTR)
    # =========================================================================
    if "जन्म समय शुद्धि" in selected_suite or "BTR" in selected_suite:
        st.markdown(f'<div class="section-title">{"⏳ जन्म समय शुद्धि (Birth Time Rectification - कुन्द व तत्व शोधन)" if is_hi else "⏳ Birth Time Rectification (BTR Engine)"}</div>', unsafe_allow_html=True)
        st.info("ऋषि पराशर एवं आधुनिक KP अनुसंधान के अनुसार जन्म समय में 1-2 मिनट का भी अंतर लग्न कस्प, D60 और सब-लॉर्ड्स को बदल देता है। नीचे दिए गए शास्त्रीय परीक्षणों से अपने समय की प्रामाणिकता जांचें:")

        k_ok, k_nak, k_msg = vyas_btr.kunda_shodhana(chart.ascendant_longitude, chart.planets["Moon"].longitude)
        t_ok, t_name, t_msg = vyas_btr.tattva_shodhana(birth['local'], gender="Male")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid {'#2a9d8f' if k_ok else '#e63946'};">
                <div style="font-weight: 700; color: #f0c05a;">1. कुन्द शुद्धि (Kunda Shodhana - 81x गुणनफल)</div>
                <div style="color: #eedc9a; margin-top: 4px;">कुन्द नक्षत्र: <b>{k_nak}</b></div>
                <div style="color: #fdf5e6; font-size: 0.9rem; margin-top: 4px;">{k_msg}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_b2:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid {'#2a9d8f' if t_ok else '#e63946'};">
                <div style="font-weight: 700; color: #f0c05a;">2. तत्व शुद्धि (Tattva Shodhana - पंचतत्व लिंग परीक्षण)</div>
                <div style="color: #eedc9a; margin-top: 4px;">सक्रिय तत्व: <b>{t_name}</b></div>
                <div style="color: #fdf5e6; font-size: 0.9rem; margin-top: 4px;">{t_msg}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 🔍 ±10 मिनट विंडो ऑटोमैटिक सेकंड्स स्कैनर (Automated Time Rectifier)")
        if st.button("🚀 Run Multi-Factor BTR Scanner (सटीक समय की खोज करें)", use_container_width=True):
            with st.spinner("Scanning micro-time variations across Kunda & Tattva matrices..."):
                candidates = vyas_btr.scan_rectification_window(
                    birth['local'], birth['lat'], birth['lon'], birth['tz'],
                    chart.planets['Moon'].longitude, gender="Male", window_minutes=10
                )
                if candidates:
                    st.success("सर्वाधिक सटीक एवं गणितीय रूप से शुद्ध संभावित जन्म समय:")
                    st.dataframe(pd.DataFrame(candidates), use_container_width=True, hide_index=True)
                else:
                    st.info("वर्तमान दर्ज समय ही गणितीय रूप से सर्वाधिक संतुलित है।")



    # =========================================================================
    # SUITE 1: 🌟 CHARTS & 16 VARGAS
    # =========================================================================
    if "कुण्डली" in selected_suite or "Charts" in selected_suite:
        sub_tab1, sub_tab2, sub_tab3 = st.tabs([
            "लग्न एवं नवमांश (D1 & D9 Charts)" if is_hi else "D1 & D9 Natal Charts",
            "षोडशवर्ग 16 चक्र (All 16 Vargas)" if is_hi else "All 16 Divisional Charts",
            "षष्ट्यंश देवता (D60 Shashtyamsha & Deities)" if is_hi else "D60 Shashtyamsha Deities"
        ])

        with sub_tab1:
            st.markdown(f'<div class="section-title">{"✨ वैदिक ग्रह स्थिति एवं जन्म कुण्डली" if is_hi else "✨ Vedic Planetary Positions & Natal Charts"}</div>', unsafe_allow_html=True)
            
            # Overview metric cards
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 20px;">
                <div class="glass-card" style="text-align: center; padding: 12px;">
                    <div style="color: #eedc9a; font-size: 0.8rem; font-weight: 600;">{'जातक का नाम' if is_hi else 'NATIVE NAME'}</div>
                    <div style="color: #f0c05a; font-size: 1.15rem; font-weight: 700; font-family: 'Cinzel', serif;">{birth.get('name', 'Nikhil Vyas')}</div>
                </div>
                <div class="glass-card" style="text-align: center; padding: 12px;">
                    <div style="color: #eedc9a; font-size: 0.8rem; font-weight: 600;">{'जन्म लग्न' if is_hi else 'LAGNA (ASCENDANT)'}</div>
                    <div style="color: #f0c05a; font-size: 1.15rem; font-weight: 700;">{constants.SIGNS_HI[asc_sign_idx] if is_hi else constants.SIGNS[asc_sign_idx]} ({format_varga_dms(chart.ascendant_longitude)})</div>
                </div>
                <div class="glass-card" style="text-align: center; padding: 12px;">
                    <div style="color: #eedc9a; font-size: 0.8rem; font-weight: 600;">{'चन्द्र राशि एवं नक्षत्र' if is_hi else 'MOON RASHI & NAKSHATRA'}</div>
                    <div style="color: #f0c05a; font-size: 1.15rem; font-weight: 700;">{constants.SIGNS_HI[chart.planets['Moon'].sign_index] if is_hi else chart.planets['Moon'].sign_name} • {constants.NAKSHATRAS_HI[int(chart.planets['Moon'].longitude // constants.NAKSHATRA_SPAN) % 27] if is_hi else constants.NAKSHATRAS[int(chart.planets['Moon'].longitude // constants.NAKSHATRA_SPAN) % 27]}</div>
                </div>
                <div class="glass-card" style="text-align: center; padding: 12px;">
                    <div style="color: #eedc9a; font-size: 0.8rem; font-weight: 600;">{'अयनांश' if is_hi else 'AYANAMSA'}</div>
                    <div style="color: #f0c05a; font-size: 1.15rem; font-weight: 700;">{vyas_ephem.AYANAMSA_NAME}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            chart_style = st.radio("Kundli Style (कुंडली प्रारूप)", ["North Indian (उत्तर भारतीय हीरा शैली)", "South Indian (दक्षिण भारतीय चौकोर शैली)"], horizontal=True)

            col1, col2 = st.columns([1.1, 1.3])
            with col1:
                title_txt = f"{'लग्न चक्र: ' if is_hi else 'D1 Lagna: '}{constants.SIGNS_HI[asc_sign_idx] if is_hi else constants.SIGNS[asc_sign_idx]} {format_varga_dms(chart.ascendant_longitude)}"
                if "South" in chart_style:
                    si_data = {r: [] for r in range(12)}
                    for p_name, p in chart.planets.items():
                        abbr = f"{constants.PLANETS_HI.get(p_name, p_name)[:2] if is_hi else p_name[:2]} {int(p.longitude % 30)}°{int((p.longitude % 1)*60):02d}'"
                        if p.is_retrograde:
                            abbr += " (व)" if is_hi else " (R)"
                        si_data[p.sign_index].append(abbr)
                    svg_d1 = get_south_indian_chart_svg(si_data, asc_sign_idx, size=430, chart_title=title_txt)
                else:
                    svg_d1 = get_north_indian_chart_svg(d1_houses, size=430, chart_title=title_txt)
                render_kundli(svg_d1)
                
            with col2:
                st.markdown(f"#### {'🪐 ग्रह स्पष्ट एवं अधिपति तालिका' if is_hi else '🪐 Planetary Degrees & Dispositor Matrix'}")
                p_data = []
                asc_nak = int(chart.ascendant_longitude // constants.NAKSHATRA_SPAN) % 27
                asc_pada = int((chart.ascendant_longitude % constants.NAKSHATRA_SPAN) // constants.PADA_SPAN) + 1
                asc_subs = calculate_sub_lords(chart.ascendant_longitude, depth=4)
                
                p_data.append({
                    "ग्रह" if is_hi else "Graha": "लग्न (Ascendant)" if is_hi else "Lagna (Asc)",
                    "राशि" if is_hi else "Rashi": constants.SIGNS_HI[asc_sign_idx] if is_hi else constants.SIGNS[asc_sign_idx],
                    "स्पष्ट अंश" if is_hi else "Degree (DMS)": format_varga_dms(chart.ascendant_longitude),
                    "नक्षत्र" if is_hi else "Nakshatra": constants.NAKSHATRAS_HI[asc_nak] if is_hi else constants.NAKSHATRAS[asc_nak],
                    "पद" if is_hi else "Pada": asc_pada,
                    "राशि स्वामी" if is_hi else "Rashi Lord": constants.PLANETS_HI.get(constants.SIGN_LORD[asc_sign_idx], constants.SIGN_LORD[asc_sign_idx]) if is_hi else constants.SIGN_LORD[asc_sign_idx],
                    "नक्षत्र स्वामी" if is_hi else "Star Lord (NL)": constants.PLANETS_HI.get(asc_subs["NL"], asc_subs["NL"]) if is_hi else asc_subs["NL"],
                    "उप-स्वामी" if is_hi else "Sub Lord (SL)": constants.PLANETS_HI.get(asc_subs["SL"], asc_subs["SL"]) if is_hi else asc_subs["SL"],
                    "गति" if is_hi else "Speed": "-"
                })
                for p_name, p in chart.planets.items():
                    subs = calculate_sub_lords(p.longitude, depth=4)
                    nak_idx = int(p.longitude // constants.NAKSHATRA_SPAN) % 27
                    p_label = constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name
                    if p.is_retrograde:
                        p_label += " (वक्री)" if is_hi else " (R)"
                    p_data.append({
                        "ग्रह" if is_hi else "Graha": p_label,
                        "राशि" if is_hi else "Rashi": constants.SIGNS_HI[p.sign_index] if is_hi else p.sign_name,
                        "स्पष्ट अंश" if is_hi else "Degree (DMS)": format_varga_dms(p.longitude),
                        "नक्षत्र" if is_hi else "Nakshatra": constants.NAKSHATRAS_HI[nak_idx] if is_hi else constants.NAKSHATRAS[nak_idx],
                        "पद" if is_hi else "Pada": p.pada,
                        "राशि स्वामी" if is_hi else "Rashi Lord": constants.PLANETS_HI.get(constants.SIGN_LORD[p.sign_index], constants.SIGN_LORD[p.sign_index]) if is_hi else constants.SIGN_LORD[p.sign_index],
                        "नक्षत्र स्वामी" if is_hi else "Star Lord (NL)": constants.PLANETS_HI.get(subs["NL"], subs["NL"]) if is_hi else subs["NL"],
                        "उप-स्वामी" if is_hi else "Sub Lord (SL)": constants.PLANETS_HI.get(subs["SL"], subs["SL"]) if is_hi else subs["SL"],
                        "गति" if is_hi else "Speed": f"{p.speed:.3f}°/d"
                    })
                st.dataframe(pd.DataFrame(p_data), use_container_width=True, hide_index=True)

        with sub_tab2:
            st.markdown(f'<div class="section-title">{"षोडशवर्ग 16 कुण्डलियाँ (Shodashvarga 16 Divisional Charts)" if is_hi else "Shodashvarga 16 Divisional Charts"}</div>', unsafe_allow_html=True)
            varga_list = ["D9", "D10", "D60", "D2", "D3", "D4", "D7", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45"]
            varga_sel = st.selectbox("जाँच हेतु वर्ग कुण्डली का चयन करें (Select Divisional Chart):", varga_list, index=0)
            
            asc_v_pos = vargas_matrix[varga_sel]["Ascendant"]
            v_houses = {h: [] for h in range(1, 13)}
            for h in range(1, 13):
                sign = (asc_v_pos.sign_index + h - 1) % 12
                v_houses[h].append(str(sign + 1))
                
            for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                pv_pos = vargas_matrix[varga_sel][p_name]
                house_num = (pv_pos.sign_index - asc_v_pos.sign_index + 12) % 12 + 1
                p_abbr = constants.PLANETS_HI.get(p_name, p_name)[:2] if is_hi else p_name[:2]
                v_houses[house_num].append(f"{p_abbr} {pv_pos.dms_str}")
                
            vcol1, vcol2 = st.columns([1, 1.2])
            with vcol1:
                st.markdown(f"<h4 style='text-align: center; color: #f0c05a;'>{varga_sel} {'कुण्डली' if is_hi else 'Kundli'}</h4>", unsafe_allow_html=True)
                svg_v = get_north_indian_chart_svg(v_houses, size=400, chart_title=f"{varga_sel} Lagna: {asc_v_pos.sign_name} {asc_v_pos.dms_str}")
                render_kundli(svg_v)
                
            with vcol2:
                st.markdown(f"#### {varga_sel} {'सूक्ष्म ग्रह स्थिति' if is_hi else 'Micro-Positions'}")
                v_rows = []
                v_rows.append({
                    "बिंदु" if is_hi else "Point": "लग्न (Lagna)" if is_hi else "Lagna",
                    "राशि" if is_hi else "Divisional Sign": constants.SIGNS_HI[asc_v_pos.sign_index] if is_hi else asc_v_pos.sign_name,
                    "वर्ग में अंश" if is_hi else "Degree in Varga": asc_v_pos.dms_str,
                    "राशि स्वामी" if is_hi else "Sign Lord": constants.PLANETS_HI.get(constants.SIGN_LORD[asc_v_pos.sign_index], constants.SIGN_LORD[asc_v_pos.sign_index]) if is_hi else constants.SIGN_LORD[asc_v_pos.sign_index],
                    "षष्ट्यंश देवता" if is_hi else "D60 Deity": asc_v_pos.deity if varga_sel == "D60" else "-",
                    "प्रकृति" if is_hi else "Disposition": ("शुभ (Benefic)" if asc_v_pos.is_benefic else "अशुभ (Malefic)") if varga_sel == "D60" else "-"
                })
                for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                    p_v_res = vargas_matrix[varga_sel][p_name]
                    v_rows.append({
                        "बिंदु" if is_hi else "Point": constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name,
                        "राशि" if is_hi else "Divisional Sign": constants.SIGNS_HI[p_v_res.sign_index] if is_hi else p_v_res.sign_name,
                        "वर्ग में अंश" if is_hi else "Degree in Varga": p_v_res.dms_str,
                        "राशि स्वामी" if is_hi else "Sign Lord": constants.PLANETS_HI.get(constants.SIGN_LORD[p_v_res.sign_index], constants.SIGN_LORD[p_v_res.sign_index]) if is_hi else constants.SIGN_LORD[p_v_res.sign_index],
                        "षष्ट्यंश देवता" if is_hi else "D60 Deity": p_v_res.deity if varga_sel == "D60" else "-",
                        "प्रकृति" if is_hi else "Disposition": ("शुभ (Benefic)" if p_v_res.is_benefic else "अशुभ (Malefic)") if varga_sel == "D60" else "-"
                    })
                st.dataframe(pd.DataFrame(v_rows), use_container_width=True, hide_index=True)

            # Automated Varga Prediction Card (Relative to D1 Lagna)
            vp_planets = {p: {"sign_index": vargas_matrix[varga_sel][p].sign_index, "sign_name": vargas_matrix[varga_sel][p].sign_name}
                          for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]}
            v_pred = vyas_vp.predict_varga(varga_sel, asc_v_pos.sign_index, vp_planets, asc_sign_idx)
            st.markdown(f"""
            <div class="glass-card" style="margin-top: 15px; border-left: 4px solid #f0c05a;">
                <div style="font-weight: 800; font-size: 1.1rem; color: #f0c05a; margin-bottom: 6px;">
                    📜 {varga_sel} वर्ग फलित एवं लग्न सापेक्ष विश्लेषण (Automated Synthesis)
                </div>
                <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;">
                    {v_pred['narrative']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with sub_tab3:
            st.markdown(f'<div class="section-title">{"D60 षष्ट्यंश विश्लेषण एवं अधिष्ठाता देवता (Prarabdha Karma Alignment)" if is_hi else "D60 Shashtyamsha & Deities"}</div>', unsafe_allow_html=True)
            st.info("पाराशरी सिद्धांत: षष्ट्यंश कुण्डली में पूर्वजन्म संचित प्रारब्ध एवं कर्म संस्कारों का अंतिम निर्णय होता है। प्रत्येक 30 कला (0°30') पर विशिष्ट अधिष्ठाता देवता का आधिपत्य होता है।")
            d60_table = []
            for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                pv = vargas_matrix["D60"][p_name]
                d60_table.append({
                    "ग्रह" if is_hi else "Planet": constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name,
                    "D60 राशि" if is_hi else "D60 Sign": constants.SIGNS_HI[pv.sign_index] if is_hi else pv.sign_name,
                    "अंश": pv.dms_str,
                    "अधिष्ठाता देवता": pv.deity,
                    "प्रकृति / स्वभाव": "शुभ (Benefic)" if pv.is_benefic else "अशुभ / शोधन योग्य"
                })
            st.dataframe(pd.DataFrame(d60_table), use_container_width=True, hide_index=True)

    # =========================================================================
    # SUITE: 💍 ASHTAKOOTA MILAN & DOSHA CANCELLATIONS
    # =========================================================================
    elif "अष्टकूट" in selected_suite or "Ashtakoota" in selected_suite:
        st.markdown(f'<div class="section-title">{"💍 अष्टकूट गुण मिलान (36 गुण) एवं शास्त्रीय दोष परिहार विश्लेषण" if is_hi else "💍 Ashtakoota 36 Gunas Match & Classical Dosha Cancellation"}</div>', unsafe_allow_html=True)
        st.info("विवाह मिलान केवल 36 में से 18 गुण मिलाने तक सीमित नहीं है। ऋषि पराशर एवं मुहुर्त चिंतामणि के अनुसार यदि नाड़ी या भकूट में शास्त्रीय परिहार (Exceptions) लागू हो जाएं, तो शून्य अंक भी दोषमुक्त होकर शुभ फल प्रदान करते हैं।")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("<h4 style='color: #48cae4;'>👦 वर विवरण (Boy Details)</h4>", unsafe_allow_html=True)
            boy_name = st.text_input("वर का नाम (Boy Name)", birth.get('name', 'वर (Groom)'), key="match_boy_name")
            boy_m_lon = chart.planets["Moon"].longitude
            boy_mars_h = (chart.planets["Mars"].sign_index - asc_sign_idx + 12) % 12 + 1
            st.markdown(f"<b>चन्द्र राशि:</b> {constants.SIGNS_HI[int(boy_m_lon // 30) % 12]} | <b>नक्षत्र:</b> {constants.NAKSHATRAS_HI[int(boy_m_lon // constants.NAKSHATRA_SPAN) % 27]} | <b>मंगल भाव:</b> भाव {boy_mars_h}", unsafe_allow_html=True)

        with col_m2:
            st.markdown("<h4 style='color: #ff858d;'>👧 कन्या विवरण (Girl Details)</h4>", unsafe_allow_html=True)
            girl_name = st.text_input("कन्या का नाम (Girl Name)", "कन्या (Bride)", key="match_girl_name")
            girl_sign_choice = st.selectbox("कन्या की चन्द्र राशि (Girl Moon Sign)", constants.SIGNS_HI, index=(int(boy_m_lon // 30) + 4) % 12, key="match_girl_sign")
            girl_sign_idx = constants.SIGNS_HI.index(girl_sign_choice)
            girl_deg_in_sign = st.slider("कन्या चन्द्र अंश (Degrees in Sign)", min_value=0.0, max_value=29.9, value=15.0, step=0.5, key="match_girl_deg")
            girl_m_lon = girl_sign_idx * 30.0 + girl_deg_in_sign
            girl_mars_h = st.number_input("कन्या की कुण्डली में मंगल का भाव (Girl Mars House 1-12)", min_value=1, max_value=12, value=1, key="match_girl_mars")

        match_res = vyas_match.calculate_ashtakoota(boy_m_lon, girl_m_lon, boy_mars_h, girl_mars_h)

        # Overview score card
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; border: 2px solid #f0c05a; margin-top: 15px; margin-bottom: 20px;">
            <div style="font-size: 0.95rem; color: #eedc9a; font-weight: 700;">अष्टकूट कुल प्राप्तांक (TOTAL ASHTAKOOTA SCORE)</div>
            <div style="font-size: 3rem; font-weight: 900; color: #ffd97d; font-family: 'Cinzel', serif; margin: 4px 0;">
                {match_res['total_score']} / {match_res['max_score']} <span style="font-size: 1.2rem; color: #cbd5e1;">गुण</span>
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; color: {'#4ade80' if match_res['total_score'] >= 18 else '#f87171'};">
                {match_res['verdict']}
            </div>
            <div style="font-size: 0.95rem; color: #93c5fd; margin-top: 8px;">
                <b>मांगलिक (कुज) दोष स्थिति:</b> {match_res['manglik_status']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"#### 📜 8 कूटों का विस्तृत परीक्षण एवं दोष परिहार सारणी")
        st.dataframe(pd.DataFrame(match_res["kootas"]), use_container_width=True, hide_index=True)
    elif "दशा" in selected_suite or "Dasha" in selected_suite:
        d_tab1, d_tab2, d_tab3, d_tab4 = st.tabs([
            "विंशोत्तरी 5-स्तरीय दशा (Vimshottari 5-Levels)" if is_hi else "Vimshottari 5-Levels",
            "योगिनी दशा चक्र (Yogini Dasha 36-Year)" if is_hi else "Yogini Dasha",
            "ताजिक वर्षफल एवं मुन्था (Tajik Varshphal)" if is_hi else "Tajik Varshphal",
            "गोचर संचरण (Realtime Gochar Transits)" if is_hi else "Gochar Transits"
        ])

        with d_tab1:
            st.markdown(f'<div class="section-title">{"विंशोत्तरी दशा: 5-स्तरीय सूक्ष्म समय कालक्रम" if is_hi else "Vimshottari 5-Fold Micro-Dasha"}</div>', unsafe_allow_html=True)
            cur_dasha = dasha_engine.get_running_dasha(datetime.now()) if hasattr(dasha_engine, 'get_running_dasha') else dasha_engine.get_dasha_at(datetime.now())
            st.markdown(f"""
            <div class="glass-card">
                <span style="color: #eedc9a; font-weight: bold;">{'वर्तमान सक्रिय 5-स्तरीय दशा: ' if is_hi else 'Current Active 5-Level Dasha: '}</span>
                <span style="color: #f0c05a; font-size: 1.15rem; font-weight: bold;">
                    {constants.PLANETS_HI.get(cur_dasha['MD']['lord'], cur_dasha['MD']['lord'])} MD | 
                    {constants.PLANETS_HI.get(cur_dasha['AD']['lord'], cur_dasha['AD']['lord'])} AD | 
                    {constants.PLANETS_HI.get(cur_dasha['PD']['lord'], cur_dasha['PD']['lord'])} PD | 
                    {constants.PLANETS_HI.get(cur_dasha['SD']['lord'], cur_dasha['SD']['lord'])} SD | 
                    {constants.PLANETS_HI.get(cur_dasha['PrD']['lord'], cur_dasha['PrD']['lord'])} PrD
                </span>
                <div style="color: #a0aec0; font-size: 0.85rem; margin-top: 4px;">
                    {'प्रत्यन्तर्दशा समाप्ति:' if is_hi else 'Pratyantar Ends:'} {cur_dasha['PD']['end']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Active Dasha Phala Synthesis (दशा फल)
            active_dasha_synth = forensic_predictor.compute_active_dasha_synthesis(chart, cur_dasha, dignities, bhavas)
            st.markdown(f"""
            <div class="predict-card" style="border-left-color: #ffd97d; margin-top: 15px; margin-bottom: 20px;">
                <div class="predict-header" style="color: #ffd97d; font-size: 1.15rem;">
                    👑 वर्तमान सक्रिय विंशोत्तरी दशा महा-फलित (Active MD-AD-PD Synthesis)
                </div>
                <div style="font-size: 1.02rem; line-height: 1.7; color: #f8fafc; white-space: pre-line; margin-top: 8px;">
                    {active_dasha_synth['synthesis_hi']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"#### {'120-वर्षीय महादशा चक्र' if is_hi else '120-Year Mahadasha Trajectory'}")
            mds = dasha_engine.calculate_mahadashas(num_cycles=1)
            md_table = []
            for md in mds:
                md_table.append({
                    "महादशा स्वामी" if is_hi else "MD Lord": constants.PLANETS_HI.get(md.lord, md.lord) if is_hi else md.lord,
                    "आरम्भ तिथि" if is_hi else "Start Date": md.start_date.strftime("%d/%m/%Y"),
                    "समाप्ति तिथि" if is_hi else "End Date": md.end_date.strftime("%d/%m/%Y"),
                    "पूर्ण अवधि" if is_hi else "Duration": f"{constants.VIMSHOTTARI_YEARS.get(md.lord, 0)} {'वर्ष' if is_hi else 'Years'}"
                })
            st.dataframe(pd.DataFrame(md_table), use_container_width=True, hide_index=True)

        with d_tab2:
            st.markdown(f'<div class="section-title">{"योगिनी दशा: 36-वर्षीय जीवन चक्र एवं अन्तर्दशाएँ" if is_hi else "Yogini Dasha 36-Year Lifecycle"}</div>', unsafe_allow_html=True)
            y_cycles = forensic_predictor.compute_yogini_dasha(chart.planets["Moon"].longitude, birth["local"])
            y_table = []
            for yc in y_cycles[:16]:
                y_table.append({
                    "योगिनी नाम" if is_hi else "Yogini": yc["name_hi"] if is_hi else yc["name"],
                    "स्वामी ग्रह" if is_hi else "Lord": yc["lord_hi"] if is_hi else yc["lord"],
                    "अवधि" if is_hi else "Years": f"{yc['years']} {'वर्ष' if is_hi else 'Years'}",
                    "आरम्भ" if is_hi else "Start": yc["start"],
                    "समाप्ति" if is_hi else "End": yc["end"]
                })
            st.dataframe(pd.DataFrame(y_table), use_container_width=True, hide_index=True)

        with d_tab3:
            st.markdown(f'<div class="section-title">{"ताजिक वर्षफल एवं मुन्था विचार (Annual Solar Return)" if is_hi else "Tajik Varshphal & Muntha"}</div>', unsafe_allow_html=True)
            col_v1, col_v2 = st.columns([1, 2])
            with col_v1:
                varsh_choice = st.number_input(
                    "वर्षफल वर्ष का चयन करें (Target Varshphal Year):" if is_hi else "Target Varshphal Year:",
                    min_value=birth['local'].year,
                    max_value=birth['local'].year + 100,
                    value=2026,
                    step=1,
                    key="interactive_varsh_year_choice"
                )
            v_data = forensic_predictor.compute_tajik_varshphal(birth["local"], chart.planets["Sun"].longitude, int(varsh_choice), asc_sign_idx)
            
            with col_v2:
                st.markdown(f"""
                <div class="glass-card" style="margin-top: 10px;">
                    <div style="font-weight: bold; color: #f0c05a; font-size: 1.05rem;">
                        📅 वर्ष चक्र: {v_data.get('target_year', varsh_choice)}-{int(v_data.get('target_year', varsh_choice))+1} (आयु {v_data.get('age', 0)} वर्ष)
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.92rem; margin-top: 4px;">
                        अवधि: {v_data.get('varsha_start', '')} से {v_data.get('varsha_end', '')} | वर्ष लग्न: <b>{v_data.get('varsha_lagna_hi', 'लग्न')}</b> | वर्षेश: <b>{v_data.get('varshesh_hi', 'वर्षेश')}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="predict-card">
                <div class="predict-header">🎯 मुन्था स्थिति एवं वार्षिक महा-फलादेश:</div>
                <div style="font-size: 1.15rem; font-weight: bold; color: #4ade80;">{v_data.get('annual_summary_hi', '')}</div>
                <p style="margin-top: 8px; color: #e2e8f0; line-height: 1.6;">
                    मुन्था जन्म लग्न से <b>{v_data.get('muntha_house', 1)}वें भाव ({v_data.get('muntha_sign_hi', '')} राशि)</b> में संचरण कर रही है। {v_data.get('muntha_phal_hi', '')}
                </p>
                <div style="background: rgba(240, 192, 90, 0.1); border-left: 3px solid #f0c05a; padding: 8px 12px; border-radius: 4px; margin-top: 6px; color: #ffd97d; font-size: 0.9rem;">
                    📖 <b>ताजिक नीलकण्ठी सूत्र:</b> यदि मुन्था 1, 2, 3, 5, 9, 10, 11 भावों में हो तो वर्ष अत्यंत शुभ, पदोन्नति, धन लाभ एवं यश प्रदायक होता है। त्रिक भावों (6, 8, 12) में स्वास्थ्य व विवादों से सतर्कता अपेक्षित है।
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"#### {'वार्षिक मुद्धा दशा तालिका (1-Year Patyayini Dasha)' if is_hi else 'Annual Mudda Dasha'}")
            mudda_df = []
            for md in v_data["mudda_periods"]:
                mudda_df.append({
                    "दशा स्वामी": md["planet_hi"] if is_hi else md["planet"],
                    "आरम्भ तिथि": md["start"],
                    "समाप्ति तिथि": md["end"],
                    "अवधि": f"{md['days']} दिन",
                    "प्रभाव फलित": f"{md['planet_hi']} के प्रभाव से वर्ष में इस अवधि में कर्म, स्वास्थ्य व वित्त पर विशेष प्रभाव रहता है।"
                })
            st.dataframe(pd.DataFrame(mudda_df), use_container_width=True, hide_index=True)

        with d_tab4:
            st.markdown(f'<div class="section-title">{"तात्कालिक गोचर संचरण एवं शास्त्रीय वेध विश्लेषण" if is_hi else "Gochar Transits & Vedha Analysis"}</div>', unsafe_allow_html=True)
            if hasattr(vyas_gochar, "get_current_transit_positions"):
                gochar_pos = vyas_gochar.get_current_transit_positions()
            else:
                pos_now = vyas_ephem.planet_positions(datetime.now(timezone.utc))
                gochar_pos = {name: PlanetState(name=name, longitude=p.longitude, speed=p.speed) for name, p in pos_now.items()}
            
            g_table = []
            for p_name in ["Jupiter", "Saturn", "Rahu", "Ketu", "Mars", "Sun", "Mercury", "Venus", "Moon"]:
                if p_name in gochar_pos:
                    gp = gochar_pos[p_name]
                    g_house = (gp.sign_index - asc_sign_idx + 12) % 12 + 1
                    g_from_moon = (gp.sign_index - chart.planets["Moon"].sign_index + 12) % 12 + 1
                    g_table.append({
                        "ग्रह" if is_hi else "Planet": constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name,
                        "गोचर राशि" if is_hi else "Transit Sign": constants.SIGNS_HI[gp.sign_index] if is_hi else constants.SIGNS[gp.sign_index],
                        "लग्न से भाव" if is_hi else "House from Lagna": f"भाव {g_house}",
                        "चन्द्र से भाव" if is_hi else "House from Moon": f"भाव {g_from_moon}",
                        "स्थिति": "वक्री (R)" if gp.speed < 0 else "मार्गी (Direct)"
                    })
            st.dataframe(pd.DataFrame(g_table), use_container_width=True, hide_index=True)

            st.markdown(f"#### {'फलदीपिका शास्त्रीय गोचर, तारा बल एवं वेध तालिका' if is_hi else 'Phaladeepika Transit, Tara & Vedha'}")
            try:
                transit_rows = vyas_gochar.transits(datetime.now(), 5.5, chart.planets["Moon"].longitude, chart.ascendant_longitude, with_ingress=True)
                t_table = []
                for tr in transit_rows:
                    t_table.append({
                        "ग्रह": constants.PLANETS_HI.get(tr.planet, tr.planet) if is_hi else tr.planet,
                        "गोचर राशि": constants.SIGNS_HI[tr.sign] if is_hi and tr.sign < 12 else tr.sign,
                        "अंश": f"{tr.degree:.2f}°",
                        "नक्षत्र": tr.nakshatra,
                        "तारा बल": tr.tara,
                        "वेध स्थिति": tr.vedha_by or "वेध-मुक्त (अबाधित)",
                        "गोचर प्रभाव": "शुभ फलदायी" if tr.favourable else "सावधानी अपेक्षित",
                        "आगामी राशि परिवर्तन": tr.next_ingress or "-"
                    })
                st.dataframe(pd.DataFrame(t_table), use_container_width=True, hide_index=True)
            except Exception as e:
                st.caption(f"Classical transit table: {e}")


    # =========================================================================
    # SUITE 3: ⚖️ ASHTAKAVARGA, SHADBALA & MAITRI
    # =========================================================================
    elif "अष्टकवर्ग" in selected_suite or "Ashtakavarga" in selected_suite:
        b_tab1, b_tab2, b_tab3 = st.tabs([
            "अष्टकवर्ग चक्र एवं शोधन (SAV & BAV)" if is_hi else "Ashtakavarga Matrix",
            "षड्बल एवं भावबल (Shadbala & Bhavabala)" if is_hi else "Shadbala & Bhavabala",
            "भाव चलित एवं पञ्चधा मैत्री (Chalit & Maitri)" if is_hi else "Chalit & Maitri"
        ])

        p_signs = {n: p.sign_index for n, p in chart.planets.items()}
        av_res = vyas_ashtaka.compute_ashtakavarga(p_signs, asc_sign_idx)

        with b_tab1:
            st.markdown(f'<div class="section-title">{"समुदाय अष्टकवर्ग (SAV: 337 बिंदु) एवं शोधन" if is_hi else "Samudaya Ashtakavarga"}</div>', unsafe_allow_html=True)
            sav_pred = forensic_predictor.compute_ashtakavarga_predictions(av_res["sav"], asc_sign_idx)
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-weight: bold; color: #f0c05a; font-size: 1.1rem;">अष्टकवर्ग शास्त्रीय निष्कर्ष:</div>
                <p style="color: #eedc9a; margin-top: 4px;">{sav_pred['wealth_flow_hi']}</p>
            </div>
            """, unsafe_allow_html=True)

            sav_display = []
            for he in sav_pred["house_evals"]:
                sav_display.append({
                    "भाव": f"भाव {he['house']}",
                    "राशि": he["sign_hi"] if is_hi else constants.SIGNS[(asc_sign_idx + he['house'] - 1) % 12],
                    "SAV बिंदु": he["bindus"],
                    "सामर्थ्य": he["verdict"],
                    "शास्त्रीय फलित": he["analysis_hi"]
                })
            st.dataframe(pd.DataFrame(sav_display), use_container_width=True, hide_index=True)

        with b_tab2:
            st.markdown(f'<div class="section-title">{"षड्बल एवं भावबल विश्लेषण (Six-Fold Planetary Strengths)" if is_hi else "Shadbala Six-Fold Strengths"}</div>', unsafe_allow_html=True)
            shad_res, bhava_res = vyas_shadbala.compute_shadbala(chart, asc_sign_idx)
            shad_table = []
            for p, s in shad_res.items():
                shad_table.append({
                    "ग्रह": constants.PLANETS_HI.get(p, p) if is_hi else p,
                    "स्थान बल": f"{s.sthana_bala:.1f}",
                    "दिग् बल": f"{s.dig_bala:.1f}",
                    "काल बल": f"{s.kala_bala:.1f}",
                    "चेष्टा बल": f"{s.chesta_bala:.1f}",
                    "नैसर्गिक": f"{s.naisargika_bala:.1f}",
                    "दृग् बल": f"{s.drik_bala:.1f}",
                    "कुल विरूप": f"{s.total_virupas:.1f}",
                    "रूप में": f"{s.total_rupas:.2f}",
                    "श्रेणी": f"#{s.rank}",
                    "परिणाम": "प्रबल (बली)" if s.strength_ratio >= 1.0 else "निर्बल (दुर्बल)"
                })
            st.dataframe(pd.DataFrame(shad_table), use_container_width=True, hide_index=True)

        with b_tab3:
            st.markdown(f'<div class="section-title">{"श्रीपति भाव चलित चक्र एवं पञ्चधा मैत्री" if is_hi else "Sripati Chalit Chart & Maitri"}</div>', unsafe_allow_html=True)
            pl_lons = {n: p.longitude for n, p in chart.planets.items()}
            mc_lon = kp_cusps[9].longitude
            chalit_data = vyas_chalit.compute_sripati_chalit(chart.ascendant_longitude, mc_lon, pl_lons)
            
            # Construct Bhava Chalit Houses for Chart SVG
            chalit_houses = {h: [] for h in range(1, 13)}
            for cd in chalit_data:
                # Sign index of Bhava Madhya
                m_sign_idx = int(cd.madhya_deg // 30.0) % 12
                chalit_houses[cd.bhava_num].append(str(m_sign_idx + 1))
                for p in cd.planets_in_bhava:
                    p_obj = chart.planets[p]
                    p_hi_abbr = constants.PLANETS_HI.get(p, p)[:2] if is_hi else p[:2]
                    abbr = f"{p_hi_abbr} {int(p_obj.longitude % 30)}°{int((p_obj.longitude % 1)*60):02d}'"
                    if p_obj.is_retrograde:
                        abbr += " (व)" if is_hi else " (R)"
                    chalit_houses[cd.bhava_num].append(abbr)
                    
            ch_col1, ch_col2 = st.columns([1, 1.2])
            with ch_col1:
                st.markdown(f"<h4 style='text-align: center; color: #f0c05a;'>{'श्रीपति भाव-चलित चक्र' if is_hi else 'Sripati Bhava Chalit Chart'}</h4>", unsafe_allow_html=True)
                svg_chalit = get_north_indian_chart_svg(chalit_houses, size=410, chart_title="श्रीपति भाव चलित चक्र" if is_hi else "Sripati Bhava Chalit")
                render_kundli(svg_chalit)
            with ch_col2:
                st.markdown(f"#### {'📐 भाव आरम्भ, मध्य (संधि) एवं अन्त सारणी' if is_hi else 'Bhava Sandhi & Cuspal Table'}")
                chalit_table = []
                for cd in chalit_data:
                    chalit_table.append({
                        "भाव": f"भाव {cd.bhava_num}",
                        "आरम्भ": f"{constants.SIGNS_HI[constants.SIGNS.index(cd.arambha_sign)] if is_hi and cd.arambha_sign in constants.SIGNS else cd.arambha_sign} {cd.arambha_dms}",
                        "मध्य (शिखर)": f"{constants.SIGNS_HI[constants.SIGNS.index(cd.madhya_sign)] if is_hi and cd.madhya_sign in constants.SIGNS else cd.madhya_sign} {cd.madhya_dms}",
                        "अन्त (संधि)": f"{constants.SIGNS_HI[constants.SIGNS.index(cd.anta_sign)] if is_hi and cd.anta_sign in constants.SIGNS else cd.anta_sign} {cd.anta_dms}",
                        "चलित भावस्थ ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in cd.planets_in_bhava]) if cd.planets_in_bhava else "-"
                    })
                st.dataframe(pd.DataFrame(chalit_table), use_container_width=True, hide_index=True)

            # Panchadha Maitri Matrix
            st.markdown(f"#### {'🤝 सप्तग्रह पञ्चधा मैत्री चक्र (Compound 5-Fold Friendship Matrix)' if is_hi else 'Panchadha Maitri Matrix'}")
            pm_matrix = vyas_chalit.compute_panchadha_maitri(p_signs)
            pm_rows = []
            for p1, rels in pm_matrix.items():
                row = {"ग्रह": constants.PLANETS_HI.get(p1, p1) if is_hi else p1}
                for p2, relation in rels.items():
                    p2_lbl = constants.PLANETS_HI.get(p2, p2) if is_hi else p2
                    row[p2_lbl] = relation
                pm_rows.append(row)
            st.dataframe(pd.DataFrame(pm_rows), use_container_width=True, hide_index=True)

    # =========================================================================
    # SUITE 4: 👑 KP, JAIMINI, NADI & CHAKRAS
    # =========================================================================
    elif "केपी" in selected_suite or "KP" in selected_suite:
        k_tab1, k_tab2, k_tab3, k_tab4, k_tab5 = st.tabs([
            "🎯 केपी सूक्ष्म प्रणाली (KP SSSSSL & Promises)" if is_hi else "KP SSSSSL & Promises",
            "👑 जैमिनी चर कारक (Jaimini Chara Karakas)" if is_hi else "Jaimini Karakas",
            "🧬 भृगु नन्दी नाड़ी (Nadi Combinations)" if is_hi else "Bhrigu Nandi Nadi",
            "☸️ वैदिक चक्र (Sudarshan, SBC, Kota & Navatara)" if is_hi else "Classical Chakras",
            "📜 पंचांग एवं अवकहड़ा (Panchang & Avakhada)" if is_hi else "Panchang & Avakhada"
        ])

        with k_tab1:
            st.markdown(f'<div class="section-title">{"🎯 कृष्णमूर्ति पद्धति (KP System) • SSSSSL गणना, 4-Step कार्येश एवं जीवन प्रॉमिस" if is_hi else "Krishnamurti Paddhati (KP System) Master Engine"}</div>', unsafe_allow_html=True)
            
            # Precompute KP 4-fold significators and planet lords
            kp_sigs = compute_kp_4fold_house_significators(chart.planets, kp_cusps)
            house_significators = kp_sigs["house_significators"]
            planet_significators = kp_sigs["planet_significators"]
            planet_kp_lords = calculate_planet_kp_lords(chart.planets, kp_cusps)
            kp_promises = evaluate_kp_house_promises(kp_cusps, planet_significators, chart.planets)
            dasha_active = evaluate_active_houses_by_dasha(cur_dasha, planet_significators, kp_cusps)

            # --- SUB-SECTION 1: KAB KAUNSA BHAV ACTIVE HO RAHA HAI ---
            st.markdown(f"#### {'⚡ वर्तमान सक्रिय भाव एवं घटना कालक्रम (Active Houses by Dasha)' if is_hi else 'Active Houses by Running Dasha'}")
            
            md_hi = dasha_active['mahadasha_lord_hi']
            ad_hi = dasha_active['antardasha_lord_hi']
            pd_hi = dasha_active['pratyantardasha_lord_hi']
            co_active_str = ", ".join([f"भाव {h}" for h in dasha_active['co_active_houses']]) if dasha_active['co_active_houses'] else "समानुपातिक प्रभाव"
            all_active_str = ", ".join([f"भाव {h}" for h in dasha_active['all_active_houses']])

            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #38bdf8; margin-bottom: 18px;">
                <div style="font-size: 1.15rem; font-weight: bold; color: #38bdf8;">
                    ⏳ वर्तमान सक्रिय दशा चक्र: महादशा [{md_hi}] ➔ अन्तर्दशा [{ad_hi}] ➔ प्रत्यन्तर्दशा [{pd_hi}]
                </div>
                <div style="margin-top: 8px; font-size: 0.98rem; line-height: 1.7; color: #f8fafc;">
                    <b>🔥 अत्यंत तीव्र सक्रिय भाव (MD + AD सह-कार्येश):</b> <span style="color: #4ade80; font-weight: bold; font-size: 1.05rem;">{co_active_str}</span><br>
                    <b>🌐 समस्त सक्रिय भाव स्पेक्ट्रम (Total Active Spectrum):</b> <span style="color: #93c5fd;">{all_active_str}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Render event triggers
            for trg in dasha_active['event_triggers']:
                st.markdown(f"""
                <div class="predict-card" style="border-left-color: #06b6d4; margin-bottom: 8px; padding: 10px 14px;">
                    <div style="font-size: 0.98rem; color: #e2e8f0; line-height: 1.6;">{trg}</div>
                </div>
                """, unsafe_allow_html=True)

            # Active houses breakdown grid
            with st.expander("🔍 सक्रिय भावों का विस्तृत कार्येश प्रभाव (Active Houses Influence Details)"):
                col_act1, col_act2 = st.columns(2)
                for i, ad_item in enumerate(dasha_active['active_details']):
                    target_c = col_act1 if i % 2 == 0 else col_act2
                    with target_c:
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 3px solid {ad_item['color']}; margin-bottom: 8px; padding: 8px 12px;">
                            <b style="color: {ad_item['color']};">भाव {ad_item['house']}: {ad_item['title']}</b> 
                            <span style="font-size: 0.8rem; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; margin-left: 6px;">{ad_item['intensity']}</span>
                            <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">{ad_item['meaning']}</div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 25px 0;'>", unsafe_allow_html=True)

            # --- SUB-SECTION 2: KIS BAAT KA KYA PROMISE HAI KUNDLI MEIN ---
            st.markdown(f"#### {'🏆 कुण्डली में किस बात का प्रॉमिस है और क्या नहीं (KP Life Promises Verification)' if is_hi else 'KP Life Promises Verification'}")
            st.markdown("""
            <p style="font-size: 0.95rem; color: #cbd5e1; margin-bottom: 15px;">
                कृष्णमूर्ति पद्धति का अकाट्य नियम: किसी भी जीवन प्रसंग की सिद्धि या निषेध उस भाव के <b>कस्प उप-स्वामी (Cusp Sub-Lord)</b> तथा उसके <b>नक्षत्र स्वामी</b> द्वारा सिग्निफाई किए जाने वाले भावों पर निर्भर करती है।
            </p>
            """, unsafe_allow_html=True)

            col_p1, col_p2 = st.columns(2)
            for i, p_item in enumerate(kp_promises):
                t_col = col_p1 if i % 2 == 0 else col_p2
                with t_col:
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 4px solid {p_item['status_color']}; margin-bottom: 14px; min-height: 220px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: bold; font-size: 1.05rem; color: #f8fafc;">{p_item['icon']} {p_item['title_hi']}</span>
                            <span style="background: {p_item['status_color']}22; color: {p_item['status_color']}; border: 1px solid {p_item['status_color']}; font-size: 0.82rem; font-weight: bold; padding: 2px 8px; border-radius: 4px;">
                                {p_item['status_hi']}
                            </span>
                        </div>
                        <div style="font-size: 0.88rem; color: #eedc9a; margin-bottom: 6px;">
                            प्राथमिक कस्प: <b>भाव {p_item['primary_cusp']}</b> | उप-स्वामी (SL): <b>{p_item['sub_lord_hi']}</b> (नक्षत्र स्वामी: <b>{p_item['star_lord_hi']}</b>)
                        </div>
                        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 8px;">
                            अनुकूल भाव: <b style="color: #4ade80;">{p_item['favorable_houses']}</b> (सक्रिय: {p_item['favorable_active'] or 'कोई नहीं'}) | 
                            विरोधी भाव: <b style="color: #f87171;">{p_item['detrimental_houses']}</b> (सक्रिय: {p_item['detrimental_active'] or 'कोई नहीं'})
                        </div>
                        <p style="font-size: 0.95rem; line-height: 1.6; color: #f1f5f9; text-align: justify; margin: 0;">
                            {p_item['verdict_text']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 25px 0;'>", unsafe_allow_html=True)

            # --- SUB-SECTION 3: KP PLACIDUS 12 CUSPS TABLE (DOWN TO SSSSSL) ---
            st.markdown(f"#### {'📐 केपी 12 भाव कस्प स्पष्ट तालिका (Placidus Cusps down to SSSSSL)' if is_hi else 'KP Placidus Cusps (down to SSSSSL)'}")
            kp_table = []
            for c in kp_cusps:
                kp_table.append({
                    "भाव कस्प": f"भाव {c.cusp_num}",
                    "स्पष्ट अंश": c.dms_str,
                    "राशि": constants.SIGNS_HI[c.sign_index] if is_hi else c.sign_name,
                    "राशि स्वामी (RL)": constants.PLANETS_HI.get(c.sign_lord, c.sign_lord) if is_hi else c.sign_lord,
                    "नक्षत्र स्वामी (NL)": constants.PLANETS_HI.get(c.star_lord, c.star_lord) if is_hi else c.star_lord,
                    "उप-स्वामी (SL)": constants.PLANETS_HI.get(c.sub_lord, c.sub_lord) if is_hi else c.sub_lord,
                    "SSL": constants.PLANETS_HI.get(c.sub_sub_lord, c.sub_sub_lord) if is_hi else c.sub_sub_lord,
                    "SSSL": constants.PLANETS_HI.get(c.sub_sub_sub_lord, c.sub_sub_sub_lord) if is_hi else c.sub_sub_sub_lord,
                    "SSSSL": constants.PLANETS_HI.get(c.sub_sub_sub_sub_lord, c.sub_sub_sub_sub_lord) if is_hi else c.sub_sub_sub_sub_lord,
                    "SSSSSL": constants.PLANETS_HI.get(c.sub_sub_sub_sub_sub_lord, c.sub_sub_sub_sub_sub_lord) if is_hi else c.sub_sub_sub_sub_sub_lord
                })
            st.dataframe(pd.DataFrame(kp_table), use_container_width=True, hide_index=True)

            # --- SUB-SECTION 4: 9 PLANETARY KP TABLE (DOWN TO SSSSSL) ---
            st.markdown(f"#### {'🪐 नवग्रह केपी स्पष्ट एवं SSSSSL तालिका (Planetary KP Table down to SSSSSL)' if is_hi else 'Planetary KP Table (down to SSSSSL)'}")
            kp_pl_table = []
            for pl in planet_kp_lords:
                kp_pl_table.append({
                    "ग्रह": pl.planet_hi if is_hi else pl.planet,
                    "स्पष्ट अंश": pl.dms_str,
                    "राशि": constants.SIGNS_HI[pl.sign_index] if is_hi else pl.sign_name,
                    "चलित भाव": f"भाव {pl.house_occupied}",
                    "राशि स्वामी (RL)": constants.PLANETS_HI.get(pl.sign_lord, pl.sign_lord) if is_hi else pl.sign_lord,
                    "नक्षत्र स्वामी (NL)": constants.PLANETS_HI.get(pl.star_lord, pl.star_lord) if is_hi else pl.star_lord,
                    "उप-स्वामी (SL)": constants.PLANETS_HI.get(pl.sub_lord, pl.sub_lord) if is_hi else pl.sub_lord,
                    "SSL": constants.PLANETS_HI.get(pl.sub_sub_lord, pl.sub_sub_lord) if is_hi else pl.sub_sub_lord,
                    "SSSL": constants.PLANETS_HI.get(pl.sub_sub_sub_lord, pl.sub_sub_sub_lord) if is_hi else pl.sub_sub_sub_lord,
                    "SSSSL": constants.PLANETS_HI.get(pl.sub_sub_sub_sub_lord, pl.sub_sub_sub_sub_lord) if is_hi else pl.sub_sub_sub_sub_lord,
                    "SSSSSL": constants.PLANETS_HI.get(pl.sub_sub_sub_sub_sub_lord, pl.sub_sub_sub_sub_sub_lord) if is_hi else pl.sub_sub_sub_sub_sub_lord
                })
            st.dataframe(pd.DataFrame(kp_pl_table), use_container_width=True, hide_index=True)

            # --- SUB-SECTION 5: 4-FOLD SIGNIFICATORS (चतुर्विध कार्येश) ---
            st.markdown(f"#### {'📊 केपी 4-Step कार्येश तालिका (KP 4-Fold Significators Matrix)' if is_hi else 'KP 4-Fold Significators Matrix'}")
            
            sig_tab_p, sig_tab_h = st.tabs([
                "ग्रह अनुसार कार्येश (Planet-wise Significators)" if is_hi else "Planet-wise Significators",
                "भाव अनुसार कार्येश (House-wise Significators)" if is_hi else "House-wise Significators"
            ])
            
            with sig_tab_p:
                pl_sig_rows = []
                for p_name in constants.PLANETS:
                    if p_name in planet_significators:
                        s_info = planet_significators[p_name]
                        pl_sig_rows.append({
                            "ग्रह": constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name,
                            "स्थित भाव": f"भाव {s_info.get('house_occupied', '-')}",
                            "नक्षत्र स्वामी": constants.PLANETS_HI.get(s_info.get('star_lord', ''), s_info.get('star_lord', '')) if is_hi else s_info.get('star_lord', ''),
                            "कक्षा A (Star of Occ.)": ", ".join([f"भाव {h}" for h in s_info.get('lvl_A', [])]) or "-",
                            "कक्षा B (Occ. House)": ", ".join([f"भाव {h}" for h in s_info.get('lvl_B', [])]) or "-",
                            "कक्षा C (Star of Lord)": ", ".join([f"भाव {h}" for h in s_info.get('lvl_C', [])]) or "-",
                            "कक्षा D (Lord of House)": ", ".join([f"भाव {h}" for h in s_info.get('lvl_D', [])]) or "-",
                            "समस्त कार्येश भाव": ", ".join([f"भाव {h}" for h in s_info.get('all_signified', [])]) or "-"
                        })
                st.dataframe(pd.DataFrame(pl_sig_rows), use_container_width=True, hide_index=True)

            with sig_tab_h:
                h_sig_rows = []
                for h in range(1, 13):
                    hs = house_significators[h]
                    h_sig_rows.append({
                        "भाव": f"भाव {h}",
                        "भाव स्वामी": constants.PLANETS_HI.get(hs['house_lord'], hs['house_lord']) if is_hi else hs['house_lord'],
                        "भावस्थ ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['occupants']]) or "-",
                        "कक्षा A ग्रह (परम बलवान)": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['level_a']]) or "-",
                        "कक्षा B ग्रह (बलवान)": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['level_b']]) or "-",
                        "कक्षा C ग्रह (मध्यम)": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['level_c']]) or "-",
                        "कक्षा D ग्रह (सामान्य)": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['level_d']]) or "-",
                        "समस्त कार्येश ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['all_significators']]) or "-"
                    })
                st.dataframe(pd.DataFrame(h_sig_rows), use_container_width=True, hide_index=True)

            # KP Predictions & Dasha Event Timing Synthesis
            kp_preds = forensic_predictor.compute_kp_predictions_and_dasha_phala(chart, kp_cusps, cur_dasha)
            st.markdown(f"#### {'केपी कस्प उप-स्वामी सूक्ष्म फलकथन (Cusp Sub-Lord Predictions)' if is_hi else 'KP Cusp Sub-Lord Predictions'}")
            col_k1, col_k2 = st.columns(2)
            for i, ce in enumerate(kp_preds['cusp_evaluations']):
                target_col = col_k1 if i % 2 == 0 else col_k2
                with target_col:
                    with st.expander(f"📍 {ce['title_hi']} [SL: {ce['sub_lord_hi']}]", expanded=(ce['cusp_num'] in [1, 2, 10])):
                        st.markdown(f"""
                        <div style="font-size: 0.85rem; color: #eedc9a; margin-bottom: 4px;">
                            राशि स्वामी: <b>{ce['sign_lord_hi']}</b> | नक्षत्र स्वामी: <b>{ce['star_lord_hi']}</b> | उप-स्वामी: <b>{ce['sub_lord_hi']}</b>
                        </div>
                        <p style="font-size: 0.98rem; line-height: 1.6; color: #f8fafc;">
                            {ce['prediction_hi']}
                        </p>
                        """, unsafe_allow_html=True)

        with k_tab2:
            st.markdown(f'<div class="section-title">{"जैमिनी सप्त चर कारक एवं आत्मकारक" if is_hi else "Jaimini Chara Karakas"}</div>', unsafe_allow_html=True)
            j_karakas, ak_p, km_sign = vyas_jaimini.compute_chara_karakas(chart.planets)
            jk_table = []
            for k in j_karakas:
                jk_table.append({
                    "चर कारक": f"{k.karaka_name} ({k.abbreviation})",
                    "ग्रह": constants.PLANETS_HI.get(k.planet, k.planet) if is_hi else k.planet,
                    "राशि में अंश": k.dms_str,
                    "राशि": constants.SIGNS_HI[constants.SIGNS.index(k.sign_name)] if is_hi and k.sign_name in constants.SIGNS else k.sign_name,
                    "शास्त्रीय कारकत्व": k.signification
                })
            st.dataframe(pd.DataFrame(jk_table), use_container_width=True, hide_index=True)

            # Jaimini Predictions & Chara Dasha Phala Synthesis
            chara_dashas = forensic_predictor.compute_chara_dasha(chart.ascendant_sign, birth['local'], chart)
            j_preds = forensic_predictor.compute_jaimini_predictions_and_chara_dasha_phala(chart, j_karakas, ak_p, chara_dashas, birth['local'])

            st.markdown(f"""
            <div class="predict-card" style="border-left-color: #f0c05a; margin-top: 15px;">
                <div class="predict-header" style="color: #f0c05a; font-size: 1.15rem;">
                    👑 आत्मकारक (AK) एवं अमात्यकारक (AmK) जैमिनी राजयोग
                </div>
                <p style="font-size: 1.02rem; line-height: 1.7; color: #f8fafc; margin-top: 8px;">
                    {j_preds['ak_synthesis_hi']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            cd_info = j_preds['active_chara_dasha']
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #a855f7; margin-top: 12px; margin-bottom: 15px;">
                <div style="font-weight: bold; color: #c084fc; font-size: 1.1rem;">
                    🔮 वर्तमान सक्रिय चर महादशा फलित: {cd_info['sign_hi']} राशि ({cd_info['start']} से {cd_info['end']})
                </div>
                <p style="font-size: 1.02rem; line-height: 1.7; color: #e2e8f0; margin-top: 6px;">
                    {cd_info['prediction_hi']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"#### {'जैमिनी चर महादशा कालक्रम चक्र' if is_hi else 'Jaimini Chara Dasha Trajectory'}")
            cd_table = []
            for cd in chara_dashas:
                cd_table.append({
                    "राशि": cd.get("sign_hi", cd.get("sign", "")),
                    "अवधि": f"{cd.get('years', 0)} वर्ष",
                    "आरम्भ तिथि": cd.get("start", ""),
                    "समाप्ति तिथि": cd.get("end", "")
                })
            st.dataframe(pd.DataFrame(cd_table), use_container_width=True, hide_index=True)

        with k_tab3:
            st.markdown(f'<div class="section-title">{"भृगु नन्दी नाड़ी: गहन जीवन फलादेश एवं ग्रह संयोजन" if is_hi else "Bhrigu Nandi Nadi"}</div>', unsafe_allow_html=True)
            
            # BNN Deep 4-Pillar Life Predictions
            bnn_life = forensic_predictor.compute_bnn_detailed_life_predictions(chart)
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; margin-top: 15px; margin-bottom: 20px;">
                <div class="glass-card" style="border-left: 4px solid #eab308;">
                    <div style="font-weight: bold; color: #facc15; font-size: 1.05rem;">🧬 जीव कारक (Jeeva Karaka - देवगुरु)</div>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc; margin-top: 6px;">{bnn_life['jeeva_karaka_hi']}</p>
                </div>
                <div class="glass-card" style="border-left: 4px solid #3b82f6;">
                    <div style="font-weight: bold; color: #60a5fa; font-size: 1.05rem;">⚖️ कर्म कारक (Karma Karaka - शनिदेव)</div>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc; margin-top: 6px;">{bnn_life['karma_karaka_hi']}</p>
                </div>
                <div class="glass-card" style="border-left: 4px solid #10b981;">
                    <div style="font-weight: bold; color: #34d399; font-size: 1.05rem;">🔮 बुद्धि एवं गूढ़ विद्या कारक (Mercury-Ketu)</div>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc; margin-top: 6px;">{bnn_life['occult_mercury_hi']}</p>
                </div>
                <div class="glass-card" style="border-left: 4px solid #ec4899;">
                    <div style="font-weight: bold; color: #f472b6; font-size: 1.05rem;">🧭 नाड़ी दिशा संयोजन (Directional Trines)</div>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc; margin-top: 6px;">{bnn_life['directional_trines_hi']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"#### {'पारस्परिक नाड़ी ग्रह संयोजन (Nadi Planetary Conjunctions)' if is_hi else 'Nadi Conjunctions'}")
            if hasattr(vyas_nadi, 'analyze_nadi_combinations'):
                nadi_res = vyas_nadi.analyze_nadi_combinations(chart.planets)
            elif hasattr(vyas_nadi, 'analyze_bhrigu_nandi_nadi'):
                res = vyas_nadi.analyze_bhrigu_nandi_nadi({p: st.sign for p, st in chart.planets.items()})
                combs = [{"name": c.title, "result": f"<b>{c.relationship}</b> ({c.auspiciousness})<br>{c.life_impact}"} for c in res.get("nadi_combinations", [])]
                nadi_res = {"combinations": combs}
            else:
                nadi_res = {"combinations": []}
            for comb in nadi_res.get("combinations", [])[:6]:
                st.markdown(f"""
                <div class="predict-card">
                    <div class="predict-header">⚡ नाड़ी संयोजन: {comb.get('name', 'ग्रह युति')}</div>
                    <p>{comb.get('result', 'नाड़ी प्रभाव')}</p>
                </div>
                """, unsafe_allow_html=True)


        with k_tab4:
            st.markdown(f'<div class="section-title">{"☸️ वैदिक चक्र अनुसंधान: सुदर्शन चक्र, कोटा, सर्वतोभद्र एवं 27 नवतारा" if is_hi else "Classical Vedic Chakras Engine"}</div>', unsafe_allow_html=True)
            
            pl_lons = {n: p.longitude for n, p in chart.planets.items()}
            sudarshan_analysis = vyas_chakras.compute_sudarshan_chakra(chart)
            sbc_points = vyas_chakras.compute_sbc_special_points(chart.planets['Moon'].longitude, pl_lons)
            kota_res = vyas_chakras.compute_kota_chakra(chart.planets['Moon'].longitude, chart.ascendant_longitude, pl_lons)
            navatara_items = vyas_chakras.compute_navatara_chakra(chart.planets['Moon'].longitude, pl_lons)

            ch_sub1, ch_sub2, ch_sub3, ch_sub4 = st.tabs([
                "🌟 सुदर्शन चक्र (Sudarshan Tri-Wheel)" if is_hi else "Sudarshan Chakra",
                "🛡️ कोटा चक्र (Kota Fortress Chart)" if is_hi else "Kota Chakra",
                "🔮 सर्वतोभद्र चक्र (Sarvatobhadra Chakra)" if is_hi else "Sarvatobhadra Chakra",
                "✨ 27 नवतारा चक्र (27 Navatara System)" if is_hi else "27 Navatara Chakra"
            ])

            with ch_sub1:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #f59e0b; margin-bottom: 16px;">
                    <div style="font-size: 1.15rem; font-weight: bold; color: #fbbf24;">
                        ☸️ महर्षि पाराशर प्रणीत सुदर्शन चक्र • त्रिविध संगम विश्लेषण
                    </div>
                    <p style="font-size: 0.98rem; line-height: 1.7; color: #f8fafc; margin-top: 8px;">
                        {sudarshan_analysis.sudarshan_verdict_hi}
                    </p>
                    <div style="font-size: 0.88rem; color: #eedc9a; margin-top: 6px;">
                        देह केंद्र (लग्न): <b>{sudarshan_analysis.lagna_sign_hi}</b> | 
                        मन केंद्र (चन्द्र): <b>{sudarshan_analysis.chandra_sign_hi}</b> | 
                        आत्मा केंद्र (सूर्य): <b>{sudarshan_analysis.surya_sign_hi}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                sd_table = []
                for sh in sudarshan_analysis.houses:
                    sd_table.append({
                        "भाव": f"भाव {sh.house_num}",
                        "शास्त्रीय नाम": sh.name_hi.split(" (")[1].replace(")", "") if " (" in sh.name_hi else sh.name_hi,
                        "लग्न से राशि (देह)": f"{sh.lagna_sign_hi} ({', '.join([constants.PLANETS_HI.get(p, p) for p in sh.lagna_planets]) or 'रिक्त'})",
                        "चन्द्र से राशि (मन)": f"{sh.chandra_sign_hi} ({', '.join([constants.PLANETS_HI.get(p, p) for p in sh.chandra_planets]) or 'रिक्त'})",
                        "सूर्य से राशि (आत्मा)": f"{sh.surya_sign_hi} ({', '.join([constants.PLANETS_HI.get(p, p) for p in sh.surya_planets]) or 'रिक्त'})",
                        "त्रिविध प्रभाव स्थिति": sh.status
                    })
                st.dataframe(pd.DataFrame(sd_table), use_container_width=True, hide_index=True)

                with st.expander("📖 सुदर्शन चक्र द्वादश भाव विस्तृत फलादेश"):
                    for sh in sudarshan_analysis.houses:
                        st.markdown(f"""
                        <div style="margin-bottom: 10px; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 6px;">
                            <b style="color: #f0c05a;">{sh.name_hi}:</b> 
                            <span style="color: #cbd5e1; font-size: 0.95rem;">{sh.summary_hi}</span>
                        </div>
                        """, unsafe_allow_html=True)

            with ch_sub2:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid {'#ef4444' if kota_res.is_fort_under_siege else '#22c55e'}; margin-bottom: 16px;">
                    <div style="font-size: 1.15rem; font-weight: bold; color: {'#f87171' if kota_res.is_fort_under_siege else '#4ade80'};">
                        🛡️ कोटा चक्र (दुर्ग सुरक्षा व आक्रमण परीक्षण)
                    </div>
                    <p style="font-size: 0.98rem; line-height: 1.7; color: #f8fafc; margin-top: 8px;">
                        {kota_res.summary}
                    </p>
                    <div style="font-size: 0.88rem; color: #eedc9a; margin-top: 6px;">
                        कोटा स्वामी (दुर्ग अधिपति): <b>{constants.PLANETS_HI.get(kota_res.kota_swami, kota_res.kota_swami)}</b> | 
                        कोटा पाल (दुर्ग रक्षक): <b>{constants.PLANETS_HI.get(kota_res.kota_pala, kota_res.kota_pala)}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                kota_table = []
                for s_name, seg in kota_res.segments.items():
                    kota_table.append({
                        "दुर्ग प्राचीर खंड": seg.segment_name,
                        "समाहित नक्षत्र": ", ".join(seg.nakshatras[:4]) + ("..." if len(seg.nakshatras) > 4 else ""),
                        "उपस्थित ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) for p in seg.planets_present]) if seg.planets_present else "कोई ग्रह नहीं",
                        "सामरिक प्रभाव": seg.nature
                    })
                st.dataframe(pd.DataFrame(kota_table), use_container_width=True, hide_index=True)

            with ch_sub3:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #8b5cf6; margin-bottom: 16px;">
                    <div style="font-size: 1.15rem; font-weight: bold; color: #a78bfa;">
                        🔮 सर्वतोभद्र चक्र (28 नक्षत्र एवं 7 संवेदी मर्म बिंदु)
                    </div>
                    <p style="font-size: 0.95rem; color: #cbd5e1; margin-top: 6px;">
                        सर्वतोभद्र चक्र में अभिजित सहित 28 नक्षत्रों का प्रयोग होता है। जन्म नक्षत्र से 1, 10, 16, 18, 23, 25 एवं 26वें नक्षत्र विशेष संवेदी बिंदु होते हैं जिन पर क्रूर ग्रहों का गोचर अथवा वेध संकटकारक और शुभ ग्रहों का वेध कल्याणकारी होता है।
                    </p>
                </div>
                """, unsafe_allow_html=True)

                sbc_table = []
                for sp in sbc_points:
                    sbc_table.append({
                        "संवेदी मर्म बिंदु": sp.name,
                        "28-नक्षत्र": sp.nakshatra_28,
                        "जन्मनक्षत्र से दूरी": f"{sp.index_from_janma}वाँ नक्षत्र",
                        "कारकत्व एवं प्रभाव क्षेत्र": sp.significance,
                        "वर्तमान गोचरस्थ ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) for p in sp.transiting_planets]) if sp.transiting_planets else "शुद्ध (वेध रहित)"
                    })
                st.dataframe(pd.DataFrame(sbc_table), use_container_width=True, hide_index=True)

            with ch_sub4:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #06b6d4; margin-bottom: 16px;">
                    <div style="font-size: 1.15rem; font-weight: bold; color: #22d3ee;">
                        ✨ 27 नवतारा चक्र (3 पर्य्याय: शारीरिक, कर्मिक एवं पारलौकिक)
                    </div>
                    <p style="font-size: 0.95rem; color: #cbd5e1; margin-top: 6px;">
                        जन्मनक्षत्र से 9 ताराओं का तीन आवृत्तियों में विभाजन: प्रथम पर्य्याय (व्यक्तिगत), द्वितीय पर्य्याय (कर्म व समाज), तृतीय पर्य्याय (आंतरिक व प्रारब्ध)।
                    </p>
                </div>
                """, unsafe_allow_html=True)

                nt_table = []
                for item in navatara_items:
                    nt_table.append({
                        "पर्य्याय": f"पर्य्याय {item.paryaya_num}",
                        "तारा नाम": item.tara_name,
                        "नक्षत्र": item.nakshatra_name,
                        "नक्षत्र स्वामी": constants.PLANETS_HI.get(item.nakshatra_lord, item.nakshatra_lord),
                        "गुणवत्ता": item.quality,
                        "उपस्थित ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) for p in item.planets_present]) if item.planets_present else "-"
                    })
                st.dataframe(pd.DataFrame(nt_table), use_container_width=True, hide_index=True)

        with k_tab5:
            st.markdown(f'<div class="section-title">{"दैनिक पंचांग एवं अवकहड़ा चक्र" if is_hi else "Panchang & Avakhada"}</div>', unsafe_allow_html=True)
            panch_obj = vyas_panchang.compute(birth['local'], birth['lat'], birth['lon'], birth['tz'], chart.ascendant_longitude)
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="font-weight: bold; color: #f0c05a;">पंचांग विवरण:</div>
                    <p>वार: <b>{panch_obj.vara}</b><br>
                    तिथि: <b>{panch_obj.tithi}</b><br>
                    नक्षत्र: <b>{panch_obj.nakshatra} (पद {panch_obj.nakshatra_pada})</b><br>
                    योग: <b>{panch_obj.yoga}</b><br>
                    करण: <b>{panch_obj.karana}</b><br>
                    सूर्योदय: <b>{panch_obj.sunrise}</b> | सूर्यास्त: <b>{panch_obj.sunset}</b></p>
                </div>
                """, unsafe_allow_html=True)
            with col_p2:
                av = panch_obj.avakhada
                st.markdown(f"""
                <div class="glass-card">
                    <div style="font-weight: bold; color: #f0c05a;">अवकहड़ा चक्र:</div>
                    <p>वर्ण: <b>{av.get('Varna', 'Brahmin')}</b><br>
                    वश्य: <b>{av.get('Vashya', 'Keet')}</b><br>
                    योनि: <b>{av.get('Yoni', 'Mrig')}</b><br>
                    गण: <b>{av.get('Gana', 'Deva')}</b><br>
                    नाड़ी: <b>{av.get('Nadi', 'Madhya')}</b><br>
                    नाम अक्षर: <b>{av.get('Naam Akshar', 'न')}</b></p>
                </div>
                """, unsafe_allow_html=True)

    # =========================================================================
    # SUITE 5: 📖 DEEP FORENSIC PREDICTIONS (Extensive Classical Analysis)
    # =========================================================================
    elif "फलित" in selected_suite or "Predictions" in selected_suite:
        p_signs = {n: p.sign_index for n, p in chart.planets.items()}
        av_res = vyas_ashtaka.compute_ashtakavarga(p_signs, asc_sign_idx)
        sav = av_res["sav"]
        dignities = forensic_predictor.analyze_all_planetary_dignities(chart, vargas_matrix)
        bhavas = forensic_predictor.analyze_all_12_bhavas(chart, dignities)
        overall_forecast = forensic_predictor.compute_overall_life_forecast(chart, dignities, bhavas, sav, vargas_matrix)

        p_tab0, p_tab1, p_tab2, p_tab3, p_tab4, p_tab5, p_tab6, p_tab7, p_tab8 = st.tabs([
            "🌟 समग्र जीवन फलादेश (Senior Master Forecast)" if is_hi else "Master Overall Life Forecast",
            "द्वादश भाव विस्तृत फलित (12 Bhavas)" if is_hi else "12 Bhavas In-Depth",
            "🏛️ भावत् भावम् सूक्ष्म विश्लेषण (Bhavat Bhavam)" if is_hi else "Bhavat Bhavam Matrix",
            "ग्रह अवस्था एवं दृष्टि (Dignities & Aspects)" if is_hi else "Dignities & Aspects",
            "मंगल दोष सम्पूर्ण विवेचन (Mangal Dosha)" if is_hi else "Mangal Dosha Analysis",
            "शनि साढ़े साती एवं ढैय्या (Sade Sati Report)" if is_hi else "Sade Sati Report",
            "कालसर्प दोष परीक्षण (Kalsarp Dosha)" if is_hi else "Kalsarp Dosha",
            "लाल किताब फलित एवं उपाय (Lal Kitab & Upay)" if is_hi else "Lal Kitab & Remedies",
            "शास्त्रीय सूत्र डेटाबैंक (Classical Sutras)" if is_hi else "Classical Sutras"
        ])

        with p_tab0:
            st.markdown(f'<div class="section-title">{"🌟 महर्षि पाराशर व कल्याणवर्मा परंपरा: समग्र जीवन महा-फलादेश (13 जीवन अध्याय)" if is_hi else "Comprehensive Classical Life Horoscope Synthesis"}</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="border-left: 4px solid #f0c05a; margin-bottom: 20px;">
                <div style="font-size: 1.15rem; font-weight: bold; color: #f0c05a;">📜 फलित ज्योतिष शोध प्रबन्ध • वरिष्ठ ज्योतिषी दृष्टिकोण</div>
                <p style="color: #e2e8f0; margin-top: 6px; font-size: 0.98rem; line-height: 1.6;">
                    यह फलादेश केवल सतही ग्रह स्थिति नहीं, अपितु बृहत्पाराशर होराशास्त्र, फलदीपिका, सारावली, जातक पारिजात एवं सर्वार्थचिंतामणि के संयुक्त शास्त्रीय नियमों पर आधारित 13 विस्तृत अध्यायों का महा-संश्लेषण है।
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            for ch in overall_forecast:
                ch_num = ch.get('chapter_num', 1)
                ch_title = ch.get('title_hi', ch.get('title', 'जीवन अध्याय'))
                ch_icon = ch.get('icon', '📜')
                with st.expander(f"{ch_icon} अध्याय {ch_num}: {ch_title}", expanded=(ch_num in [1, 4, 5, 8])):
                    st.markdown(f"""
                    <div class="predict-card" style="border-left-color: #ffd97d;">
                        <div class="predict-header" style="font-size: 1.15rem; color: #ffd97d;">{ch_icon} {ch_title}</div>
                        <p style="font-size: 1.05rem; line-height: 1.75; color: #f8fafc; text-align: justify; margin-top: 10px;">
                            {ch.get('content_hi', '')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

        with p_tab1:
            st.markdown(f'<div class="section-title">{"द्वादश भाव गहन ज्योतिषीय फलित (Bhava-by-Bhava Analysis)" if is_hi else "12 Houses Forensic Interpretation"}</div>', unsafe_allow_html=True)
            for bh in bhavas:
                with st.expander(f"🏛️ भाव {bh.bhava_num}: {bh.sign_hi} राशि (स्वामी: {bh.lord_hi}) — [{bh.strength_type}]", expanded=(bh.bhava_num in [1, 7, 10])):
                    st.markdown(f"""
                    <div class="predict-card">
                        <div style="color: #eedc9a; font-weight: bold; margin-bottom: 6px;">
                            भावाधिपति स्थिति: भाव {bh.lord_house} ({bh.lord_sign_hi}) | 
                            भावस्थ ग्रह: {', '.join(bh.occupants_hi) or 'कोई नहीं (रिक्त)'} | 
                            दृष्टि डालने वाले ग्रह: {', '.join(bh.aspecting_planets_hi) or 'कोई नहीं'}
                        </div>
                        <p style="font-size: 1.05rem; line-height: 1.6; color: #f8fafc;">{bh.prediction_hi}</p>
                    </div>
                    """, unsafe_allow_html=True)

        with p_tab2:
            st.markdown(f'<div class="section-title">{"🏛️ भावत् भावम् सूक्ष्म सिद्धांत एवं फलित (Bhavat Bhavam Recursive Matrix)" if is_hi else "Bhavat Bhavam Matrix"}</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="border-left: 4px solid #f0c05a; margin-bottom: 20px;">
                <div style="font-size: 1.15rem; font-weight: bold; color: #f0c05a;">📜 भावत् भावम् सिद्धांत • बृहत्पाराशर होराशास्त्र एवं फलदीपिका</div>
                <p style="color: #e2e8f0; margin-top: 6px; font-size: 0.98rem; line-height: 1.6;">
                    वैदिक ज्योतिष का अमर नियम: किसी भी भाव का सूक्ष्म फल जानने के लिए उस भाव से उतनी ही दूरी वाले भाव (H-from-H) का परीक्षण करना अनिवार्य है।
                    उदा. द्वितीय का द्वितीय = तृतीय भाव (धन की सुरक्षा व पराक्रम), अष्टम का अष्टम = तृतीय भाव (आयु का आधार), दशम का दशम = सप्तम भाव (व्यापार व प्रतिष्ठा)।
                </p>
            </div>
            """, unsafe_allow_html=True)

            bb_data = forensic_predictor.compute_bhavat_bhavam_analysis(chart, dignities, bhavas, sav)
            
            bb_table = []
            for b in bb_data:
                bb_table.append({
                    "सम्बद्ध भाव": f"भाव {b['primary_house']} ➔ भाव {b['secondary_house']}",
                    "शास्त्रीय सूत्र": b["title_hi"],
                    "प्राथमिक स्वामी": f"{b['prim_lord_hi']} ({b['prim_sign_hi']})",
                    "प्राथमिक SAV": b["prim_sav"],
                    "भावत् भावम् स्वामी": f"{b['sec_lord_hi']} ({b['sec_sign_hi']})",
                    "द्वितीयक SAV": b["sec_sav"],
                    "सामर्थ्य निर्णय": b["status_verdict"]
                })
            st.dataframe(pd.DataFrame(bb_table), use_container_width=True, hide_index=True)

            st.markdown("#### भावत् भावम् द्वादश गहन फलकथन:")
            col_bb1, col_bb2 = st.columns(2)
            for idx_bb, b in enumerate(bb_data):
                target_col = col_bb1 if idx_bb % 2 == 0 else col_bb2
                with target_col:
                    with st.expander(f"🏛️ {b['title_hi']} [{b['status_verdict']}]", expanded=(b['primary_house'] in [1, 2, 7, 10])):
                        st.markdown(f"""
                        <div style="font-size: 0.9rem; color: #eedc9a; margin-bottom: 6px;">
                            <b>मूल कारकत्व:</b> {b['karakatwa_hi']}<br>
                            प्राथमिक भाव {b['primary_house']} ({b['prim_sign_hi']} - {b['prim_sav']} SAV) | 
                            द्वितीयक भाव {b['secondary_house']} ({b['sec_sign_hi']} - {b['sec_sav']} SAV)
                        </div>
                        <p style="font-size: 0.98rem; line-height: 1.65; color: #f8fafc; text-align: justify;">
                            {b['verdict_hi']}
                        </p>
                        """, unsafe_allow_html=True)

        with p_tab3:
            st.markdown(f'<div class="section-title">{"ग्रह अवस्था, अस्त/वक्री एवं दृष्टि बल विश्लेषण" if is_hi else "Planetary Dignities & States"}</div>', unsafe_allow_html=True)
            dig_rows = []
            for p_name, dig in dignities.items():
                p_hi = constants.PLANETS_HI.get(p_name, p_name)
                dig_rows.append({
                    "ग्रह": p_hi,
                    "राशि": dig.sign_hi,
                    "भाव": f"भाव {dig.house}",
                    "अवस्था": dig.awastha_hi,
                    "नवमांश (D9)": dig.d9_sign_hi + (" (वर्गोत्तम)" if dig.is_vargottama else ""),
                    "दृष्टि डालने वाले ग्रह": ", ".join([constants.PLANETS_HI.get(x, x) for x in dig.aspects_received_from]) or "-",
                    "शास्त्रीय गरिमा": dig.dignity_summary_hi
                })
            st.dataframe(pd.DataFrame(dig_rows), use_container_width=True, hide_index=True)

        with p_tab4:
            st.markdown(f'<div class="section-title">{"मंगल दोष सम्पूर्ण शास्त्रीय विवेचन एवं परिहार" if is_hi else "Mangal Dosha Assessment"}</div>', unsafe_allow_html=True)
            m_dosha = forensic_predictor.compute_comprehensive_mangal_dosha(chart)
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-size: 1.2rem; font-weight: bold; color: #4ade80;">स्थिति: {m_dosha['severity']}</div>
                <p style="margin-top: 8px; font-size: 1.05rem; line-height: 1.6;">{m_dosha['summary_hi']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("#### सर्वकल्याणकारी मङ्गल शांति उपाय:")
            for r in m_dosha['remedies_hi']:
                st.markdown(f"• {r}")

        with p_tab5:
            st.markdown(f'<div class="section-title">{"शनि साढ़े साती एवं ढैय्या 46-चरणीय जीवन चक्र" if is_hi else "Shani Sade Sati Full Report"}</div>', unsafe_allow_html=True)
            sade_phases = forensic_predictor.compute_comprehensive_sade_sati(birth["local"], chart.planets["Moon"].longitude)
            s_table = []
            for sp in sade_phases:
                s_table.append({
                    "साढ़े साती चरण": sp.phase_name_hi,
                    "शनि राशि": sp.saturn_sign_hi,
                    "आरम्भ दिनांक": sp.start_date,
                    "समाप्ति दिनांक": sp.end_date,
                    "चरण भेद": sp.charan_hi,
                    "विशिष्ट शास्त्रीय प्रभाव": sp.impact_hi
                })
            st.dataframe(pd.DataFrame(s_table), use_container_width=True, hide_index=True)

        with p_tab6:
            st.markdown(f'<div class="section-title">{"कालसर्प दोष 12 भेदों की सूक्ष्म जाँच" if is_hi else "Kalsarp Dosha Analysis"}</div>', unsafe_allow_html=True)
            k_dosha = forensic_predictor.compute_comprehensive_kalsarp(chart)
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-size: 1.2rem; font-weight: bold; color: #4ade80;">निर्णय: {k_dosha['status_hi']}</div>
                <p style="margin-top: 8px; font-size: 1.05rem; line-height: 1.6;">{k_dosha['description_hi']}</p>
            </div>
            """, unsafe_allow_html=True)

        with p_tab7:
            st.markdown(f'<div class="section-title">{"लाल किताब भाव फलकथन एवं अचूक उपाय" if is_hi else "Lal Kitab Predictions & Remedies"}</div>', unsafe_allow_html=True)
            lk_items = forensic_predictor.compute_lal_kitab_predictions_and_upay(chart)
            for item in lk_items:
                with st.expander(f"📕 {item['planet_hi']} (भाव {item['house']} - {item['sign_hi']} राशि)"):
                    st.markdown(f"<p style='font-size: 1.05rem; line-height: 1.6;'>{item['phal_hi']}</p>", unsafe_allow_html=True)
                    st.markdown("<b>लाल किताब अचूक उपाय:</b>", unsafe_allow_html=True)
                    for u in item["upay_hi"]:
                        st.markdown(f"✓ {u}")

        with p_tab8:
            st.markdown(f'<div class="section-title">{"शास्त्रीय सूत्र डेटाबैंक (Laghu Parashari, Phaladeepika, Saravali)" if is_hi else "Classical Sutras Bank"}</div>', unsafe_allow_html=True)
            sutra_eval = vyas_sutra_bank.evaluate_classical_sutras(chart)
            for se in sutra_eval:
                st.markdown(f"""
                <div class="predict-card">
                    <div class="predict-header">📜 {se.name} — <span style="font-size: 0.9rem; color: #a0aec0;">[{se.source}]</span></div>
                    <div style="font-family: 'Tiro Devanagari Sanskrit', serif; color: #ffd97d; font-weight: bold; margin: 4px 0;">{se.shloka_sanskrit}</div>
                    <div style="color: #cbd5e1; font-size: 0.95rem;"><b>सत्यापित स्थिति:</b> {se.condition_description}</div>
                    <div style="color: #4ade80; font-size: 0.95rem; margin-top: 4px;"><b>फलकथन:</b> {se.deterministic_result}</div>
                </div>
                """, unsafe_allow_html=True)

    # =========================================================================
    # SUITE 6: 📄 43+ PAGE PUBLICATION PDF (AstroSage-Class Publication)
    # =========================================================================
    elif "PDF" in selected_suite or "शोध प्रबंध" in selected_suite:
        st.markdown(f'<div class="section-title">{"📄 43+ पेज सम्पूर्ण वैदिक ज्योतिष शोध प्रबंध PDF" if is_hi else "📄 43+ Page Executive Vedic Thesis PDF"}</div>', unsafe_allow_html=True)
        st.info("यह रिपोर्ट एस्ट्रोसेज की 35-पेज प्रीमियम कुण्डली से कहीं अधिक समृद्ध, 43 पृष्ठों के शोध-स्तरीय कलेवर, 100% शुद्ध देवनागरी (Chrome HarfBuzz) और 13 विस्तृत जीवन अध्यायों से युक्त है।")
        
        pdf_out_path = os.path.join(os.path.dirname(__file__), "VYAS_Executive_Publication_Thesis.pdf")
        
        col_gen1, col_gen2 = st.columns([1, 1.2])
        with col_gen1:
            varsh_choice_pdf = st.number_input(
                "वर्षफल वर्ष का चयन (Varshphal Year in PDF):" if is_hi else "Varshphal Year in PDF:",
                min_value=birth['local'].year,
                max_value=birth['local'].year + 100,
                value=2026,
                step=1,
                key="suite6_varsh_year"
            )
            if st.button("🚀 43-पेज सम्पूर्ण शोध प्रबंध PDF तैयार करें (Generate 43-Page Thesis)", type="primary", use_container_width=True):
                with st.spinner("Compiling 43-Page Master Thesis with High-Resolution SVG Charts, 13 Life Chapters & Chrome HarfBuzz Typography..."):
                    success = publication_engine.build_publication_pdf(
                        chart, birth, kp_cusps, dasha_engine, vargas_matrix, pdf_out_path, target_varsh_year=int(varsh_choice_pdf)
                    )
                    if success and os.path.exists(pdf_out_path):
                        st.session_state['pdf_ready'] = True
                        st.success(f"🎉 43-पेज शोध प्रबंध PDF सफलतापूर्वक तैयार हो गया है! (आकार: {os.path.getsize(pdf_out_path)/1024/1024:.2f} MB)")
                    else:
                        st.error("PDF generation encountered an issue. Please verify Chrome headless availability.")

            if os.path.exists(pdf_out_path):
                with open(pdf_out_path, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(
                    label="📥 सम्पूर्ण 43-पेज वैदिक शोध प्रबंध PDF डाउनलोड करें",
                    data=pdf_bytes,
                    file_name=f"VYAS_Thesis_{birth.get('name', 'Native').replace(' ', '_')}_43_Pages.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        with col_gen2:
            st.markdown("""
            <div class="glass-card">
                <div style="font-weight: bold; color: #f0c05a; font-size: 1.1rem;">43-पेज शोध प्रबंध की प्रमुख विशिष्टताएँ:</div>
                <ul style="color: #cbd5e1; font-size: 0.95rem; margin-top: 6px; line-height: 1.6;">
                    <li><b>शुद्ध देवनागरी टंकण:</b> गूगल क्रोम के हार्फबज़ (HarfBuzz) इंजन द्वारा 100% सही मात्राएं, संयुक्ताक्षर व मुद्रण सौंदर्य।</li>
                    <li><b>43 पृष्ठों का अखंड महा-ग्रंथ:</b> अवकहड़ा, घातक, लग्न, नवमांश, षोडशवर्ग (16 चक्र), मंगल दोष, शनि साढ़े साती (46 चक्र), कालसर्प, वर्षफल (वर्ष 2026/चयनित), योगिनी दशा (36 वर्ष चक्र), चर दशा, लाल किताब (9 ग्रह व अचूक उपाय), केपी पद्धति, अष्टकवर्ग व प्रस्तराष्टकवर्ग।</li>
                    <li><b>समग्र जीवन महा-फलादेश (13 विस्तृत अध्याय):</b> व्यक्तित्व, मानसिकता, विद्या, आजीविका, धन, दांपत्य, संतान, भाग्य, स्वास्थ्य, शत्रु निवारण, विदेश योग, मोक्ष (D60 प्रारब्ध), एवं आगामी 5 वर्षों की रणनीतिक योजना।</li>
                    <li><b>शोधकर्ता एवं परामर्शदाता:</b> निखिल व्यास (एम.ए. ज्योतिष - स्नातकोत्तर / M.A. Jyotish) • 9414121172</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
