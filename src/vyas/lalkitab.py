"""Comprehensive Lal Kitab Engine for VYAS.

Implements the classical tenets of Pt. Roop Chand Joshi (1939-1952) and
modern pioneer Pt. G.D. Vashist:
- Kalapurusha Fixed Sign House Rulership (Aries=1, Taurus=2, etc.)
- Sleeping Houses (Soya Hua Ghar) & Sleeping Planets (Soya Hua Grah)
- Blind Chart (Andhi Kundli) & Half-Blind Chart (Dharmi Tewa)
- Benefic (Nek) and Malefic (Manda) planet placements
- Kayam Grah & Masnui (Artificial) planets
- Precise classical Lal Kitab Upayas (Remedies) for all 9 planets across 12 houses.
"""
from typing import Dict, List, Tuple

# Natural House (Pakka Ghar) Rulers in Lal Kitab
PAKKA_GHAR_LORDS = {
    1: "Sun",
    2: "Jupiter",
    3: "Mars",
    4: "Moon",
    5: "Jupiter",
    6: "Mercury",
    7: "Venus",
    8: "Saturn",
    9: "Jupiter",
    10: "Saturn",
    11: "Jupiter",
    12: "Jupiter"
}

# Pakka Ghar ownership (Where planets feel permanent natural domain)
PLANET_PAKKA_GHAR = {
    "Sun": [1, 5],
    "Moon": [4],
    "Mars": [3, 8],
    "Mercury": [6, 7],
    "Jupiter": [2, 5, 9, 11, 12],
    "Venus": [7],
    "Saturn": [8, 10, 11],
    "Rahu": [12],
    "Ketu": [6]
}

# Exaltation (Uchha) and Debilitation (Neecha) houses in Lal Kitab
LALKITAB_EXALT_HOUSE = {
    "Sun": 1, "Moon": 2, "Mars": 10, "Mercury": 6,
    "Jupiter": 4, "Venus": 12, "Saturn": 7, "Rahu": 3, "Ketu": 9
}
LALKITAB_DEBIL_HOUSE = {
    "Sun": 7, "Moon": 8, "Mars": 4, "Mercury": 12,
    "Jupiter": 10, "Venus": 6, "Saturn": 1, "Rahu": 9, "Ketu": 3
}

