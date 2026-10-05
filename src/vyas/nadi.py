"""Bhrigu Nandi Nadi (BNN) & Chandra Kala Nadi Astrology Engine.

Core Nadi Tenets:
1. Directional Conjunctions (Dik-Sambandha):
   - East (Fire: Aries, Leo, Sagittarius)
   - South (Earth: Taurus, Virgo, Capricorn)
   - West (Air: Gemini, Libra, Aquarius)
   - North (Water: Cancer, Scorpio, Pisces)
   Planets in the same directional trine (1-5-9) act conjunct and intertwine their energies.

2. Positional Sequence:
   - 2nd from planet: Future development / Resource feeding the planet.
   - 12th from planet: Past karma / Roots / Drag on the planet.
   - 7th from planet: Direct counter-force / Partnership.

3. Planetary Roles (Karakattvas):
   - Jupiter (Jiva - The Self, Wisdom, Vitality)
   - Saturn (Karma - Profession, Labor, Destiny)
   - Venus (Lakshmi - Wealth, Spouse in male chart, Vehicles)
   - Mars (Shakti - Brother, Husband in female chart, Energy)
   - Mercury (Buddhi - Intelligence, Trade, Education, Property)
   - Sun (Atma - Father, Government, Status)
   - Moon (Manas - Mother, Change, Motion, Liquids)
   - Rahu (Maya - Foreign, Ambition, Paternal grandfather, Illusion)
   - Ketu (Moksha - Spirituality, Law, De-attachment, Maternal grandfather)

4. Classical Nadi Planetary Combinations & Inferences.
"""
from typing import Dict, List, Tuple, NamedTuple

DIRECTIONS = {
    "East (Fire / Dharma)": [0, 4, 8],     # Aries, Leo, Sagittarius
    "South (Earth / Artha)": [1, 5, 9],    # Taurus, Virgo, Capricorn
    "West (Air / Kama)": [2, 6, 10],       # Gemini, Libra, Aquarius
    "North (Water / Moksha)": [3, 7, 11]   # Cancer, Scorpio, Pisces
}

SIGN_TO_DIRECTION = {}
for d_name, signs in DIRECTIONS.items():
    for s in signs:
        SIGN_TO_DIRECTION[s] = d_name

class NadiCombination(NamedTuple):
    title: str
    planets_involved: List[str]
    relationship: str    # Trinal (Same Direction), 2nd/12th, 7th Opposition
    classical_sutra: str
    life_impact: str
    auspiciousness: str

