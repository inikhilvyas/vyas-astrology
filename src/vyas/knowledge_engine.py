"""AI Jyotish Knowledge Engine for VYAS (2073 Classical Astrological Sutras).

Integrates the comprehensive classical database `ai_jyotish_knowledge_bank_2000.jsonl`
into the deterministic predictive astrology pipeline:
1. Bhrigu Sutram (Bhava Phala & Dignities) - 432 rules
2. Bhavadhipati Phala (Parashari 1st-12th Lords across all 12 houses) - 144 rules
3. Classical Vedic Sutras (210 authentic Raja, Dhana, Career, Health, Marriage Yogas) - 210 rules
4. Jaimini Upadesha Sutras (Karakamsa, AL, UL, Chara Karakas) - 22 rules
5. Dasha & Gochara Phala (Vimshottari MD/AD combinations & Gochara transits) - 97 rules
6. Bhrigu Nandi Nadi (Planetary connections, conjunctions, trikone relations) - 1168 rules

Evaluates natal charts dynamically and provides contextual deterministic predictions.
"""
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from vyas import constants

KNOWLEDGE_FILE_PATH = Path(__file__).resolve().parents[2] / "books" / "ai_jyotish_knowledge_bank_2000.jsonl"

_CACHED_KNOWLEDGE: Optional[List[Dict[str, Any]]] = None

SIGNS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
SIGN_MAP = {s.lower(): idx for idx, s in enumerate(SIGNS_EN)}

PLANET_NAMES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

ORDINAL_HOUSES = {
    "1st": 1, "first": 1, "2nd": 2, "second": 2, "3rd": 3, "third": 3,
    "4th": 4, "fourth": 4, "5th": 5, "fifth": 5, "6th": 6, "sixth": 6,
    "7th": 7, "seventh": 7, "8th": 8, "eighth": 8, "9th": 9, "ninth": 9,
    "10th": 10, "tenth": 10, "11th": 11, "eleventh": 11, "12th": 12, "twelfth": 12
}

@dataclass
class MatchedSutra:
    sutra_id: str
    category: str
    sub_category: str
    primary_factor: str
    planetary_condition: str
    condition_hi: str
    prediction_en: str
    prediction_hi: str
    life_domain: str
    source: str
    strength_modifiers: str
    matched_detail: str

