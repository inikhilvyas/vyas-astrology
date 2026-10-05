"""North Indian and South Indian Vedic Chart SVG Generator with Degree & Minute Overlay.

Renders crisp, high-resolution SVG astrological charts with:
- Outer rectangular frame with golden/ruby styling
- Classical diagonal and diamond line geometry
- House numbers / Sign numbers in distinct ruby color
- Planetary glyphs with exact Degree & Minute (e.g. 'Su 07°42'', 'Me 29°15' (R)')
- Multi-line balanced spacing so multiple planets in a single house remain legible
"""
import re
from typing import Dict, List, Tuple


def _clean_svg(svg_str: str) -> str:
    """Strip HTML comments and collapse multiple whitespace/newlines to single space."""
    clean = re.sub(r'<!--.*?-->', '', svg_str, flags=re.DOTALL)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def get_north_indian_chart_svg(houses_data: dict, size: int = 440, chart_title: str = "") -> str:
    """
    Generates an SVG string for a North Indian style astrology chart.
    houses_data: Dict[int, list] where keys are 1-12 (houses).
                 First item in list is the sign number (string).
                 Subsequent items are planet strings, optionally with degrees (e.g. 'Su 07°42\'').
    """
    s = size
    h = size / 2.0
    q = size / 4.0
    
    parts = [
        f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        '<linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#0a1224"/>',
        '<stop offset="50%" stop-color="#050913"/>',
        '<stop offset="100%" stop-color="#020408"/>',
        '</linearGradient>',
        '<linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#fcedaa"/>',
        '<stop offset="50%" stop-color="#d4af37"/>',
        '<stop offset="100%" stop-color="#9a7b1c"/>',
        '</linearGradient>',
        '<filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">',
        '<feGaussianBlur stdDeviation="2" result="blur"/>',
        '<feComposite in="SourceGraphic" in2="blur" operator="over"/>',
        '</filter>',
        '</defs>',
        f'<rect x="0" y="0" width="{s}" height="{s}" fill="url(#bgGrad)" stroke="url(#goldGrad)" stroke-width="2.5" rx="10"/>',
        f'<rect x="6" y="6" width="{s-12}" height="{s-12}" fill="none" stroke="#d4af37" stroke-width="0.75" stroke-opacity="0.6" stroke-dasharray="6,3" rx="6"/>',
        f'<rect x="10" y="10" width="{s-20}" height="{s-20}" fill="none" stroke="#d4af37" stroke-width="0.5" stroke-opacity="0.3"/>'
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
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d4af37" stroke-width="1.6" stroke-opacity="0.85"/>')
        
    # House center coordinates
    positions = {
        1: (h, q - 10),
        2: (q, q/2 - 2),
        3: (q/2 + 5, q),
        4: (q, h),
        5: (q/2 + 5, s - q),
        6: (q, s - q/2 + 2),
        7: (h, s - q + 10),
        8: (s - q, s - q/2 + 2),
        9: (s - q/2 - 5, s - q),
        10: (s - q, h),
        11: (s - q/2 - 5, q),
        12: (s - q, q/2 - 2)
    }
    
    for house, pos in positions.items():
        x, y = pos
        data = houses_data.get(house, [])
        if not data:
            continue
            
        sign_num = str(data[0])
        planets = data[1:]
        
        # Draw sign number (Coral Red with subtle circle background)
        parts.append(f'<circle cx="{x}" cy="{y - 17}" r="7.5" fill="#2d0a0a" stroke="#ff4d4d" stroke-width="0.8" stroke-opacity="0.7"/>')
        parts.append(f'<text x="{x}" y="{y - 13.5}" font-family="Cinzel, Georgia, serif" font-size="10.5" font-weight="bold" fill="#ff6b6b" text-anchor="middle">{sign_num}</text>')
        
        # Draw planets in balanced multi-lines
        if planets:
            line_spacing = 12
            start_y = y + 2
            if len(planets) > 2:
                start_y = y - 4
                
            for idx, p_text in enumerate(planets):
                p_y = start_y + (idx * line_spacing)
                is_retro = "(R)" in p_text
                color = "#ff9f43" if is_retro else "#fef0cd"
                weight = "700" if is_retro else "600"
                parts.append(f'<text x="{x}" y="{p_y}" font-family="Plus Jakarta Sans, Trebuchet MS, sans-serif" font-size="9.5" font-weight="{weight}" fill="{color}" text-anchor="middle" letter-spacing="0.2px">{p_text}</text>')

    if chart_title:
        parts.append(f'<rect x="{h - 130}" y="10" width="260" height="24" rx="12" fill="#0b1326" stroke="#d4af37" stroke-width="0.8" stroke-opacity="0.8"/>')
        parts.append(f'<text x="{h}" y="26" font-family="Cinzel, Georgia, serif" font-size="11.5" font-weight="bold" fill="#f0c05a" text-anchor="middle" letter-spacing="1px">{chart_title}</text>')

    parts.append('</svg>')
    return _clean_svg("".join(parts))


def get_north_indian_chart_svg_print(houses_data: dict, size: int = 400, chart_title: str = "") -> str:
    """
    Generates a high-contrast publication-grade SVG for print / PDF with white background,
    crisp ruby/crimson geometry, and dark typography.
    """
    s = size
    h = size / 2.0
    q = size / 4.0
    
    parts = [
        f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect x="0" y="0" width="{s}" height="{s}" fill="#ffffff" stroke="#990000" stroke-width="2" rx="4"/>',
        f'<rect x="4" y="4" width="{s-8}" height="{s-8}" fill="none" stroke="#b30000" stroke-width="0.8" stroke-opacity="0.5"/>'
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
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#b30000" stroke-width="1.4"/>')
        
    positions = {
        1: (h, q - 8),
        2: (q, q/2 - 2),
        3: (q/2 + 5, q),
        4: (q, h),
        5: (q/2 + 5, s - q),
        6: (q, s - q/2 + 2),
        7: (h, s - q + 8),
        8: (s - q, s - q/2 + 2),
        9: (s - q/2 - 5, s - q),
        10: (s - q, h),
        11: (s - q/2 - 5, q),
        12: (s - q, q/2 - 2)
    }
    
    for house, pos in positions.items():
        x, y = pos
        data = houses_data.get(house, [])
        if not data:
            continue
            
        sign_num = str(data[0])
        planets = data[1:]
        
        # Draw sign number in subtle circle
        parts.append(f'<text x="{x}" y="{y - 14}" font-family="Cinzel, Georgia, serif" font-size="11" font-weight="bold" fill="#7a1010" text-anchor="middle">{sign_num}</text>')
        
        if planets:
            line_spacing = 11.5
            start_y = y + 1
            if len(planets) > 2:
                start_y = y - 4
                
            for idx, p_text in enumerate(planets):
                p_y = start_y + (idx * line_spacing)
                is_retro = "(R)" in p_text
                color = "#a02020" if is_retro else "#111111"
                weight = "bold" if is_retro else "600"
                parts.append(f'<text x="{x}" y="{p_y}" font-family="Noto Sans Devanagari, Plus Jakarta Sans, Arial, sans-serif" font-size="9.5" font-weight="{weight}" fill="{color}" text-anchor="middle">{p_text}</text>')

    if chart_title:
        parts.append(f'<rect x="{h - 110}" y="6" width="220" height="20" rx="4" fill="#fff9f5" stroke="#990000" stroke-width="0.8"/>')
        parts.append(f'<text x="{h}" y="20" font-family="Cinzel, Georgia, serif" font-size="10" font-weight="bold" fill="#990000" text-anchor="middle">{chart_title}</text>')

    parts.append('</svg>')
    return _clean_svg("".join(parts))



def get_south_indian_chart_svg(rashi_planets_data: dict, asc_sign_idx: int, size: int = 440, chart_title: str = "") -> str:
    """
    Generates an SVG string for a South Indian style square grid astrology chart.
    rashi_planets_data: Dict[int, list] where keys are 0-11 (Aries to Pisces signs).
                        Items are list of planet strings.
    asc_sign_idx: 0-11 for Lagna sign.
    """
    s = size
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
        '<stop offset="0%" stop-color="#0a1224"/>',
        '<stop offset="100%" stop-color="#03050a"/>',
        '</linearGradient>',
        '<linearGradient id="goldGrad2" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#fcedaa"/>',
        '<stop offset="50%" stop-color="#d4af37"/>',
        '<stop offset="100%" stop-color="#9a7b1c"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect x="0" y="0" width="{s}" height="{s}" fill="url(#siBgGrad)" stroke="url(#goldGrad2)" stroke-width="2.5" rx="10"/>',
        f'<rect x="6" y="6" width="{s-12}" height="{s-12}" fill="none" stroke="#d4af37" stroke-width="0.7" stroke-dasharray="6,3" rx="6"/>',
        f'<rect x="{box}" y="{box}" width="{box*2}" height="{box*2}" fill="#060c18" stroke="#d4af37" stroke-width="1.2" rx="4"/>',
        f'<text x="{s/2}" y="{s/2 - 8}" font-family="Cinzel, Georgia, serif" font-size="14" font-weight="900" fill="#f0c05a" text-anchor="middle" letter-spacing="1.5px">VYAS ASTRA</text>',
        f'<text x="{s/2}" y="{s/2 + 14}" font-family="Plus Jakarta Sans, sans-serif" font-size="9" font-weight="600" fill="#eedc9a" text-anchor="middle" letter-spacing="0.5px">SOUTH INDIAN FORMAT</text>'
    ]
    
    # Grid lines
    for i in range(1, 4):
        y_pos = i * box
        parts.append(f'<line x1="0" y1="{y_pos}" x2="{s}" y2="{y_pos}" stroke="#d4af37" stroke-width="1.2" stroke-opacity="0.8"/>')
        x_pos = i * box
        parts.append(f'<line x1="{x_pos}" y1="0" x2="{x_pos}" y2="{s}" stroke="#d4af37" stroke-width="1.2" stroke-opacity="0.8"/>')

    sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    for sign_idx, (col, row) in sign_boxes.items():
        bx = col * box
        by = row * box
        
        is_lagna = (sign_idx == asc_sign_idx)
        if is_lagna:
            parts.append(f'<line x1="{bx}" y1="{by}" x2="{bx+box}" y2="{by+box}" stroke="#ff4d4d" stroke-width="1.2" stroke-opacity="0.8"/>')
            parts.append(f'<text x="{bx + 8}" y="{by + 16}" font-family="Plus Jakarta Sans, sans-serif" font-size="9" font-weight="900" fill="#ff4d4d">LAGNA</text>')

        parts.append(f'<text x="{bx + box - 6}" y="{by + 14}" font-family="Cinzel, Georgia, serif" font-size="8" font-weight="700" fill="#d4af37" text-anchor="end" opacity="0.6">{sign_names[sign_idx][:3].upper()}</text>')
        
        p_list = rashi_planets_data.get(sign_idx, [])
        if p_list:
            start_py = by + 28 if is_lagna else by + 24
            for p_idx, p_str in enumerate(p_list):
                py = start_py + (p_idx * 12)
                color = "#ff9f43" if "(R)" in p_str else "#fef0cd"
                parts.append(f'<text x="{bx + box/2}" y="{py}" font-family="Plus Jakarta Sans, sans-serif" font-size="9" font-weight="700" fill="{color}" text-anchor="middle">{p_str}</text>')

    if chart_title:
        parts.append(f'<rect x="{s/2 - 120}" y="{s - 28}" width="240" height="22" rx="10" fill="#090f1f" stroke="#d4af37" stroke-width="0.8"/>')
        parts.append(f'<text x="{s/2}" y="{s - 13}" font-family="Cinzel, serif" font-size="10.5" font-weight="bold" fill="#f0c05a" text-anchor="middle">{chart_title}</text>')

    parts.append('</svg>')
    return _clean_svg("".join(parts))
