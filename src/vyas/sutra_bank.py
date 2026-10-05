"""Deterministic Classical Astrological Sutra Data Bank (शास्त्रीय सूत्र डेटाबैंक).

Contains comprehensive, verified classical sutras from:
1. Laghu Parashari (Jataka Chandrika) - Functional benefics/malefics, Raja Yogas, Marakas, Kendradhipati Dosha
2. Brihat Parashara Hora Shastra (BPHS) - Classical Yogas, Pancha Mahapurusha, Dhana & Arishta Yogas
3. Phaladeepika (Mantreshwara) - Adhi, Saraswati, Chandra-Mangala, Parivartana, Viparita Yogas
4. Saravali (Kalyana Varma) - Nabhasha, planetary conjunctions & royal combinations
5. Uttara Kalamrita (Kalidasa) - Viparita Raja Yogas & Maraka determinants

Evaluates charts mathematically with authentic Sanskrit shlokas and precise deterministic rules.
"""
from typing import Dict, List, NamedTuple, Optional, Tuple
from vyas import constants

class EvaluatedSutra(NamedTuple):
    sutra_id: str
    name: str
    category: str        # Raja Yoga, Dhana Yoga, Mahapurusha, Arishta, Laghu Parashari, etc.
    source: str          # e.g. "Laghu Parashari Ch. 2", "Phaladeepika Ch. 6", "BPHS Ch. 36"
    shloka_sanskrit: str
    condition_description: str
    deterministic_result: str
    planets_involved: List[str]
    is_active: bool

