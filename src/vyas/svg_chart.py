"""North Indian and South Indian Vedic Chart SVG Generator with Large, High-Contrast Typography.

Renders crisp, high-resolution SVG astrological charts with:
- Outer rectangular frame with golden/ruby styling
- Classical diagonal and diamond line geometry
- Large, bold House numbers / Sign numbers (15-16px) with vibrant contrast circles
- Large, crystal-clear Planetary glyphs (13.5-15px) with exact Degree & Minute
- Smart multi-line layout so multiple planets in a single house remain completely legible
"""
import re
from typing import Dict, List, Tuple


def _clean_svg(svg_str: str) -> str:
    """Strip HTML comments and collapse multiple whitespace/newlines to single space."""
    clean = re.sub(r'<!--.*?-->', '', svg_str, flags=re.DOTALL)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def get_north_indian_chart_svg(houses_data: dict, size: int = 500, chart_title: str = "") -> str:
    """
    Generates an SVG string for a North Indian style astrology chart with large, readable fonts.
    houses_data: Dict[int, list] where keys are 1-12 (houses).
                 First item in list is the sign number (string).
                 Subsequent items are planet strings, optionally with degrees (e.g. 'Su 07°42\'').
    """
    s = max(size, 480)
    h = s / 2.0
    q = s / 4.0
    
    parts = [
        f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        '<linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#0c1427"/>',
        '<stop offset="50%" stop-color="#060a15"/>',
        '<stop offset="100%" stop-color="#020409"/>',
        '</linearGradient>',
        '<linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#fcedaa"/>',
        '<stop offset="50%" stop-color="#d4af37"/>',
        '<stop offset="100%" stop-color="#9a7b1c"/>',
        '</linearGradient>',
        '<filter id="textShadow">',
        '<feDropShadow dx="0" dy="1" stdDeviation="1.5" flood-color="#000000" flood-opacity="0.9"/>',
        '</filter>',
        '</defs>',
        f'<rect x="0" y="0" width="{s}" height="{s}" fill="url(#bgGrad)" stroke="url(#goldGrad)" stroke-width="3" rx="12"/>',
        f'<rect x="7" y="7" width="{s-14}" height="{s-14}" fill="none" stroke="#d4af37" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="6,3" rx="8"/>',
        f'<rect x="12" y="12" width="{s-24}" height="{s-24}" fill="none" stroke="#d4af37" stroke-width="0.5" stroke-opacity="0.3"/>'
    ]
    
    # Diagonals and inner diamond (Gold lines)
    lines = [
        (0, 0, s, s),
        (0, s, s, 0),
        (h, 0, s, h),
        (s, h, h, s),
        (h, s, 0, h),
        (0, h, h, 0)
    ]
    for x1, y1, x2, y2 in lines:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4af37" stroke-width="1.8" stroke-opacity="0.9"/>')
        
    # House center coordinates (optimized for large font breathing room)
    positions = {
        1: (h, q - 6),
        2: (q, q/2 + 2),
        3: (q/2 + 10, q + 6),
        4: (q + 4, h),
        5: (q/2 + 10, s - q - 6),
        6: (q, s - q/2 - 2),
        7: (h, s - q + 14),
        8: (s - q, s - q/2 - 2),
        9: (s - q/2 - 10, s - q - 6),
        10: (s - q - 4, h),
        11: (s - q/2 - 10, q + 6),
        12: (s - q, q/2 + 2)
    }
    
    for house, pos in positions.items():
        x, y = pos
        data = houses_data.get(house, [])
        if not data:
            continue
            
        sign_num = str(data[0])
        planets = data[1:]
        count = len(planets)
        
        # Position the Sign number badge with large font and high-contrast circle
        if house in (6, 8):
            sign_y = y - 30
        elif house in (2, 12):
            sign_y = y - 26
        elif house == 1:
            sign_y = y - 32
        elif house == 7:
            sign_y = y - 28
        else:
            sign_y = y - 25
            
        parts.append(f'<circle cx="{x}" cy="{sign_y}" r="12.5" fill="#320606" stroke="#ef4444" stroke-width="1.4" stroke-opacity="0.95"/>')
        parts.append(f'<text x="{x}" y="{sign_y + 5.5}" font-family="Cinzel, Georgia, serif" font-size="16" font-weight="900" fill="#fca5a5" text-anchor="middle" filter="url(#textShadow)">{sign_num}</text>')
        
        # Draw planets with large, bold, crystal-clear typography (2-column balanced layout for 3+ planets)
        if count == 0:
            continue
        elif count <= 2:
            font_sz = "16.5" if count == 1 else "15.5"
            line_spacing = 22
            start_y = (y + 10) if count == 1 else (y + 2)
            for idx, p_text in enumerate(planets):
                p_y = start_y + (idx * line_spacing)
                is_retro = "(R)" in p_text or "(व)" in p_text
                color = "#fb923c" if is_retro else "#ffffff"
                weight = "900" if is_retro else "800"
                parts.append(f'<text x="{x}" y="{p_y}" font-family="Noto Sans Devanagari, Plus Jakarta Sans, Arial, sans-serif" font-size="{font_sz}" font-weight="{weight}" fill="{color}" text-anchor="middle" letter-spacing="0.3px" filter="url(#textShadow)">{p_text}</text>')
        elif count in (3, 4):
            # 2-column layout so multi-planet conjunctions never get squeezed into corners
            font_sz = "15"
            x_offset = 36
            y_start = y + 2
            row_spacing = 22
            for idx, p_text in enumerate(planets):
                col_idx = idx % 2
                row_idx = idx // 2
                p_x = (x - x_offset) if col_idx == 0 else (x + x_offset)
                p_y = y_start + (row_idx * row_spacing)
                is_retro = "(R)" in p_text or "(व)" in p_text
                color = "#fb923c" if is_retro else "#ffffff"
                weight = "900" if is_retro else "800"
                parts.append(f'<text x="{p_x}" y="{p_y}" font-family="Noto Sans Devanagari, Plus Jakarta Sans, Arial, sans-serif" font-size="{font_sz}" font-weight="{weight}" fill="{color}" text-anchor="middle" letter-spacing="0.2px" filter="url(#textShadow)">{p_text}</text>')
        else:
            font_sz = "13.5"
            x_offset = 35
            y_start = y - 4
            row_spacing = 18
            for idx, p_text in enumerate(planets):
                col_idx = idx % 2
                row_idx = idx // 2
                p_x = (x - x_offset) if col_idx == 0 else (x + x_offset)
                p_y = y_start + (row_idx * row_spacing)
                is_retro = "(R)" in p_text or "(व)" in p_text
                color = "#fb923c" if is_retro else "#ffffff"
                weight = "900" if is_retro else "800"
                parts.append(f'<text x="{p_x}" y="{p_y}" font-family="Noto Sans Devanagari, Plus Jakarta Sans, Arial, sans-serif" font-size="{font_sz}" font-weight="{weight}" fill="{color}" text-anchor="middle" letter-spacing="0.2px" filter="url(#textShadow)">{p_text}</text>')

    if chart_title:
        title_w = min(s - 40, max(280, len(chart_title) * 11))
        parts.append(f'<rect x="{h - title_w/2}" y="10" width="{title_w}" height="28" rx="14" fill="#0b1326" stroke="#d4af37" stroke-width="1.2" stroke-opacity="0.9"/>')
        parts.append(f'<text x="{h}" y="29" font-family="Noto Sans Devanagari, Cinzel, serif" font-size="14" font-weight="900" fill="#f0c05a" text-anchor="middle" letter-spacing="0.8px" filter="url(#textShadow)">{chart_title}</text>')

    parts.append('</svg>')
    return _clean_svg("".join(parts))


