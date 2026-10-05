"""Chakra Systems Engine: Sarvatobhadra Chakra (SBC), Kota Chakra, and 27-Navatara Chakra.

Classical implementations:
1. Sarvatobhadra Chakra (SBC):
   - 28 Nakshatras including Abhijit (between Uttara Ashadha and Shravana: 276°40' to 280°53'20").
   - 9 Special Sensitive Nakshatras from Janma Nakshatra:
     * 1. Janma (Birth)
     * 10. Karma (Profession/Action)
     * 16. Sanghatika (Alliances/Partnerships)
     * 18. Samudayika (Community/General prosperity)
     * 23. Vainashika / Vinasha (Destruction/Loss)
     * 25. Manasa (Mental state/Mind)
     * 26. Rajyada / Abhisheka (Authority/Coronation)
   - Planetary Vedha aspects: Left (Vama), Right (Dakshina), Front (Sammukha).

2. Kota Chakra (Fortress Chart):
   - 4 concentric segments:
     * Stambha (Central Pillar / Core - Most vulnerable)
     * Madhya (Inner Court / Wall)
     * Prakaara (Outer Boundary)
     * Bahya (Exterior / Outskirts)
   - Kota Swami (Lord of the Fort: Rashi Lord of Janma Rashi)
   - Kota Pala (Guardian of the Fort: Star Lord of Janma Nakshatra)
   - Transit planets on Pravesha (Entry) vs Nirgama (Exit) rays.

3. Navatara Chakra (27 Taras across 3 Paryayas):
   - Prathama Paryaya (1-9: Janma, Sampat, Vipat, Kshema, Pratyari, Sadhaka, Vadha, Mitra, Ati-Mitra)
   - Dvitiya Paryaya (10-18: Karmika / Anujanma series)
   - Tritiya Paryaya (19-27: Trijanma / Vainashika series)
"""
from typing import Dict, List, Tuple, NamedTuple
import math
from vyas import constants

