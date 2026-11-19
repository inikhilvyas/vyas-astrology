#!/usr/bin/env python3
"""
Shastric Markdown Books Sutra Harvester
=======================================
Parses classical astrology books in markdown format from books/*.md
and converts their core yogas, planetary combinations, and predictions
into structured JSONL sutras compatible with knowledge_engine and SFT training.
"""

import os
import re
import json
import glob
from typing import List, Dict, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BOOKS_DIR = os.path.join(PROJECT_ROOT, "books")
OUTPUT_JSONL = os.path.join(BOOKS_DIR, "ai_jyotish_knowledge_bank_part23_shastric_md.jsonl")

def extract_bhrigu_nandi_combinations() -> List[Dict[str, Any]]:
    """Extracts planetary combinations from Bhrigu Nandi Nadi."""
    sutras = []
    path = os.path.join(BOOKS_DIR, "bhrigu nandi nadi book.md")
    if not os.path.exists(path):
        return sutras

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    sections = re.split(r'\n(?=[A-Z\s]{4,30}\b)', text)
    count = 1
    for sec in sections:
        sec = sec.strip()
        if len(sec) < 80 or len(sec) > 3000:
            continue
            
        lines = sec.split("\n")
        title = lines[0].strip()
        body = " ".join([l.strip() for l in lines[1:] if l.strip()])
        
        planets = ["Jupiter", "Saturn", "Mars", "Venus", "Mercury", "Sun", "Moon", "Rahu", "Ketu"]
        matched_planets = [p for p in planets if p.lower() in sec.lower()]
        
        if len(matched_planets) >= 2 and any(k in sec.lower() for k in ["native", "father", "profession", "marriage", "wealth", "knowledge", "health", "results"]):
            sutra = {
                "sutra_id": f"JYOTISH_SUTRA_MD_BNN_{count:04d}",
                "category": "Bhrigu Nandi Nadi",
                "sub_category": f"{' & '.join(matched_planets[:2])} Yoga",
                "primary_factor": matched_planets[0],
                "planetary_condition": title[:100],
                "condition_hi": f"{matched_planets[0]} व {matched_planets[1]} का भृगु नाड़ी योग।",
                "prediction_en": body[:350],
                "prediction_hi": f"भृगु नन्दी नाड़ी के अनुसार: {body[:350]}",
                "life_domain": "Career & Destiny",
                "source": "Bhrigu Nandi Nadi (R.G. Rao Classical Codices)",
                "strength_modifiers": "Modified by natural friendships, trinal aspects (1-5-9), and Gochar transit of Jupiter/Saturn."
            }
            sutras.append(sutra)
            count += 1
            if count > 800:
                break
                
    return sutras

def extract_lal_kitab_remedies() -> List[Dict[str, Any]]:
    """Extracts planetary conditions and satvik remedies from Lal Kitab.md."""
    sutras = []
    path = os.path.join(BOOKS_DIR, "Lal Kitab.md")
    if not os.path.exists(path):
        return sutras

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    blocks = re.split(r'\n(?=भाव\s*\d+|खाना\s*नंबर\s*\d+|सूर्य|चन्द्र|मंगल|बुध|बृहस्पति|शुक्र|शनि|राहु|केतु)', text)
    count = 1
    for blk in blocks:
        blk = blk.strip()
        if len(blk) < 60 or len(blk) > 2500:
            continue
            
        planets_hi = ["सूर्य", "चन्द्र", "मंगल", "बुध", "बृहस्पति", "गुरु", "शुक्र", "शनि", "राहु", "केतु"]
        m_p = [p for p in planets_hi if p in blk[:60]]
        
        if m_p and ("उपाय" in blk or "सावधानी" in blk or "फल" in blk or "प्रभाव" in blk):
            sutra = {
                "sutra_id": f"JYOTISH_SUTRA_MD_LK_{count:04d}",
                "category": "Lal Kitab",
                "sub_category": f"{m_p[0]} लाल किताब फरमान व उपाय",
                "primary_factor": m_p[0],
                "planetary_condition": blk[:120].replace("\n", " "),
                "condition_hi": blk[:120].replace("\n", " "),
                "prediction_en": f"Lal Kitab planetary condition for {m_p[0]} with specific behavioral remedy and satvik precaution.",
                "prediction_hi": blk[:400].replace("\n", " "),
                "life_domain": "Remedies & Protection",
                "source": "Lal Kitab (1952 Authentic Shastric Edition)",
                "strength_modifiers": "Always verify Dharmi Teva vs Andha Teva before prescribing remedies."
            }
            sutras.append(sutra)
            count += 1
            if count > 600:
                break
                
    return sutras

