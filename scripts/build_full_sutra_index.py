import sqlite3
import json
import re
import os

def build_index():
    db_path = 'data/vyas_phalit_vault.db'
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT sutra_id, category, sub_category, primary_factor, planetary_condition, condition_hi, prediction_en, prediction_hi, life_domain, source FROM sutras')
    rows = c.fetchall()
    print(f"Loaded {len(rows)} sutras from {db_path}...")

    planets_map = {
        'sun': 'Sun', 'surya': 'Sun', 'सूर्य': 'Sun',
        'moon': 'Moon', 'chandra': 'Moon', 'चन्द्र': 'Moon', 'चंद्र': 'Moon',
        'mars': 'Mars', 'mangal': 'Mars', 'मंगल': 'Mars',
        'mercury': 'Mercury', 'budh': 'Mercury', 'बुध': 'Mercury',
        'jupiter': 'Jupiter', 'guru': 'Jupiter', 'बृहस्पति': 'Jupiter', 'गुरु': 'Jupiter',
        'venus': 'Venus', 'shukra': 'Venus', 'शुक्र': 'Venus',
        'saturn': 'Saturn', 'shani': 'Saturn', 'शनि': 'Saturn',
        'rahu': 'Rahu', 'राहु': 'Rahu',
        'ketu': 'Ketu', 'केतु': 'Ketu'
    }

    signs_en = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    signs_hi = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']
    sign_lookup = {}
    for i, s in enumerate(signs_en):
        sign_lookup[s.lower()] = s
        sign_lookup[signs_hi[i]] = s

    house_hindi_ords = {
        'प्रथम': 1, 'लग्न': 1, 'द्वितीय': 2, 'तृतीय': 3, 'चतुर्थ': 4,
        'पंचम': 5, 'षष्ठ': 6, 'छठे': 6, 'सप्तम': 7, 'अष्टम': 8,
        'नवम': 9, 'दशम': 10, 'एकादश': 11, 'ग्यारहवें': 11, 'द्वादश': 12, 'बारहवें': 12
    }

    index_data = {
        'planet_signs': {},
        'planet_houses': {},
        'yutis': {},
        'dignities': {},
        'lagna_signs': {},
        'domains': {
            'career': [], 'wealth': [], 'marriage': [], 'health': [], 'mind': [], 'spirituality': [], 'general': []
        }
    }

    def add_to_idx(category, key, item):
        if key not in index_data[category]:
            index_data[category][key] = []
        if len(index_data[category][key]) < 100:  # Cap at 100 highest quality per placement
            index_data[category][key].append(item)

    for r in rows:
        sid, cat, subcat, factor, cond_en, cond_hi, pred_en, pred_hi, domain, src = r
        if not pred_hi or not cond_hi:
            continue

        item = {
            'id': sid,
            'factor': factor or 'Universal',
            'cond_hi': cond_hi,
            'cond_en': cond_en or '',
            'pred_hi': pred_hi,
            'domain': domain or 'General',
            'src': src or 'बृहत्पाराशर होराशास्त्र'
        }

        # 1. Map to Domain
        d_lower = (domain or '').lower() + ' ' + (cat or '').lower()
        dom_key = 'general'
        if any(w in d_lower for w in ['career', 'profession', 'व्यवसाय', 'कर्म', 'नौकरी']):
            dom_key = 'career'
        elif any(w in d_lower for w in ['wealth', 'finance', 'assets', 'धन', 'आय']):
            dom_key = 'wealth'
        elif any(w in d_lower for w in ['marriage', 'spouse', 'relationship', 'विवाह', 'पत्नी']):
            dom_key = 'marriage'
        elif any(w in d_lower for w in ['health', 'disease', 'रोग', 'स्वास्थ्य', 'आयु']):
            dom_key = 'health'
        elif any(w in d_lower for w in ['child', 'children', 'progeny', 'संतान', 'विद्या', 'शिक्षा', 'education']):
            dom_key = 'mind'
        elif any(w in d_lower for w in ['spiritual', 'dharma', 'धर्म', 'अध्यात्म', 'उपासना']):
            dom_key = 'spirituality'
        
        if len(index_data['domains'][dom_key]) < 200:
            index_data['domains'][dom_key].append(item)

        # 2. Extract Planet + Sign
        text_en = (cond_en or '').lower()
        text_hi = (cond_hi or '').lower()

        found_planet = None
        for p_k, p_norm in planets_map.items():
            if p_k in text_en or p_k in text_hi or (factor and factor.lower() == p_k):
                found_planet = p_norm
                break

        found_sign = None
        for s_k, s_norm in sign_lookup.items():
            if s_k in text_en or s_k in text_hi:
                found_sign = s_norm
                break

        if found_planet and found_sign:
            add_to_idx('planet_signs', f"{found_planet}_{found_sign}", item)

        # 3. Extract Planet + House
        found_house = None
        h_match = re.search(r'(\d+)(st|nd|rd|th)?\s*house', text_en)
        if h_match:
            found_house = int(h_match.group(1))
        else:
            for h_k, h_val in house_hindi_ords.items():
                if f"{h_k} भाव" in text_hi or f"{h_k} स्थान" in text_hi:
                    found_house = h_val
                    break

        if found_planet and found_house and 1 <= found_house <= 12:
            add_to_idx('planet_houses', f"{found_planet}_{found_house}", item)

        # 4. Extract Yutis (Conjunctions)
        present_planets = set()
        for p_k, p_norm in planets_map.items():
            if p_k in text_en or p_k in text_hi:
                present_planets.add(p_norm)
        
        if len(present_planets) >= 2:
            sorted_p = sorted(list(present_planets))
            for i in range(len(sorted_p)):
                for j in range(i+1, len(sorted_p)):
                    add_to_idx('yutis', f"{sorted_p[i]}_{sorted_p[j]}", item)

        # 5. Extract Dignities
        if found_planet:
            if 'exalt' in text_en or 'उच्च' in text_hi:
                add_to_idx('dignities', f"{found_planet}_Exalted", item)
            elif 'debilitat' in text_en or 'नीच' in text_hi:
                add_to_idx('dignities', f"{found_planet}_Debilitated", item)
            elif 'own sign' in text_en or 'स्वक्षेत्र' in text_hi:
                add_to_idx('dignities', f"{found_planet}_Own", item)

    out_file = 'data/vyas_sutras_fast_index.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    print(f"SUCCESS: Created comprehensive multi-dimensional index {out_file}!")
    print(f"  Planet-Sign keys: {len(index_data['planet_signs'])}")
    print(f"  Planet-House keys: {len(index_data['planet_houses'])}")
    print(f"  Yuti keys: {len(index_data['yutis'])}")
    print(f"  Dignity keys: {len(index_data['dignities'])}")
    for d, items in index_data['domains'].items():
        print(f"  Domain '{d}': {len(items)} sutras")

if __name__ == '__main__':
    build_index()