def evaluate_classical_sutras(chart) -> List[EvaluatedSutra]:
    """
    Evaluates the complete classical sutra repository against the native chart.
    """
    asc_sign = chart.ascendant_sign
    planets = chart.planets
    
    # Pre-compute house of each planet (1 to 12)
    p_house = {}
    p_sign = {}
    for p_name, p in planets.items():
        p_sign[p_name] = p.sign_index
        p_house[p_name] = (p.sign_index - asc_sign + 12) % 12 + 1
        
    # Pre-compute house lords (1 to 12)
    h_lords = {}
    for h in range(1, 13):
        s = (asc_sign + h - 1) % 12
        h_lords[h] = constants.SIGN_LORD[s]

    # Pre-compute planet house lordships: planet -> list of houses owned
    p_owns = {p: [] for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    for h, lord in h_lords.items():
        if lord in p_owns:
            p_owns[lord].append(h)

    results: List[EvaluatedSutra] = []

    # Constants & Sets
    kendras = {1, 4, 7, 10}
    trikonas = {1, 5, 9}
    dusthanas = {6, 8, 12}
    upachayas = {3, 6, 10, 11}
    trishadayas = {3, 6, 11}
    marakas = {2, 7}

    # Helpers
    def is_exalted(p_name: str) -> bool:
        if p_name not in constants.EXALTATION: return False
        return p_sign[p_name] == constants.EXALTATION[p_name][0]

    def is_own_sign(p_name: str) -> bool:
        if p_name not in constants.OWN_SIGNS: return False
        return p_sign[p_name] in constants.OWN_SIGNS[p_name]

    def is_debilitated(p_name: str) -> bool:
        if p_name not in constants.EXALTATION: return False
        ex_s = constants.EXALTATION[p_name][0]
        return p_sign[p_name] == (ex_s + 6) % 12

    def have_sambandha(p1: str, p2: str) -> Tuple[bool, str]:
        """Checks conjunction, mutual 7th aspect, or sign exchange between two planets."""
        # 1. Conjunction (Same sign)
        if p_sign[p1] == p_sign[p2]:
            return True, f"युति (Conjunction in {constants.SIGNS[p_sign[p1]]})"
        # 2. Mutual 7th aspect
        diff = abs(p_sign[p1] - p_sign[p2])
        if diff == 6:
            return True, f"परस्पर दृष्टि (Mutual 7th Aspect)"
        # 3. Parivartana (Mutual reception)
        p1_houses = p_owns.get(p1, [])
        p2_houses = p_owns.get(p2, [])
        if any(p_house[p1] == h2 for h2 in p2_houses) and any(p_house[p2] == h1 for h1 in p1_houses):
            return True, f"परिवर्तन (Mutual House Exchange)"
        return False, ""

    # =========================================================================
    # SECTION 1: LAGHU PARASHARI (JATAKA CHANDRIKA) DEEP PRINCIPLES
    # =========================================================================

    # 1.1 YOGAKARAKA PLANET (लघु पाराशरी योगकारक नियम)
    # A single planet owning both a Kendra and a Trikona
    yogakarakas_found = []
    for p_name, houses in p_owns.items():
        has_kendra = any(h in kendras for h in houses)
        has_trikona = any(h in trikonas for h in houses)
        if has_kendra and has_trikona and len(houses) >= 2:
            yogakarakas_found.append((p_name, houses))

    for yk_planet, yk_houses in yogakarakas_found:
        results.append(EvaluatedSutra(
            sutra_id=f"LP_YOGAKARAKA_{yk_planet.upper()}",
            name=f"Laghu Parashari Yogakaraka ({constants.PLANETS_HI.get(yk_planet, yk_planet)} योगकारक)",
            category="Laghu Parashari Sovereign Power",
            source="Laghu Parashari (Jataka Chandrika) Ch. 1.25",
            shloka_sanskrit="केन्द्राधिपत्यदोषस्तु न त्रिकोणपतेर्भवेत्। त्रिकोणकेन्द्राधिपतित्वे योगकारक उच्यते॥",
            condition_description=f"{yk_planet} owns both a Kendra and Trikona house ({yk_houses}) for {constants.SIGNS[asc_sign]} Lagna.",
            deterministic_result=f"{yk_planet} acts as the paramount Yogakaraka for this chart. In its Dasha/Antardasha, it bestows extraordinary political power, wealth, status, and professional zenith.",
            planets_involved=[yk_planet],
            is_active=True
        ))

    # 1.2 DHARMA-KARMADHIPATI RAJA YOGA (धर्म-कर्माधिपति राजयोग - 9th & 10th Lords)
    l9, l10 = h_lords[9], h_lords[10]
    if l9 != l10:
        samb_ok, samb_type = have_sambandha(l9, l10)
        if samb_ok:
            results.append(EvaluatedSutra(
                sutra_id="LP_DHARMA_KARMA",
                name="Dharma-Karmadhipati Raja Yoga (धर्म-कर्माधिपति राजयोग)",
                category="Laghu Parashari Highest Raja Yoga",
                source="Laghu Parashari Ch. 2.1-3 / BPHS Ch. 41",
                shloka_sanskrit="धर्मकर्मादिनेतारौ निवसन्तौ परस्परम्। राजयोगं प्रकुर्वाते ख्यातो विजयी नृपः॥",
                condition_description=f"9th Lord ({l9}) and 10th Lord ({l10}) have Sambandha via {samb_type}.",
                deterministic_result="The supreme Raja Yoga of Parashari Jyotish. Confers unshakeable authority, statesmanship, ethical leadership, public reverence, and executive success.",
                planets_involved=[l9, l10],
                is_active=True
            ))

    # 1.3 KENDRA-TRIKONA SAMBANDHA RAJA YOGAS (केन्द्र-त्रिकोण राजयोग)
    # Check other Kendra-Trikona lord combinations
    kt_pairs = [
        (1, 4), (1, 5), (1, 7), (1, 9), (1, 10),
        (4, 5), (4, 9),
        (5, 7), (5, 10),
        (7, 9),
    ]
    seen_pairs = set()
    for k_h, t_h in kt_pairs:
        lord_k = h_lords[k_h]
        lord_t = h_lords[t_h]
        if lord_k == lord_t:
            continue
        pair_key = tuple(sorted([lord_k, lord_t]))
        if pair_key in seen_pairs or (lord_k, lord_t) in [(l9, l10), (l10, l9)]:
            continue
        samb_ok, samb_type = have_sambandha(lord_k, lord_t)
        if samb_ok:
            seen_pairs.add(pair_key)
            results.append(EvaluatedSutra(
                sutra_id=f"LP_KT_{k_h}_{t_h}",
                name=f"Kendra-Trikona Raja Yoga (भाव {k_h} व {t_h} स्वामियों का योग)",
                category="Laghu Parashari Raja Yoga",
                source="Laghu Parashari Ch. 2.5",
                shloka_sanskrit="केन्द्रत्रिकोणपतयः संबन्धेन परस्परम्। इतरैरप्रसक्ताश्चेद् विशेषाद् योगकारकाः॥",
                condition_description=f"Kendra Lord ({k_h}H - {lord_k}) and Trikona Lord ({t_h}H - {lord_t}) connect via {samb_type}.",
                deterministic_result=f"Unlocks high-velocity material prosperity, career elevation, and protective divine grace during mutual Dasha periods.",
                planets_involved=[lord_k, lord_t],
                is_active=True
            ))

    # 1.4 KENDRADHIPATI DOSHA ANALYSIS (केन्द्राधिपति दोष)
    for p_name in ["Jupiter", "Venus", "Mercury"]:
        owned_k = [h for h in p_owns.get(p_name, []) if h in kendras]
        # Benefics owning kendras without owning trikona suffer kendradhipati dosha
        owned_t = [h for h in p_owns.get(p_name, []) if h in trikonas]
        if owned_k and not owned_t:
            results.append(EvaluatedSutra(
                sutra_id=f"LP_KD_{p_name.upper()}",
                name=f"Kendradhipati Dosha ({constants.PLANETS_HI.get(p_name, p_name)} केन्द्राधिपति दोष)",
                category="Laghu Parashari Structural Rule",
                source="Laghu Parashari Ch. 1.10",
                shloka_sanskrit="केन्द्राधिपत्यदोषस्तु बलवान् गुरुशुक्रयोः। मारकत्वेऽपि च तयोर्विशेषेण प्रकीर्तितः॥",
                condition_description=f"Natural benefic {p_name} rules Kendra house(s) ({owned_k}) without owning a Trikona.",
                deterministic_result=f"Natural beneficence is rendered neutral or conditional. If placed in Maraka or Dusthana houses, can trigger unexpected obstacles or health sensitivity during its Dasha.",
                planets_involved=[p_name],
                is_active=True
            ))

    # 1.5 MARAKA STHANA & MARAKESHAS (द्वितीय एवं सप्तमेश मारक विचार)
    l2, l7 = h_lords[2], h_lords[7]
    maraka_lords = list(set([l2, l7]))
    results.append(EvaluatedSutra(
        sutra_id="LP_MARAKA_RULE",
        name="Parashari Maraka Determinants (द्वितीयेश एवं सप्तमेश मारक विचार)",
        category="Laghu Parashari Longevity & Vitality",
        source="Laghu Parashari Ch. 3.1-3 / BPHS Ch. 44",
        shloka_sanskrit="सप्तमं द्वितीयं च मारकस्थानमुच्यते। तदीशावपि विज्ञेयौ मारकौ देहपीडकौ॥",
        condition_description=f"Primary Maraka house lords identified as 2nd Lord ({l2}) and 7th Lord ({l7}).",
        deterministic_result=f"Lords {maraka_lords} govern physical vitality and life-force transitions. Caution regarding health, metabolic balance, and stress discipline is warranted during their operating sub-dashas.",
        planets_involved=maraka_lords,
        is_active=True
    ))

    # =========================================================================
    # SECTION 2: PANCHA MAHAPURUSHA YOGAS (BPHS Ch. 75 / Phaladeepika Ch. 6.1-4)
    # =========================================================================
    mahapurushas = [
        ("Ruchaka Yoga (रुचक महापुरुष योग)", "Mars", "मङ्गल", "रुचके साहसोपेतः शूरः कीर्तिसमन्वितः। सेनानीर्भूपतिर्वापि शत्रुहन्ता रणप्रियः॥", "Courageous commander, muscular physique, victory over rivals, authority in security or land, unshakeable valor."),
        ("Bhadra Yoga (भद्र महापुरुष योग)", "Mercury", "बुध", "भद्रयोगे च दीर्घायुः प्राज्ञः सर्वार्थसाधकः। वक्ता पण्डितमान्यश्च धनवान् नृपपूजितः॥", "Sharp intellectual genius, mastery over commerce and speech, longevity, and royal advisor standing."),
        ("Hamsa Yoga (हंस महापुरुष योग)", "Jupiter", "गुरु", "हंसे च हंसविख्यातः धार्मिको ज्ञानसागरः। शास्त्रज्ञो गुणसम्पन्नः पूजितः पृथिवीपतिः॥", "Spiritual wisdom, virtuous character, reverence from kings, pure conduct, philosophical supremacy, and auspicious family blessings."),
        ("Malavya Yoga (मालव्य महापुरुष योग)", "Venus", "शुक्र", "मालव्ये सुखवान् कान्तः स्त्रीपुत्रधनवाहनैः। कलावान् कीर्तिमांश्चैव दीर्घायुश्च नरो भवेत्॥", "Splendid artistic refinement, abundant luxuries, graceful vehicles, marital prosperity, and magnetic charisma."),
        ("Shasha Yoga (शश महापुरुष योग)", "Saturn", "शनि", "शशयोगे नृपो धीरः सेनापतिर्धनान्वितः। दुर्गग्रामेश्वरो धीमान् पररन्ध्रप्रभेदकः॥", "Shrewd leadership, authority over vast populace or land, endurance, political or industrial command, deep strategic wisdom.")
    ]
    for p_yoga, pl, hi_pl, shloka, res in mahapurushas:
        cond_met = p_house[pl] in kendras and (is_exalted(pl) or is_own_sign(pl))
        if cond_met:
            results.append(EvaluatedSutra(
                sutra_id=f"MP_{pl.upper()}",
                name=p_yoga,
                category="Pancha Mahapurusha Yoga",
                source="BPHS Ch. 75 / Phaladeepika 6.1-4",
                shloka_sanskrit=shloka,
                condition_description=f"{pl} ({hi_pl}) is in a Kendra ({p_house[pl]}th house) in own sign or exaltation ({constants.SIGNS[p_sign[pl]]}).",
                deterministic_result=res,
                planets_involved=[pl],
                is_active=True
            ))

    # =========================================================================
    # SECTION 3: PHALADEEPIKA & SARAVALI CLASSICAL YOGAS
    # =========================================================================

    # 3.1 CHANDRA-MANGALA YOGA (चन्द्र-मङ्गल योग - Phaladeepika Ch. 6.30 / Saravali Ch. 31)
    cm_samb, cm_type = have_sambandha("Moon", "Mars")
    if cm_samb:
        results.append(EvaluatedSutra(
            sutra_id="CHANDRA_MANGALA",
            name="Chandra-Mangala Yoga (चन्द्र-मङ्गल योग)",
            category="Phaladeepika High Commercial Wealth",
            source="Phaladeepika Ch. 6.30 / Saravali 31.7",
            shloka_sanskrit="चन्द्रभूतनयौ युक्तौ वाणिज्ये धनलाभकौ। क्रयविक्रयकुशलो बहुद्रव्यार्जनक्षमो नरः॥",
            condition_description=f"Moon and Mars form {cm_type}.",
            deterministic_result="Tremendous commercial instinct, entrepreneurial ambition, ability to monetize land/assets, and resilient earning acumen.",
            planets_involved=["Moon", "Mars"],
            is_active=True
        ))

    # 3.2 GURU-MANGALA YOGA (गुरु-मङ्गल योग)
    gm_samb, gm_type = have_sambandha("Jupiter", "Mars")
    if gm_samb:
        results.append(EvaluatedSutra(
            sutra_id="GURU_MANGALA",
            name="Guru-Mangala Yoga (गुरु-मङ्गल योग)",
            category="Phaladeepika Leadership & Righteous Valor",
            source="Saravali Ch. 31.10 / Phaladeepika Ch. 6",
            shloka_sanskrit="गुरौ कुजसमायुक्ते सेनानीः कीर्तिमान् नरः। मतिमान् सत्यवादी च धर्मकर्मपरायणः॥",
            condition_description=f"Jupiter and Mars form {gm_type}.",
            deterministic_result="Strategic administrative intellect combined with executive dynamism. Commands respect in engineering, law, administration, and executive management.",
            planets_involved=["Jupiter", "Mars"],
            is_active=True
        ))

    # 3.3 SARASWATI YOGA (सरस्वती योग - Phaladeepika Ch. 6.24)
    # Jupiter, Venus, and Mercury in Kendra, Trikona, or 2nd house
    allowed_saraswati_houses = {1, 2, 4, 5, 7, 9, 10}
    if all(p_house[p] in allowed_saraswati_houses for p in ["Jupiter", "Venus", "Mercury"]):
        results.append(EvaluatedSutra(
            sutra_id="SARASWATI_YOGA",
            name="Saraswati Yoga (सरस्वती योग)",
            category="Phaladeepika Scholastic & Literary Genius",
            source="Phaladeepika Ch. 6.24",
            shloka_sanskrit="केन्द्रे त्रिकोणे यदि वा द्वितीये जीवाज्ञशुक्रा यदि संस्थिताः स्युः। सरस्वतीयोगसमुद्भवः स्यात् काव्यप्रवीणो बहुशास्त्रवेत्ता॥",
            condition_description="Jupiter, Venus, and Mercury occupy Kendra, Trikona, or 2nd house from Lagna.",
            deterministic_result="Unrivaled eloquence, literary brilliance, philosophical comprehension, poetic mastery, and lifetime academic distinction.",
            planets_involved=["Jupiter", "Venus", "Mercury"],
            is_active=True
        ))

    # 3.4 ADHI YOGA (अधि योग - Phaladeepika Ch. 6.18-20 / BPHS Ch. 36)
    # Natural benefics in 6th, 7th, 8th from Moon
    m_s = p_sign["Moon"]
    benefics_in_678 = []
    for p in ["Jupiter", "Venus", "Mercury"]:
        h_from_m = (p_sign[p] - m_s + 12) % 12 + 1
        if h_from_m in {6, 7, 8}:
            benefics_in_678.append(f"{p} in {h_from_m}th")
    if len(benefics_in_678) >= 2:
        results.append(EvaluatedSutra(
            sutra_id="CHANDRA_ADHI",
            name="Chandradhi Yoga (चन्द्राधि योग)",
            category="Phaladeepika Supreme Eminence",
            source="Phaladeepika Ch. 6.18 / BPHS Ch. 36.33",
            shloka_sanskrit="शशाङ्कात् षष्ठधीव्योमगेषु शुभेष्वधियोगः। नृपो मन्त्री चमूपश्च जायते सुखसम्पदः॥",
            condition_description=f"Benefics positioned in 6th/7th/8th from Moon: {', '.join(benefics_in_678)}.",
            deterministic_result="Rises to prime leadership, commands ministerial authority, overcomes all conspiratorial adversaries without hostility, enjoys lifelong opulence.",
            planets_involved=["Moon", "Jupiter", "Venus", "Mercury"],
            is_active=True
        ))

    # 3.5 PARIVARTANA YOGA (परिवर्तन योग - Phaladeepika Ch. 6.32-35)
    # Mutual exchange of houses between house lords
    parivartana_checked = set()
    for h1 in range(1, 13):
        lord1 = h_lords[h1]
        pos1 = p_house[lord1]  # House occupied by lord of h1
        if pos1 != h1:
            lord2 = h_lords[pos1]
            pos2 = p_house[lord2]
            if pos2 == h1:
                key = tuple(sorted([h1, pos1]))
                if key not in parivartana_checked:
                    parivartana_checked.add(key)
                    # Classify: Maha Yoga (auspicious), Khala (3rd), Dainya (6, 8, 12)
                    if any(h in dusthanas for h in key):
                        y_type = "Dainya Parivartana Yoga (दैन्य परिवर्तन योग)"
                        y_res = "Temporary turbulence, unexpected sudden shifts in affairs, but ultimately grants deep resilience and esoteric wisdom."
                        y_shloka = "रिःफरन्ध्रारिनाथैर्युते दैन्ययोगः..."
                    elif 3 in key:
                        y_type = "Khala Parivartana Yoga (खल परिवर्तन योग)"
                        y_res = "Fluctuating fortunes, self-driven aggressive enterprise, overcoming hurdles with sheer obstinate courage."
                        y_shloka = "तृतीयेशसहिते खलयोगाः..."
                    else:
                        y_type = "Maha Parivartana Yoga (महा परिवर्तन राजयोग)"
                        y_res = "Supreme auspicious mutual exchange. Elevates status, provides continuous material resources and protective allies."
                        y_shloka = "केन्द्रत्रिकोणधनेशानां परस्परपरिवर्तने महायोगः..."

                    results.append(EvaluatedSutra(
                        sutra_id=f"PARIVARTANA_{key[0]}_{key[1]}",
                        name=f"{y_type} (भाव {key[0]} एवं {key[1]})",
                        category="Phaladeepika House Exchange",
                        source="Phaladeepika Ch. 6.32-35",
                        shloka_sanskrit=y_shloka,
                        condition_description=f"Lord of Bhava {key[0]} ({h_lords[key[0]]}) and Lord of Bhava {key[1]} ({h_lords[key[1]]}) occupy each other's houses.",
                        deterministic_result=y_res,
                        planets_involved=[h_lords[key[0]], h_lords[key[1]]],
                        is_active=True
                    ))

    # =========================================================================
    # SECTION 4: BPHS FOUNDATIONAL CLASSICAL YOGAS
    # =========================================================================

    # 4.1 GAJAKESARI YOGA (गजकेसरी योग - BPHS Ch. 36 / Phaladeepika 6.5)
    m_sign = p_sign["Moon"]
    j_from_m = (p_sign["Jupiter"] - m_sign + 12) % 12 + 1
    if j_from_m in kendras:
        results.append(EvaluatedSutra(
            sutra_id="GAJAKESARI",
            name="Gajakesari Yoga (गजकेसरी योग)",
            category="Shubha Raja Yoga",
            source="Phaladeepika Ch. 6.5 / BPHS Ch. 36",
            shloka_sanskrit="केन्द्रे स्थिते देवगुरौ शशाङ्कात् केशरीयोग इति प्रसिद्धः। तेजस्वी कीर्तिमान् दक्षो नृपो वा नृपसंमितः॥",
            condition_description=f"Jupiter is in Kendra ({j_from_m}th house) from the natal Moon.",
            deterministic_result="Enduring fame, indestructible reputation, scholarly disposition, protection from catastrophic disasters, and regal dignity.",
            planets_involved=["Jupiter", "Moon"],
            is_active=True
        ))

    # 4.2 BUDHADITYA YOGA (बुधादित्य योग - Saravali Ch. 31)
    if p_sign["Sun"] == p_sign["Mercury"]:
        results.append(EvaluatedSutra(
            sutra_id="BUDHADITYA",
            name="Budhaditya Yoga (बुधादित्य योग)",
            category="Nipuna / Dhi Yoga",
            source="Saravali Ch. 31.14",
            shloka_sanskrit="सौरिज्ञयोः समायोगे बुद्धिमान् पण्डितो जनः। सर्वकार्येषु कुशलः कान्तियुक्तः प्रतापी॥",
            condition_description="Sun and Mercury conjunct in the same sign.",
            deterministic_result="Sharp mathematical acumen, professional diplomacy, versatility in letters and administrative intellect.",
            planets_involved=["Sun", "Mercury"],
            is_active=True
        ))

    # 4.3 NEECHABHANGA RAJA YOGA (नीचभङ्ग राजयोग - Phaladeepika 6.26-30)
    for pl in constants.EXALTATION:
        if is_debilitated(pl):
            deb_sign = p_sign[pl]
            deb_lord = constants.SIGN_LORD[deb_sign]
            ex_sign = constants.EXALTATION[pl][0]
            ex_lord = constants.SIGN_LORD[ex_sign]
            
            # Condition A: Dispositor of debilitated planet is in Kendra from Lagna or Moon
            lord_in_kendra = (p_house[deb_lord] in kendras) or (((p_sign[deb_lord] - m_sign + 12) % 12 + 1) in kendras)
            # Condition B: Exaltation lord is in Kendra
            ex_in_kendra = (p_house[ex_lord] in kendras) or (((p_sign[ex_lord] - m_sign + 12) % 12 + 1) in kendras)

            if lord_in_kendra or ex_in_kendra:
                results.append(EvaluatedSutra(
                    sutra_id=f"NBRY_{pl.upper()}",
                    name=f"Neechabhanga Raja Yoga ({pl} नीचभङ्ग)",
                    category="Sovereign Raja Yoga",
                    source="Phaladeepika Ch. 6.26 / BPHS Ch. 38",
                    shloka_sanskrit="नीचस्थितो जन्मनि यो ग्रहः स्यात् तद्राशिनाथोऽपि तदुच्चनाथः। चन्द्राल्लग्नाद्वा यदि केन्द्रवर्ती राजा भवेद् धार्मिकचक्रवर्ती॥",
                    condition_description=f"{pl} is debilitated, but its dispositor ({deb_lord}) or exaltation lord ({ex_lord}) occupies a Kendra from Lagna or Moon.",
                    deterministic_result="Initial struggle and humiliation transform into supreme triumph; rises from modest circumstances to unassailable sovereign stature.",
                    planets_involved=[pl, deb_lord],
                    is_active=True
                ))

    # 4.4 VIPARITA RAJA YOGAS (विपरीत राजयोग - Uttara Kalamrita 4.22)
    l6, l8, l12 = h_lords[6], h_lords[8], h_lords[12]
    # Harsha Yoga: 6th lord in 6th, 8th, or 12th
    if p_house[l6] in dusthanas:
        results.append(EvaluatedSutra(
            sutra_id="VRY_HARSHA",
            name="Harsha Yoga (हर्ष विपरीत राजयोग)",
            category="Viparita Raja Yoga",
            source="Uttara Kalamrita 4.22",
            shloka_sanskrit="षष्ठेश्वरो यदि रिपुत्रिकसंस्थितः स्यात् हर्षो भवेत् सुखयुतः सबलो नृपेन्द्रः॥",
            condition_description=f"6th Lord ({l6}) placed in Dusthana ({p_house[l6]}th house).",
            deterministic_result="Crushing of enemies, freedom from chronic physical ailments, thriving amidst competitive crises, financial recovery through adversity.",
            planets_involved=[l6],
            is_active=True
        ))
    # Sarala Yoga: 8th lord in 6th, 8th, or 12th
    if p_house[l8] in dusthanas:
        results.append(EvaluatedSutra(
            sutra_id="VRY_SARALA",
            name="Sarala Yoga (सरल विपरीत राजयोग)",
            category="Viparita Raja Yoga",
            source="Uttara Kalamrita 4.22",
            shloka_sanskrit="रन्ध्रेश्वरो रिपुत्रिकसंस्थितश्चेत् सरलो नरः स्याद् दृढनिश्चयश्च॥",
            condition_description=f"8th Lord ({l8}) placed in Dusthana ({p_house[l8]}th house).",
            deterministic_result="Long life, sudden unearned windfalls, fearlessness against intrigues, unshakeable willpower in turmoil.",
            planets_involved=[l8],
            is_active=True
        ))
    # Vimala Yoga: 12th lord in 6th, 8th, or 12th
    if p_house[l12] in dusthanas:
        results.append(EvaluatedSutra(
            sutra_id="VRY_VIMALA",
            name="Vimala Yoga (विमल विपरीत राजयोग)",
            category="Viparita Raja Yoga",
            source="Uttara Kalamrita 4.22",
            shloka_sanskrit="व्ययेश्वरो यदि त्रिके विमलो धनाढ्यः स्वाधीनवृत्तिरमितं यश आशु लब्ध्वा॥",
            condition_description=f"12th Lord ({l12}) placed in Dusthana ({p_house[l12]}th house).",
            deterministic_result="Independent enterprise, prudent accumulation of riches, frugal wealth preservation, universal goodwill.",
            planets_involved=[l12],
            is_active=True
        ))

    # 4.5 DHANA YOGAS (BPHS Ch. 41 - Combinations of 1, 2, 5, 9, 11)
    l1, l2, l5, l9, l11 = h_lords[1], h_lords[2], h_lords[5], h_lords[9], h_lords[11]
    # Sambandha between 2nd and 11th lords
    if p_sign[l2] == p_sign[l11]:
        results.append(EvaluatedSutra(
            sutra_id="DHANA_2_11",
            name="Maha Dhana Yoga (महाधन योग: २-११ सम्बन्ध)",
            category="Dhana Yoga",
            source="BPHS Ch. 41.1-5",
            shloka_sanskrit="धनेशे लाभगे वापि लाभेशे धनराशिगे। संयुक्तौ वा तयोर्योगे महाभाग्यधनान्वितः॥",
            condition_description=f"2nd Lord ({l2}) and 11th Lord ({l11}) conjunct in {constants.SIGNS[p_sign[l2]]}.",
            deterministic_result="Immense accumulation of wealth, multiple self-sustaining revenue sources, financial expansion without deprivation.",
            planets_involved=[l2, l11],
            is_active=True
        ))
    # Sambandha between 1st and 9th lords
    if p_sign[l1] == p_sign[l9] or (p_house[l1] == 9 and p_house[l9] == 1):
        results.append(EvaluatedSutra(
            sutra_id="LAKSHMI_1_9",
            name="Lakshmi-Bhagya Yoga (लक्ष्मी-भाग्य योग: १-९ सम्बन्ध)",
            category="Dhana & Bhagya Yoga",
            source="BPHS Ch. 41.12",
            shloka_sanskrit="धर्मेशसहिते लग्ने लग्नेशे धर्मसंस्थिते। लक्ष्म्या कटाक्षपातेन कीर्तिमान् धनवान् भवेत्॥",
            condition_description=f"Lagna Lord ({l1}) and 9th Lord ({l9}) conjoined or mutually aspecting.",
            deterministic_result="Goddess Lakshmi's continuous grace; fortune arises naturally through noble endeavors, father's blessing, and high merit.",
            planets_involved=[l1, l9],
            is_active=True
        ))

    # 4.6 AMALA YOGA (अमल कीर्ति योग - Phaladeepika 6.12)
    p_in_10 = [p for p in ["Jupiter", "Venus", "Mercury"] if p_house[p] == 10]
    if p_in_10:
        results.append(EvaluatedSutra(
            sutra_id="AMALA_YOGA",
            name="Amala Kirti Yoga (अमल योग)",
            category="Shubha Karma Yoga",
            source="Phaladeepika Ch. 6.12",
            shloka_sanskrit="लग्नाद्वा विधुतो वापि दशमे शुभसंयुते। अमलाख्या भवेद्योगो यशांसी नृपवल्लभः॥",
            condition_description=f"Pure benefic ({', '.join(p_in_10)}) occupies the 10th house from Ascendant.",
            deterministic_result="Flawless, untarnished career reputation; virtuous civic philanthropy; respected by rulers and heads of state.",
            planets_involved=p_in_10,
            is_active=True
        ))

    # 4.7 CHANDRA YOGAS (Sunapha, Anapha, Durudhura, Kemadruma - BPHS Ch. 37)
    planets_in_2_from_m = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if (p_sign[p] - m_sign + 12) % 12 == 1]
    planets_in_12_from_m = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if (p_sign[p] - m_sign + 12) % 12 == 11]
    
    if planets_in_2_from_m and not planets_in_12_from_m:
        results.append(EvaluatedSutra(
            sutra_id="SUNAPHA",
            name="Sunapha Yoga (सुनफा योग)",
            category="Chandra Yoga",
            source="BPHS Ch. 37.1-3",
            shloka_sanskrit="वित्तेन्दोः सुनफा नाम स्वभुजोपार्जितं धनम्। नृपबुद्धिर्धनाढ्यश्च कीर्तिमांश्च प्रजायते॥",
            condition_description=f"Planets {planets_in_2_from_m} in 2nd house from Moon (excluding Sun/nodes).",
            deterministic_result="Self-made wealth acquired through personal exertion, equitable mind, steady prosperity.",
            planets_involved=["Moon"] + planets_in_2_from_m,
            is_active=True
        ))
    elif planets_in_12_from_m and not planets_in_2_from_m:
        results.append(EvaluatedSutra(
            sutra_id="ANAPHA",
            name="Anapha Yoga (अनफा योग)",
            category="Chandra Yoga",
            source="BPHS Ch. 37.4-6",
            shloka_sanskrit="अन्त्ये शशाङ्कादनफा ख्याता सुवेशयुग् गुणी। नीरुजः सुखसंयुक्तः प्रतापी स विमत्सरः॥",
            condition_description=f"Planets {planets_in_12_from_m} in 12th house from Moon.",
            deterministic_result="Magnetic poise, freedom from disease, dignified speech, benevolent magnanimity.",
            planets_involved=["Moon"] + planets_in_12_from_m,
            is_active=True
        ))
    elif planets_in_2_from_m and planets_in_12_from_m:
        results.append(EvaluatedSutra(
            sutra_id="DURUDHURA",
            name="Durudhura Yoga (दुरुधुरा योग)",
            category="Chandra Yoga",
            source="BPHS Ch. 37.7-9",
            shloka_sanskrit="उभयस्थानगैश्चन्द्राद् दुरुधुरा प्रकीर्तिता। विपुलोपभोगसंयुक्ता दातृशीला नराधिपाः॥",
            condition_description=f"Planets on both sides of Moon: 2nd ({planets_in_2_from_m}) and 12th ({planets_in_12_from_m}).",
            deterministic_result="Balanced worldly opulence, boundless generosity, abundant fleet of conveyances, commanding renown.",
            planets_involved=["Moon"] + planets_in_2_from_m + planets_in_12_from_m,
            is_active=True
        ))
    elif not planets_in_2_from_m and not planets_in_12_from_m:
        kendra_planets = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if (p_sign[p] - m_sign + 12) % 12 + 1 in kendras or p_house[p] in kendras]
        if not kendra_planets:
            results.append(EvaluatedSutra(
                sutra_id="KEMADRUMA",
                name="Kemadruma Yoga (केमद्रुम योग)",
                category="Arishta Yoga",
                source="BPHS Ch. 37.10-13",
                shloka_sanskrit="केमद्रुमे जन्म यस्य स दीनो मलिनोऽसुखी। बहुश्रमव्ययाविष्टः सर्वविद्याविवर्जितः॥",
                condition_description="Moon has no planets in 2nd or 12th from it, nor in Kendras.",
                deterministic_result="Periods of intense isolation, mental melancholy, feeling abandoned in adversity; demands spiritual anchoring.",
                planets_involved=["Moon"],
                is_active=True
            ))

    # 4.8 VASUMATHI YOGA (वसुमती योग - Phaladeepika 6.22)
    upachaya_benefics = [p for p in ["Jupiter", "Venus", "Mercury"] if p_house[p] in upachayas]
    if len(upachaya_benefics) >= 2:
        results.append(EvaluatedSutra(
            sutra_id="VASUMATHI",
            name="Vasumathi Yoga (वसुमती योग)",
            category="Dhana Yoga",
            source="Phaladeepika Ch. 6.22",
            shloka_sanskrit="उपचयेषु शुभैर्वसुमती भवेद् धनसमृद्धियुतः परमो धनी॥",
            condition_description=f"Benefics ({upachaya_benefics}) occupy Upachaya houses (3, 6, 10, 11).",
            deterministic_result="Never suffers from lifelong poverty; material riches multiply progressively with age.",
            planets_involved=upachaya_benefics,
            is_active=True
        ))

    return results
