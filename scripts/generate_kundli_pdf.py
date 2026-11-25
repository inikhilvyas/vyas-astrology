"""
VYAS ASTRA • High-Precision Forensic Vedic Astrology PDF Dossier Generator
Engine: PyMuPDF (fitz) with Devanagari Hindi Unicode & High-DPI Vector Graphics
Author: Nikhil Vyas, M.A.(Jyotish), LL.B, Pali Rajasthan
"""

import sys
import os
import json
import argparse
import fitz # PyMuPDF
from datetime import datetime

# Color Palette (Store-grade Luxury Gold & Dark Vedic Slate)
C_DARK_BG   = (15/255, 23/255, 42/255)   # #0f172a
C_GOLD      = (217/255, 119/255, 6/255)  # #d97706
C_LIGHT_GOLD= (245/255, 158/255, 11/255) # #f59e0b
C_ACCENT_BG = (248/255, 250/255, 252/255)# #f8fafc
C_CARD_BORDER=(226/255, 232/255, 240/255)# #e2e8f0
C_TEXT_DARK = (30/255, 41/255, 59/255)   # #1e293b
C_TEXT_MUTED= (100/255, 116/255, 139/255)# #64748b
C_BLUE_HDR  = (30/255, 58/255, 138/255)  # #1e3a8a
C_WHITE     = (1.0, 1.0, 1.0)
C_ROW_ALT   = (241/255, 245/255, 249/255)# #f1f5f9

def get_font_paths():
    nirmala = "C:/Windows/Fonts/nirmala.ttf"
    nirmalab = "C:/Windows/Fonts/nirmalab.ttf"
    if not os.path.exists(nirmala):
        nirmala = "C:/Windows/Fonts/mangal.ttf"
        nirmalab = "C:/Windows/Fonts/mangalb.ttf" if os.path.exists("C:/Windows/Fonts/mangalb.ttf") else nirmala
    return nirmala, nirmalab

FONT_REG, FONT_BOLD = get_font_paths()

def setup_page(doc, page_num=1, total_pages=5):
    page = doc.new_page(width=595, height=842) # A4
    page.insert_font(fontname="hindi", fontfile=FONT_REG)
    page.insert_font(fontname="hindib", fontfile=FONT_BOLD)

    # Outer decorative Vedic gold & slate border
    rect_outer = fitz.Rect(20, 20, 575, 822)
    page.draw_rect(rect_outer, color=C_GOLD, width=1.5)
    rect_inner = fitz.Rect(23, 23, 572, 819)
    page.draw_rect(rect_inner, color=C_CARD_BORDER, width=0.75)

    # Running Footer on all pages
    page.draw_line((25, 805), (570, 805), color=C_CARD_BORDER, width=0.5)
    page.insert_text((30, 815), "व्यास अस्त्र वैदिक शोध संस्थान • संस्थापक: निखिल व्यास, पाली (राज.) | Mob: 9414121172",
                     fontname="hindi", fontsize=7.5, color=C_TEXT_MUTED)
    page.insert_text((490, 815), f"पृष्ठ {page_num} of {total_pages}",
                     fontname="hindi", fontsize=7.5, color=C_TEXT_MUTED)

    return page

def draw_header_banner(page, y_start=28):
    # Top Luxury Banner Box
    banner_rect = fitz.Rect(25, y_start, 570, y_start + 68)
    page.draw_rect(banner_rect, color=C_BLUE_HDR, fill=C_DARK_BG, width=1)

    # Om Symbol & Title
    page.insert_text((40, y_start + 24), "ॐ  VYAS ASTRA • VEDIC YIELD ASTROLOGY SYSTEMS",
                     fontname="hindib", fontsize=13, color=C_LIGHT_GOLD)
    page.insert_text((40, y_start + 40), "उच्च-परिशुद्धता नासा JPL DE440s पंचांग एवं बहु-शास्त्रीय केपी/पाराशरी वेधशाला",
                     fontname="hindi", fontsize=9.5, color=C_WHITE)
    page.insert_text((40, y_start + 55), "Official Forensic Vedic & KP Astrological Dossier (Microsoft Store Edition)",
                     fontname="hindi", fontsize=8, color=(203/255, 213/255, 225/255))

    # Founder Box on Right Side of Header
    page.draw_line((380, y_start + 8), (380, y_start + 60), color=C_GOLD, width=0.8)
    page.insert_text((390, y_start + 20), "संस्थापक (Founder): निखिल व्यास",
                     fontname="hindib", fontsize=8.5, color=C_LIGHT_GOLD)
    page.insert_text((390, y_start + 33), "M.A. (ज्योतिष), LL.B | पाली (राजस्थान)",
                     fontname="hindi", fontsize=7.5, color=C_WHITE)
    page.insert_text((390, y_start + 46), "📞 9414121172 | ✉️ inikhilvyas@gmail.com",
                     fontname="hindi", fontsize=7.5, color=(226/255, 232/255, 240/255))
    page.insert_text((390, y_start + 58), "🌐 https://vyasastro.in",
                     fontname="hindi", fontsize=7.5, color=C_LIGHT_GOLD)

    return y_start + 74