def get_north_indian_chart_svg_print(houses_data: dict, size: int = 480, chart_title: str = "") -> str:
    """
    Generates a high-contrast publication-grade SVG for print / PDF with white background,
    crisp ruby/crimson geometry, and large dark typography.
    """
    s = max(size, 460)
    h = s / 2.0
    q = s / 4.0
    
    parts = [
        f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect x="0" y="0" width="{s}" height="{s}" fill="#ffffff" stroke="#990000" stroke-width="2.5" rx="6"/>',
        f'<rect x="5" y="5" width="{s-10}" height="{s-10}" fill="none" stroke="#b30000" stroke-width="1" stroke-opacity="0.6"/>'
    ]
    
    lines = [
        (0, 0, s, s),
        (0, s, s, 0),
        (h, 0, s, h),
        (s, h, h, s),
        (h, s, 0, h),
        (0, h, h, 0)
    ]
    for x1, y1, x2, y2 in lines:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#b30000" stroke-width="1.6"/>')
        
    positions = {
        1: (h, q - 6),
        2: (q, q/2 + 2),
        3: (q/2 + 10, q + 6),
        4: (q + 4, h),
        5: (q/2 + 10, s - q - 6),
        6: (q, s - q/2 - 2),
        7: (h, s - q + 14),
        8: (s - q, s - q/2 - 2),
        9: (s - q/2 - 10, s - q - 6),
        10: (s - q - 4, h),
        11: (s - q/2 - 10, q + 6),
        12: (s - q, q/2 + 2)
    }
    
    for house, pos in positions.items():
        x, y = pos
        data = houses_data.get(house, [])
        if not data:
            continue
            
        sign_num = str(data[0])
        planets = data[1:]
        count = len(planets)
        
        if house in (6, 8):
            sign_y = y - 30
        elif house in (2, 12):
            sign_y = y - 26
        elif house == 1:
            sign_y = y - 32
        elif house == 7:
            sign_y = y - 28
        else:
            sign_y = y - 25
            
        parts.append(f'<circle cx="{x}" cy="{sign_y}" r="12.5" fill="#ffebee" stroke="#c62828" stroke-width="1.4"/>')
        parts.append(f'<text x="{x}" y="{sign_y + 5.5}" font-family="Georgia, serif" font-size="16" font-weight="900" fill="#b71c1c" text-anchor="middle">{sign_num}</text>')
        
        if count == 0:
            continue
        elif count <= 2:
            font_sz = "16.5" if count == 1 else "15.5"
            line_spacing = 22
            start_y = (y + 10) if count == 1 else (y + 2)
            for idx, p_text in enumerate(planets):
                p_y = start_y + (idx * line_spacing)
                is_retro = "(R)" in p_text or "(व)" in p_text
                color = "#c2410c" if is_retro else "#0f172a"
                weight = "900" if is_retro else "800"
                parts.append(f'<text x="{x}" y="{p_y}" font-family="Noto Sans Devanagari, Arial, sans-serif" font-size="{font_sz}" font-weight="{weight}" fill="{color}" text-anchor="middle">{p_text}</text>')
        elif count in (3, 4):
            font_sz = "15"
            x_offset = 36
            y_start = y + 2
            row_spacing = 22
            for idx, p_text in enumerate(planets):
                col_idx = idx % 2
                row_idx = idx // 2
                p_x = (x - x_offset) if col_idx == 0 else (x + x_offset)
                p_y = y_start + (row_idx * row_spacing)
                is_retro = "(R)" in p_text or "(व)" in p_text
                color = "#c2410c" if is_retro else "#0f172a"
                weight = "900" if is_retro else "800"
                parts.append(f'<text x="{p_x}" y="{p_y}" font-family="Noto Sans Devanagari, Arial, sans-serif" font-size="{font_sz}" font-weight="{weight}" fill="{color}" text-anchor="middle">{p_text}</text>')
        else:
            font_sz = "13.5"
            x_offset = 35
            y_start = y - 4
            row_spacing = 18
            for idx, p_text in enumerate(planets):
                col_idx = idx % 2
                row_idx = idx // 2
                p_x = (x - x_offset) if col_idx == 0 else (x + x_offset)
                p_y = y_start + (row_idx * row_spacing)
                is_retro = "(R)" in p_text or "(व)" in p_text
                color = "#c2410c" if is_retro else "#0f172a"
                weight = "900" if is_retro else "800"
                parts.append(f'<text x="{p_x}" y="{p_y}" font-family="Noto Sans Devanagari, Arial, sans-serif" font-size="{font_sz}" font-weight="{weight}" fill="{color}" text-anchor="middle">{p_text}</text>')

    if chart_title:
        title_w = min(s - 40, max(260, len(chart_title) * 11))
        parts.append(f'<rect x="{h - title_w/2}" y="8" width="{title_w}" height="26" rx="6" fill="#fff9f5" stroke="#990000" stroke-width="1.2"/>')
        parts.append(f'<text x="{h}" y="26" font-family="Noto Sans Devanagari, Georgia, serif" font-size="14" font-weight="bold" fill="#990000" text-anchor="middle">{chart_title}</text>')

    parts.append('</svg>')
    return _clean_svg("".join(parts))