# 28 Nakshatra definitions (incorporating Abhijit)
NAKSHATRAS_28 = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Abhijit", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_28_nakshatra_index(longitude: float) -> int:
    """
    Computes index in 28-nakshatra scheme (0 to 27).
    Abhijit occupies the last quarter of Uttara Ashadha (from 276°40' to 280°00')
    and the first 1/15th of Shravana (up to 280°53'20").
    """
    lon = longitude % 360.0
    # Abhijit span: 276.6667° to 280.8889°
    if 276.666667 <= lon < 280.888889:
        return 21 # Abhijit
    elif lon < 276.666667:
        # Before Abhijit
        std_idx = int(lon // constants.NAKSHATRA_SPAN)
        return min(std_idx, 20)
    else:
        # After Abhijit (Shravana onwards shifted by 1)
        # Remainder of 360 from 280.8889 onwards maps to Shravana (22) .. Revati (27)
        deg_after = lon - 280.888889
        span_remaining = (360.0 - 280.888889) / 6.0
        shifted_idx = 22 + int(deg_after // span_remaining)
        return min(shifted_idx, 27)

# --- 1. SARVATOBHADRA CHAKRA (SBC) ---
class SBCSpecialPoint(NamedTuple):
    name: str
    nakshatra_28: str
    index_from_janma: int
    significance: str
    transiting_planets: List[str]

def compute_sbc_special_points(natal_moon_lon: float, transit_planet_lons: Dict[str, float]) -> List[SBCSpecialPoint]:
    """
    Calculates the 7 primary sensitive Nakshatras in Sarvatobhadra Chakra and checks for transiting vedha/afflictions.
    """
    janma_idx_28 = get_28_nakshatra_index(natal_moon_lon)
    
    # Offsets in 28-nakshatra scheme
    # Janma (1), Karma (10), Sanghatika (16), Samudayika (18), Vainashika (23), Manasa (25), Rajyada (26)
    offsets = [
        (1, "Janma Nakshatra", "Physical body, vitality, and primary personal destiny"),
        (10, "Karma Nakshatra", "Career, profession, social standing, and actions"),
        (16, "Sanghatika Nakshatra", "Alliances, partnerships, debts, and relationships"),
        (18, "Samudayika Nakshatra", "Community standing, crowd support, and general prosperity"),
        (23, "Vainashika (Vinasha)", "Vulnerability, loss, sudden obstacles, and destruction"),
        (25, "Manasa Nakshatra", "Psychological tranquility, intellect, and mental focus"),
        (26, "Rajyada / Abhisheka", "Authority, coronation, recognition, and government favor")
    ]
    
    # Map transit planets to 28-nakshatra
    tr_map: Dict[int, List[str]] = {i: [] for i in range(28)}
    for p_name, p_lon in transit_planet_lons.items():
        p_idx = get_28_nakshatra_index(p_lon)
        tr_map[p_idx].append(p_name)
        
    points = []
    for off, title, desc in offsets:
        target_idx = (janma_idx_28 + off - 1) % 28
        nak_name = NAKSHATRAS_28[target_idx]
        occupants = tr_map[target_idx]
        points.append(SBCSpecialPoint(
            name=title,
            nakshatra_28=nak_name,
            index_from_janma=off,
            significance=desc,
            transiting_planets=occupants
        ))
    return points


# --- 2. KOTA CHAKRA ---
class KotaSegment(NamedTuple):
    segment_name: str
    nakshatras: List[str]
    planets_present: List[str]
    nature: str

class KotaAnalysis(NamedTuple):
    kota_swami: str       # Lord of the Fort (Janma Rashi Lord)
    kota_pala: str        # Guardian of the Fort (Janma Nakshatra Lord)
    segments: Dict[str, KotaSegment]
    is_fort_under_siege: bool
    summary: str

def compute_kota_chakra(natal_moon_lon: float, natal_asc_lon: float, 
                        planet_lons: Dict[str, float]) -> KotaAnalysis:
    """
    Computes Kota Chakra segments and evaluates the security/vulnerability of the native's fort.
    Segments (from interior to exterior):
    1. Stambha (Central Pillar): 4 nakshatras (center)
    2. Madhya (Inner Circle): 4 nakshatras
    3. Prakaara (Fort Wall): 8 nakshatras
    4. Bahya (Outer Field): 12 nakshatras
    """
    janma_nak_idx = int(natal_moon_lon // constants.NAKSHATRA_SPAN) % 27
    janma_sign_idx = int(natal_moon_lon // 30.0) % 12
    
    kota_swami = constants.SIGN_LORD[janma_sign_idx]
    kota_pala = constants.VIMSHOTTARI_ORDER[janma_nak_idx % 9]
    
    # Relative mapping of the 28 nakshatras to Kota concentric regions
    # Classical distribution based on Janma Nakshatra orientation:
    stambha_offsets = [0, 7, 14, 21]           # 4 Pillar nakshatras
    madhya_offsets = [1, 6, 15, 20]            # 4 Inner Court nakshatras
    prakaara_offsets = [2, 5, 8, 13, 16, 19, 22, 27] # 8 Boundary Wall nakshatras
    bahya_offsets = [3, 4, 9, 10, 11, 12, 17, 18, 23, 24, 25, 26] # 12 Exterior nakshatras
    
    def get_names(offsets):
        return [constants.NAKSHATRAS[(janma_nak_idx + o) % 27] for o in offsets if (janma_nak_idx + o) % 27 < 27]

    seg_names = {
        "Stambha (Pillar / Core)": (get_names(stambha_offsets), "Most Vital Core: Malefics here threaten foundation/health."),
        "Madhya (Inner Court)": (get_names(madhya_offsets), "Inner Enclosure: Influences emotional and familial peace."),
        "Prakaara (Fort Wall)": (get_names(prakaara_offsets), "Rampart / Defense: Gateways of entry and exit."),
        "Bahya (Exterior / Outskirts)": (get_names(bahya_offsets), "External Surroundings: Outside forces and worldly contact.")
    }
    
    # Map planets
    seg_results = {}
    malefics_in_stambha = []
    benefics_in_stambha = []
    
    for s_name, (nak_list, nat_desc) in seg_names.items():
        present = []
        for p_name, p_lon in planet_lons.items():
            p_nak = constants.NAKSHATRAS[int(p_lon // constants.NAKSHATRA_SPAN) % 27]
            if p_nak in nak_list:
                present.append(p_name)
                if s_name.startswith("Stambha"):
                    if p_name in ("Saturn", "Mars", "Rahu", "Ketu", "Sun"):
                        malefics_in_stambha.append(p_name)
                    else:
                        benefics_in_stambha.append(p_name)
                        
        seg_results[s_name] = KotaSegment(
            segment_name=s_name,
            nakshatras=nak_list,
            planets_present=present,
            nature=nat_desc
        )
        
    under_siege = len(malefics_in_stambha) > 0 and len(benefics_in_stambha) == 0
    if under_siege:
        summary = (f"Fortress is under distress: Malefic(s) {malefics_in_stambha} afflict the central Stambha (Core) "
                   f"without protective benefic cushion. Demands caution against disputes, accidents, or sudden setbacks.")
    elif len(benefics_in_stambha) > 0:
        summary = (f"Fortress is fortified: Benefic(s) {benefics_in_stambha} grace the Stambha (Pillar). "
                   f"The native's inner fortitude and resistance remain resilient.")
    else:
        summary = "Fortress balance is stable. Planetary distribution occupies exterior and defensive ramparts."

    return KotaAnalysis(
        kota_swami=kota_swami,
        kota_pala=kota_pala,
        segments=seg_results,
        is_fort_under_siege=under_siege,
        summary=summary
    )


# --- 3. 27 NAVATARA CHAKRA (3 PARYAYAS) ---
TARA_NAMES = [
    ("Janma", "Birth / Body / Personal Identity", "Neutral/Mixed"),
    ("Sampat", "Wealth / Inflow / Prosperity", "Auspicious"),
    ("Vipat", "Peril / Obstacles / Sudden Complications", "Inauspicious"),
    ("Kshema", "Well-being / Security / Preservation", "Auspicious"),
    ("Pratyari", "Enmity / Contention / Opposition", "Inauspicious"),
    ("Sadhaka", "Achievement / Fulfillment / Success in endeavors", "Auspicious"),
    ("Vadha (Naidhana)", "Destruction / Fatal affliction / Severe strain", "Highly Inauspicious"),
    ("Mitra", "Friendly alliance / Cooperative progress", "Auspicious"),
    ("Ati-Mitra", "Intimate companionship / Peak fortune", "Highly Auspicious")
]

class NavataraItem(NamedTuple):
    paryaya_num: int
    paryaya_name: str
    tara_name: str
    tara_index: int
    nakshatra_name: str
    nakshatra_lord: str
    quality: str
    planets_present: List[str]

def compute_navatara_chakra(natal_moon_lon: float, planet_lons: Dict[str, float]) -> List[NavataraItem]:
    """
    Computes all 27 Taras across the 3 Paryayas:
    1. Prathama Paryaya (1-9): Immediate physical manifestation
    2. Dvitiya Paryaya (10-18): Karmic / Professional realm (Karmika)
    3. Tritiya Paryaya (19-27): Subconscious / Ancestral realm (Trijanma / Vainashika)
    """
    janma_nak_idx = int(natal_moon_lon // constants.NAKSHATRA_SPAN) % 27
    
    paryayas = [
        (1, "Prathama Paryaya (Personal / Physical Realm)"),
        (2, "Dvitiya Paryaya (Karmic / Societal Realm)"),
        (3, "Tritiya Paryaya (Ancestral / Transcendent Realm)")
    ]
    
    # Map planets to nakshatra index
    pl_in_nak: Dict[int, List[str]] = {i: [] for i in range(27)}
    for p_name, p_lon in planet_lons.items():
        idx = int(p_lon // constants.NAKSHATRA_SPAN) % 27
        pl_in_nak[idx].append(p_name)
        
    items = []
    for p_num, p_title in paryayas:
        base_offset = (p_num - 1) * 9
        for t_idx in range(9):
            nak_idx = (janma_nak_idx + base_offset + t_idx) % 27
            nak_name = constants.NAKSHATRAS[nak_idx]
            nak_lord = constants.VIMSHOTTARI_ORDER[nak_idx % 9]
            t_name, t_desc, t_qual = TARA_NAMES[t_idx]
            
            items.append(NavataraItem(
                paryaya_num=p_num,
                paryaya_name=p_title,
                tara_name=t_name,
                tara_index=t_idx + 1,
                nakshatra_name=nak_name,
                nakshatra_lord=nak_lord,
                quality=t_qual,
                planets_present=pl_in_nak[nak_idx]
            ))
            
    return items


# --- 4. SUDARSHAN CHAKRA (सुदर्शन चक्र) ---
class SudarshanHouse(NamedTuple):
    house_num: int
    name_hi: str
    lagna_sign: str
    lagna_sign_hi: str
    lagna_sign_lord: str
    lagna_planets: List[str]
    chandra_sign: str
    chandra_sign_hi: str
    chandra_sign_lord: str
    chandra_planets: List[str]
    surya_sign: str
    surya_sign_hi: str
    surya_sign_lord: str
    surya_planets: List[str]
    confluence_score: int
    status: str
    summary_hi: str


class SudarshanChakraAnalysis(NamedTuple):
    lagna_sign: str
    lagna_sign_hi: str
    chandra_sign: str
    chandra_sign_hi: str
    surya_sign: str
    surya_sign_hi: str
    houses: List[SudarshanHouse]
    power_houses: List[int]
    vulnerable_houses: List[int]
    sudarshan_verdict_hi: str


def compute_sudarshan_chakra(chart) -> SudarshanChakraAnalysis:
    """
    Computes Sudarshan Chakra (सुदर्शन चक्र) analyzing 12 Bhavas from Lagna, Chandra, and Surya charts.
    BPHS Ch 73: 'Lagnam Chandram tatha Suryam trikam Sudarshanam viduh'.
    """
    asc_sign = chart.ascendant_sign
    planets = chart.planets
    
    moon_sign = planets["Moon"].sign_index if "Moon" in planets else 0
    sun_sign = planets["Sun"].sign_index if "Sun" in planets else 0
    
    # Map sign index -> list of planets
    sign_planets: Dict[int, List[str]] = {s: [] for s in range(12)}
    for p_name, p_state in planets.items():
        if p_name in constants.PLANETS:
            sign_planets[p_state.sign_index].append(p_name)
            
    house_names_hi = [
        "प्रथम भाव (तनु / शारीरिक आरोग्य व व्यक्तित्व)",
        "द्वितीय भाव (धन / संचित कोष व कुटुंब)",
        "तृतीय भाव (सहज / पराक्रम, भ्रातृ व उद्यम)",
        "चतुर्थ भाव (सुख / माता, भूमि, भवन व वाहन)",
        "पंचम भाव (सुत / विद्या, बुद्धि, संतान व विवेक)",
        "षष्ठ भाव (रिपु / रोग, ऋण, शत्रु व प्रतिस्पर्धा)",
        "सप्तम भाव (जाया / जीवनसाथी, साझेदारी व पद)",
        "अष्टम भाव (आयु / गूढ़ ज्ञान, संकट व आकस्मिकता)",
        "नवम भाव (भाग्य / धर्म, उच्च दर्शन व तीर्थ)",
        "दशम भाव (कर्म / आजीविका, प्रतिष्ठा व प्रभुत्व)",
        "एकादश भाव (लाभ / आय, मनोरथ सिद्धि व उपलब्धि)",
        "द्वादश भाव (व्यय / मोक्ष, विदेश वास व त्याग)"
    ]
    
    benefics = {"Jupiter", "Venus", "Mercury", "Moon"}
    malefics = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}
    
    houses: List[SudarshanHouse] = []
    power_houses: List[int] = []
    vulnerable_houses: List[int] = []
    
    for h in range(1, 13):
        # 1. Lagna wheel
        l_sign = (asc_sign + h - 1) % 12
        l_lord = constants.SIGN_LORD[l_sign]
        l_pls = sign_planets[l_sign]
        
        # 2. Chandra wheel
        c_sign = (moon_sign + h - 1) % 12
        c_lord = constants.SIGN_LORD[c_sign]
        c_pls = sign_planets[c_sign]
        
        # 3. Surya wheel
        s_sign = (sun_sign + h - 1) % 12
        s_lord = constants.SIGN_LORD[s_sign]
        s_pls = sign_planets[s_sign]
        
        # All planets influencing this bhava across the 3 wheels
        all_wheel_pls = l_pls + c_pls + s_pls
        ben_count = sum(1 for p in all_wheel_pls if p in benefics)
        mal_count = sum(1 for p in all_wheel_pls if p in malefics)
        score = ben_count - mal_count
        
        if ben_count >= 2 and mal_count == 0:
            status = "त्रिविध शक्ति केंद्र (Triple Power Center)"
            power_houses.append(h)
            summary_hi = f"सुदर्शन चक्र के तीनों आयामों (लग्न, चन्द्र, सूर्य) से यह भाव शुभ ग्रहों द्वारा अनुप्राणित है। इस भाव से सम्बद्ध विषय जातक को सहज यश, पूर्ण संतुष्टि और अक्षुण्ण सफलता प्रदान करेंगे।"
        elif ben_count >= mal_count and ben_count > 0:
            status = "सशक्त शुभ भाव (Auspicious Confluence)"
            if score >= 1:
                power_houses.append(h)
            summary_hi = f"यह भाव सुदर्शन चक्र में शुभ ऊर्जा से युक्त है। देह (लग्न) और मन (चन्द्र) अथवा आत्मा (सूर्य) का सकारात्मक सहयोग इस भाव के फलों को अभिवर्धित करेगा।"
        elif mal_count >= 2 and ben_count == 0:
            status = "कर्मिक परीक्षा केंद्र (Karmic Stress Center)"
            vulnerable_houses.append(h)
            summary_hi = f"तीनों संदर्भों में पाप ग्रहों का प्रभाव केंद्रित होने से यह भाव जीवन में परीक्षा, विलंब अथवा संघर्ष का कारक बन सकता है। इस भाव सम्बन्धी निर्णयों में विशेष विवेक व उपाय आवश्यक हैं।"
        elif mal_count > ben_count:
            status = "सावधानी अपेक्षित (Caution Advised)"
            vulnerable_houses.append(h)
            summary_hi = f"पाप ग्रहों का आंशिक दबाव है। जातक को परिश्रम और संयम के उपरांत ही इस भाव के यथोचित परिणाम प्राप्त होंगे।"
        else:
            status = "संतुलित भाव (Neutral / Balanced)"
            summary_hi = f"सुदर्शन चक्र में यह भाव सम अवस्था में है। गोचर और दशा अनुकूल होने पर सामान्य शुभ फल प्राप्त होंगे।"
            
        houses.append(SudarshanHouse(
            house_num=h,
            name_hi=house_names_hi[h - 1],
            lagna_sign=constants.SIGNS[l_sign],
            lagna_sign_hi=constants.SIGNS_HI[l_sign],
            lagna_sign_lord=l_lord,
            lagna_planets=l_pls,
            chandra_sign=constants.SIGNS[c_sign],
            chandra_sign_hi=constants.SIGNS_HI[c_sign],
            chandra_sign_lord=c_lord,
            chandra_planets=c_pls,
            surya_sign=constants.SIGNS[s_sign],
            surya_sign_hi=constants.SIGNS_HI[s_sign],
            surya_sign_lord=s_lord,
            surya_planets=s_pls,
            confluence_score=score,
            status=status,
            summary_hi=summary_hi
        ))
        
    p_str = ", ".join([f"भाव {h}" for h in power_houses]) if power_houses else "कोई विशिष्ट शक्ति केंद्र नहीं"
    v_str = ", ".join([f"भाव {h}" for h in vulnerable_houses]) if vulnerable_houses else "कोई गंभीर परीक्षा केंद्र नहीं"
    
    verdict = (
        f"सुदर्शन चक्र के त्रिविध विश्लेषण (देह: {constants.SIGNS_HI[asc_sign]}, मन: {constants.SIGNS_HI[moon_sign]}, आत्मा: {constants.SIGNS_HI[sun_sign]}) "
        f"के अनुसार जातक के सर्वोच्च शक्ति केंद्र **{p_str}** हैं जहाँ शुभ ग्रहों का त्रिक संगम प्राप्त है। "
        f"इसके विपरीत **{v_str}** पर पाप प्रभाव केंद्रित होने से अतिरिक्त सजगता व शांति उपाय अभीष्ट हैं।"
    )
    
    return SudarshanChakraAnalysis(
        lagna_sign=constants.SIGNS[asc_sign],
        lagna_sign_hi=constants.SIGNS_HI[asc_sign],
        chandra_sign=constants.SIGNS[moon_sign],
        chandra_sign_hi=constants.SIGNS_HI[moon_sign],
        surya_sign=constants.SIGNS[sun_sign],
        surya_sign_hi=constants.SIGNS_HI[sun_sign],
        houses=houses,
        power_houses=power_houses,
        vulnerable_houses=vulnerable_houses,
        sudarshan_verdict_hi=verdict
    )