def draw_section_title(page, x, y, title):
    # Decorative bullet & bar
    page.draw_rect(fitz.Rect(x, y, x + 5, y + 14), color=C_GOLD, fill=C_GOLD)
    page.insert_text((x + 12, y + 11), title, fontname="hindib", fontsize=11, color=C_BLUE_HDR)
    page.draw_line((x + 12 + len(title)*6.5, y + 8), (565, y + 8), color=C_CARD_BORDER, width=0.75)
    return y + 20

def draw_native_details(page, data, y):
    box_rect = fitz.Rect(25, y, 570, y + 68)
    page.draw_rect(box_rect, color=C_CARD_BORDER, fill=C_ACCENT_BG, width=0.8)

    name = data.get("native_name", "जातक (Native)")
    dob = f"{data.get('year', 1984)}-{data.get('month', 11):02d}-{data.get('day', 23):02d}"
    tob = f"{data.get('hour', 16):02d}:{data.get('minute', 45):02d}:{data.get('second', 0):02d}"
    place = data.get("location_name", "Pali, Rajasthan, India")
    lat = f"{data.get('latitude', 25.7711):.4f}° N"
    lon = f"{data.get('longitude', 73.3234):.4f}° E"
    tz = f"+{data.get('tz_hours', 5.5)} hrs"
    ayanamsa = f"{data.get('ayanamsa', 23.6401):.4f}° (Chitrapaksha Lahiri)"
    lagna_rashi = data.get("lagna_rashi_name", "मेष (Aries)")
    moon_rashi = data.get("moon_rashi_name", "वृश्चिक (Scorpio)")
    nakshatra = data.get("birth_nakshatra", "अनुराधा (Anuradha Pada-4)")

    # Row 1
    page.insert_text((35, y + 18), "जातक का नाम:", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    page.insert_text((105, y + 18), str(name), fontname="hindib", fontsize=9.5, color=C_BLUE_HDR)

    page.insert_text((220, y + 18), "जन्म दिनांक:", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    page.insert_text((285, y + 18), dob, fontname="hindi", fontsize=9, color=C_TEXT_DARK)

    page.insert_text((395, y + 18), "जन्म समय:", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    page.insert_text((455, y + 18), f"{tob} (TZ: {tz})", fontname="hindi", fontsize=9, color=C_TEXT_DARK)

    # Row 2
    page.insert_text((35, y + 36), "जन्म स्थान:", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    page.insert_text((105, y + 36), str(place)[:32], fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    page.insert_text((220, y + 36), "अक्षांश / रेखांश:", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    page.insert_text((285, y + 36), f"{lat}, {lon}", fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    page.insert_text((395, y + 36), "अयनांश:", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    page.insert_text((455, y + 36), ayanamsa, fontname="hindi", fontsize=8, color=C_TEXT_DARK)

    # Row 3
    page.insert_text((35, y + 54), "लग्न राशि:", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    page.insert_text((105, y + 54), lagna_rashi, fontname="hindib", fontsize=9, color=C_GOLD)

    page.insert_text((220, y + 54), "चन्द्र राशि (नाम राशि):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    page.insert_text((320, y + 54), moon_rashi, fontname="hindib", fontsize=9, color=C_BLUE_HDR)

    page.insert_text((395, y + 54), "जन्म नक्षत्र:", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    page.insert_text((455, y + 54), nakshatra, fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)

    return y + 74

def draw_north_chart(page, cx, cy, size, title, rashi_houses, planets_in_houses):
    # Diamond North Indian Chart
    half = size / 2.0
    x0, y0 = cx - half, cy - half
    x1, y1 = cx + half, cy + half

    # Background Card
    page.draw_rect(fitz.Rect(x0, y0 - 18, x1, y1), color=C_CARD_BORDER, fill=(253/255, 252/255, 248/255), width=0.8)
    page.insert_text((x0 + 8, y0 - 5), title, fontname="hindib", fontsize=9, color=C_BLUE_HDR)

    # Outer Square
    page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=C_GOLD, width=1.2)
    # Inner Diamond
    p_top = (cx, y0)
    p_right = (x1, cy)
    p_bottom = (cx, y1)
    p_left = (x0, cy)
    page.draw_line(p_top, p_right, color=C_GOLD, width=1)
    page.draw_line(p_right, p_bottom, color=C_GOLD, width=1)
    page.draw_line(p_bottom, p_left, color=C_GOLD, width=1)
    page.draw_line(p_left, p_top, color=C_GOLD, width=1)

    # Diagonals
    page.draw_line((x0, y0), (x1, y1), color=C_GOLD, width=1)
    page.draw_line((x0, y1), (x1, y0), color=C_GOLD, width=1)

    # House Center Points (North Indian Standard 1..12)
    centers = [
        (cx, cy - size*0.25),          # H1 (Lagna)
        (cx - size*0.25, cy - size*0.38),# H2
        (cx - size*0.38, cy - size*0.25),# H3
        (cx - size*0.25, cy),          # H4
        (cx - size*0.38, cy + size*0.25),# H5
        (cx - size*0.25, cy + size*0.38),# H6
        (cx, cy + size*0.25),          # H7
        (cx + size*0.25, cy + size*0.38),# H8
        (cx + size*0.38, cy + size*0.25),# H9
        (cx + size*0.25, cy),          # H10
        (cx + size*0.38, cy - size*0.25),# H11
        (cx + size*0.25, cy - size*0.38) # H12
    ]

    for h in range(12):
        px, py = centers[h]
        rashi_num = rashi_houses[h] if h < len(rashi_houses) else (h + 1)
        # Rashi number tag
        page.insert_text((px - 3, py - 12), str(rashi_num), fontname="hindib", fontsize=7.5, color=C_GOLD)
        # Planets in this house
        plist = planets_in_houses.get(h + 1, [])
        if plist:
            txt = " ".join(plist[:4])
            page.insert_text((px - len(txt)*2.5, py + 2), txt, fontname="hindib", fontsize=7.2, color=C_TEXT_DARK)
            if len(plist) > 4:
                txt2 = " ".join(plist[4:])
                page.insert_text((px - len(txt2)*2.5, py + 12), txt2, fontname="hindib", fontsize=7.2, color=C_TEXT_DARK)

def build_pdf_dossier(data, output_pdf_path):
    doc = fitz.open()
    total_pages = 5

    # --------------------------------------------------------------------------
    # PAGE 1: Master Charts (D1 & D9) & Planetary Table
    # --------------------------------------------------------------------------
    p1 = setup_page(doc, 1, total_pages)
    y = draw_header_banner(p1, 28)
    y = draw_section_title(p1, 25, y, "१. जातक विवरण एवं जन्म कुण्डली (Native Profile & Core Charts)")
    y = draw_native_details(p1, data, y)

    # Compute North Indian Rashi numbers per house for D1 & D9
    lagna_rashi = data.get("lagna_rashi_num", 1) # 1..12
    d1_rashis = [((lagna_rashi - 1 + h) % 12) + 1 for h in range(12)]

    navamsha_lagna = data.get("navamsha_lagna_num", 1)
    d9_rashis = [((navamsha_lagna - 1 + h) % 12) + 1 for h in range(12)]

    d1_planets = data.get("d1_house_planets", {})
    d9_planets = data.get("d9_house_planets", {})

    # Draw D1 and D9 Charts side by side
    chart_y = y + 115
    draw_north_chart(p1, 160, chart_y, 220, "D1 • लग्न कुण्डली (Lagna Rashi Chart)", d1_rashis, d1_planets)
    draw_north_chart(p1, 435, chart_y, 220, "D9 • नवांश कुण्डली (Navamsha D9 Chart)", d9_rashis, d9_planets)

    # Planetary Positions Table on Bottom of Page 1
    table_y = chart_y + 120
    draw_section_title(p1, 25, table_y, "२. ग्रह स्थिति एवं नवांश स्पष्ट (Planetary Positions & Dignity)")

    headers = ["ग्रह (Graha)", "स्पष्ट अंश (Degree)", "राशि (Sign)", "भाव", "नक्षत्र (Pada)", "स्वामी", "अवस्था", "बल (Dignity)", "जैमिनी कारक"]
    col_w   = [65, 80, 55, 30, 85, 45, 65, 75, 70]
    tx_start = 25
    ty = table_y + 22

    # Draw Header Row
    page_hdr_rect = fitz.Rect(tx_start, ty, tx_start + sum(col_w), ty + 16)
    p1.draw_rect(page_hdr_rect, color=C_BLUE_HDR, fill=C_BLUE_HDR)
    cx = tx_start
    for idx, htext in enumerate(headers):
        p1.insert_text((cx + 3, ty + 12), htext, fontname="hindib", fontsize=7.5, color=C_WHITE)
        cx += col_w[idx]
    ty += 16

    planets_data = data.get("planets_table", [])
    for row_idx, pl in enumerate(planets_data):
        row_rect = fitz.Rect(tx_start, ty, tx_start + sum(col_w), ty + 14)
        bg = C_ROW_ALT if (row_idx % 2 == 1) else C_WHITE
        p1.draw_rect(row_rect, color=C_CARD_BORDER, fill=bg, width=0.4)

        vals = [
            pl.get("name", ""),
            pl.get("degree", ""),
            pl.get("rashi", ""),
            str(pl.get("house", "")),
            pl.get("nakshatra", ""),
            pl.get("lord", ""),
            pl.get("awastha", ""),
            pl.get("dignity", ""),
            pl.get("karaka", "")
        ]
        cx = tx_start
        for cidx, val in enumerate(vals):
            col_color = C_GOLD if cidx == 0 else C_TEXT_DARK
            p1.insert_text((cx + 3, ty + 10.5), str(val)[:18], fontname="hindi", fontsize=7.2, color=col_color)
            cx += col_w[cidx]
        ty += 14

    # --------------------------------------------------------------------------
    # PAGE 2: Complete Panchang, Muhurtas, Avakhada Chakra & Ashtakavarga 337
    # --------------------------------------------------------------------------
    p2 = setup_page(doc, 2, total_pages)
    y = draw_header_banner(p2, 28)

    y = draw_section_title(p2, 25, y, "३. दैनिक पंचांग विवरण एवं जन्म अवकहड़ा चक्र (Panchang & Avakhada)")
    pan = data.get("panchang", {})
    pan_rect = fitz.Rect(25, y, 570, y + 80)
    p2.draw_rect(pan_rect, color=C_CARD_BORDER, fill=C_ACCENT_BG, width=0.8)

    p2.insert_text((35, y + 16), "तिथि (Tithi):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p2.insert_text((115, y + 16), pan.get("tithi", "प्रतिपदा (शुक्ल पक्ष)"), fontname="hindi", fontsize=8.5, color=C_BLUE_HDR)

    p2.insert_text((220, y + 16), "वार (Weekday):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p2.insert_text((300, y + 16), pan.get("vaar", "शुक्रवार (Friday)"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p2.insert_text((395, y + 16), "नक्षत्र (Star):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p2.insert_text((475, y + 16), pan.get("nakshatra", "अनुराधा"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p2.insert_text((35, y + 34), "योग (Yoga):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p2.insert_text((115, y + 34), pan.get("yoga", "सुकर्मा"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p2.insert_text((220, y + 34), "करण (Karana):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p2.insert_text((300, y + 34), pan.get("karana", "बव"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p2.insert_text((395, y + 34), "सूर्योदय / सूर्यास्त:", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p2.insert_text((475, y + 34), f"{pan.get('sunrise', '06:48 AM')} / {pan.get('sunset', '05:42 PM')}", fontname="hindi", fontsize=8, color=C_TEXT_DARK)

    # Avakhada Chakra
    avak = data.get("avakhada", {})
    p2.draw_line((35, y + 46), (560, y + 46), color=C_CARD_BORDER, width=0.5)
    p2.insert_text((35, y + 62), f"वर्ण: {avak.get('varna', 'Brahmin')}  |  वश्य: {avak.get('vashya', 'Keet')}  |  योनि: {avak.get('yoni', 'Mrig')}  |  गण: {avak.get('gana', 'Deva')}  |  नाड़ी: {avak.get('nadi', 'Madhya')}  |  तत्व: {avak.get('tattva', 'Jal (जल)')}",
                   fontname="hindi", fontsize=8, color=C_TEXT_DARK)
    y += 90

    # Auspicious & Inauspicious Muhurtas
    y = draw_section_title(p2, 25, y, "४. शुभ एवं अशुभ मुहूर्त (Auspicious & Inauspicious Timings)")
    muh = data.get("muhurtas", {})
    muh_rect = fitz.Rect(25, y, 570, y + 55)
    p2.draw_rect(muh_rect, color=C_CARD_BORDER, fill=C_WHITE, width=0.8)

    p2.insert_text((35, y + 18), "⭐ अभिजीत मुहूर्त:", fontname="hindib", fontsize=8.5, color=(16/255, 120/255, 50/255))
    p2.insert_text((125, y + 18), muh.get("abhijit", "11:46 AM से 12:32 PM"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p2.insert_text((300, y + 18), "⭐ ब्रह्म मुहूर्त:", fontname="hindib", fontsize=8.5, color=(16/255, 120/255, 50/255))
    p2.insert_text((380, y + 18), muh.get("brahma", "05:08 AM से 05:58 AM"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p2.insert_text((35, y + 38), "⚠️ राहु काल (वर्जित):", fontname="hindib", fontsize=8.5, color=(185/255, 28/255, 28/255))
    p2.insert_text((125, y + 38), muh.get("rahu_kaal", "10:30 AM से 12:00 PM"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p2.insert_text((300, y + 38), "⚠️ यमघण्ट काल:", fontname="hindib", fontsize=8.5, color=(185/255, 28/255, 28/255))
    p2.insert_text((380, y + 38), muh.get("yamaganda", "09:30 AM से 11:00 AM"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)
    y += 65

    # Ashtakavarga 337 Matrix Table
    y = draw_section_title(p2, 25, y, "५. सम्पूर्ण अष्टकवर्ग सारणी (337 बिन्दु परीक्षण एवं भाव सामर्थ्य)")
    ashtak_headers = ["ग्रह", "१", "२", "३", "४", "५", "६", "७", "८", "९", "१०", "११", "१२", "योग"]
    a_col_w = [65, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 49]
    a_tx = 25
    a_ty = y

    # Header Row
    p2.draw_rect(fitz.Rect(a_tx, a_ty, a_tx + sum(a_col_w), a_ty + 16), color=C_BLUE_HDR, fill=C_BLUE_HDR)
    cx = a_tx
    for idx, ah in enumerate(ashtak_headers):
        p2.insert_text((cx + 6, a_ty + 12), ah, fontname="hindib", fontsize=8, color=C_WHITE)
        cx += a_col_w[idx]
    a_ty += 16

    ashtak_rows = data.get("ashtakavarga_rows", [])
    for ridx, arow in enumerate(ashtak_rows):
        is_sav = (ridx == len(ashtak_rows) - 1)
        row_bg = (254/255, 243/255, 199/255) if is_sav else (C_ROW_ALT if ridx % 2 == 1 else C_WHITE)
        p2.draw_rect(fitz.Rect(a_tx, a_ty, a_tx + sum(a_col_w), a_ty + 14), color=C_CARD_BORDER, fill=row_bg, width=0.4)

        cx = a_tx
        fname = "hindib" if is_sav else "hindi"
        fcolor = C_GOLD if is_sav else C_TEXT_DARK
        for cidx, val in enumerate(arow):
            p2.insert_text((cx + 6, a_ty + 10.5), str(val), fontname=fname, fontsize=7.5, color=fcolor)
            cx += a_col_w[cidx]
        a_ty += 14

    # --------------------------------------------------------------------------
    # PAGE 3: KP Sub-Lord System, 5-Level Hierarchy & Jaimini Karakas
    # --------------------------------------------------------------------------
    p3 = setup_page(doc, 3, total_pages)
    y = draw_header_banner(p3, 28)

    y = draw_section_title(p3, 25, y, "६. केपी कृष्णमूर्ति पद्धति (12 Cuspal Sub-Lords & 5-Level Hierarchy)")

    kp_headers = ["भाव (Cusp)", "आरम्भ अंश (Cusp Degree)", "राशि (Sign)", "राशि स्वामी", "नक्षत्र स्वामी (Star)", "उप-स्वामी (Sub-Lord)", "उप-उप स्वामी (SSL)"]
    kp_col_w = [55, 95, 75, 75, 85, 95, 90]
    k_tx = 25
    k_ty = y

    p3.draw_rect(fitz.Rect(k_tx, k_ty, k_tx + sum(kp_col_w), k_ty + 16), color=C_BLUE_HDR, fill=C_BLUE_HDR)
    cx = k_tx
    for idx, kh in enumerate(kp_headers):
        p3.insert_text((cx + 4, k_ty + 12), kh, fontname="hindib", fontsize=7.5, color=C_WHITE)
        cx += kp_col_w[idx]
    k_ty += 16

    kp_rows = data.get("kp_cusps_table", [])
    for ridx, krow in enumerate(kp_rows):
        bg = C_ROW_ALT if ridx % 2 == 1 else C_WHITE
        p3.draw_rect(fitz.Rect(k_tx, k_ty, k_tx + sum(kp_col_w), k_ty + 14), color=C_CARD_BORDER, fill=bg, width=0.4)
        cx = k_tx
        for cidx, val in enumerate(krow):
            fcolor = C_GOLD if cidx == 0 or cidx == 5 else C_TEXT_DARK
            p3.insert_text((cx + 4, k_ty + 10.5), str(val), fontname="hindi", fontsize=7.2, color=fcolor)
            cx += kp_col_w[cidx]
        k_ty += 14

    y = k_ty + 20

    # Jaimini & Advanced System Box
    y = draw_section_title(p3, 25, y, "७. जैमिनी ज्योतिष एवं गुप्त कारक (Jaimini Chara Karakas & Arudhas)")
    jaimini_rect = fitz.Rect(25, y, 570, y + 105)
    p3.draw_rect(jaimini_rect, color=C_CARD_BORDER, fill=C_ACCENT_BG, width=0.8)

    jm = data.get("jaimini_info", {})
    p3.insert_text((35, y + 18), "आत्मकारक (AK):", fontname="hindib", fontsize=8.5, color=C_GOLD)
    p3.insert_text((120, y + 18), jm.get("ak", "बुध (Mercury) - आत्मा व जीवन का मुख्य उद्देश्य"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p3.insert_text((35, y + 36), "अमात्यकारक (AmK):", fontname="hindib", fontsize=8.5, color=C_BLUE_HDR)
    p3.insert_text((120, y + 36), jm.get("amk", "शनि (Saturn) - आजीविका, कर्म व अधिकार"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p3.insert_text((35, y + 54), "भ्रातृकारक (BK):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p3.insert_text((120, y + 54), jm.get("bk", "गुरु (Jupiter) - पराक्रम व मार्गदर्शक"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p3.insert_text((35, y + 72), "मातृकारक (MK):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p3.insert_text((120, y + 72), jm.get("mk", "शुक्र (Venus) - सुख, वाहन व माता"), fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    p3.insert_text((35, y + 90), "आरूढ़ लग्न (AL):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p3.insert_text((120, y + 90), f"{jm.get('al', 'कर्क (Cancer)')}  |  उपपद लग्न (UL): {jm.get('ul', 'वृषभ (Taurus)')}  |  कारकांश लग्न: {jm.get('kl', 'धनु (Sagittarius)')}",
                   fontname="hindi", fontsize=8.5, color=C_TEXT_DARK)

    # --------------------------------------------------------------------------
    # PAGE 4: 5-Tier Vimshottari Dasha Hierarchy
    # --------------------------------------------------------------------------
    p4 = setup_page(doc, 4, total_pages)
    y = draw_header_banner(p4, 28)

    y = draw_section_title(p4, 25, y, "८. विंशोत्तरी दशा प्रणाली (5-Tier Running Dasha & Lifetime Trajectory)")

    dasha = data.get("dasha_info", {})
    d_box = fitz.Rect(25, y, 570, y + 75)
    p4.draw_rect(d_box, color=C_GOLD, fill=C_DARK_BG, width=1)

    p4.insert_text((35, y + 20), "⚡ वर्तमान सक्रिय प्राण दशा तक (Active 5-Tier Running Dasha):",
                   fontname="hindib", fontsize=9.5, color=C_LIGHT_GOLD)

    running_dasha = dasha.get("running_dasha_full", "महादशा: शुक्र (Venus) > अन्तर्दशा: गुरु (Jupiter) > प्रत्यन्तर: शनि (Saturn) > सूक्ष्म: बुध (Mercury) > प्राण दशा: केतु (Ketu)")
    p4.insert_text((35, y + 42), running_dasha, fontname="hindib", fontsize=8.5, color=C_WHITE)

    balance_txt = dasha.get("birth_balance", "जन्म के समय विंशोत्तरी शेष: शनि (Saturn) - 3 वर्ष 0 माह 2 दिन")
    p4.insert_text((35, y + 62), balance_txt, fontname="hindi", fontsize=8.5, color=(203/255, 213/255, 225/255))
    y += 85

    # 120-Year Mahadasha Trajectory Table
    y = draw_section_title(p4, 25, y, "९. जीवन पर्यन्त 120 वर्षीय महादशा एवं अन्तर्दशा काल-क्रम")

    dt_headers = ["महादशा (Mahadasha)", "ग्रह अवधि (Years)", "प्रारम्भ तिथि (Start Date)", "समाप्ति तिथि (End Date)", "जीवन प्रभाव व फलादेश संक्षेप"]
    dt_col_w = [100, 75, 95, 95, 205]
    d_tx = 25
    d_ty = y

    p4.draw_rect(fitz.Rect(d_tx, d_ty, d_tx + sum(dt_col_w), d_ty + 16), color=C_BLUE_HDR, fill=C_BLUE_HDR)
    cx = d_tx
    for idx, dh in enumerate(dt_headers):
        p4.insert_text((cx + 4, d_ty + 12), dh, fontname="hindib", fontsize=7.5, color=C_WHITE)
        cx += dt_col_w[idx]
    d_ty += 16

    dasha_table_rows = dasha.get("lifetime_rows", [])
    for ridx, drow in enumerate(dasha_table_rows):
        is_active = drow.get("active", False)
        bg = (254/255, 243/255, 199/255) if is_active else (C_ROW_ALT if ridx % 2 == 1 else C_WHITE)
        p4.draw_rect(fitz.Rect(d_tx, d_ty, d_tx + sum(dt_col_w), d_ty + 18), color=C_CARD_BORDER, fill=bg, width=0.4)

        cx = d_tx
        fname = "hindib" if is_active else "hindi"
        fcolor = C_GOLD if is_active else C_TEXT_DARK
        vals = [
            drow.get("lord", ""),
            f"{drow.get('years', '')} वर्ष",
            drow.get("start", ""),
            drow.get("end", ""),
            drow.get("summary", "")
        ]
        for cidx, val in enumerate(vals):
            p4.insert_text((cx + 4, d_ty + 12), str(val)[:45], fontname=fname, fontsize=7.5, color=fcolor)
            cx += dt_col_w[cidx]
        d_ty += 18

    # --------------------------------------------------------------------------
    # PAGE 5: Forensic Verdict, Sutras & 3-Tier Satvik Remedies
    # --------------------------------------------------------------------------
    p5 = setup_page(doc, 5, total_pages)
    y = draw_header_banner(p5, 28)

    y = draw_section_title(p5, 25, y, "१०. दैवज्ञ निर्णय एवं शास्त्रीय सूत्र (Forensic Classical Verdict)")

    verdict_text = data.get("verdict_text", "")
    lines = verdict_text.split("\n")
    cur_y = y
    for line in lines:
        line = line.strip()
        if not line:
            cur_y += 5
            continue
        if cur_y > 440:
            break
        if line.startswith("🎯") or line.startswith("🔍") or line.startswith("⚡") or line.startswith("⏱️") or line.startswith("---"):
            p5.insert_text((28, cur_y + 11), line[:95], fontname="hindib", fontsize=8.5, color=C_BLUE_HDR)
            cur_y += 15
        else:
            p5.insert_text((35, cur_y + 10), line[:110], fontname="hindi", fontsize=7.5, color=C_TEXT_DARK)
            cur_y += 13

    # 3-Tier Satvik Remedies Box
    rem_y = 450
    draw_section_title(p5, 25, rem_y, "११. अचूक 3-स्तरीय सात्विक वैदिक उपाय (Three-Tier Satvik Remedies)")

    rem_box = fitz.Rect(25, rem_y + 18, 570, 785)
    p5.draw_rect(rem_box, color=C_GOLD, fill=C_ACCENT_BG, width=0.8)

    ry = rem_y + 35
    p5.insert_text((35, ry), "प्रथम स्तर: मनोवैज्ञानिक व कर्म बोध (Tier 1: Cognitive Karmic Understanding):",
                   fontname="hindib", fontsize=8.5, color=C_GOLD)
    t1 = data.get("remedy_t1", "अपनी मूल ऊर्जा को पहचानें। दशम व नवम भाव के संरेखण अनुसार सेवा भाव एवं अनुशासन में वृद्धि करें।")
    p5.insert_text((45, ry + 15), t1[:105], fontname="hindi", fontsize=8, color=C_TEXT_DARK)

    ry += 40
    p5.insert_text((35, ry), "द्वितीय स्तर: दैनिक सात्विक आचरण व लाल किताब सूत्र (Tier 2: Behavioral Habits):",
                   fontname="hindib", fontsize=8.5, color=C_BLUE_HDR)
    t2 = data.get("remedy_t2", "प्रतिदिन सूर्योदय के समय गायत्री मंत्र का मानसिक जप करें। पक्षियों को जल व सप्तधान्य अर्पित करें।")
    p5.insert_text((45, ry + 15), t2[:105], fontname="hindi", fontsize=8, color=C_TEXT_DARK)

    ry += 40
    p5.insert_text((35, ry), "तृतीय स्तर: वैदिक बीज मंत्र एवं सात्विक दान (Tier 3: Energetic Prescription):",
                   fontname="hindib", fontsize=8.5, color=(16/255, 120/255, 50/255))
    t3 = data.get("remedy_t3", "वैदिक बीज मंत्र: ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः (108 बार नित्य जप)। शनिवार को काले तिल व तेल का छाया दान करें।")
    p5.insert_text((45, ry + 15), t3[:105], fontname="hindi", fontsize=8, color=C_TEXT_DARK)

    # Signature and Stamp Box
    ry += 55
    p5.draw_line((35, ry), (560, ry), color=C_CARD_BORDER, width=0.5)
    p5.insert_text((35, ry + 20), "प्रमाणीकरण मुहर (Certified Astrological Seal):", fontname="hindib", fontsize=8.5, color=C_TEXT_DARK)
    p5.insert_text((35, ry + 35), "व्यास अस्त्र डिजिटल हस्ताक्षर द्वारा अधिकृत • अपरिवर्तनीय खगोलीय गणना", fontname="hindi", fontsize=7.5, color=C_TEXT_MUTED)

    p5.insert_text((400, ry + 20), "आचार्य निखिल व्यास", fontname="hindib", fontsize=10, color=C_GOLD)
    p5.insert_text((400, ry + 34), "M.A. (ज्योतिष), LL.B, पाली (राज.)", fontname="hindi", fontsize=8, color=C_TEXT_DARK)
    p5.insert_text((400, ry + 46), "फ़ोन: 9414121172 | inikhilvyas@gmail.com", fontname="hindi", fontsize=7.5, color=C_TEXT_MUTED)

    # Save Document
    doc.save(output_pdf_path)
    doc.close()
    print(f"SUCCESS: Generated 5-Page Dossier PDF at {output_pdf_path}")
    return output_pdf_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate VYAS Astra Kundli PDF Dossier")
    parser.add_argument("--input", "-i", type=str, required=True, help="Input JSON path")
    parser.add_argument("--output", "-o", type=str, default="VYAS_Kundli_Mahapatrika.pdf", help="Output PDF path")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        kundli_data = json.load(f)

    build_pdf_dossier(kundli_data, args.output)