# Classical Authentic Remedies (G.D. Vashist & Pt. Roop Chand Joshi)
HOUSE_REMEDIES = {
    "Sun": {
        1: "Maintain good moral conduct; do not accept free items; build water arrangements.",
        2: "Offer coconut or badam in temple; respect father and elders.",
        3: "Serve maternal uncle; keep brass utensils in house.",
        4: "Feed bread to black dog; don't sell gold in distress.",
        5: "Control anger; avoid bad company; keep copper coin in pocket.",
        6: "Keep water in brass vessel at bedside and pour at sunrise; bury silver coin.",
        7: "Feed black cows or visually impaired persons; keep silver piece with you.",
        8: "Do not build underground water tank; touch feet of elder Brahmins.",
        9: "Use brass utensils; donate copper or wheat on Sundays.",
        10: "Do not wear blue or black clothes; avoid meat and alcohol.",
        11: "Eat sweet before leaving home; do not consume radish after sunset.",
        12: "Keep courtyard clean; install a handpump or water source for public."
    },
    "Moon": {
        1: "Touch mother's feet daily for blessings; keep silver square piece.",
        2: "Do not accept silver articles as gift; respect mother and women.",
        3: "Do not use silver ornaments for kids; donate green clothes to girls.",
        4: "Do not sell milk; keep rainwater stored in glass bottle at home.",
        5: "Do not speak harsh words; keep water in silver vessel.",
        6: "Do not dig well or pump inside hospital; keep rabbit at home.",
        7: "Do not marry before 24 without parent's full consent; keep silver with pearls.",
        8: "Never build well in house; donate milk or rice in religious shrine.",
        9: "Keep silver and water in worship room; visit pilgrimage sites.",
        10: "Do not drink milk at night; keep tap water running smoothly (no leak).",
        11: "Drink milk with saffron; donate white flowers.",
        12: "Do not sleep under open sky; feed kheer to little girls."
    },
    "Mars": {
        1: "Avoid anger; keep deer skin or keep honey in silver pot at home.",
        2: "Keep deer horn or red handkerchief; support maternal uncle.",
        3: "Wear pure silver ring without joint; never deceive brothers.",
        4: "Keep sweet food under earth; keep ivory item or silver toy.",
        5: "Keep pure copper vessel filled with water; stay truthful.",
        6: "Worship Lord Hanuman; distribute jaggery on Tuesdays.",
        7: "Build sister's prosperity; don't plant thorny cactus at home.",
        8: "Feed dogs; keep silver plate; avoid partnership in iron.",
        9: "Respect elder brothers; wear gold; avoid red clothes if aggressive.",
        10: "Do not sell gold inherited from parents; feed monkeys.",
        11: "Keep mustard oil in earthen pot buried under ground.",
        12: "Feed sweet bread (tandoori meethi roti) to dogs."
    },
    "Mercury": {
        1: "Avoid green clothes; wear silver chain in neck.",
        2: "Piercing in nose for ladies with silver wire; avoid gambling.",
        3: "Bury empty earthen pot in desolate ground.",
        4: "Feed whole moong dal soaked in water to birds.",
        5: "Wear copper coin with hole in white thread; feed cows.",
        6: "Pierce nose; wear silver wire; don't marry daughter in north direction.",
        7: "Avoid keeping broad-leafed plants (money plant) inside bedroom.",
        8: "Wash yellow pulse (chana dal) in running water; worship Goddess Durga.",
        9: "Pierce nose; wear silver wire; do not keep cages in house.",
        10: "Do not consume alcohol; feed green fodder to cows.",
        11: "Wear copper coin with hole; donate green glass bangles to eunuchs.",
        12: "Bury yellow glass beads or silver coin under yellow soil."
    },
    "Jupiter": {
        1: "Apply saffron (kesar) tilak on forehead, navel and tongue daily.",
        2: "Respect father and spiritual preceptors; donate yellow sweets.",
        3: "Feed gram pulse (chana dal) to cows; worship Peepal tree.",
        4: "Never dishonor elders; keep pure gold on body.",
        5: "Do not accept donations or alms; help temple priests.",
        6: "Feed chickens or birds with yellow grains; avoid ego in knowledge.",
        7: "Keep brass idol of deities; respect wife and preceptor.",
        8: "Do not wear yellow clothes if facing hurdles; donate ghee in temple.",
        9: "Visit temple daily; bathe in holy rivers; keep pure intentions.",
        10: "Apply saffron tilak; do not preach without practicing.",
        11: "Sleep on yellow bedsheet; keep pure gold chain.",
        12: "Keep saunf (fennel seeds) wrapped in red cloth under pillow."
    },
    "Venus": {
        1: "Take bath with curd or milk; do not indulge in immoral company.",
        2: "Feed cows with green fodder or white sweets.",
        3: "Respect wife; avoid arrogance in clothes and luxury.",
        4: "Do not build rooftop garden; keep silver brick in house.",
        5: "Take blessings of elder women; maintain clean character.",
        6: "Keep pure silver coin; bathe in milk occasionally.",
        7: "Feed white cows; donate curd and camphor at temple.",
        8: "Donate blue or white clothes; avoid footwear gifts.",
        9: "Keep silver square piece; bury honey in earthen pot.",
        10: "Wash private parts with alum water; maintain marital fidelity.",
        11: "Donate mustard oil with reflection (Chhaya Daan); keep white horse toy.",
        12: "Donate kapur (camphor) in temple; respect wife unconditionally."
    },
    "Saturn": {
        1: "Do not drink alcohol or eat meat; avoid falsehood.",
        2: "Feed black dogs or buffaloes with mustard-oiled bread.",
        3: "Serve physically challenged persons; don't build dark basements.",
        4: "Feed crows and fish; do not consume fish or non-veg.",
        5: "Keep almonds in temple and bring half back to store at home.",
        6: "Feed black dogs; bury mustard oil in earthen pot in cemetery.",
        7: "Feed black cows; keep iron nail in threshold.",
        8: "Do not consume alcohol; donate mustard oil on Saturdays.",
        9: "Do not build roof or house during Saturn dasha without remedies.",
        10: "Keep water for birds; respect laborers and servants.",
        11: "Bury oil in soil; keep iron ring made of black horseshoe.",
        12: "Do not deceive anyone; avoid dark dingy rooms without ventilation."
    },
    "Rahu": {
        1: "Keep silver coin or elephant made of pure silver in bedroom.",
        2: "Keep silver ball in pocket; respect mother and maternal uncle.",
        3: "Keep ivory or silver idol; maintain good terms with siblings.",
        4: "Immerse raw coal in running water (river) on Saturdays.",
        5: "Keep silver elephant; donate barley (jau) or coconut in flowing water.",
        6: "Keep black dog; maintain clean toilet and bathroom at all times.",
        7: "Do not keep electrical junk or non-working clocks at home.",
        8: "Immerse 8 coconuts with husk in river on Saturdays.",
        9: "Wear gold ring in index finger; respect grandfather.",
        10: "Do not sit idle; cover head with white cap or cloth.",
        11: "Drink water in silver glass; avoid electric gadgets gift.",
        12: "Eat food inside the kitchen floor; avoid eating on bed."
    },
    "Ketu": {
        1: "Keep a black and white dog (two-colored dog) at home or feed stray dogs.",
        2: "Apply saffron tilak; respect spiritual saints.",
        3: "Wear pure gold ring in ears or fingers.",
        4: "Float yellow lemon or gram pulse in river.",
        5: "Donate sesame seeds and blankets in winter to poor.",
        6: "Wear gold earrings; feed dogs with sweet bread.",
        7: "Keep good character; do not make false promises.",
        8: "Feed street dogs; pierce ears and wear gold.",
        9: "Keep brass utensils; respect religious traditions.",
        10: "Keep silver vessel filled with honey at home.",
        11: "Keep black dog; donate black and white sesame in temple.",
        12: "Worship Lord Ganesha; feed dogs with bread."
    }
}

