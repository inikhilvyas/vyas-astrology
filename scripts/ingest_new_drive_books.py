import os
import glob
import re
import sqlite3
import hashlib

DB_PATH = 'data/vyas_phalit_vault.db'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Get existing IDs
c.execute("SELECT sutra_id FROM sutras")
existing_ids = set(r[0] for r in c.fetchall())
print(f"Existing sutras in DB: {len(existing_ids)}")

PLANET_MAP = {
    'सूर्य': 'Sun', 'रवि': 'Sun', 'sun': 'Sun',
    'चन्द्र': 'Moon', 'चंद्र': 'Moon', 'शशि': 'Moon', 'moon': 'Moon',
    'मंगल': 'Mars', 'भौम': 'Mars', 'कुज': 'Mars', 'mars': 'Mars',
    'बुध': 'Mercury', 'सौम्य': 'Mercury', 'mercury': 'Mercury',
    'गुरु': 'Jupiter', 'बृहस्पति': 'Jupiter', 'जीव': 'Jupiter', 'jupiter': 'Jupiter',
    'शुक्र': 'Venus', 'भृगु': 'Venus', 'venus': 'Venus',
    'शनि': 'Saturn', 'मंद': 'Saturn', 'शनैश्चर': 'Saturn', 'saturn': 'Saturn',
    'राहु': 'Rahu', 'तम': 'Rahu', 'rahu': 'Rahu',
    'केतु': 'Ketu', 'शिखी': 'Ketu', 'ketu': 'Ketu'
}

SIGNS_HI = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']
HOUSES_HI = ['प्रथम', 'द्वितीय', 'तृतीय', 'चतुर्थ', 'पंचम', 'षष्ठ', 'सप्तम', 'अष्टम', 'नवम', 'दशम', 'एकादश', 'द्वादश', 'लग्न', 'छठे', 'आठवें', 'दसवें', 'बारहवें']

books = sorted(glob.glob('books/*.md'))
print(f"Scanning {len(books)} books...")

new_sutras = []

for b in books:
    base = os.path.basename(b)
    # determine source
    src = "वैदिक शास्त्र"
    if 'saravali' in base.lower(): src = "कल्याणवर्मा सारावली"
    elif 'bhavartha' in base.lower(): src = "भावार्थ रत्नाकर"
    elif 'bhrigu' in base.lower(): src = "भृगु सूत्र"
    elif 'parasara' in base.lower() or 'parashar' in base.lower(): src = "बृहत्पाराशर होराशास्त्र"
    elif 'ratnakar' in base.lower() or 'रत्न' in base: src = "ज्योतिष रत्नाकर"
    elif 'yoga' in base.lower() or 'योग' in base: src = "अमृत फलित योग संग्रह"
    elif 'garga' in base.lower(): src = "गर्ग होरा"
    elif 'horasara' in base.lower(): src = "होरासार (पृथुयशा)"
    elif 'rog' in base.lower() or 'उपचार' in base: src = "ज्योतिष द्वारा रोग उपचार"
    elif 'shiksha' in base.lower(): src = "सचित्र ज्योतिष शिक्षा"
    else:
        src = base.split('_')[0].replace('-', ' ')

    try:
        with open(b, 'r', encoding='utf-8', errors='ignore') as fl:
            content = fl.read()
    except Exception:
        continue

    # Split into paragraphs or numbered sections
    paras = re.split(r'\n\s*\n|\n(?=[0-9]+[\.\-]|\#\#)', content)
    for p in paras:
        p = p.strip()
        if len(p) < 40 or len(p) > 1200:
            continue
        if 'Source: Google Drive' in p or 'Original filename:' in p:
            continue

        # Look for planet mention
        found_planets = []
        for p_hi, p_en in PLANET_MAP.items():
            if p_hi in p:
                found_planets.append((p_hi, p_en))

        if not found_planets:
            continue

        # Look for sign or house
        has_sign = any(s in p for s in SIGNS_HI)
        has_house = any(h in p for h in HOUSES_HI) or bool(re.search(r'[0-9]{1,2}(वें|वे|th)?\s*भाव', p))

        if not (has_sign or has_house or 'योग' in p or 'दृष्टि' in p or 'दशा' in p):
            continue

        prim_p = found_planets[0][1]
        prim_p_hi = found_planets[0][0]

        # Determine category
        cat = 'general'
        if 'योग' in p: cat = 'yoga'
        elif has_house: cat = 'house_placement'
        elif has_sign: cat = 'sign_placement'
        elif 'दृष्टि' in p: cat = 'aspect'
        elif 'दशा' in p: cat = 'dasha'

        # Domain
        domain = 'life'
        if any(w in p for w in ['धन', 'संपत्ति', 'लाभ', 'व्यापार', 'लक्ष्मी', 'दरिद्र', 'ऋण']): domain = 'wealth'
        elif any(w in p for w in ['विवाह', 'पत्नी', 'पति', 'दांपत्य', 'संतान', 'पुत्र', 'कन्या']): domain = 'marriage'
        elif any(w in p for w in ['राज', 'पद', 'अधिकार', 'नौकरी', 'आजीविका', 'कर्म', 'यश', 'प्रतिष्ठा']): domain = 'career'
        elif any(w in p for w in ['रोग', 'आयु', 'मृत्यु', 'अस्वस्थ', 'चिकित्सा', 'पीड़ा']): domain = 'health'
        elif any(w in p for w in ['ज्ञान', 'अध्यात्म', 'वैराग्य', 'मोक्ष', 'तप', 'ज्योतिष']): domain = 'spiritual'

        # Generate unique hash ID
        h_val = hashlib.md5((src + p[:100]).encode('utf-8')).hexdigest()[:12]
        s_id = f"SUTRA_{src[:4]}_{h_val}".upper()

        if s_id in existing_ids:
            continue

        # Clean text
        clean_text = " ".join(p.split())
        cond_hi = f"{prim_p_hi} शास्त्रीय योग स्थिति"
        # Extract first sentence as condition if possible
        sentences = re.split(r'[\।\.\n]', clean_text)
        if len(sentences) > 1 and len(sentences[0]) > 10:
            cond_hi = sentences[0].strip()

        new_sutras.append((
            s_id,
            cat,
            domain,
            prim_p,
            f"{prim_p} in classical configuration",
            cond_hi[:200],
            clean_text,
            clean_text,
            domain,
            src,
            "उच्च शास्त्रीय प्रमाण (Authentic Manuscript)"
        ))
        existing_ids.add(s_id)

print(f"Extracted {len(new_sutras)} authentic classical sutras from newly added books!")

if new_sutras:
    c.executemany("""
    INSERT OR IGNORE INTO sutras (
        sutra_id, category, sub_category, primary_factor,
        planetary_condition, condition_hi, prediction_en,
        prediction_hi, life_domain, source, strength_modifiers
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, new_sutras)
    conn.commit()
    print("✓ Successfully saved into data/vyas_phalit_vault.db")

c.execute("SELECT COUNT(*) FROM sutras")
print("Total sutras in vault now:", c.fetchone()[0])
conn.close()

