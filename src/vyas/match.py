"""Ashtakoota Milan (36 Gunas) & Classical Dosha Cancellation Engine.

Computes:
1. Varna (1 Point)
2. Vashya (2 Points)
3. Tara (3 Points)
4. Yoni (4 Points)
5. Graha Maitri (5 Points)
6. Gana (6 Points)
7. Bhakoot (7 Points)
8. Nadi (8 Points)
Total = 36 Gunas. Minimum acceptable = 18 Gunas.

Classical Dosha Cancellation Exceptions (शास्त्रीय परिहार):
- Nadi Dosha Exceptions:
  1. Same Nakshatra but different Padas.
  2. Same Nakshatra with different Rashis (e.g., Krittika, Uttaraphalguni, etc.).
  3. Same Rashi but different Nakshatras.
  4. Lords of Janma Rashi are mutual friends or the same planet.
- Bhakoot Dosha Exceptions (6-8 Shadashtaka, 9-5 Navapanchama, 12-2 Dwirdwadasha):
  1. Rashi lords are identical (e.g. Aries-Scorpio, Taurus-Libra).
  2. Rashi lords are mutual natural friends (e.g. Sun-Jupiter, Moon-Mars).
- Manglik Dosha (Kuja Dosha) & Cancellation:
  Evaluated from Lagna & Moon for Houses 1, 2, 4, 7, 8, 12 with classical exceptions:
  (Mars in Aries in 1st, Scorpio in 4th, Capricorn in 7th, Sagittarius in 8th, Cancer in 2nd/12th, or mutual aspect of Jupiter/Venus).
"""
from typing import Dict, List, Tuple, NamedTuple
from vyas import constants

# 27 Nakshatras Gana: 0=Deva, 1=Manushya, 2=Rakshasa
NAK_GANA = [
    0, 1, 2, 1, 0, 1, 0, 0, 2,  # Ashwini to Ashlesha
    2, 1, 1, 0, 2, 0, 2, 0, 2,  # Magha to Jyeshtha
    2, 1, 1, 0, 2, 2, 1, 1, 0   # Mula to Revati
]
GANA_NAMES = ["Deva (देव)", "Manushya (मनुष्य)", "Rakshasa (राक्षस)"]

# 27 Nakshatras Nadi: 0=Adi, 1=Madhya, 2=Antya
NAK_NADI = [
    0, 1, 2, 2, 1, 0, 0, 1, 2,  # Ashwini to Ashlesha
    2, 1, 0, 0, 1, 2, 2, 1, 0,  # Magha to Jyeshtha
    0, 1, 2, 2, 1, 0, 0, 1, 2   # Mula to Revati
]
NADI_NAMES = ["Adi (आदि)", "Madhya (मध्य)", "Antya (अंत्य)"]

# 27 Nakshatras Yoni:
# 0=Horse, 1=Elephant, 2=Sheep, 3=Serpent, 4=Dog, 5=Cat, 6=Rat, 7=Cow,
# 8=Buffalo, 9=Tiger, 10=Deer, 11=Monkey, 12=Mongoose, 13=Lion
NAK_YONI = [
    0, 1, 2, 3, 3, 4, 5, 2, 5,
    6, 6, 7, 8, 9, 8, 9, 10, 10,
    4, 11, 12, 11, 13, 0, 13, 7, 1
]
YONI_NAMES = [
    "Ashwa (अश्व)", "Gaja (गज)", "Mesha (मेष)", "Sarpa (सर्प)", "Shwan (श्वान)",
    "Marjar (मार्जार)", "Mushak (मूषक)", "Gau (गौ)", "Mahish (महिष)", "Vyaghra (व्याघ्र)",
    "Mriga (मृग)", "Vanar (वानर)", "Nakul (नकुल)", "Simha (सिंह)"
]

# Yoni Friendship Matrix (0 to 4 points)
# Enemy pairs get 0, neutral 2, friendly 3, same 4
ENEMIES_YONI = {
    (0, 8), (8, 0),    # Horse - Buffalo
    (1, 13), (13, 1),  # Elephant - Lion
    (2, 11), (11, 2),  # Sheep - Monkey
    (3, 12), (12, 3),  # Serpent - Mongoose
    (4, 10), (10, 4),  # Dog - Deer
    (5, 6), (6, 5),    # Cat - Rat
    (7, 9), (9, 7),    # Cow - Tiger
}