def load_knowledge_bank() -> List[Dict[str, Any]]:
    """Loads and caches all sutras from all knowledge bank jsonl/json files in the books/ folder."""
    global _CACHED_KNOWLEDGE
    if _CACHED_KNOWLEDGE is not None:
        return _CACHED_KNOWLEDGE
    
    records = []
    b_dir = Path(__file__).resolve().parents[2] / "books"
    if b_dir.exists():
        # Match all files containing knowledge/sutra in name or jsonl/json
        target_files = sorted(b_dir.glob("*.jsonl")) + sorted(b_dir.glob("*sutra*.json")) + sorted(b_dir.glob("*knowledge*.json"))
        # If no specific matched, check default ai_jyotish file
        if not target_files and KNOWLEDGE_FILE_PATH.exists():
            target_files = [KNOWLEDGE_FILE_PATH]

        seen_ids = set()
        for k_file in target_files:
            try:
                with open(k_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                d = json.loads(line)
                                sid = d.get("sutra_id", "")
                                if sid and sid in seen_ids:
                                    continue
                                if sid:
                                    seen_ids.add(sid)
                                records.append(d)
                            except Exception:
                                pass
            except Exception:
                pass

    _CACHED_KNOWLEDGE = records
    return _CACHED_KNOWLEDGE

def evaluate_chart_sutras(chart, current_dasha: Optional[Tuple[str, str]] = None, current_transits: Optional[Dict[str, int]] = None) -> List[MatchedSutra]:
    """
    Evaluates natal chart against the 2,073 formulas in ai_jyotish_knowledge_bank_2000.
    Returns list of matched sutras with full bilingual predictions.
    """
    knowledge = load_knowledge_bank()
    if not knowledge:
        return []

    asc_sign = chart.ascendant_sign
    planets = chart.planets

    p_house: Dict[str, int] = {}
    p_sign: Dict[str, int] = {}
    for p_name, p in planets.items():
        p_sign[p_name] = p.sign_index
        p_house[p_name] = (p.sign_index - asc_sign + 12) % 12 + 1

    # House Lords
    h_lords: Dict[int, str] = {}
    for h in range(1, 13):
        s_idx = (asc_sign + h - 1) % 12
        h_lords[h] = constants.SIGN_LORD[s_idx]

    # Planet house lordships
    p_owns: Dict[str, List[int]] = {p: [] for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    for h, lord in h_lords.items():
        if lord in p_owns:
            p_owns[lord].append(h)

    # Planets in each house
    h_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for p_name, h in p_house.items():
        h_planets[h].append(p_name)

    # Aspects cast by each planet
    aspects_cast: Dict[str, List[int]] = {p: [] for p in planets}
    for p_name in planets:
        offsets = constants.ASPECTS.get(p_name, [7])
        h_from_p = p_house[p_name]
        for off in offsets:
            tgt_h = (h_from_p + off - 2) % 12 + 1
            aspects_cast[p_name].append(tgt_h)

    # Dignity sets
    exalted_planets = set()
    debilitated_planets = set()
    own_sign_planets = set()
    for p_name, p in planets.items():
        s_idx = p.sign_index
        if p_name in constants.EXALTATION and s_idx == constants.EXALTATION[p_name][0]:
            exalted_planets.add(p_name)
        elif p_name in constants.EXALTATION and s_idx == (constants.EXALTATION[p_name][0] + 6) % 12:
            debilitated_planets.add(p_name)
        elif p_name in constants.OWN_SIGNS and s_idx in constants.OWN_SIGNS[p_name]:
            own_sign_planets.add(p_name)

    # Jaimini Chara Karakas
    sevengrahas = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    deg_list = []
    for g in sevengrahas:
        if g in planets:
            deg_in_sign = planets[g].longitude % 30.0
            deg_list.append((deg_in_sign, g))
    deg_list.sort(key=lambda x: x[0], reverse=True)
    ak_planet = deg_list[0][1] if deg_list else "Jupiter"
    amk_planet = deg_list[1][1] if len(deg_list) > 1 else "Sun"

    # Arudha Lagna (AL)
    lagna_lord = h_lords[1]
    lagna_lord_house = p_house.get(lagna_lord, 1)
    al_sign = (asc_sign + 2 * (lagna_lord_house - 1)) % 12
    al_house = (al_sign - asc_sign + 12) % 12 + 1

    matched: List[MatchedSutra] = []
    seen_ids: Set[str] = set()

    for item in knowledge:
        sid = item.get("sutra_id", "")
        cat = item.get("category", "")
        cond_str = item.get("planetary_condition", "")
        pf = item.get("primary_factor", "")
        is_hit = False
        detail = ""

        # ---------------------------------------------------------
        # 1. Bhrigu Sutram (Bhava Phala)
        # ---------------------------------------------------------
        if "Bhrigu Sutram" in cat:
            # Check pattern: [Planet] placed in the [N]th House
            m_placed = re.search(r"(\w+)\s+(?:placed\s+in|in)\s+the\s+(\d+)(?:st|nd|rd|th)?\s+House", cond_str, re.I)
            if m_placed:
                pl = m_placed.group(1).capitalize()
                h_target = int(m_placed.group(2))
                if p_house.get(pl) == h_target:
                    # check sub-conditions
                    if "Exaltation or Own Sign" in cond_str:
                        if pl in exalted_planets or pl in own_sign_planets:
                            is_hit = True
                            detail = f"{pl} is in House {h_target} in Exaltation/Own Sign."
                    elif "Debilitation" in cond_str:
                        if pl in debilitated_planets:
                            is_hit = True
                            detail = f"{pl} is in House {h_target} in Debilitation."
                    elif "aspect of Jupiter or Venus" in cond_str:
                        asp_j = h_target in aspects_cast.get("Jupiter", [])
                        asp_v = h_target in aspects_cast.get("Venus", [])
                        if asp_j or asp_v:
                            is_hit = True
                            detail = f"{pl} in House {h_target} receives aspect of {'Jupiter' if asp_j else ''} {'Venus' if asp_v else ''}."
                    elif "placed in the" in cond_str or "(मूल भाव फल)" in item.get("condition_hi", ""):
                        is_hit = True
                        detail = f"{pl} occupies House {h_target}."

        # ---------------------------------------------------------
        # 2. Bhavadhipati Phala (Parashari 1st-12th Lords)
        # ---------------------------------------------------------
        elif "Bhavadhipati Phala" in cat:
            m_lord = re.search(r"(\d+)(?:st|nd|rd|th)?\s+Lord.*?\s+posited\s+in\s+the\s+(\d+)(?:st|nd|rd|th)?\s+House", cond_str, re.I)
            if m_lord:
                lord_h = int(m_lord.group(1))
                target_h = int(m_lord.group(2))
                ruling_graha = h_lords.get(lord_h)
                if ruling_graha and p_house.get(ruling_graha) == target_h:
                    is_hit = True
                    detail = f"Lord of House {lord_h} ({ruling_graha}) sits in House {target_h}."

        # ---------------------------------------------------------
        # 3. Classical Vedic Sutras (Raja, Dhana, Career, Health, etc.)
        # ---------------------------------------------------------
        elif "Classical Vedic Sutras" in cat:
            sub = item.get("sub_category", "")
            # Evaluate deterministic formulas
            if "Dharma-Karmadhipati" in sub:
                l9 = h_lords[9]
                l10 = h_lords[10]
                if p_house[l9] == p_house[l10] or p_house[l10] in aspects_cast.get(l9, []) or p_house[l9] in aspects_cast.get(l10, []):
                    is_hit = True
                    detail = f"9th Lord {l9} & 10th Lord {l10} mutually related."
            elif "Simhasana Prapti" in sub:
                l1, l9, l10 = h_lords[1], h_lords[9], h_lords[10]
                if p_house[l1] == 10 and p_house[l9] == 10 and p_house[l10] == 10:
                    is_hit = True
                    detail = f"Lagna lord {l1}, 9th lord {l9}, and 10th lord {l10} all conjunct in 10th house."
            elif "Maha Parivartana Yoga (1st & 10th)" in sub:
                l1, l10 = h_lords[1], h_lords[10]
                if p_house[l1] == 10 and p_house[l10] == 1:
                    is_hit = True
                    detail = f"Parivartana between 1st Lord {l1} in 10th and 10th Lord {l10} in 1st."
            elif "Maha Parivartana Yoga (1st & 11th)" in sub:
                l1, l11 = h_lords[1], h_lords[11]
                if p_house[l1] == 11 and p_house[l11] == 1:
                    is_hit = True
                    detail = f"Parivartana between 1st Lord {l1} in 11th and 11th Lord {l11} in 1st."
            elif "Shree Yoga" in sub:
                l2, l9 = h_lords[2], h_lords[9]
                if p_house[l2] in {1, 4, 7, 10} and p_house[l9] in {1, 4, 7, 10} and p_house[l2] == p_house[l9]:
                    is_hit = True
                    detail = f"2nd Lord {l2} and 9th Lord {l9} in Kendra house {p_house[l2]}."
            elif "Sunapha Yoga" in sub:
                m_h = p_house["Moon"]
                h_next = (m_h % 12) + 1
                planets_next = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if p_house[p] == h_next]
                if planets_next:
                    is_hit = True
                    detail = f"Planets {planets_next} in 2nd from Moon (House {h_next})."
            elif "Anapha Yoga" in sub:
                m_h = p_house["Moon"]
                h_prev = ((m_h - 2 + 12) % 12) + 1
                planets_prev = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if p_house[p] == h_prev]
                if planets_prev:
                    is_hit = True
                    detail = f"Planets {planets_prev} in 12th from Moon (House {h_prev})."
            elif "Durdhara Yoga" in sub:
                m_h = p_house["Moon"]
                h_next = (m_h % 12) + 1
                h_prev = ((m_h - 2 + 12) % 12) + 1
                pn = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if p_house[p] == h_next]
                pp = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if p_house[p] == h_prev]
                if pn and pp:
                    is_hit = True
                    detail = f"Planets flanking Moon: {pn} in 2nd and {pp} in 12th."
            elif "Gajakesari" in sub:
                m_h = p_house["Moon"]
                j_h = p_house["Jupiter"]
                rel = (j_h - m_h + 12) % 12 + 1
                if rel in {1, 4, 7, 10}:
                    is_hit = True
                    detail = f"Jupiter in Kendra ({rel}th) from Moon."
            elif "Panchamahapurusha" in sub or "Mahapurusha" in sub:
                for pl, yname in [("Mars", "Ruchaka"), ("Mercury", "Bhadra"), ("Jupiter", "Hamsa"), ("Venus", "Malavya"), ("Saturn", "Shasha")]:
                    if yname in sub and p_house[pl] in {1, 4, 7, 10} and (pl in exalted_planets or pl in own_sign_planets):
                        is_hit = True
                        detail = f"{pl} exalted/swakshetra in Kendra house {p_house[pl]} forming {yname} Yoga."
            elif "Vipareeta" in sub or "Viparita" in sub:
                l6, l8, l12 = h_lords[6], h_lords[8], h_lords[12]
                if "Harsha" in sub and p_house[l6] in {6, 8, 12}:
                    is_hit = True
                    detail = f"6th lord {l6} placed in dusthana house {p_house[l6]} forming Harsha VRY."
                elif "Sarala" in sub and p_house[l8] in {6, 8, 12}:
                    is_hit = True
                    detail = f"8th lord {l8} placed in dusthana house {p_house[l8]} forming Sarala VRY."
                elif "Vimala" in sub and p_house[l12] in {6, 8, 12}:
                    is_hit = True
                    detail = f"12th lord {l12} placed in dusthana house {p_house[l12]} forming Vimala VRY."
            elif "Conjunction" in sub or "Budhaditya" in sub:
                m_cj = re.search(r"(\w+)-(\w+)\s+Conjunction", sub)
                if m_cj:
                    p1, p2 = m_cj.group(1), m_cj.group(2)
                    if p1 in p_house and p2 in p_house and p_house[p1] == p_house[p2]:
                        is_hit = True
                        detail = f"{p1} and {p2} conjunct in house {p_house[p1]}."
            elif "Lord in" in sub:
                m_li = re.search(r"(\d+)(?:st|nd|rd|th)?\s+Lord\s+in\s+(\d+)(?:st|nd|rd|th)?\s+House", sub)
                if m_li:
                    lh, th = int(m_li.group(1)), int(m_li.group(2))
                    if p_house[h_lords[lh]] == th:
                        is_hit = True
                        detail = f"{lh}th lord {h_lords[lh]} placed in house {th}."
            elif "Lord Conjuncted with" in sub:
                m_lc = re.search(r"(\d+)(?:st|nd|rd|th)?\s+Lord\s+Conjuncted\s+with\s+(\d+)(?:st|nd|rd|th)?\s+Lord", sub)
                if m_lc:
                    lh1, lh2 = int(m_lc.group(1)), int(m_lc.group(2))
                    if p_house[h_lords[lh1]] == p_house[h_lords[lh2]]:
                        is_hit = True
                        detail = f"{lh1}th lord {h_lords[lh1]} conjunct {lh2}th lord {h_lords[lh2]} in house {p_house[h_lords[lh1]]}."
            elif "Centenarian" in sub or "Long Life" in sub:
                if "Rule 4" in sub and p_house["Jupiter"] == 1:
                    is_hit = True
                    detail = "Jupiter posited in Lagna granting paramount longevity."
                elif "Rule 5" in sub and p_house["Jupiter"] == 1 and p_house["Moon"] == 1:
                    is_hit = True
                    detail = "Jupiter-Moon Gajakesari in Lagna."

        # ---------------------------------------------------------
        # 4. Jaimini Upadesha Sutras
        # ---------------------------------------------------------
        elif "Jaimini Upadesha" in cat:
            sub = item.get("sub_category", "")
            if "Amatyakaraka conjunct Atmakaraka" in cond_str:
                if p_house.get(ak_planet) == p_house.get(amk_planet):
                    is_hit = True
                    detail = f"Atmakaraka ({ak_planet}) and Amatyakaraka ({amk_planet}) conjunct in house {p_house[ak_planet]}."
            elif "Atmakaraka in Karakamsa" in sub:
                # Ak sign
                ak_s = p_sign.get(ak_planet, 0)
                ak_s_name = SIGNS_EN[ak_s].lower()
                if ak_s_name in cond_str.lower():
                    is_hit = True
                    detail = f"Atmakaraka ({ak_planet}) occupies {SIGNS_EN[ak_s]} Karakamsa."
            elif "from Arudha Lagna" in cond_str:
                m_al = re.search(r"(\d+)(?:st|nd|rd|th)?\s+from\s+Arudha\s+Lagna", cond_str, re.I)
                if m_al:
                    rel_al = int(m_al.group(1))
                    target_h_al = ((al_house + rel_al - 2) % 12) + 1
                    benefics_in_target = [p for p in ["Jupiter", "Venus", "Mercury"] if p_house[p] == target_h_al]
                    if benefics_in_target:
                        is_hit = True
                        detail = f"Benefics {benefics_in_target} in {rel_al}th from Arudha Lagna (House {target_h_al})."

        # ---------------------------------------------------------
        # 5. Dasha & Gochara Phala
        # ---------------------------------------------------------
        elif "Dasha" in cat:
            sub = item.get("sub_category", "")
            if current_dasha and "Mahadasha" in sub:
                cur_md, cur_ad = current_dasha
                # cond_str: e.g. "Vimshottari Dasha: Sun Mahadasha with Moon Antardasha"
                if f"{cur_md} Mahadasha" in cond_str and f"{cur_ad} Antardasha" in cond_str:
                    is_hit = True
                    detail = f"Active Vimshottari Dasha: {cur_md} MD - {cur_ad} AD."
            elif current_transits and "Gochara" in sub:
                # check transits from Moon
                m_h = p_house["Moon"]
                for p_t, cur_t_sign in current_transits.items():
                    rel_from_moon = (cur_t_sign - p_sign["Moon"] + 12) % 12 + 1
                    # match: "Jupiter Transit 1st House from Moon" or "Saturn Transit 3rd House from Moon"
                    pat = f"{p_t} Transit {rel_from_moon}"
                    if pat.lower() in cond_str.lower():
                        is_hit = True
                        detail = f"Transit of {p_t} in {rel_from_moon}th house from Natal Moon."

        # ---------------------------------------------------------
        # 6. Bhrigu Nandi Nadi (BNN)
        # ---------------------------------------------------------
        elif "Bhrigu Nandi Nadi" in cat:
            # Check sign placement
            m_sign = re.search(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b\s+(?:is\s+)?in\s+([A-Za-z]+)", cond_str)
            if m_sign:
                pl_n, s_n = m_sign.group(1).capitalize(), m_sign.group(2).lower()
                if s_n in SIGN_MAP and p_sign.get(pl_n) == SIGN_MAP[s_n]:
                    is_hit = True
                    detail = f"{pl_n} is placed in {SIGNS_EN[SIGN_MAP[s_n]]}."
            
            # Check planetary conjunction / contact
            if not is_hit:
                m_conj = re.search(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b\s+(?:with|touches|conjunct|and)\s+\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b", cond_str)
                if m_conj:
                    p1, p2 = m_conj.group(1).capitalize(), m_conj.group(2).capitalize()
                    # In Nadi, conjunction or 1-5-9 trinal link constitutes contact
                    h1 = p_house.get(p1, 0)
                    h2 = p_house.get(p2, 0)
                    if h1 == h2:
                        is_hit = True
                        detail = f"{p1} and {p2} in mutual conjunction in house {h1}."
                    elif (h2 - h1 + 12) % 12 in {4, 8}:
                        is_hit = True
                        detail = f"{p1} and {p2} in trinal Nadi contact (1-5-9 axis)."

            # Check house relative to planet
            if not is_hit:
                m_hrel = re.search(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b.*?(?:in|to|from).*?(\d+)(?:st|nd|rd|th)?\s+house", cond_str, re.I)
                m_p2 = re.search(r"having\s+\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b", cond_str, re.I)
                if m_hrel and m_p2:
                    p1 = m_hrel.group(1).capitalize()
                    target_rel = int(m_hrel.group(2))
                    p2 = m_p2.group(1).capitalize()
                    rel_calc = (p_house.get(p2, 0) - p_house.get(p1, 0) + 12) % 12 + 1
                    if rel_calc == target_rel:
                        is_hit = True
                        detail = f"{p2} is in {target_rel}th house from {p1}."

        if is_hit and sid not in seen_ids:
            seen_ids.add(sid)
            matched.append(MatchedSutra(
                sutra_id=sid,
                category=cat,
                sub_category=item.get("sub_category", ""),
                primary_factor=pf,
                planetary_condition=cond_str,
                condition_hi=item.get("condition_hi", ""),
                prediction_en=item.get("prediction_en", ""),
                prediction_hi=item.get("prediction_hi", ""),
                life_domain=item.get("life_domain", "General Life Pattern"),
                source=item.get("source", "Classical Jyotish"),
                strength_modifiers=item.get("strength_modifiers", ""),
                matched_detail=detail
            ))

    return matched

def synthesize_knowledge_predictions(chart, current_dasha: Optional[Tuple[str, str]] = None) -> Dict[str, Any]:
    """
    Synthesizes evaluated knowledge sutras into thematic life-domain chapters.
    """
    matched = evaluate_chart_sutras(chart, current_dasha=current_dasha)
    
    by_domain: Dict[str, List[MatchedSutra]] = {}
    by_category: Dict[str, List[MatchedSutra]] = {}

    for m in matched:
        by_domain.setdefault(m.life_domain, []).append(m)
        by_category.setdefault(m.category, []).append(m)

    return {
        "total_active_sutras": len(matched),
        "all_matched": matched,
        "by_domain": by_domain,
        "by_category": by_category,
    }