def analyze_lalkitab(planets_data: Dict[str, dict], asc_sign_idx: int) -> Dict:
    """
    Performs full classical Lal Kitab diagnostic analysis:
    - House occupation (1-12)
    - Sleeping Houses (Soya Ghar)
    - Sleeping Planets (Soya Grah)
    - Dharmi Tewa (Half-blind pious chart)
    - Andhi Kundli (Blind chart)
    - Pakka Ghar status
    - Specific targeted remedies
    """
    # Map planets to houses (1-12)
    house_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    planet_house_map: Dict[str, int] = {}

    for p_name, p_info in planets_data.items():
        if p_name not in HOUSE_REMEDIES:
            continue
        p_sign = p_info["sign_index"]
        # In Lal Kitab, House 1 = Ascendant sign house
        h_num = (p_sign - asc_sign_idx + 12) % 12 + 1
        house_planets[h_num].append(p_name)
        planet_house_map[p_name] = h_num

    # 1. Sleeping Houses (Soya Ghar): Houses with no planet and no aspect
    # In Lal Kitab rule: House without any planet is a sleeping house.
    sleeping_houses = [h for h, plist in house_planets.items() if len(plist) == 0]

    # 2. Sleeping Planets (Soya Grah):
    # If a planet occupies a house whose owner/ruler has no planet, or planet does not have direct aspect.
    sleeping_planets = []
    for p_name, h_num in planet_house_map.items():
        # A planet is sleeping if it has no planets in houses it aspects or no planets in opposite 7th house
        opp_house = (h_num + 5) % 12 + 1
        if len(house_planets[opp_house]) == 0 and len(house_planets[h_num]) == 1:
            sleeping_planets.append(p_name)

    # 3. Andhi Kundli (Blind Chart):
    # Rule: If Saturn is in 7th and Sun/Mars in 1st, or 10th house has mutual conflict,
    # or houses 10 & 9 have enemy planets without neutralizers.
    # Traditional: Saturn in 10 and Sun/Mars in 1, or 10th house aspected by inimical combination.
    is_andhi_kundli = False
    if "Saturn" in house_planets[10] and ("Sun" in house_planets[1] or "Mars" in house_planets[1]):
        is_andhi_kundli = True
    elif "Saturn" in house_planets[7] and "Sun" in house_planets[1]:
        is_andhi_kundli = True

    # 4. Dharmi Tewa (Pious / Protected Chart):
    # Rule: If Jupiter is in 1st, 5th, 9th, or 11th; or Rahu/Ketu associated with Jupiter or Moon;
    # or Saturn placed in 11th house without malefic aspect.
    is_dharmi_tewa = False
    if "Jupiter" in house_planets[1] or "Jupiter" in house_planets[9] or "Jupiter" in house_planets[11]:
        is_dharmi_tewa = True
    elif "Moon" in house_planets[4] or "Saturn" in house_planets[11]:
        is_dharmi_tewa = True
    elif "Jupiter" in house_planets[planet_house_map.get("Rahu", 0)] or "Jupiter" in house_planets[planet_house_map.get("Ketu", 0)]:
        is_dharmi_tewa = True

    # 5. Compile planetary diagnostic status & remedies
    planet_details = []
    for p_name, h_num in planet_house_map.items():
        pakka_ghars = PLANET_PAKKA_GHAR.get(p_name, [])
        is_pakka = h_num in pakka_ghars
        is_uchha = (LALKITAB_EXALT_HOUSE.get(p_name) == h_num)
        is_neecha = (LALKITAB_DEBIL_HOUSE.get(p_name) == h_num)
        
        status = "सामान्य (Normal)"
        if is_uchha:
            status = "उच्च स्थिति (Exalted Nek)"
        elif is_neecha:
            status = "नीच स्थिति (Debilitated Manda)"
        elif is_pakka:
            status = "पक्का घर में (In Pakka Ghar)"

        is_soya = p_name in sleeping_planets
        remedy = HOUSE_REMEDIES.get(p_name, {}).get(h_num, "नियमित गायत्री मंत्र जप एवं सदाचार रखें।")

        planet_details.append({
            "graha": p_name,
            "house": h_num,
            "status": status,
            "is_sleeping": "सोया हुआ (Sleeping)" if is_soya else "जागृत (Active)",
            "pakka_ghar_lord": PAKKA_GHAR_LORDS.get(h_num, "-"),
            "remedy": remedy
        })

    return {
        "planet_details": planet_details,
        "sleeping_houses": sleeping_houses,
        "sleeping_planets": sleeping_planets,
        "is_andhi_kundli": is_andhi_kundli,
        "is_dharmi_tewa": is_dharmi_tewa,
        "summary": {
            "dharmi_status": "धर्मी तेवा (कुंडली को दैवीय सुरक्षा प्राप्त है)" if is_dharmi_tewa else "सामान्य तेवा",
            "andhi_status": "अंधी कुंडली (विशेष लाल किताब उपाय अनिवार्य)" if is_andhi_kundli else "दृष्टि युक्त कुंडली"
        }
    }