def get_south_indian_chart_svg(rashi_planets_data: dict, asc_sign_idx: int, size: int = 500, chart_title: str = "") -> str:
    """
    Generates an SVG string for a South Indian style square grid astrology chart with large fonts.
    rashi_planets_data: Dict[int, list] where keys are 0-11 (Aries to Pisces signs).
                        Items are list of planet strings.
    asc_sign_idx: 0-11 for Lagna sign.
    """
    s = max(size, 480)
    box = s / 4.0
    
    sign_boxes = {
        11: (0, 0),
        0: (1, 0),
        1: (2, 0),
        2: (3, 0),
        3: (3, 1),
        4: (3, 2),
        5: (3, 3),
        6: (2, 3),
        7: (1, 3),
        8: (0, 3),
        9: (0, 2),
        10: (0, 1),
    }
    
    parts = [
        f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        '<linearGradient id="siBgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#0c1427"/>',
        '<stop offset="100%" stop-color="#03050b"/>',
        '</linearGradient>',
        '<linearGradient id="goldGrad2" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#fcedaa"/>',
        '<stop offset="50%" stop-color="#d4af37"/>',
        '<stop offset="100%" stop-color="#9a7b1c"/>',
        '</linearGradient>',
        '<filter id="textShadowSi">',
        '<feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#000000" flood-opacity="0.9"/>',
        '</filter>',
        '</defs>',
        f'<rect x="0" y="0" width="{s}" height="{s}" fill="url(#siBgGrad)" stroke="url(#goldGrad2)" stroke-width="3" rx="12"/>',
        f'<rect x="7" y="7" width="{s-14}" height="{s-14}" fill="none" stroke="#d4af37" stroke-width="0.8" stroke-dasharray="6,3" rx="8"/>',
        f'<rect x="{box}" y="{box}" width="{box*2}" height="{box*2}" fill="#060c18" stroke="#d4af37" stroke-width="1.5" rx="6"/>',
        f'<text x="{s/2}" y="{s/2 - 10}" font-family="Cinzel, Georgia, serif" font-size="16" font-weight="900" fill="#f0c05a" text-anchor="middle" letter-spacing="1.5px" filter="url(#textShadowSi)">VYAS ASTRA</text>',
        f'<text x="{s/2}" y="{s/2 + 16}" font-family="Noto Sans Devanagari, Plus Jakarta Sans, sans-serif" font-size="11" font-weight="700" fill="#eedc9a" text-anchor="middle" letter-spacing="0.5px">दक्षिण भारतीय चौकोर चक्र</text>'
    ]
    
    # Grid lines
    for i in range(1, 4):
        y_pos = i * box
        parts.append(f'<line x1="0" y1="{y_pos}" x2="{s}" y2="{y_pos}" stroke="#d4af37" stroke-width="1.4" stroke-opacity="0.85"/>')
        x_pos = i * box
        parts.append(f'<line x1="{x_pos}" y1="0" x2="{x_pos}" y2="{s}" stroke="#d4af37" stroke-width="1.4" stroke-opacity="0.85"/>')

    sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    for sign_idx, (col, row) in sign_boxes.items():
        bx = col * box
        by = row * box
        
        is_lagna = (sign_idx == asc_sign_idx)
        if is_lagna:
            parts.append(f'<line x1="{bx}" y1="{by}" x2="{bx+box}" y2="{by+box}" stroke="#ff4d4d" stroke-width="1.6" stroke-opacity="0.9"/>')
            parts.append(f'<text x="{bx + 8}" y="{by + 20}" font-family="Noto Sans Devanagari, sans-serif" font-size="12" font-weight="900" fill="#ff4d4d" filter="url(#textShadowSi)">लग्न (Asc)</text>')

        parts.append(f'<text x="{bx + box - 8}" y="{by + 18}" font-family="Cinzel, Georgia, serif" font-size="11.5" font-weight="800" fill="#d4af37" text-anchor="end" opacity="0.75">{sign_names[sign_idx][:3].upper()}</text>')
        
        p_list = rashi_planets_data.get(sign_idx, [])
        if p_list:
            count = len(p_list)
            if count <= 2:
                start_py = by + 42 if is_lagna else by + 36
                font_sz = "16" if count == 1 else "15"
                line_spacing = 22
                for p_idx, p_str in enumerate(p_list):
                    py = start_py + (p_idx * line_spacing)
                    is_retro = "(R)" in p_str or "(व)" in p_str
                    color = "#fb923c" if is_retro else "#ffffff"
                    parts.append(f'<text x="{bx + box/2}" y="{py}" font-family="Noto Sans Devanagari, Arial, sans-serif" font-size="{font_sz}" font-weight="800" fill="{color}" text-anchor="middle" filter="url(#textShadowSi)">{p_str}</text>')
            elif count in (3, 4):
                font_sz = "14.5"
                row_spacing = 22
                y_start = by + 42 if is_lagna else by + 36
                for p_idx, p_str in enumerate(p_list):
                    col_idx = p_idx % 2
                    row_idx = p_idx // 2
                    px = (bx + box * 0.28) if col_idx == 0 else (bx + box * 0.72)
                    py = y_start + (row_idx * row_spacing)
                    is_retro = "(R)" in p_str or "(व)" in p_str
                    color = "#fb923c" if is_retro else "#ffffff"
                    parts.append(f'<text x="{px}" y="{py}" font-family="Noto Sans Devanagari, Arial, sans-serif" font-size="{font_sz}" font-weight="800" fill="{color}" text-anchor="middle" letter-spacing="0.2px" filter="url(#textShadowSi)">{p_str}</text>')
            else:
                font_sz = "13"
                row_spacing = 18
                y_start = by + 38 if is_lagna else by + 32
                for p_idx, p_str in enumerate(p_list):
                    col_idx = p_idx % 2
                    row_idx = p_idx // 2
                    px = (bx + box * 0.28) if col_idx == 0 else (bx + box * 0.72)
                    py = y_start + (row_idx * row_spacing)
                    is_retro = "(R)" in p_str or "(व)" in p_str
                    color = "#fb923c" if is_retro else "#ffffff"
                    parts.append(f'<text x="{px}" y="{py}" font-family="Noto Sans Devanagari, Arial, sans-serif" font-size="{font_sz}" font-weight="800" fill="{color}" text-anchor="middle" filter="url(#textShadowSi)">{p_str}</text>')

    if chart_title:
        title_w = min(s - 40, max(260, len(chart_title) * 11))
        parts.append(f'<rect x="{s/2 - title_w/2}" y="{s - 32}" width="{title_w}" height="26" rx="12" fill="#090f1f" stroke="#d4af37" stroke-width="1.2"/>')
        parts.append(f'<text x="{s/2}" y="{s - 14}" font-family="Noto Sans Devanagari, Cinzel, serif" font-size="13" font-weight="bold" fill="#f0c05a" text-anchor="middle" filter="url(#textShadowSi)">{chart_title}</text>')

    parts.append('</svg>')
    return _clean_svg("".join(parts))
