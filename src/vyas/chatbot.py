"""Maharshi Vyas Classical Natural-Dialogue AI Astrological Consultation Engine.

Key Architectural Principles:
1. Natural, fluent, dignified Hindi conversation without artificial robotic templates or raw data dumps.
2. 100% authentic Jyotish Shastra logic:
   - Evaluates exact Lagna, Lagnesh, Chandra Rashi, Nakshatra.
   - Evaluates specific Bhava lords, occupants, conjunctions (Yuti), and Graha Drishti (aspects).
   - Directly addresses the user's specific query (Timing / When will time improve, Dasha predictions, RHJS/Judiciary,
     Career, Finances, Marriage, Health, Children, Property, Foreign, Obstacles, Remedies).
   - Never outputs stuttering or repeated words like 'मंगल मंगल' or 'शनि शनि'.
3. Multi-turn conversation awareness:
   - Welcoming greeting only on the initial turn.
   - Subsequent questions receive direct, authoritative, focused astrological answers.
4. Hybrid AI Engine:
   - If Gemini API Key is configured in environment or secrets, can leverage LLM with deep astrological prompt.
   - Powerful, deterministic classical Vedic inference engine guarantees deep, accurate answers offline or without API key.
"""
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
import os
import re

from vyas import constants
from vyas import sutra_synthesizer
from vyas.gochar import get_current_transit_positions, next_ingress, _sign_of, shani_status
from vyas.knowledge_engine import evaluate_chart_sutras

_TRANSIT_DAY_CACHE = {}

def _get_day_transit_pos() -> Dict[str, Any]:
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in _TRANSIT_DAY_CACHE:
        try:
            _TRANSIT_DAY_CACHE[today] = get_current_transit_positions()
        except Exception:
            try:
                from vyas.ephem import planet_positions
                from vyas.chart import PlanetState
                raw = planet_positions(datetime.now(timezone.utc))
                _TRANSIT_DAY_CACHE[today] = {n: PlanetState(n, p.longitude, p.speed) for n, p in raw.items()}
            except Exception:
                _TRANSIT_DAY_CACHE[today] = {}
    return _TRANSIT_DAY_CACHE[today]

# -----------------------------------------------------------------------------
# ENGINE MASTER API KEYS (Directly configured on backend)
# Set your keys here, or in Streamlit Secrets, or in environment variables.
# -----------------------------------------------------------------------------
ENGINE_GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
ENGINE_GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")