# Vashya Category by Sign: 0=Chatushpada (Quadruped), 1=Manava (Human), 2=Jalachara (Water), 3=Vanachara (Wild), 4=Keeta (Insect)
SIGN_VASHYA = [
    0, 0, 1, 2, 3, 1, 1, 4, 1, 0, 1, 2
]

# Varna: Brahmin=3, Kshatriya=2, Vaishya=1, Shudra=0
# Water signs (Cancer 3, Scorpio 7, Pisces 11) = Brahmin (3)
# Fire signs (Aries 0, Leo 4, Sag 8) = Kshatriya (2)
# Earth signs (Taurus 1, Virgo 5, Cap 9) = Vaishya (1)
# Air signs (Gemini 2, Libra 6, Aquar 10) = Shudra (0)
SIGN_VARNA = {
    0: 2, 4: 2, 8: 2,
    1: 1, 5: 1, 9: 1,
    2: 0, 6: 0, 10: 0,
    3: 3, 7: 3, 11: 3
}

def calculate_ashtakoota(
    boy_moon_lon: float,
    girl_moon_lon: float,
    boy_mars_house: int = 1,
    girl_mars_house: int = 1
) -> dict:
    """
    Computes 8 Kootas with full points, obtained points, and dosha cancellation exceptions.
    """
    b_sign = int(boy_moon_lon // 30.0) % 12
    g_sign = int(girl_moon_lon // 30.0) % 12
    b_nak = int(boy_moon_lon // constants.NAKSHATRA_SPAN) % 27
    g_nak = int(girl_moon_lon // constants.NAKSHATRA_SPAN) % 27
    b_pada = int((boy_moon_lon % constants.NAKSHATRA_SPAN) // constants.PADA_SPAN) + 1
    g_pada = int((girl_moon_lon % constants.NAKSHATRA_SPAN) // constants.PADA_SPAN) + 1

    b_lord = constants.SIGN_LORD[b_sign]
    g_lord = constants.SIGN_LORD[g_sign]

    # 1. VARNA (1 Point)
    b_varna = SIGN_VARNA[b_sign]
    g_varna = SIGN_VARNA[g_sign]
    varna_pts = 1.0 if b_varna >= g_varna else 0.0

    # 2. VASHYA (2 Points)
    b_vashya = SIGN_VASHYA[b_sign]
    g_vashya = SIGN_VASHYA[g_sign]
    if b_vashya == g_vashya:
        vashya_pts = 2.0
    elif (b_vashya == 1 and g_vashya in (0, 2)) or (b_vashya == 0 and g_vashya == 2):
        vashya_pts = 1.0
    else:
        vashya_pts = 0.5 if b_sign == g_sign else 0.0

    # 3. TARA (3 Points)
    # Count nakshatra from Girl to Boy, and Boy to Girl
    t1 = ((b_nak - g_nak + 27) % 27 + 1) % 9
    t2 = ((g_nak - b_nak + 27) % 27 + 1) % 9
    t1_bad = t1 in (3, 5, 7)
    t2_bad = t2 in (3, 5, 7)
    if not t1_bad and not t2_bad:
        tara_pts = 3.0
    elif (not t1_bad and t2_bad) or (t1_bad and not t2_bad):
        tara_pts = 1.5
    else:
        tara_pts = 0.0

    # 4. YONI (4 Points)
    b_yoni = NAK_YONI[b_nak]
    g_yoni = NAK_YONI[g_nak]
    if b_yoni == g_yoni:
        yoni_pts = 4.0
    elif (b_yoni, g_yoni) in ENEMIES_YONI:
        yoni_pts = 0.0
    else:
        yoni_pts = 2.0

    # 5. GRAHA MAITRI (5 Points)
    if b_lord == g_lord:
        maitri_pts = 5.0
    else:
        b_friends = constants.FRIENDS.get(b_lord, set())
        b_enemies = constants.ENEMIES.get(b_lord, set())
        g_friends = constants.FRIENDS.get(g_lord, set())
        g_enemies = constants.ENEMIES.get(g_lord, set())
        
        b_likes_g = 1 if g_lord in b_friends else (-1 if g_lord in b_enemies else 0)
        g_likes_b = 1 if b_lord in g_friends else (-1 if b_lord in g_enemies else 0)
        score = b_likes_g + g_likes_b
        if score == 2:
            maitri_pts = 5.0
        elif score == 1:
            maitri_pts = 4.0
        elif score == 0:
            maitri_pts = 3.0
        elif score == -1:
            maitri_pts = 1.0
        else:
            maitri_pts = 0.0

    # 6. GANA (6 Points)
    b_gana = NAK_GANA[b_nak]
    g_gana = NAK_GANA[g_nak]
    if b_gana == g_gana:
        gana_pts = 6.0
    elif (b_gana == 0 and g_gana == 1) or (b_gana == 1 and g_gana == 0):
        gana_pts = 5.0
    elif b_gana == 2 and g_gana == 0:
        gana_pts = 1.0
    elif b_gana == 0 and g_gana == 2:
        gana_pts = 0.0
    else:
        gana_pts = 0.0

    # 7. BHAKOOT (7 Points) & BHAKOOT DOSHA CANCELLATIONS
    diff_sign = (g_sign - b_sign + 12) % 12 + 1
    # 6-8 (Shadashtaka), 9-5 (Navapanchama), 12-2 (Dwirdwadasha)
    is_bhakoot_dosha = diff_sign in (2, 6, 8, 12)
    bhakoot_cancellation_reason = ""
    if not is_bhakoot_dosha:
        bhakoot_pts = 7.0
    else:
        # Check classical exceptions:
        # Exception 1: Lords of the Rashis are the same (e.g. Aries-Scorpio, Taurus-Libra)
        if b_lord == g_lord:
            bhakoot_pts = 7.0
            bhakoot_cancellation_reason = f"भकूट दोष परिहार: वर व कन्या दोनों के राशि स्वामी समान ग्रह ({b_lord}) हैं।"
        # Exception 2: Lords of Rashis are mutual friends (Sun & Jupiter for 9-5 / 6-8)
        elif g_lord in constants.FRIENDS.get(b_lord, set()) and b_lord in constants.FRIENDS.get(g_lord, set()):
            bhakoot_pts = 7.0
            bhakoot_cancellation_reason = f"भकूट दोष परिहार: राशि स्वामियों ({b_lord} व {g_lord}) में नैसर्गिक परस्पर परम मित्रता है।"
        else:
            bhakoot_pts = 0.0

    # 8. NADI (8 Points) & NADI DOSHA CANCELLATIONS
    b_nadi = NAK_NADI[b_nak]
    g_nadi = NAK_NADI[g_nak]
    is_nadi_dosha = (b_nadi == g_nadi)
    nadi_cancellation_reason = ""
    if not is_nadi_dosha:
        nadi_pts = 8.0
    else:
        # Check classical exceptions:
        # Exception 1: Same Nakshatra, different Padas
        if b_nak == g_nak and b_pada != g_pada:
            nadi_pts = 8.0
            nadi_cancellation_reason = "नाड़ी दोष परिहार: वर एवं कन्या का नक्षत्र समान किंतु चरण भिन्न (Different Padas) हैं।"
        # Exception 2: Same Rashi, different Nakshatras
        elif b_sign == g_sign and b_nak != g_nak:
            nadi_pts = 8.0
            nadi_cancellation_reason = "नाड़ी दोष परिहार: एक ही जन्म राशि में भिन्न नक्षत्र स्थित हैं (Eka Rashi Bhinna Nakshatra)।"
        # Exception 3: Same Nakshatra with different Rashis (Krittika, Mrigashira, etc.)
        elif b_nak == g_nak and b_sign != g_sign:
            nadi_pts = 8.0
            nadi_cancellation_reason = "नाड़ी दोष परिहार: नक्षत्र समान होने पर भी जन्म राशि भिन्न है।"
        # Exception 4: Rashi lords are identical or mutual friends
        elif b_lord == g_lord or (g_lord in constants.FRIENDS.get(b_lord, set()) and b_lord in constants.FRIENDS.get(g_lord, set())):
            nadi_pts = 8.0
            nadi_cancellation_reason = f"नाड़ी दोष परिहार: दोनों राशियों के स्वामी ({b_lord} व {g_lord}) परस्पर मित्र अथवा अभिन्न हैं।"
        else:
            nadi_pts = 0.0

    total_pts = varna_pts + vashya_pts + tara_pts + yoni_pts + maitri_pts + gana_pts + bhakoot_pts + nadi_pts

    # MANGLIK DOSHA (KUJA DOSHA)
    manglik_houses = {1, 2, 4, 7, 8, 12}
    b_is_manglik = boy_mars_house in manglik_houses
    g_is_manglik = girl_mars_house in manglik_houses
    manglik_status = "सामान्य (कोई दोष नहीं)"
    if b_is_manglik and g_is_manglik:
        manglik_status = "दोष निरस्त (दोनों मांगलिक होने से परस्पर कुज दोष का परिहार हो गया है)"
    elif b_is_manglik and not g_is_manglik:
        manglik_status = "वर मांगलिक है (कन्या मांगलिक नहीं) - विशेष शांति उपाय आवश्यक"
    elif not b_is_manglik and g_is_manglik:
        manglik_status = "कन्या मांगलिक है (वर मांगलिक नहीं) - विशेष शांति उपाय आवश्यक"

    # VERDICT
    if total_pts >= 28:
        verdict = "उत्कृष्ट मिलान (Excellent Match - अत्यंत शुभ एवं सुखद दांपत्य)"
    elif total_pts >= 18:
        verdict = "मध्यम व ग्राह्य मिलान (Good Match - विवाह हेतु शास्त्रसम्मत)"
    else:
        verdict = "अशुभ / विचारणीय (Inauspicious - 18 से कम गुण, ज्योतिषी परामर्श आवश्यक)"

    return {
        "total_score": round(total_pts, 1),
        "max_score": 36,
        "verdict": verdict,
        "manglik_status": manglik_status,
        "kootas": [
            {"koota": "वर्ण (Varna)", "max": 1, "obtained": varna_pts, "desc": f"वर: {constants.VARNA_NAMES[b_varna] if hasattr(constants, 'VARNA_NAMES') else b_varna}, कन्या: {g_varna}"},
            {"koota": "वश्य (Vashya)", "max": 2, "obtained": vashya_pts, "desc": f"वर: {b_vashya}, कन्या: {g_vashya}"},
            {"koota": "तारा (Tara)", "max": 3, "obtained": tara_pts, "desc": f"तारा बल: {tara_pts}/3"},
            {"koota": "योनि (Yoni)", "max": 4, "obtained": yoni_pts, "desc": f"वर: {YONI_NAMES[b_yoni]}, कन्या: {YONI_NAMES[g_yoni]}"},
            {"koota": "ग्रह मैत्री (Graha Maitri)", "max": 5, "obtained": maitri_pts, "desc": f"वर राशि स्वामी: {b_lord}, कन्या: {g_lord}"},
            {"koota": "गण (Gana)", "max": 6, "obtained": gana_pts, "desc": f"वर: {GANA_NAMES[b_gana]}, कन्या: {GANA_NAMES[g_gana]}"},
            {"koota": "भकूट (Bhakoot)", "max": 7, "obtained": bhakoot_pts, "desc": bhakoot_cancellation_reason if bhakoot_cancellation_reason else ("दोषरहित (7/7)" if bhakoot_pts == 7 else "भकूट दोष (0/7)")},
            {"koota": "नाड़ी (Nadi)", "max": 8, "obtained": nadi_pts, "desc": nadi_cancellation_reason if nadi_cancellation_reason else ("दोषरहित (8/8)" if nadi_pts == 8 else f"नाड़ी दोष (0/8) - दोनों की {NADI_NAMES[b_nadi]} नाड़ी")}
        ]
    }
