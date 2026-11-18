#!/usr/bin/env python3
"""
Build High-Speed Pre-Indexed Shastric Sutras Cache for VYAS AI Copilot.
Extracts top verified classical sutras from vyas_phalit_vault.db into a lightweight JSON index.
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vyas_phalit_vault.db')
OUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vyas_sutras_fast_index.json')

def main():
    if not os.path.exists(DB_PATH):
        print("Vault DB not found:", DB_PATH)
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sutra_id, category, sub_category, primary_factor, planetary_condition, 
               condition_hi, prediction_en, prediction_hi, life_domain, source
        FROM sutras
        ORDER BY sutra_id ASC
    """)
    rows = cursor.fetchall()
    print(f"Loaded {len(rows)} sutras from vault.")

    # Organize index by:
    # 1. Domain (career, wealth, marriage, health, spirituality, education, court/adversity)
    # 2. Planet / Factor (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu, 1st..12th)
    index = {
        "domains": {
            "career": [],
            "wealth": [],
            "marriage": [],
            "health": [],
            "mind": [],
            "education": [],
            "adversity": [],
            "general": []
        },
        "planets": {
            "Sun": [], "Moon": [], "Mars": [], "Mercury": [],
            "Jupiter": [], "Venus": [], "Saturn": [], "Rahu": [], "Ketu": []
        },
        "kp_cusps": {}
    }

    def categorize_domain(ld, cat):
        text = (str(ld) + " " + str(cat)).lower()
        if any(w in text for w in ["career", "profession", "business", "status", "karm"]):
            return "career"
        if any(w in text for w in ["wealth", "finance", "money", "dhana", "asset"]):
            return "wealth"
        if any(w in text for w in ["marriage", "relationship", "spouse", "vivah"]):
            return "marriage"
        if any(w in text for w in ["health", "disease", "roga", "longevity", "ayur"]):
            return "health"
        if any(w in text for w in ["mind", "children", "progeny", "buddhi"]):
            return "mind"
        if any(w in text for w in ["education", "vidya", "learning"]):
            return "education"
        if any(w in text for w in ["adversity", "litigation", "enemy", "court", "shatru"]):
            return "adversity"
        return "general"

    for r in rows:
        item = {
            "id": r["sutra_id"],
            "src": r["source"],
            "factor": r["primary_factor"],
            "cond_hi": r["condition_hi"] or r["planetary_condition"],
            "pred_hi": r["prediction_hi"] or r["prediction_en"],
            "domain": r["life_domain"]
        }

        # Domain bucket
        d = categorize_domain(r["life_domain"], r["category"])
        if len(index["domains"][d]) < 120:  # store top representative sutras
            index["domains"][d].append(item)

        # Planet bucket
        pf = str(r["primary_factor"]).lower()
        for p in index["planets"]:
            if p.lower() in pf:
                if len(index["planets"][p]) < 60:
                    index["planets"][p].append(item)

        # KP Cusp bucket
        if "cuspal" in pf or "cusp" in pf:
            for num in range(1, 13):
                if f"{num}th" in pf or f"{num}st" in pf or f"{num}nd" in pf or f"{num}rd" in pf:
                    key = f"cusp_{num}"
                    if key not in index["kp_cusps"]:
                        index["kp_cusps"][key] = []
                    if len(index["kp_cusps"][key]) < 25:
                        index["kp_cusps"][key].append(item)

    conn.close()

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    total_indexed = sum(len(v) for v in index["domains"].values())
    print(f"Fast index written to {OUT_PATH}. Total indexed sample: {total_indexed} entries across domains.")

if __name__ == "__main__":
    main()
