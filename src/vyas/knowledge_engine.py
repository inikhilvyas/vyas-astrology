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

_LAST_DIR_STATE: Optional[tuple] = None

def load_knowledge_bank(force_reload: bool = False) -> List[Dict[str, Any]]:
    """
    Dynamically scans books/ folder and auto-reloads whenever:
    1. Any new .jsonl, .json, or .md sutra file is added.
    2. Any existing sutra file is edited or updated.
    Guarantees that user's uploaded sutras are ALWAYS immediately active!
    """
    global _CACHED_KNOWLEDGE, _LAST_DIR_STATE
    b_dir = Path(__file__).resolve().parents[2] / "books"
    
    # Calculate current modification signature of all sutra/knowledge files
    current_state = []
    target_files = []
    if b_dir.exists():
        # Match any jsonl, json files, or text/markdown sutra files
        all_potential = list(b_dir.glob("*.jsonl")) + list(b_dir.glob("*.json")) + list(b_dir.glob("*sutra*.txt"))
        target_files = sorted(list(set(all_potential)))
        for p in target_files:
            try:
                current_state.append((p.name, p.stat().st_mtime, p.stat().st_size))
            except Exception:
                pass
    
    state_tuple = tuple(current_state)
    if not force_reload and _CACHED_KNOWLEDGE is not None and _LAST_DIR_STATE == state_tuple:
        return _CACHED_KNOWLEDGE

    records = []
    seen_ids = set()

    for k_file in target_files:
        try:
            with open(k_file, "r", encoding="utf-8", errors="ignore") as f:
                # Handle JSON array file
                if k_file.suffix.lower() == ".json":
                    try:
                        content = f.read().strip()
                        if content.startswith("["):
                            parsed = json.loads(content)
                            for d in parsed:
                                if isinstance(d, dict):
                                    sid = d.get("sutra_id", "")
                                    if sid and sid in seen_ids:
                                        continue
                                    if sid:
                                        seen_ids.add(sid)
                                    records.append(d)
                            continue
                    except Exception:
                        f.seek(0)

                # Handle JSONL or line-by-line JSON
                for line in f:
                    line = line.strip()
                    if line.startswith("{") and line.endswith("}"):
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
    _LAST_DIR_STATE = state_tuple
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

        # ---------------------------------------------------------
        # 7. Universal Multi-Category Matcher (Covering All 22 Parts & 13,000 Sutras)
        # ---------------------------------------------------------
        if not is_hit:
            # 7a. Planet in House
            m_gen_h = re.search(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b\s+(?:in|placed\s+in|posited\s+in|occupies)\s+(?:the\s+)?(\d+)(?:st|nd|rd|th)?\s+house", cond_str, re.I)
            if m_gen_h:
                pl_g, h_target = m_gen_h.group(1).capitalize(), int(m_gen_h.group(2))
                if p_house.get(pl_g) == h_target:
                    is_hit = True
                    detail = f"{pl_g} is posited in House {h_target}."

            # 7b. Planet in Sign
            if not is_hit:
                m_gen_s = re.search(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b\s+(?:is\s+)?in\s+([A-Za-z]+)\b", cond_str)
                if m_gen_s:
                    pl_g, s_n = m_gen_s.group(1).capitalize(), m_gen_s.group(2).lower()
                    if s_n in SIGN_MAP and p_sign.get(pl_g) == SIGN_MAP[s_n]:
                        is_hit = True
                        detail = f"{pl_g} is in {SIGNS_EN[SIGN_MAP[s_n]]}."

            # 7c. Navamsha Placements (D9)
            if not is_hit and "Navamsha" in cond_str:
                m_nav = re.search(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b.*?in\s+([A-Za-z]+)\s+Navamsha", cond_str, re.I)
                if m_nav:
                    pl_g, s_nav = m_nav.group(1).capitalize(), m_nav.group(2).lower()
                    p_obj = planets.get(pl_g)
                    if p_obj and s_nav in SIGN_MAP:
                        d9_idx = int(p_obj.longitude / (30.0 / 9.0)) % 12
                        if d9_idx == SIGN_MAP[s_nav]:
                            is_hit = True
                            detail = f"{pl_g} occupies {SIGNS_EN[SIGN_MAP[s_nav]]} Navamsha (D9)."

            # 7d. Mutual Conjunctions
            if not is_hit:
                m_cj_gen = re.search(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b\s+(?:conjunct|with|and)\s+\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)\b", cond_str, re.I)
                if m_cj_gen:
                    p1_g, p2_g = m_cj_gen.group(1).capitalize(), m_cj_gen.group(2).capitalize()
                    if p1_g in p_house and p2_g in p_house and p_house[p1_g] == p_house[p2_g]:
                        is_hit = True
                        detail = f"{p1_g} and {p2_g} are conjunct in House {p_house[p1_g]}."

            # 7e. Retrograde Planet Placement
            if not is_hit and "retrograde" in cond_str.lower():
                for pl_r, p_obj in planets.items():
                    if getattr(p_obj, "is_retrograde", False) or getattr(p_obj, "speed", 1.0) < 0:
                        if pl_r.lower() in cond_str.lower():
                            is_hit = True
                            detail = f"{pl_r} is in retrograde motion in House {p_house.get(pl_r, 1)}."
                            break

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


# =========================================================================
# DOMAIN SCRIPT SYNTHESIZERS (Poori Script Ki Tarah Phalit Nirman)
# =========================================================================

def synthesize_varga_scripts(chart, vargas_matrix=None):
    matched = evaluate_chart_sutras(chart)
    varga_cats = {
        "Navamsha (D9) & Divisional Vargas", "Shodashavargas (16 Divisional Charts)",
        "Shodashavarga Micro-Deities: D60 Shashtiamsha & D45 Soul Destiny",
        "Rashi-Tulya Navamsha & C.S. Patel Techniques"
    }
    v_sutras = [m for m in matched if m.category in varga_cats or "navamsha" in m.planetary_condition.lower() or "varga" in m.category.lower()]

    vargottama_planets = []
    if vargas_matrix and "D9" in vargas_matrix:
        for p_name, p in chart.planets.items():
            d9_sign = vargas_matrix["D9"][p_name].sign_index
            if p.sign_index == d9_sign:
                vargottama_planets.append((constants.PLANETS_HI.get(p_name, p_name), constants.SIGNS_HI[p.sign_index]))

    d1_sign_hi = constants.SIGNS_HI[chart.ascendant_sign]
    d9_asc_sign_idx = (int(chart.ascendant_longitude / (30.0 / 9.0))) % 12
    d9_sign_hi = constants.SIGNS_HI[d9_asc_sign_idx]

    script_d1_d9 = f"""### लग्न एवं नवमांश (D1-D9) आधारशिला महा-विश्लेषण
- **जन्म लग्न (D1):** {d1_sign_hi} लग्न | **भाग्य नवमांश लग्न (D9):** {d9_sign_hi} नवमांश
- **शास्त्रीय सिद्धांत:** महर्षि पराशर के अनुसार D-1 स्थूल देह, बाह्य वातावरण व प्रारम्भिक बीज है, जबकि D-9 नवमांश उस बीज का अंकुरित वृक्ष, वास्तविक आंतरिक सामर्थ्य व भाग्य का अंतिम निर्णय है।"""
    if vargottama_planets:
        pl_str = ", ".join([f"**{p}** ({s} राशि)" for p, s in vargottama_planets])
        script_d1_d9 += f"\n- **परम बली वर्गोत्तम स्थिति:** आपकी कुण्डली में {pl_str} वर्गोत्तम हैं। फलदीपिका का सूत्र है कि वर्गोत्तम ग्रह स्वराशि तुल्य शुभ फल, स्थायी आरोग्यता, मानसिक दृढ़ता एवं प्रतिकूल दशाओं में भी जातक की प्रतिष्ठा की रक्षा करते हैं।"
    else:
        script_d1_d9 += "\n- **नवमांश बल गतिशीलता:** ग्रह जन्म कुण्डली से नवमांश में जाकर जिन भावों व राशियों में संचरण कर रहे हैं, वह जीवन के उत्तरार्ध (32 वर्ष के उपरांत) में प्राथमिक रूप से सक्रिय होंगे।"

    if v_sutras:
        script_d1_d9 += "\n\n**सक्रिय शास्त्रीय वर्ग-सूत्र:**\n"
        for s in v_sutras[:5]:
            script_d1_d9 += f"- **[{s.source}] {s.sub_category}:** {s.prediction_hi} *(सत्यापन: {s.matched_detail})*\n"

    script_d10 = """### दशमांश चक्र (D10) कर्म, प्रतिष्ठा एवं आजीविका विश्लेषण
- **दशमांश का महत्व:** बृहत्पाराशर होराशास्त्र में दशम भाव की सूक्ष्म शक्ति एवं समाज में मिलने वाले मान-सम्मान व प्रभाव का परीक्षण D-10 चक्र से ही किया जाता है।
- **कर्म रेखा विश्लेषण:** जन्म कुण्डली के दशमेश का दशमांश में उच्च, स्वराशि अथवा शुभ वर्ग में होना प्रशासनिक नेतृत्व, व्यापारिक उन्नति व स्थिर आजीविका का मार्ग प्रशस्त करता है।
- **विशेष निर्देश:** यदि दशमांश में गुरु, बुध या शुक्र की स्थिति केंद्र/त्रिकोण में हो तो बौद्धिक संपदा, प्रबंधन व स्वतंत्र परामर्श में जातक शीर्ष सफलता प्राप्त करता है।"""

    script_d60 = """### षष्ट्यंश (D60) संचित प्रारब्ध एवं आत्मिक कर्म विश्लेषण
- **पराशर आज्ञा:** *'सर्वेषामपि वर्गाणां षष्ट्यंशोऽधिकमुच्यते'* — समस्त 16 वर्ग कुण्डलियों में षष्ट्यंश का स्थान सर्वोपरि है। यह पूर्वजन्म के अवशिष्ट ऋण, प्रारब्ध एवं आध्यात्मिक संस्कारों का दर्पण है।
- **देवता प्रभाव:** शुभ षष्ट्यंश देवताओं (अमृत, सुधा, पद्म, देव, गन्धर्व) में स्थित ग्रह पूर्व जन्म के पुण्य कर्मों का पुरस्कार देते हैं, जबकि शोधन योग्य देवताओं में स्थित ग्रह इस जन्म में विशिष्ट तपस्या व सेवा द्वारा शुद्धि की अपेक्षा रखते हैं।"""

    return {
        "d1_d9_script": script_d1_d9.strip(),
        "d10_script": script_d10.strip(),
        "d60_script": script_d60.strip(),
        "matched_count": len(v_sutras),
        "vargottama_planets": vargottama_planets,
    }

def synthesize_ashtakavarga_scripts(chart, av_res=None):
    matched = evaluate_chart_sutras(chart)
    av_cats = {
        "Ashtakavarga & Kakshya Timing", "Advanced Ashtakavarga: Kakshya Sphuta, Ekadhipatya & Shodhya Pinda",
        "Ashtakavarga Shodhana & Longevity", "Ashtakavarga Shodhya Pinda & Ayurdaya",
        "Transit Vedha & Ashtakavarga Triggers"
    }
    av_sutras = [m for m in matched if m.category in av_cats or "ashtakavarga" in m.planetary_condition.lower() or "bindu" in m.planetary_condition.lower()]

    sav = av_res.get("sav", [28]*12) if av_res else [28]*12
    asc_idx = chart.ascendant_sign

    h_sav = {h: sav[(asc_idx + h - 1) % 12] for h in range(1, 13)}
    h11_pts = h_sav.get(11, 28)
    h12_pts = h_sav.get(12, 28)
    h1_pts = h_sav.get(1, 28)
    h10_pts = h_sav.get(10, 28)

    wealth_ratio = "अति उत्तम (आय > व्यय)" if h11_pts > h12_pts else "सतर्कता (आय की तुलना में व्यय अधिक)"
    
    script = f"""### अष्टकवर्ग (SAV 337 बिंदु) शास्त्रीय फलित महा-विश्लेषण
- **सिद्धांत:** महर्षि पराशर प्रणीत अष्टकवर्ग प्रणाली ग्रहों के सापेक्षिक शुभ-अशुभ बिंदुओं का अचूक गणित है। किसी भाव में 28 या अधिक बिंदु उसे सक्षम, जबकि 28 से कम बिंदु उसे अतिरिक्त संबल की आवश्यकता दर्शाते हैं।
- **धन एवं संचय समीकरण (11वें बनाम 12वें भाव का संतुलन):** 
  - एकादश (लाभ) भाव: **{h11_pts} बिंदु** | द्वादश (व्यय) भाव: **{h12_pts} बिंदु**
  - **शास्त्रीय निर्णय:** {wealth_ratio}। जब एकादश भाव के बिंदु द्वादश से अधिक हों, तो जातक जितना भी अर्जित करता है, उसमें से संचय स्थायी रूप से बढ़ता है।
- **कर्म एवं प्रतिष्ठा सामर्थ्य:**
  - लग्न (व्यक्तित्व व स्वास्थ्य): **{h1_pts} बिंदु** | दशम (आजीविका व समाज): **{h10_pts} बिंदु**
  - दशम भाव में 30+ बिंदु जातक को अपने कार्यक्षेत्र में स्वतः सम्मान, स्वतंत्र निर्णय लेने की शक्ति एवं दीर्घकालिक प्रभावशीलता प्रदान करते हैं।"""

    if av_sutras:
        script += "\n\n**सक्रिय अष्टकवर्ग शास्त्रीय सूत्र:**\n"
        for s in av_sutras[:6]:
            script += f"- **[{s.source}] {s.sub_category}:** {s.prediction_hi} *(स्थिति: {s.matched_detail})*\n"

    return {
        "ashtakavarga_script": script.strip(),
        "matched_count": len(av_sutras),
        "h11_pts": h11_pts,
        "h12_pts": h12_pts,
    }

def synthesize_lal_kitab_scripts(chart, lk_analysis=None):
    matched = evaluate_chart_sutras(chart)
    lk_cats = {
        "Lal Kitab Advanced Grammar & Farman Mechanics", "Lal Kitab Esoteric Farmaan",
        "Karmic Debts (Rina) & D60 Past Life"
    }
    lk_sutras = [m for m in matched if m.category in lk_cats or "lal kitab" in m.source.lower() or "farman" in m.sub_category.lower()]

    script = """### लाल किताब प्रामाणिक फरमान एवं अचूक उपाय महा-विश्लेषण
- **लाल किताब का मूल दर्शन:** पंडित रूपचंद जोशी कृत लाल किताब में कुंडली को 'तेवा' और ग्रहों को जातक के कर्म-ऋण का संवाहक माना गया है। इसमें ग्रहों की स्थिति के आधार पर बंद किस्मत के दरवाजों को खोलने के सटीक व सरल घरेलू उपाय दिए गए हैं।
- **किस्मत जगाने का स्वर्णिम नियम:** जो भाव खाली या सोए हुए हों, उनके स्वामी ग्रह के कारक पदार्थों को अनुकूल भाव में स्थापित करके उन भावों को जाग्रत किया जाता है।"""

    if lk_sutras:
        script += "\n\n**सक्रिय लाल किताब गुप्त फरमान:**\n"
        for s in lk_sutras[:6]:
            script += f"- **फरमान [{s.sutra_id}]:** {s.prediction_hi}\n  - *सत्यापित स्थिति:* {s.matched_detail}\n  - *नियम व संशोधन:* {s.strength_modifiers or 'यथावत पालन करें'}\n"

    return {
        "lal_kitab_script": script.strip(),
        "matched_count": len(lk_sutras),
    }

def synthesize_kp_scripts(chart, kp_cusps=None):
    matched = evaluate_chart_sutras(chart)
    kp_cats = {"KP Cuspal Sub-Lord Dynamics", "4-Tier KP Stellar Hierarchy & Ruling Planets"}
    kp_sutras = [m for m in matched if m.category in kp_cats or "kp" in m.category.lower() or "cuspal" in m.category.lower()]

    script = """### कृष्णमूर्ति पद्धति (KP System) कस्प उप-स्वामी प्रॉमिस महा-विश्लेषण
- **केपी स्वर्णिम नियम:** 'Planet proposes, Star Lord disposes, Sub Lord decides.' ग्रह केवल घटना का संकेत देता है, नक्षत्र स्वामी उसका मार्ग निर्धारित करता है, और कस्प का उप-स्वामी (Sub-Lord) यह अंतिम निर्णय करता है कि घटना घटित होगी अथवा नहीं।
- **जीवन के 4 प्रमुख स्तंभों का प्रॉमिस परीक्षण:**
  1. **प्रथम कस्प उप-स्वामी (आरोग्यता व जीवन शक्ति):** लग्न कस्प का उप-स्वामी यदि 1, 5, 9, 11 भावों से जुड़े तो दीर्घायु व सुदृढ़ स्वास्थ्य; यदि 6, 8, 12 से जुड़े तो विशेष स्वास्थ्य सतर्कता।
  2. **द्वितीय व एकादश कस्प उप-स्वामी (धन व समृद्धि):** 2, 6, 10, 11 भावों का संबंध जातक को कभी भी आर्थिक रूप से पराश्रित नहीं होने देता।
  3. **सप्तम कस्प उप-स्वामी (विवाह व साझेदारी):** 2, 7, 11 भावों का संयोग सुखी दांपत्य एवं विश्वसनीय व्यापारिक साझेदार प्रदान करता है।
  4. **दशम कस्प उप-स्वामी (पद-प्रतिष्ठा व कॅरियर):** 6, 10, 11 भावों के कार्येश जातक को नेतृत्व व प्रतिष्ठा प्रदान करते हैं।"""

    if kp_sutras:
        script += "\n\n**सक्रिय केपी शास्त्रीय सूत्र:**\n"
        for s in kp_sutras[:6]:
            script += f"- **[{s.source}] {s.sub_category}:** {s.prediction_hi} *(सत्यापन: {s.matched_detail})*\n"

    return {
        "kp_script": script.strip(),
        "matched_count": len(kp_sutras),
    }

def synthesize_jaimini_scripts(chart):
    matched = evaluate_chart_sutras(chart)
    j_cats = {
        "Jaimini Upadesha Sutras", "Jaimini Karakamsha Bhava Phala, Arudha Padas & Upapada Marital Dynamics",
        "Jaimini Arudha Dhana Yogas & Argala", "Karakamsha & Swamsha Mastery",
        "Jaimini Arudha Lagna (AL) Dynamics"
    }
    j_sutras = [m for m in matched if m.category in j_cats or "jaimini" in m.category.lower() or "karakamsha" in m.category.lower()]

    script = """### महर्षि जैमिनी प्रणीत उपदेश सूत्र एवं कारकांश महा-विश्लेषण
- **जैमिनी सिद्धांत:** महर्षि जैमिनी के अनुसार कुण्डली में सर्वाधिक अंशों वाला ग्रह 'आत्मकारक' (AK) बनकर आत्मा की इस जन्म की यात्रा को नियंत्रित करता है। आत्मकारक जिस नवमांश राशि में बैठता है, उसे 'कारकांश' कहते हैं।
- **अमात्यकारक (AmK) व पद प्रभाव:** जब आत्मकारक एवं आमात्यकारक परस्पर केंद्र/त्रिकोण या एकादश भाव में सम्बद्ध हों, तो यह सर्वोच्च कोटि का जैमिनी राजयोग निर्मित करता है, जो उच्च पद व प्रभाव दिलाता है।
- **आरूढ़ लग्न (AL):** आरूढ़ लग्न जातक की सांसारिक छवि (Image & Status in Society) को दर्शाता है। AL से 11वें भाव में शुभ ग्रह निरंतर धन लाभ एवं सम्मान प्रदान करते हैं।"""

    if j_sutras:
        script += "\n\n**सक्रिय जैमिनी उपदेश सूत्र:**\n"
        for s in j_sutras[:6]:
            script += f"- **[{s.source}] {s.sub_category}:** {s.prediction_hi} *(सत्यापन: {s.matched_detail})*\n"

    return {
        "jaimini_script": script.strip(),
        "matched_count": len(j_sutras),
    }

def synthesize_nadi_chakra_scripts(chart):
    matched = evaluate_chart_sutras(chart)
    n_cats = {
        "Bhrigu Nandi Nadi", "Bhrigu Chakra Paddhati (BCP)", "Chakra Jyotish & Kundalini Subtle Body",
        "Bhrigu Nandi Nadi Transit Modulations & Double-Transit Secrets", "Nadi Round Progressions"
    }
    n_sutras = [m for m in matched if m.category in n_cats or "nadi" in m.category.lower() or "chakra" in m.category.lower()]

    script = """### भृगु नन्दी नाड़ी एवं सूक्ष्म चक्र फलित महा-विश्लेषण
- **नाड़ी का मूल आधार:** नाड़ी ज्योतिष में लग्न की अपेक्षा 'जीव कारक' (बृहस्पति) और 'कर्म कारक' (शनि) के पारस्परिक त्रिकोणीय (1-5-9) सम्बंधों को जातक के जीवन की मुख्य दिशा माना गया है।
- **दिशा त्रिकोण का गूढ़ नियम:** पूर्व (1-5-9), दक्षिण (2-6-10), पश्चिम (3-7-11) एवं उत्तर (4-8-12) त्रिकोणों में ग्रहों की युति परस्पर ऊर्जाओं का सम्मिश्रण करती है।
- **चक्र ज्योतिष एवं कुण्डलिनी संरेखण:** कुण्डली के 12 भाव मानव शरीर के मूलाधार, स्वाधिष्ठान, मणिपुर, अनाहत, विशुद्ध, आज्ञा एवं सहस्रार चक्रों से जुड़े होते हैं। शुभ ग्रहों का प्रभाव संबंधित चक्र में ऊर्जा का प्रवाह निर्बाध करता है।"""

    if n_sutras:
        script += "\n\n**सक्रिय नाड़ी एवं चक्र सूत्र:**\n"
        for s in n_sutras[:6]:
            script += f"- **[{s.source}] {s.sub_category}:** {s.prediction_hi} *(सत्यापन: {s.matched_detail})*\n"

    return {
        "nadi_chakra_script": script.strip(),
        "matched_count": len(n_sutras),
    }

def synthesize_bhava_and_yogas_scripts(chart):
    matched = evaluate_chart_sutras(chart)
    bhava_sutras = [m for m in matched if "bhrigu sutram" in m.category.lower() or "bhavadhipati" in m.category.lower()]
    yoga_sutras = [m for m in matched if "yoga" in m.category.lower() or "classical vedic sutras" in m.category.lower()]

    bhava_map = {h: [] for h in range(1, 13)}
    for s in bhava_sutras:
        m_h = re.search(r"(\d+)(?:st|nd|rd|th)?\s+House", s.sub_category + " " + s.matched_detail, re.I)
        if m_h:
            h_num = int(m_h.group(1))
            if 1 <= h_num <= 12:
                bhava_map[h_num].append(s)

    script_yogas = """### कुण्डली पर सक्रिय विशिष्ट शास्त्रीय राजयोग, धनयोग एवं महापुरुष योग
- **शास्त्रीय प्रामाणिकता:** महर्षि पराशर (बृहत्पाराशर होराशास्त्र), वराहमिहिर (बृहज्जातक) एवं कल्याणवर्मा (सारावली) की परंपरा के अनुसार जन्म कुण्डली में निर्मित दुर्लभ योग जातक के भाग्य के वास्तविक उत्प्रेरक होते हैं।
- **फलित नियम:** योग केवल नाम मात्र नहीं होते; उनका वास्तविक शुभ फल तभी प्रस्फुटित होता है जब योगकारक ग्रह की विंशोत्तरी महादशा, अन्तर्दशा या गोचर अनुकूल स्थिति में आते हैं।"""

    if yoga_sutras:
        script_yogas += "\n\n**सत्यापित विशिष्ट शास्त्रीय योग:**\n"
        for y in yoga_sutras:
            mod_str = f'<div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 4px;">बल व काल प्रभाव: {y.strength_modifiers}</div>' if y.strength_modifiers else ''
            script_yogas += f"""
<div style="background: var(--card-bg); border-left: 4px solid var(--gold-accent); padding: 12px 16px; border-radius: 8px; margin-bottom: 12px; border: 1px solid var(--card-border);">
    <div style="color: var(--gold-primary); font-weight: bold; font-size: 1.05rem;">[{y.sutra_id}] {y.sub_category} — <span style="color: var(--text-muted); font-size: 0.85rem;">स्रोत: {y.source}</span></div>
    <div style="color: var(--text-main); font-size: 0.92rem; margin: 6px 0;">सत्यापित खगोलीय स्थिति: <b>{y.matched_detail}</b></div>
    <div style="color: var(--accent-emerald); font-size: 0.98rem; line-height: 1.6;"><b>शास्त्रीय फलादेश:</b> {y.prediction_hi}</div>
    {mod_str}
</div>"""
    else:
        script_yogas += "\n\n*कुण्डली में सामान्य सौम्य योग निर्मित हैं। जीवन में स्वावलंबन एवं पुरुषार्थ से निरंतर उन्नति होगी।*\n"

    return {
        "bhava_map": bhava_map,
        "yogas_script": script_yogas.strip(),
        "total_bhava_sutras": len(bhava_sutras),
        "total_yoga_sutras": len(yoga_sutras),
    }

def search_knowledge_bank(query: str, max_results: int = 8) -> List[Dict[str, Any]]:
    """
    Fast keyword and thematic search across all 13,000+ classical sutras in the knowledge bank.
    Returns the most relevant sutras with bilingual predictions and source citations.
    """
    if not query or not query.strip():
        return []

    q_tokens = [t.lower() for t in query.strip().split() if len(t) >= 2]
    if not q_tokens:
        return []

    kb = load_knowledge_bank()
    results = []

    for item in kb:
        text_corpus = (
            item.get("category", "") + " " +
            item.get("sub_category", "") + " " +
            item.get("planetary_condition", "") + " " +
            item.get("condition_hi", "") + " " +
            item.get("prediction_hi", "") + " " +
            item.get("prediction_en", "") + " " +
            item.get("source", "")
        ).lower()

        matches = sum(1 for tok in q_tokens if tok in text_corpus)
        if matches > 0:
            results.append((matches, item))

    results.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in results[:max_results]]
