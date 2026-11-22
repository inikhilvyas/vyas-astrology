# Method Registry

Each school is a separate methodology with its own conventions and permitted evidence. First-pass analysis is isolated per method. Mixed use is allowed only in the cross-system step, labelled by origin.

## Contents
Parashari · KP · Jaimini · Nakshatra-Pada · Nadi / BNN · Vargas · Ashtakavarga · Shadbala/Avastha · Dasha systems · Transits · Chakras · Special Lagnas · Aspect geometry · Yoga scanning

## Parashari
- Evaluate: house lords (functional benefic/malefic by lagna), dignity (exalt/debil/moolatrikona/own/friend/enemy), placement, conjunction, graha drishti (7th all; Mars 4/8; Jupiter 5/9; Saturn 3/10; Rahu/Ketu 5/9 = school-dependent, label it), combustion, retrogression, planetary war, dispositor chains, argala, karakas, nakshatra refinement, D9 confirmation, vargottama.
- Yoga verification: name the rule, list conditions, test each against CHART_STATE, test cancellations (e.g. Neecha Bhanga conditions, Kemadruma cancellation), assign status. Naming a yoga because two planets are "connected" is forbidden.
- Strong != benefic: a strong functional malefic strongly delivers its significations.
- House system: whole-sign by default unless the source declares otherwise; say so.

## KP (Krishnamurti Paddhati)
- Own conventions: KP ayanamsha (preserve KP New if the report uses it), Placidus cusps, sub-lord as the decisive layer.
- Chain to evaluate for an event: **Cusp -> star lord -> sub lord -> (sub-sub) -> significators of event houses -> negating houses -> dasha lord chain -> transit/ruling planets.**
- Planet significators in the standard four-level order: planets in the star of occupants of the house; occupants; planets in the star of the lord; lord. Keep the level of each link visible.
- Event houses are event-specific (e.g. marriage commonly 2-7-11; job 2-6-10-11; foreign settlement 3-9-12, with 12 as separation from birthplace; children 2-5-11) with negating houses (e.g. 1-6-10-12 for marriage). These are KP conventions - do not import them into Parashari reasoning.
- Verdict vocabulary: SUPPORTS / DENIES / WEAKENS / UNRESOLVED. A cusp sub-lord that signifies the event houses supports promise; sub-lord signifying negating houses weakens or denies; mixed -> state which dominates and why.
- Use `scripts/vyas_calc.py` for star/sub/sub-sub; heed boundary warnings (sub-lords flip over small arcs; a few arcminutes of birth-time error can change a cusp sub-lord).
- Never stop at "cusp is in sign X": sign is not the KP result.

## Jaimini
- Chara karakas (7- or 8-karaka scheme: declare which), AK, AmK, DK etc.; rashi drishti (movable->fixed except adjacent, fixed->movable except adjacent, dual->other duals); Arudha Lagna, Upapada, A7, A10; Karakamsa; Chara dasha when requested.
- Report as Jaimini conclusions. Do not relabel as Parashari/KP.

## Nakshatra-Pada (refinement layer unless the method makes it primary)
For Lagna, Moon, Sun and each relevant planet: exact degree -> nakshatra -> nakshatra lord (house, sign, condition) -> pada -> navamsha sign -> PADA/NAVAMSHA LORD -> dispositor chain; deity/guna/purushartha where traditionally applicable; tara relationship to Janma nakshatra. A nakshatra reading must not override stronger contradictory foundational evidence without stating why.

## Nadi / Bhrigu Nandi Nadi
Planetary chains, conjunction/trine relations, sequencing, Moon relations, Bhrigu Bindu, transit activation. Every observation carries a source status: TRADITIONAL, TEXTUAL, LINEAGE-SPECIFIC, INTERPRETIVE, EXPERIMENTAL. Unsourced formulas are never attributed to BNN or any historical author.

## Vargas (use only what the question needs, and only if present/verified)
Career D1+D10(+D9); marriage D1+D9(+Upapada); children D1+D7(+D9); wealth D1+D2(+Indu lagna); education D1+D24; property D1+D4; spirituality D1+D20 (+Karakamsa); health D1+D6+D30 (symbolic only). D40/D45/D60 only when technically justified; D60 is highly time-sensitive -> block or downgrade unless birth time is grade A. An unavailable/unverified varga never silently becomes evidence.

## Ashtakavarga
Preserve the source's own method. Thresholds (e.g. SAV 28+, BAV 4+/5+; below 20 weak) are configurable heuristics, not validated cut-offs - say so. For transits: BAV of the transiting planet in the sign + natal promise + dasha. Ashtakavarga alone cannot authorise an event lacking natal promise.

## Shadbala / Avastha
Sthana, Dig, Kala, Cheshta, Naisargika, Drik bala; avasthas as available. Interpret through functional lordship and event relevance.

## Dasha systems
Vimshottari (maha/antar/pratyantar; sookshma/prana only for strongly supported events), Chara (Jaimini), Yogini or others on request. Dasha activates a promise; it cannot create one. State year-length convention.

## Transits
Layer: natal promise -> dasha -> transit (Saturn/Jupiter primary in most traditional timing; Rahu/Ketu/Mars/Sun/Moon/Venus/Mercury as event triggers) -> nakshatra transit -> degree refinement. Contacts: Lagna, Moon, Sun, relevant lords, karakas, Bhrigu Bindu, AK/DK, cusps. A transit alone never guarantees an event. Without a trustworthy ephemeris source and a stated reference date, say transits are unverified - do not quote positions from memory.

## Chakras and special Lagnas
Sarvatobhadra, Sudarshana, Kota, Navadhara, Tara Bala: enhancement layers only, cannot override denial or data uncertainty; declare which chakra method. Arudha/Upapada/Indu/Karakamsa/A7/A10/Ghati: activate only when relevant.

## Aspect geometry
Keep separate: Parashari graha drishti, Jaimini rashi drishti, special aspects, exact angular separation/orb. An orb rule is a geometric overlay unless a source supports it as classical; label experimental orbs as such. Natal vs transit; applying vs separating where meaningful.
