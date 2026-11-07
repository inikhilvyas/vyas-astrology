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
from typing import Dict, List, Tuple, NamedTuple, Optional
from datetime import datetime, timezone
from vyas import constants

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

            # Surya + Budha (Nipuna / Budhaditya Nadi)
            if "Sun" in p_set and "Mercury" in p_set:
                combinations.append(NadiCombination(
                    title="Budhaditya Nipuna Nadi Yoga (Surya + Budha)",
                    planets_involved=["Sun", "Mercury"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="रविबुधसमायोगे तीव्रबुद्धिर्महामनाः (Sun and Mercury bestow exceptional intellect and government/administrative renown)",
                    life_impact="Analytical sharpness, high administrative recognition, legal/commercial eloquence, and academic honor.",
                    auspiciousness="Highly Auspicious"
                ))

            # Chandra + Guru (Gajakesari Nadi)
            if "Moon" in p_set and "Jupiter" in p_set:
                combinations.append(NadiCombination(
                    title="Chandra-Guru Nadi Yoga (Gajakesari)",
                    planets_involved=["Moon", "Jupiter"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="गुरुशशाङ्कसंयोगे कीर्तिमान् लोकपूजितः (Moon and Jupiter bestow public reverence, mental peace, and noble lineage)",
                    life_impact="Unshakeable reputation, empathetic leadership, abundance of domestic comforts, and respected advisory role.",
                    auspiciousness="Supreme Auspicious"
                ))

            # Shani + Mangala (Yama / Technical Karma)
            if "Saturn" in p_set and "Mars" in p_set:
                combinations.append(NadiCombination(
                    title="Shani-Bhauma Nadi Yoga (Technical / Mechanical Karma)",
                    planets_involved=["Saturn", "Mars"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="शनिकुजसमायोगे यन्त्रकर्मप्रवर्तकः (Saturn and Mars align work with machinery, engineering, and dynamic enterprise)",
                    life_impact="Success in engineering, manufacturing, construction, technical surgery, or defensive industries; demands anger management.",
                    auspiciousness="Dynamic / Demanding"
                ))

            # Shani + Budha (Vanik & Analytical Karma)
            if "Saturn" in p_set and "Mercury" in p_set:
                combinations.append(NadiCombination(
                    title="Shani-Budha Nadi Yoga (Commercial & Intellectual Karma)",
                    planets_involved=["Saturn", "Mercury"],
                    relationship=f"Trinal Conjunction ({d_name})",
                    classical_sutra="शनिबुधसमायोगे लेखको वाणिज्यतत्परः (Saturn and Mercury channel career into writing, software, commerce, and accounting)",
                    life_impact="Long-term mastery in documentation, business management, IT/data systems, trade contracts, and strategic planning.",
                    auspiciousness="Very Auspicious"
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


def compute_bnn_karaka_synthesis(planets) -> Dict[str, str]:
    """
    Computes 100% dynamic, authentic Bhrigu Nandi Nadi (BNN) qualitative predictions:
    - Jeeva Karaka (Jupiter) Life Path & Soul Guidance
    - Karma Karaka (Saturn) Professional Destiny
    - Dhana Karaka (Venus & Mercury) Material Opulence
    - Directional Trine Balance (Dharma, Artha, Kama, Moksha)
    """
    clean_signs: Dict[str, int] = {}
    for p_name, val in planets.items():
        if hasattr(val, 'sign_index'):
            clean_signs[p_name] = int(val.sign_index) % 12
        elif hasattr(val, 'sign'):
            clean_signs[p_name] = int(val.sign) % 12
        elif hasattr(val, 'longitude'):
            clean_signs[p_name] = int(val.longitude // 30) % 12
        elif isinstance(val, (int, float)):
            clean_signs[p_name] = int(val) % 12

    jup_sign = clean_signs.get("Jupiter", 0)
    sat_sign = clean_signs.get("Saturn", 0)
    ven_sign = clean_signs.get("Venus", 0)
    merc_sign = clean_signs.get("Mercury", 0)

    # 1. Jeeva Karaka (Jupiter)
    jup_dir = SIGN_TO_DIRECTION.get(jup_sign, "East (Fire / Dharma)")
    trine_to_jup = [p for p, s in clean_signs.items() if p != "Jupiter" and (s - jup_sign) % 4 == 0]
    feed_to_jup = [p for p, s in clean_signs.items() if s == (jup_sign + 1) % 12]
    drag_to_jup = [p for p, s in clean_signs.items() if s == (jup_sign - 1) % 12]
    opp_to_jup = [p for p, s in clean_signs.items() if s == (jup_sign + 6) % 12]

    trine_hi = ", ".join([constants.PLANETS_HI.get(p, p) for p in trine_to_jup]) if trine_to_jup else "कोई नहीं"
    feed_hi = ", ".join([constants.PLANETS_HI.get(p, p) for p in feed_to_jup]) if feed_to_jup else "मार्ग निष्कंटक है"
    drag_hi = ", ".join([constants.PLANETS_HI.get(p, p) for p in drag_to_jup]) if drag_to_jup else "पूर्व ऋणों से मुक्त"

    jup_sign_hi = constants.SIGNS_HI[jup_sign] if jup_sign < len(constants.SIGNS_HI) else str(jup_sign)
    jeeva_text = (
        f"भृगु नन्दी नाड़ी में देवगुरु बृहस्पति को <b>'जीव कारक' (Jeeva Karaka)</b> माना गया है, जो जातक की चेतना व जीवन-शक्ति का प्रतीक है। "
        f"आपकी कुण्डली में जीव कारक गुरु <b>{jup_sign_hi} राशि</b> ({jup_dir}) में अवस्थित हैं। "
    )
    if trine_to_jup:
        jeeva_text += f"गुरु के साथ दिशीय त्रिकोण में <b>{trine_hi}</b> की युति ऊर्जा का आदान-प्रदान कर रही है, जिससे जातक का व्यक्तित्व बहुमुखी ज्ञान, दूरदर्शिता व स्वाभिमान से युक्त होता है। "
    else:
        jeeva_text += "गुरु स्वतंत्र त्रिकोण में होने से जातक अपनी मौलिक विचारधारा व आत्मबल पर अग्रसर होता है। "

    jeeva_text += (
        f"गुरु से द्वितीय भाव (भावी संसाधन) में {feed_hi} स्थित होने से जीवन में संसाधनों का प्रवाह बना रहता है, "
        f"तथा द्वादश भाव (पूर्व जन्म संस्कार) में {drag_hi} का प्रभाव जातक की आध्यात्मिक चेतना को जागृत रखता है।"
    )

    # 2. Karma Karaka (Saturn)
    sat_dir = SIGN_TO_DIRECTION.get(sat_sign, "West (Air / Kama)")
    trine_to_sat = [p for p, s in clean_signs.items() if p != "Saturn" and (s - sat_sign) % 4 == 0]
    feed_to_sat = [p for p, s in clean_signs.items() if s == (sat_sign + 1) % 12]
    drag_to_sat = [p for p, s in clean_signs.items() if s == (sat_sign - 1) % 12]

    sat_trine_hi = ", ".join([constants.PLANETS_HI.get(p, p) for p in trine_to_sat]) if trine_to_sat else "स्वतंत्र कर्म"
    sat_sign_hi = constants.SIGNS_HI[sat_sign] if sat_sign < len(constants.SIGNS_HI) else str(sat_sign)

    karma_text = (
        f"नाड़ी दर्शन में शनिदेव को <b>'कर्म कारक' (Karma Karaka)</b> कहा गया है, जो जातक की आजीविका, सामाजिक दायित्व व पुरुषार्थ के नियंता हैं। "
        f"आपकी कुण्डली में कर्म कारक शनि <b>{sat_sign_hi} राशि</b> ({sat_dir}) में प्रतिष्ठित हैं। "
    )
    if "Sun" in trine_to_sat:
        karma_text += "सूर्य के साथ दिशीय संबंध से शासन, सरकारी तंत्र, प्रशासनिक प्रतिष्ठा अथवा सत्ताधारी प्रतिष्ठानों से आजीविका का योग बनता है। "
    if "Mercury" in trine_to_sat:
        karma_text += "बुध के साथ त्रिकोण संबंध से वाणिज्य, सॉफ्टवेयर कोडिंग, लेखन, प्रकाशन, अनुसंधान एवं ज्योतिषीय विश्लेषण में असाधारण निपुणता मिलती है। "
    if "Jupiter" in trine_to_sat:
        karma_text += "गुरु के साथ योग (धर्म-कर्माधिपति नाड़ी योग) जातक को समाज में सलाहकार, शिक्षक अथवा सम्मानित मार्गदर्शक का शीर्ष स्थान दिलाता है। "
    if "Venus" in trine_to_sat:
        karma_text += "शुक्र के साथ संयोग से वित्तीय प्रबंधन, कला, विलासिता, वाहन अथवा बड़े व्यापारिक संस्थानों में दीर्घकालिक स्थायित्व प्राप्त होता है। "
    if "Mars" in trine_to_sat:
        karma_text += "मंगल के साथ संबंध से तकनीकी, इंजीनियरिंग, विनिर्माण अथवा रक्षा/भूमि संबंधी परियोजनाओं में पुरुषार्थ सिद्ध होता है। "
    if "Rahu" in trine_to_sat:
        karma_text += "राहु के साथ संयोग से विदेशी कंपनियों, नवीन तकनीकों व अप्रत्याशित व्यावसायिक विस्तार के द्वार खुलते हैं। "
    if "Ketu" in trine_to_sat:
        karma_text += "केतु के साथ संबंध से विधि, न्यायशास्त्र, आध्यात्मिक परामर्श अथवा गूढ़ दर्शन के क्षेत्र में जातक का यश फैलता है। "

    karma_text += f"शनि से 1-5-9 त्रिकोण में सम्बद्ध ग्रह ({sat_trine_hi}) यह स्पष्ट करते हैं कि निरंतर परिश्रम के उपरांत जातक का कार्यक्षेत्र में पूर्ण वर्चस्व स्थापित होगा।"

    # 3. Dhana & Vidya Karakas (Venus & Mercury)
    ven_sign_hi = constants.SIGNS_HI[ven_sign] if ven_sign < len(constants.SIGNS_HI) else str(ven_sign)
    merc_sign_hi = constants.SIGNS_HI[merc_sign] if merc_sign < len(constants.SIGNS_HI) else str(merc_sign)
    dhana_text = (
        f"नाड़ी में शुक्र <b>'लक्ष्मी/धन कारक'</b> तथा बुध <b>'व्यापार व बुद्धि कारक'</b> हैं। "
        f"शुक्र {ven_sign_hi} राशि में एवं बुध {merc_sign_hi} राशि में स्थित होकर धनार्जन के निरंतर स्रोत निर्मित करते हैं। "
        f"जातक का बौद्धिक पराक्रम ही उसकी स्थायी सम्पत्ति व यश का मूल आधार बनता है।"
    )

    # 4. Directional Trines (दिशीय संयोजन)
    dir_counts: Dict[str, List[str]] = {d: [] for d in DIRECTIONS}
    for p_name, s_idx in clean_signs.items():
        d_name = SIGN_TO_DIRECTION.get(s_idx, "East (Fire / Dharma)")
        dir_counts[d_name].append(constants.PLANETS_HI.get(p_name, p_name))

    trines_text = (
        f"नाड़ी चतुर्विध पुरुषार्थ संयोजन:\n"
        f"• <b>पूर्व दिशा (धर्म त्रिकोण):</b> {', '.join(dir_counts['East (Fire / Dharma)']) or 'रिक्त'}\n"
        f"• <b>दक्षिण दिशा (अर्थ त्रिकोण):</b> {', '.join(dir_counts['South (Earth / Artha)']) or 'रिक्त'}\n"
        f"• <b>पश्चिम दिशा (काम त्रिकोण):</b> {', '.join(dir_counts['West (Air / Kama)']) or 'रिक्त'}\n"
        f"• <b>उत्तर दिशा (मोक्ष त्रिकोण):</b> {', '.join(dir_counts['North (Water / Moksha)']) or 'रिक्त'}\n"
        f"जिस दिशा में सर्वाधिक शुभ ग्रहों का समूह होता है, जातक का जीवन उसी पुरुषार्थ की सिद्धि में केंद्रित रहता है।"
    )

    return {
        "jeeva_karaka_hi": jeeva_text,
        "karma_karaka_hi": karma_text,
        "dhana_karaka_hi": dhana_text,
        "directional_trines_hi": trines_text
    }


def compute_bhrigu_progression(
    jupiter_sign: int,
    birth_date: datetime,
    current_date: Optional[datetime] = None
) -> Dict[str, any]:
    """
    Computes classical Bhrigu Nandi Nadi 12-Year Progression Cycle (भृगु 12 वर्षीय चक्र भ्रमण).
    Jupiter transits each 12-year epoch activating sequential houses and karmic milestones.
    """
    if current_date is None:
        current_date = datetime.now(timezone.utc)
    elif current_date.tzinfo is None:
        current_date = current_date.replace(tzinfo=timezone.utc)

    if birth_date.tzinfo is None:
        birth_date = birth_date.replace(tzinfo=timezone.utc)

    age_days = (current_date - birth_date).total_seconds() / 86400.0
    age_years = max(0.0, age_days / 365.25)

    cycle_idx = min(6, int(age_years // 12) + 1)
    cycle_start = (cycle_idx - 1) * 12
    cycle_end = cycle_idx * 12

    progressed_sign_idx = (jupiter_sign + cycle_idx - 1) % 12
    prog_sign_name = constants.SIGNS[progressed_sign_idx]
    prog_sign_hi = constants.SIGNS_HI[progressed_sign_idx]

    cycle_themes = {
        1: {
            "title_hi": "प्रथम चक्र (आयु 0 से 12 वर्ष) — आधारशिला एवं बाल्यकाल",
            "focus_hi": "शारीरिक स्वास्थ्य, प्रारंभिक पारिवारिक संस्कार एवं मूल शिक्षा का निर्माण।",
            "karmic_mandate_hi": "माता-पिता के संरक्षण में आत्म-चेतना का विकास।"
        },
        2: {
            "title_hi": "द्वितीय चक्र (आयु 12 से 24 वर्ष) — विद्या, कौशल एवं युवा जागृति",
            "focus_hi": "उच्चतर माध्यमिक व विश्वविद्यालयीन विद्या, मित्रों का चयन एवं आजीविका के मूल कौशलों का अर्जन।",
            "karmic_mandate_hi": "बुद्धि व कर्म की दिशा निर्धारित करना।"
        },
        3: {
            "title_hi": "तृतीय चक्र (आयु 24 से 36 वर्ष) — कर्म प्रतिष्ठा, विवाह व गृहस्थ आरम्भ",
            "focus_hi": "स्वयं के पैरों पर खड़े होना, आजीविका में प्रारंभिक संघर्ष के पश्चात स्थायित्व, विवाह एवं पारिवारिक विस्तार।",
            "karmic_mandate_hi": "सांसारिक कर्तव्यों व सामाजिक प्रतिष्ठा का निर्माण।"
        },
        4: {
            "title_hi": "चतुर्थ चक्र (आयु 36 से 48 वर्ष) — चरम पुरुषार्थ, अधिकार एवं स्थायित्व",
            "focus_hi": "करियर का शीर्ष काल, स्वतंत्र उद्यम/शोध में बड़ी उपलब्धियां, अचल सम्पत्ति का संचय एवं उच्च सम्मान।",
            "karmic_mandate_hi": "अपने अर्जित ज्ञान व कौशल से समाज का नेतृत्व करना।"
        },
        5: {
            "title_hi": "पंचम चक्र (आयु 48 से 60 वर्ष) — परामर्श, वरिष्ठता एवं आध्यात्मिक परिपक्वता",
            "focus_hi": "संस्थानों में सर्वोच्च सलाहकार या नीति-निर्माता की भूमिका, संतानों का अभ्युदय, आध्यात्मिक व दार्शनिक चिंतन।",
            "karmic_mandate_hi": "अग्रजों के रूप में नई पीढ़ी को मार्गदर्शन व धर्म पालन।"
        },
        6: {
            "title_hi": "षष्ठ चक्र (आयु 60 से 72 वर्ष) — विरक्ति, आत्म-सिद्धि एवं मोक्ष मार्ग",
            "focus_hi": "सांसारिक उत्तरदायित्वों से मुक्ति, परा-विद्या, ईश्वरीय शरणागति एवं आत्म-साक्षात्कार।",
            "karmic_mandate_hi": "परम शांति व मोक्ष पद की प्राप्ति।"
        }
    }

    info = cycle_themes.get(cycle_idx, cycle_themes[4])

    return {
        "current_age_years": round(age_years, 1),
        "cycle_index": cycle_idx,
        "cycle_span_str": f"{cycle_start} से {cycle_end} वर्ष",
        "progressed_sign": prog_sign_name,
        "progressed_sign_hi": prog_sign_hi,
        "cycle_title_hi": info["title_hi"],
        "cycle_focus_hi": info["focus_hi"],
        "cycle_mandate_hi": info["karmic_mandate_hi"]
    }
