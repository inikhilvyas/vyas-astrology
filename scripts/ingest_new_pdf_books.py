import os
import re
import sqlite3
import fitz

DB_PATH = 'data/vyas_phalit_vault.db'

def extract_pdf_sutras():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT count(*) FROM sutras")
    init_count = c.fetchone()[0]
    print(f"Initial sutras in DB: {init_count}")

    books = [
        ('books/जातकचांद्रिका.pdf', 'जातकचन्द्रिका (कालिदास/वेंकटेश)', 'Parashari Yogas'),
        ('books/preview-9788120837065_A24265326.pdf', 'वैदिक दृष्टि फल (गोपेश कुमार ओझा)', 'Planetary Aspects'),
        ('books/null-Fundamentals of Vedic Astrology_ Vedic Astrologer_s Handbook Vol. I ( PDFDrive.com ).pdf', 'फंडामेंटल्स ऑफ वैदिक एस्ट्रोलॉजी (बिपिन बिहारी)', 'Predictive Fundamentals'),
        ('books/A book on Mathematical astrology_Bansal.pdf', 'मैथमेटिकल एस्ट्रोलॉजी (वाई.के. बंसल)', 'Mathematical & Shodashvarga')
    ]

    new_sutras = []
    
    planets_hi = ['सूर्य', 'चन्द्र', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि', 'राहु', 'केतु']
    houses_hi = ['प्रथम', 'द्वितीय', 'तृतीय', 'चतुर्थ', 'पंचम', 'षष्ठ', 'सप्तम', 'अष्टम', 'नवम', 'दशम', 'एकादश', 'द्वादश', 'लग्न']
    rashis_hi = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']

    planets_en = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    houses_en = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', 'ascendant', 'lagna']
    rashis_en = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    for pdf_path, src_name, cat in books:
        if not os.path.exists(pdf_path):
            continue
        try:
            doc = fitz.open(pdf_path)
            print(f"Reading {pdf_path} ({len(doc)} pages)...")
            full_text = ""
            for page in doc:
                full_text += page.get_text() + "\n"

            # Split into paragraphs or numbered aphorisms
            paragraphs = re.split(r'\n\s*\n|(?:\r?\n(?=\d+[\.\)]|\bश्लोक\b|\bसूत्र\b))', full_text)
            for p in paragraphs:
                p_clean = re.sub(r'\s+', ' ', p).strip()
                if len(p_clean) < 40 or len(p_clean) > 800:
                    continue

                # Check if it mentions astrological factor
                has_factor = False
                matched_factor = None
                matched_domain = 'General'

                # Hindi match
                for pl in planets_hi:
                    if pl in p_clean:
                        has_factor = True
                        matched_factor = pl
                        break

                # English match if not matched
                if not has_factor:
                    for pl in planets_en:
                        if re.search(r'\b' + pl + r'\b', p_clean, re.I):
                            has_factor = True
                            matched_factor = pl
                            break

                if not has_factor:
                    continue

                # Check domain
                p_lower = p_clean.lower()
                if any(w in p_lower for w in ['career', 'profession', 'job', 'business', 'कर्म', 'आजीविका', 'नौकरी', 'राज्य']):
                    matched_domain = 'Career'
                elif any(w in p_lower for w in ['wealth', 'money', 'rich', 'finance', 'धन', 'संपत्ति', 'आय', 'लाभ']):
                    matched_domain = 'Wealth'
                elif any(w in p_lower for w in ['marriage', 'spouse', 'wife', 'husband', 'विवाह', 'पत्नी', 'पति', 'दांपत्य']):
                    matched_domain = 'Marriage'
                elif any(w in p_lower for w in ['health', 'disease', 'illness', 'रोग', 'स्वास्थ्य', 'आयु']):
                    matched_domain = 'Health'
                elif any(w in p_lower for w in ['spirituality', 'moksha', 'dharma', 'धर्म', 'मोक्ष', 'अध्यात्म', 'उपासना']):
                    matched_domain = 'Spirituality'

                sutra_id = f"NEW_PDF_{len(new_sutras)+1:05d}"
                cond_text = p_clean[:120]
                pred_text = p_clean

                new_sutras.append((
                    sutra_id,
                    cat,
                    'Classical Aphorism',
                    matched_factor or 'Graha',
                    cond_text,
                    cond_text,
                    pred_text,
                    pred_text,
                    matched_domain,
                    src_name
                ))

        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

    print(f"Extracted {len(new_sutras)} new sutras from PDF treatises!")
    if new_sutras:
        c.executemany("""
            INSERT OR REPLACE INTO sutras 
            (sutra_id, category, sub_category, primary_factor, planetary_condition, condition_hi, prediction_en, prediction_hi, life_domain, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, new_sutras)
        conn.commit()

    c.execute("SELECT count(*) FROM sutras")
    final_count = c.fetchone()[0]
    conn.close()
    print(f"Total sutras in vault now: {final_count}")

if __name__ == '__main__':
    extract_pdf_sutras()

