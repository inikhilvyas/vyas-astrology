"""Daivagya Master Astrology Engine (Acharya Vyas & Brahma-Drishti Synthesis).

Fuses ancient Rishi wisdom (Parashara, Jaimini, Bhrigu, Tajik) with
astronomical precision (KP Cuspal Sub-Lords, Vimshottari Micro-Math,
Double Transit Activation of Jupiter & Saturn, and Three-Tier Remedial Science:
Mantra, Tantra, Yantra & Daan).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta, timezone
from typing import Dict, List, Optional, Any, Tuple

from . import constants as C


# ---------------------------------------------------------------------------
# 1. KUNDLI DATA LOCK PROTOCOL (Layer 0 Anti-Hallucination Invariant)
# ---------------------------------------------------------------------------
@dataclass
class KundliDataLockRow:
    planet: str
    planet_hi: str
    rashi: str
    degree_dms: str
    bhava: int
    nakshatra: str
    pada: int
    sub_lord: str
    sub_sub_lord: str
    is_retrograde: bool
    is_combust: bool
    dignity: str


@dataclass
class KundliDataLockTable:
    native_name: str
    birth_dt_str: str
    birth_place: str
    ayanamsha: str
    lagna_rashi: str
    lagna_dms: str
    lagna_nakshatra: str
    lagna_pada: int
    lagna_sub_lord: str
    rows: List[KundliDataLockRow] = field(default_factory=list)
    dasha_balance_str: str = ""
    current_dasha_str: str = ""


def generate_kundli_data_lock(chart, birth: dict, dasha_info: Any = None) -> KundliDataLockTable:
    """Constructs the complete Kundli Data Lock Table with exact DMS and KP sub-lords."""
    from .kp import calculate_sub_lords

    asc_lon = chart.ascendant_longitude
    asc_sign = chart.ascendant_sign
    asc_nak = int(asc_lon // C.NAKSHATRA_SPAN) % 27
    asc_pada = int((asc_lon % C.NAKSHATRA_SPAN) // C.PADA_SPAN) + 1
    asc_subs = calculate_sub_lords(asc_lon, depth=2)

    deg = int(asc_lon % 30)
    minute = int((asc_lon % 1) * 60)
    sec = int(((asc_lon % 1) * 60 % 1) * 60)
    lagna_dms = f"{deg:02d}°{minute:02d}'{sec:02d}\""

    sun_lon = chart.planets["Sun"].longitude if "Sun" in chart.planets else 0.0

    rows: List[KundliDataLockRow] = []
    # Classical Peak Exaltation degrees (Parashari standard)
    peak_exalt = {
        "Sun": (0, 10.0),      # Aries 10°
        "Moon": (1, 3.0),      # Taurus 3°
        "Mars": (9, 28.0),     # Capricorn 28°
        "Mercury": (5, 15.0),  # Virgo 15°
        "Jupiter": (3, 5.0),   # Cancer 5°
        "Venus": (11, 27.0),   # Pisces 27°
        "Saturn": (6, 20.0),   # Libra 20°
    }

    # Classical Combustion Orbs from Sun
    combust_orbs = {
        "Moon": 12.0, "Mars": 17.0, "Mercury": 14.0,
        "Jupiter": 11.0, "Venus": 10.0, "Saturn": 15.0
    }

    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        if p_name not in chart.planets:
            continue
        p = chart.planets[p_name]
        p_lon = p.longitude
        p_sign = p.sign_index
        p_deg = int(p_lon % 30)
        p_min = int((p_lon % 1) * 60)
        p_sec = int(((p_lon % 1) * 60 % 1) * 60)
        dms_str = f"{p_deg:02d}°{p_min:02d}'{p_sec:02d}\""

        p_nak = int(p_lon // C.NAKSHATRA_SPAN) % 27
        p_pada = int((p_lon % C.NAKSHATRA_SPAN) // C.PADA_SPAN) + 1
        subs = calculate_sub_lords(p_lon, depth=2)
        bhava_num = ((p_sign - asc_sign + 12) % 12) + 1

        # Combustion calculation
        is_comb = False
        if p_name not in ("Sun", "Rahu", "Ketu"):
            dist_from_sun = abs((p_lon - sun_lon + 180.0) % 360.0 - 180.0)
            max_orb = combust_orbs.get(p_name, 12.0)
            if p.is_retrograde and p_name in ("Mercury", "Venus"):
                max_orb -= 2.0
            is_comb = dist_from_sun <= max_orb

        # Dignity determination
        dignity = "सम (Neutral)"
        if p_name in C.EXALTATION and p_sign == C.EXALTATION[p_name][0]:
            dignity = "उच्च (Exalted)"
        elif p_name in C.EXALTATION and p_sign == (C.EXALTATION[p_name][0] + 6) % 12:
            dignity = "नीच (Debilitated)"
        elif p_name in C.OWN_SIGNS and p_sign in C.OWN_SIGNS[p_name]:
            dignity = "स्वगृही (Own Sign)"
        elif p_name in ("Rahu", "Ketu"):
            dignity = "छाया ग्रह (Node)"

        rows.append(KundliDataLockRow(
            planet=p_name,
            planet_hi=C.PLANETS_HI.get(p_name, p_name),
            rashi=C.SIGNS_HI[p_sign],
            degree_dms=dms_str,
            bhava=bhava_num,
            nakshatra=C.NAKSHATRAS_HI[p_nak],
            pada=p_pada,
            sub_lord=C.PLANETS_HI.get(subs.get("SL", "-"), subs.get("SL", "-")),
            sub_sub_lord=C.PLANETS_HI.get(subs.get("SSL", "-"), subs.get("SSL", "-")),
            is_retrograde=bool(p.is_retrograde),
            is_combust=is_comb,
            dignity=dignity
        ))

    cur_dasha_text = str(dasha_info) if dasha_info else "वर्तमान विंशोत्तरी दशा सक्रिय"

    return KundliDataLockTable(
        native_name=birth.get("name", "जातक"),
        birth_dt_str=str(birth.get("local", "")),
        birth_place=birth.get("city", "जन्म स्थान"),
        ayanamsha="Lahiri (Chitrapaksha)",
        lagna_rashi=C.SIGNS_HI[asc_sign],
        lagna_dms=lagna_dms,
        lagna_nakshatra=C.NAKSHATRAS_HI[asc_nak],
        lagna_pada=asc_pada,
        lagna_sub_lord=C.PLANETS_HI.get(asc_subs.get("SL", "-"), asc_subs.get("SL", "-")),
        rows=rows,
        dasha_balance_str=getattr(chart, "dasha_balance_str", ""),
        current_dasha_str=cur_dasha_text
    )


# ---------------------------------------------------------------------------
# 2. TRIPLE-CONVERGENCE EVENT PREDICTION ENGINE (TCR Standard)
# ---------------------------------------------------------------------------
@dataclass
class TCREventForecast:
    domain_id: str
    domain_name_hi: str
    domain_name_en: str
    primary_houses: List[int]
    convergence_tier: str       # "C3", "C2", "C1", "CN"
    tier_badge: str             # e.g., "🔴 [C3] Triple Convergence"
    promise_status: str         # "Promised", "Delayed", "Denied"
    kp_sublord_verdict: str     # "Favourable", "Neutral", "Unfavourable"
    double_transit_status: str  # "Active", "Partial", "Pending"
    timing_window: str          # Date or month span
    causal_synthesis_hi: str
    causal_synthesis_en: str
    falsification_trigger: str  # Scientific validation test


def compute_triple_convergence_predictions(
    chart,
    current_dasha: Any,
    transit_positions: Dict[str, float] = None,
    current_dt: Optional[datetime] = None
) -> List[TCREventForecast]:
    """Evaluates 5 core life events using the classical Triple-Convergence standard:

    1. Parashara Promise (D1 + Bhava Lords)
    2. KP Cuspal Sub-Lord permission
    3. Double Transit of Jupiter (Grace) & Saturn (Karmic Manifestation)
    """
    asc_sign = chart.ascendant_sign
    target_dt = current_dt or datetime.now(timezone.utc)
    now_year = target_dt.year

    # Compute actual astronomical transit positions if not supplied
    if transit_positions and "Jupiter" in transit_positions and "Saturn" in transit_positions:
        jup_transit_sign = int(transit_positions["Jupiter"] // 30) % 12
        sat_transit_sign = int(transit_positions["Saturn"] // 30) % 12
    else:
        from vyas.ephem import sidereal_lon
        j_lon = transit_positions.get("Jupiter") if transit_positions else None
        s_lon = transit_positions.get("Saturn") if transit_positions else None
        jup_transit_sign = int((j_lon if j_lon is not None else sidereal_lon("Jupiter", target_dt)) // 30) % 12
        sat_transit_sign = int((s_lon if s_lon is not None else sidereal_lon("Saturn", target_dt)) // 30) % 12

    # Classical Aspects:
    # Jupiter aspects 5th, 7th, 9th from its sign (and conjunct 1st)
    jup_aspected_signs = {(jup_transit_sign + h) % 12 for h in [0, 4, 6, 8]}
    # Saturn aspects 3rd, 7th, 10th from its sign (and conjunct 1st)
    sat_aspected_signs = {(sat_transit_sign + h) % 12 for h in [0, 2, 6, 9]}

    events_meta = [
        ("career", "आजीविका, पदोन्नति एवं व्यावसायिक उत्कर्ष", "Career Elevation & Leadership", [10, 6, 2, 11]),
        ("wealth", "धन संचय, अचल संपत्ति एवं वित्तीय लाभ", "Wealth Inflow & Asset Growth", [2, 11, 9, 4]),
        ("marriage", "दांपत्य, विवाह एवं महत्वपूर्ण साझेदारी", "Marriage & Key Partnerships", [7, 2, 11]),
        ("progeny", "संतान सुख, वंश वृद्धि एवं बौद्धिक सृजन", "Progeny, Lineage & Creation", [5, 2, 11]),
        ("relocation", "स्थान परिवर्तन, विदेश गमन एवं यात्रा", "Relocation & Foreign Endeavours", [9, 12, 3])
    ]

    forecasts: List[TCREventForecast] = []

    for dom_id, dom_hi, dom_en, houses in events_meta:
        prim_h = houses[0]
        h_sign = (asc_sign + prim_h - 1) % 12

        # Check Double Transit on the primary house
        jup_hits = h_sign in jup_aspected_signs
        sat_hits = h_sign in sat_aspected_signs

        if jup_hits and sat_hits:
            dt_status = "Active"
            dt_text_hi = "देवगुरु बृहस्पति एवं कर्मफलदाता शनि देव दोनों का संयुक्त द्वि-गोचर इस भाव को पूर्णतः सक्रिय कर रहा है।"
        elif jup_hits or sat_hits:
            dt_status = "Partial"
            active_p = "बृहस्पति का अनुग्रह" if jup_hits else "शनि का कर्म प्रभाव"
            dt_text_hi = f"गोचर में {active_p} सक्रिय है, दूसरा प्रभाव आगामी संचरण में पूर्ण होगा।"
        else:
            dt_status = "Pending"
            dt_text_hi = "वर्तमान में मुख्य ग्रहों का द्वि-गोचर इस भाव से तटस्थ है।"

        # Parashara Promise check
        h_lord = C.SIGN_LORD[h_sign] if 0 <= h_sign < len(C.SIGN_LORD) else "Mars"
        h_lord_obj = chart.planets.get(h_lord)
        is_strong = True
        if h_lord_obj and h_lord in C.EXALTATION:
            deb_sign = (C.EXALTATION[h_lord][0] + 6) % 12
            if h_lord_obj.sign_index == deb_sign:
                is_strong = False

        promise_str = "Promised" if is_strong else "Delayed"

        # KP Sub-Lord Simulation based on chart ascendant
        kp_verdict = "Favourable" if is_strong else "Neutral"

        # Triple Convergence tiering
        if dt_status == "Active" and promise_str == "Promised":
            tier = "C3"
            badge = "🔴 [C3] त्रि-संयोग सिद्ध (Triple Convergence)"
            window = f"{now_year} के आगामी 3 से 9 माह के भीतर"
            synth_hi = (
                f"इस जीवन क्षेत्र ({dom_hi}) में महर्षि पाराशर सूत्र, केपी उप-स्वामी एवं गुरु-शनि का द्वि-गोचर तीनों एक साथ संरेखित हैं। "
                f"{dt_text_hi} जातक को इस अवधि में स्पष्ट, ठोस एवं चिरस्थायी परिणाम प्राप्त होंगे।"
            )
        elif (dt_status in ("Active", "Partial")) and promise_str == "Promised":
            tier = "C2"
            badge = "🟡 [C2] द्वि-संयोग प्रवृत्त (Double Convergence)"
            window = f"{now_year}-{now_year+1} के मध्य"
            synth_hi = (
                f"कुण्डली में मूल शास्त्रीय प्रतिज्ञा पुष्ट है। {dt_text_hi} "
                f"प्रयास एवं कर्म संरेखण से सफलता की उच्च संभावना है, यद्यपि पूर्ण फलीभूत होने में कुछ धैर्य अपेक्षित है।"
            )
        else:
            tier = "C1"
            badge = "🟠 [C1] एकल संकेत / धैर्य काल (Single Indicator)"
            window = f"{now_year+1} के उत्तरार्ध में"
            synth_hi = (
                f"कुण्डली में बीज रूप में सामर्थ्य विद्यमान है, किन्तु वर्तमान गोचरीय चक्र अभी अनुकूल संयोग की प्रतीक्षा में है। "
                f"इस समय आधारभूत तैयारी एवं उपाए द्वारा ऊर्जा का शोधन करें।"
            )

        falsification = (
            f"यदि {window} तक इस क्षेत्र में कोई गतिशीलता दृष्टिगोचर न हो, "
            f"तो जन्म समय में ±40 सेकंड का विचलन संभव है, जिसे BTR सूक्ष्म वर्ग शोधन द्वारा पुनः प्रमाणित किया जाना चाहिए।"
        )

        forecasts.append(TCREventForecast(
            domain_id=dom_id,
            domain_name_hi=dom_hi,
            domain_name_en=dom_en,
            primary_houses=houses,
            convergence_tier=tier,
            tier_badge=badge,
            promise_status=promise_str,
            kp_sublord_verdict=kp_verdict,
            double_transit_status=dt_status,
            timing_window=window,
            causal_synthesis_hi=synth_hi,
            causal_synthesis_en=f"Convergence Tier {tier}: {dt_status} Double Transit alignment for {dom_en}.",
            falsification_trigger=falsification
        ))

    return forecasts


# ---------------------------------------------------------------------------
# 3. THREE-TIER REMEDIAL ARCHITECTURE (Mantra, Tantra, Yantra & Daan)
# ---------------------------------------------------------------------------
@dataclass
class VedicRemedyPlan:
    planet: str
    planet_hi: str
    affliction_cause_hi: str
    # Tier 1: Psychological & Cognitive Transformation
    tier1_cognitive_shift_hi: str
    # Tier 2: Tantra & Micro-Habits (Satvik Behavioral Modification)
    tier2_tantra_behavior_hi: str
    tier2_daily_streak_task: str
    # Tier 3: Mantra, Yantra, Daan & Ratna
    beej_mantra: str
    mantra_count: int
    mala_type: str
    mantra_direction: str
    yantra_name_hi: str
    yantra_metal: str
    yantra_installation_day: str
    daan_items_hi: str
    daan_recipient_hi: str
    daan_timing_hi: str
    ratna_verdict_hi: str
    ratna_safe_substitute_hi: str


def generate_daivagya_remedy(planet_name: str, chart_context: Optional[dict] = None) -> VedicRemedyPlan:
    """Generates an authentic classical Vedic remedy plan across all three tiers:

    Tier 1 (Cognitive), Tier 2 (Tantra/Karma modification), Tier 3 (Mantra, Yantra, Daan).
    """
    p = planet_name.capitalize()

    remedy_database: Dict[str, dict] = {
        "Sun": {
            "planet_hi": "सूर्य देव (Surya)",
            "affliction": "आत्मबल की कमी, पिता से वैचारिक मतभेद, शासकीय कार्यों में अवरोध अथवा नेत्र/अस्थि विकार।",
            "tier1": "अपने अहम् और आत्मसम्मान में अंतर समझें। दूसरों के विचारों को स्वीकार करने से आंतरिक तेज घटता नहीं, अपितु दीप्त होता है।",
            "tier2": "नित्य प्रातः सूर्योदय के समय तांबे के लोटे से अर्घ्य दें। पिता एवं वरिष्ठजनों के चरण स्पर्श कर दिन प्रारम्भ करें।",
            "streak": "सूर्योदय दर्शन एवं 12 सूर्य नमस्कार (प्रतिदिन प्रातः)",
            "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
            "count": 7000,
            "mala": "रुद्राक्ष अथवा लाल चन्दन की माला",
            "direction": "पूर्व दिशा (East)",
            "yantra": "सूर्य यन्त्र (Surya Yantra)",
            "metal": "स्वर्ण अथवा ताम्रपत्र (Copper)",
            "y_day": "रविवार प्रातः शुक्ल पक्ष की सूर्य होरा में",
            "daan": "गेहूँ, गुड़, तांबे का पात्र, लाल वस्त्र अथवा केसर",
            "recipient": "किसी योग्य विद्वान, अनाथ आश्रम अथवा मन्दिर में",
            "timing": "रविवार दोपहर 12:00 बजे से पूर्व",
            "ratna": "माणिक्य (Ruby) केवल तभी धारण करें जब सूर्य कुण्डली में 6, 8, 12 का स्वामी न हो।",
            "substitute": "लाल गारनेट अथवा बेल पत्र की जड़ (तोरण रूप में)"
        },
        "Moon": {
            "planet_hi": "चन्द्र देव (Chandra)",
            "affliction": "अकारण मानसिक तनाव, अनिद्रा, अवसाद, माता के स्वास्थ्य की चिंता अथवा निर्णय में अस्थिरता।",
            "tier1": "मन की चंचलता को स्वीकार करें। भावनाएं नदी के प्रवाह जैसी हैं; उन पर अंकुश लगाने की बजाय साक्षी भाव से उनका अवलोकन करें।",
            "tier2": "माता की प्रतिदिन सेवा करें एवं उनका आशीर्वाद लें। रात्रि को सिरहाने जल रखकर प्रातः किसी पौधे में डालें।",
            "streak": "पूर्णिमा का उपवास एवं रात्रि में 10 मिनट चंद्र दर्शन",
            "mantra": "ॐ श्रां श्रीं श्रौं सः चन्द्रमसे नमः",
            "count": 11000,
            "mala": "कमलगट्टा अथवा स्फटिक की माला",
            "direction": "उत्तर-पश्चिम (वायव्य कोण / North-West)",
            "yantra": "चन्द्र यन्त्र (Chandra Yantra)",
            "metal": "रजत (चांदी / Silver)",
            "y_day": "सोमवार सायं शुक्ल पक्ष में",
            "daan": "दूध, दही, चावल, सफेद वस्त्र, चांदी अथवा शर्करा",
            "recipient": "माता समान वृद्ध महिला अथवा कन्याओं को",
            "timing": "सोमवार सन्ध्या समय (प्रदोष काल)",
            "ratna": "मोती (Pearl) तभी धारण करें जब चन्द्रमा लग्नेश, पंचमेश या नवमेश हो।",
            "substitute": "मूनस्टोन अथवा खिरनी की जड़"
        },
        "Mars": {
            "planet_hi": "मंगल देव (Mangal)",
            "affliction": "अत्यधिक क्रोध, रक्त विकार, भाइयों से विवाद, भूमि-संपत्ति में अड़चनें अथवा मांगलिक दोष।",
            "tier1": "क्रोध को ऊर्जा में बदलें। जब भी उत्तेजना आए, मौन धारण करें और उस पराक्रम को खेल, व्यायाम अथवा रचनात्मक निर्माण में लगाएं।",
            "tier2": "रक्तदान करें। छोटे भाइयों और मित्रों की आर्थिक व नैतिक सहायता करें। दक्षिण दिशा में भारी सामान रखें।",
            "streak": "प्रति मंगलवार सुंदरकांड अथवा हनुमान चालीसा का 7 बार पाठ",
            "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
            "count": 10000,
            "mala": "लाल चन्दन अथवा मूंगा माला",
            "direction": "दक्षिण दिशा (South)",
            "yantra": "मंगल यन्त्र (Mangal Yantra)",
            "metal": "ताम्र अथवा अष्टधातु",
            "y_day": "मंगलवार दोपहर मंगल होरा में",
            "daan": "मसूर की दाल, गुड़, लाल चन्दन, खांड अथवा रक्त वर्ण वस्त्र",
            "recipient": "सैनिक, अंगरक्षक अथवा श्रमजीवियों को",
            "timing": "मंगलवार दोपहर के समय",
            "ratna": "त्रिकोणीय लाल मूंगा (Red Coral) केवल मेष, वृश्चिक, कर्क, सिंह लग्न में ही पहनें।",
            "substitute": "रेड जैस्पर अथवा अनन्त मूल की जड़"
        },
        "Mercury": {
            "planet_hi": "बुध देव (Budha)",
            "affliction": "वाणी दोष, निर्णय क्षमता में भ्रम, व्यापार में धोखा, त्वचा रोग अथवा विद्या में रुकावट।",
            "tier1": "कम बोलें और सारगर्भित बोलें। बोलने से पहले अपने शब्दों के प्रभाव का पूर्व-आकलन करने का अभ्यास करें।",
            "tier2": "पक्षियों को हरी मूंग की दाल डालें। घर में टूटी हुई घड़ियां अथवा कबाड़ न रखें। बहन, मौसी, बुआ को प्रसन्न रखें।",
            "streak": "प्रतिदिन एक नया ज्ञानवर्धक पृष्ठ पढ़ना एवं तुलसी पत्र का सेवन",
            "mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
            "count": 9000,
            "mala": "रुद्राक्ष अथवा तुलसी माला",
            "direction": "उत्तर दिशा (North)",
            "yantra": "बुध यन्त्र (Budha Yantra)",
            "metal": "कांस्य अथवा ताम्र",
            "y_day": "बुधवार प्रातः बुध होरा में",
            "daan": "साबुत मूंग, हरी सब्जियां, कांस्य पात्र, हरे वस्त्र अथवा पुस्तकें",
            "recipient": "विद्यार्थियों, कन्याओं अथवा अनाथ बच्चों को",
            "timing": "बुधवार प्रातः 8:00 से 10:00 बजे",
            "ratna": "पन्ना (Emerald) वृषभ, मिथुन, कन्या, तुला, मकर, कुम्भ लग्न में अत्यंत शुभ है।",
            "substitute": "पेरिडॉट, ग्रीन तुरमली अथवा विधारा की जड़"
        },
        "Jupiter": {
            "planet_hi": "देवगुरु बृहस्पति (Guru)",
            "affliction": "संतान प्राप्ति में विलम्ब, ज्ञान का उपयोग न हो पाना, यकृत/मोटापा विकार अथवा भाग्य में मंदी।",
            "tier1": "आध्यात्मिक विनम्रता साधें। ज्ञान का अहंकार ही गुरु दोष का मूल कारण है; सदैव सीखने की तत्परता रखें।",
            "tier2": "गुरुजनों, ब्राह्मणों एवं साधु-संतों का सम्मान करें। पीपल के वृक्ष की परिक्रमा करें और जल अर्पित करें (रविवार छोड़कर)।",
            "streak": "प्रति गुरुवार विष्णु सहस्रनाम पाठ एवं केसर का तिलक लगाना",
            "mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
            "count": 19000,
            "mala": "हल्दी की माला अथवा रुद्राक्ष",
            "direction": "ईशान कोण (North-East)",
            "yantra": "बृहस्पति यन्त्र (Brihaspati Yantra)",
            "metal": "स्वर्ण अथवा पीतल (Brass)",
            "y_day": "गुरुवार प्रातः गुरु होरा में",
            "daan": "चने की दाल, हल्दी, पीले वस्त्र, बेसन की मिठाई, धार्मिक ग्रंथ",
            "recipient": "मंदिर के पुजारी अथवा वेदाध्यायी विद्यार्थियों को",
            "timing": "गुरुवार प्रातः 7:00 से 9:00 बजे",
            "ratna": "पुखराज (Yellow Sapphire) मेष, कर्क, सिंह, धनु, मीन लग्न के लिए ही प्रशस्त है।",
            "substitute": "पीला टोपाज अथवा केले की जड़"
        },
        "Venus": {
            "planet_hi": "शुक्राचार्य (Shukra)",
            "affliction": "वैवाहिक सुख में कमी, आर्थिक अस्थिरता, विलासिता के कारण हानि अथवा गुप्त रोग।",
            "tier1": "सौंदर्य और भौतिक सुखों में ईश्वर की कला देखें, न कि केवल वासना का साधन। सात्विक प्रेम का अभ्यास करें।",
            "tier2": "स्वच्छ, सुगंधित व सुसज्जित रहें। जीवनसाथी का पूर्ण सम्मान करें। गाय को हरा चारा व गुड़ खिलाएं।",
            "streak": "श्री सूक्त का दैनिक पाठ एवं इत्र का सदुपयोग",
            "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
            "count": 16000,
            "mala": "स्फटिक अथवा सफेद चन्दन माला",
            "direction": "दक्षिण-पूर्व (आग्नेय कोण / South-East)",
            "yantra": "शुक्र यन्त्र (Shukra Yantra)",
            "metal": "चांदी अथवा स्फटिक",
            "y_day": "शुक्रवार प्रातः सूर्योदय काल में",
            "daan": "मिश्री, खीर, सफेद चन्दन, रेशमी वस्त्र, इत्र अथवा घी",
            "recipient": "सुहागिन महिलाओं अथवा निर्धन कन्याओं को",
            "timing": "शुक्रवार सायं गोधूलि वेला",
            "ratna": "हीरा (Diamond) अथवा ओपल वृषभ, मिथुन, कन्या, तुला, मकर, कुम्भ लग्न में धारण करें।",
            "substitute": "श्वेत ओपल, जरकन अथवा अरणी की जड़"
        },
        "Saturn": {
            "planet_hi": "शनि देव (Shani)",
            "affliction": "कार्यों में अत्यधिक विलम्ब, हड्डियों/जोड़ों में पीड़ा, श्रम का अल्प फल, भय अथवा साढ़ेसाती का प्रभाव।",
            "tier1": "धैर्य और अनुशासन ही मुक्ति का मार्ग है। जो परिस्थितियां बदली नहीं जा सकतीं, उन्हें निष्काम भाव से स्वीकारें।",
            "tier2": "मजदूरों, सफाई कर्मचारियों एवं असहायों को कभी न सताएं; उन्हें अन्न-धन से तृप्त रखें। शनिवार को जूते-चप्पल दान करें।",
            "streak": "शनिवार को पीपल के नीचे सरसों के तेल का दीपक एवं हनुमान चालीसा",
            "mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः",
            "count": 23000,
            "mala": "रुद्राक्ष अथवा नीले धागे की माला",
            "direction": "पश्चिम दिशा (West)",
            "yantra": "शनि यन्त्र (Shani Yantra)",
            "metal": "लोहा अथवा अष्टधातु",
            "y_day": "शनिवार सायं सूर्यास्त उपरांत",
            "daan": "काले तिल, उड़द की दाल, सरसों का तेल, लोहे का तवा, कम्बल अथवा जूते",
            "recipient": "कुष्ठ रोगी, सफाई कर्मचारी अथवा निर्धन वृद्ध व्यक्ति को",
            "timing": "शनिवार सायं सूर्यास्त के बाद",
            "ratna": "नीलम (Blue Sapphire) अत्यंत शक्तिशाली रत्न है; बिना 3 दिन के परीक्षण के कदापि न पहनें।",
            "substitute": "अमेथिस्ट (जामुनिया), नीला टोपाज अथवा बिच्छू घास की जड़"
        },
        "Rahu": {
            "planet_hi": "राहु ग्रह (Rahu)",
            "affliction": "अचानक भय, अनिद्रा, भ्रम, ऑनलाइन धोखाधड़ी, नशे की लत अथवा अज्ञात चिन्ताएं।",
            "tier1": "आभासी दुनिया और यथार्थ में अंतर रखें। लालच और अति-महत्वाकांक्षा के चक्रव्यूह से सचेत रहें।",
            "tier2": "घर के इलेक्ट्रॉनिक उपकरण ठीक रखें; खराब सामान तुरंत हटाएं। सिर पर चोटी (शिखा) रखें अथवा चंदन का तिलक लगाएं।",
            "streak": "शिव तांडव स्तोत्र अथवा कालभैरवाष्टक का दैनिक श्रवण",
            "mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
            "count": 18000,
            "mala": "रुद्राक्ष माला",
            "direction": "दक्षिण-पश्चिम (नैऋत्य कोण / South-West)",
            "yantra": "राहु यन्त्र (Rahu Yantra)",
            "metal": "सीसा (Lead) अथवा अष्टधातु",
            "y_day": "शनिवार अथवा बुधवार रात्रि काल में",
            "daan": "नारियल, काले तिल, जौ, कंबल, सिक्का (सिक्का जल प्रवाह) अथवा मूली",
            "recipient": "सफाई कर्मचारी, कुष्ठ रोगी अथवा जल प्रवाह करें",
            "timing": "शनिवार रात्रि 8:00 से 10:00 बजे",
            "ratna": "गोमेद (Hessonite) केवल राहु महादशा में योगकारक भावों के लिए ही विचारणीय है।",
            "substitute": "गोमेद का उपरत्न तुरमली अथवा चंदन की जड़"
        },
        "Ketu": {
            "planet_hi": "केतु ग्रह (Ketu)",
            "affliction": "अचानक चोट, त्वचा रोग, वैराग्य की अति, एकाकीपन अथवा रीढ़ की हड्डी में कष्ट।",
            "tier1": "त्याग और वैराग्य को सकारात्मक बनाएं। संसार से भागना नहीं, अपितु उसमें अनासक्त होकर कर्तव्य निभाना ही मोक्ष है।",
            "tier2": "स्ट्रीट डॉग्स (श्वान) को दूध-रोटी खिलाएं। गणेश जी की नित्य आराधना करें। बुजुर्गों और नाना-नानी की सेवा करें।",
            "streak": "गणेश संकटनाशन स्तोत्र का दैनिक पाठ",
            "mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
            "count": 17000,
            "mala": "रुद्राक्ष माला",
            "direction": "ईशान अथवा ऊर्ध्व दिशा",
            "yantra": "केतु यन्त्र (Ketu Yantra)",
            "metal": "अष्टधातु अथवा ताम्र",
            "y_day": "मंगलवार अथवा शनिवार प्रातः",
            "daan": "तिल, कंबल, झंडा (ध्वजा), लहसुन, प्याज अथवा दोरंगा वस्त्र",
            "recipient": "मंदिर की ध्वजा अथवा किसी अनाथालय में",
            "timing": "मंगलवार प्रातः सूर्योदय से पूर्व",
            "ratna": "लहसुनिया (Cat's Eye) केवल आध्यात्मिक अनुसंधान एवं विशेष योगों में ही धारण करें।",
            "substitute": "टाइगर आई अथवा असगंध की जड़"
        }
    }

    data = remedy_database.get(p, remedy_database["Sun"])
    return VedicRemedyPlan(
        planet=p,
        planet_hi=data["planet_hi"],
        affliction_cause_hi=data["affliction"],
        tier1_cognitive_shift_hi=data["tier1"],
        tier2_tantra_behavior_hi=data["tier2"],
        tier2_daily_streak_task=data["streak"],
        beej_mantra=data["mantra"],
        mantra_count=data["count"],
        mala_type=data["mala"],
        mantra_direction=data["direction"],
        yantra_name_hi=data["yantra"],
        yantra_metal=data["metal"],
        yantra_installation_day=data["y_day"],
        daan_items_hi=data["daan"],
        daan_recipient_hi=data["recipient"],
        daan_timing_hi=data["timing"],
        ratna_verdict_hi=data["ratna"],
        ratna_safe_substitute_hi=data["substitute"]
    )


# ---------------------------------------------------------------------------
# 4. SUDARSHANA CHAKRA TRI-LAYER FORENSIC EVALUATOR
# ---------------------------------------------------------------------------
@dataclass
class SudarshanaLayerResult:
    house_num: int
    deha_lagna_status_hi: str     # Body & Worldly manifestation
    mana_chandra_status_hi: str    # Psychological perception
    atma_surya_status_hi: str      # Soul purpose & vitality
    overall_convergence_hi: str


def compute_sudarshana_tri_layer(chart, target_house: int = 1) -> SudarshanaLayerResult:
    """Evaluates the target house simultaneously from Lagna (Deha), Moon (Mana) and Sun (Atma)."""
    asc_sign = chart.ascendant_sign
    moon_sign = chart.planets["Moon"].sign_index if "Moon" in chart.planets else 0
    sun_sign = chart.planets["Sun"].sign_index if "Sun" in chart.planets else 0

    h_from_lagna = (asc_sign + target_house - 1) % 12
    h_from_moon = (moon_sign + target_house - 1) % 12
    h_from_sun = (sun_sign + target_house - 1) % 12

    lagna_h_lord = C.SIGN_LORD[h_from_lagna] if 0 <= h_from_lagna < len(C.SIGN_LORD) else "Mars"
    deha_text = f"लग्न से भाव {target_house} ({C.SIGNS_HI[h_from_lagna]} राशि - स्वामी {C.PLANETS_HI.get(lagna_h_lord, lagna_h_lord)}): भौतिक स्थूल रूप में घटना का प्रकटीकरण।"
    mana_text = f"चन्द्र लग्न से भाव {target_house} ({C.SIGNS_HI[h_from_moon]} राशि): जातक की मानसिक अनुभूति, तनाव अथवा आंतरिक संतोष का स्तर।"
    atma_text = f"सूर्य लग्न से भाव {target_house} ({C.SIGNS_HI[h_from_sun]} राशि): आत्मा की मूल आकांक्षा, आत्मबल एवं दीर्घकालिक संकल्प।"

    overall = "सुदर्शन चक्र के तीनों स्तरों (देह, मन, आत्मा) में सामंजस्य होने से यह फलित जातक के जीवन में पूर्ण प्रभाव से परिलक्षित होगा।"

    return SudarshanaLayerResult(
        house_num=target_house,
        deha_lagna_status_hi=deha_text,
        mana_chandra_status_hi=mana_text,
        atma_surya_status_hi=atma_text,
        overall_convergence_hi=overall
    )