def analyze_bhrigu_nandi_nadi(planet_signs: Dict[str, any]) -> Dict[str, any]:
    """
    Analyzes chart according to classical Bhrigu Nandi Nadi principles.
    planet_signs: Dict mapping planet name to sign index (0-11) or PlanetState.
    """
    clean_signs: Dict[str, int] = {}
    for p_name, val in planet_signs.items():
        if hasattr(val, 'sign'):
            clean_signs[p_name] = int(val.sign)
        elif hasattr(val, 'longitude'):
            clean_signs[p_name] = int(val.longitude // 30) % 12
        elif isinstance(val, (int, float)):
            clean_signs[p_name] = int(val) % 12

    # 1. Group planets by Directional Trine
    dir_planets: Dict[str, List[str]] = {d: [] for d in DIRECTIONS}
    for p_name, s_idx in clean_signs.items():
        d_name = SIGN_TO_DIRECTION.get(s_idx, "East (Fire / Dharma)")
        dir_planets[d_name].append(p_name)
        
    combinations: List[NadiCombination] = []
    
    # 2. Check Trinal Combinations (Same Direction)
    for d_name, p_list in dir_planets.items():
        if len(p_list) >= 2:
            p_set = set(p_list)
            
            # Guru + Shani (Dharma-Karma Yoga)
            if "Jupiter" in p_set and "Saturn" in p_set:
                combinations.append(NadiCombination(
                    title="Dharma-Karmadhipati Nadi Yoga (Guru + Shani)",
                    planets_involved=["Jupiter", "Saturn"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="जीवार्कजौ समायोगे कर्मधर्मप्रवर्तकः (Jiva and Shani combined direct high karma and ethical profession)",
                    life_impact="The native achieves dignity in profession, holds advising or authoritative responsibility, and performs honorable service.",
                    auspiciousness="Highly Auspicious"
                ))
                
            # Guru + Shukra (Bhrigu Rishi Yoga)
            if "Jupiter" in p_set and "Venus" in p_set:
                combinations.append(NadiCombination(
                    title="Bhrigu-Brihaspati Yoga (Guru + Shukra)",
                    planets_involved=["Jupiter", "Venus"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="गुरुशुक्रसमायोगे विद्याधनसुखावहः (Union of two preceptors grants elite wisdom and affluence)",
                    life_impact="Conferment of high intellectual refinement, refined speech, luxury vehicles, and prosperous family lineage.",
                    auspiciousness="Extremely Auspicious"
                ))
                
            # Guru + Rahu (Guru-Chandal Nadi Yoga)
            if "Jupiter" in p_set and "Rahu" in p_set:
                combinations.append(NadiCombination(
                    title="Guru-Chandal Nadi Yoga (Guru + Rahu)",
                    planets_involved=["Jupiter", "Rahu"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="जीवे राहुसमायुक्ते विजातीयविचारकः (Jiva afflicted by Rahu seeks unconventional or foreign domains)",
                    life_impact="Unconventional philosophical perspective, attraction to esoteric or foreign methodologies, potential respiratory/liver sensitivity.",
                    auspiciousness="Mixed / Transformational"
                ))
                
            # Guru + Ketu (Moksha & Gnanakaraka Yoga)
            if "Jupiter" in p_set and "Ketu" in p_set:
                combinations.append(NadiCombination(
                    title="Jnana-Moksha Nadi Yoga (Guru + Ketu)",
                    planets_involved=["Jupiter", "Ketu"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="जीवकेत्वोस्तु संयोगे मुक्तिमार्गरतः सदा (Jiva with Ketu walks the path of inner liberation and discernment)",
                    life_impact="Profound spiritual detachment, mastery in occult, astrology, law, or traditional medicine; philanthropic mindset.",
                    auspiciousness="Spiritually Auspicious"
                ))
                
            # Shani + Rahu (Shani-Rahu Karmic Knot)
            if "Saturn" in p_set and "Rahu" in p_set:
                combinations.append(NadiCombination(
                    title="Karmic Knot Yoga (Shani + Rahu)",
                    planets_involved=["Saturn", "Rahu"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="शनिमन्दे राहुयोगे कर्मविघ्नं मुहुर्मुहुः (Saturn with Rahu presents complex professional karmas)",
                    life_impact="Career path encounters sudden shifts, foreign employment, technical or hazardous domains, requiring diligent patience.",
                    auspiciousness="Challenging / Hard Labor"
                ))
                
            # Budha + Shukra (Kalanidhi & Commercial Acumen)
            if "Mercury" in p_set and "Venus" in p_set:
                combinations.append(NadiCombination(
                    title="Kalanidhi Vanijya Yoga (Budha + Shukra)",
                    planets_involved=["Mercury", "Venus"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="बुधशुक्रसमायोगे व्यापारकौशले युतः (Mercury and Venus endow exceptional commercial and artistic talents)",
                    life_impact="Elite analytical eloquence, mastery in trade, accounts, literature, aesthetics, and wealth creation.",
                    auspiciousness="Highly Auspicious"
                ))

            # Mangala + Shukra (Bhoga & Passion)
            if "Mars" in p_set and "Venus" in p_set:
                combinations.append(NadiCombination(
                    title="Bhauma-Bhargava Yoga (Mangala + Shukra)",
                    planets_involved=["Mars", "Venus"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="भौमशुक्रसमायोगे भोगभाग्यसमन्वितः (Mars and Venus trigger energetic romantic and real-estate pursuits)",
                    life_impact="Magnetic charm, acquisition of immovable properties and vehicles, dynamic romantic relationships.",
                    auspiciousness="Auspicious / Passionate"
                ))

    # 3. Positional Flow for Jiva (Jupiter) and Karma (Saturn)
    jup_sign = clean_signs.get("Jupiter", 0)
    sat_sign = clean_signs.get("Saturn", 0)
    
    def get_forward_backward(sign):
        fwd_sign = (sign + 1) % 12
        bwd_sign = (sign - 1) % 12
        fwd_planets = [p for p, s in clean_signs.items() if s == fwd_sign]
        bwd_planets = [p for p, s in clean_signs.items() if s == bwd_sign]
        return fwd_planets, bwd_planets

    jup_fwd, jup_bwd = get_forward_backward(jup_sign)
    sat_fwd, sat_bwd = get_forward_backward(sat_sign)

    flow_insights = {
        "Jiva_Future_Feed": f"Planets 2nd to Jupiter: {jup_fwd if jup_fwd else 'None (Clean path ahead)'}",
        "Jiva_Past_Root": f"Planets 12th to Jupiter: {jup_bwd if jup_bwd else 'None (Free from past drag)'}",
        "Karma_Future_Feed": f"Planets 2nd to Saturn: {sat_fwd if sat_fwd else 'None (Open field in career)'}",
        "Karma_Past_Root": f"Planets 12th to Saturn: {sat_bwd if sat_bwd else 'None (Independent karma)'}"
    }

    return {
        "directional_groups": dir_planets,
        "nadi_combinations": combinations,
        "flow_insights": flow_insights
    }


def analyze_nadi_combinations(planets) -> Dict[str, any]:
    """Analyzes chart according to classical Bhrigu Nandi Nadi principles.
    planets: Dict mapping planet name to PlanetState or sign index.
    """
    res = analyze_bhrigu_nandi_nadi(planets)
    combs = []
    for c in res.get("nadi_combinations", []):
        combs.append({
            "name": c.title,
            "result": f"<b>{c.relationship}</b> ({c.auspiciousness})<br>{c.classical_sutra}<br><br>{c.life_impact}"
        })
    if not combs:
        for d_name, p_list in res.get("directional_groups", {}).items():
            if len(p_list) >= 2:
                combs.append({
                    "name": f"दिशीय सम्बन्धी युति ({d_name})",
                    "result": f"ग्रह: {', '.join(p_list)} एक ही दिशा त्रिकोण में परस्पर ऊर्जा विनिमय कर रहे हैं।"
                })
    return {"combinations": combs, "raw": res}
