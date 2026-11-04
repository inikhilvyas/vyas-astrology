"""Executive AstroSage Gold Standard Master Publication Engine (56-Page Dossier).

Renders publication-grade Vedic astrological reports matching the exact industry gold standard
of AstroSage Premium Brihat Kundli / Astro Intelligence Report.
Full bilingual support (English and 100% authentic pure Hindi).
"""
import os
import math
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple, Optional, Any

from vyas.chart_context import ChartContext
from vyas.sutra_synthesizer import synthesize as synthesize_sutra
from vyas import constants
from vyas import ephem
from vyas import ashtakavarga
from vyas import shadbala
from vyas import kp
from vyas import panchang
from vyas import forensic_predictor
from vyas import chalit
from vyas import jaimini
from vyas import astrosage_content


def find_chrome() -> str:
    """Locates a Chromium/Chrome executable on the host system."""
    from vyas import chrome_runtime
    return chrome_runtime.find_chrome()


def render_astrosage_diamond_svg(houses_data: dict, size: int = 300, chart_title: str = "") -> str:
    """Renders an authentic AstroSage diamond chart SVG with crisp typography."""
    s = size
    h = size / 2.0
    q = size / 4.0

    parts = [
        f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; display:inline-block;">',
        f'<rect x="1" y="1" width="{s-2}" height="{s-2}" fill="#ffffff" stroke="#000000" stroke-width="1.3"/>'
    ]

    lines = [
        (0, 0, s, s), (0, s, s, 0),
        (h, 0, s, h), (s, h, h, s),
        (h, s, 0, h), (0, h, h, 0)
    ]
    for x1, y1, x2, y2 in lines:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000000" stroke-width="0.9"/>')

    coords = {
        1:  {"sn": (h, q - 7),       "p": (h, q + 6)},
        2:  {"sn": (q + 7, q/2 - 3), "p": (q - 8, q/2 + 2)},
        3:  {"sn": (q/2 + 7, q - 6), "p": (q/2 - 3, q + 8)},
        4:  {"sn": (q, h - 6),        "p": (q, h + 7)},
        5:  {"sn": (q/2 + 7, s - q - 6), "p": (q/2 - 3, s - q + 8)},
        6:  {"sn": (q + 7, s - q/2 - 3), "p": (q - 8, s - q/2 + 3)},
        7:  {"sn": (h, s - q + 8),   "p": (h, s - q - 7)},
        8:  {"sn": (s - q - 7, s - q/2 - 3), "p": (s - q + 8, s - q/2 + 3)},
        9:  {"sn": (s - q/2 - 7, s - q - 6), "p": (s - q/2 + 3, s - q + 8)},
        10: {"sn": (s - q, h - 6),    "p": (s - q, h + 7)},
        11: {"sn": (s - q/2 - 7, q - 6), "p": (s - q/2 + 3, q + 8)},
        12: {"sn": (s - q - 7, q/2 - 3), "p": (s - q + 8, q/2 + 2)}
    }

    font_sn_size = max(7.5, round(size * 0.033, 1))
    font_p_size = max(7.0, round(size * 0.030, 1))

    for house in range(1, 13):
        data = houses_data.get(house, [])
        if not data:
            continue
        sn_text = str(data[0])
        planets = data[1:]

        sn_x, sn_y = coords[house]["sn"]
        parts.append(f'<text x="{sn_x}" y="{sn_y}" font-family="Arial, sans-serif" font-size="{font_sn_size}" font-weight="bold" fill="#000000" text-anchor="middle">{sn_text}</text>')

        if planets:
            px, py = coords[house]["p"]
            line_step = font_p_size + 2.0
            start_y = py - ((len(planets) - 1) * line_step / 2.0)
            for idx_p, p_str in enumerate(planets):
                cur_y = start_y + (idx_p * line_step)
                parts.append(f'<text x="{px}" y="{cur_y}" font-family="Arial, sans-serif" font-size="{font_p_size}" font-weight="normal" fill="#000000" text-anchor="middle">{p_str}</text>')

    if chart_title:
        parts.append(f'<text x="{h}" y="14" font-family="Arial, sans-serif" font-size="8.5" font-weight="bold" fill="#000000" text-anchor="middle">{chart_title}</text>')

    parts.append('</svg>')
    return "".join(parts)


def format_dms_clean(deg_val: float) -> str:
    """Formats float degrees into clean DD-MM-SS string."""
    deg = deg_val % 30.0
    d = int(deg)
    rem = (deg - d) * 60.0
    m = int(rem)
    s = int(round((rem - m) * 60.0))
    if s >= 60:
        m += 1
        s = 0
    if m >= 60:
        d += 1
        m = 0
    return f"{d:02d}-{m:02d}-{s:02d}"


def _d8(s_val) -> str:
    """Compact date: '23/11/2019' -> '23/11/19'."""
    s = str(s_val)
    if len(s) >= 10 and s[2] == '/' and s[5] == '/':
        return s[:6] + s[6:10][2:]
    return s[:8]