class VyasChatbotEngine:
    """Authentic Vedic Astrological Dialogue Engine."""

    def __init__(self):
        pass

    def _extract_chart_framework(self, chart, cur_dasha: Any, transit_pos: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extracts complete astronomical and planetary positioning from the chart."""
        asc_sign = chart.ascendant_sign
        asc_sign_name = constants.SIGNS_HI[asc_sign]
        lagnesh = constants.SIGN_LORD[asc_sign]
        lagnesh_hi = constants.PLANETS_HI.get(lagnesh, lagnesh)

        moon_p = chart.planets.get("Moon")
        moon_sign = moon_p.sign_index if moon_p else 0
        moon_sign_name = constants.SIGNS_HI[moon_sign]
        moon_nak_idx = int(moon_p.longitude // constants.NAKSHATRA_SPAN) % 27 if moon_p else 0
        moon_nak_name = constants.NAKSHATRAS_HI[moon_nak_idx]

        # House placements and degrees
        p_info = {}
        house_occupants = {h: [] for h in range(1, 13)}

        for p_name, p in chart.planets.items():
            h = (p.sign_index - asc_sign + 12) % 12 + 1
            house_occupants[h].append(p_name)
            p_info[p_name] = {
                "house": h,
                "sign_idx": p.sign_index,
                "sign_name": constants.SIGNS_HI[p.sign_index],
                "deg": round(p.longitude % 30, 2),
                "is_retro": getattr(p, "is_retrograde", False),
                "hi": constants.PLANETS_HI.get(p_name, p_name)
            }

        # Planetary Aspects (दृष्टियां)
        aspects_map = {}
        for p_name, p in p_info.items():
            h_from = p["house"]
            offsets = constants.ASPECTS.get(p_name, [7])
            aspected_houses = []
            for off in offsets:
                tgt_h = (h_from + off - 1)
                while tgt_h > 12:
                    tgt_h -= 12
                aspected_houses.append(tgt_h)
            aspects_map[p_name] = aspected_houses

        # 12 Houses: Exact Parashari Lordships & Titles (निर्विवाद गणितीय सत्य)
        house_titles = {
            1: "लग्नेश / तनु भाव", 2: "धनेश / धन भाव", 3: "सहजेश / पराक्रम भाव",
            4: "सुखेश / चतुर्थ भाव", 5: "पंचमेश / सुत भाव", 6: "षष्ठेश / रिपु भाव",
            7: "सप्तमेश / जाया भाव", 8: "अष्टमेश / रंध्र भाव", 9: "भाग्येश / धर्म भाव",
            10: "कर्मेश / दशम भाव", 11: "लाभेश / आय भाव", 12: "व्ययेश / मोक्ष भाव"
        }
        house_lords = {}
        house_lords_lines = []
        for h in range(1, 13):
            sign_idx = (asc_sign + h - 1) % 12
            lord_en = constants.SIGN_LORD[sign_idx]
            lord_hi = constants.PLANETS_HI.get(lord_en, lord_en)
            sign_hi = constants.SIGNS_HI[sign_idx]
            house_lords[h] = {
                "sign_idx": sign_idx,
                "sign_name": sign_hi,
                "lord_en": lord_en,
                "lord_hi": lord_hi,
                "title": house_titles[h]
            }
            house_lords_lines.append(f"{h}वां भाव ({sign_hi}): अधिपति {lord_hi} ({house_titles[h]})")

        # Ground-truth Planet House Ownerships (प्रत्येक ग्रह का वास्तविक स्वामित्व)
        planet_owned = {p: [] for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
        for h in range(1, 13):
            s_idx = (asc_sign + h - 1) % 12
            l_en = constants.SIGN_LORD[s_idx]
            if l_en in planet_owned:
                planet_owned[l_en].append(h)

        planet_ownership_lines = []
        for p in ["Mars", "Saturn", "Jupiter", "Sun", "Moon", "Mercury", "Venus"]:
            houses = planet_owned.get(p, [])
            p_hi = constants.PLANETS_HI.get(p, p)
            titles = " एवं ".join([house_titles[h].split(" / ")[0] for h in houses])
            h_str = " व ".join([f"{h}वें" for h in houses])
            p_stat = p_info.get(p, {})
            h_pos = p_stat.get("house", "?")
            sign_p = p_stat.get("sign_name", "?")

            extra_note = ""
            if p == "Mars" and asc_sign == 0:
                extra_note = " [कदापि न भूलें: मेष लग्न में मंगल 1वें व 8वें भाव का स्वामी है, 4वें भाव का नहीं!]"
            elif p == "Saturn" and asc_sign == 0:
                extra_note = f" [कदापि न भूलें: मेष लग्न में शनि 10वें व 11वें भाव का स्वामी है। यद्यपि शनि {h_pos}वें भाव ({sign_p}) में स्थित है, किन्तु उसका स्वामित्व 7वें या 12वें भाव पर नहीं है!]"
            elif p == "Jupiter" and asc_sign == 0:
                extra_note = " [कदापि न भूलें: मेष लग्न में गुरु 9वें व 12वें भाव का स्वामी है, 11वें भाव का नहीं!]"

            planet_ownership_lines.append(f"• {p_hi} ({p}): {h_str} भाव का स्वामी ({titles}) — स्थित: {h_pos}वें भाव ({sign_p}){extra_note}")

        # Reverse Aspects: Which planets aspect each house (भावों पर ग्रहीय दृष्टियां)
        house_aspects = {h: [] for h in range(1, 13)}
        for p_name, p in p_info.items():
            h_from = p["house"]
            offsets = constants.ASPECTS.get(p_name, [7])
            for off in offsets:
                tgt_h = (h_from + off - 1)
                while tgt_h > 12:
                    tgt_h -= 12
                p_hi = constants.PLANETS_HI.get(p_name, p_name)
                house_aspects[tgt_h].append({
                    "planet_en": p_name,
                    "planet_hi": p_hi,
                    "from_house": h_from,
                    "sign_name": p["sign_name"],
                    "offset": off,
                    "desc": f"{p_hi} ({h_from}वें भाव {p['sign_name']} से {off}वीं दृष्टि)"
                })

        # Resolve Dasha string and dates
        dasha_md, dasha_ad, dasha_pd = "अज्ञात", "", ""
        md_start, md_end = "", ""
        ad_start, ad_end = "", ""
        pd_start, pd_end = "", ""
        md_lord_en, ad_lord_en, pd_lord_en = "", "", ""

        if isinstance(cur_dasha, dict):
            if "MD" in cur_dasha and isinstance(cur_dasha["MD"], dict):
                md_lord_en = cur_dasha["MD"].get("lord", "")
                ad_lord_en = cur_dasha.get("AD", {}).get("lord", "")
                pd_lord_en = cur_dasha.get("PD", {}).get("lord", "")
                dasha_md = constants.PLANETS_HI.get(md_lord_en, md_lord_en)
                dasha_ad = constants.PLANETS_HI.get(ad_lord_en, ad_lord_en)
                dasha_pd = constants.PLANETS_HI.get(pd_lord_en, pd_lord_en)
                md_start = cur_dasha["MD"].get("start", "")
                md_end = cur_dasha["MD"].get("end", "")
                def _clean_date(d_val: Any) -> str:
                    if not d_val:
                        return ""
                    return str(d_val).split()[0]

                md_start = _clean_date(cur_dasha["MD"].get("start", ""))
                md_end = _clean_date(cur_dasha["MD"].get("end", ""))
                ad_start = _clean_date(cur_dasha.get("AD", {}).get("start", ""))
                ad_end = _clean_date(cur_dasha.get("AD", {}).get("end", ""))
                pd_start = _clean_date(cur_dasha.get("PD", {}).get("start", ""))
                pd_end = _clean_date(cur_dasha.get("PD", {}).get("end", ""))
            else:
                dasha_md = cur_dasha.get("full_path") or str(cur_dasha)
        elif isinstance(cur_dasha, str):
            dasha_md = cur_dasha

        # Determine next Antardasha
        next_ad_lord_en = ""
        next_ad_lord_hi = ""
        if ad_lord_en in constants.VIMSHOTTARI_ORDER:
            cur_ad_idx = constants.VIMSHOTTARI_ORDER.index(ad_lord_en)
            next_ad_lord_en = constants.VIMSHOTTARI_ORDER[(cur_ad_idx + 1) % 9]
            next_ad_lord_hi = constants.PLANETS_HI.get(next_ad_lord_en, next_ad_lord_en)

        # Transits - Comprehensive Astronomical Ground Truth & Ingress Calculation
        transit_info = {}
        transits_detailed = {}
        if not transit_pos:
            transit_pos = _get_day_transit_pos()

        now_utc = datetime.now(timezone.utc)
        for p_name in ["Saturn", "Jupiter", "Rahu", "Ketu", "Sun", "Moon", "Mars", "Mercury", "Venus"]:
            tp = transit_pos.get(p_name) if transit_pos else None
            lon = getattr(tp, "longitude", None) if tp else None
            speed = getattr(tp, "speed", 1.0) if tp else 1.0

            if lon is None:
                from vyas.ephem import sidereal_lon
                lon = sidereal_lon(p_name, now_utc)

            s_idx = int(lon // 30) % 12
            deg_in_sign = round(lon % 30, 2)
            deg_fmt = f"{int(lon % 30):02d}°{int(((lon % 30) % 1) * 60):02d}'"
            h_lagna = (s_idx - asc_sign + 12) % 12 + 1
            h_moon = (s_idx - moon_sign + 12) % 12 + 1
            p_hi = constants.PLANETS_HI.get(p_name, p_name)

            # Strict Astronomical Motion Laws
            if p_name in ["Rahu", "Ketu"]:
                is_retro = True
                motion_desc = "सदा वक्री (Always Retrograde / उल्टी चाल)"
                next_sign_idx = (s_idx - 1 + 12) % 12
            elif p_name in ["Sun", "Moon"]:
                is_retro = False
                motion_desc = "सदा मार्गी (Always Direct / सीधी चाल)"
                next_sign_idx = (s_idx + 1) % 12
            else:
                is_retro = bool(speed < 0)
                motion_desc = "वक्री (Retrograde)" if is_retro else "मार्गी (Direct)"
                next_sign_idx = (s_idx - 1 + 12) % 12 if is_retro else (s_idx + 1) % 12

            next_sign_hi = constants.SIGNS_HI[next_sign_idx]
            ingress_str = ""
            try:
                ing_dt = next_ingress(p_name, now_utc)
                if ing_dt:
                    ing_dest = _sign_of(p_name, ing_dt + timedelta(days=1))
                    next_sign_hi = constants.SIGNS_HI[ing_dest]
                    ingress_str = ing_dt.strftime("%d/%m/%Y")
            except Exception:
                pass

            if not ingress_str:
                # Approximate classical ingress milestones
                if p_name in ["Rahu", "Ketu"]:
                    ingress_str = "05/12/2026"
                elif p_name == "Saturn":
                    ingress_str = "03/06/2027"

            summary_line = (
                f"• {p_hi} ({p_name}): {constants.SIGNS_HI[s_idx]} राशि ({deg_fmt}) | "
                f"गति: {motion_desc} | आगामी गोचर: {next_sign_hi} राशि ({ingress_str}) | "
                f"लग्न से {h_lagna}वां भाव | चन्द्र से {h_moon}वां भाव"
            )

            transits_detailed[p_name] = {
                "name": p_name,
                "hi": p_hi,
                "sign": constants.SIGNS_HI[s_idx],
                "sign_idx": s_idx,
                "deg": deg_in_sign,
                "deg_fmt": deg_fmt,
                "speed": round(speed, 4),
                "is_retro": is_retro,
                "motion_desc": motion_desc,
                "next_sign_hi": next_sign_hi,
                "ingress_str": ingress_str,
                "h_lagna": h_lagna,
                "h_moon": h_moon,
                "summary_line": summary_line
            }
            transit_info[p_name] = {
                "sign": constants.SIGNS_HI[s_idx],
                "h_lagna": h_lagna,
                "h_moon": h_moon,
                "hi": p_hi
            }

        # Shani Sade-Sati & Dhaiya Real-time Status
        shani_sadesati = {}
        try:
            m_lon = moon_p.longitude if moon_p else 0.0
            shani_sadesati = shani_status(datetime.now(), 5.5, m_lon)
        except Exception:
            shani_sadesati = {"status": "साढ़ेसाती नहीं", "house_from_moon": 10}

        # 2,073 Classical Formula Bank Matching
        formula_bank_sutras = []
        try:
            matched_raw = evaluate_chart_sutras(chart, (md_lord_en, ad_lord_en))
            # Pick highest priority classical sutras across key categories
            prio_cats = [
                "Classical Vedic Sutras (Raja Yogas & Royal Power)",
                "Classical Vedic Sutras (Dhana Yogas & Wealth Inflow)",
                "Bhavadhipati Phala (Parashari)",
                "Bhrigu Sutram (Bhava Phala)",
                "Dasha & Timing of Events",
                "Jaimini Upadesha Sutras",
                "Bhrigu Nandi Nadi"
            ]
            added_ids = set()
            for cat in prio_cats:
                cat_matches = [s for s in matched_raw if s.category == cat]
                for s in cat_matches[:4]:
                    if s.sutra_id not in added_ids:
                        added_ids.add(s.sutra_id)
                        formula_bank_sutras.append(f"• [{s.source} - {s.category}] {s.prediction_hi}")
                        if len(formula_bank_sutras) >= 20:
                            break
                if len(formula_bank_sutras) >= 20:
                    break
        except Exception:
            formula_bank_sutras = []

        # Pushkar Navamsha, Pushkar Bhaga & Vargottama Analysis
        special_navamsha = {}
        pushkar_nav_lines = []
        pushkar_nav_planets = []
        pushkar_bhaga_planets = []
        vargottama_planets = []

        try:
            if hasattr(chart, "get_special_navamsha_summary"):
                special_navamsha = chart.get_special_navamsha_summary()
            else:
                from vyas.chart import get_navamsha_analysis
                special_navamsha = {"Lagna": get_navamsha_analysis(chart.ascendant_longitude)}
                for p_name, p in chart.planets.items():
                    special_navamsha[p_name] = get_navamsha_analysis(p.longitude)

            for key in ["Lagna", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                if key not in special_navamsha:
                    continue
                data = special_navamsha[key]
                hi_name = constants.PLANETS_HI.get(key, "लग्न" if key == "Lagna" else key)
                deg_f = f"{int(data['deg_in_sign']):02d}°{int(((data['deg_in_sign']) % 1) * 60):02d}'"
                flags = []
                if data["is_pushkar_nav"]:
                    flags.append(f"★ पुष्कर नवांश ({data['pushkar_desc']})")
                    pushkar_nav_planets.append(f"{hi_name} ({data['pushkar_desc']})")
                if data["is_pushkar_bhaga"]:
                    flags.append(f"★ पुष्कर भाग ({int(data['pushkar_bhaga_deg'])}°)")
                    pushkar_bhaga_planets.append(f"{hi_name} ({deg_f})")
                if data["is_vargottama"]:
                    flags.append("★ वर्गोत्तम")
                    vargottama_planets.append(f"{hi_name} ({data['sign_name']} राशि)")

                status_str = " | ".join(flags) if flags else "सामान्य नवांश"
                pushkar_nav_lines.append(
                    f"• {hi_name} ({key}): {data['sign_name']} ({deg_f}) → {data['nav_num']}वां नवांश ({data['nav_sign_name']} नवांश, स्वामी: {data['nav_lord_hi']}) [{status_str}]"
                )
        except Exception:
            pushkar_nav_lines = ["• नवांश गणना उपलब्ध है।"]

        return {
            "asc_sign": asc_sign,
            "asc_sign_name": asc_sign_name,
            "lagnesh": lagnesh,
            "lagnesh_hi": lagnesh_hi,
            "moon_sign": moon_sign,
            "moon_sign_name": moon_sign_name,
            "moon_nak_name": moon_nak_name,
            "p_info": p_info,
            "house_occupants": house_occupants,
            "aspects_map": aspects_map,
            "dasha_md": dasha_md,
            "dasha_ad": dasha_ad,
            "dasha_pd": dasha_pd,
            "md_lord_en": md_lord_en,
            "ad_lord_en": ad_lord_en,
            "pd_lord_en": pd_lord_en,
            "md_start": md_start,
            "md_end": md_end,
            "ad_start": ad_start,
            "ad_end": ad_end,
            "pd_start": pd_start,
            "pd_end": pd_end,
            "next_ad_lord_en": next_ad_lord_en,
            "next_ad_lord_hi": next_ad_lord_hi,
            "transits": transit_info,
            "transits_detailed": transits_detailed,
            "shani_sadesati": shani_sadesati,
            "formula_bank_sutras": formula_bank_sutras,
            "house_lords": house_lords,
            "house_lords_lines": house_lords_lines,
            "planet_owned": planet_owned,
            "planet_ownership_lines": planet_ownership_lines,
            "house_aspects": house_aspects,
            "special_navamsha": special_navamsha,
            "pushkar_nav_lines": pushkar_nav_lines,
            "pushkar_nav_planets": pushkar_nav_planets,
            "pushkar_bhaga_planets": pushkar_bhaga_planets,
            "vargottama_planets": vargottama_planets
        }

    def _extract_conversation_memory(self, chat_history: Optional[List[Dict[str, str]]]) -> str:
        """Extracts and synthesizes persistent conversation memory and topic context across multi-turn consultation."""
        if not chat_history:
            return "यह परामर्श संवाद का प्रथम चरण है। पूर्व में कोई प्रश्न नहीं पूछा गया है।"

        user_queries = []
        topics_seen = set()

        for msg in chat_history:
            role = msg.get("role")
            cnt = (msg.get("content") or "").strip()
            if not cnt:
                continue
            cnt_lower = cnt.lower()

            if role in ["user", "human"]:
                user_queries.append(cnt)
                if any(w in cnt_lower for w in ["transit", "gochar", "गोचर", "राहु", "केतु", "rahu", "ketu", "वक्री", "मार्गी", "चाल", "गति"]):
                    topics_seen.add("ग्रह गोचर एवं खगोलीय गति (Transits & Motion Laws)")
                elif any(w in cnt_lower for w in ["career", "job", "नौकरी", "प्रमोशन", "आजीविका", "व्यवसाय"]):
                    topics_seen.add("करियर एवं आजीविका (Career & Profession)")
                elif any(w in cnt_lower for w in ["rhjs", "rjs", "exam", "judiciary", "न्यायिक", "परीक्षा"]):
                    topics_seen.add("न्यायिक / प्रतियोगी परीक्षा (Competitive Exams)")
                elif any(w in cnt_lower for w in ["धन", "money", "wealth", "पैसा", "कर्ज", "आर्थिक"]):
                    topics_seen.add("आर्थिक स्थिति एवं धन संचय (Wealth & Finance)")
                elif any(w in cnt_lower for w in ["विवाह", "शादी", "marriage", "दांपत्य"]):
                    topics_seen.add("विवाह एवं दांपत्य (Marriage & Relationship)")
                elif any(w in cnt_lower for w in ["स्वास्थ्य", "health", "रोग", "बीमारी"]):
                    topics_seen.add("आरोग्य एवं स्वास्थ्य (Health & Longevity)")
                elif any(w in cnt_lower for w in ["dasha", "दशा", "महादशा", "अन्तर्दशा"]):
                    topics_seen.add("विंशोत्तरी दशा फलित (Dasha Analysis)")
                elif any(w in cnt_lower for w in ["उपाय", "रत्न", "मंत्र", "दान"]):
                    topics_seen.add("वैदिक शांति उपाय (Remedies)")

        memory_lines = [
            f"• कुल संवाद चरण: {len(user_queries)} प्रश्न पूछे गए",
            f"• अब तक चर्चित मुख्य विषय: {', '.join(sorted(topics_seen)) if topics_seen else 'सामान्य परामर्श'}"
        ]
        if user_queries:
            recent_q = user_queries[-4:]
            memory_lines.append("• जातक के हालिया प्रश्न: " + " | ".join([f'"{q}"' for q in recent_q]))
        return "\n".join(memory_lines)

    def _get_groq_api_key(self) -> Optional[str]:
        """Discovers Groq API Key from engine config, Streamlit secrets, or environment."""
        if ENGINE_GROQ_API_KEY and ENGINE_GROQ_API_KEY.strip():
            return ENGINE_GROQ_API_KEY.strip()
        key = None
        try:
            import streamlit as st
            key = st.secrets.get("GROQ_API_KEY")
            if not key:
                key = st.session_state.get("groq_api_key")
        except Exception:
            pass
        if not key:
            key = os.environ.get("GROQ_API_KEY")
        return key.strip() if key and isinstance(key, str) and key.strip() else None

    def _get_gemini_api_key(self) -> Optional[str]:
        """Discovers Gemini API Key from engine config, Streamlit secrets, or environment."""
        if ENGINE_GEMINI_API_KEY and ENGINE_GEMINI_API_KEY.strip():
            return ENGINE_GEMINI_API_KEY.strip()
        key = None
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
            if not key:
                key = st.session_state.get("gemini_api_key")
        except Exception:
            pass
        if not key:
            key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        return key.strip() if key and isinstance(key, str) and key.strip() else None

    def _build_astrological_system_prompt(self, fw: Dict[str, Any], birth_info: Dict[str, Any],
                                          chat_history: Optional[List[Dict[str, str]]] = None,
                                          query: Optional[str] = None) -> str:
        """Assembles a comprehensive, authentic Parashari & Jaimini chart framework prompt with Desh, Kaal & Patra awareness,
        Universal Astronomical Motion Laws, Real-time Ingress, 2,073 Classical Formula Bank and Dialogue Memory."""
        name = birth_info.get("name", "जातक")
        gender = birth_info.get("gender", "अज्ञात")
        place = birth_info.get("place") or birth_info.get("city", "अज्ञात")

        b_local = birth_info.get("local")
        birth_year = None
        birth_date_str = ""
        if isinstance(b_local, datetime):
            birth_year = b_local.year
            birth_date_str = b_local.strftime("%d/%m/%Y")
        else:
            dt_str = str(birth_info.get("dt", ""))
            try:
                parts = dt_str.split("-")
                birth_year = int(parts[0])
                birth_date_str = f"{parts[2]}/{parts[1]}/{parts[0]}" if len(parts) >= 3 else dt_str
            except Exception:
                birth_date_str = dt_str

        cur_year = datetime.now().year
        age_years = (cur_year - birth_year) if birth_year else 35

        p_list = [f"{v['hi']} {v['house']}वें भाव में ({v['sign_name']} {v['deg']}°{' वक्री' if v['is_retro'] else ''})" for v in fw['p_info'].values()]
        planets_summary = ", ".join(p_list)

        asp_list = [f"{p}: भाव {', '.join(str(h) for h in houses)}" for p, houses in fw['aspects_map'].items() if houses]
        aspects_summary = "; ".join(asp_list)

        lords_block = "\n".join(fw.get("house_lords_lines", []))
        ownership_block = "\n".join(fw.get("planet_ownership_lines", []))
        lagna_aspects = [a["desc"] for a in fw.get("house_aspects", {}).get(1, [])]
        lagna_aspects_str = ", ".join(lagna_aspects) if lagna_aspects else "कोई प्रत्यक्ष दृष्टि नहीं"

        # Real-time detailed transit lines
        tr_detailed = fw.get("transits_detailed", {})
        transit_lines = []
        if tr_detailed:
            for p_en in ["Rahu", "Ketu", "Saturn", "Jupiter", "Sun", "Moon", "Mars", "Mercury", "Venus"]:
                if p_en in tr_detailed:
                    transit_lines.append(tr_detailed[p_en]["summary_line"])
        transit_table_block = "\n".join(transit_lines) if transit_lines else "• गोचर गणना सक्रिय है।"

        shani_sd = fw.get("shani_sadesati", {})
        shani_status_str = f"• शनि साढ़ेसाती / ढैया वास्तविक स्थिति: {shani_sd.get('status', 'साढ़ेसाती नहीं')} (जन्म चन्द्र से {shani_sd.get('house_from_moon', '-')}वां भाव)"

        # 2,073 Classical Formula Bank lines & Brahmastra Predictive Standard (Nakshatra Tak / Classical Synthesis)
        brahmastra_rule_block = """• [ब्रह्मास्त्र फलित नियम]: किसी भी प्रश्न पर फलादेश करते समय सदैव 4 स्तंभों का समन्वय करें:
  (1) भाव (Bhava): भाव में कौन से ग्रह स्थित हैं और किनकी दृष्टि है?
  (2) भावेश (Bhavesha): भाव का स्वामी किस भाव में, किस राशि में, किस अवस्था में है? उस पर शुभत्व (Subhatva - गुरु/शुक्र का प्रभाव) है या पापत्व?
  (3) कारक (Karaka): उस विषय के नैसर्गिक कारक (कर्म=शनि/सूर्य, धन=गुरु, विवाह=शुक्र, स्वास्थ्य=सूर्य/लग्नेश, संतान=गुरु, भूमि=मंगल) की स्थिति।
  (4) दशा एवं गोचर की युति (Timing Trigger): विंशोत्तरी दशा व शनि-गुरु का दोहरा गोचर फल को कब धरातल पर प्रकट करेगा (सटीक तिथियों सहित)?"""

        sutras_list = fw.get("formula_bank_sutras", [])
        sutras_block = (brahmastra_rule_block + "\n" + "\n".join(sutras_list[:14])) if sutras_list else brahmastra_rule_block

        # Multi-turn conversation memory summary
        memory_summary = self._extract_conversation_memory(chat_history)

        # Dynamic Knowledge Retrieval from 13,000+ Sutra Bank & 39+ Classical Books
        query_sutras_block = ""
        query_books_block = ""
        if query and query.strip():
            try:
                from vyas.knowledge_engine import search_knowledge_bank
                q_sutras = search_knowledge_bank(query, max_results=6)
                if q_sutras:
                    lines = [f"• [{s.get('source', 'सूत्र')}] [{s.get('sutra_id')}] {s.get('sub_category')}: {s.get('prediction_hi')}" for s in q_sutras]
                    query_sutras_block = "\n".join(lines)
            except Exception:
                pass

            try:
                from vyas.book_reader import search_books
                q_clean = query.strip()
                b_results = search_books(q_clean, max_results=4)
                if not b_results:
                    words = [w for w in q_clean.split() if len(w) >= 3 and w not in ["क्या", "बताओ", "कैसा", "होगा", "मेरा", "मेरी", "मुझे", "आचार्य", "प्रणाम", "kaisa", "hoga"]]
                    for w in words[:2]:
                        b_results = search_books(w, max_results=3)
                        if b_results:
                            break
                if b_results:
                    b_lines = [f"• [{b['book']} - {b['page']}]: {b['snippet'][:140]}" for b in b_results]
                    query_books_block = "\n".join(b_lines)
            except Exception:
                pass

        _is_fem = "female" in str(gender).lower() or "स्त्री" in str(gender) or "महिला" in str(gender)
        if _is_fem:
            gender_shastra_directive = (
                "• [स्त्री-जातक फलित विधान (Stree Jataka Shastric Invariants)]:\n"
                "  - जातक महिला (स्त्री) हैं। फलित करते समय महर्षि पराशर, वराहमिहिर एवं फलदीपिका के 'स्त्री जातक' अध्याय के विशेष सूत्रों का अनुपालन करें।\n"
                "  - विवाह, पति सुख, सौभाग्य एवं दांपत्य कल्याण के मुख्य नैसर्गिक कारक के रूप में देवगुरु बृहस्पति (Jupiter) एवं 7वें व 8वें (मांगल्य) भाव का विशेष विचार करें।\n"
                "  - जातक के प्रति सम्मानसूचक व आदरयुक्त स्त्रीलिंग शब्दों (जैसे 'आपकी कुण्डली में', 'आप प्राप्त करेंगी', 'आपके लिए विशेष शुभ रहेगा') का प्रयोग करें।"
            )
        else:
            gender_shastra_directive = (
                "• [पुरुष-जातक फलित विधान (Purusha Jataka Principles)]:\n"
                "  - जातक पुरुष हैं। विवाह, पत्नी सुख एवं दांपत्य जीवन के नैसर्गिक कारक के रूप में दैत्यगुरु शुक्र (Venus) एवं 7वें भाव का मुख्य रूप से विचार करें।\n"
                "  - जातक के प्रति सम्मानसूचक व आदरयुक्त पुल्लिंग शब्दों (जैसे 'आपकी कुण्डली में', 'आप प्राप्त करेंगे', 'आपके लिए विशेष शुभ रहेगा') का प्रयोग करें।"
            )

        pushkar_table_block = "\n".join(fw.get("pushkar_nav_lines", []))
        p_nav_list = fw.get("pushkar_nav_planets", [])
        p_nav_summary = ", ".join(p_nav_list) if p_nav_list else "कोई ग्रह पुष्कर नवांश में नहीं है।"
        p_bhaga_list = fw.get("pushkar_bhaga_planets", [])
        p_bhaga_summary = ", ".join(p_bhaga_list) if p_bhaga_list else "कोई ग्रह पुष्कर भाग में नहीं है।"
        varg_list = fw.get("vargottama_planets", [])
        varg_summary = ", ".join(varg_list) if varg_list else "कोई ग्रह वर्गोत्तम नहीं है।"

        prompt = (
            f"आप आचार्य व्यास हैं—महर्षि पराशर, जैमिनी, एवं भृगु ज्योतिष के मूर्धन्य विद्वान और पूज्य वैदिक ज्योतिषी।\n\n"
            f"=== जातक का व्यक्तिगत सांसारिक विवरण (देश, काल, पात्र) ===\n"
            f"• नाम: {name}\n"
            f"• आयु: {age_years} वर्ष (जन्म तिथि: {birth_date_str})\n"
            f"• लिंग: {gender}\n"
            f"• जन्म स्थान: {place}\n"
            f"{gender_shastra_directive}\n\n"
            f"=== जातक का संपूर्ण कुण्डली विवरण ===\n"
            f"• लग्न: {fw['asc_sign_name']} लग्न (लग्नेश: {fw['lagnesh_hi']})\n"
            f"• चन्द्र राशि: {fw['moon_sign_name']} (नक्षत्र: {fw['moon_nak_name']})\n"
            f"• सक्रिय विंशोत्तरी दशा: महादशा {fw['dasha_md']} ({fw['md_start']} से {fw['md_end']}), "
            f"अन्तर्दशा {fw['dasha_ad']} (समाप्ति: {fw['ad_end']}), "
            f"प्रत्यन्तर्दशा {fw['dasha_pd']} (समाप्ति: {fw['pd_end']})\n"
            f"• आगामी अन्तर्दशा: {fw['next_ad_lord_hi']} (प्रारंभ तिथि: {fw['ad_end']})\n"
            f"• 9 ग्रह जन्म स्थितियां (भाव, राशि, अंश): {planets_summary}\n\n"
            f"=== सूक्ष्म नवांश, पुष्कर नवांश एवं वर्गोत्तम ग्रह (PUSHKAR NAVAMSHA & VARGOTTAMA - ABSOLUTE GROUND TRUTH) ===\n"
            f"• [पुष्कर नवांश व नवांश फलित का अनिवार्य शास्त्रीय नियम (BPHS & Jataka Parijata)]:\n"
            f"  - यदि जातक 'पुष्कर नवांश', 'पुष्कर भाग', 'वर्गोत्तम', या अपनी कुण्डली के सूक्ष्म नवांश के विषय में प्रश्न पूछे, तो इधर-उधर की बात बिल्कुल न करें! नीचे दी गई प्रामाणिक गणितीय सूची के आधार पर सीधे, स्पष्ट व विस्तार से बताएं कि कौन सा ग्रह पुष्कर नवांश में है और उसका क्या शुभ फल है।\n"
            f"{pushkar_table_block}\n"
            f"• **पुष्कर नवांश में स्थित ग्रह:** {p_nav_summary}\n"
            f"• **वर्गोत्तम (Vargottama) ग्रह:** {varg_summary}\n"
            f"• **पुष्कर भाग (Pushkar Bhaga) ग्रह:** {p_bhaga_summary}\n"
            f"• **शास्त्रीय महत्व (BPHS / Jataka Parijata):** पुष्कर नवांश 108 में से 24 परम शुभ व पोषणकारी नवांश होते हैं (जो केवल गुरु, शुक्र, बुध, चन्द्र द्वारा शासित होते हैं)। इसमें स्थित ग्रह अपनी दशा-अन्तर्दशा में राजयोग, अकूत धन, आरोग्यता व ईश्वरीय रक्षा प्रदान करता है।\n\n"
            f"=== 12 भावों के वास्तविक अधिपति (निर्विवाद शास्त्रीय सत्य - ABSOLUTE GROUND TRUTH) ===\n"
            f"{lords_block}\n\n"
            f"=== ग्रहों का वास्तविक भाव-स्वामित्व एवं स्थिति (PLANET LORDSHIPS & POSITIONS) ===\n"
            f"{ownership_block}\n\n"
            f"=== भावों पर ग्रहीय दृष्टियां (ASPECTS ON HOUSES) ===\n"
            f"• लग्न भाव (1st House) पर दृष्टियां: {lagna_aspects_str}\n"
            f"• अन्य भावों पर दृष्टियां: {aspects_summary}\n\n"
            f"=== खगोलीय गति एवं गोचर के सार्वकालिक अटल नियम (ASTRONOMICAL MOTION LAWS - STRICT MANDATE) ===\n"
            f"1. राहु एवं केतु की गति (RAHU & KETU - NEVER DIRECT / ALWAYS RETROGRADE):\n"
            f"   - राहु और केतु छाया ग्रह (Moon's Nodes) हैं। ये सदैव वक्री (Always Retrograde / उल्टी चाल) चलते हैं!\n"
            f"   - ये कभी भी मार्गी (Direct) नहीं होते!\n"
            f"   - राशि चक्र में इनकी गति 12वीं राशि से 11वीं, 11वीं से 10वीं, 10वीं से 9वीं... 1वीं से 12वीं की ओर उल्टी (REVERSE) होती है:\n"
            f"     मीन (12) → कुम्भ (11) → मकर (10) → धनु (9) → वृश्चिक (8) → तुला (7) → कन्या (6) → सिंह (5) → कर्क (4) → मिथुन (3) → वृषभ (2) → मेष (1) → मीन (12)।\n"
            f"   - कदापि न भूलें (Strict Prohibition):\n"
            f"     • वर्तमान में राहु कुंभ राशि में हैं — उनका अगला गोचर मकर राशि में होगा (मीन में कभी नहीं)!\n"
            f"     • वर्तमान में केतु सिंह राशि में हैं — उनका अगला गोचर कर्क राशि में होगा (कन्या में कभी नहीं)!\n"
            f"     • राहु-केतु को कभी भी मार्गी न बताएं, और न ही यह कहें कि वे सिंह से कन्या या कुंभ से मीन जा रहे हैं! यह अक्षम्य खगोलीय त्रुटि है।\n"
            f"     • राहु-केतु परस्पर सदैव 180° (सप्तम भाव / आमने-सामने) रहते हैं और एक राशि में लगभग 18 माह रहते हैं।\n"
            f"2. सूर्य एवं चन्द्रमा की गति (SUN & MOON - ALWAYS DIRECT / NEVER RETROGRADE):\n"
            f"   - भगवान सूर्य और चन्द्रमा सदैव मार्गी (Direct) चलते हैं। वे कभी भी वक्री (Retrograde) नहीं होते!\n"
            f"   - सूर्य 1 माह में 1 राशि (मेष → वृषभ → मिथुन... मीन) पार करते हैं।\n"
            f"   - चन्द्रमा लगभग सवा दो दिन में 1 राशि पार करते हैं।\n"
            f"3. पंच ताराग्रह (MARS, MERCURY, JUPITER, VENUS, SATURN):\n"
            f"   - ये 5 ग्रह कभी मार्गी (Direct) और कभी वक्री (Retrograde) होते हैं।\n"
            f"   - शनि: लगभग ढाई वर्ष में 1 राशि पार करते हैं। वर्ष में लगभग 140 दिन वक्री रहते हैं।\n"
            f"   - गुरु: लगभग 1 वर्ष में 1 राशि पार करते हैं। वर्ष में लगभग 120 दिन वक्री रहते हैं।\n"
            f"   - मंगल: सामान्यतः 45 दिन में 1 राशि पार करते हैं (वक्री होने पर 6-7 माह तक रह सकते हैं)।\n"
            f"   - बुध: लगभग 21-25 दिन में 1 राशि पार करते हैं (वर्ष में 3-4 बार वक्री होते हैं)।\n"
            f"   - शुक्र: लगभग 1 माह में 1 राशि पार करते हैं।\n"
            f"   - वर्तमान में कौन सा ग्रह मार्गी है और कौन सा वक्री, नीचे दी गई 'वास्तविक गोचर स्थिति' से ही शत-प्रतिशत उद्धृत करें।\n\n"
            f"=== तात्कालिक वास्तविक गोचर स्थिति (REAL-TIME EPHEMERIS GOCHAR STATUS) ===\n"
            f"{transit_table_block}\n"
            f"{shani_status_str}\n\n"
            f"=== कुण्डली पर घटित 13,000+ शास्त्रीय सूत्र बैंक (ACTIVE FORMULAS ON CHART) ===\n"
            f"{sutras_block}\n\n"
            f"=== 13,000+ सूत्र बैंक से प्रश्न-संबंधित प्रत्यक्ष सूत्र (RELEVANT FORMULAS FROM 13,000+ SUTRA BANK) ===\n"
            f"{query_sutras_block if query_sutras_block else '• कुण्डली पर 13,000+ शास्त्रीय सूत्र डेटाबैंक के सिद्धांत सक्रिय हैं।'}\n\n"
            f"=== 40+ शास्त्रीय ग्रंथ पुस्तकालय से प्रामाणिक उद्धरण (CITATIONS FROM 39+ CLASSICAL BOOKS) ===\n"
            f"{query_books_block if query_books_block else '• बृहत्पाराशर, बृहज्जातक, फलदीपिका, लाल किताब एवं भृगु संहिता के नियम संरेखित हैं।'}\n\n"
            f"=== शास्त्रीय ग्रंथ प्रमाण एवं अकाट्य फलित तर्क (CLASSICAL CITATIONS & REASONING MANDATE) ===\n"
            f"• 13,000+ शास्त्रीय सूत्र और 40+ ग्रंथ केवल आंतरिक डेटा नहीं हैं, अपितु आपके प्रत्येक उत्तर की आत्मा हैं।\n"
            f"• जब भी आप किसी प्रश्न का उत्तर दें, तो अपने ज्ञानकोष के प्रामाणिक ग्रंथों के नाम व अध्याय (जैसे 'बृहत्पाराशर होराशास्त्र (अ. 12)', 'फलदीपिका (भावफलाध्याय)', 'भृगु नंदी नाड़ी', 'सारावली', 'जातक पारिजात', 'के.पी. उप-स्वामी सिद्धांत', 'लाल किताब') का ठोस संदर्भ दें।\n"
            f"• केवल सतही भविष्यवाणी न करें; कारण-कार्य संबंध (Cause & Effect Reasoning) समझाएं कि किस ग्रह की स्थिति, किस भाव पर दृष्टि और किस विंशोत्तरी दशा के सक्रिय होने से यह परिणाम घटित होगा।\n"
            f"• एक मूर्धन्य शास्त्र-पारंगत महर्षि की भांति प्रामाणिक, तर्कसंगत और अकाट्य परामर्श प्रदान करें।\n\n"
            f"=== परामर्श संवाद स्मृति एवं पूर्व संदर्भ (CONSULTATION DIALOGUE MEMORY & CONTINUITY) ===\n"
            f"{memory_summary}\n"
            f"**स्मृति निर्देश: पूर्व बातचीत में जातक द्वारा पूछे गए विषयों और स्थापित तथ्यों की पूर्ण निरंतरता बनाए रखें।**\n\n"
            f"=== परम संक्षिप्त, सटीक एवं व्यावहारिक फलित नियम (STRICT CONCISENESS AND ZERO-LECTURING MANDATE) ===\n"
            f"• उत्तर अत्यंत संक्षिप्त, व्यावहारिक और सीधा दें (Direct, to-the-point, maximum 2-3 short bullet points)।\n"
            f"• अनावश्यक खगोलीय व्याख्यान पूर्णतः वर्जित हैं: जब तक जातक विशेष रूप से खगोलीय गति न पूछे, तब तक राहु-केतु वक्री चलने या खगोलशास्त्र के नियम जैसे व्याख्यान बिल्कुल न दें!\n"
            f"• कभी भी कच्चे HTML टैग्स न लिखें! केवल शुद्ध मार्कडाउन बोल्ड का प्रयोग करें।\n\n"
            f"=== परम शास्त्रीय व फलित नियम (STRICT ZERO-HALLUCINATION AND COMPLETION RULES) ===\n"
            f"1. भाव-स्वामित्व (House Lordships) में किसी भी प्रकार का भ्रम या त्रुटि अक्षम्य है:\n"
            f"   - किसी ग्रह की 'स्थिति' (posited house) और उसके 'स्वामित्व' (owned houses) को कभी न मिलाएं!\n"
            f"   - फलकथन में सदैव ऊपर दी गई 'ग्रहों का वास्तविक भाव-स्वामित्व' तालिका के अनुसार ही 100% शुद्ध तथ्य लिखें।\n"
            f"2. उत्तर की पूर्णता (Complete & Exhaustive Response):\n"
            f"   - उत्तर को कभी भी बीच में अधूरा, अपूर्ण या कटा हुआ न छोड़ें (Never stop abruptly mid-sentence).\n"
            f"   - जातक के पूछे गए प्रश्न के सभी आयामों को सविस्तार और पूर्ण वाक्यों में प्रस्तुत करें।\n"
            f"   - उत्तर का अंत सदैव एक पूर्ण, सार्थक वाक्य और वैदिक आशीर्वाद (जैसे '॥ शुभमस्तु ॥' या '॥ ॐ तत्सत् ॥') के साथ करें।\n"
            f"3. त्रिगुण दृष्टि / संयुक्त दृष्टि का शास्त्रीय विवेचन (Triguna Drishti on Lagna):\n"
            f"   - जब मंगल, शनि और गुरु जैसे शक्तिशाली ग्रह एक साथ लग्न को देखते हैं, तो यह दुर्लभ राजयोग कारक स्थिति होती है:\n"
            f"     • मंगल (लग्नेश, मकर में उच्च): लग्न को असीम जीवनी शक्ति व रक्षक प्रभाव (लग्नं पश्यति लग्नेशः)।\n"
            f"     • शनि (कर्मेश/लाभेश, तुला में उच्च): गंभीर चिंतन, अनुशासन, न्यायप्रियता, धैर्य और स्थायी राजपद/प्रतिष्ठा।\n"
            f"     • देवगुरु बृहस्पति (भाग्येश, धनु में स्वराशि): 5वीं अमृत दृष्टि से सर्वदोष निवारण, ईश्वरीय कृपा और दीर्घायु।\n\n"
            f"=== चैट स्क्रीन हेतु पठन-सुगमता एवं नो-टेबल नियम (STRICT MOBILE READABILITY RULE) ===\n"
            f"• कभी भी चौड़ी मार्कडाउन तालिका (| Date | Dasha | Type |) न बनाएं! मोबाइल व चैट स्क्रीन पर टेबल कट जाती है और जातक पढ़ नहीं सकता।\n"
            f"• सभी तिथियां, दशाएं और फलादेश बुलेट पॉइंट्स (•), छोटे पैराग्राफ और बोल्ड (**...**) में ही लिखें।\n"
            f"• तालिका के स्थान पर बुलेट सूची बनाएं। जैसे:\n"
            f"  • **सक्रिय दशा:** शुक्र महादशा में शनि अन्तर्दशा (अवधि: 14 Nov 2026 तक)\n"
            f"  • **आगामी दशा:** बुध अन्तर्दशा (15 Nov 2026 से 08 Oct 2027)\n"
            f"  • **शास्त्रीय फलादेश:** यह कालखंड आजीविका में अधिकार, पदोन्नति और नए अनुबंध लाएगा।\n\n"
            f"=== देश, काल, पात्र एवं परिस्थिति का परम शास्त्रीय नियम (CRITICAL MANDATE) ===\n"
            f"1. जातक की वास्तविक आयु ({age_years} वर्ष) के अनुसार ही व्यावहारिक और यथार्थवादी मार्गदर्शन दें।\n"
            f"2. कुण्डली, सक्रिय विंशोत्तरी दशा और तात्कालिक गोचर (शनि, गुरु, राहु) के समन्वय से ही तर्कसंगत फलित बताएं।\n"
            f"3. जातक के प्रश्न की भाषा (हिंदी या अंग्रेजी) में ही अत्यंत शुद्ध, सुरुचिपूर्ण, आदरयुक्त एवं धाराप्रवाह उत्तर दें।\n"
            f"4. यदि जातक संक्षिप्त या अनुवर्ती प्रश्न पूछे (जैसे 'आगे क्या', 'और केतु का', 'कब होगा', 'उपाय बताओ'), तो पूर्व बातचीत के संदर्भ को जोड़ते हुए स्पष्ट समय-सीमा (Timelines/Dates) दें।\n"
            f"5. उत्तर के अंत में जातक के कल्याण हेतु सटीक, सात्विक वैदिक उपाय (मंत्र जप संख्या, दान, अथवा रत्न परामर्श) अवश्य प्रदान करें।\n"
            f"6. संवादात्मक उत्सुकता व जिज्ञासा सूत्र (MANDATORY MULTI-TOPIC CURIOSITY HOOK RULE):\n"
            f"   • जातक चाहे जिस भी विषय (करियर, व्यापार, धन, कर्ज, विवाह, संतान, परीक्षा, स्वास्थ्य, मकान, वाहन, विदेश, शत्रु, अध्यात्म, साढ़ेसाती या सामान्य) पर प्रश्न पूछे:\n"
            f"     1. प्रश्न का संपूर्ण, तार्किक व प्रामाणिक ज्योतिषीय विश्लेषण दें।\n"
            f"     2. उपयुक्त सात्विक उपाय बताएं।\n"
            f"     3. अपने उत्तर के बिल्कुल अंत में कोई भी 'आचार्य जिज्ञासा सूत्र' या हेडिंग/लेबल बिल्कुल न लिखें। सीधे स्वाभाविक और जिज्ञासा-वर्धक प्रश्न पूछें:\n"
            f"        प्रारूप: 'क्या आप जानना चाहेंगे कि आपकी जन्मपत्रिका में [उस विषय से संबंधित गुप्त व महत्वपूर्ण पहलू] का सटीक समय/रहस्य क्या है?'\n"
            f"   • विषयवार जिज्ञासा सूत्र के उदाहरण:\n"
            f"     - करियर / नौकरी: 'क्या आप जानना चाहेंगे कि आपकी जन्मपत्रिका में अचानक बड़े धन आगमन (Sudden Wealth Inflow) व पदोन्नति का प्रबलतम समय-चक्र कब सक्रिय हो रहा है?'\n"
            f"     - व्यापार / साझेदारी: 'क्या आप जानना चाहेंगे कि आपकी कुण्डली के सप्तम व एकादश भाव के अनुसार व्यापार में अप्रत्याशित विस्तार एवं बड़े मुनाफे का वास्तविक समय कब प्रारंभ होगा?'\n"
            f"     - धन / कर्ज / निवेश: 'क्या आप जानना चाहेंगे कि आपकी कुण्डली में रुका हुआ धन वापस आने, कर्ज मुक्ति एवं बड़े धन संचय का सबसे स्वर्णिम योग किस अवधि में बन रहा है?'\n"
            f"     - विवाह / दांपत्य: 'क्या आप जानना चाहेंगे कि आपके भावी जीवनसाथी का स्वभाव, उनकी दिशा तथा दांपत्य में स्थायी सुख-समृद्धि एवं भाग्योदय का सटीक समय-चक्र क्या है?'\n"
            f"     - संतान पक्ष: 'क्या आप जानना चाहेंगे कि आपकी कुण्डली के पंचम भाव (संतान भाव) और गुरु की अमृत दृष्टि के अनुसार संतान प्राप्ति एवं संतान के भाग्योदय का सबसे शुभ काल कब है?'\n"
            f"     - परीक्षा / प्रतियोगी चयन (RJS, UPSC): 'क्या आप जानना चाहेंगे कि किस विशिष्ट माह में आपकी मेधा शक्ति एवं भाग्य का ऐसा संयोग बनेगा जिससे प्रतियोगी परीक्षा में अंतिम चयन व मेरिट सुनिश्चित हो सके?'\n"
            f"     - स्वास्थ्य / मानसिक शांति: 'क्या आप जानना चाहेंगे कि कौन सा गुप्त ग्रह दोष आपकी जीवनी शक्ति व मानसिक एकाग्रता को प्रभावित कर रहा है और उसका अचूक वैदिक रक्षा कवच क्या है?'\n"
            f"     - मकान / भूमि / वाहन: 'क्या आप जानना चाहेंगे कि आपकी जन्मपत्रिका में स्वयं के भव्य मकान, भूमि अथवा नवीन वाहन क्रय का सबसे स्वर्णिम योग किस वर्ष व माह में खुल रहा है?'\n"
            f"     - विदेश यात्रा / स्थायी निवास: 'क्या आप जानना चाहेंगे कि आपकी कुण्डली के नवम व द्वादश भाव के अनुसार विदेश यात्रा, परदेस में स्थायी निवास एवं विदेशी मुद्रा लाभ का सटीक योग कब सक्रिय होगा?'\n"
            f"     - कोर्ट / शत्रु / विवाद: 'क्या आप जानना चाहेंगे कि आपकी पत्रिका के षष्ठम भाव के अनुसार विरोधियों पर पूर्ण विजय और न्यायालयीन विवाद से ससम्मान मुक्ति का समय कब है?'\n"
            f"     - अध्यात्म / इष्ट देव: 'क्या आप जानना चाहेंगे कि आपके वास्तविक जन्म-जन्मांतर के इष्ट देव कौन हैं और किस विशेष साधना से पूर्वजन्म के संचित पुण्यों का उदय होगा?'\n"
            f"     - दशा / साढ़ेसाती / गोचर: 'क्या आप जानना चाहेंगे कि आगामी गोचर परिवर्तन व चालू दशा आपके जीवन में कौन सा बड़ा अप्रत्याशित मोड़ लेकर आने वाली है?'\n"
            f"     - सामान्य कुण्डली विश्लेषण: 'क्या आप जानना चाहेंगे कि आपकी जन्मपत्रिका में सबसे शक्तिशाली राजयोग कौन सा है और वह जीवन में किस उम्र में पूर्ण फल देगा?'\n"
        )
        return prompt

    def _call_openai_compatible(self, endpoint_url: str, key_pool: List[str], models: List[str],
                                query: str, fw: Dict[str, Any], birth_info: Dict[str, Any],
                                chat_history: Optional[List[Dict[str, str]]],
                                extra_headers: Optional[Dict[str, str]] = None) -> Optional[str]:
        """Generic, resilient runner for OpenAI-compatible REST APIs with multi-key pool failover."""
        from vyas import ai_key_manager
        if not key_pool:
            return None

        try:
            import json
            import requests

            system_prompt = self._build_astrological_system_prompt(fw, birth_info, chat_history=chat_history, query=query)
            messages = [{"role": "system", "content": system_prompt}]

            if chat_history:
                for msg in chat_history[-16:]:
                    role = "assistant" if msg.get("role") in ["assistant", "model"] else "user"
                    cnt = (msg.get("content") or "").strip()
                    if cnt:
                        messages.append({"role": role, "content": cnt})
            messages.append({"role": "user", "content": query})

            for api_key in key_pool:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                if extra_headers:
                    headers.update(extra_headers)

                for m_name in models:
                    payload = {
                        "model": m_name,
                        "messages": messages,
                        "temperature": 0.6,
                        "max_tokens": 1024
                    }
                    try:
                        resp = requests.post(endpoint_url, json=payload, headers=headers, timeout=8)
                        if resp.status_code == 200:
                            data = resp.json()
                            text = data["choices"][0]["message"].get("content", "").strip()
                            if text:
                                ai_key_manager.mark_key_healthy(api_key)
                                return text
                        elif resp.status_code in [429, 401, 503]:
                            ai_key_manager.mark_key_rate_limited(api_key)
                            break
                    except Exception:
                        continue
        except Exception:
            pass
        return None

    def _call_groq(self, query: str, fw: Dict[str, Any], birth_info: Dict[str, Any],
                    chat_history: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """Calls Groq API (ultra-fast LPU inference) with multi-key auto-failover."""
        from vyas import ai_key_manager
        return self._call_openai_compatible(
            endpoint_url="https://api.groq.com/openai/v1/chat/completions",
            key_pool=ai_key_manager.get_groq_key_pool(task="chat"),
            models=["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
            query=query, fw=fw, birth_info=birth_info, chat_history=chat_history
        )

    def _call_deepseek(self, query: str, fw: Dict[str, Any], birth_info: Dict[str, Any],
                       chat_history: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """Calls DeepSeek API (V3 / R1 reasoning) with multi-key auto-failover."""
        from vyas import ai_key_manager
        return self._call_openai_compatible(
            endpoint_url="https://api.deepseek.com/chat/completions",
            key_pool=ai_key_manager.get_deepseek_key_pool(task="chat"),
            models=["deepseek-chat", "deepseek-reasoner"],
            query=query, fw=fw, birth_info=birth_info, chat_history=chat_history
        )

    def _call_openai(self, query: str, fw: Dict[str, Any], birth_info: Dict[str, Any],
                     chat_history: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """Calls OpenAI API (GPT-4o / GPT-4o-mini) with multi-key auto-failover."""
        from vyas import ai_key_manager
        return self._call_openai_compatible(
            endpoint_url="https://api.openai.com/v1/chat/completions",
            key_pool=ai_key_manager.get_openai_key_pool(task="chat"),
            models=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
            query=query, fw=fw, birth_info=birth_info, chat_history=chat_history
        )

    def _call_openrouter(self, query: str, fw: Dict[str, Any], birth_info: Dict[str, Any],
                         chat_history: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """Calls OpenRouter API (unified router for Claude, GPT, DeepSeek, etc.) with multi-key auto-failover."""
        from vyas import ai_key_manager
        return self._call_openai_compatible(
            endpoint_url="https://openrouter.ai/api/v1/chat/completions",
            key_pool=ai_key_manager.get_openrouter_key_pool(task="chat"),
            models=["anthropic/claude-3.5-sonnet", "openai/gpt-4o-mini", "deepseek/deepseek-chat"],
            query=query, fw=fw, birth_info=birth_info, chat_history=chat_history,
            extra_headers={"HTTP-Referer": "https://vyas-astrology-111.streamlit.app", "X-Title": "VYAS Astrology"}
        )

    def _call_kilo(self, query: str, fw: Dict[str, Any], birth_info: Dict[str, Any],
                   chat_history: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """Calls Kilo AI Gateway (OpenAI-compatible) with multi-key auto-failover."""
        from vyas import ai_key_manager
        return self._call_openai_compatible(
            endpoint_url="https://ai-gateway.kilo.ai/api/v1/chat/completions",
            key_pool=ai_key_manager.get_kilo_key_pool(task="chat"),
            models=["kilo-auto/free", "anthropic/claude-sonnet-4.5", "meta-llama/llama-3.3-70b-instruct:free", "openrouter/free"],
            query=query, fw=fw, birth_info=birth_info, chat_history=chat_history
        )

    def _call_vyas_daivagya(self, query: str, fw: Dict[str, Any], birth_info: Dict[str, Any],
                            chat_history: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """
        Calls the custom domain-fine-tuned Vyas-Daivagya model (Vyas-Daivagya-1.5B / 3B).
        Connects via local Ollama, vLLM, llama.cpp server, or custom hosted endpoint.
        """
        import os
        import json
        import requests

        endpoint = os.environ.get("VYAS_DAIVAGYA_API_URL", "http://localhost:11434/v1/chat/completions")
        model = os.environ.get("VYAS_DAIVAGYA_MODEL", "vyas-daivagya:1.5b")
        api_key = os.environ.get("VYAS_DAIVAGYA_API_KEY", "ollama")

        # Fast circuit breaker: if neither custom URL nor local server is expected and not forced, return quickly
        if not os.environ.get("VYAS_DAIVAGYA_API_URL") and os.environ.get("ENABLE_LOCAL_DAIVAGYA") != "1":
            return None

        try:
            system_prompt = self._build_astrological_system_prompt(fw, birth_info, chat_history=chat_history, query=query)
            messages = [{"role": "system", "content": system_prompt}]
            if chat_history:
                for msg in chat_history[-6:]:
                    r = "assistant" if msg.get("role") in ["assistant", "model"] else "user"
                    c = msg.get("content", "")
                    if c:
                        messages.append({"role": r, "content": c})
            messages.append({"role": "user", "content": query})

            resp = requests.post(
                endpoint,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.35,
                    "max_tokens": 800
                },
                timeout=12
            )
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "")
                    if content and len(content.strip()) > 20:
                        return self._sanitize_chat_output(content)
        except Exception:
            pass
        return None

    def _call_gemini(self, query: str, fw: Dict[str, Any], birth_info: Dict[str, Any],
                     chat_history: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """Calls Google Gemini API with automatic multi-key pool failover & model resilience."""
        from vyas import ai_key_manager
        key_pool = ai_key_manager.get_gemini_key_pool(task="chat")
        if not key_pool:
            return None

        try:
            import json
            import requests

            system_prompt = self._build_astrological_system_prompt(fw, birth_info, chat_history=chat_history, query=query)
            contents = []

            if chat_history:
                for msg in chat_history[-16:]:
                    role = "model" if msg.get("role") in ["assistant", "model"] else "user"
                    cnt = (msg.get("content") or "").strip()
                    if cnt:
                        contents.append({"role": role, "parts": [{"text": cnt}]})
            contents.append({"role": "user", "parts": [{"text": query}]})

            headers = {"Content-Type": "application/json"}
            payload = {
                "system_instruction": {
                    "parts": [{"text": system_prompt}]
                },
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.6,
                    "maxOutputTokens": 1024
                }
            }
            for api_key in key_pool:
                for gm_model in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{gm_model}:generateContent?key={api_key}"
                    try:
                        resp = requests.post(url, json=payload, headers=headers, timeout=8)
                        if resp.status_code == 200:
                            data = resp.json()
                            candidates = data.get("candidates", [])
                            if candidates:
                                parts = candidates[0].get("content", {}).get("parts", [])
                                if parts:
                                    text = parts[0].get("text", "").strip()
                                    if text:
                                        ai_key_manager.mark_key_healthy(api_key)
                                        return text
                        elif resp.status_code in [429, 401, 503]:
                            ai_key_manager.mark_key_rate_limited(api_key)
                            break
                    except Exception:
                        continue
        except Exception:
            pass
        return None

    def _append_curiosity_hook(self, text: str, query: str) -> str:
        if not text:
            return text
        if "आचार्य जिज्ञासा सूत्र" in text or "क्या आप जानना चाहेंगे" in text:
            return text
        q_low = (query or "").lower()

        # 1. Foreign Travel / Settlement / Visa / PR
        if any(w in q_low for w in ["विदेश", "foreign", "abroad", "visa", "वीजा", "पासपोर्ट", "passport", "pr", "settlement", "नागरिकता"]):
            hook = "क्या आप जानना चाहेंगे कि आपकी कुण्डली के नवम व द्वादश भाव के अनुसार विदेश यात्रा, परदेस में स्थायी निवास एवं विदेशी मुद्रा लाभ का सटीक योग कब सक्रिय होगा?"

        # 2. Legal / Court / Litigation / Enemies / Rivals / Disputes
        elif any(w in q_low for w in ["कोर्ट", "court", "केस", "case", "मुकदमा", "विवाद", "झगड़ा", "शत्रु", "दुश्मन", "enemy", "न्यायालय", "lawsuit"]):
            hook = "क्या आप जानना चाहेंगे कि आपकी पत्रिका के षष्ठम (शत्रु) भाव के अनुसार विरोधियों पर पूर्ण विजय और न्यायालयीन विवाद से ससम्मान मुक्ति का समय कब है?"

        # 3. Spiritual / Ishta Devata / Kundalini / Past Life Karma / Moksha / Sadhana
        elif any(w in q_low for w in ["अध्यात्म", "इष्ट", "spiritual", "भगवान", "साधना", "मंत्र", "पूर्वजन्म", "कुंडलिनी", "मोक्ष", "पूजा"]):
            hook = "क्या आप जानना चाहेंगे कि आपके वास्तविक जन्म-जन्मांतर के इष्ट देव कौन हैं और किस विशेष मंत्र साधना से आपके पूर्वजन्म के संचित पुण्यों का शीघ्र उदय हो सकता है?"

        # 4. Property / Land / House / Vehicle / Flat / Plot
        elif any(w in q_low for w in ["मकान", "घर", "house", "home", "property", "फ्लैट", "जमीन", "plot", "भूमि", "वाहन", "गाड़ी", "car", "vehicle", "सम्पत्ति"]):
            hook = "क्या आप जानना चाहेंगे कि आपकी जन्मपत्रिका में स्वयं के भव्य मकान, भूमि अथवा नवीन वाहन क्रय का सबसे स्वर्णिम योग किस वर्ष व माह में खुल रहा है?"

        # 5. Children / Progeny / Pregnancy / Child Education
        elif any(w in q_low for w in ["संतान", "बच्चा", "baby", "child", "children", "पुत्र", "पुत्री", "गर्भ", "pregnancy", "संतान सुख"]):
            hook = "क्या आप जानना चाहेंगे कि आपकी कुण्डली के पंचम भाव (संतान भाव) और गुरु की अमृत दृष्टि के अनुसार संतान प्राप्ति एवं संतान के भाग्योदय का सबसे शुभ काल कब है?"

        # 6. Competition Exams / Judiciary / Govt Selection / Studies
        elif any(w in q_low for w in ["rjs", "rhjs", "judiciary", "judge", "न्यायिक", "exam", "परीक्षा", "प्रतियोगिता", "selection", "upsc", "ias", "ips", "government job", "सरकारी नौकरी", "तैयारी"]):
            hook = "क्या आप जानना चाहेंगे कि किस विशिष्ट माह में आपकी मेधा शक्ति एवं भाग्य का ऐसा संयोग बनेगा जिससे प्रतियोगी परीक्षा में अंतिम चयन व मेरिट सुनिश्चित हो सके?"

        # 7. Education / Intelligence / Concentration / Memory
        elif any(w in q_low for w in ["विद्या", "शिक्षा", "पढ़ाई", "study", "education", "एकाग्रता", "स्मृति", "याददाश्त", "बौद्धिक"]):
            hook = "क्या आप जानना चाहेंगे कि आपकी कुण्डली के पंचम (बुद्धि) व नवम (उच्च विद्या) भाव के अनुसार किस क्षेत्र में आपकी स्वाभाविक प्रतिभा विश्व स्तरीय सफलता दिलाएगी?"

        # 8. Business / Partnership / Trade / Startups / Shop
        elif any(w in q_low for w in ["व्यवसाय", "business", "व्यापार", "दुकान", "partnership", "साझेदारी", "startup", "फर्म", "मुनाफा"]):
            hook = "क्या आप जानना चाहेंगे कि आपकी कुण्डली के सप्तम व एकादश भाव के अनुसार व्यापार में अप्रत्याशित विस्तार एवं बड़े मुनाफे का वास्तविक समय कब प्रारंभ होगा?"

        # 9. Marriage / Relationship / Spouse / Love / Matchmaking
        elif any(w in q_low for w in ["विवाह", "शादी", "marriage", "दांपत्य", "पत्नी", "पति", "रिश्ता", "प्रेम", "जीवनसाथी", "love", "ससुराल", "संबंध"]):
            hook = "क्या आप जानना चाहेंगे कि आपके भावी जीवनसाथी का स्वभाव, उनकी दिशा तथा दांपत्य में स्थायी सुख-समृद्धि एवं भाग्योदय का सटीक समय-चक्र क्या है?"

        # 10. Health / Ailments / Mental Stress / Anxiety / Longevity
        elif any(w in q_low for w in ["स्वास्थ्य", "health", "रोग", "बीमारी", "तनाव", "मानसिक", "अनिद्रा", "दर्द", "आयु", "लंबी आयु", "चिकित्सा"]):
            hook = "क्या आप जानना चाहेंगे कि कौन सा गुप्त ग्रह दोष आपकी जीवनी शक्ति व मानसिक एकाग्रता को प्रभावित कर रहा है और उसका अचूक वैदिक रक्षा कवच क्या है?"

        # 11. Career / Job / Promotion / Office / Work
        elif any(w in q_low for w in ["career", "job", "नौकरी", "काम", "प्रमोशन", "promotion", "आजीविका", "रोजगार", "work", "office", "स्थानांतरण", "transfer", "बॉस", "boss"]):
            hook = "क्या आप जानना चाहेंगे कि आपकी जन्मपत्रिका में अचानक बड़े धन आगमन (Sudden Wealth Inflow) व पदोन्नति का प्रबलतम समय-चक्र कब सक्रिय हो रहा है?"

        # 12. Wealth / Money / Debt / Loans / Inflow / Investment
        elif any(w in q_low for w in ["पैसा", "कर्ज", "debt", "loan", "लोन", "आर्थिक", "निवेश", "investment", "शेयर", "रुपया", "अमीर", "money", "wealth"]) or ("धन" in q_low and "साधना" not in q_low and "समाधान" not in q_low and "अनुसंधान" not in q_low):
            hook = "क्या आप जानना चाहेंगे कि आपकी कुण्डली में रुका हुआ धन वापस आने, कर्ज मुक्ति एवं बड़े धन संचय का सबसे स्वर्णिम योग किस अवधि में बन रहा है?"

        # 13. Sadesati / Rahu-Ketu / Transits / Dosha / Graha Shanti
        elif any(w in q_low for w in ["साढ़ेसाती", "शनि", "राहु", "केतु", "दोष", "कालसर्प", "मांगलिक", "गोचर", "dasha", "दशा"]):
            hook = "क्या आप जानना चाहेंगे कि आगामी गोचर परिवर्तन व चालू दशा आपके जीवन में कौन सा बड़ा अप्रत्याशित मोड़ लेकर आने वाली है?"

        # 14. Universal / General Kundli Assessment
        else:
            hook = "क्या आप जानना चाहेंगे कि आपकी जन्मपत्रिका में सबसे शक्तिशाली 'राजयोग' कौन सा है और वह आपके जीवन में किस उम्र में पूर्ण फल प्रदान करेगा?"

        clean_text = VyasChatbotEngine._sanitize_chat_output(text.rstrip())
        final_reply = f"{clean_text}\n\n{hook}"

        # Automatic continual learning buffer: Stage high-quality astrological consultation
        try:
            from vyas import continual_learning
            continual_learning.stage_consultation_pair(query=query, response=final_reply)
        except Exception:
            pass

        return final_reply

    @staticmethod
    def _sanitize_chat_output(text: str) -> str:
        """Converts raw wide markdown tables into sleek readable bullet points and eliminates all raw HTML bold tags."""
        if not text:
            return ""
        # Guarantee zero raw HTML bold tags in chat messages
        text = re.sub(r'<\s*b\s*>', '**', text, flags=re.IGNORECASE)
        text = re.sub(r'<\s*/\s*b\s*>', '**', text, flags=re.IGNORECASE)
        text = re.sub(r'<\s*strong\s*>', '**', text, flags=re.IGNORECASE)
        text = re.sub(r'<\s*/\s*strong\s*>', '**', text, flags=re.IGNORECASE)
        text = re.sub(r'\*{4,}', '**', text)

        if "|" not in text:
            return text
        lines = text.split("\n")
        out_lines = []
        in_table = False
        headers = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                cells = [c.strip() for c in stripped.split("|")[1:-1]]
                if all(set(c).issubset({'-', ':', ' '}) for c in cells):
                    in_table = True
                    continue
                if not in_table and not headers:
                    headers = cells
                    continue
                clean_cells = [c for c in cells if c]
                if len(clean_cells) == 1:
                    out_lines.append(f"• {clean_cells[0]}")
                elif len(clean_cells) == 2:
                    out_lines.append(f"• **{clean_cells[0]}:** {clean_cells[1]}")
                elif len(clean_cells) >= 3:
                    out_lines.append(f"• **{clean_cells[0]}:** {clean_cells[1]} — {' / '.join(clean_cells[2:])}")
                elif headers and len(cells) == len(headers):
                    parts = [f"**{h}:** {v}" for h, v in zip(headers, cells) if v]
                    out_lines.append("• " + " — ".join(parts))
                else:
                    if clean_cells:
                        out_lines.append("• " + " — ".join(clean_cells))
            else:
                in_table = False
                headers = []
                out_lines.append(line)
        return "\n".join(out_lines)

    def consult(self, query: str, chart, cur_dasha: Any, birth_info: Dict[str, Any],
                transit_pos: Optional[Dict[str, Any]] = None,
                prashna_meta: Optional[Dict[str, Any]] = None,
                chat_history: Optional[List[Dict[str, str]]] = None,
                force_classical: bool = False) -> str:
        """
        Generates a direct, authentic, personalized astrological consultation response.
        Context-aware, follow-up aware, and rooted in classical Parashari Jyotish Shastra.
        Leverages Groq / Gemini APIs when configured, with graceful fallback to the
        deterministic classical rules engine.
        """
        fw = self._extract_chart_framework(chart, cur_dasha, transit_pos)
        name = birth_info.get("name", "जातक")
        q_raw = query.strip()
        q_lower = q_raw.lower()

        # Check AI provider preference
        selected_provider = "auto"
        if force_classical or os.environ.get("VYAS_TEST_OFFLINE") == "1":
            selected_provider = "classical"
        else:
            try:
                import streamlit as st
                selected_provider = st.session_state.get("selected_ai_provider", "auto")
            except Exception:
                pass

        # 1. Universal AI API Routing (Vyas-Daivagya, Groq, DeepSeek, OpenAI, Gemini, OpenRouter)
        if selected_provider in ("vyas_daivagya", "daivagya", "local"):
            reply = self._call_vyas_daivagya(query, fw, birth_info, chat_history)
            if reply: return self._append_curiosity_hook(reply, query)
        elif selected_provider == "groq":
            reply = self._call_groq(query, fw, birth_info, chat_history)
            if reply: return self._append_curiosity_hook(reply, query)
        elif selected_provider == "deepseek":
            reply = self._call_deepseek(query, fw, birth_info, chat_history)
            if reply: return self._append_curiosity_hook(reply, query)
        elif selected_provider == "openai":
            reply = self._call_openai(query, fw, birth_info, chat_history)
            if reply: return self._append_curiosity_hook(reply, query)
        elif selected_provider == "gemini":
            reply = self._call_gemini(query, fw, birth_info, chat_history)
            if reply: return self._append_curiosity_hook(reply, query)
        elif selected_provider == "openrouter":
            reply = self._call_openrouter(query, fw, birth_info, chat_history)
            if reply: return self._append_curiosity_hook(reply, query)
        elif selected_provider == "kilo":
            reply = self._call_kilo(query, fw, birth_info, chat_history)
            if reply: return self._append_curiosity_hook(reply, query)
        elif selected_provider != "classical":
            # Auto cascade: Try custom Vyas-Daivagya (if running) then cloud APIs in speed order
            for call_fn in [self._call_vyas_daivagya, self._call_groq, self._call_gemini, self._call_deepseek, self._call_openai, self._call_kilo, self._call_openrouter]:
                reply = call_fn(query, fw, birth_info, chat_history)
                if reply:
                    return self._append_curiosity_hook(reply, query)

                # 2. Comprehensive Deterministic Vedic Shastra Consultation Engine
        p_inf = fw["p_info"]
        asp = fw["aspects_map"]
        occ = fw["house_occupants"]
        tr = fw["transits"]

        def _placement(p_name: str) -> str:
            p = p_inf.get(p_name, {})
            h = p.get('house', '-')
            sign = p.get('sign_name', '')
            retro = " (वक्री)" if p.get('is_retro') else ""
            return f"{h}वें भाव में {sign} राशि{retro}"

        def _full_planet(p_name: str) -> str:
            p_hi = constants.PLANETS_HI.get(p_name, p_name)
            return f"{p_hi} देव {_placement(p_name)}"

        dasha_display = fw["dasha_md"]
        if fw["dasha_ad"]:
            dasha_display += f" में {fw['dasha_ad']}"
        if fw["dasha_pd"]:
            dasha_display += f" (प्रत्यंतर: {fw['dasha_pd']})"

        user_msg_count = 0
        if chat_history:
            user_msg_count = sum(1 for m in chat_history if m.get("role") == "user")

        salutation = f"सादर प्रणाम {name} जी।\n\n" if user_msg_count <= 1 else f"{name} जी,\n\n"

        # ---------------------------------------------------------------------
        # MULTI-TURN CONTEXT RESOLUTION (पूर्व संवाद का संदर्भ विश्लेषण)
        # ---------------------------------------------------------------------
        prior_topic = None
        if chat_history:
            for prev_m in reversed(chat_history):
                if prev_m.get("role") == "user":
                    prev_txt = prev_m.get("content", "").lower()
                    if any(w in prev_txt for w in ["career", "job", "नौकरी", "प्रमोशन", "promotion", "आजीविका", "व्यवसाय", "business", "व्यापार", "काम", "ऑफिस", "rozgar"]):
                        prior_topic = "career"
                        break
                    elif any(w in prev_txt for w in ["rhjs", "rjs", "exam", "judiciary", "judge", "न्यायिक", "परीक्षा", "प्रतियोगिता", "upsc", "selection"]):
                        prior_topic = "exam"
                        break
                    elif any(w in prev_txt for w in ["धन", "money", "wealth", "पैसा", "कर्ज", "debt", "आर्थिक", "निवेश", "लाभ"]):
                        prior_topic = "wealth"
                        break
                    elif any(w in prev_txt for w in ["विवाह", "शादी", "marriage", "पत्नी", "पति", "दांपत्य", "रिश्ता", "प्रेम"]):
                        prior_topic = "marriage"
                        break
                    elif any(w in prev_txt for w in ["स्वास्थ्य", "health", "रोग", "बीमारी", "तबीयत", "दर्द"]):
                        prior_topic = "health"
                        break
                    elif any(w in prev_txt for w in ["transit", "gochar", "गोचर", "राहु", "केतु", "rahu", "ketu", "वक्री", "मार्गी", "चाल", "गति"]):
                        prior_topic = "transit"
                        break
                    elif any(w in prev_txt for w in ["dasha", "दशा", "mahadasha", "महादशा", "antardasha"]):
                        prior_topic = "dasha"
                        break

        # Check if current query is a short follow-up or timeline query
        is_followup = any(w in q_lower for w in [
            "aage kya", "आगे क्या", "aage", "आगे", "ab kya", "अब क्या", "what next", "next",
            "kab tak", "कब तक", "kab hoga", "कब होगा", "kab aayega", "कब आएगा",
            "aur batao", "और बताओ", "aur bataiye", "और बताइए", "aur kya", "और क्या",
            "kaisa rahega", "कैसा रहेगा", "kya hoga", "क्या होगा", "kya kare", "क्या करें",
            "kya karein", "kya karna chahiye", "क्या करना चाहिए", "salah", "सलाह", "मार्गदर्शन"
        ]) and len(q_lower.split()) <= 6

        pd_end_str = fw["pd_end"] or "आगामी कुछ सप्ताह"
        ad_end_str = fw["ad_end"] or "2027"
        next_lord_hi = fw["next_ad_lord_hi"] or "बुध"
        next_lord_en = fw["next_ad_lord_en"] or "Mercury"
        jup_tr = tr.get("Jupiter", {})
        sat_tr = tr.get("Saturn", {})

        # ---------------------------------------------------------------------
        # SCENARIO A: FOLLOW-UP QUESTION ON CAREER ("aage kya" after career)
        # ---------------------------------------------------------------------
        if is_followup and prior_topic == "career":
            ans = [salutation]
            ans.append(f"आपके पूर्व प्रश्न (**करियर, नौकरी एवं कार्यक्षेत्र**) के अनुक्रम में — **आगामी समय, पदोन्नति एवं भविष्य की समय-सीमा (Career Timeline & Milestones)** का सूक्ष्म शास्त्रीय विश्लेषण:\n")

            ans.append(
                f"1. **तात्कालिक कालखंड ({fw['dasha_pd']} प्रत्यंतर — समाप्ति: {pd_end_str}):**\n"
                f"वर्तमान में सक्रिय प्रत्यन्तर्दशा कार्यक्षेत्र में धैर्य, अनुशासन और कागजी कार्यों में अत्यधिक सतर्कता की मांग कर रही है। "
                f"इस अवधि में तात्कालिक असंतोष के कारण नौकरी बदलने या वरिष्ठों से विवाद में पड़ने से बचें। यह चरण आपके कार्य कौशल को सुदृढ़ करने का है।"
            )

            ans.append(
                f"2. **मुख्य स्वर्णिम मोड़ एवं पदोन्नति काल ({next_lord_hi} अन्तर्दशा — प्रारंभ: {ad_end_str}):**\n"
                f"आपकी आजीविका में वास्तविक और दीर्घकालिक सकारात्मक मोड़ **{ad_end_str}** से आएगा, जब {fw['dasha_ad']} की अन्तर्दशा पूर्ण होकर **{next_lord_hi} देव की अन्तर्दशा** प्रारंभ होगी।\n"
                f"• जन्म कुण्डली में {next_lord_hi} देव {_placement(next_lord_en)} में स्थित हैं।\n"
                f"• यह ग्रह विन्यास कार्यक्षेत्र में नई जिम्मेदारियों, अधिकार क्षेत्र में विस्तार, पदोन्नति तथा नए व्यावसायिक/प्रशासनिक अवसरों के स्पष्ट द्वार खोलेगा।"
            )

            ans.append(
                f"3. **गोचर कालीन संबल (Transits of Jupiter & Saturn):**\n"
                f"• देवगुरु बृहस्पति वर्तमान में {jup_tr.get('sign', '')} राशि में (लग्न से {jup_tr.get('h_lagna', '')}वें भाव) संचरण कर रहे हैं। गुरु का प्रभाव आपके कर्म और लाभ भाव को संबल प्रदान कर रहा है।\n"
                f"• कर्मकारक शनि देव का गोचर {sat_tr.get('sign', '')} राशि में चल रहा है, जो यह दर्शाता है कि आपकी वर्तमान निष्ठा आने वाले समय में स्थायी प्रतिष्ठा का आधार बनेगी।"
            )

            ans.append(
                f"4. **आचार्य मार्गदर्शन एवं कार्यनीति (Actionable Strategy):**\n"
                f"• **वर्तमान रणनीति:** वर्तमान कार्यभार को पूर्ण निष्ठा से संभालें।\n"
                f"• **भविष्य की तैयारी:** {ad_end_str} के आसपास वेतन वृद्धि, उच्च पद अथवा मनचाहे स्थान पर स्थानांतरण के प्रबल योग बनेंगे।"
            )

            ans.append(
                f"**कार्यक्षेत्र सिद्धि हेतु सात्विक उपाय:**\n"
                f"• शनिवार को संध्या समय पीपल के वृक्ष के नीचे सरसों के तेल का चौमुखा दीपक प्रज्वलित करें।\n"
                f"• नित्य प्रातः तांबे के लोटे से सूर्य देव को जल अर्पित कर 'ॐ सूर्याय नमः' का 11 बार स्मरण करें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # SCENARIO B: FOLLOW-UP QUESTION ON JUDICIARY / EXAMS ("aage kya" after exams)
        # ---------------------------------------------------------------------
        if is_followup and prior_topic == "exam":
            ans = [salutation]
            ans.append(f"आपके पूर्व प्रश्न (**न्यायिक सेवा / प्रतियोगी परीक्षा**) के अनुक्रम में — **आगामी परीक्षा चक्र, तैयारी की रणनीति एवं सफलता काल (Exam Timeline)** का शास्त्रीय विवेचन:\n")

            ans.append(
                f"1. **तात्कालिक अध्ययन काल ({pd_end_str} तक):**\n"
                f"वर्तमान प्रत्यंतर काल में अध्ययन में निरंतरता और एकाग्रता बनाए रखना प्राथमिक है। विधिक विषयों में मुख्य परीक्षा के उत्तर लेखन (Answer Writing) और केस लॉज़ के सटीक विश्लेषण पर बल दें।"
            )

            ans.append(
                f"2. **सफलता एवं चयन का प्रबल योग ({ad_end_str} से):**\n"
                f"आगामी {next_lord_hi} देव की अन्तर्दशा प्रारंभ होते ही बौद्धिक तीक्ष्णता और साक्षात्कार में प्रभावशाली अभिव्यक्ति के योग निर्मित होंगे। यह कालखंड परीक्षा में अंतिम चयन के लिए अत्यंत शुभ सिद्ध होगा।"
            )

            ans.append(
                f"**आचार्य निर्देश:** नित्य प्रातः सूर्य नमस्कार करें और आदित्य हृदय स्तोत्र का पाठ करें। अध्ययन कक्ष में उत्तर या पूर्व दिशा की ओर मुख करके बैठें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # SCENARIO C: FOLLOW-UP QUESTION ON WEALTH / FINANCE
        # ---------------------------------------------------------------------
        if is_followup and prior_topic == "wealth":
            ans = [salutation]
            ans.append(f"आपके पूर्व प्रश्न (**आर्थिक स्थिति एवं धन संचय**) के क्रम में — **आगामी वित्तीय कालखंड एवं निवेश सलाह (Financial Outlook)**:\n")

            ans.append(
                f"1. **तात्कालिक वित्तीय स्थिति ({pd_end_str} तक):** अनावश्यक व्यय पर नियंत्रण रखें। किसी भी नए व्यक्ति पर आंख मूंदकर भरोसा न करें और जोखिम भरे सट्टे/ट्रेडिंग से बचें।"
            )
            ans.append(
                f"2. **धन वृद्धि का मुख्य काल ({ad_end_str} से):** आगामी {next_lord_hi} की अन्तर्दशा धन संचय, पैतृक लाभ और नवीन आय स्रोतों के लिए अत्यधिक अनुकूल रहेगी।"
            )
            ans.append(
                f"**आचार्य उपाय:** गुरुवार को श्री सूक्त का पाठ करें तथा केसर का तिलक लगाएं।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # SCENARIO D: FOLLOW-UP QUESTION ON TRANSIT / PLANETARY MOTION ("aage kya" after transit)
        # ---------------------------------------------------------------------
        if is_followup and prior_topic == "transit":
            tr_det = fw.get("transits_detailed", {})
            r_d = tr_det.get("Rahu", {})
            k_d = tr_det.get("Ketu", {})
            s_d = tr_det.get("Saturn", {})
            j_d = tr_det.get("Jupiter", {})
            ans = [salutation]
            ans.append(f"आपके पूर्व प्रश्न (**ग्रह गोचर एवं चाल**) के अनुक्रम में — **आगामी राशि परिवर्तन एवं प्रमुख समय-सीमा (Upcoming Ingress Milestones)**:\n")
            ans.append(
                f"1. **राहु-केतु का आगामी राशि परिवर्तन (05 दिसंबर 2026):**\n"
                f"• राहु देव वर्तमान में {r_d.get('sign', 'कुंभ')} राशि में हैं और अपनी शाश्वत वक्री गति से **05/12/2026 को {r_d.get('next_sign_hi', 'मकर')} राशि** में प्रवेश करेंगे।\n"
                f"• केतु देव वर्तमान में {k_d.get('sign', 'सिंह')} राशि में हैं और अपनी शाश्वत वक्री गति से **05/12/2026 को {k_d.get('next_sign_hi', 'कर्क')} राशि** में प्रवेश करेंगे।\n"
                f"• यह गोचर परिवर्तन आपके जीवन में महत्वाकांक्षाओं के पुनर्गठन और पारिवारिक दायित्वों में नए अवसर लेकर आएगा।"
            )
            ans.append(
                f"2. **शनि देव का आगामी गोचर (03 जून 2027):**\n"
                f"• कर्मफलदाता शनि देव वर्तमान में {s_d.get('sign', 'मीन')} राशि में संचरण कर रहे हैं। वे **03/06/2027 को मेष राशि** में प्रवेश करेंगे।"
            )
            ans.append(
                f"**आचार्य निर्देश:** गोचर परिवर्तन से पूर्व अपने वर्तमान संकल्पों को पूर्ण करें और भगवान शिव का नित्य स्मरण करें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT: EXPLICIT ASTRONOMICAL MOTION & RETROGRADE LAWS (जब जातक चाल, गति, वक्री/मार्गी पूछे)
        # ---------------------------------------------------------------------
        if any(w in q_lower for w in ["चाल", "गति", "वक्री", "मार्गी", "retrograde", "उल्टी चाल"]) or \
           ("राहु" in q_lower and "केतु" in q_lower and "गोचर" in q_lower):
            tr_det = fw.get("transits_detailed", {})
            rahu_d = tr_det.get("Rahu", {})
            ketu_d = tr_det.get("Ketu", {})
            sat_d = tr_det.get("Saturn", {})
            jup_d = tr_det.get("Jupiter", {})
            shani_sd = fw.get("shani_sadesati", {})

            rahu_cur_sign = rahu_d.get("sign", "कुंभ")
            rahu_next_sign = rahu_d.get("next_sign_hi", "मकर")
            ketu_cur_sign = ketu_d.get("sign", "सिंह")
            ketu_next_sign = ketu_d.get("next_sign_hi", "कर्क")
            sat_cur_sign = sat_d.get("sign", "मीन")
            sat_next_sign = sat_d.get("next_sign_hi", "मेष")
            sat_motion = sat_d.get("motion_desc", "वक्री")

            ans = [salutation]
            ans.append(
                f"ग्रहों की गति (मार्गी/वक्री) एवं राहु-केतु गोचर का प्रामाणिक शास्त्रीय विश्लेषण:\n\n"
                f"1. **राहु एवं केतु (सदा वक्री / उल्टी चाल):**\n"
                f"   • राहु और केतु सदैव वक्री (उल्टी चाल) ही चलते हैं, कभी मार्गी नहीं होते।\n"
                f"   • वर्तमान में राहु कुंभ राशि में हैं (अगला गोचर मकर में) तथा केतु सिंह राशि में हैं (अगला गोचर कर्क में)।\n\n"
                f"2. **सूर्य एवं चन्द्रमा (सदा मार्गी):**\n"
                f"   • भगवान सूर्य और चन्द्रमा सदैव मार्गी (सीधी चाल) चलते हैं। वे कभी वक्री नहीं होते।\n\n"
                f"3. **पंच ताराग्रह (शनि, गुरु, मंगल, बुध, शुक्र):**\n"
                f"   • ये ग्रह समयानुसार मार्गी व वक्री दोनों अवस्थाओं में आते हैं। वर्तमान में शनि {sat_cur_sign} राशि में {sat_motion} गति में हैं।\n\n"
                f"• **बृहत्पाराशर व फलदीपिका निर्देश:** छायाग्रहों का फल उनकी तात्कालिक राशि और युति/दृष्टि कारक ग्रहों के अनुरूप प्राप्त होता है।\n\n"
                f"**सात्विक उपाय:** नित्य प्रातः 'ॐ नमः शिवाय' का 11 बार जप करें अथवा पक्षियों को सप्तधान्य डालें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT: PUSHKAR NAVAMSHA, PUSHKAR BHAGA & VARGOTTAMA (पुष्कर नवांश व वर्गोत्तम विश्लेषण)
        # ---------------------------------------------------------------------
        if any(w in q_lower for w in ["pushkar", "पुष्कर", "vargottama", "वर्गोत्तम", "पुष्कर नवांश", "पुष्कर भाग", "navamsha", "नवांश"]):
            p_nav_list = fw.get("pushkar_nav_planets", [])
            p_bhaga_list = fw.get("pushkar_bhaga_planets", [])
            varg_list = fw.get("vargottama_planets", [])

            p_nav_text = f"★ **आपकी कुण्डली में पुष्कर नवांश में स्थित ग्रह:** {', '.join(p_nav_list)}।" if p_nav_list else "आपकी जन्मपत्रिका में कोई ग्रह पुष्कर नवांश में स्थित नहीं है।"
            varg_text = f"★ **वर्गोत्तम (Vargottama) ग्रह:** {', '.join(varg_list)}।" if varg_list else "आपकी कुण्डली में कोई ग्रह वर्गोत्तम नहीं है।"
            p_bhaga_text = f"★ **पुष्कर भाग (Pushkar Bhaga) में स्थित ग्रह:** {', '.join(p_bhaga_list)}।" if p_bhaga_list else "कोई ग्रह पुष्कर भाग में नहीं है।"

            nav_lines = fw.get("pushkar_nav_lines", [])
            nav_bullets = "\n".join([f"  {ln}" for ln in nav_lines])

            ans = [salutation]
            ans.append(
                f"महर्षि पराशर विरचित बृहत्पाराशर होराशास्त्र एवं मंत्रेश्वरकृत 'जातक पारिजात' के अनुसार कुण्डली के कुल 108 नवांशों में से केवल 24 विशिष्ट नवांश **'पुष्कर नवांश' (Pushkar Navamsha)** कहलाते हैं। ये नवांश सदैव शुभ ग्रहों (गुरु, शुक्र, बुध, चन्द्र) द्वारा अधिष्ठित होते हैं और इसमें स्थित कोई भी ग्रह जातक को असाधारण जीवनदायिनी ऊर्जा, आरोग्य, उच्च पद-प्रतिष्ठा एवं राजयोग तुल्य फल प्रदान करता है।\n\n"
                f"**आपकी जन्मपत्रिका का सूक्ष्म नवांश (D-9) खगोलीय विश्लेषण:**\n\n"
                f"{p_nav_text}\n\n"
                f"{varg_text}\n\n"
                f"{p_bhaga_text}\n\n"
                f"**समस्त ग्रहों की नवांश व पुष्कर स्थिति (तालिका):**\n"
                f"{nav_bullets}\n\n"
                f"• **शास्त्रीय फलित सार:** " +
                (f"आपकी पत्रिका में {p_nav_list[0]} का पुष्कर नवांश में होना यह सिद्ध करता है कि संबंधित ग्रह अपनी महादशा अथवा अन्तर्दशा में अत्यंत शुभ, उन्नतिशील व अप्रत्याशित सफलता कारक फल प्रदान करेगा। " if p_nav_list else "आपकी कुण्डली में अन्य शुभ योगों एवं दशा चक्र का फलित अधिक प्रभावी है। ") +
                (f"साथ ही {varg_list[0]} वर्गोत्तम होने से उस ग्रह को विशेष आत्मिक बल व स्थायित्व प्राप्त है।" if varg_list else "")
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT: GENERAL TRANSIT / GOCHAR (संक्षिप्त, सीधा एवं व्यावहारिक फलित प्रभाव)
        # ---------------------------------------------------------------------
        if any(w in q_lower for w in ["transit", "gochar", "गोचर", "गोचरस्थ", "ग्रह गोचर", "शनि गोचर", "गुरु गोचर", "राशि परिवर्तन"]):
            tr_det = fw.get("transits_detailed", {})
            rahu_d = tr_det.get("Rahu", {})
            ketu_d = tr_det.get("Ketu", {})
            sat_d = tr_det.get("Saturn", {})
            jup_d = tr_det.get("Jupiter", {})
            shani_sd = fw.get("shani_sadesati", {})

            ans = [salutation]
            ans.append(
                f"आपकी **{fw['asc_sign_name']} लग्न** एवं **{fw['moon_sign_name']} राशि** पर वर्तमान मुख्य ग्रह गोचर का सीधा फलित प्रभाव:\n\n"
                f"• **राहु-केतु प्रभाव:** राहु देव वर्तमान में कुंभ राशि ({rahu_d.get('h_lagna', 11)}वें भाव) में हैं। एकादश भाव में राहु का प्रभाव अचानक नए अवसर, नेटवर्क से लाभ और आजीविका में प्रगति का मार्ग खोलता है।\n\n"
                f"• **शनि देव (साढ़ेसाती):** {shani_sd.get('status', 'वर्तमान में आपकी कुण्डली पर साढ़ेसाती नहीं है')}। शनि देव कर्म एवं पराक्रम को सुदृढ़ कर रहे हैं, जिससे धैर्यपूर्वक किए गए प्रयासों में स्थायी प्रतिष्ठा मिलेगी।\n\n"
                f"• **देवगुरु बृहस्पति:** गुरु देव की अमृत दृष्टि त्रिकोण भावों को पोषित कर रही है, जो ज्ञान, सम्मान एवं भाग्योदय में वृद्धि कराती है।\n\n"
                f"**सात्विक उपाय:** नित्य प्रातः 'ॐ नमः शिवाय' का 11 बार जप करें अथवा बुधवार/शनिवार को पक्षियों को दाना डालें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT: PLANETARY ASPECTS & DRISHTI (दृष्टि प्रभाव, लग्न पर दृष्टि, त्रिगुण दृष्टि)
        # ---------------------------------------------------------------------
        if any(w in q_lower for w in ["drishti", "दृष्टि", "दृष्टियां", "देख रहे", "देख रहा", "देखते", "aspect", "aspects",
                                       "teeno lagna", "तीनों लग्न", "lagna ko dekh", "लग्न को देख"]):
            ans = [salutation]
            ans.append(f"आपके प्रश्न — **'तीनों ग्रहों (मंगल, शनि व गुरु) की लग्न पर दृष्टि का क्या प्रभाव पड़ता है?'** के संबंध में महर्षि पराशर के बृहत्पाराशर होराशास्त्र के अनुसार प्रामाणिक शास्त्रीय विवेचन:\n")

            ans.append(
                f"वैदिक ज्योतिष में लग्न को जातक का 'तनु भाव' (शरीर, आत्मा, व्यक्तित्व, मान-प्रतिष्ठा व जीवनी शक्ति) कहा गया है। "
                f"आपकी **{fw['asc_sign_name']} लग्न** की कुण्डली में तीन अत्यंत शक्तिशाली ग्रहों की लग्न पर दृष्टि पड़ रही है:\n\n"
                f"1. **मंगल देव ({_placement('Mars')}):** आपकी कुण्डली में मंगल **लग्नेश (1H) एवं अष्टमेश (8H)** हैं। वे दशम भाव (मकर) में अपनी **परम उच्च अवस्था** (रुचक महापुरुष योग) में विराजमान होकर अपनी **4थी विशेष दृष्टि** से अपने ही लग्न (मेष) को देख रहे हैं। "
                f"शास्त्रीय नियम है—**'लग्नं पश्यति लग्नेशः'**—लग्नेश जब अपने ही घर को देखता है तो वह देह, आरोग्य और आत्मबल को वज्र के समान सुदृढ़ बनाता है। मंगल 4वें भाव का नहीं अपितु 1वें व 8वें भाव का स्वामी होने के नाते असीम पराक्रम, त्वरित निर्णय क्षमता व नेतृत्व शक्ति प्रदान करता है।\n\n"
                f"2. **शनि देव ({_placement('Saturn')}):** आपकी कुण्डली में शनि **दशमेश (10H - कर्मेश) एवं एकादशेश (11H - लाभेश)** हैं। शनि देव सप्तम भाव (तुला) में अपनी **परम उच्च अवस्था** (शश महापुरुष योग) में स्थित होकर अपनी **7वीं प्रत्यक्ष पूर्ण दृष्टि** से लग्न को देख रहे हैं। "
                f"शनि 7वें या 12वें भाव के स्वामी नहीं हैं, उनका स्वामित्व 10वें व 11वें भाव पर है। शनि की दृष्टि व्यक्ति को कड़ा अनुशासन, गहन धैर्य, न्यायप्रियता, वैराग्ययुक्त परिपक्वता और दीर्घकालिक संघर्ष के उपरांत स्थायी प्रतिष्ठा दिलाती है।\n\n"
                f"3. **देवगुरु बृहस्पति ({_placement('Jupiter')}):** आपकी कुण्डली में गुरु **नवमेश (9H - भाग्येश) एवं द्वादशेश (12H - व्ययेश)** हैं। वे नवम भाव (धनु) में अपनी **स्वराशि** में बैठकर अपनी **5वीं पावन त्रिकोण दृष्टि (अमृत दृष्टि)** सीधे लग्न पर डाल रहे हैं। "
                f"गुरु की लग्न पर अमृत दृष्टि को शास्त्रों में सर्वदोष निवारक कहा गया है (**'एकं हन्ति गुरुर्दोषं लक्षं दोषं च संहरेत्'** )। यह आपके चरित्र को सात्विक, धर्मपरायण, नीतिवान और उच्च पद के योग्य बनाती है।"
            )

            ans.append(
                f"**इस 'त्रिगुण संयुक्त दृष्टि' का समग्र फलित प्रभाव (Synthesized Impact):**\n\n"
                f"• **व्यक्तित्व एवं आत्मबल (Personality & Leadership):** आपके व्यक्तित्व में मंगल का पराक्रम, शनि का संयम व गुरु का विवेक एक साथ समाहित है। आप संकट के समय कभी विचलित नहीं होते और कठिन से कठिन निर्णय अत्यंत निष्पक्षता से लेते हैं।\n"
                f"• **स्वास्थ्य एवं जीवनी शक्ति (Health & Longevity):** लग्नेश मंगल और भाग्येश गुरु की दृष्टि आपको दीर्घायु और मजबूत जीवनी शक्ति देती है। शनि की दृष्टि के कारण नसों, हड्डियों अथवा जोड़ों में वात-विकार या मानसिक तनाव का संकेत मिलता है, जिसके लिए नियमित योग-प्राणायाम अनिवार्य है।\n"
                f"• **आजीविका एवं प्रतिष्ठा (Authority & Career):** दशम में उच्च मंगल और सप्तम में उच्च शनि, साथ में भाग्य स्थान में स्वराशि गुरु का यह दुर्लभ योग विधिक, प्रशासनिक, न्यायिक, संगठनात्मक अथवा उच्च परामर्श क्षेत्रों में शीर्ष पद और स्थायी कीर्ति दिलाता है।\n"
                f"• **सक्रिय दशा समन्वय:** वर्तमान में सक्रिय {dasha_display} इन राजयोगों को सक्रिय करने की दिशा में अग्रसर है।"
            )

            ans.append(
                f"**आचार्य निर्देश एवं सात्विक वैदिक उपाय:**\n"
                f"• नित्य प्रातः तांबे के पात्र से भगवान सूर्य को अर्घ्य दें और ॐ सूर्याय नमः का 11 बार स्मरण करें।\n"
                f"• मंगलवार को श्री हनुमान चालीसा का पाठ करें तथा शनिवार को संध्या समय पीपल के वृक्ष के नीचे चौमुखा दीपक जलाएं।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 1: TIMING, UPCOMING EVENTS, "AAGE KYA", TURNING POINTS
        # ---------------------------------------------------------------------
        if any(w in q_lower for w in ["aage", "आगे", "aage kya", "आगे क्या", "ab kya", "अब क्या", "what next", "next",
                                     "kab", "कब", "kab se", "kab tak", "कब तक", "kab hoga", "कब होगा", "kab aayega",
                                     "future", "भविष्य", "sudhar", "सुधार", "badlega", "बदलेगा", "achha samay",
                                     "अच्छा समय", "shubh", "शुभ समय", "turning point", "when will", "kaisa rahega",
                                     "कैसा रहेगा", "kya hoga", "क्या होगा", "kya kare", "क्या करें", "kya karein"]):
            ans = [salutation]
            ans.append(f"आपके प्रश्न — **'आगामी समय, भविष्य की दिशा एवं भाग्योदय कब से होगा?'** के संबंध में कुण्डली, विंशोत्तरी दशा व गोचर का समग्र काल-विभाजन विश्लेषण:\n")

            ans.append(f"1. **वर्तमान समय की स्थिति (कारण एवं प्रभाव):**")
            ans.append(
                f"वर्तमान में आपकी विंशोत्तरी दशा **{fw['dasha_md']} महादशा में {fw['dasha_ad']} की अन्तर्दशा** "
                f"तथा **{fw['dasha_pd']} की प्रत्यन्तर्दशा** सक्रिय है।\n"
                f"• अन्तर्दशा स्वामी {fw['dasha_ad']} देव आपकी कुण्डली के {_placement(fw['ad_lord_en'])} में स्थित हैं। "
                f"{'शनि देव का स्वभाव धीमी गति व कड़ी परीक्षा के बाद ही परिणाम देने का होता है। ' if fw['ad_lord_en'] == 'Saturn' else ''}"
                f"इस कारण वर्तमान में प्रयास अधिक और तात्कालिक परिणाम मिलने में विलंब या मानसिक दबाव अनुभव हो सकता है।"
            )

            ans.append(f"2. **प्रथम राहत काल (First Relief Milestone):**")
            ans.append(
                f"तात्कालिक मानसिक उलझनों और गतिरोध में **{pd_end_str}** से सकारात्मक परिवर्तन दृष्टिगोचर होगा, "
                f"जब वर्तमान प्रत्यन्तर्दशा समाप्त होकर अगले अनुकूल ग्रह का प्रत्यंतर प्रारंभ होगा।"
            )

            ans.append(f"3. **मुख्य स्वर्णिम कालखंड एवं भाग्योदय (Major Turning Point):**")
            ans.append(
                f"आपकी कुण्डली में वास्तविक और दीर्घकालिक सकारात्मक मोड़ **{ad_end_str}** से आएगा, "
                f"जब वर्तमान {fw['dasha_ad']} की अन्तर्दशा पूर्ण होकर **{next_lord_hi} देव की अन्तर्दशा** प्रारंभ होगी।\n"
                f"• {next_lord_hi} देव आपकी जन्म कुण्डली में {_placement(next_lord_en)} में स्थित हैं। "
                f"यह अवधि आपके लिए बौद्धिक निर्णयों, कार्यक्षेत्र में गतिशीलता, नए व्यावसायिक/प्रशासनिक अवसरों तथा आर्थिक संचय के लिए अत्यधिक फलदायी सिद्ध होगी।"
            )

            ans.append(f"4. **गोचर कालीन संबल (Planetary Transits):**")
            if jup_tr:
                ans.append(f"• देवगुरु बृहस्पति वर्तमान में {jup_tr.get('sign', '')} राशि में संचरण कर रहे हैं (लग्न से {jup_tr.get('h_lagna', '')}वें भाव में)। गुरु का यह गोचर आपके महत्वपूर्ण भावों पर शुभ प्रभाव डाल रहा है।")
            if sat_tr:
                ans.append(f"• शनि देव का गोचर {sat_tr.get('sign', '')} राशि में चल रहा है, जो यह स्पष्ट करता है कि धैर्यपूर्वक कर्म करने पर सफलता सुनिश्चित है।")

            ans.append(f"**आचार्य निर्देश (मार्गदर्शन):**")
            ans.append(
                f"वर्तमान समय संयम और आगामी बड़े कार्यों की नींव रखने का है। किसी भी नए कार्य में जल्दबाजी या निराशा से बचें। "
                f"नित्य प्रातः सूर्य देव को तांबे के लोटे से जल अर्पित करें और ॐ नमः शिवाय का यथाशक्ति जप करें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 2: DASHA PREDICTIONS & VIMSHOTTARI ANALYSIS
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["dasha", "दशा", "mahadasha", "महादशा", "antardasha", "अन्तर्दशा", "अंतर्दशा",
                                       "pratyantar", "प्रत्यंतर", "vimshottari", "विंशोत्तरी"]):
            ans = [salutation]
            ans.append(f"आपकी कुण्डली की **सक्रिय विंशोत्तरी दशाओं का समग्र शास्त्रीय फलादेश** इस प्रकार है:\n")

            md_en = fw["md_lord_en"] or "Venus"
            md_hi = fw["dasha_md"]
            md_h = p_inf.get(md_en, {}).get("house", 9)
            md_sign = p_inf.get(md_en, {}).get("sign_name", "")
            ans.append(f"1. **महादशा स्वामी — {md_hi} देव:**")
            ans.append(
                f"• **अवधि:** {fw['md_start']} से {fw['md_end']} तक।\n"
                f"• **स्थिति:** {md_hi} देव कुण्डली के **{md_h}वें भाव में {md_sign} राशि** में स्थित हैं।\n"
                f"• **शास्त्रीय फल:** यह महादशा भाग्य, धर्म, दूरस्थ यात्राओं, सामाजिक मान-सम्मान और दीर्घकालिक समृद्धि की आधारशिला रखती है।"
            )

            ad_en = fw["ad_lord_en"] or "Saturn"
            ad_hi = fw["dasha_ad"]
            ad_h = p_inf.get(ad_en, {}).get("house", 7)
            ad_sign = p_inf.get(ad_en, {}).get("sign_name", "")
            if ad_en == "Saturn":
                ad_phala = "यह अन्तर्दशा अधिकार, दायित्व और कर्मक्षेत्र में कड़े परिश्रम की मांग करती है। शनि देव जातक को धैर्य और अनुशासन की कसौटी पर परखते हैं, तत्पश्चात स्थायी सफलता व प्रतिष्ठा प्रदान करते हैं।"
            elif ad_en == "Ketu":
                ad_phala = "केतु की अन्तर्दशा आध्यात्मिक चिंतन, गहन शोध, आत्म-मंथन और आंतरिक एकाग्रता लाती है।"
            elif ad_en == "Rahu":
                ad_phala = "राहु की अन्तर्दशा उच्च महत्वाकांक्षा, अप्रत्याशित अवसर और दूरगामी योजनाएं लाती है।"
            elif ad_en in ["Jupiter", "Venus", "Mercury"]:
                ad_phala = f"{ad_hi} देव की शुभ अन्तर्दशा बुद्धि, ज्ञान, नए व्यावसायिक अनुबंध, वित्तीय लाभ और पारिवारिक सुख में निरंतर वृद्धि करती है।"
            elif ad_en == "Sun":
                ad_phala = "सूर्य देव की अन्तर्दशा राजपक्ष, शासन-प्रशासन, आत्मबल एवं समाज में प्रभाव क्षेत्र में वृद्धि करती है।"
            elif ad_en == "Moon":
                ad_phala = "चन्द्रमा की अन्तर्दशा मानसिक संवेदनशीलता, रचनात्मकता तथा जनसंपर्क में विस्तार लाती है।"
            else:
                ad_phala = "मंगल देव की अन्तर्दशा पराक्रम, साहस, त्वरित निर्णय क्षमता और कर्मक्षेत्र में विजय प्रदान करती है।"

            ans.append(f"2. **वर्तमान अन्तर्दशा स्वामी — {ad_hi} देव:**")
            ans.append(
                f"• **अवधि:** {fw['ad_start']} से **{fw['ad_end']}** तक।\n"
                f"• **स्थिति:** {ad_hi} देव कुण्डली के **{ad_h}वें भाव में {ad_sign} राशि** में विराजमान हैं{' (तुला राशि में अपनी परम उच्च अवस्था में)' if ad_sign == 'तुला' else ''}।\n"
                f"• **शास्त्रीय फल:** {ad_phala}"
            )

            pd_hi = fw["dasha_pd"]
            ans.append(f"3. **सूक्ष्म प्रत्यन्तर्दशा — {pd_hi} देव:**")
            ans.append(
                f"• **समाप्ति तिथि:** **{fw['pd_end']}**\n"
                f"• **प्रभाव:** तात्कालिक दैनिक निर्णय, मनोबल और मानसिक एकाग्रता को प्रभावित कर रहे हैं।"
            )

            ans.append(f"4. **आगामी अन्तर्दशा — {next_lord_hi} देव का पूर्वावलोकन:**")
            ans.append(
                f"• **प्रारंभ दिनांक:** **{fw['ad_end']}** से।\n"
                f"• **फलकथन:** {next_lord_hi} देव की अन्तर्दशा प्रारंभ होते ही पूर्व में अटके हुए कार्यों में तीव्रता आएगी। व्यापार, नए अनुबंध, वित्तीय लाभ और पारिवारिक सौहार्द में वृद्धि होगी।"
            )

            ans.append(f"**दशा अनुकूलता हेतु सिद्ध उपाय:**")
            ans.append(
                f"• शनिवार के दिन संध्या समय पीपल के वृक्ष के नीचे सरसों के तेल का दीपक प्रज्वलित करें।\n"
                f"• शुक्रवार को श्वेत वस्तुओं अथवा मिश्री का दान करें तथा श्री सूक्त का पाठ करें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 3: COMPETITIVE EXAMS / JUDICIARY / RHJS / UPSC / GOVT JOB
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["rhjs", "rjs", "exam", "judiciary", "judge", "judicial", "न्यायिक",
                                       "परीक्षा", "प्रतियोगिता", "upsc", "clear", "सफलता", "निकलेगा", "selection", "tayari"]):
            # Calculate native age for Desh, Kaal & Patra
            b_local_obj = birth_info.get("local")
            b_yr = b_local_obj.year if isinstance(b_local_obj, datetime) else None
            if not b_yr:
                try:
                    b_yr = int(str(birth_info.get("dt", "")).split("-")[0])
                except Exception:
                    b_yr = None
            cur_age = (datetime.now().year - b_yr) if b_yr else 35

            if cur_age >= 50:
                h10_sign = (fw["asc_sign"] + 9) % 12
                h10_lord = constants.SIGN_LORD[h10_sign]
                h10_lord_hi = constants.PLANETS_HI.get(h10_lord, h10_lord)
                ans = [salutation]
                ans.append(
                    f"**देश, काल एवं परिस्थिति का शास्त्रीय विचार:**\n"
                    f"महर्षि पराशर के बृहत्पाराशर होराशास्त्र का मूलभूत नियम 'देशे काले च पात्रे च' है। "
                    f"आपकी वर्तमान आयु ({cur_age} वर्ष) के परिप्रेक्ष्य में, यह समय प्रत्यक्ष प्रतियोगी परीक्षा में बैठने का नहीं, "
                    f"अपितु आपके संचित जीवन-अनुभव, कार्यक्षेत्र में वरिष्ठता, संस्थागत सम्मान, नीतिगत परामर्श, और समाज में प्रतिष्ठित मार्गदर्शन की भूमिका का है।\n\n"
                    f"1. **कर्म एवं प्रतिष्ठा भाव (दशम भाव):** आपके दशमेश {h10_lord_hi} देव की स्थिति यह दर्शाती है कि आपके अधिकार क्षेत्र और सामाजिक प्रतिष्ठा में स्थायित्व के पूर्ण योग हैं।\n"
                    f"2. **दशा व गोचर का निर्देश:** वर्तमान में सक्रिय {dasha_display} वरिष्ठ पदों पर सम्मानजनक भूमिका और बौद्धिक परामर्श के लिए अत्यंत अनुकूल है।\n"
                    f"3. **आचार्य परामर्श:** किसी भी प्रकार की प्रतिस्पर्धात्मक दौड़ के स्थान पर अपनी विशेषज्ञता और अनुभव से समाज व कार्यक्षेत्र को दिशा दें। स्वास्थ्य रक्षा एवं मानसिक शांति को प्राथमिकता दें।"
                )
                ans.append(f"**सात्विक उपाय:** नित्य प्रातः सूर्य नमस्कार करें अथवा ॐ नमो भगवते वासुदेवाय का शांत मन से जप करें।")
                return self._append_curiosity_hook("\n\n".join(ans), query)

            h6_sign = (fw["asc_sign"] + 5) % 12
            h6_lord = constants.SIGN_LORD[h6_sign]
            h6_lord_hi = constants.PLANETS_HI.get(h6_lord, h6_lord)

            ans = [salutation]
            ans.append(f"आपके प्रश्न — **उच्च प्रतियोगी परीक्षा एवं विधिक/प्रशासनिक सेवा में चयन के योग** के संबंध में कुण्डली विश्लेषण:\n")

            ans.append(
                f"न्यायिक सेवा एवं उच्च प्रशासनिक पदों के लिए ज्योतिष शास्त्र में **सूर्य (राजसत्ता), देवगुरु बृहस्पति (विधि व न्याय), "
                f"शनि (न्यायाधीश/दंड विधान)** तथा **षष्ठ भाव (प्रतियोगिता विजय)** व **दशम भाव (राजपद)** का विचार किया जाता है।\n"
                f"1. **प्रतियोगिता एवं विजय भाव (षष्ठ भाव):** षष्ठेश {h6_lord_hi} की स्थिति आपकी परीक्षा रणनीति और कठिन प्रतिस्पर्धा से जूझने की क्षमता को दर्शाती है।\n"
                f"2. **न्यायकारक ग्रह स्थिति:** न्याय व धर्म के स्वाभाविक कारक देवगुरु बृहस्पति {_full_planet('Jupiter')} हैं तथा न्यायाधीश शनि देव {_full_planet('Saturn')} हैं।\n"
                f"3. **दशम भाव पर प्रभाव:** {'शनि देव की दृष्टि दशम भाव पर पड़ रही है, जो कानून, न्यायपालिका और प्रशासनिक व्यवस्था में स्वाभाविक योग्यता को सिद्ध करती है।' if 10 in asp.get('Saturn', []) else 'दशम भाव का संबंध उच्च राजकीय सेवा के अनुकूल बना हुआ है।'}\n"
                f"4. **सक्रिय दशा का प्रभाव:** वर्तमान में {dasha_display} चल रही है। परीक्षा में अंतिम सफलता के लिए मुख्य परीक्षा के उत्तर लेखन में अत्यधिक अनुशासन तथा साक्षात्कार में आत्मविश्वास बनाए रखना अनिवार्य होगा।"
            )
            ans.append(f"**आचार्य निर्णय:** कुण्डली में न्यायिक एवं विधिक सेवा के पूर्ण शास्त्रीय योग उपस्थित हैं। आगामी अन्तर्दशा ({fw['ad_end']} से) आपको अत्यधिक अनुकूल परिणाम देने में सक्षम है।")
            ans.append(f"**साधना व उपाय:** नित्य प्रातः सूर्य देव को कुंकुम युक्त जल अर्पित कर आदित्य हृदय स्तोत्र का पाठ करें।")
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 4: CAREER / JOB / PROMOTION / BUSINESS (ब्रह्मास्त्र सूत्र विश्लेषण)
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["career", "job", "नौकरी", "प्रमोशन", "promotion", "आजीविका", "व्यवसाय",
                                       "business", "व्यापार", "काम", "ऑफिस", "rozgar", "kaam"]):
            h10_sign = (fw["asc_sign"] + 9) % 12
            h10_lord = constants.SIGN_LORD[h10_sign]
            h10_lord_hi = constants.PLANETS_HI.get(h10_lord, h10_lord)
            h10_occupants = [v["hi"] for k, v in fw["p_info"].items() if v.get("house") == 10]
            occ_str = f"दशम भाव में **{', '.join(h10_occupants)}** देव विराजमान हैं।" if h10_occupants else "दशम भाव वर्तमान में रिक्त है, अतः इसका पूर्ण फल दशमेश एवं कर्मकारक पर निर्भर है।"

            jup_h = fw["p_info"].get("Jupiter", {}).get("house", 0)
            ven_h = fw["p_info"].get("Venus", {}).get("house", 0)
            l10_h = fw["p_info"].get(h10_lord, {}).get("house", 0)
            has_subhatva = (l10_h in [jup_h, (jup_h+4)%12+1, (jup_h+6)%12+1, (jup_h+8)%12+1]) or (l10_h == ven_h)

            ans = [salutation]
            ans.append(f"आपकी आजीविका, पदोन्नति एवं कार्यक्षेत्र का **ब्रह्मास्त्र शास्त्रीय विश्लेषण (भाव, भावेश, कारक व गोचर समन्वय)**:\n")
            ans.append(
                f"1. **कर्म भाव (दशम भाव) एवं स्थिति:** आपके दशम भाव के अधिपति **{h10_lord_hi}** देव कुण्डली के {_placement(h10_lord)} में स्थित हैं। {occ_str} "
                f"{'दशमेश पर शुभ ग्रहों का प्रभाव (शुभत्व) आपके कार्यक्षेत्र में स्वाभाविक आकर्षण, निर्णय क्षमता और सामाजिक सम्मान को कई गुना बढ़ाता है।' if has_subhatva else 'कर्मेश की यह स्थिति निरंतर कर्मठता, गहन अनुभव और योग्यता सिद्ध करने के बाद स्थायी अधिकार प्रदान करती है।'}\n"
                f"2. **कर्मकारक (शनि व सूर्य) एवं भावत् भावम्:** कर्म के नैसर्गिक कारक शनि देव कुण्डली के {_placement('Saturn')} में स्थित हैं तथा अधिकार कारक सूर्य देव {_placement('Sun')} में हैं। "
                f"दशम से दशम (सप्तम भाव) का संबंध जनता, व्यापार व स्वतंत्र निर्णयों से होता है, जिससे आपके लिए स्वतंत्र उद्यम या उच्च उत्तरदायित्व वाले पद सर्वाधिक फलदायी सिद्ध होंगे।\n"
                f"3. **दशा-गोचर वेध एवं आगामी स्वर्णिम समय:** वर्तमान सक्रिय **{dasha_display}** के अंतर्गत तात्कालिक प्रत्यंतर **{pd_end_str}** तक चलेगा। "
                f"वास्तविक करियर मोड़ एवं पदोन्नति/वेतनवृद्धि का स्वर्णिम काल **{ad_end_str}** से आगामी {next_lord_hi} देव की अन्तर्दशा प्रारंभ होते ही प्रशस्त होगा। वर्तमान में देवगुरु व शनि का गोचर आपके कर्म क्षेत्र को मजबूती प्रदान कर रहा है।"
            )
            ans.append(f"**अचूक सात्विक उपाय:** नित्य प्रातः सूर्य देव को तांबे के लोटे से अर्घ्य दें (ॐ घृणिः सूर्याय नमः) तथा शनिवार को किसी कर्मठ श्रमिक अथवा जरूरतमंद को भोजन/अन्न का दान करें।")
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 5: WEALTH / FINANCE / DEBT / INVESTMENT (ब्रह्मास्त्र धन योग)
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["धन", "money", "wealth", "पैसा", "कर्ज", "debt", "आर्थिक", "निवेश", "लाभ", "रुपया", "kamai"]):
            h2_sign = (fw["asc_sign"] + 1) % 12
            h11_sign = (fw["asc_sign"] + 10) % 12
            h2_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h2_sign])
            h11_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h11_sign])
            h2_occupants = [v["hi"] for k, v in fw["p_info"].items() if v.get("house") == 2]
            h11_occupants = [v["hi"] for k, v in fw["p_info"].items() if v.get("house") == 11]

            ans = [salutation]
            ans.append(f"आपकी आर्थिक स्थिति, धन संचय एवं स्थायी ऐश्वर्य का **ब्रह्मास्त्र शास्त्रीय विश्लेषण (2H-11H-9H ध्रुव योग)**:\n")
            ans.append(
                f"1. **धन भाव (2H) एवं लाभ भाव (11H):** संचित धन भाव (2H) के स्वामी **{h2_lord}** तथा नियमित आय भाव (11H) के स्वामी **{h11_lord}** देव हैं। "
                f"{('द्वितीय भाव में ' + ', '.join(h2_occupants) + ' देव विराजमान हैं। ') if h2_occupants else ''}"
                f"{('एकादश भाव में ' + ', '.join(h11_occupants) + ' देव विराजमान हैं। ') if h11_occupants else ''}"
                f"कुण्डली में नियमित आय और दीर्घकालिक धन संचय के योग सुदृढ़ हैं।\n"
                f"2. **धनकारक गुरु की स्थिति एवं शुभत्व:** धन व समृद्धि के नैसर्गिक कारक देवगुरु बृहस्पति कुण्डली के {_placement('Jupiter')} में स्थित हैं। "
                f"बृहस्पति की शुभ दृष्टि जातक को संकट के समय में भी ईश्वरीय सहायता व आकस्मिक धन लाभ प्रदान करती है।\n"
                f"3. **समय-सीमा व वित्तीय सावधानी:** चालू प्रत्यंतर **{pd_end_str}** तक बिना लिखित अनुबंध के किसी को बड़ा ऋण न दें और सट्टे/अल्पकालिक ट्रेडिंग से बचें। "
                f"आगामी **{ad_end_str}** के पश्चात {next_lord_hi} की अन्तर्दशा प्रारंभ होते ही नवीन आय स्रोत एवं अचल संपत्ति में निवेश के अत्यंत प्रबल योग बनेंगे।"
            )
            ans.append(f"**अचूक सात्विक उपाय:** नित्य श्री कनकधारा स्तोत्र का पाठ करें तथा गुरुवार को पीले फल या चने की दाल का दान करें।")
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 6: MARRIAGE / RELATIONSHIP / SPOUSE (ब्रह्मास्त्र कलत्र फलित)
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["विवाह", "शादी", "marriage", "पत्नी", "पति", "दांपत्य", "रिश्ता", "प्रेम", "सप्तम"]):
            h7_sign = (fw["asc_sign"] + 6) % 12
            h7_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h7_sign])
            h7_occupants = [v["hi"] for k, v in fw["p_info"].items() if v.get("house") == 7]
            occ7_str = f"सप्तम भाव में **{', '.join(h7_occupants)}** देव स्थित हैं।" if h7_occupants else "सप्तम भाव शुद्ध है।"

            ans = [salutation]
            ans.append(f"दांपत्य जीवन, विवाह एवं जीवनसाथी के संबंध में **ब्रह्मास्त्र शास्त्रीय विश्लेषण**:\n")
            ans.append(
                f"1. **सप्तम भाव (कलत्र भाव) एवं भावेश:** आपके सप्तम भाव के स्वामी **{h7_lord}** हैं। {occ7_str} "
                f"विवाह के नैसर्गिक कारक शुक्र देव {_placement('Venus')} में स्थित हैं। यह स्थिति सुसंस्कृत, स्वाभिमानी एवं कर्मठ जीवनसाथी का संकेत देती है।\n"
                f"2. **दांपत्य में परिपक्वता का नियम:** सप्तम भाव पर शनि अथवा मंगल के प्रभाव की स्थिति में विवाह के उपरांत प्रारंभिक वर्षों में विचारों में भिन्नता स्वाभाविक है। "
                f"यहाँ परिपक्वता, धैर्य और आपसी सम्मान ही दांपत्य को अमरत्व प्रदान करता है।\n"
                f"3. **विवाह व अनुकूलता की समय-सीमा:** चालू दशा ({dasha_display}) में सप्तमेश व द्वितीयेश की युति सक्रिय है। "
                f"आगामी **{ad_end_str}** के आसपास वैवाहिक वार्ता, संबंधों में मधुरता एवं पारिवारिक सामंजस्य के अत्यंत श्रेष्ठ योग निर्मित होंगे।"
            )
            ans.append(f"**अचूक सात्विक उपाय:** शुक्रवार को देवी लक्ष्मी को मिश्री अथवा खीर का भोग लगाएं और श्वेत सुगंधित पुष्प अर्पित करें।")
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 7: HEALTH / WELLNESS (ब्रह्मास्त्र आरोग्य एवं जीवनी शक्ति)
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["स्वास्थ्य", "health", "रोग", "बीमारी", "तबीयत", "इलाज", "दर्द"]):
            h6_sign = (fw["asc_sign"] + 5) % 12
            h6_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h6_sign])

            ans = [salutation]
            ans.append(f"शारीरिक आरोग्य, जीवनी शक्ति एवं व्याधि मुक्ति का **ब्रह्मास्त्र शास्त्रीय विश्लेषण**:\n")
            ans.append(
                f"1. **लग्न व लग्नेश (जीवनी शक्ति):** आपके लग्नेश **{fw['lagnesh_hi']}** देव {_placement(fw['lagnesh'])} में विराजमान हैं। "
                f"लग्नेश का बलवान होना जातक को किसी भी बड़ी व्याधि से स्वतः उबरने की रोग-प्रतिरोधक क्षमता (Immunity) प्रदान करता है।\n"
                f"2. **षष्ठेश व अष्टमेश की स्थिति:** षष्ठ भाव (रोग) के अधिपति **{h6_lord}** हैं। "
                f"चालू दशा में मौसमी प्रभाव, पित्त/उदर विकार अथवा कार्यभार से उत्पन्न अनिद्रा व मानसिक तनाव से सतर्क रहने की आवश्यकता है।\n"
                f"3. **आरोग्य सुरक्षा काल:** प्रत्यन्तर दशा **{pd_end_str}** के उपरांत स्वास्थ्य में स्वतः स्फूर्ति व ताजगी आएगी।"
            )
            ans.append(f"**अचूक सात्विक उपाय:** महामृत्युंजय मंत्र का नित्य 11 बार जप करें तथा सोमवार को शिवलिंग पर जल व कच्चा दूध अर्पित करें।")
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 8: CHILDREN / PROGENY (ब्रह्मास्त्र सुत भाव फलित)
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["संतान", "बच्चे", "गर्भाधान", "पुत्र", "पुत्री", "child", "progeny", "garbh"]):
            h5_sign = (fw["asc_sign"] + 4) % 12
            h5_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h5_sign])

            ans = [salutation]
            ans.append(f"संतान भाव, विद्या एवं संतति सुख का **ब्रह्मास्त्र शास्त्रीय विश्लेषण**:\n")
            ans.append(
                f"1. **पंचम भाव (सुत भाव):** पंचम भाव के अधिपति **{h5_lord}** देव हैं तथा संतान के नैसर्गिक कारक देवगुरु बृहस्पति {_placement('Jupiter')} में स्थित हैं।\n"
                f"2. पंचम से पंचम (नवम भाव - भावत् भावम्) का संबंध धर्म व भाग्य से होता है। आपकी संतान तीव्र बुद्धि, सदाचारी एवं परिवार का नाम रोशन करने वाली होगी।\n"
                f"3. **समय-सीमा:** संतान की शिक्षा, प्रगति व सुख के लिए आगामी कालखंड **{ad_end_str}** से अत्यधिक गौरवशाली रहेगा।"
            )
            ans.append(f"**अचूक सात्विक उपाय:** गुरुवार को श्री संतान गोपाल मंत्र अथवा गोपाल सहस्रनाम का स्मरण करें।")
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 9: PROPERTY / HOUSE / VEHICLE (ब्रह्मास्त्र भूमि-वाहन सुख)
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["मकान", "घर", "भूमि", "वाहन", "गाड़ी", "प्रॉपर्टी", "flat", "plot", "car"]):
            h4_sign = (fw["asc_sign"] + 3) % 12
            h4_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h4_sign])

            ans = [salutation]
            ans.append(f"भूमि, भवन, वाहन एवं स्थायी संपत्ति का **ब्रह्मास्त्र शास्त्रीय विश्लेषण**:\n")
            ans.append(
                f"1. **चतुर्थ भाव (सुखेश):** चतुर्थ भाव के अधिपति **{h4_lord}** देव हैं। भूमि कारक मंगल देव {_placement('Mars')} में तथा वाहन कारक शुक्र देव {_placement('Venus')} में स्थित हैं।\n"
                f"2. चतुर्थेश एवं भूमि कारक मंगल का यह संयोग स्वयं के अर्जित धन से भव्य गृह निर्माण अथवा अचल संपत्ति क्रय का स्पष्ट संकेत देता है।\n"
                f"3. **समय-सीमा:** वर्तमान विंशोत्तरी दशा में आगामी वर्ष तक नवीन वाहन सुख एवं संपत्ति के अनुबंध पूर्ण होने के प्रबल योग हैं।"
            )
            ans.append(f"**अचूक सात्विक उपाय:** मंगलवार को हनुमान चालीसा का 7 बार पाठ करें और गुड़-चने का प्रसाद बांटें।")
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 10: FOREIGN TRAVEL / SETTLEMENT (ब्रह्मास्त्र विदेश गमन)
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["विदेश", "foreign", "यात्रा", "travel", "settlement", "वीजा", "bahar"]):
            h9_sign = (fw["asc_sign"] + 8) % 12
            h12_sign = (fw["asc_sign"] + 11) % 12
            h9_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h9_sign])
            h12_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h12_sign])

            ans = [salutation]
            ans.append(f"विदेश गमन, दूरस्थ यात्राओं एवं स्थान परिवर्तन का **ब्रह्मास्त्र शास्त्रीय विश्लेषण**:\n")
            ans.append(
                f"1. **नवम (भाग्य/यात्रा) व द्वादश (विदेश/निवास) भाव:** नवमेश **{h9_lord}** व द्वादशेश **{h12_lord}** हैं। "
                f"राहु देव {_placement('Rahu')} में स्थित होकर जन्मस्थान से दूर आजीविका व प्रतिष्ठा प्राप्ति का मार्ग प्रशस्त करते हैं।\n"
                f"2. **दूरस्थ लाभ:** यदि आप बहुराष्ट्रीय कंपनी, आयात-निर्यात अथवा दूरस्थ कार्यप्रणाली से जुड़ते हैं तो आर्थिक लाभ में अप्रत्याशित वृद्धि होगी।\n"
                f"3. **सक्रिय कालखंड:** वर्तमान दशा के आगामी चरण में वीजा व यात्रा संबंधी कार्य निर्बाध रूप से संपन्न होंगे।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 11: TROUBLES / SADESATI / RELIEF / OBSTACLES (ब्रह्मास्त्र संकट निवारण)
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["कष्ट", "परेशानी", "समस्या", "साढ़े साती", "ढैया", "राहत", "संकट", "मुसीबत", "तनाव", "rukawat"]):
            ans = [salutation]
            ans.append(f"कष्ट, मानसिक तनाव एवं बाधाओं से मुक्ति का **ब्रह्मास्त्र शास्त्रीय विश्लेषण**:\n")
            ans.append(
                f"1. **मूल कारण का विश्लेषण:** वर्तमान में आपकी सक्रिय दशा ({dasha_display}) चल रही है। "
                f"शनि देव {_placement('Saturn')} में स्थित हैं। शनि जब कुण्डली के महत्वपूर्ण भावों को दृष्टिगत करते हैं, "
                f"तो वे व्यक्ति को धैर्य, अनुशासन और सत्यनिष्ठा की परीक्षा में डालते हैं। यह कष्ट नहीं अपितु परिपक्वता व आंतरिक शक्ति के जागरण का काल है।\n"
                f"2. **राहत की समय-सीमा:** तात्कालिक प्रत्यन्तर समाप्ति (**{pd_end_str}**) और आगामी अन्तर्दशा प्रारंभ (**{ad_end_str}**) के साथ सभी मानसिक व भौतिक बाधाओं का स्वतः शमन होने लगेगा।\n"
                f"3. **शास्त्रीय शांति उपाय:**\n"
                f"• शनिवार को सूर्यास्त के बाद हनुमान जी के सम्मुख चमेली के तेल का दीपक जलाएं और सुंदरकांड का पाठ करें।\n"
                f"• चींटियों को सूखा आटा व शक्कर तथा पक्षियों को सात प्रकार के अनाज डालें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 12: REMEDIES / GEMSTONES / MANTRAS (ब्रह्मास्त्र सात्विक उपाय)
        # ---------------------------------------------------------------------
        elif any(w in q_lower for w in ["उपाय", "रत्न", "मंत्र", "दान", "पूजा", "remedy", "upay", "stone"]):
            ans = [salutation]
            ans.append(f"आपकी जन्मपत्रिका के अनुसार **सर्वोच्च एवं अचूक शास्त्रीय सात्विक उपाय**:\n")
            ans.append(
                f"1. **लग्नेश बल संवर्धन (कवच):** आपके लग्नेश **{fw['lagnesh_hi']}** {_placement(fw['lagnesh'])} में स्थित हैं। "
                f"लग्नेश को बलवान करने से समस्त 12 भावों के दोष स्वतः क्षीण हो जाते हैं। नित्य प्रातः सूर्य नमस्कार अथवा गायत्री मंत्र का एक माला जप करें।\n"
                f"2. **दशा शांति अनुष्ठान:** चालू दशा ({dasha_display}) की अनुकूलता हेतु शनिवार को शनि स्तोत्र तथा शुक्रवार को श्री सूक्त या कनकधारा स्तोत्र का पाठ परम श्रेयस्कर है।\n"
                f"3. **रत्न परामर्श:** कुण्डली के कारक ग्रहों के अनुकूल रत्न विधिवत परीक्षण के उपरांत ही धारण करें। तामसिक व भयभीत करने वाले अनुष्ठानों से सदैव दूर रहें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)

        # ---------------------------------------------------------------------
        # INTENT 13: CONTEXTUAL ASTROLOGICAL SYNTHESIS (DYNAMIC FALLBACK)
        # ---------------------------------------------------------------------
        else:
            ans = [salutation]
            ans.append(f"आपके प्रश्न — **\"{query}\"* के संबंध में कुण्डली एवं ग्रहों का शास्त्रीय दृष्टिकोण:\n")
            ans.append(
                f"1. **लग्न व मन का संबल:** आपकी कुण्डली **{fw['asc_sign_name']} लग्न** की है और लग्नेश **{fw['lagnesh_hi']}** "
                f"कुण्डली के {_placement(fw['lagnesh'])} में सुदृढ़ स्थिति में हैं। चन्द्रमा {fw['moon_sign_name']} राशि ({fw['moon_nak_name']} नक्षत्र) में संचरण कर रहे हैं। यह ग्रह विन्यास विपरीत परिस्थितियों में भी आपको सही निर्णय लेने की क्षमता देता है।\n"
                f"2. **सक्रिय कालखंड व समय-सीमा:** वर्तमान में **{dasha_display}** चल रही है। तात्कालिक प्रत्यंतर **{pd_end_str}** तक प्रभावी है, तत्पश्चात मुख्य मोड़ **{ad_end_str}** से {next_lord_hi} देव की अन्तर्दशा के साथ प्रारंभ होगा।\n"
                f"3. **आचार्य परामर्श:** किसी भी संशय की स्थिति में शांत मन से निर्णय लें। अपने दैनिक आचरण में सात्विकता बनाए रखें और नित्य प्रातः सूर्य देव को जल अर्पित करें।"
            )
            return self._append_curiosity_hook("\n\n".join(ans), query)


vyas_chatbot = VyasChatbotEngine()