def extract_advanced_techniques_kn_rao() -> List[Dict[str, Any]]:
    """Extracts K.N. Rao & research team principles from Advanced Techniques of Astrological Predictions."""
    sutras = []
    path = os.path.join(BOOKS_DIR, "Advanced Techniques of Astrological Predictions.md")
    if not os.path.exists(path):
        return sutras

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    paragraphs = text.split("\n\n")
    count = 1
    for p in paragraphs:
        p = p.strip().replace("\n", " ")
        if len(p) < 100 or len(p) > 2000:
            continue

        keywords = ["dasha", "career", "marriage", "ashtakavarga", "darakaraka", "kaal sarpa", "disease", "timing", "jaimini", "profession", "service", "business"]
        matches = [k for k in keywords if k in p.lower()]
        
        if len(matches) >= 2:
            sutra = {
                "sutra_id": f"JYOTISH_SUTRA_MD_KNRAO_{count:04d}",
                "category": "K.N. Rao Advanced Predictive Astrology",
                "sub_category": f"{matches[0].capitalize()} & {matches[1].capitalize()} Technique",
                "primary_factor": matches[0].capitalize(),
                "planetary_condition": p[:120],
                "condition_hi": f"के.एन. राव आधुनिक शोध फलित नियम ({matches[0]} / {matches[1]} संदर्भ).",
                "prediction_en": p[:380],
                "prediction_hi": f"आधुनिक वैदिक शोध के अनुसार: {p[:380]}",
                "life_domain": "Career, Timing & Event Prediction",
                "source": "Advanced Techniques of Astrological Predictions (K.N. Rao & Research Team)",
                "strength_modifiers": "Synthesized with Vimshottari Dasha, Char Dasha, and Ashtakavarga bindu distribution."
            }
            sutras.append(sutra)
            count += 1
            if count > 800:
                break
                
    return sutras

def extract_jyotish_rahasya() -> List[Dict[str, Any]]:
    """Extracts predictive and diagnostic rules from ज्योतिष_रहस्य_दोनों_भाग_text.md."""
    sutras = []
    path = os.path.join(BOOKS_DIR, "ज्योतिष_रहस्य_दोनों_भाग_text.md")
    if not os.path.exists(path):
        return sutras

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    blocks = text.split("॥")
    count = 1
    for b in blocks:
        b = b.strip().replace("\n", " ")
        if len(b) < 80 or len(b) > 2000:
            continue
            
        if any(k in b for k in ["योग", "भाव", "दशा", "लग्नेश", "भाग्य", "राजयोग", "धनयोग", "रोग", "विवाह", "कर्म"]):
            sutra = {
                "sutra_id": f"JYOTISH_SUTRA_MD_RAHASYA_{count:04d}",
                "category": "Parashari Rahasya",
                "sub_category": "Classical Phalit & Yogas",
                "primary_factor": "Bhava & Bhavesha",
                "planetary_condition": b[:110],
                "condition_hi": b[:110],
                "prediction_en": f"Classical Parashari aphorism on planetary configuration and life outcomes: {b[:300]}",
                "prediction_hi": f"ज्योतिष रहस्य शास्त्रानुसार: {b[:350]}",
                "life_domain": "Wealth, Career & Health",
                "source": "Jyotish Rahasya (Jagjeevan Das Gupta Classical Edition)",
                "strength_modifiers": "Verify with Shadbala, Navamsha placement, and active Mahadasha."
            }
            sutras.append(sutra)
            count += 1
            if count > 700:
                break
                
    return sutras

def main():
    print("Beginning extraction of classical sutras from Markdown books...")
    all_extracted = []
    
    bnn = extract_bhrigu_nandi_combinations()
    print(f"Extracted {len(bnn)} Bhrigu Nandi Nadi sutras.")
    all_extracted.extend(bnn)
    
    lk = extract_lal_kitab_remedies()
    print(f"Extracted {len(lk)} Lal Kitab remedy & precaution sutras.")
    all_extracted.extend(lk)
    
    knr = extract_advanced_techniques_kn_rao()
    print(f"Extracted {len(knr)} K.N. Rao Advanced Predictive Astrology sutras.")
    all_extracted.extend(knr)
    
    rahasya = extract_jyotish_rahasya()
    print(f"Extracted {len(rahasya)} Jyotish Rahasya classical yogas.")
    all_extracted.extend(rahasya)
    
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for s in all_extracted:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            
    print(f"\n🎉 Successfully created {OUTPUT_JSONL} with {len(all_extracted)} new classical sutras!")

if __name__ == "__main__":
    main()