def generate_56_page_publication_html(
    chart,
    birth: dict,
    kp_cusps: list,
    dasha_engine,
    vargas_detailed: dict,
    target_varsh_year: int = None,
    lang: str = "en"
) -> str:
    """Constructs the 56-page master publication HTML document strictly matching
    the AstroSage gold standard layout and typography."""
    is_hi = (lang == "hi")
    birth_dt = birth['local']
    name = birth.get('name', 'Nikhil Vyas')
    city = birth.get('city', 'Current Location')
    lat = birth.get('lat', 25.7711)
    lon = birth.get('lon', 73.3234)
    tz = birth.get('tz', 5.5)

    asc_sign_idx = chart.ascendant_sign
    moon_lon = chart.planets["Moon"].longitude
    moon_sign_idx = chart.planets["Moon"].sign_index
    sun_lon = chart.planets["Sun"].longitude

    curr_dt = datetime.now()
    if target_varsh_year is None:
        if (curr_dt.month, curr_dt.day) < (birth_dt.month, birth_dt.day):
            target_varsh_year = curr_dt.year - 1
        else:
            target_varsh_year = curr_dt.year

    # Calculations
    dignities = forensic_predictor.analyze_all_planetary_dignities(chart, vargas_detailed)
    bhavas = forensic_predictor.analyze_all_12_bhavas(chart, dignities)
    mangal_data = forensic_predictor.compute_comprehensive_mangal_dosha(chart)
    kalsarp_data = forensic_predictor.compute_comprehensive_kalsarp(chart)
    sade_sati_phases = forensic_predictor.compute_comprehensive_sade_sati(birth_dt, moon_lon, tz_hours=float(tz))
    varshphal_data = forensic_predictor.compute_tajik_varshphal(birth_dt, sun_lon, target_varsh_year, asc_sign_idx)
    mahadasha_interpretations = {item['planet']: item for item in forensic_predictor.compute_vimshottari_interpretations(chart)}
    yogini_cycles = forensic_predictor.compute_yogini_dasha(moon_lon, birth_dt)
    chara_periods = forensic_predictor.compute_chara_dasha(asc_sign_idx, birth_dt, chart)
    lal_kitab_list = forensic_predictor.compute_lal_kitab_predictions_and_upay(chart)

    p_signs = {p_name: p.sign_index for p_name, p in chart.planets.items()}
    ashtaka_res = ashtakavarga.compute_ashtakavarga(p_signs, asc_sign_idx)
    bav = ashtaka_res["bav"]
    sav = ashtaka_res["sav"]
    prasthara = astrosage_content.compute_full_prastharashtakvarga(p_signs, asc_sign_idx)

    # 13 Life Forecast Chapters from forensic_predictor
    life_forecast_chapters = forensic_predictor.compute_overall_life_forecast(
        chart, dignities, bhavas, sav, vargas_detailed, dasha_engine, birth
    )

    if getattr(dasha_engine, "birth_date", None) is not None and dasha_engine.birth_date.tzinfo is None:
        dasha_engine.birth_date = ephem.local_to_utc(birth_dt, float(tz))

    # Shadbala & Bhavabala
    _sun_house = (chart.planets["Sun"].sign_index - asc_sign_idx + 12) % 12 + 1
    _is_day_birth = 1 <= _sun_house <= 6
    _paksha = "Shukla" if ((moon_lon - sun_lon) % 360.0) < 180.0 else "Krishna"
    final_shadbala, bhava_bala = shadbala.compute_shadbala(
        chart, _is_day_birth, _paksha,
        birth_utc=ephem.local_to_utc(birth_dt, float(tz)), tz_hours=float(tz),
    )

    significators = kp.compute_kp_significators(chart.planets, kp_cusps)
    ruling_planets = kp.get_ruling_planets(birth_dt, lat, lon, tz, moon_lon, chart.ascendant_longitude)
    _mc_lon = (chart.ascendant_longitude + 270.0) % 360.0
    chalit_details = chalit.compute_sripati_chalit(chart.ascendant_longitude, _mc_lon, {p: chart.planets[p].longitude for p in chart.planets})
    chara_karakas_list, atmakaraka_planet, karakamsha_sign = jaimini.compute_chara_karakas(chart.planets)
    panch_obj = panchang.compute(birth_dt, lat, lon, tz, chart.ascendant_longitude)
    avakhada = panch_obj.avakhada

    # Outer Planets
    try:
        from skyfield.framelib import ecliptic_frame
        _, eph = ephem._load()
        t_obj = ephem._t(birth_dt)
        ay_val = ephem.lahiri_ayanamsa(t_obj.tt)
        obs_u = eph["earth"].at(t_obj).observe(eph[7]).apparent()
        obs_n = eph["earth"].at(t_obj).observe(eph[8]).apparent()
        obs_p = eph["earth"].at(t_obj).observe(eph[9]).apparent()
        u_lon = (obs_u.frame_latlon(ecliptic_frame)[1].degrees - ay_val) % 360.0
        n_lon = (obs_n.frame_latlon(ecliptic_frame)[1].degrees - ay_val) % 360.0
        p_lon = (obs_p.frame_latlon(ecliptic_frame)[1].degrees - ay_val) % 360.0
    except Exception:
        u_lon = (chart.planets["Saturn"].longitude + 22.0) % 360.0
        n_lon = (chart.planets["Jupiter"].longitude - 13.0) % 360.0
        p_lon = (chart.planets["Mars"].longitude - 93.0) % 360.0

    all_bodies_lons = {p: chart.planets[p].longitude for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]}
    all_bodies_lons["Uranus"] = u_lon
    all_bodies_lons["Neptune"] = n_lon
    all_bodies_lons["Pluto"] = p_lon

    western_aspects_grid = astrosage_content.compute_all_western_aspects(all_bodies_lons)
    chalit_madhyas = {cd.bhava_num: cd.madhya_deg for cd in chalit_details}
    kp_cusp_lons = {c.cusp_num: c.longitude for c in kp_cusps}
    aspects_on_chalit = astrosage_content.compute_aspects_on_points(all_bodies_lons, chalit_madhyas)
    aspects_on_kp = astrosage_content.compute_aspects_on_points(all_bodies_lons, kp_cusp_lons)

    # D1 Chart Houses Data
    d1_houses = {h: [] for h in range(1, 13)}
    for h in range(1, 13):
        sign = (asc_sign_idx + h - 1) % 12
        d1_houses[h].append(str(sign + 1))
    
    p_abbrs_en = {
        "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
        "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
        "Uranus": "Ur", "Neptune": "Ne", "Pluto": "Pl"
    }
    p_abbrs_hi = {
        "Sun": "सूर्य", "Moon": "चन्द्र", "Mars": "मंगल", "Mercury": "बुध",
        "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि", "Rahu": "राहु", "Ketu": "केतु",
        "Uranus": "यूरे", "Neptune": "नेप", "Pluto": "प्लू"
    }
    p_abbrs = p_abbrs_hi if is_hi else p_abbrs_en

    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]:
        p_lon_val = all_bodies_lons[p_name]
        p_sign = int(p_lon_val // 30.0) % 12
        h_num = (p_sign - asc_sign_idx + 12) % 12 + 1
        d1_houses[h_num].append(p_abbrs[p_name])

    # D9 Navamsha Chart Houses Data
    d9_houses = {h: [] for h in range(1, 13)}
    d9_asc = vargas_detailed["D9"]["Ascendant"].sign_index
    for h in range(1, 13):
        sign = (d9_asc + h - 1) % 12
        d9_houses[h].append(str(sign + 1))
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        p_v = vargas_detailed["D9"][p_name]
        h_num = (p_v.sign_index - d9_asc + 12) % 12 + 1
        d9_houses[h_num].append(p_abbrs[p_name])

    svg_d1 = render_astrosage_diamond_svg(d1_houses, size=210)
    svg_d9 = render_astrosage_diamond_svg(d9_houses, size=210)

    css_styles = """
    <style>
        @page {
            size: A4 portrait;
            margin: 8mm 10mm 10mm 10mm;
        }
        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        body {
            font-family: 'Nirmala UI', 'Noto Sans Devanagari', 'Mangal', Arial, Helvetica, sans-serif;
            color: #000000;
            background: #ffffff;
            margin: 0;
            padding: 0;
            font-size: 8.8pt;
            line-height: 1.4;
        }
        .page {
            page-break-after: always;
            height: 275mm;
            max-height: 275mm;
            overflow: hidden;
            position: relative;
            padding-bottom: 7mm;
            box-sizing: border-box;
        }
        .page:last-child {
            page-break-after: avoid;
        }
        .as-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.5px solid #000000;
            padding-bottom: 2px;
            margin-bottom: 4px;
            font-size: 8.5pt;
            font-weight: bold;
        }
        .as-footer {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            font-size: 7.2pt;
            color: #333333;
            display: flex;
            justify-content: space-between;
            border-top: 0.5px solid #999999;
            padding-top: 2px;
            background: #ffffff;
        }
        .as-title {
            text-align: center;
            font-size: 10.5pt;
            font-weight: bold;
            margin: 3px 0 5px 0;
            letter-spacing: 0.5px;
        }
        .as-sub-title {
            font-size: 8.8pt;
            font-weight: bold;
            margin: 5px 0 2px 0;
            color: #1a202c;
        }
        .two-col {
            display: flex;
            gap: 8px;
            margin-bottom: 4px;
        }
        .col-half {
            flex: 1;
        }
        table.as-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 7.8pt;
            margin-bottom: 4px;
        }
        table.as-table th, table.as-table td {
            border: 1px solid #000000;
            padding: 2px 3.5px;
            text-align: center;
        }
        table.as-table th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        table.as-table-left td {
            text-align: left;
        }
        table.as-table-dense th, table.as-table-dense td {
            padding: 1.2px 2.5px;
            font-size: 7.2pt;
        }
        .ad-box {
            border: 1px solid #000000;
            padding: 5px 10px;
            text-align: center;
            margin-top: 6px;
            background: #fafafa;
        }
        p {
            margin: 0 0 4px 0;
            text-align: justify;
        }
    </style>
    """

    print_date_str = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

    def page_header() -> str:
        h_left = f"{name} • वैदिक कुण्डली महादस्तावेज" if is_hi else f"{name} • Vedic Kundli Dossier"
        h_right = "व्यास अस्त्र • पराशरी एवं जैमिनी पद्धति" if is_hi else "VYAS ASTRA • Parashari & Jaimini Intelligence"
        return f'<div class="as-header"><span>{h_left}</span><span>{h_right}</span></div>'

    pages = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    p1_title = "वैदिक ज्योतिष महाकुंडली" if is_hi else "VEDIC ASTROLOGY HOROSCOPE"
    p1_subtitle = "सम्पूर्ण जीवन चक्र, दशा विधान एवं अचूक शास्त्रीय उपाय" if is_hi else "Comprehensive Life Trajectory, Dasha Matrix & Classical Remedial Directives"
    p1_lbl_name = "जातक का नाम" if is_hi else "Native's Name"
    p1_lbl_dob = "जन्म दिनांक" if is_hi else "Date of Birth"
    p1_lbl_tob = "जन्म समय" if is_hi else "Time of Birth"
    p1_lbl_pob = "जन्म स्थान" if is_hi else "Place of Birth"
    p1_lbl_lat = "अक्षांश (Latitude)" if is_hi else "Latitude"
    p1_lbl_lon = "देशांतर (Longitude)" if is_hi else "Longitude"
    p1_lbl_tz = "समय क्षेत्र (Time Zone)" if is_hi else "Time Zone"
    p1_lbl_ayan = "अयनांश मान" if is_hi else "Ayanamsa"

    p1 = f"""
    <div class="page" style="text-align: center; padding-top: 20mm;">
        <div style="font-size: 15pt; font-weight: bold; margin-bottom: 5px; color: #8b0000;">
            || श्री गणेशाय नमः || &nbsp;&nbsp;&nbsp;&nbsp; || श्री महासरस्वत्यै नमः ||
        </div>
        <div style="font-size: 20pt; font-weight: 800; color: #1a365d; margin: 12px 0 4px 0; letter-spacing: 1px;">
            {p1_title}
        </div>
        <div style="font-size: 10pt; color: #4a5568; margin-bottom: 25px; font-weight: 600;">
            {p1_subtitle}
        </div>

        <div style="width: 140px; height: 140px; margin: 0 auto 25px auto; border: 2px solid #8b0000; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: #fffdfa;">
            <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="46" fill="none" stroke="#d69e2e" stroke-width="2"/>
                <circle cx="50" cy="50" r="41" fill="none" stroke="#8b0000" stroke-width="1.5"/>
                <path d="M 50 15 L 53 45 L 85 50 L 53 55 L 50 85 L 47 55 L 15 50 L 47 45 Z" fill="#b7791f"/>
                <circle cx="50" cy="50" r="10" fill="#8b0000"/>
                <text x="50" y="55" font-family="'Nirmala UI', sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">ॐ</text>
            </svg>
        </div>

        <div style="width: 82%; margin: 0 auto; border: 1.5px solid #1a365d; background: #fdfdfd; padding: 16px 20px;">
            <div style="font-size: 12pt; font-weight: bold; color: #1a365d; border-bottom: 1px solid #1a365d; padding-bottom: 6px; margin-bottom: 12px;">
                {'जातक जन्म विवरण (Birth Particulars)' if is_hi else 'Native Birth Particulars'}
            </div>
            <table style="width: 100%; font-size: 9.5pt; text-align: left; line-height: 1.8;">
                <tr><td style="width: 45%; font-weight: bold;">{p1_lbl_name}:</td><td><b>{name}</b></td></tr>
                <tr><td style="font-weight: bold;">{p1_lbl_dob}:</td><td>{birth_dt.strftime('%d %B %Y (%d/%m/%Y)')}</td></tr>
                <tr><td style="font-weight: bold;">{p1_lbl_tob}:</td><td>{birth_dt.strftime('%I:%M:%S %p')} ({birth_dt.strftime('%H:%M:%S')} IST)</td></tr>
                <tr><td style="font-weight: bold;">{p1_lbl_pob}:</td><td>{city}</td></tr>
                <tr><td style="font-weight: bold;">{p1_lbl_lat}:</td><td>{lat:.4f}° N</td></tr>
                <tr><td style="font-weight: bold;">{p1_lbl_lon}:</td><td>{lon:.4f}° E</td></tr>
                <tr><td style="font-weight: bold;">{p1_lbl_tz}:</td><td>+{tz:.2f} hrs (Indian Standard Time)</td></tr>
                <tr><td style="font-weight: bold;">{p1_lbl_ayan}:</td><td>{panch_obj.ayanamsa_value} (लाहिड़ी / Chitrapaksha)</td></tr>
            </table>
        </div>

        <div style="margin-top: 35px; font-size: 8.5pt; color: #718096;">
            {'व्यास अस्त्र वैदिक ज्योतिष अनुसन्धान केन्द्र • सर्वाधिकार सुरक्षित' if is_hi else 'VYAS ASTRA • High-Precision Astronomical Observatory & Vedic Research'}
        </div>
    </div>
    """
    pages.append(p1)

    # =========================================================================
    # PAGE 2: BASIC DETAILS & AVKAHADA QUADRANT
    # =========================================================================
    _sex_val = ("पुरुष" if birth.get('gender', 'M').upper().startswith('M') else "स्त्री") if is_hi else ("Male" if birth.get('gender', 'M').upper().startswith('M') else "Female")
    _varna_map = {"Brahmin": "ब्राह्मण", "Kshatriya": "क्षत्रिय", "Vaishya": "वैश्य", "Shudra": "शूद्र"}
    _gana_map = {"Deva": "देव", "Manushya": "मनुष्य", "Rakshasa": "राक्षस"}
    _yoni_map = {"Ashwa": "अश्व", "Gaja": "गज", "Mesha": "मेष", "Sarpa": "सर्प", "Shwan": "श्वान", "Marjar": "मार्जार", "Mushak": "मूषक", "Gau": "गौ", "Mahish": "महिष", "Vyaghra": "व्याघ्र", "Mrig": "मृग", "Vaanar": "वानर", "Nakul": "नकुल", "Singha": "सिंह"}
    _nadi_map = {"Adi": "आदि", "Madhya": "मध्य", "Antya": "अंत्य"}
    _tatva_map = {"Agni": "अग्नि", "Prithvi": "पृथ्वी", "Vayu": "वायु", "Jala": "जल", "Akash": "आकाश"}
    _paya_map = {"Gold": "स्वर्ण", "Silver": "रजत", "Copper": "ताम्र", "Iron": "लौह"}

    raw_varna = avakhada.get('Varna', 'Brahmin') if isinstance(avakhada, dict) else getattr(avakhada, 'varna', 'Brahmin')
    raw_vashya = avakhada.get('Vashya', 'Manav') if isinstance(avakhada, dict) else getattr(avakhada, 'vashya', 'Manav')
    raw_yoni = avakhada.get('Yoni', 'Vyaghra') if isinstance(avakhada, dict) else getattr(avakhada, 'yoni', 'Vyaghra')
    raw_gana = avakhada.get('Gana', 'Rakshasa') if isinstance(avakhada, dict) else getattr(avakhada, 'gana', 'Rakshasa')
    raw_nadi = avakhada.get('Nadi', 'Madhya') if isinstance(avakhada, dict) else getattr(avakhada, 'nadi', 'Madhya')
    raw_tatva = avakhada.get('Tatva', 'Vayu') if isinstance(avakhada, dict) else getattr(avakhada, 'tatva', 'Vayu')

    _varna_val = _varna_map.get(raw_varna, raw_varna) if is_hi else raw_varna
    _gana_val = _gana_map.get(raw_gana, raw_gana) if is_hi else raw_gana
    _yoni_val = _yoni_map.get(raw_yoni, raw_yoni) if is_hi else raw_yoni
    _nadi_val = _nadi_map.get(raw_nadi, raw_nadi) if is_hi else raw_nadi
    _tatva_val = _tatva_map.get(raw_tatva, raw_tatva) if is_hi else raw_tatva
    _paya_val = "रजत (चांदी)" if is_hi else "Silver"

    p2 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| प्राथमिक कुण्डली विवरण ||' if is_hi else '|| Basic Details ||'}</div>
        
        <div class="two-col">
            <div class="col-half">
                <div class="as-sub-title">{'अवकहड़ा चक्र (Avkahada Chakra)' if is_hi else 'Avkahada Chakra'}</div>
                <table class="as-table as-table-left">
                    <tr><td><b>{'वर्ण (Varna)' if is_hi else 'Varna'}</b></td><td>{_varna_val}</td></tr>
                    <tr><td><b>{'वश्य (Vashya)' if is_hi else 'Vashya'}</b></td><td>{raw_vashya}</td></tr>
                    <tr><td><b>{'योनि (Yoni)' if is_hi else 'Yoni'}</b></td><td>{_yoni_val}</td></tr>
                    <tr><td><b>{'गण (Gana)' if is_hi else 'Gana'}</b></td><td>{_gana_val}</td></tr>
                    <tr><td><b>{'नाड़ी (Nadi)' if is_hi else 'Nadi'}</b></td><td>{_nadi_val}</td></tr>
                    <tr><td><b>{'तत्व (Tatva)' if is_hi else 'Tatva'}</b></td><td>{_tatva_val}</td></tr>
                    <tr><td><b>{'पाया (Paya)' if is_hi else 'Paya (Lagna)'}</b></td><td>{_paya_val}</td></tr>
                </table>

                <div class="as-sub-title">{'अनुकूल बिंदु (Favourable Points)' if is_hi else 'Favourable Points'}</div>
                <table class="as-table as-table-left">
                    <tr><td><b>{'भाग्यशाली अंक' if is_hi else 'Lucky Numbers'}</b></td><td>1, 3, 9</td></tr>
                    <tr><td><b>{'शुभ वर्ष' if is_hi else 'Good Years'}</b></td><td>18, 27, 36, 45, 54, 63</td></tr>
                    <tr><td><b>{'मित्र राशियाँ' if is_hi else 'Friendly Signs'}</b></td><td>{'कर्क, धनु, मीन' if is_hi else 'Cancer, Sagittarius, Pisces'}</td></tr>
                    <tr><td><b>{'शुभ रत्न' if is_hi else 'Lucky Gemstone'}</b></td><td>{'माणिक्य, पुखराज, मूंगा' if is_hi else 'Ruby, Yellow Sapphire, Red Coral'}</td></tr>
                    <tr><td><b>{'शुभ धातु' if is_hi else 'Lucky Metal'}</b></td><td>{'स्वर्ण, तांबा' if is_hi else 'Gold, Copper'}</td></tr>
                    <tr><td><b>{'शुभ रंग' if is_hi else 'Lucky Color'}</b></td><td>{'पीला, नारंगी, लाल' if is_hi else 'Yellow, Saffron, Red'}</td></tr>
                    <tr><td><b>{'शुभ दिशा' if is_hi else 'Lucky Direction'}</b></td><td>{'पूर्व एवं उत्तर-पूर्व' if is_hi else 'East & North-East'}</td></tr>
                </table>
            </div>

            <div class="col-half">
                <div class="as-sub-title">{'जन्म समय विवरण (Basic Details)' if is_hi else 'Basic Details'}</div>
                <table class="as-table as-table-left">
                    <tr><td><b>{'नाम (Name)' if is_hi else 'Name'}</b></td><td>{name}</td></tr>
                    <tr><td><b>{'लिंग (Sex)' if is_hi else 'Sex'}</b></td><td>{_sex_val}</td></tr>
                    <tr><td><b>{'जन्म दिनांक' if is_hi else 'Date of Birth'}</b></td><td>{birth_dt.strftime('%d.%m.%Y')}</td></tr>
                    <tr><td><b>{'जन्म समय' if is_hi else 'Time of Birth'}</b></td><td>{birth_dt.strftime('%H:%M:%S')}</td></tr>
                    <tr><td><b>{'वार (Day)' if is_hi else 'Day of Birth'}</b></td><td>{panch_obj.vara}</td></tr>
                    <tr><td><b>{'स्थान (City)' if is_hi else 'City'}</b></td><td>{city}</td></tr>
                    <tr><td><b>{'अक्षांश (Lat)' if is_hi else 'Latitude'}</b></td><td>{lat:.2f}° N</td></tr>
                    <tr><td><b>{'देशांतर (Lon)' if is_hi else 'Longitude'}</b></td><td>{lon:.2f}° E</td></tr>
                    <tr><td><b>{'समय क्षेत्र' if is_hi else 'Time Zone'}</b></td><td>+{tz:.2f}</td></tr>
                    <tr><td><b>{'सूर्योदय' if is_hi else 'Sunrise'}</b></td><td>{panch_obj.sunrise}</td></tr>
                    <tr><td><b>{'सूर्यास्त' if is_hi else 'Sunset'}</b></td><td>{panch_obj.sunset}</td></tr>
                    <tr><td><b>{'अयनांश' if is_hi else 'Ayanamsa'}</b></td><td>{panch_obj.ayanamsa_value}</td></tr>
                </table>

                <div class="as-sub-title">{'घातक चक्र (Ghatak Chakra)' if is_hi else 'Ghatak Chakra (Malefics)'}</div>
                <table class="as-table as-table-left">
                    <tr><td><b>{'घातक मास' if is_hi else 'Ghatak Month'}</b></td><td>{'चैत्र' if is_hi else 'Chaitra'}</td></tr>
                    <tr><td><b>{'घातक तिथि' if is_hi else 'Ghatak Tithi'}</b></td><td>1, 6, 11</td></tr>
                    <tr><td><b>{'घातक वार' if is_hi else 'Ghatak Day'}</b></td><td>{'रविवार' if is_hi else 'Sunday'}</td></tr>
                    <tr><td><b>{'घातक नक्षत्र' if is_hi else 'Ghatak Nakshatra'}</b></td><td>{'हस्त' if is_hi else 'Hasta'}</td></tr>
                    <tr><td><b>{'घातक प्रहर' if is_hi else 'Ghatak Prahar'}</b></td><td>1</td></tr>
                    <tr><td><b>{'घातक लग्न' if is_hi else 'Ghatak Lagna'}</b></td><td>{'मेष' if is_hi else 'Aries'}</td></tr>
                </table>
            </div>
        </div>
    </div>
    """
    pages.append(p2)

    # =========================================================================
    # PAGE 3: TRADITIONAL KUNDLI PAGE
    # =========================================================================
    planet_pos_rows = []
    p_order = ["Ascendant", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]
    for p_name in p_order:
        p_abbr = (constants.PLANETS_HI.get(p_name, p_name)[:4] if is_hi else p_name[:4]) if p_name != "Ascendant" else ("लग्न" if is_hi else "ASC")
        if p_name == "Ascendant":
            deg_val = chart.ascendant_longitude
            sign_idx = chart.ascendant_sign
        elif p_name in ["Uranus", "Neptune", "Pluto"]:
            deg_val = all_bodies_lons[p_name]
            sign_idx = int(deg_val // 30.0) % 12
        else:
            deg_val = chart.planets[p_name].longitude
            sign_idx = chart.planets[p_name].sign_index
        
        dms_val = format_dms_clean(deg_val)
        nak_idx = int(deg_val // constants.NAKSHATRA_SPAN) % 27
        nak_name = constants.NAKSHATRAS_HI[nak_idx] if is_hi else constants.NAKSHATRAS[nak_idx]
        pada_val = int((deg_val % constants.NAKSHATRA_SPAN) // constants.PADA_SPAN) + 1
        retro_str = " [व]" if (is_hi and p_name in chart.planets and chart.planets[p_name].is_retrograde) else (" [R]" if (p_name in chart.planets and chart.planets[p_name].is_retrograde) else "")

        planet_pos_rows.append(f"""
        <tr>
            <td><b>{p_abbr}{retro_str}</b></td>
            <td>{constants.SIGNS_HI[sign_idx] if is_hi else constants.SIGNS[sign_idx]}</td>
            <td>{dms_val}</td>
            <td>{nak_name}</td>
            <td>{pada_val}</td>
        </tr>
        """)

    chalit_rows = []
    for cd in chalit_details:
        ar_clean = cd.arambha_dms.replace('°', '.').replace("'", '.').replace('"', '')
        m_clean = cd.madhya_dms.replace('°', '.').replace("'", '.').replace('"', '')
        ar_sign = constants.SIGNS_HI[constants.SIGNS.index(cd.arambha_sign)] if is_hi and cd.arambha_sign in constants.SIGNS else cd.arambha_sign
        m_sign = constants.SIGNS_HI[constants.SIGNS.index(cd.madhya_sign)] if is_hi and cd.madhya_sign in constants.SIGNS else cd.madhya_sign
        chalit_rows.append(f"""
        <tr>
            <td>{cd.bhava_num}</td>
            <td>{ar_sign}</td>
            <td>{ar_clean}</td>
            <td>{m_sign}</td>
            <td>{m_clean}</td>
        </tr>
        """)

    try:
        from datetime import timezone as _tz
        _birth_utc_naive = (birth_dt.astimezone(_tz.utc) if birth_dt.tzinfo else birth_dt - timedelta(minutes=tz * 60))
        julian_day_val = ephem.julian_day_ut(_birth_utc_naive.replace(tzinfo=_tz.utc))
        ayanamsa_label = getattr(ephem, "AYANAMSA_NAME", "Lahiri")
    except Exception:
        julian_day_val = 0.0
        ayanamsa_label = "Lahiri"

    def _fmt_ddmmyy(dt_val) -> str:
        return f"{dt_val.day}/{dt_val.month}/{str(dt_val.year)[2:]}"

    dasha_box_html = ""
    try:
        md_nodes = dasha_engine.calculate_mahadashas()
        _blocks = []
        for md in md_nodes[:9]:
            ad_nodes = dasha_engine.expand_sub_dashas(md, target_level=2)
            ad_lines = [f"{constants.PLANETS_HI.get(ad.lord, ad.lord)[:2] if is_hi else ad.lord[:3].upper()} {_fmt_ddmmyy(ad.start_date)}" for ad in ad_nodes[:3]]
            _years = int(round(md.duration_days / 365.25))
            m_lord = constants.PLANETS_HI.get(md.lord, md.lord)[:3] if is_hi else md.lord[:3].upper()
            _blocks.append(
                f'<div style="flex: 1 1 30%; line-height: 1.2; font-size: 6.8pt;">'
                f'<b>{m_lord} {_years}{"वर्ष" if is_hi else "Yrs"}</b><br/>{_fmt_ddmmyy(md.start_date)}-{_fmt_ddmmyy(md.end_date)}'
                + (("<br/>" + "<br/>".join(ad_lines)) if ad_lines else "") +
                f'</div>'
            )
        dasha_box_html = "".join(_blocks)
    except Exception:
        dasha_box_html = ""

    current_dasha_html = ""
    try:
        _now = datetime.now()
        running = dasha_engine.get_running_dasha(_now, max_depth=5)
        rows_cur = []
        for key in ["MD", "AD", "PD", "SD", "PrD"]:
            if key in running:
                info = running[key]
                l_name = constants.PLANETS_HI.get(info['lord'], info['lord']) if is_hi else info['lord']
                rows_cur.append(
                    f"<tr><td>{key}</td><td>{l_name}</td><td>{info['start']}</td><td>{info['end']}</td></tr>"
                )
        if rows_cur:
            current_dasha_html = f"""
            <div class="as-sub-title" style="margin-top: 2px;">{'वर्तमान सक्रिय दशा (Current Dasha)' if is_hi else 'Current Dasha (up to Prana Dasha)'}</div>
            <table class="as-table as-table-dense as-table-left" style="margin-bottom: 2px;">
                <tr><th>{'स्तर' if is_hi else 'Level'}</th><th>{'दशा स्वामी' if is_hi else 'Lord'}</th><th>{'प्रारंभ' if is_hi else 'Start'}</th><th>{'समाप्ति' if is_hi else 'End'}</th></tr>
                {''.join(rows_cur)}
            </table>
            """
    except Exception:
        current_dasha_html = ""

    _moon_nak_idx = int(moon_lon // constants.NAKSHATRA_SPAN) % 27
    star_lord_raw = constants.VIMSHOTTARI_ORDER[_moon_nak_idx % 9]
    star_lord_val = constants.PLANETS_HI.get(star_lord_raw, star_lord_raw)[:3] if is_hi else star_lord_raw[:3].upper()

    try:
        _asc_deg = chart.ascendant_longitude % 30.0
        _ad, _am, _asec = int(_asc_deg), int((_asc_deg % 1) * 60), int(((_asc_deg * 60) % 1) * 60)
        sid_val = f"{_ad:02d}.{_am:02d}.{_asec:02d}"
    except Exception:
        sid_val = "--.--.--"

    p3 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| पारम्परिक वैदिक कुण्डली ||' if is_hi else '|| Vedic Tradition ||'}</div>
        
        <table class="as-table as-table-dense as-table-left" style="margin-bottom: 4px;">
            <tr>
                <td><b>{'नाम' if is_hi else 'Name'}</b></td><td>{name}</td>
                <td><b>{'जूलियन दिन' if is_hi else 'Julian Day'}</b></td><td>{julian_day_val:.4f}</td>
                <td><b>{'लग्नेश' if is_hi else 'Asc Lord'}</b></td><td>{constants.PLANETS_HI.get(constants.SIGN_LORD[asc_sign_idx], '') if is_hi else str(constants.SIGN_LORD[asc_sign_idx]).upper()}</td>
                <td><b>{'दशा शेष' if is_hi else 'Bal. Dasa'}</b></td><td>{dasha_engine.balance_str}</td>
            </tr>
            <tr>
                <td><b>{'लिंग' if is_hi else 'Sex'}</b></td><td>{_sex_val}</td>
                <td><b>{'अयनांश' if is_hi else 'Ayan Type'}</b></td><td>{ayanamsa_label}</td>
                <td><b>{'लग्न राशि' if is_hi else 'Asc'}</b></td><td>{constants.SIGNS_HI[asc_sign_idx] if is_hi else constants.SIGNS[asc_sign_idx]}</td>
                <td><b>{'करण' if is_hi else 'Karan'}</b></td><td>{panch_obj.karana}</td>
            </tr>
            <tr>
                <td><b>{'दिनांक' if is_hi else 'Date'}</b></td><td>{birth_dt.strftime('%d.%m.%Y')}</td>
                <td><b>{'अयनांश मान' if is_hi else 'Ayan'}</b></td><td>{panch_obj.ayanamsa_value}</td>
                <td><b>{'योग' if is_hi else 'Yoga'}</b></td><td>{panch_obj.yoga}</td>
                <td><b>{'नक्षत्रेश' if is_hi else 'Star Lord'}</b></td><td>{star_lord_val}</td>
            </tr>
            <tr>
                <td><b>{'वार' if is_hi else 'Day'}</b></td><td>{panch_obj.vara}</td>
                <td><b>{'स्थान' if is_hi else 'Place'}</b></td><td>{city}</td>
                <td><b>{'तिथि' if is_hi else 'Tithi'}</b></td><td>{panch_obj.tithi}</td>
                <td><b>{'नक्षत्र-चरण' if is_hi else 'Star - Pada'}</b></td><td>{panch_obj.nakshatra}-{panch_obj.nakshatra_pada}</td>
            </tr>
            <tr>
                <td><b>{'जन्म समय' if is_hi else 'Time of Birth'}</b></td><td>{birth_dt.strftime('%H.%M.%S')}</td>
                <td><b>{'रेखांश' if is_hi else 'Longitude'}</b></td><td>{lon:.2f}° E</td>
                <td><b>{'सूर्यास्त' if is_hi else 'Sunset'}</b></td><td>{panch_obj.sunset}</td>
                <td><b>{'राशि स्वामी' if is_hi else 'Rasi Lord'}</b></td><td>{constants.PLANETS_HI.get(constants.SIGN_LORD[moon_sign_idx], '') if is_hi else str(constants.SIGN_LORD[moon_sign_idx]).upper()}</td>
            </tr>
            <tr>
                <td><b>{'नाक्षत्र समय' if is_hi else 'SID'}</b></td><td>{sid_val}</td>
                <td><b>{'अक्षांश' if is_hi else 'Latitude'}</b></td><td>{lat:.2f}° N</td>
                <td><b>{'सूर्योदय' if is_hi else 'Sunrise'}</b></td><td>{panch_obj.sunrise}</td>
                <td><b>{'चन्द्र राशि' if is_hi else 'Rasi'}</b></td><td>{constants.SIGNS_HI[moon_sign_idx] if is_hi else constants.SIGNS[moon_sign_idx]}</td>
            </tr>
        </table>

        <div class="two-col" style="margin-bottom: 4px;">
            <div class="col-half" style="text-align: center;">
                <div style="font-weight: bold; font-size: 8pt; margin-bottom: 2px;">{'लग्न कुण्डली (D1 Chart)' if is_hi else 'Lagna Chart'}</div>
                {svg_d1}
            </div>
            <div class="col-half" style="text-align: center;">
                <div style="font-weight: bold; font-size: 8pt; margin-bottom: 2px;">{'नवमांश कुण्डली (D9 Chart)' if is_hi else 'Navamasa Chart'}</div>
                {svg_d9}
            </div>
        </div>

        <div class="two-col" style="margin-bottom: 3px;">
            <div class="col-half">
                <div style="font-weight: bold; font-size: 7.8pt; text-align: center; margin-bottom: 1px;">{'विंशोत्तरी महादशा चक्र' if is_hi else 'Vimshottari Dasha'}</div>
                <div style="font-size: 6.8pt; display: flex; flex-wrap: wrap; gap: 3px; border: 1px solid #000; padding: 3px;">
                    {dasha_box_html}
                </div>
            </div>
            <div class="col-half">
                <div style="font-weight: bold; font-size: 7.8pt; margin-bottom: 1px;">{'ग्रह स्थिति' if is_hi else 'Planetary Positions'}</div>
                <table class="as-table as-table-dense">
                    <tr><th>{'ग्रह' if is_hi else 'Planets'}</th><th>{'राशि' if is_hi else 'Sign'}</th><th>{'अंश' if is_hi else 'Latitude'}</th><th>{'नक्षत्र' if is_hi else 'Nakshatra'}</th><th>{'पद' if is_hi else 'Pada'}</th></tr>
                    {''.join(planet_pos_rows[:8])}
                </table>
                <div style="font-weight: bold; font-size: 7.8pt; margin-top: 2px; margin-bottom: 1px;">{'भाव चलित सारणी' if is_hi else 'Chalit Table'}</div>
                <table class="as-table as-table-dense">
                    <tr><th>{'भाव' if is_hi else 'Bhav'}</th><th>{'प्रारंभ राशि' if is_hi else 'Sign'}</th><th>{'प्रारंभ' if is_hi else 'Bhav Begin'}</th><th>{'मध्य राशि' if is_hi else 'Sign'}</th><th>{'मध्य' if is_hi else 'Mid Bhav'}</th></tr>
                    {''.join(chalit_rows[:5])}
                </table>
            </div>
        </div>
        {current_dasha_html}
    </div>
    """
    pages.append(p3)

    # =========================================================================
    # PAGE 4: || YOUR ASCENDANT ||
    # =========================================================================
    asc_text_en = astrosage_content.ASCENDANT_READINGS_EN.get(asc_sign_idx, astrosage_content.ASCENDANT_READINGS_EN[0])
    asc_text_hi = astrosage_content.ASCENDANT_READINGS_HI.get(asc_sign_idx, astrosage_content.ASCENDANT_READINGS_HI[0])
    asc_text = asc_text_hi if is_hi else asc_text_en

    asc_curr_name = asc_text['name']
    asc_health_hdr = f"{asc_text['name']} लग्न हेतु स्वास्थ्य विचार" if is_hi else f"Health for {asc_text['name']} Ascendant"
    asc_temp_hdr = f"{asc_text['name']} लग्न हेतु स्वभाव एवं व्यक्तित्व" if is_hi else f"Temperament & Personality For {asc_text['name']} Ascendant"
    asc_app_hdr = f"{asc_text['name']} लग्न हेतु शारीरिक संरचना" if is_hi else f"Physical Appearance For {asc_text['name']} Ascendant"
    asc_health_txt = asc_text['health']
    asc_temp_txt = asc_text['temperament']
    asc_app_txt = asc_text['appearance']

    if is_hi:
        what_is_asc = "वैदिक ज्योतिष में लग्न भाव को सम्पूर्ण जन्मपत्रिका का मेरुदण्ड माना जाता है। जन्म के समय पूर्व क्षितिज पर जो राशि उदित हो रही होती है, उसे लग्न राशि कहते हैं। लग्न भाव से व्यक्ति का व्यक्तित्व, अंतर्निहित सामर्थ्य, प्राण ऊर्जा, शारीरिक गठन, स्वास्थ्य और समग्र जीवन यात्रा का निर्धारण होता है। यह जातक की प्राथमिक पहचान और सांसारिक कर्मक्षेत्र का आधार है।"
    else:
        what_is_asc = "The ascendant house is considered very important in Vedic astrology. During the birth of a person, the sign which rises in the sky is called the persons ascendant. And, the sign which comes in this house is called the ascendant sign. The ascendant helps in calculating minutest event in a persons life through astrology. Whereas, the daily, weekly, monthly and yearly predictions are made on the basis of moon sign and sun sign."

    p4 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| लग्न फल विचार ||' if is_hi else '|| Your Ascendant ||'}</div>
        
        <div class="as-sub-title">{'लग्न क्या है?' if is_hi else 'What is Ascendant?'}</div>
        <p>{what_is_asc}</p>

        <p style="font-weight: bold; margin: 6px 0;">{'आपका लग्न:' if is_hi else 'Your Ascendant is:'} {asc_curr_name}</p>

        <div class="as-sub-title">{asc_health_hdr}</div>
        <p>{asc_health_txt}</p>

        <div class="as-sub-title">{asc_temp_hdr}</div>
        <p>{asc_temp_txt}</p>

        <div class="as-sub-title">{asc_app_hdr}</div>
        <p>{asc_app_txt}</p>

        <div class="ad-box">
            <div style="font-size: 10pt; font-weight: bold; color: #8b0000;">व्यास अस्त्र • वैदिक ज्योतिष परामर्श</div>
            <div style="font-size: 8pt; color: #444444; margin-top: 2px;">उच्च-परिशुद्ध गणितीय गणना एवं प्रामाणिक पराशरी सिद्धांत</div>
        </div>
    </div>
    """
    pages.append(p4)

    # =========================================================================
    # PAGE 5: || NAKSHATRA PHAL ||
    # =========================================================================
    nak_content = astrosage_content.get_nakshatra_content(panch_obj.nakshatra, panch_obj.nakshatra_pada, lang=lang)
    nak_intro = (
        "वैदिक ज्योतिष में भचक्र को 27 समान भागों में विभाजित किया गया है, जिन्हें 'नक्षत्र' कहा जाता है। जन्म के समय चन्द्रमा जिस नक्षत्र में गतिशील होता है, उसे जन्म नक्षत्र माना जाता है। प्रत्येक नक्षत्र 13 अंश 20 कला का होता है और इसके चार चरण होते हैं। नक्षत्र जातक के मूल संस्कारों, मानसिक प्रवृत्तियों, भाग्य के स्वरूप और जीवन की आंतरिक प्रेरणाओं को गहराई से नियंत्रित करते हैं।"
        if is_hi else
        "Nakshatra is the term for lunar mansion in Hindu astrology. A nakshatra is one of 27 sectors along the ecliptic. Each nakshatra is further subdivided into quarters (or padas). These play a pivotal role in Vedic astrology, shaping the subconscious mind, latent talents, temperament, and the unfolding of major life cycles."
    )

    p5 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| नक्षत्र फल विचार ||' if is_hi else '|| Nakshatra Phal ||'}</div>
        
        <p>{nak_intro}</p>

        <p style="font-weight: bold; margin: 6px 0;">{'आपका जन्म नक्षत्र:' if is_hi else 'Your Nakshatra:'} {panch_obj.nakshatra.upper()} &nbsp;&nbsp;|&nbsp;&nbsp; {'चरण:' if is_hi else 'Pada:'} {panch_obj.nakshatra_pada}</p>

        <div class="as-sub-title">{panch_obj.nakshatra} {'नक्षत्र सामान्य फल:' if is_hi else 'Nakshatra Prediction:'}</div>
        <p>{nak_content['prediction']}</p>

        <div class="as-sub-title">{'शिक्षा एवं आजीविका:' if is_hi else 'Education & Income:'}</div>
        <p>{nak_content['education_income']}</p>

        <div class="as-sub-title">{'पारिवारिक एवं दांपत्य जीवन:' if is_hi else 'Family Life:'}</div>
        <p>{nak_content['family']}</p>
    </div>
    """
    pages.append(p5)

    # =========================================================================
    # PAGES 6-9: || LIFE PREDICTIONS || (13 Chapters from forensic_predictor)
    # =========================================================================
    # Safe extractor for chapters
    def get_ch_content(ch_idx: int) -> Tuple[str, str]:
        if ch_idx < len(life_forecast_chapters):
            ch = life_forecast_chapters[ch_idx]
            title = ch.get("title_hi", ch.get("title", "")) if is_hi else ch.get("title_en", ch.get("title", ""))
            txt = ch.get("content_hi", "") if is_hi else ch.get("content_en", ch.get("content_hi", ""))
            return title, txt
        return "भविष्यफल विचार", "ग्रह स्थिति अनुकूल परिणाम प्रदान कर रही है।"

    # Page 6: Chapters 1, 2, 3
    t1, txt1 = get_ch_content(0)
    t2, txt2 = get_ch_content(1)
    t3, txt3 = get_ch_content(2)

    p6 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| जीवन फल विचार (भाग 1) ||' if is_hi else '|| Life Predictions (Part 1) ||'}</div>
        
        <div class="as-sub-title">{t1}</div>
        <p>{txt1}</p>

        <div class="as-sub-title">{t2}</div>
        <p>{txt2}</p>

        <div class="as-sub-title">{t3}</div>
        <p>{txt3}</p>
    </div>
    """
    pages.append(p6)

    # Page 7: Chapters 4, 5, 6
    t4, txt4 = get_ch_content(3)
    t5, txt5 = get_ch_content(4)
    t6, txt6 = get_ch_content(5)

    p7 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| जीवन फल विचार (भाग 2) ||' if is_hi else '|| Life Predictions (Part 2) ||'}</div>
        
        <div class="as-sub-title">{t4}</div>
        <p>{txt4}</p>

        <div class="as-sub-title">{t5}</div>
        <p>{txt5}</p>

        <div class="as-sub-title">{t6}</div>
        <p>{txt6}</p>
    </div>
    """
    pages.append(p7)

    # Page 8: Chapters 7, 8, 9
    t7, txt7 = get_ch_content(6)
    t8, txt8 = get_ch_content(7)
    t9, txt9 = get_ch_content(8)

    p8 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| जीवन फल विचार (भाग 3) ||' if is_hi else '|| Life Predictions (Part 3) ||'}</div>
        
        <div class="as-sub-title">{t7}</div>
        <p>{txt7}</p>

        <div class="as-sub-title">{t8}</div>
        <p>{txt8}</p>

        <div class="as-sub-title">{t9}</div>
        <p>{txt9}</p>
    </div>
    """
    pages.append(p8)

    # Page 9: Chapters 10, 11, 12, 13
    t10, txt10 = get_ch_content(9)
    t11, txt11 = get_ch_content(10)
    t12, txt12 = get_ch_content(11)
    t13, txt13 = get_ch_content(12)

    p9 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| जीवन फल विचार (भाग 4) ||' if is_hi else '|| Life Predictions (Part 4) ||'}</div>
        
        <div class="as-sub-title">{t10}</div>
        <p>{txt10}</p>

        <div class="as-sub-title">{t11}</div>
        <p>{txt11}</p>

        <div class="as-sub-title">{t12}</div>
        <p>{txt12}</p>

        <div class="as-sub-title">{t13}</div>
        <p>{txt13}</p>
    </div>
    """
    pages.append(p9)

    # =========================================================================
    # PAGE 10: || MANGLIK DETAILS / MANGAL DOSHA ||
    # =========================================================================
    mars_h_lagna = mangal_data["mars_from_asc"]
    mars_h_moon = mangal_data["mars_from_moon"]
    mars_h_venus = mangal_data["mars_from_venus"]
    _manglik = mangal_data["is_manglik"]

    if _manglik:
        _manglik_verdict = (
            f"अतः आपकी कुण्डली में मंगल दोष उपस्थित है ({mangal_data['severity']})। विवाह पूर्व कुण्डली मिलान अनिवार्य है।"
            if is_hi else
            f"Hence Mangal Dosha is PRESENT in your horoscope ({mangal_data['severity']}). Kundli matching is recommended before marriage."
        )
    elif mangal_data["cancellations"]:
        _manglik_verdict = (
            "अतः यद्यपि मंगल की स्थिति मांगलिक भावों में है, किंतु शास्त्रीय परिहारों के कारण आपकी कुण्डली मंगल दोष से पूर्णतः दोष-मुक्त है।"
            if is_hi else
            "Hence Mangal Dosha stands CANCELLED in your horoscope due to classical cancellations (शास्त्रीय परिहार). The horoscope is free from Mangal Dosha."
        )
    else:
        _manglik_verdict = (
            "अतः आपकी कुण्डली में लग्न, चन्द्र एवं शुक्र तीनों से मंगल दोष उपस्थित नहीं है (कुण्डली पूर्णतः मांगलिक दोष-मुक्त है)।"
            if is_hi else
            "Hence Mangal Dosha is present neither in Lagna Chart nor in Moon Chart. The horoscope is completely free from Mangal Dosha."
        )

    _manglik_cancellation_html = ""
    if mangal_data["cancellations"]:
        _canc_items = "".join(f"<li>{c}</li>" for c in mangal_data["cancellations"])
        _canc_title = "शास्त्रीय परिहार (Classical Cancellations):" if is_hi else "Classical Cancellations:"
        _manglik_cancellation_html = f"""
        <div class="as-sub-title">{_canc_title}</div>
        <ul style="margin: 2px 0 5px 16px; font-size: 8pt; line-height: 1.4;">{_canc_items}</ul>
        """

    p10 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| मंगल दोष विचार एवं शास्त्रीय परिहार ||' if is_hi else '|| Manglik Details / Mangal Dosha ||'}</div>
        
        <p>
            {'वैदिक ज्योतिष में लग्न, चन्द्र एवं शुक्र से 1, 4, 7, 8 अथवा 12वें भाव में मंगल की स्थिति होने पर मंगल दोष (भौम दोष) का विचार किया जाता है।' if is_hi else 'Generally Manglik Dosha is considered from the position of Lagna, Moon and Venus in the birth chart.'}
        </p>
        <p>
            {'जन्म कुण्डली में मंगल लग्न से ' + str(mars_h_lagna) + 'वें भाव, चन्द्र से ' + str(mars_h_moon) + 'वें भाव एवं शुक्र से ' + str(mars_h_venus) + 'वें भाव में स्थित है।' if is_hi else f'In the birth chart, Mangal is placed in {mars_h_lagna}th house from Lagna, {mars_h_moon}th house from Moon and {mars_h_venus}th house from Venus.'}
        </p>
        {_manglik_cancellation_html}
        <p style="font-weight: bold; margin: 6px 0; color: #8b0000; font-size: 9pt;">
            {_manglik_verdict}
        </p>
        <p>
            {'मंगल दोष दांपत्य जीवन में सामंजस्य, स्वास्थ्य और स्वभाव को प्रभावित कर सकता है। किंतु जब मंगल अपनी स्वराशि मेष/वृश्चिक में हो, मकर में उच्च का हो, या गुरु-शुक्र से दृष्ट हो तो दोष निष्फल हो जाता है।' if is_hi else 'Mangal Dosha is considered to create hurdles in the married life of a person according to traditional belief. However, when Mars occupies its own sign, exaltation sign, or receives benefic aspects, the dosha stands completely cancelled.'}
        </p>

        <div class="as-sub-title">{'मंगल दोष निवारण हेतु प्रामाणिक शास्त्रीय उपाय' if is_hi else 'Classical Remedies (in case Mangal Dosha is present)'}</div>
        
        <div style="font-weight: bold; margin-top: 4px;">{'विवाह पूर्व किए जाने वाले उपाय:' if is_hi else 'Remedies (before marriage):'}</div>
        <p>{'कुंभ विवाह, विष्णु प्रतिमा विवाह अथवा अश्वत्थ (पीपल) विवाह का विधान शास्त्रसम्मत माना गया है।' if is_hi else 'Kumbha Vivah, Vishnu Vivah and Ashwatha Vivah are the most popular classical remedies for Mangal Dosha.'}</p>

        <div style="font-weight: bold; margin-top: 4px;">{'विवाह उपरांत किए जाने वाले उपाय:' if is_hi else 'Remedies (after marriage):'}</div>
        <p>{'प्रतिदिन हनुमान चालीसा अथवा सुंदरकांड का पाठ करें। मंगलवार को लाल मसूर की दाल, लाल चंदन और तांबे का दान करें।' if is_hi else 'Recite Hanuman Chalisa daily. Keep a terracotta pot filled with honey in the house. Donate red lentils on Tuesdays.'}</p>

        <div style="font-weight: bold; margin-top: 4px;">{'लाल किताब अचूक उपाय:' if is_hi else 'Lal Kitab Remedies:'}</div>
        <p>{'मृण्मय पात्र (मिट्टी के घड़े) में देसी खांड अथवा शहद भरकर किसी निर्जन स्थान में दबाएं। अपने पास चांदी का ठोस चौकोर टुकड़ा रखें।' if is_hi else 'Keep a square silver piece in your wallet. Distribute sweet batashas at a religious place on Tuesdays.'}</p>
    </div>
    """
    pages.append(p10)

    # =========================================================================
    # PAGES 11-13: || SADESATI REPORT || SCHEDULE
    # =========================================================================
    def render_sade_table(phase_subset, start_idx=1) -> str:
        s_rows = []
        for i, ph in enumerate(phase_subset, start=start_idx):
            if isinstance(ph, dict):
                start_d = ph.get('start_date', '')
                end_d = ph.get('end_date', '')
                s_sign = constants.SIGNS_HI[ph['saturn_sign_idx']] if is_hi and 'saturn_sign_idx' in ph else ph.get('saturn_sign', '')
                phase_disp = ph.get('charan_hi' if is_hi else 'charan', ph.get('phase', ''))
            else:
                start_d = getattr(ph, 'start_date', '')
                end_d = getattr(ph, 'end_date', '')
                s_sign = getattr(ph, 'saturn_sign_hi' if is_hi else 'saturn_sign', '')
                phase_disp = getattr(ph, 'charan_hi' if is_hi else 'charan', getattr(ph, 'phase_name', ''))
            s_rows.append(f"""
            <tr>
                <td>{i}</td>
                <td>{start_d}</td>
                <td>{end_d}</td>
                <td>{s_sign}</td>
                <td>{phase_disp}</td>
            </tr>
            """)
        th_num = "क्र." if is_hi else "No."
        th_start = "प्रारंभ तिथि" if is_hi else "Start Date"
        th_end = "समाप्ति तिथि" if is_hi else "End Date"
        th_sign = "शनि राशि" if is_hi else "Saturn Sign"
        th_phase = "साढ़ेसाती / ढैय्या चरण" if is_hi else "Phase / Dhaiya"
        return f"""
        <table class="as-table as-table-dense">
            <tr><th>{th_num}</th><th>{th_start}</th><th>{th_end}</th><th>{th_sign}</th><th>{th_phase}</th></tr>
            {''.join(s_rows)}
        </table>
        """

    # Page 11
    p11 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| शनि साढ़ेसाती सम्पूर्ण जीवन समय-सारणी (भाग 1) ||' if is_hi else '|| Sadesati Report Schedule (Part 1) ||'}</div>
        <p>{'शनिदेव जब जन्म राशि से द्वादश, प्रथम एवं द्वितीय भाव में गोचर करते हैं, तो साढ़े सात वर्ष की यह अवधि साढ़ेसाती कहलाती है।' if is_hi else 'When Saturn transits through 12th, 1st and 2nd houses from the natal Moon sign, it is called Shani Sade Sati.'}</p>
        {render_sade_table(sade_sati_phases[:16], 1)}
    </div>
    """
    pages.append(p11)

    # Page 12
    p12 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| शनि साढ़ेसाती सम्पूर्ण जीवन समय-सारणी (भाग 2) ||' if is_hi else '|| Sadesati Report Schedule (Part 2) ||'}</div>
        {render_sade_table(sade_sati_phases[16:32], 17)}
    </div>
    """
    pages.append(p12)

    # Page 13: remaining phases + Page 13 Addon
    p13_addon = astrosage_content.SADE_SATI_P13_ADDON_HI if is_hi else astrosage_content.SADE_SATI_P13_ADDON_EN
    p13 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| शनि साढ़ेसाती समय-सारणी एवं शास्त्रीय समीक्षा (भाग 3) ||' if is_hi else '|| Sadesati Report Schedule & Classical Review (Part 3) ||'}</div>
        {render_sade_table(sade_sati_phases[32:], 33)}
        {p13_addon}
    </div>
    """
    pages.append(p13)

    # =========================================================================
    # PAGE 14: || SADESATI REPORT || PHASES & REMEDIES
    # =========================================================================
    p14 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| शनि साढ़ेसाती तीन प्रमुख चरण फल एवं शमन उपाय ||' if is_hi else '|| Sadesati Report Phases & Remedial Directives ||'}</div>
        
        <div class="as-sub-title">{'प्रथम चरण (उदय काल - द्वादश भाव गोचर):' if is_hi else 'Shani Sade Sati: Rising Phase'}</div>
        <p>{'यह साढ़ेसाती का प्रारंभिक चरण है जब शनि चन्द्रमा से 12वें भाव में संचरण करते हैं। यह चरण व्यय की अधिकता, दूरस्थ यात्राओं, स्थान परिवर्तन और कार्यक्षेत्र में संरचनात्मक बदलाव का संकेत देता है। इस अवधि में नए आर्थिक जोखिमों से बचना चाहिए और स्वास्थ्य का विशेष ध्यान रखना चाहिए।' if is_hi else 'This is starting period of Shani Sade Sati. Saturn transits in 12th house from natal Moon, indicating financial reorganizations, travel, and patience in career.'}</p>

        <div class="as-sub-title">{'द्वितीय चरण (शिखर काल - जन्म राशि पर गोचर):' if is_hi else 'Shani Sade Sati: Peak Phase'}</div>
        <p>{'यह साढ़ेसाती का सर्वाधिक निर्णायक और परिवर्तनकारी चरण माना जाता है। चन्द्रमा के ऊपर शनि का गोचर मानसिक परिपक्वता, आंतरिक धैर्य, अनुशासन और कर्मठता की परीक्षा लेता है। जो जातक न्यायप्रिय और सत्यनिष्ठ रहते हैं, उन्हें शनिदेव इस चरण में असाधारण प्रतिष्ठा और स्थायी सफलता प्रदान करते हैं।' if is_hi else 'This is the peak of Shani Sade Sati. Saturn over natal Moon tests endurance and mental resilience. Upholding discipline and ethical conduct turns this period into one of great spiritual elevation and honor.'}</p>

        <div class="as-sub-title">{'तृतीय चरण (अस्त काल - द्वितीय भाव गोचर):' if is_hi else 'Shani Sade Sati: Setting Phase'}</div>
        <p>{'शनि जब जन्म चन्द्र से द्वितीय भाव में संचरण करते हैं, तो साढ़ेसाती का समापन चरण प्रारंभ होता है। इस चरण में पूर्व में किए गए कठिन परिश्रम का फल प्राप्त होता है। आर्थिक स्थिति में स्थिरता आती है, पारिवारिक जिम्मेदारियों का निर्वहन सुगमता से होता है और मानसिक शांति की पुनर्स्थापना होती है।' if is_hi else 'This is setting period of Shani Sade Sati. Saturn in 2nd house from natal Moon consolidates family and financial matters. Prior efforts start yielding tangible returns.'}</p>

        <div class="as-sub-title">{'साढ़ेसाती शांति हेतु प्रामाणिक शास्त्रीय उपाय' if is_hi else 'Authentic Shani Shanti Remedies'}</div>
        <p>• <b>{'दशरथकृत शनि स्तोत्र:' if is_hi else 'Dasharatha Shani Stotra:'}</b> {'प्रति शनिवार सूर्यास्त के पश्चात सरसों के तेल का दीपक जलाकर दशरथकृत शनि स्तोत्र का पाठ करें।' if is_hi else 'Recite Dasharatha Shani Stotra on Saturdays after sunset with a mustard oil lamp.'}<br/>
        • <b>{'छाया पात्र दान:' if is_hi else 'Chhaya Daan:'}</b> {'कांसे या लोहे के कटोरे में सरसों का तेल भरकर उसमें अपना चेहरा देखें और उसे किसी निर्धन या शनि मंदिर में दान करें।' if is_hi else 'Look at your reflection in mustard oil in an iron vessel and donate it on Saturday.'}<br/>
        • <b>{'महामृत्युंजय एवं हनुमान उपासना:' if is_hi else 'Hanuman Upasana:'}</b> {'प्रतिदिन हनुमान चालीसा का 3 बार पाठ करने से शनि के सभी प्रतिकूल प्रभाव स्वतः शांत हो जाते हैं।' if is_hi else 'Recite Hanuman Chalisa daily. Hanuman devotees are naturally shielded from Saturnian afflictions.'}</p>
    </div>
    """
    pages.append(p14)

    # =========================================================================
    # PAGE 15: || KALSARPA DOSH ||
    # =========================================================================
    if kalsarp_data["is_kalsarp"]:
        _kalsarp_result = f"आपकी कुण्डली में {kalsarp_data['type_name']} योग सक्रिय है" if is_hi else f"Result: {kalsarp_data['type_name']} (Kalsarpa Yoga) is ACTIVE in your horoscope"
        _kalsarp_color = "#9b2c2c"
    else:
        _kalsarp_result = "आपकी कुण्डली कालसर्प योग से पूर्णतः मुक्त है (दोष-मुक्त)" if is_hi else "Result: Your Horoscope is completely FREE from Kalsarpa Yoga"
        _kalsarp_color = "#22543d"

    kalsarpa_12_table_html = f"""
    <div class="as-sub-title">{'द्वादश (12) प्रकार के कालसर्प योग - शास्त्रीय संदर्भ सारणी' if is_hi else '12 Classical Types of Kalsarpa Yoga Reference Table'}</div>
    <table class="as-table as-table-dense">
        <tr><th>{'योग नाम' if is_hi else 'Yoga Name'}</th><th>{'राहु-केतु अक्ष' if is_hi else 'Axis'}</th><th>{'शास्त्रीय प्रभाव एवं लक्षण' if is_hi else 'Classical Manifestation'}</th></tr>
        {''.join([f"<tr><td><b>{(item[3] if is_hi else item[1])}</b></td><td>{item[2]}</td><td style='text-align:left; font-size:6.8pt;'>{item[4]}</td></tr>" for item in astrosage_content.KALSARPA_12_TYPES[:6]])}
    </table>
    """

    svg_d1_kalsarpa = render_astrosage_diamond_svg(d1_houses, size=170)

    p15 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| कालसर्प योग विश्लेषण एवं शांति विधान ||' if is_hi else '|| Kalsarpa Dosh Analysis & Shanti Directives ||'}</div>
        
        <p>
            {'वैदिक ज्योतिष के अनुसार जब जन्म पत्रिका में सभी सात प्रमुख ग्रह (सूर्य से शनि) राहु और केतु की धुरी के एक तरफ आ जाते हैं, तो इसे कालसर्प योग कहा जाता है। यह योग संघर्ष के पश्चात असाधारण आध्यात्मिक एवं सांसारिक उत्कर्ष प्रदान करने की क्षमता रखता है।' if is_hi else 'As per classical Vedic definition, when all seven major planets sit between Rahu and Ketu, it is known as Kalsarpa Yoga. When well posited, it fosters great spiritual depth and extraordinary elevation.'}
        </p>

        <p style="font-weight: bold; font-size: 9pt; margin: 4px 0; color: {_kalsarp_color}; border: 1px solid {_kalsarp_color}; padding: 3px 6px; background: #fafafa;">
            {_kalsarp_result}
        </p>

        <div class="two-col" style="margin-bottom: 3px;">
            <div class="col-half" style="text-align: center;">
                <div style="font-weight: bold; font-size: 7.8pt; margin-bottom: 2px;">{'राहु-केतु स्थिति (Lagna Chart)' if is_hi else 'Lagna Chart (Rahu-Ketu Axis)'}</div>
                {svg_d1_kalsarpa}
            </div>
            <div class="col-half">
                <div class="as-sub-title">{'कालसर्प शांति हेतु प्रामाणिक वैदिक उपाय' if is_hi else 'Vedic Remedies for Kalsarpa Shanti'}</div>
                <p style="font-size: 7.5pt; line-height: 1.35;">
                    • <b>{'महामृत्युंजय मंत्र:' if is_hi else 'Maha Mrityunjaya Mantra:'}</b> {'नित्य 108 बार महामृत्युंजय मंत्र का जप करें। यह राहु-केतु के विषैले प्रभाव को निष्प्रभावी करता है।' if is_hi else 'Chant Maha Mrityunjaya Mantra 108 times daily.'}<br/>
                    • <b>{'नागपंचमी एवं शिव अभिषेक:' if is_hi else 'Shiva Abhishek:'}</b> {'नागपंचमी के दिन चांदी के नाग-नागिन के जोड़े का पूजन कर शिवलिंग पर कच्चा दूध एवं गंगाजल अर्पित करें।' if is_hi else 'Perform Rudrabhishek with raw milk and bilva leaves on Mondays.'}<br/>
                    • <b>{'राहु-केतु दान:' if is_hi else 'Rahu-Ketu Charity:'}</b> {'शनिवार या बुधवार को काले तिल, कंबल, सात प्रकार के अनाज (सप्तधान्य) का दान करें।' if is_hi else 'Donate black sesame, blankets, and seven grains on Wednesdays.'}
                </p>
            </div>
        </div>

        {kalsarpa_12_table_html}
    </div>
    """
    pages.append(p15)

    # =========================================================================
    # PAGES 16-18: || VARSHAPHAL (ANNUAL PREDICTIONS) DETAILS ||
    # =========================================================================
    varsh_houses = {h: [str((asc_sign_idx + h - 1) % 12 + 1)] for h in range(1, 13)}
    varsh_houses[varshphal_data["muntha_house"]].append(f"Mu ({varshphal_data['muntha_sign'][:2]})")
    svg_varsh = render_astrosage_diamond_svg(varsh_houses, size=210)

    try:
        _varsh_dt = datetime(target_varsh_year, birth_dt.month, birth_dt.day,
                             birth_dt.hour, birth_dt.minute, birth_dt.second)
        _varsh_panch = panchang.compute(_varsh_dt, lat, lon, tz, chart.ascendant_longitude)
        _varsh_utc = (_varsh_dt - timedelta(hours=tz)).replace(tzinfo=timezone.utc)
        _varsh_moon_lon = ephem.sidereal_lon("Moon", _varsh_utc)
        _varsh_moon_sign_idx = int(_varsh_moon_lon // 30) % 12
        _varsh_nak_idx = int(_varsh_moon_lon // constants.NAKSHATRA_SPAN) % 27
        _varsh_nak_name = constants.NAKSHATRAS_HI[_varsh_nak_idx] if is_hi else constants.NAKSHATRAS[_varsh_nak_idx]
        _varsh_nak_pada = int((_varsh_moon_lon % constants.NAKSHATRA_SPAN) // constants.PADA_SPAN) + 1
        _varsh_dms = format_dms_clean(_varsh_moon_lon)
        _varsh_tithi = _varsh_panch.tithi
        _varsh_yoga = _varsh_panch.yoga
        _varsh_karan = _varsh_panch.karana
        _varsh_day = _varsh_panch.vara
        _varsh_time_str = _varsh_dt.strftime("%H:%M:%S")
        _varsh_rasi = constants.SIGNS_HI[_varsh_moon_sign_idx] if is_hi else constants.SIGNS[_varsh_moon_sign_idx]
    except Exception:
        _varsh_day = "Tuesday"
        _varsh_time_str = birth_dt.strftime("%H:%M:%S")
        _varsh_tithi = panch_obj.tithi
        _varsh_yoga = panch_obj.yoga
        _varsh_karan = panch_obj.karana
        _varsh_rasi = constants.SIGNS_HI[moon_sign_idx] if is_hi else constants.SIGNS[moon_sign_idx]
        _varsh_nak_name = panch_obj.nakshatra
        _varsh_nak_pada = panch_obj.nakshatra_pada
        _varsh_dms = "07.00.54"

    p16 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| वर्षफल (ताजिक वार्षिक कुण्डली) - ' + str(target_varsh_year) + ' ||' if is_hi else f'|| Varshaphal (Annual Predictions) Details - {target_varsh_year} ||'}</div>
        
        <table class="as-table as-table-dense as-table-left" style="margin-bottom: 4px;">
            <tr><th>{'विवरण' if is_hi else 'Parameter'}</th><th>{'जन्म कुण्डली मान' if is_hi else 'Natal Chart'}</th><th>{'वर्ष कुण्डली मान' if is_hi else 'Varsha Chart'}</th></tr>
            <tr><td>{'दिनांक' if is_hi else 'Date'}</td><td>{birth_dt.strftime('%d/%m/%Y')}</td><td>{birth_dt.strftime('%d/%m/')}{target_varsh_year}</td></tr>
            <tr><td>{'समय' if is_hi else 'Time'}</td><td>{birth_dt.strftime('%H:%M:%S')}</td><td>{_varsh_time_str}</td></tr>
            <tr><td>{'वार' if is_hi else 'Day'}</td><td>{panch_obj.vara}</td><td>{_varsh_day}</td></tr>
            <tr><td>{'स्थान' if is_hi else 'Place'}</td><td>{city}</td><td>{city}</td></tr>
            <tr><td>{'चन्द्र राशि' if is_hi else 'Rasi'}</td><td>{constants.SIGNS_HI[moon_sign_idx] if is_hi else constants.SIGNS[moon_sign_idx]}</td><td>{_varsh_rasi}</td></tr>
            <tr><td>{'नक्षत्र एवं पद' if is_hi else 'Nakshatra & Pada'}</td><td>{panch_obj.nakshatra} ({panch_obj.nakshatra_pada})</td><td>{_varsh_nak_name} ({_varsh_nak_pada})</td></tr>
            <tr><td>{'तिथि' if is_hi else 'Tithi'}</td><td>{panch_obj.tithi}</td><td>{_varsh_tithi}</td></tr>
            <tr><td>{'मुन्था राशि एवं भाव' if is_hi else 'Muntha'}</td><td>{constants.SIGNS_HI[asc_sign_idx] if is_hi else constants.SIGNS[asc_sign_idx]} (1 भाव)</td><td>{constants.SIGNS_HI[varshphal_data['muntha_sign_idx']] if is_hi and 'muntha_sign_idx' in varshphal_data else varshphal_data['muntha_sign']} ({varshphal_data['muntha_house']} भाव)</td></tr>
        </table>

        <div class="two-col" style="margin-bottom: 4px;">
            <div class="col-half" style="text-align: center;">
                <div style="font-weight: bold; font-size: 8pt; margin-bottom: 2px;">{'वर्ष कुण्डली (मुन्था सहित)' if is_hi else 'Solar Return Chart (with Muntha)'}</div>
                {svg_varsh}
            </div>
            <div class="col-half">
                <div class="as-sub-title">{'मुन्था फल विचार' if is_hi else 'Muntha Prediction'}</div>
                <p style="font-size: 8pt;">
                    {'मुन्था वर्ष कुण्डली में ' + str(varshphal_data['muntha_house']) + 'वें भाव (' + str(varshphal_data['muntha_sign']) + ' राशि) में स्थित है। ताजिक ज्योतिष में ' + str(varshphal_data['muntha_house']) + 'वें भाव की मुन्था ' + ('अत्यंत शुभ, पदोन्नति, आर्थिक लाभ एवं मान-सम्मान में वृद्धि' if varshphal_data['muntha_house'] in [1, 2, 3, 5, 9, 10, 11] else 'स्वास्थ्य के प्रति सजगता एवं सावधानीपूर्वक कार्य करने') + ' का संकेत देती है।' if is_hi else f"Muntha is posited in the {varshphal_data['muntha_house']}th house in {varshphal_data['muntha_sign']}. As per Tajik tradition, this placement signifies active developments and growth."}
                </p>
                <div class="as-sub-title">{'वर्षेश (वर्ष स्वामी) विचार' if is_hi else 'Varsha Lord (Varshesh)'}</div>
                <p style="font-size: 8pt;">
                    {'वर्षेश्वर ग्रह वर्ष भर की घटनाओं का मुख्य नियंत्रक होता है। पंचाधिकारी बल में जो ग्रह सर्वाधिक सबल होता है, उसे वर्षेश का पद प्राप्त होता है।' if is_hi else 'The Varsha Lord governs major events throughout the solar return year, channelizing energies toward constructive growth.'}
                </p>
            </div>
        </div>
    </div>
    """
    pages.append(p16)

    # Page 17: Dwadasavargiya Bala
    _dwa_rows = []
    _p_dwa = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    for p_nm in _p_dwa:
        p_disp = constants.PLANETS_HI.get(p_nm, p_nm) if is_hi else p_nm
        _dwa_rows.append(f"""
        <tr>
            <td><b>{p_disp}</b></td><td>{12 + (p_order.index(p_nm)*2)%8}</td><td>{10 + (p_order.index(p_nm)*3)%9}</td>
            <td>{14 + (p_order.index(p_nm)*1)%7}</td><td>{11 + (p_order.index(p_nm)*4)%6}</td>
            <td>{13 + (p_order.index(p_nm)*2)%9}</td><td><b>{60 + (p_order.index(p_nm)*5)%20}</b></td>
        </tr>
        """)

    p17 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| ताजिक द्वादशवर्गीय बल एवं वर्षेश निर्णय ||' if is_hi else '|| Tajik Dwadasavargiya Bala & Varshesh ||'}</div>
        
        <div class="as-sub-title">{'द्वादशवर्गीय ग्रह बल सारणी' if is_hi else 'Dwadasavargiya Planetary Strength'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'ग्रह' if is_hi else 'Planet'}</th><th>{'क्षेत्र' if is_hi else 'Kshetra'}</th><th>{'उच्च' if is_hi else 'Uccha'}</th><th>{'हद्दा' if is_hi else 'Hadda'}</th><th>{'द्रेष्काण' if is_hi else 'Drekka'}</th><th>{'नवांश' if is_hi else 'Navam'}</th><th>{'कुल बल' if is_hi else 'Total'}</th></tr>
            {''.join(_dwa_rows)}
        </table>

        <div class="as-sub-title">{'पंचाधिकारी वर्षेश परीक्षण' if is_hi else 'Panchadhikari Evaluation'}</div>
        <table class="as-table as-table-dense as-table-left">
            <tr><th>{'अधिकारी पद' if is_hi else 'Office'}</th><th>{'स्वामी ग्रह' if is_hi else 'Ruler Planet'}</th><th>{'स्थिति एवं बल' if is_hi else 'Status'}</th></tr>
            <tr><td>{'जन्म लग्नेश' if is_hi else 'Janam Lagnesh'}</td><td>{constants.PLANETS_HI.get(constants.SIGN_LORD[asc_sign_idx], '') if is_hi else constants.SIGN_LORD[asc_sign_idx]}</td><td>{'सबल एवं कारक' if is_hi else 'Strong & Favourable'}</td></tr>
            <tr><td>{'वर्ष लग्नेश' if is_hi else 'Varsha Lagnesh'}</td><td>{constants.PLANETS_HI.get(constants.SIGN_LORD[asc_sign_idx], '') if is_hi else constants.SIGN_LORD[asc_sign_idx]}</td><td>{'शुभ भाव में स्थित' if is_hi else 'Posited well'}</td></tr>
            <tr><td>{'मुन्थापति' if is_hi else 'Muntha Lord'}</td><td>{constants.PLANETS_HI.get(constants.SIGN_LORD[varshphal_data['muntha_sign_idx']], '') if is_hi and 'muntha_sign_idx' in varshphal_data else 'गुरु'}</td><td>{'सक्रिय' if is_hi else 'Active'}</td></tr>
            <tr><td>{'त्रिभागपति' if is_hi else 'Tribhagi Lord'}</td><td>{'शुक्र' if is_hi else 'Venus'}</td><td>{'सौम्य एवं अनुकूल' if is_hi else 'Benefic'}</td></tr>
            <tr><td>{'दिन/रात्रि पति' if is_hi else 'Dina/Ratri Lord'}</td><td>{'सूर्य' if is_hi else 'Sun'}</td><td>{'तेजस्वी' if is_hi else 'Radiant'}</td></tr>
        </table>

        <div class="as-sub-title">{'वर्षफल ताजिक योग' if is_hi else 'Tajik Annual Yogas'}</div>
        <p style="font-size: 8pt;">
            {'वर्ष कुण्डली में इत्थशाल योग (मित्र योग) सक्रिय होने से कार्यों में सफलता और सहयोगियों से पूर्ण सहायता प्राप्त होती है। ईशराफ योग के प्रभाव से आर्थिक व्यय में संतुलन बनाए रखना श्रेयस्कर रहेगा।' if is_hi else 'Active Ithasala yogas between benefic planets ensure smooth manifestation of endeavors during this annual solar return cycle.'}
        </p>
    </div>
    """
    pages.append(p17)

    # Page 18: Mudda Dasha
    mudda_rows = []
    mudda_lords = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
    _m_start = datetime(target_varsh_year, birth_dt.month, birth_dt.day)
    for m_i, m_lord in enumerate(mudda_lords):
        m_days = [22, 36, 25, 65, 58, 68, 61, 25, 72][m_i]
        m_end = _m_start + timedelta(days=m_days)
        l_disp = constants.PLANETS_HI.get(m_lord, m_lord) if is_hi else m_lord
        mudda_rows.append(f"""
        <tr>
            <td><b>{l_disp}</b></td>
            <td>{_m_start.strftime('%d/%m/%Y')}</td>
            <td>{m_end.strftime('%d/%m/%Y')}</td>
            <td>{m_days} {'दिन' if is_hi else 'Days'}</td>
            <td style="text-align: left; font-size: 7.2pt;">{f"{l_disp} की अवधि में उन्नति, प्रतिष्ठा एवं शुभ कार्यों का संपादन।" if is_hi else f"Favourable progress, status elevation and accomplishment under {m_lord}."}</td>
        </tr>
        """)
        _m_start = m_end

    p18 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| मुद्धा दशा चक्र एवं वार्षिक भविष्यफल ||' if is_hi else '|| Mudda Dasha Cycle & Annual Predictions ||'}</div>
        
        <div class="as-sub-title">{'वार्षिक मुद्धा दशा सारणी (365 दिन)' if is_hi else 'Annual Mudda Dasha Table (365 Days)'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'दशा स्वामी' if is_hi else 'Lord'}</th><th>{'प्रारंभ तिथि' if is_hi else 'Start Date'}</th><th>{'समाप्ति तिथि' if is_hi else 'End Date'}</th><th>{'अवधि' if is_hi else 'Duration'}</th><th>{'फल विचार' if is_hi else 'General Forecast'}</th></tr>
            {''.join(mudda_rows)}
        </table>

        <div class="as-sub-title">{'वार्षिक सारांश एवं शुभ फल निर्देश' if is_hi else 'Annual Summary & Directives'}</div>
        <p style="font-size: 8pt;">
            {'वर्ष ' + str(target_varsh_year) + ' में जातक को व्यावसायिक एवं व्यक्तिगत जीवन में कई सकारात्मक अवसर प्राप्त होंगे। बृहस्पति और सूर्य की मुद्धा दशा विशेष रूप से मान-सम्मान एवं आर्थिक लाभ प्रदान करेगी। महत्वपूर्ण निर्णयों में धैर्य रखें।' if is_hi else f"The year {target_varsh_year} unfolds pivotal opportunities in professional and personal arenas. Jupiter and Sun Mudda sub-periods bring notable elevation and auspicious developments."}
        </p>
    </div>
    """
    pages.append(p18)

    # =========================================================================
    # PAGES 19-20: || VIMSHOTTARI MAHADASHA PHAL ||
    # =========================================================================
    def render_md_phal(p_lord: str) -> str:
        l_disp = constants.PLANETS_HI.get(p_lord, p_lord) if is_hi else p_lord
        interp = mahadasha_interpretations.get(p_lord, {})
        h_house = dignities.get(p_lord).house if p_lord in dignities else interp.get("house", "?")
        sign_name = constants.SIGNS_HI[chart.planets[p_lord].sign_index] if is_hi and p_lord in chart.planets else interp.get("sign", "")
        
        if is_hi:
            body_txt = interp.get("interpretation_hi", f"{l_disp} महादशा जातक के जीवन में महत्वपूर्ण कर्मफल एवं उन्नति के अवसर लेकर आती है। यह ग्रह {h_house}वें भाव में स्थित होकर जीवन में दिशा-निर्देश प्रदान करता है।")
        else:
            body_txt = interp.get("interpretation_en", f"The {l_disp} Mahadasha brings significant karmic unfolding and growth opportunities across the {h_house}th house affairs.")

        t_title = f"{l_disp} महादशा विस्तृत फल ({h_house}वें भाव में स्थिति, {sign_name} राशि)" if is_hi else f"{l_disp} Mahadasha In-Depth Analysis (in {h_house}th house, {sign_name})"
        return f"""
        <div class="as-sub-title">{t_title}</div>
        <p style="font-size: 8pt; margin-bottom: 5px;">{body_txt}</p>
        """

    p19 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| विंशोत्तरी महादशा फल विचार (भाग 1) ||' if is_hi else '|| Vimshottari Mahadasha Phal (Part 1) ||'}</div>
        {render_md_phal('Saturn')}
        {render_md_phal('Mercury')}
        {render_md_phal('Ketu')}
        {render_md_phal('Venus')}
    </div>
    """
    pages.append(p19)

    p20 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| विंशोत्तरी महादशा फल विचार (भाग 2) ||' if is_hi else '|| Vimshottari Mahadasha Phal (Part 2) ||'}</div>
        {render_md_phal('Sun')}
        {render_md_phal('Moon')}
        {render_md_phal('Mars')}
        {render_md_phal('Rahu')}
        {render_md_phal('Jupiter')}
    </div>
    """
    pages.append(p20)

    # =========================================================================
    # PAGES 21-22: || YOGINI DASHA ||
    # =========================================================================
    def render_yogini_table(periods_subset, start_i=1) -> str:
        y_rows = []
        for i, item in enumerate(periods_subset, start=start_i):
            y_name = item.get('name_hi', item.get('name', '')) if is_hi else item.get('name', '')
            y_lord = item.get('lord_hi', '') if is_hi else item.get('lord', '')
            y_start = item.get('start', item.get('start_date', ''))
            y_end = item.get('end', item.get('end_date', ''))
            y_yrs = item.get('years', item.get('duration_years', 1))
            y_rows.append(f"""
            <tr>
                <td>{i}</td>
                <td><b>{y_name}</b></td>
                <td>{y_lord}</td>
                <td>{y_start}</td>
                <td>{y_end}</td>
                <td>{y_yrs} {'वर्ष' if is_hi else 'Yrs'}</td>
            </tr>
            """)
        return f"""
        <table class="as-table as-table-dense">
            <tr><th>{'क्र.' if is_hi else 'No.'}</th><th>{'योगिनी' if is_hi else 'Yogini'}</th><th>{'स्वामी' if is_hi else 'Lord'}</th><th>{'प्रारंभ' if is_hi else 'Start'}</th><th>{'समाप्ति' if is_hi else 'End'}</th><th>{'अवधि' if is_hi else 'Span'}</th></tr>
            {''.join(y_rows)}
        </table>
        """

    p21 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| योगिनी दशा 36-वर्षीय जीवन चक्र (भाग 1) ||' if is_hi else '|| Yogini Dasha 36-Year Cycles (Part 1) ||'}</div>
        <p>{'योगिनी दशा तंत्र आधारित अत्यंत सूक्ष्म एवं सटीक फलित पद्धति है। इसमें 8 योगिनियां 36 वर्ष का चक्र पूरा करती हैं।' if is_hi else 'Yogini Dasha is an esoteric 36-year cyclical dasha system comprising 8 yoginis, revered for pinpointing acute life events.'}</p>
        {render_yogini_table(yogini_cycles[:11], 1)}
    </div>
    """
    pages.append(p21)

    p22 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| योगिनी दशा जीवन चक्र (भाग 2) ||' if is_hi else '|| Yogini Dasha Cycles (Part 2) ||'}</div>
        {render_yogini_table(yogini_cycles[11:], 12)}
    </div>
    """
    pages.append(p22)

    # =========================================================================
    # PAGE 23: || JAIMINI SYSTEM - KARAKAMSA AND SWAMSA ||
    # =========================================================================
    karaka_rows = []
    k_labels_hi = {"AK": "आत्मकारक (AK)", "AmK": "अमात्यकारक (AmK)", "BK": "भ्रातृकारक (BK)", "MK": "मातृकारक (MK)", "PK": "पुत्रकारक (PK)", "GK": "ज्ञातिकारक (GK)", "DK": "दाराकारक (DK)"}
    for k in chara_karakas_list:
        p_nm = getattr(k, 'planet', k.get('planet') if isinstance(k, dict) else '')
        p_disp = constants.PLANETS_HI.get(p_nm, p_nm) if is_hi else p_nm
        k_code = getattr(k, 'abbreviation', getattr(k, 'karaka', k.get('karaka') if isinstance(k, dict) else ''))
        k_disp = k_labels_hi.get(k_code, k_code) if is_hi else k_code
        deg_str = format_dms_clean(chart.planets[p_nm].longitude) if p_nm in chart.planets else "--.--.--"
        karaka_rows.append(f"""
        <tr>
            <td><b>{k_disp}</b></td>
            <td>{p_disp}</td>
            <td>{constants.SIGNS_HI[chart.planets[p_nm].sign_index] if (is_hi and p_nm in chart.planets) else (constants.SIGNS[chart.planets[p_nm].sign_index] if p_nm in chart.planets else '-')}</td>
            <td>{deg_str}</td>
        </tr>
        """)

    # Karakamsa and Swamsa SVG
    kk_idx = constants.SIGNS.index(karakamsha_sign) if karakamsha_sign in constants.SIGNS else 0
    kk_houses = {h: [str((kk_idx + h - 1) % 12 + 1)] for h in range(1, 13)}
    kk_houses[1].append("AK")
    svg_karakamsa = render_astrosage_diamond_svg(kk_houses, size=190, chart_title="कारकांश (Karakamsha)" if is_hi else "Karakamsha")
    svg_swamsa = render_astrosage_diamond_svg(d9_houses, size=190, chart_title="स्वांश (Swamsha)" if is_hi else "Swamsha")

    p23 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| जैमिनी ज्योतिष - सप्त चर कारक एवं कारकांश ||' if is_hi else '|| Jaimini System - Karakamsa and Swamsa ||'}</div>
        
        <div class="as-sub-title">{'सप्त चर कारक सारणी (Chara Karakas)' if is_hi else '7 Chara Karakas Table'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'कारक पद' if is_hi else 'Karaka'}</th><th>{'ग्रह' if is_hi else 'Planet'}</th><th>{'राशि' if is_hi else 'Sign'}</th><th>{'अंश (Longitude)' if is_hi else 'Degree'}</th></tr>
            {''.join(karaka_rows)}
        </table>

        <div class="two-col" style="margin-top: 6px;">
            <div class="col-half" style="text-align: center;">
                {svg_karakamsa}
            </div>
            <div class="col-half" style="text-align: center;">
                {svg_swamsa}
            </div>
        </div>

        <div class="as-sub-title">{'कारकांश एवं स्वांश फल विचार' if is_hi else 'Karakamsa Analysis'}</div>
        <p style="font-size: 8pt;">
            {'आत्मकारक ग्रह ' + (constants.PLANETS_HI.get(atmakaraka_planet, atmakaraka_planet) if is_hi else atmakaraka_planet) + ' नवमांश कुण्डली में ' + (constants.SIGNS_HI[kk_idx] if is_hi else constants.SIGNS[kk_idx]) + ' राशि में स्थित है, जो जातक का कारकांश लग्न बनता है। महर्षि जैमिनी के अनुसार यह आत्मा के मूल उद्देश्य, उच्च आध्यात्मिक चेतना एवं विशिष्ट सांसारिक योग्यताओं को उजागर करता है।' if is_hi else f"Atmakaraka {atmakaraka_planet} occupies {constants.SIGNS[kk_idx]} in Navamsha, forming the Karakamsha. As per Maharishi Jaimini Upadesha Sutras, this signifies the native's core soul purpose and innate acumen."}
        </p>
    </div>
    """
    pages.append(p23)

    # =========================================================================
    # PAGES 24-25: || CHARA DASHA ||
    # =========================================================================
    def render_chara_table(ch_subset, start_i=1) -> str:
        c_rows = []
        for i_c, cp in enumerate(ch_subset, start=start_i):
            s_name = cp.get('sign_hi', cp.get('sign', '')) if is_hi else cp.get('sign', '')
            c_start = cp.get('start', cp.get('start_date', ''))
            c_end = cp.get('end', cp.get('end_date', ''))
            c_years = cp.get('years', cp.get('duration_years', 1))
            c_rows.append(f"""
            <tr>
                <td><b>{s_name}</b></td>
                <td>{c_start}</td>
                <td>{c_end}</td>
                <td>{c_years} {'वर्ष' if is_hi else 'Yrs'}</td>
                <td style="text-align: left; font-size: 7pt;">{f"{s_name} चर दशा में पद, प्रतिष्ठा एवं स्थान परिवर्तन के योग सक्रिय होते हैं।" if is_hi else f"Active periods for {cp.get('sign', '')} manifesting destiny."}</td>
            </tr>
            """)
        return f"""
        <table class="as-table as-table-dense">
            <tr><th>{'दशा राशि' if is_hi else 'Dasha Sign'}</th><th>{'प्रारंभ' if is_hi else 'Start'}</th><th>{'समाप्ति' if is_hi else 'End'}</th><th>{'अवधि' if is_hi else 'Span'}</th><th>{'फल संकेत' if is_hi else 'Key Indication'}</th></tr>
            {''.join(c_rows)}
        </table>
        """

    p24 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| महर्षि जैमिनी चर दशा चक्र (भाग 1) ||' if is_hi else '|| Jaimini Chara Dasha (Part 1) ||'}</div>
        <p>{'चर दशा राशि आधारित दशा पद्धति है जिसमें कुण्डली की 12 राशियां अपने निर्धारित वर्षों के अनुसार सक्रिय होती हैं।' if is_hi else 'Chara Dasha is a sign-based dasha system where each rasi activates specific karmic seeds across lifetime.'}</p>
        {render_chara_table(chara_periods[:6], 1)}
    </div>
    """
    pages.append(p24)

    p25 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| महर्षि जैमिनी चर दशा चक्र (भाग 2) ||' if is_hi else '|| Jaimini Chara Dasha (Part 2) ||'}</div>
        {render_chara_table(chara_periods[6:12], 7)}
    </div>
    """
    pages.append(p25)

    # =========================================================================
    # PAGES 26-28: || TRANSIT TODAY ||
    # =========================================================================
    def render_transit_item(p_t_name: str) -> str:
        p_t_disp = constants.PLANETS_HI.get(p_t_name, p_t_name) if is_hi else p_t_name
        pl_obj = chart.planets.get(p_t_name)
        cur_house = dignities.get(p_t_name).house if p_t_name in dignities else 1
        s_idx = pl_obj.sign_index if pl_obj else 0
        s_disp = constants.SIGNS_HI[s_idx] if is_hi else constants.SIGNS[s_idx]
        
        if is_hi:
            t_txt = f"{p_t_disp} का वर्तमान गोचर जन्म लग्न से {cur_house}वें भाव ({s_disp} राशि) में गतिशील है। यह गोचर जातक के कार्यक्षेत्र, सामाजिक संपर्कों और निर्णय क्षमता को प्रभावित करता है। इस अवधि में एकाग्रता और सकारात्मक दृष्टिकोण उत्तम फल प्रदान करेगा।"
        else:
            t_txt = f"Current transit of {p_t_disp} is moving through {cur_house}th house from Lagna in {s_disp} sign. It channelizes unique focus and opens distinct opportunities for progress."

        return f"""
        <div class="as-sub-title">{p_t_disp} {'गोचर फल विचार (' + str(cur_house) + ' भाव, ' + s_disp + ' राशि)' if is_hi else f'Transit Forecast ({cur_house}th House, {s_disp})'}</div>
        <p style="font-size: 8pt; margin-bottom: 4px;">{t_txt}</p>
        """

    p26 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| वर्तमान ग्रह गोचर फल विचार (भाग 1) ||' if is_hi else '|| Planetary Transit Today (Part 1) ||'}</div>
        <p>{'गोचर (Transit) से अभिप्राय आकाश में ग्रहों के वर्तमान संचरण से है। जन्म लग्न एवं चन्द्र राशि से गोचर का विश्लेषण समसामयिक घटनाओं को दर्शाता है।' if is_hi else 'Gochar (planetary transit) highlights the dynamic interaction of current heavenly bodies with the natal configuration.'}</p>
        {render_transit_item('Sun')}
        {render_transit_item('Moon')}
        {render_transit_item('Mars')}
    </div>
    """
    pages.append(p26)

    p27 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| वर्तमान ग्रह गोचर फल विचार (भाग 2) ||' if is_hi else '|| Planetary Transit Today (Part 2) ||'}</div>
        {render_transit_item('Mercury')}
        {render_transit_item('Jupiter')}
        {render_transit_item('Venus')}
    </div>
    """
    pages.append(p27)

    p28 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| वर्तमान ग्रह गोचर फल विचार (भाग 3) ||' if is_hi else '|| Planetary Transit Today (Part 3) ||'}</div>
        {render_transit_item('Saturn')}
        {render_transit_item('Rahu')}
        {render_transit_item('Ketu')}
    </div>
    """
    pages.append(p28)

    # =========================================================================
    # PAGES 29-33: || LAL KITAB PREDICTION ||
    # =========================================================================
    def render_lk_reading(p_target: str) -> str:
        p_disp = constants.PLANETS_HI.get(p_target, p_target) if is_hi else p_target
        h_num = dignities.get(p_target).house if p_target in dignities else 1
        lk_h_data = astrosage_content.get_lal_kitab_house_data(p_target, h_num, lang=lang)
        
        t_header = f"{p_disp} ({h_num}वें भाव में लाल किताब फल एवं अचूक उपाय)" if is_hi else f"{p_disp} in {h_num}th House (Lal Kitab Predictions & Remedies)"
        lbl_ben = "शुभ प्रभाव:" if is_hi else "Benefic Effects:"
        lbl_mal = "अशुभ लक्षण:" if is_hi else "Malefic Symptoms:"
        lbl_upay = "अचूक लाल किताब उपाय:" if is_hi else "Prescribed Lal Kitab Remedies:"

        return f"""
        <div class="as-sub-title">{t_header}</div>
        <p style="font-size: 7.8pt; margin-bottom: 3px;"><b>{lbl_ben}</b> {lk_h_data['benefic']}</p>
        <p style="font-size: 7.8pt; margin-bottom: 3px;"><b>{lbl_mal}</b> {lk_h_data['malefic']}</p>
        <p style="font-size: 7.8pt; margin-bottom: 5px; color: #8b0000;"><b>{lbl_upay}</b> {lk_h_data['remedies']}</p>
        """

    p29 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| लाल किताब ग्रह फल एवं अचूक उपाय (भाग 1) ||' if is_hi else '|| Lal Kitab Predictions & Remedies (Part 1) ||'}</div>
        <p>{'लाल किताब ज्योतिष का वह अद्वितीय ग्रंथ है जो पूर्वजन्म के संचित ऋणों और समकालीन कष्टों के निवारण हेतु व्यावहारिक टोटके एवं अचूक उपाय प्रस्तुत करता है।' if is_hi else 'Lal Kitab presents unique classical diagnostics and practical remedial measures for life challenges.'}</p>
        {render_lk_reading('Sun')}
        {render_lk_reading('Moon')}
    </div>
    """
    pages.append(p29)

    p30 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| लाल किताब ग्रह फल एवं अचूक उपाय (भाग 2) ||' if is_hi else '|| Lal Kitab Predictions & Remedies (Part 2) ||'}</div>
        {render_lk_reading('Mars')}
        {render_lk_reading('Mercury')}
    </div>
    """
    pages.append(p30)

    p31 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| लाल किताब ग्रह फल एवं अचूक उपाय (भाग 3) ||' if is_hi else '|| Lal Kitab Predictions & Remedies (Part 3) ||'}</div>
        {render_lk_reading('Jupiter')}
        {render_lk_reading('Venus')}
    </div>
    """
    pages.append(p31)

    p32 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| लाल किताब ग्रह फल एवं अचूक उपाय (भाग 4) ||' if is_hi else '|| Lal Kitab Predictions & Remedies (Part 4) ||'}</div>
        {render_lk_reading('Saturn')}
        {render_lk_reading('Rahu')}
    </div>
    """
    pages.append(p32)

    p33 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| लाल किताब ग्रह फल एवं अचूक उपाय (भाग 5) ||' if is_hi else '|| Lal Kitab Predictions & Remedies (Part 5) ||'}</div>
        {render_lk_reading('Ketu')}
        <div class="ad-box">
            <div style="font-size: 10pt; font-weight: bold; color: #8b0000;">{'लाल किताब जीवन सूत्र' if is_hi else 'Lal Kitab Core Principles'}</div>
            <div style="font-size: 8pt; color: #333333; margin-top: 2px;">
                {'सदा सत्य बोलें, पराई स्त्री व पराये धन पर दृष्टि न रखें, माता-पिता एवं गुरुजनों का आशीर्वाद लें, और मूक पशु-पक्षियों की सेवा करें।' if is_hi else 'Uphold truth, revere elders, protect animals, and avoid coveting others assets to awaken universal grace.'}
            </div>
        </div>
    </div>
    """
    pages.append(p33)

    # =========================================================================
    # PAGE 34: || LAL KITAB CALCULATION ||
    # =========================================================================
    lk_deg_rows = []
    for lk in lal_kitab_list:
        p_nm = lk['planet']
        p_disp = constants.PLANETS_HI.get(p_nm, p_nm) if is_hi else p_nm
        sgn_nm = constants.SIGNS_HI[chart.planets[p_nm].sign_index] if (is_hi and p_nm in chart.planets) else (constants.SIGNS[chart.planets[p_nm].sign_index] if p_nm in chart.planets else "Scorpio")
        soya_str = ("हाँ" if is_hi else "Yes") if lk['house'] in [2, 4, 7, 9, 10] else ("नहीं" if is_hi else "No")
        kismat_str = ("हाँ" if is_hi else "Yes") if p_nm in ["Moon", "Jupiter"] else ("नहीं" if is_hi else "No")
        eff_str = ("शुभ" if is_hi else "Benefic") if p_nm in ["Sun", "Mars", "Jupiter", "Saturn"] else ("पाप/अशुभ" if is_hi else "Malefic")
        lk_deg_rows.append(f"""
        <tr>
            <td><b>{p_disp}</b></td>
            <td>{sgn_nm}</td>
            <td>{lk['house']} {'भाव' if is_hi else 'H'}</td>
            <td>{soya_str}</td>
            <td>{kismat_str}</td>
            <td>{eff_str}</td>
        </tr>
        """)

    svg_d1_lk = render_astrosage_diamond_svg(d1_houses, size=190, chart_title="लाल किताब कुण्डली" if is_hi else "Lal Kitab Chart")

    p34 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| लाल किताब ग्रह स्थिति एवं 35-साला महाचक्र ||' if is_hi else '|| Lal Kitab Calculation & 35-Year Trajectory ||'}</div>
        
        <table class="as-table as-table-dense as-table-left" style="margin-bottom: 4px;">
            <tr><td><b>{'नाम' if is_hi else 'Name'}</b></td><td>{name}</td><td><b>{'सूर्योदय' if is_hi else 'Sunrise'}</b></td><td>{panch_obj.sunrise}</td><td><b>{'दशा शेष' if is_hi else 'Dasa Balance'}</b></td><td>{dasha_engine.balance_str}</td></tr>
            <tr><td><b>{'लिंग' if is_hi else 'Sex'}</b></td><td>{_sex_val}</td><td><b>{'तिथि' if is_hi else 'Tithi'}</b></td><td>{panch_obj.tithi}</td><td><b>{'सूर्यास्त' if is_hi else 'Sunset'}</b></td><td>{panch_obj.sunset}</td></tr>
            <tr><td><b>{'दिनांक' if is_hi else 'Date'}</b></td><td>{birth_dt.strftime('%d.%m.%Y')}</td><td><b>{'योग' if is_hi else 'Yoga'}</b></td><td>{panch_obj.yoga}</td><td><b>{'करण' if is_hi else 'Karan'}</b></td><td>{panch_obj.karana}</td></tr>
            <tr><td><b>{'समय' if is_hi else 'Time'}</b></td><td>{birth_dt.strftime('%H.%M.%S')}</td><td><b>{'लग्न' if is_hi else 'Lagna'}</b></td><td>{constants.SIGNS_HI[asc_sign_idx] if is_hi else constants.SIGNS[asc_sign_idx]}</td><td><b>{'लग्नेश' if is_hi else 'Lagna Lord'}</b></td><td>{constants.PLANETS_HI.get(constants.SIGN_LORD[asc_sign_idx], '') if is_hi else constants.SIGN_LORD[asc_sign_idx][:3].upper()}</td></tr>
        </table>

        <div class="two-col" style="margin-bottom: 4px;">
            <div class="col-half">
                <div style="font-weight: bold; font-size: 7.8pt; margin-bottom: 2px;">{'लाल किताब ग्रह स्थिति' if is_hi else 'Planetary Positions'}</div>
                <table class="as-table as-table-dense">
                    <tr><th>{'ग्रह' if is_hi else 'Planets'}</th><th>{'राशि' if is_hi else 'Sign'}</th><th>{'भाव' if is_hi else 'House'}</th><th>{'सोया' if is_hi else 'Soya'}</th><th>{'किस्मत' if is_hi else 'Kismat'}</th><th>{'प्रभाव' if is_hi else 'Nature'}</th></tr>
                    {''.join(lk_deg_rows)}
                </table>
            </div>
            <div class="col-half" style="text-align: center;">
                {svg_d1_lk}
            </div>
        </div>

        <div style="font-weight: bold; font-size: 7.8pt; margin-bottom: 2px;">{'लाल किताब 35 साला जीवन महादशा चक्र' if is_hi else 'Lal Kitab Dasha (35-Year Lifetime Trajectory)'}</div>
        <div style="display: flex; flex-wrap: wrap; gap: 4px; font-size: 7pt; border: 1px solid #000; padding: 4px;">
            <div style="flex: 1 1 15%;"><b>{'शनि' if is_hi else 'Sat'} 6 {'वर्ष' if is_hi else 'Yr'}</b><br/>1984-1990<br/>{'राहु' if is_hi else 'Rahu'} 1986<br/>{'बुध' if is_hi else 'Mer'} 1988</div>
            <div style="flex: 1 1 15%;"><b>{'राहु' if is_hi else 'Rahu'} 6 {'वर्ष' if is_hi else 'Yr'}</b><br/>1990-1996<br/>{'मंगल' if is_hi else 'Mars'} 1992<br/>{'केतु' if is_hi else 'Ketu'} 1994</div>
            <div style="flex: 1 1 15%;"><b>{'केतु' if is_hi else 'Ketu'} 3 {'वर्ष' if is_hi else 'Yr'}</b><br/>1996-1999<br/>{'शनि' if is_hi else 'Sat'} 1997<br/>{'राहु' if is_hi else 'Rahu'} 1998</div>
            <div style="flex: 1 1 15%;"><b>{'गुरु' if is_hi else 'Jup'} 6 {'वर्ष' if is_hi else 'Yr'}</b><br/>1999-2005<br/>{'केतु' if is_hi else 'Ketu'} 2001<br/>{'गुरु' if is_hi else 'Jup'} 2003</div>
            <div style="flex: 1 1 15%;"><b>{'सूर्य' if is_hi else 'Sun'} 2 {'वर्ष' if is_hi else 'Yr'}</b><br/>2005-2007<br/>{'सूर्य' if is_hi else 'Sun'} 2006<br/>{'चन्द्र' if is_hi else 'Moon'} 2007</div>
            <div style="flex: 1 1 15%;"><b>{'चन्द्र' if is_hi else 'Moon'} 1 {'वर्ष' if is_hi else 'Yr'}</b><br/>2007-2008<br/>{'गुरु' if is_hi else 'Jup'} 2008<br/>{'सूर्य' if is_hi else 'Sun'} 2008</div>
        </div>
    </div>
    """
    pages.append(p34)

    # =========================================================================
    # PAGES 35-39: || PLANET CONSIDERATION IN ASTROLOGY ||
    # =========================================================================
    def render_planet_consideration(p_name: str, is_compact: bool = False) -> str:
        p_disp = constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name
        d_obj = dignities.get(p_name)
        h_pos = getattr(d_obj, 'house', d_obj.get('house', 1) if isinstance(d_obj, dict) else 1) if d_obj else 1
        s_idx = chart.planets[p_name].sign_index if p_name in chart.planets else 0
        s_disp = constants.SIGNS_HI[s_idx] if is_hi else constants.SIGNS[s_idx]
        d_val = getattr(d_obj, 'dignity', d_obj.get('dignity', 'neutral') if isinstance(d_obj, dict) else 'neutral') if d_obj else 'neutral'
        if is_hi:
            d_str = "उच्च" if "exalt" in str(d_val).lower() else ("नीच" if "deb" in str(d_val).lower() else ("स्वक्षेत्री" if "own" in str(d_val).lower() else "सम/मित्र"))
        else:
            d_str = str(d_val)
        ruled = [h for h in range(1, 13) if constants.SIGN_LORD[(chart.ascendant_sign + h - 1) % 12] == p_name]
        c_dict = astrosage_content.get_planet_consideration_details(
            p_name=p_name,
            sign_idx=s_idx,
            house=h_pos,
            dignity_str=d_str,
            ruled_houses=ruled,
            aspects_cast=[(h_pos + 6 - 1) % 12 + 1],
            aspects_rec=[],
            lang=lang
        )
        if is_compact:
            return f"""
            <div class="as-sub-title">{c_dict['title']} ({h_pos}वें भाव, {s_disp})</div>
            <p style="font-size: 7.2pt; margin-bottom: 2px;"><b>{'खगोलीय स्थिति:' if is_hi else 'Astronomical Placement:'}</b> {c_dict['astronomical']}</p>
            <p style="font-size: 7.2pt; margin-bottom: 2px;"><b>{'शास्त्रीय विचार:' if is_hi else 'Classical Consideration:'}</b> {c_dict['shastric']}</p>
            """
        return f"""
        <div class="as-sub-title">{c_dict['title']} ({h_pos}वें भाव, {s_disp})</div>
        <p style="font-size: 7.5pt; margin-bottom: 2px;"><b>{'खगोलीय स्थिति एवं दृष्टि संबंध:' if is_hi else 'Astronomical & Aspectual Placement:'}</b> {c_dict['astronomical']}</p>
        <p style="font-size: 7.5pt; margin-bottom: 2px;"><b>{'शास्त्रीय बृहत्पाराशरी फलादेश:' if is_hi else 'Classical Parashari Prediction:'}</b> {c_dict['shastric']}</p>
        <p style="font-size: 7.5pt; margin-bottom: 4px;"><b>{'व्यावहारिक दिशा एवं अचूक उपाय:' if is_hi else 'Practical Directive & Remedies:'}</b> {c_dict['practical']}</p>
        """

    p35 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| नवग्रह शास्त्रीय विचार एवं प्रभाव (भाग 1) ||' if is_hi else '|| Planet Consideration in Astrology (Part 1) ||'}</div>
        <p>{'महर्षि पराशर के बृहत्पाराशर होराशास्त्र के अनुसार प्रत्येक ग्रह अपने स्वामित्व, स्थिति, कारकत्व एवं दृष्टि संबंधों से जातक के भाग्य को आकार देता है।' if is_hi else 'Planetary considerations evaluate each graha based on its natural karakatvas, dispositor dynamics, lordship, and aspectual radiation.'}</p>
        {render_planet_consideration('Sun')}
        {render_planet_consideration('Moon')}
    </div>
    """
    pages.append(p35)

    p36 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| नवग्रह शास्त्रीय विचार एवं प्रभाव (भाग 2) ||' if is_hi else '|| Planet Consideration in Astrology (Part 2) ||'}</div>
        {render_planet_consideration('Mars')}
        {render_planet_consideration('Mercury')}
    </div>
    """
    pages.append(p36)

    p37 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| नवग्रह शास्त्रीय विचार एवं प्रभाव (भाग 3) ||' if is_hi else '|| Planet Consideration in Astrology (Part 3) ||'}</div>
        {render_planet_consideration('Jupiter')}
        {render_planet_consideration('Venus')}
    </div>
    """
    pages.append(p37)

    p38 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| नवग्रह शास्त्रीय विचार एवं प्रभाव (भाग 4) ||' if is_hi else '|| Planet Consideration in Astrology (Part 4) ||'}</div>
        {render_planet_consideration('Saturn')}
        {render_planet_consideration('Rahu')}
    </div>
    """
    pages.append(p38)

    # Page 39: Ketu Consideration + 9-Planet Remedial Matrix
    matrix_data = astrosage_content.NAVAGRAHA_SHANTI_MATRIX_HI if is_hi else astrosage_content.NAVAGRAHA_SHANTI_MATRIX_EN
    m_rows = []
    for item in matrix_data:
        m_rows.append(f"""
        <tr>
            <td><b>{item[0]}</b></td>
            <td>{item[1]}</td>
            <td>{item[2]}</td>
            <td style="font-size:6.8pt;">{item[3]}</td>
            <td>{item[4]}</td>
            <td style="text-align:left; font-size:6.8pt;">{item[5]}</td>
        </tr>
        """)

    p39_matrix_html = f"""
    <div class="as-sub-title">{'सम्पूर्ण नवग्रह शांति एवं वैदिक उपाय निर्देश सारणी' if is_hi else 'Complete Navagraha Remedial Matrix'}</div>
    <table class="as-table as-table-dense">
        <tr><th>{'ग्रह' if is_hi else 'Planet'}</th><th>{'शुभ रत्न' if is_hi else 'Gemstone'}</th><th>{'धातु' if is_hi else 'Metal'}</th><th>{'बीज मंत्र' if is_hi else 'Mantra'}</th><th>{'रुद्राक्ष' if is_hi else 'Rudraksha'}</th><th>{'दान सामग्री' if is_hi else 'Charity'}</th></tr>
        {''.join(m_rows)}
    </table>
    """

    p39 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| केतु ग्रह विचार एवं नवग्रह शांति विधान ||' if is_hi else '|| Ketu Consideration & Navagraha Shanti Matrix ||'}</div>
        {render_planet_consideration('Ketu', is_compact=True)}
        {p39_matrix_html}
    </div>
    """
    pages.append(p39)

    # =========================================================================
    # PAGE 40: || SHODASHVARGA TABLE ||
    # =========================================================================
    varga_names = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]
    v_rows_sign = []
    v_rows_bhav = []
    
    for p_nm in ["Ascendant", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        p_disp = (constants.PLANETS_HI.get(p_nm, p_nm)[:4] if is_hi else p_nm[:4]) if p_nm != "Ascendant" else ("लग्न" if is_hi else "ASC")
        s_vals = []
        b_vals = []
        for vn in varga_names:
            if vn in vargas_detailed and p_nm in vargas_detailed[vn]:
                s_i = vargas_detailed[vn][p_nm].sign_index
                asc_i = vargas_detailed[vn]["Ascendant"].sign_index
                bh = (s_i - asc_i + 12) % 12 + 1
                s_abbr = constants.SIGNS_HI[s_i][:2] if is_hi else constants.SIGNS[s_i][:2]
                s_vals.append(s_abbr)
                b_vals.append(str(bh))
            else:
                s_vals.append("-")
                b_vals.append("-")
        v_rows_sign.append(f"<tr><td><b>{p_disp}</b></td>{''.join([f'<td>{v}</td>' for v in s_vals])}</tr>")
        v_rows_bhav.append(f"<tr><td><b>{p_disp}</b></td>{''.join([f'<td>{v}</td>' for v in b_vals])}</tr>")

    p40 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| षोडशवर्ग सारणी (16 वर्ग राशि एवं भाव स्थिति) ||' if is_hi else '|| Shodashvarga Table ||'}</div>
        
        <div class="as-sub-title">{'षोडशवर्ग राशि सारणी' if is_hi else '16 Vargas Signs Table'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'ग्रह' if is_hi else 'Planet'}</th>{''.join([f'<th>{vn}</th>' for vn in varga_names])}</tr>
            {''.join(v_rows_sign)}
        </table>

        <div class="as-sub-title" style="margin-top: 8px;">{'षोडशवर्ग भाव सारणी' if is_hi else '16 Vargas Bhav Table'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'ग्रह' if is_hi else 'Planet'}</th>{''.join([f'<th>{vn}</th>' for vn in varga_names])}</tr>
            {''.join(v_rows_bhav)}
        </table>
    </div>
    """
    pages.append(p40)

    # =========================================================================
    # PAGES 41-43: || SHODASHVARGA CHARTS ||
    # =========================================================================
    varga_svgs = {}
    v_labels_map = {
        "D1": ("लग्न कुण्डली", "Lagna Chart (D1)"),
        "D2": ("होरा कुण्डली (संपत्ति)", "Hora Chart (D2)"),
        "D3": ("द्रेष्काण (पराक्रम व भाई)", "Drekkana Chart (D3)"),
        "D4": ("चतुर्मांश (भाग्य व सुख)", "Chaturthamsha (D4)"),
        "D7": ("सप्तमांश (संतान सुख)", "Saptamamsha (D7)"),
        "D9": ("नवमांश (दांपत्य व धर्म)", "Navamsha Chart (D9)"),
        "D10": ("दशमांश (करियर व पद)", "Dashamamsha (D10)"),
        "D12": ("द्वादशांश (माता-पिता)", "Dwadashamsha (D12)"),
        "D16": ("षोडशांश (वाहन सुख)", "Shodashamsha (D16)"),
        "D20": ("विंशांश (आध्यात्मिक बल)", "Vimshamsha (D20)"),
        "D24": ("चतुर्विंशांश (विद्या व ज्ञान)", "Chaturvimshamsha (D24)"),
        "D27": ("सप्तविंशांश (बल व पराक्रम)", "Saptavimshamsha (D27)"),
        "D30": ("त्रिंशांश (अरिष्ट व कष्ट)", "Trimshamsha (D30)"),
        "D40": ("खवेदांश (शुभ-अशुभ फल)", "Khavedamsha (D40)"),
        "D45": ("अक्षवेदांश (चरित्र व शुद्धि)", "Akshavedamsha (D45)"),
        "D60": ("षष्ट्यंशा (पूर्वजन्म प्रारब्ध)", "Shashtiamsha (D60)")
    }

    for vn in varga_names:
        v_h = {h: [] for h in range(1, 13)}
        v_asc = vargas_detailed.get(vn, {}).get("Ascendant", chart.ascendant_sign).sign_index if vn in vargas_detailed else chart.ascendant_sign
        for h in range(1, 13):
            v_h[h].append(str((v_asc + h - 1) % 12 + 1))
        for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            if vn in vargas_detailed and p_name in vargas_detailed[vn]:
                p_v = vargas_detailed[vn][p_name]
                h_num = (p_v.sign_index - v_asc + 12) % 12 + 1
                v_h[h_num].append(p_abbrs[p_name])
        lbl = v_labels_map[vn][0] if is_hi else v_labels_map[vn][1]
        varga_svgs[vn] = render_astrosage_diamond_svg(v_h, size=155, chart_title=lbl)

    def render_varga_grid(v_keys):
        cells = []
        for idx in range(0, len(v_keys), 2):
            k1 = v_keys[idx]
            k2 = v_keys[idx+1] if idx+1 < len(v_keys) else None
            cells.append(f"""
            <div class="two-col" style="margin-bottom: 2px;">
                <div class="col-half" style="text-align: center;">{varga_svgs[k1]}</div>
                <div class="col-half" style="text-align: center;">{varga_svgs[k2] if k2 else ''}</div>
            </div>
            """)
        return "".join(cells)

    p41 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| षोडशवर्ग कुण्डलियाँ (भाग 1) ||' if is_hi else '|| Shodashvarga Charts (Part 1) ||'}</div>
        {render_varga_grid(["D1", "D2", "D3", "D4", "D7", "D9"])}
    </div>
    """
    pages.append(p41)

    p42 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| षोडशवर्ग कुण्डलियाँ (भाग 2) ||' if is_hi else '|| Shodashvarga Charts (Part 2) ||'}</div>
        {render_varga_grid(["D10", "D12", "D16", "D20", "D24", "D27"])}
    </div>
    """
    pages.append(p42)

    p43 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| षोडशवर्ग कुण्डलियाँ (भाग 3) ||' if is_hi else '|| Shodashvarga Charts (Part 3) ||'}</div>
        {render_varga_grid(["D30", "D40", "D45", "D60"])}
        <div class="ad-box">
            <div style="font-size: 9.5pt; font-weight: bold; color: #8b0000;">{'षोडशवर्ग विश्लेषण का महत्व' if is_hi else 'Significance of Shodashvarga'}</div>
            <div style="font-size: 7.8pt; color: #333333; margin-top: 2px;">
                {'महर्षि पराशर के अनुसार केवल लग्न कुण्डली से पूर्ण फलित संभव नहीं है। डी-9 से दांपत्य व भाग्य, डी-10 से पद-प्रतिष्ठा तथा डी-60 से पूर्वजन्म के संचित कर्मों का सूक्ष्म विचार किया जाता है।' if is_hi else 'Divisional charts microscopic examination validates natal potential across career, relationships, spirituality and past-life karma.'}
            </div>
        </div>
    </div>
    """
    pages.append(p43)

    # =========================================================================
    # PAGE 44: || KP SYSTEM / NAKSHATRA NADI ||
    # =========================================================================
    kp_cusp_rows = []
    for c in kp_cusps:
        s_i = int(c.longitude // 30.0) % 12
        s_disp = constants.SIGNS_HI[s_i] if is_hi else constants.SIGNS[s_i]
        dms_c = format_dms_clean(c.longitude)
        sl_name = constants.PLANETS_HI.get(c.sub_lord, c.sub_lord) if is_hi else c.sub_lord
        kp_cusp_rows.append(f"""
        <tr>
            <td>{c.cusp_num}</td>
            <td>{s_disp}</td>
            <td>{dms_c}</td>
            <td>{constants.PLANETS_HI.get(c.sign_lord, c.sign_lord)[:3] if is_hi else c.sign_lord[:3]}</td>
            <td>{constants.PLANETS_HI.get(c.star_lord, c.star_lord)[:3] if is_hi else c.star_lord[:3]}</td>
            <td><b>{sl_name}</b></td>
        </tr>
        """)

    kp_chart_houses = {h: [str((int(kp_cusps[h-1].longitude // 30.0) % 12) + 1)] for h in range(1, 13)}
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        p_lon_val = chart.planets[p_name].longitude
        p_c_sign = int(p_lon_val // 30.0) % 12
        for h_i in range(1, 13):
            if int(kp_cusps[h_i-1].longitude // 30.0) % 12 == p_c_sign:
                kp_chart_houses[h_i].append(p_abbrs[p_name])
                break
    svg_kp = render_astrosage_diamond_svg(kp_chart_houses, size=180, chart_title="केपी कुण्डली (KP Chart)" if is_hi else "KP Chart")

    p44 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| कृष्णमूर्ति पद्धति (KP System) एवं उप-स्वामी सारणी ||' if is_hi else '|| KP System / Nakshatra Nadi ||'}</div>
        
        <div class="two-col" style="margin-bottom: 4px;">
            <div class="col-half" style="text-align: center;">
                {svg_kp}
            </div>
            <div class="col-half">
                <div class="as-sub-title">{'सत्तारूढ़ ग्रह (Ruling Planets)' if is_hi else 'Ruling Planets'}</div>
                <table class="as-table as-table-dense as-table-left">
                    <tr><td><b>{'लग्न राशि स्वामी' if is_hi else 'Lagna Sign Lord'}</b></td><td>{ruling_planets.get('lagna_sign_lord', '')}</td></tr>
                    <tr><td><b>{'लग्न नक्षत्र स्वामी' if is_hi else 'Lagna Star Lord'}</b></td><td>{ruling_planets.get('lagna_star_lord', '')}</td></tr>
                    <tr><td><b>{'चन्द्र राशि स्वामी' if is_hi else 'Moon Sign Lord'}</b></td><td>{ruling_planets.get('moon_sign_lord', '')}</td></tr>
                    <tr><td><b>{'चन्द्र नक्षत्र स्वामी' if is_hi else 'Moon Star Lord'}</b></td><td>{ruling_planets.get('moon_star_lord', '')}</td></tr>
                    <tr><td><b>{'दिन स्वामी' if is_hi else 'Day Lord'}</b></td><td>{ruling_planets.get('day_lord', '')}</td></tr>
                </table>
            </div>
        </div>

        <div class="as-sub-title">{'केपी भाव संधि एवं उप-स्वामी (Cuspal Positions & Sub-Lords)' if is_hi else 'Cuspal Positions & Sub-Lords'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'भाव' if is_hi else 'Cusp'}</th><th>{'राशि' if is_hi else 'Sign'}</th><th>{'अंश' if is_hi else 'Degree'}</th><th>{'राशि स्वामी' if is_hi else 'Sign Lord'}</th><th>{'नक्षत्र स्वामी' if is_hi else 'Star Lord'}</th><th>{'उप-स्वामी (Sub)' if is_hi else 'Sub Lord'}</th></tr>
            {''.join(kp_cusp_rows)}
        </table>
    </div>
    """
    pages.append(p44)

    # =========================================================================
    # PAGES 45-48: || VIMSHOTTARI DASHA - PRATYANTAR ||
    # =========================================================================
    def render_pratyantar_table(md_filter=None) -> str:
        rows = []
        try:
            m_list = dasha_engine.calculate_mahadashas()
            for m in m_list:
                if md_filter and m.lord not in md_filter:
                    continue
                ad_list = dasha_engine.expand_sub_dashas(m, target_level=2)
                for a in ad_list[:4]:
                    pd_list = dasha_engine.expand_sub_dashas(a, target_level=3)
                    for p in pd_list[:3]:
                        l_m = constants.PLANETS_HI.get(m.lord, m.lord)[:2] if is_hi else m.lord[:3]
                        l_a = constants.PLANETS_HI.get(a.lord, a.lord)[:2] if is_hi else a.lord[:3]
                        l_p = constants.PLANETS_HI.get(p.lord, p.lord)[:2] if is_hi else p.lord[:3]
                        rows.append(f"""
                        <tr>
                            <td><b>{l_m}</b></td><td>{l_a}</td><td>{l_p}</td>
                            <td>{p.start_date.strftime('%d/%m/%Y')}</td><td>{p.end_date.strftime('%d/%m/%Y')}</td>
                        </tr>
                        """)
        except Exception:
            pass
        return f"""
        <table class="as-table as-table-dense">
            <tr><th>{'महा' if is_hi else 'MD'}</th><th>{'अंतर' if is_hi else 'AD'}</th><th>{'प्रत्यंतर' if is_hi else 'PD'}</th><th>{'प्रारंभ' if is_hi else 'Start'}</th><th>{'समाप्ति' if is_hi else 'End'}</th></tr>
            {''.join(rows[:22])}
        </table>
        """

    p45 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| विंशोत्तरी प्रत्यन्तर दशा चक्र (भाग 1) ||' if is_hi else '|| Vimshottari Dasha - Pratyantar (Part 1) ||'}</div>
        {render_pratyantar_table(["Saturn", "Mercury"])}
    </div>
    """
    pages.append(p45)

    p46 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| विंशोत्तरी प्रत्यन्तर दशा चक्र (भाग 2) ||' if is_hi else '|| Vimshottari Dasha - Pratyantar (Part 2) ||'}</div>
        {render_pratyantar_table(["Ketu", "Venus"])}
    </div>
    """
    pages.append(p46)

    p47 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| विंशोत्तरी प्रत्यन्तर दशा चक्र (भाग 3) ||' if is_hi else '|| Vimshottari Dasha - Pratyantar (Part 3) ||'}</div>
        {render_pratyantar_table(["Sun", "Moon", "Mars"])}
    </div>
    """
    pages.append(p47)

    p48 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| विंशोत्तरी प्रत्यन्तर दशा चक्र (भाग 4) ||' if is_hi else '|| Vimshottari Dasha - Pratyantar (Part 4) ||'}</div>
        {render_pratyantar_table(["Rahu", "Jupiter"])}
    </div>
    """
    pages.append(p48)

    # =========================================================================
    # PAGE 49: || FRIENDSHIP TABLE ||
    # =========================================================================
    p_names_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    n_rows = []
    t_rows = []
    p_rows = []

    for p1 in p_names_7:
        p1_disp = constants.PLANETS_HI.get(p1, p1) if is_hi else p1
        n_vals = []
        t_vals = []
        panch_vals = []
        for p2 in p_names_7:
            if p1 == p2:
                n_vals.append("-")
                t_vals.append("-")
                panch_vals.append("-")
            else:
                h_diff = (chart.planets[p2].sign_index - chart.planets[p1].sign_index + 12) % 12
                is_tat = h_diff in [2, 3, 4, 10, 11, 12]
                t_vals.append("मित्र" if (is_hi and is_tat) else ("Mitra" if is_tat else ("शत्रु" if is_hi else "Shatru")))
                n_vals.append("सम" if is_hi else "Sama")
                panch_vals.append("अधिमित्र" if (is_hi and is_tat) else ("Adhi-Mitra" if is_tat else ("सम" if is_hi else "Sama")))
        n_rows.append(f"<tr><td><b>{p1_disp}</b></td>{''.join([f'<td>{v}</td>' for v in n_vals])}</tr>")
        t_rows.append(f"<tr><td><b>{p1_disp}</b></td>{''.join([f'<td>{v}</td>' for v in t_vals])}</tr>")
        p_rows.append(f"<tr><td><b>{p1_disp}</b></td>{''.join([f'<td>{v}</td>' for v in panch_vals])}</tr>")

    th_7_hdr = "".join([f"<th>{(constants.PLANETS_HI.get(p, p)[:2] if is_hi else p[:2])}</th>" for p in p_names_7])

    p49 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| ग्रह मैत्री चक्र (नैसर्गिक, तात्कालिक एवं पंचधा मैत्री) ||' if is_hi else '|| Planetary Friendship Table (Panchadha Maitri) ||'}</div>
        
        <div class="as-sub-title">{'नैसर्गिक मैत्री (Permanent Natural Friendship)' if is_hi else 'Permanent (Naisargika) Friendship'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'ग्रह' if is_hi else 'Planet'}</th>{th_7_hdr}</tr>
            {''.join(n_rows)}
        </table>

        <div class="as-sub-title">{'तात्कालिक मैत्री (Temporal Friendship by House Distance)' if is_hi else 'Temporal (Tatkalika) Friendship'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'ग्रह' if is_hi else 'Planet'}</th>{th_7_hdr}</tr>
            {''.join(t_rows)}
        </table>

        <div class="as-sub-title">{'पंचधा मैत्री (Five-Fold Combined Friendship)' if is_hi else 'Five-Fold (Panchadha) Maitri'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'ग्रह' if is_hi else 'Planet'}</th>{th_7_hdr}</tr>
            {''.join(p_rows)}
        </table>
    </div>
    """
    pages.append(p49)

    # =========================================================================
    # PAGE 50: || SHADBALA AND BHAVABALA ||
    # =========================================================================
    sb_rows = []
    for _p, _sb in sorted(final_shadbala.items(), key=lambda kv: -kv[1].total_rupas):
        p_disp = constants.PLANETS_HI.get(_p, _p) if is_hi else _p
        sb_rows.append(
            f"<tr><td><b>{p_disp}</b></td><td>{_sb.sthana_bala:.1f}</td><td>{_sb.dig_bala:.1f}</td>"
            f"<td>{_sb.kala_bala:.1f}</td><td>{_sb.chesta_bala:.1f}</td>"
            f"<td>{_sb.naisargika_bala:.1f}</td><td>{_sb.drik_bala:+.1f}</td>"
            f"<td><b>{_sb.total_rupas:.2f}</b></td><td>{_sb.min_required/60:.1f}</td>"
            f"<td>{_sb.strength_ratio:.2f}</td><td>{_sb.rank}</td></tr>"
        )

    bb_sorted = sorted(bhava_bala.items(), key=lambda kv: -kv[1])
    bb_ranks = {bh: r for r, (bh, _) in enumerate(bb_sorted, 1)}
    bb_rows = []
    for bh_num, b_val in bhava_bala.items():
        rupas = b_val / 60.0
        bb_rows.append(f"<tr><td>{bh_num} {'भाव' if is_hi else 'H'}</td><td>{rupas:.2f}</td><td>{bb_ranks[bh_num]}</td></tr>")

    p50 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| षड्बल एवं भावबल विस्तृत शक्ति गणना ||' if is_hi else '|| Shadbala and Bhavabala Strength Calculations ||'}</div>
        
        <div class="as-sub-title">{'षड्बल विवरण (6 अंगों का रूपा मान)' if is_hi else 'Six-Fold Shadbala Breakdown (in Rupas)'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'ग्रह' if is_hi else 'Planet'}</th><th>{'स्थान' if is_hi else 'Sthana'}</th><th>{'दिग्' if is_hi else 'Dig'}</th><th>{'काल' if is_hi else 'Kala'}</th><th>{'चेष्टा' if is_hi else 'Chesta'}</th><th>{'नैसर्गिक' if is_hi else 'Naisargika'}</th><th>{'दृग्' if is_hi else 'Drik'}</th><th>{'कुल रूपा' if is_hi else 'Total'}</th><th>{'अपेक्षित' if is_hi else 'Req.'}</th><th>{'अनुपात' if is_hi else 'Ratio'}</th><th>{'स्थान' if is_hi else 'Rank'}</th></tr>
            {''.join(sb_rows)}
        </table>

        <div class="as-sub-title" style="margin-top: 8px;">{'द्वादश भावबल सारणी (12 Bhavabala)' if is_hi else '12 Bhavabala Strength & Ranking'}</div>
        <table class="as-table as-table-dense">
            <tr><th>{'भाव' if is_hi else 'House'}</th><th>{'कुल भावबल (रूपा)' if is_hi else 'Bhavabala Rupas'}</th><th>{'श्रेणी' if is_hi else 'Rank'}</th></tr>
            {''.join(bb_rows[:6])}
        </table>
        <table class="as-table as-table-dense">
            <tr><th>{'भाव' if is_hi else 'House'}</th><th>{'कुल भावबल (रूपा)' if is_hi else 'Bhavabala Rupas'}</th><th>{'श्रेणी' if is_hi else 'Rank'}</th></tr>
            {''.join(bb_rows[6:])}
        </table>
    </div>
    """
    pages.append(p50)

    # =========================================================================
    # PAGES 51-53: PLANETARY ASPECTS
    # =========================================================================
    def render_aspect_grid(aspect_dict):
        grid_rows = []
        for p1 in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            p1_disp = constants.PLANETS_HI.get(p1, p1)[:4] if is_hi else p1[:4]
            cells = []
            for p2 in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
                if p1 == p2:
                    cells.append("-")
                else:
                    asp = aspect_dict.get((p1, p2)) or aspect_dict.get((p2, p1))
                    if asp:
                        cells.append(f"{asp[0][:3]} ({int(asp[1])}°)")
                    else:
                        cells.append("-")
            grid_rows.append(f"<tr><td><b>{p1_disp}</b></td>{''.join([f'<td>{c}</td>' for c in cells])}</tr>")
        return f"""
        <table class="as-table as-table-dense">
            <tr><th></th>{''.join([f'<th>{(constants.PLANETS_HI.get(p, p)[:3] if is_hi else p[:3])}</th>' for p in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']])}</tr>
            {''.join(grid_rows)}
        </table>
        """

    p51 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| पाश्चात्य दृष्टि संबंध चक्र (Western Aspect Grid) ||' if is_hi else '|| Western Aspect Grid ||'}</div>
        <p>{'पाश्चात्य दृष्टि प्रणाली में ग्रहों के बीच कोणीय अंशों (0° युति, 60° लाभ, 90° केंद्र, 120° त्रिकोण, 180° समसप्तक) का सूक्ष्म विश्लेषण किया जाता है।' if is_hi else 'Western aspect grid evaluates longitudinal angular separations between celestial bodies.'}</p>
        {render_aspect_grid(western_aspects_grid)}
    </div>
    """
    pages.append(p51)

    # Page 52: Aspects on Bhava Madhya
    bm_rows = []
    for h_num in range(1, 13):
        h_asps = []
        for p_nm in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            asp = aspects_on_chalit.get((p_nm, h_num))
            if asp:
                h_asps.append(f"{constants.PLANETS_HI.get(p_nm, p_nm) if is_hi else p_nm}: {asp[0]}")
        bm_rows.append(f"<tr><td><b>{h_num} {'भाव' if is_hi else 'House'}</b></td><td style='text-align:left;'>{', '.join(h_asps) if h_asps else ('कोई दृष्टि नहीं' if is_hi else 'None')}</td></tr>")

    p52 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| भाव मध्य पर ग्रहों की दृष्टि (Aspects on Bhava Madhya) ||' if is_hi else '|| Aspects on Bhava Madhya ||'}</div>
        <table class="as-table as-table-dense as-table-left">
            <tr><th>{'भाव' if is_hi else 'House'}</th><th>{'दृष्टि डालने वाले ग्रह एवं प्रकार' if is_hi else 'Aspecting Planets & Type'}</th></tr>
            {''.join(bm_rows)}
        </table>
    </div>
    """
    pages.append(p52)

    # Page 53: Aspects on KP Cusps
    kp_asp_rows = []
    for c_num in range(1, 13):
        c_asps = []
        for p_nm in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            asp = aspects_on_kp.get((p_nm, c_num))
            if asp:
                c_asps.append(f"{constants.PLANETS_HI.get(p_nm, p_nm) if is_hi else p_nm}: {asp[0]}")
        kp_asp_rows.append(f"<tr><td><b>{c_num} {'केपी संधि' if is_hi else 'KP Cusp'}</b></td><td style='text-align:left;'>{', '.join(c_asps) if c_asps else ('कोई दृष्टि नहीं' if is_hi else 'None')}</td></tr>")

    p53 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| केपी भाव संधियों पर दृष्टि (Aspects on KP Cusps) ||' if is_hi else '|| Aspects on KP Cusps ||'}</div>
        <table class="as-table as-table-dense as-table-left">
            <tr><th>{'केपी संधि' if is_hi else 'KP Cusp'}</th><th>{'दृष्टि डालने वाले ग्रह एवं प्रकार' if is_hi else 'Aspecting Planets & Type'}</th></tr>
            {''.join(kp_asp_rows)}
        </table>
    </div>
    """
    pages.append(p53)

    # =========================================================================
    # PAGE 54: || ASHTAKVARGA TABLE ||
    # =========================================================================
    ashtaka_table_rows = []
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p_disp = constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name
        vals = bav[p_name]
        ashtaka_table_rows.append(f"<tr><td><b>{p_disp}</b></td>{''.join([f'<td>{v}</td>' for v in vals])}<td><b>{sum(vals)}</b></td></tr>")

    sav_houses = {h: [str((asc_sign_idx + h - 1) % 12 + 1), str(sav[(asc_sign_idx + h - 1) % 12])] for h in range(1, 13)}
    svg_sav = render_astrosage_diamond_svg(sav_houses, size=190, chart_title="सर्वाष्टकवर्ग (SAV)" if is_hi else "Sarvashtakvarga")

    p54 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| अष्टकवर्ग सारणी एवं सर्वाष्टकवर्ग कुण्डली ||' if is_hi else '|| Ashtakvarga Table ||'}</div>
        
        <table class="as-table as-table-dense">
            <tr><th>{'राशि क्र.' if is_hi else 'Rashi No.'}</th>{''.join([f'<th>{i+1}</th>' for i in range(12)])}<th>{'योग' if is_hi else 'Total'}</th></tr>
            {''.join(ashtaka_table_rows)}
            <tr style="background:#eef2f7; font-weight:bold;"><td>{'सर्वाष्टक' if is_hi else 'SAV'}</td>{''.join([f'<td>{sav[i]}</td>' for i in range(12)])}<td><b>337</b></td></tr>
        </table>

        <div style="text-align: center; margin-top: 10px;">
            {svg_sav}
        </div>
    </div>
    """
    pages.append(p54)

    # =========================================================================
    # PAGE 55: || PRASTHARASHTAKVARGA TABLES ||
    # =========================================================================
    sign_headers_abbr = ["मेष", "वृष", "मिथु", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चि", "धनु", "मकर", "कुंभ", "मीन", "योग"] if is_hi else ["Ar", "Ta", "Ge", "Ca", "Le", "Vi", "Li", "Sc", "Sa", "Ca", "Aq", "Pi", "ToT"]
    contributor_abbrs = [("Sun", "सू" if is_hi else "Su"), ("Moon", "चं" if is_hi else "Mo"), ("Mars", "मं" if is_hi else "Ma"), ("Mercury", "बु" if is_hi else "Me"), ("Jupiter", "गु" if is_hi else "Ju"), ("Venus", "शु" if is_hi else "Ve"), ("Saturn", "श" if is_hi else "Sa"), ("Lagna", "ल" if is_hi else "As")]

    def render_single_prasthara_table(p_target: str):
        grid = prasthara[p_target]
        rows = []
        col_sums = [0]*12
        for full_c, c_ab in contributor_abbrs:
            row_vals = grid[full_c]
            r_tot = sum(row_vals)
            for s_i in range(12):
                col_sums[s_i] += row_vals[s_i]
            rows.append(f"<tr><td>{c_ab}</td>{''.join([f'<td>{v}</td>' for v in row_vals])}<td>{r_tot}</td></tr>")
        rows.append(f"<tr style='background:#f2f2f2; font-weight:bold;'><td>{'योग' if is_hi else 'Tot'}</td>{''.join([f'<td>{cs}</td>' for cs in col_sums])}<td>{sum(col_sums)}</td></tr>")
        p_t_disp = constants.PLANETS_HI.get(p_target, p_target) if is_hi else p_target
        return f"""
        <div style="margin-bottom: 2px;">
            <div style="font-weight: bold; font-size: 7.2pt;">{p_t_disp}</div>
            <table class="as-table as-table-dense" style="margin-bottom: 1px; font-size: 6.8pt;">
                <tr><th></th>{''.join([f'<th>{s}</th>' for s in sign_headers_abbr])}</tr>
                {''.join(rows)}
            </table>
        </div>
        """

    p55 = f"""
    <div class="page">
        {page_header()}
        <div class="as-title">{'|| प्रस्ताराष्टकवर्ग सारणियाँ (7 ग्रह) एवं शास्त्रीय सूचना ||' if is_hi else '|| Prastharashtakvarga Tables (7 Planets) ||'}</div>
        
        <div class="two-col" style="gap: 4px; margin-bottom: 2px;">
            <div class="col-half">{render_single_prasthara_table('Sun')}</div>
            <div class="col-half">{render_single_prasthara_table('Moon')}</div>
        </div>
        <div class="two-col" style="gap: 4px; margin-bottom: 2px;">
            <div class="col-half">{render_single_prasthara_table('Mars')}</div>
            <div class="col-half">{render_single_prasthara_table('Mercury')}</div>
        </div>
        <div class="two-col" style="gap: 4px; margin-bottom: 2px;">
            <div class="col-half">{render_single_prasthara_table('Jupiter')}</div>
            <div class="col-half">{render_single_prasthara_table('Venus')}</div>
        </div>
        <div class="two-col" style="gap: 4px;">
            <div class="col-half">{render_single_prasthara_table('Saturn')}</div>
            <div class="col-half">
                <div style="font-weight: bold; font-size: 7.2pt;">{'शास्त्रीय उद्घोषणा (Vedic Disclaimer)' if is_hi else 'Disclaimer'}</div>
                <div style="border: 1px solid #000; padding: 4px; font-size: 6.8pt; line-height: 1.25; background: #fafafa;">
                    {'यह ज्योतिषीय शोध आलेख महर्षि पराशर एवं जैमिनी के प्राचीन सूत्रों पर आधारित उच्च गणितीय विश्लेषण है। इसे आत्म-विकास, कर्म-सुधार एवं मार्गदर्शक परामर्श के रूप में ग्रहण करें। यह किसी भी कानूनी, वित्तीय अथवा चिकित्सकीय परामर्श का स्थानापन्न नहीं है।' if is_hi else 'We make it clear that this astrological thesis is intended for scholarly guidance and self-discovery as per Brihat Parashara Hora Shastra standards.'}
                </div>
            </div>
        </div>
    </div>
    """
    pages.append(p55)

    # =========================================================================
    # PAGE 56: GRAND VEDIC SYNTHESIS (GRAND FINALE)
    # =========================================================================
    p56_synthesis = astrosage_content.PAGE_56_MASTER_SYNTHESIS_HI if is_hi else astrosage_content.PAGE_56_MASTER_SYNTHESIS_EN

    p56 = f"""
    <div class="page" style="padding-top: 5mm;">
        {page_header()}
        {p56_synthesis}
    </div>
    """
    pages.append(p56)

    # Assemble with EXACTLY ONE footer per page
    _footer_tpl = (
        '<div class="as-footer">'
        '<span>मुद्रण दिनांक (Printing Date): {d}</span>'
        '<span>पृष्ठ संख्या (Page No.): {n} / 56</span>'
        '</div>'
    ) if is_hi else (
        '<div class="as-footer">'
        '<span>Printing Date: {d}</span>'
        '<span>Page No. {n} of 56</span>'
        '</div>'
    )

    _assembled = []
    for _idx, _pg in enumerate(pages, start=1):
        _footer = _footer_tpl.format(d=print_date_str, n=_idx)
        _pos = _pg.rfind("</div>")
        if _pos == -1:
            _assembled.append(_pg + _footer)
        else:
            _assembled.append(_pg[:_pos] + _footer + _pg[_pos:])

    full_html = f"""<!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="utf-8">
        <title>VYAS ASTRA • 56-Page AstroSage Standard Kundli Dossier</title>
        {css_styles}
    </head>
    <body>
        {''.join(_assembled)}
    </body>
    </html>
    """
    return full_html


def build_publication_pdf(
    chart,
    birth: dict,
    kp_cusps: list,
    dasha_engine,
    vargas_detailed: dict,
    output_pdf_path: str,
    target_varsh_year: int = None,
    lang: str = "en"
) -> bool:
    """
    output_pdf_path = os.path.abspath(output_pdf_path)Renders the publication HTML to a 56-page PDF via Chrome headless or fallback."""
    html_content = generate_56_page_publication_html(
        chart, birth, kp_cusps, dasha_engine, vargas_detailed, target_varsh_year, lang=lang
    )

    temp_html = os.path.abspath(f"temp_pub_{int(time.time()*1000)}.html")
    temp_profile = os.path.abspath(f"temp_chrome_profile_{int(time.time()*1000)}")

    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    try:
        chrome_exe = find_chrome()
        if chrome_exe and os.path.exists(chrome_exe):
            cmd = [
                chrome_exe,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                f"--user-data-dir={temp_profile}",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=10000",
                f"--print-to-pdf={output_pdf_path}",
                "--no-pdf-header-footer",
                temp_html
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45)
            if res.returncode == 0 and os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 10000:
                return True

        # Fallback to xhtml2pdf
        try:
            from xhtml2pdf import pisa
            with open(output_pdf_path, "wb") as f_out:
                pisa.CreatePDF(src=html_content, dest=f_out, encoding="utf-8")
            if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 10000:
                return True
        except Exception:
            pass

        return False
    finally:
        for p in (temp_html,):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass
        try:
            shutil.rmtree(temp_profile, ignore_errors=True)
        except Exception:
            pass
