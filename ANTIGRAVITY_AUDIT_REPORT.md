# VYAS Project - Complete Audit Report

Date: 18 November 2026
Project: `G:\software\simpa\VYAS`
Audience: Google Antigravity / project maintainer

## Executive Summary

Project compile-level checks pass, but astrology accuracy is not production-safe. The largest problem is not UI: the astronomical calculation layer uses approximations while claiming Swiss Ephemeris-compatible accuracy. Prediction logic then converts incomplete/double-counted indicators into high-confidence deterministic claims.

Recommended sequence:

1. Fix authoritative astronomical calculations.
2. Normalize timezone handling.
3. Remove silent/frozen transit fallbacks.
4. Rework prediction confidence and contradiction handling.
5. Add independent reference tests.
6. Clean generated/vendor files only after confirming runtime dependencies.

No core astrology source file was modified during this audit.

## Validation Performed

### Passed

- Python compilation for tracked Python files.
- JavaScript syntax checks for tracked JavaScript files.
- JSON/JSONL validation.
- `scripts/test_in_node.js` Node smoke checks.
- `scripts/test_all_mobile_tabs.js`.
- `scripts/test_modal_and_kundli_creation.js`: 25/25.
- `scripts/test_tab_renders.js` after DOM mock correction.
- `.venv311` dependency check: `pip check` passed.
- `tests/test_engine_golden.py`.
- `tests/test_kp_and_chakras.py`.
- `tests/test_daivagya_engine.py` with `PYTHONPATH=src`.
- Combined targeted pytest result: 36 passed.
- `scripts/test_precision_math.py`.
- `scripts/test_kp_math.py`.
- `scripts/compare_ephemeris.py`.

### Test limitation

Existing astrology tests mostly test internal consistency and expected shapes. They do not sufficiently prove correctness against an independent Swiss Ephemeris reference across dates, timezones, boundary degrees, and historical ranges.

Direct execution of `tests/test_daivagya_engine.py` without project path setup fails with:

```text
ModuleNotFoundError: No module named 'vyas'
```

Test runner/package configuration should make `src` importable consistently.

# Critical Astrology Findings

## P1 - Lahiri ayanamsha is an approximation, not Swiss Ephemeris

File: `src/vyas/ephem.py`

Relevant code: `_AYANAMSA_J2000`, `_AYANAMSA_RATE`, `ayanamsa_deg()`.

The module documentation claims Swiss Ephemeris-compatible Lahiri ayanamsha, but implementation uses a fixed linear rate plus a small nutation approximation. Independent `pyswisseph` comparison:

| Date | Difference from Swiss |
|---|---:|
| 1900-01-01 | about -21.8 arcsec |
| 1956-03-21 | about -0.1 arcsec |
| 2000-01-01 | about -14.1 arcsec |
| 2020-01-01 | about -9.4 arcsec |
| 2050-01-01 | about +33.6 arcsec |
| 2100-01-01 | about +39.7 arcsec |

Impact:

- Nakshatra/pada can change near boundaries.
- KP sub-lords can change.
- D60 can change.
- Divisional charts can change.
- Dasha start balance can change.
- Historical/future charts are not consistently reliable.

Required fix:

- Use Swiss Ephemeris directly for Lahiri/KP/Raman if licensing/dependency policy permits.
- Otherwise clearly label the result as an approximation and prohibit boundary-sensitive claims.
- Add multi-date golden tests against Swiss output.

## P1 - True lunar node calculation is materially inaccurate

File: `src/vyas/ephem.py`

`true_node_tropical()` uses a shortened periodic model. Comparison against Swiss true node showed errors approximately 0.08-0.39 degrees in tested dates.

Impact:

- Rahu/Ketu sign, nakshatra, pada, KP sub-lord, and transit timing can be wrong.
- Node-sensitive predictions can flip near boundaries.

Required fix:

- Use Swiss `TRUE_NODE` directly or validate a complete high-precision model.
- Keep mean and true node selection explicit in chart metadata and reports.

## P1 - Ascendant is historically unreliable

File: `src/vyas/ephem.py`

The ascendant is close for modern test dates but diverged by about 9.3 arcminutes for a 1900 test chart against Swiss calculation.

Impact:

- Lagna sign boundary may change.
- Whole-sign houses may change.
- House lordships, yogas, dashas, and predictions can change.

Required fix:

- Compare sidereal ascendant directly against Swiss across 1800-2100.
- Investigate sidereal time, precession, ayanamsha, and historical Skyfield/Swiss time handling.
- Add latitude edge cases and date-range tests.

## P1 - Timezone semantics are inconsistent

Files:

- `src/vyas/ephem.py`
- `src/vyas/dasha.py`
- `src/vyas/gochar.py`

`ephem.py` rejects naive datetimes, while `dasha.py`, `gochar.py`, and transit helpers silently attach UTC or a supplied offset.

Risk:

- Same birth input can mean different instants in different modules.
- Dasha boundaries and ascendant can shift significantly.
- Daylight-saving locations are not safely represented by a fixed `tz_hours` value.

Required fix:

- Accept one canonical timezone-aware instant internally.
- Accept IANA timezone names for birth locations where possible.
- Reject ambiguous/naive input at the public boundary.
- Convert once to UTC; pass aware UTC internally.
- Add IST, US DST, half-hour offset, and date-boundary tests.

## P1 - Silent hard-coded transit fallback

File: `src/vyas/chatbot.py:228-235`

When ephemeris lookup fails, fallback positions for 2026 are injected silently.

Impact:

- User receives apparently precise but stale/wrong transit data.
- Failure is hidden from the user and from downstream prediction logic.

Required fix:

- Remove hard-coded planetary fallback.
- Return an explicit calculation error or clearly marked unavailable status.
- If fallback is required for offline mode, version it, timestamp it, expose it, and never present it as live astronomy.

## P1 - Approximate transit fallback in Daivagya engine

File: `src/vyas/daivagya_engine.py:191-199`

If transit positions are not supplied, Jupiter and Saturn signs are approximated using year arithmetic.

Impact:

- Double-transit status can be wrong for months.
- Timing predictions can be wrong even when natal chart is correct.

Required fix:

- Always calculate actual transit positions for target timestamp.
- Do not infer sign from calendar year.
- If ephemeris unavailable, mark status unavailable rather than approximate silently.

# Prediction Engine Findings

## P1 - C3 confidence is rule-count based and overconfident

File: `src/vyas/predictive_engine.py:71-104`

Career C3 is promoted mainly when at least two career houses are active and Jupiter transit is favourable. This does not adequately require:

- Natal promise.
- Strength of house lords.
- Benefic/malefic condition.
- Dasha lord dignity.
- Contradictory houses.
- Combustion/retrogression/context.
- D10 confirmation.
- Independent timing confirmation.

`d60_ben` is calculated but not used as a gate for the career C3 branch.

Required fix:

- Separate natal promise, event potential, and event timing.
- Require independent evidence from D1 + relevant varga + dasha + transit.
- Penalize contradictions.
- Do not use the same planet/house evidence multiple times under different labels.
- Make C3 unavailable when calculation quality or birth-time confidence is low.

## P1 - Confidence percentage is arbitrary

File: `src/vyas/prashna.py:342`

Current formula clamps confidence to 75-96% after multiplying score by 1.1. This is not calibrated against historical outcomes.

Impact:

- Weak readings look statistically certain.
- Users cannot distinguish symbolic interpretation from validated probability.

Required fix:

- Replace percentage with evidence grades unless a calibration dataset exists.
- If percentages remain, calibrate using held-out historical cases and report methodology.
- Never force a minimum confidence such as 75%.

## P1 - Generic deterministic language overstates certainty

File: `src/vyas/astrosage_content.py`

Several generated texts use guarantee/destiny language such as “guarantees”, “destined”, and fixed wealth/status claims without chart-specific evidence.

Required fix:

- Replace with conditional language.
- Tie every strong claim to visible chart factors.
- Add a disclaimer that astrology output is interpretive and not guaranteed.
- Avoid financial, health, legal, and relationship certainty claims.

## P2 - Transit favourability is too shallow

File: `src/vyas/gochar.py:116-144`

Favourability is largely determined by house and Vedha. Exact degree, natal condition, dasha relevance, retrograde station, and domain-specific promise are not sufficiently integrated.

Required fix:

- Return raw transit facts separately from interpretation.
- Let prediction layer combine transit with natal and dasha evidence.
- Avoid treating a generic favourable transit as an event guarantee.

## P2 - Evidence double-counting risk

Files:

- `src/vyas/predictive_engine.py`
- `src/vyas/kp.py`
- `src/vyas/forensic_predictor.py`
- `src/vyas/daivagya_engine.py`

The same house, planet, or transit can appear as KP significator, D60 evidence, transit evidence, and TCR evidence. Current logic does not demonstrate independence between these signals.

Required fix:

- Define evidence groups.
- Cap contribution from correlated indicators.
- Log each factor once with source and weight.
- Add contradiction and missing-data penalties.

# Jyotishi-Style Reasoning and Prediction Development Blueprint

## Objective

The engine must not behave like a rule-counting machine. It should behave like a disciplined Jyotishi: first establish what the chart actually promises, then judge strength and condition, then identify the dasha capable of delivering the promise, then use transit and secondary systems only for timing and confirmation. A favourable transit, one yoga, one KP significator, or one divisional-chart placement must never become a standalone prediction.

This is an interpretive astrology engine, not a scientifically guaranteed forecasting system. The implementation must therefore be precise about calculations, explicit about the tradition being used, transparent about evidence, and conservative when the chart is uncertain.

## Research Basis and Rule Governance

Use primary or authoritative technical references for calculations, then separately document the chosen Jyotish interpretation. Do not copy contradictory rules into one hidden formula.

- Swiss Ephemeris documentation: `https://www.astro.com/swisseph/swisseph.htm` for ephemeris access, Julian dates, sidereal modes, ayanamsha, nodes, sidereal time, ascendant, and house calculations.
- Brihat Parashara Hora Shastra reference text: `https://archive.org/stream/ParasharaHoraSastra/BrihatParasharaHoraSastraVedicAstrologyEbook_djvu.txt` for varga significance, Shadbala/Vimshopaka concepts, Vimshottari structure, time divisions, and classical house/planet results.
- Parashari/Jaimini chapter map: `https://jatakaveda.com/library/parashara-jaimini/` for separating Parashari and Jaimini rule families and locating topics for independent verification.
- KP reference material: `https://archive.org/stream/krishnamurti-padhdhati-vol-3-english/KP-Astrology-Basics_djvu.txt` and `https://archive.org/stream/krishnamurti-padhdhati-vol-3-english/Krishnamurti-Padhdhati-Vol-3%20-%20English_djvu.txt` for cusp, star-lord, sub-lord, proportional sub-period, and significator logic.

For every implemented rule, record: tradition, source chapter/page or technical reference, exact formula, supported chart scope, known exceptions, and test cases. If two traditions disagree, retain two tagged rulesets rather than averaging them.

## 1. Calculation Truth Layer

Build one authoritative calculation adapter before expanding interpretation rules.

- Use Swiss Ephemeris or another explicitly approved authoritative ephemeris adapter for Sun through outer planets, mean/true nodes, ayanamsha, sidereal time, ascendant, and houses.
- Make ayanamsha explicit: Lahiri, Raman, KP, or another named mode. Never call a linear approximation Swiss-compatible.
- Make node mode explicit: mean node or true node. Store the choice in chart metadata.
- Accept one timezone-aware local birth instant plus IANA timezone and coordinates. Convert once to aware UTC. Reject naive, ambiguous, or silently repaired datetimes at public boundaries.
- Calculate sunrise, sunset, local apparent solar time, Hora, Tribhaga, day/night, and Panchanga divisions from actual location and date. Do not infer day birth from Sun house or fixed local-hour windows.
- Return calculation metadata with every chart: ephemeris/version, ayanamsha, node mode, house system, timezone, UTC instant, coordinates, precision, boundary flags, and data-quality warnings.
- Never swallow calculation exceptions and continue with empty dictionaries. Return a typed unavailable/invalid result and prevent downstream prediction claims.

## 2. Normalized Chart Context

Create a single immutable context consumed by all predictors. It should contain raw facts and quality flags, not pre-written predictions.

- D1 planets: tropical and sidereal longitude, latitude, speed, retrograde/station status, sign, degree, nakshatra, pada, and house.
- Houses: whole-sign Parashari bhavas, chosen bhava-cusp system, Chalit mapping, and KP cusps kept as separate fields.
- Panchanga: tithi, vara, nakshatra, yoga, karana, sunrise, sunset, and local day boundary.
- Dashas: Vimshottari MD/AD/PD/SD/PrD with exact aware intervals and Moon-nakshatra balance metadata.
- Vargas: D2, D3, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60 and per-varga stability/boundary flags.
- Special systems: KP, Jaimini, Ashtakavarga, Chalit, and any Nadi/Lal Kitab module tagged by method.
- Quality: birth-time confidence, ephemeris availability, coordinate precision, boundary proximity, missing modules, and whether D60 is safe to interpret.

## 3. Evidence Ledger and Dependency Control

Every interpretation must be explainable from an evidence ledger.

Each evidence item stores:

- source system: Parashari, KP, Jaimini, Tajika, Ashtakavarga, transit, or other tagged module;
- subject: planet, house, dasha lord, karaka, varga, cusp, or transit;
- raw fact: the actual calculated placement or relation;
- interpretation: what that fact means for the selected domain;
- polarity: support, obstruction, mixed, or unavailable;
- weight and confidence impact;
- dependency group: the underlying planet/house/event factor used for correlation control;
- citation/rule ID and calculation-quality requirements.

Do not award independent points to the same planet merely because it appears in D1, KP, D60, transit, TCR, and a generated text rule. Group correlated evidence, cap its total contribution, and preserve the full trace for review.

## 4. Planet Dossier

Before judging an event, generate a structured dossier for every relevant planet:

- sign, exact degree, nakshatra, pada, and house;
- functional lordship for the selected Lagna and domain;
- exaltation, debilitation, own sign, moolatrikona, friend/neutral/enemy sign, and dignity source;
- Shadbala components, total, minimum required ratio, and interpretation of weak components;
- Bhavabala contribution and house-lord condition;
- Parashari aspects cast and received, with degree/quality where applicable;
- conjunction/yuti, planetary war if implemented, combustion, retrogression, station, and avastha;
- nakshatra lord, sub-lord, and chain relevance, without mixing KP meaning into Parashari judgment;
- relevant D9, D10, D7, D12, D20, D24, D30, and D60 confirmation or denial;
- current MD/AD/PD role and whether the planet can deliver the domain;
- domain-specific positive and negative contribution.

Fix the current Shadbala defects before using the dossier as a gate: the `is_benefic` dictionary truthiness bug, unused `is_day_birth`/`paksha` inputs, fixed-hour temporal strength approximations, binary Drik Bala, incomplete node/aspect handling, incomplete enemy/debilitation buckets, and missing house-aspect Bhavabala component.

## 5. House Dossier

For each event-relevant bhava, store:

- bhava sign, lord, occupants, and karaka;
- lord placement, dignity, Shadbala, Bhavabala, avastha, combustion, retrogression, and aspects;
- benefic and malefic influence, conjunctions, argala/obstruction where the selected tradition supports it;
- D1 promise, Chalit placement, KP cusp distinction, and relevant varga confirmation;
- BAV/SAV support for transit activation;
- positive evidence, negative evidence, missing evidence, and contradiction status.

Do not use one broad phrase such as "career house active" when the lord is combust, weak, placed in a dusthana, denied in D10, or blocked by an opposing factor. The house dossier must expose those trade-offs.

## 6. Prediction Sequence

All domain predictors should follow this order:

1. Define the question and domain precisely: career, marriage, education, health, children, finance, relocation, litigation, spirituality, or another supported area.
2. Establish D1 natal promise. If there is no promise, timing systems cannot create the event.
3. Identify event-producing houses, relevant lords, karakas, yogas, and their condition.
4. Judge strength and delivery capacity: dignity, Shadbala, Bhavabala, aspects, conjunctions, avastha, combustion, retrogression, and functional lordship.
5. Evaluate the active dasha hierarchy and whether each lord is relevant and capable of delivering the domain.
6. Confirm through the relevant varga without allowing a varga to create an unsupported D1 event.
7. Use transit as a trigger: exact relation, ingress, retrograde/station, natal contact, dasha relevance, and duration.
8. Modify transit intensity with Ashtakavarga, Tara Bala, Vedha, Sade-Sati/Dhaiya, or other selected methods.
9. Run the contradiction engine and include both supporting and weakening factors.
10. Produce a conditional timing window with assumptions, alternatives, evidence grade, and uncertainty.

## 7. Dasha Hierarchy

- MD establishes the broad life theme and should be judged by lordship, placement, dignity, strength, nakshatra chain, and relevant varga.
- AD narrows the event domain and must connect to event-producing houses/lords or karakas.
- PD refines the likely period only when MD and AD support the event.
- SD/PrD refine timing; they are not automatically more accurate and must never override a missing natal promise.
- Dasha lord name alone is not evidence. A "Jupiter period" is not automatically favourable; evaluate Jupiter's lordship, placement, dignity, strength, affliction, nakshatra/sub-lord chain, and domain relevance.
- Test Moon nakshatra balance, boundary positions, timezone-aware intervals, recursion, and inclusive/exclusive boundary semantics independently.

## 8. Varga Governance

- D1: overall promise and life structure.
- D9: relationship/dharma plus planetary maturity and confirmation; not a replacement for D1.
- D10: career, profession, authority, and status.
- D7: children and progeny.
- D12: parents and lineage.
- D24: education and learning.
- D20: spiritual practice and devotion.
- D30: misfortune, defects, and affliction.
- D60: fine karmic modifier only when birth-time precision and boundary stability are adequate.

Document sign-start conventions, especially D27, and test every boundary. Missing, unstable, or boundary-sensitive varga data lowers confidence; it must not be silently substituted with another chart or treated as decisive.

## 9. Method Separation

Keep methodologies explicit in code and output:

- Parashari: whole-sign houses, lordship, classical graha drishti, yogas, Shadbala, Bhavabala, and dasha interpretation.
- KP: Placidus cusps, cusp sub-lords, star/sub-lord chains, significators, and event decision.
- Jaimini: Chara Karaka, Karakamsha, Rashi Drishti, Arudha, and Chara Dasha.
- Tajika: annual chart and Varshaphala-specific rules only.
- Nadi/Lal Kitab: separate optional modules with their own sources and confidence.

Do not silently combine KP cusp rules with Parashari whole-sign lordship, Jaimini Rashi Drishti with Parashari graha drishti, or Tajika annual rules with natal prediction. Each output must state which method produced each conclusion.

## 10. Contradiction Engine

Explicitly test and report:

- strong natal promise versus weak or afflicted lord;
- dasha support versus adverse transit;
- D1 support versus denial in the relevant varga;
- benefic transit versus afflicted natal point;
- strong event houses versus obstructing houses;
- KP significator support versus cusp sub-lord denial;
- multiple positive rules depending on the same underlying planet or house;
- missing or low-quality calculation data.

If contradictions remain unresolved, output "mixed/conditional" rather than forcing a positive or negative verdict.

## 11. Confidence Design

Remove fake probability ranges such as 75-96% unless there is a real held-out calibration dataset. Use evidence grades:

- C1: weak, incomplete, or single-layer indication;
- C2: supported but mixed, conditional, or missing independent confirmation;
- C3: multi-layer convergence with valid calculation quality.

C3 requires independent support from natal promise, dasha activation, relevant varga or strong secondary confirmation, a transit/timing trigger, no unresolved major contradiction, and valid birth-time/ephemeris quality. Suppress C3 for uncertain birth time, boundary-sensitive charts, missing ephemeris, missing required varga, or silent fallback data.

## 12. Output Contract

Every prediction response should contain:

1. final conditional judgment;
2. what supports it, with planet/house/dasha/varga/transit evidence;
3. what weakens it or contradicts it;
4. timing window and why that window is selected;
5. alternative interpretation if evidence is mixed;
6. confidence grade and calculation-quality flags;
7. method and assumptions used;
8. health/legal/financial disclaimer where relevant.

Never use guarantee, destiny, certainty, or fixed wealth/status language. Strong wording must be tied to visible evidence and still remain conditional.

# Calculation Areas Requiring Full Independent Review

Review each file and compare against authoritative references before modifying formulas:

- `src/vyas/ephem.py`: planetary positions, nodes, ayanamsha, ascendant, Julian dates.
- `src/vyas/chart.py`: house mapping, nakshatra, dignity, aspects, retrograde/combustion.
- `src/vyas/dasha.py`: Vimshottari balance, 365.25 convention, sub-dasha boundaries, timezone.
- `src/vyas/varga.py`: D2, D3, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60 boundaries and sign starts.
- `src/vyas/kp.py`: cusp calculation, nakshatra lord, sub-lord sequence, significators.
- `src/vyas/ashtakavarga.py`: bindu rules, totals, planet-specific rules, transit interpretation.
- `src/vyas/shadbala.py`: dignity, temporal strength, ayana strength, combustion, varga strength; documentation itself mentions approximations.
- `src/vyas/gochar.py`: transit positions, ingress search, Vedha, Sade-Sati/Dhaiya.
- `src/vyas/panchang.py`: sunrise/sunset, timezone, location, tithi/nakshatra and day boundaries.
- `src/vyas/jaimini.py`: Chara Karaka and Chara Dasha rules.
- `src/vyas/nadi.py`: rule selection, timing assumptions, generic statements.
- `src/vyas/forensic_predictor.py`: scoring, fallback data, hard-coded claims.
- `src/vyas/daivagya_engine.py`: triple convergence and fallback transit logic.
- `src/vyas/prashna.py`: confidence formula and horary assumptions.
- `src/vyas/chatbot.py`: fallback data, prompt claims, stale transit handling.

# Files/Directories That Are Candidates for Removal

Do not delete blindly. First confirm runtime/build references with Antigravity. Remove from Git, not necessarily from the local machine, only after confirmation.

## Strong removal candidates

- `.venv311/` - local Python environment; approximately 9,093 tracked files.
- `AndroidDevsdk/` - vendor Android SDK; approximately 11,140 tracked files.
- `index.html.bak`.
- `page_1_rendered.png`.
- `page_2_rendered.png`.
- `page_3_rendered.png`.
- `page_9_rendered.png`.
- `page_24_clean.png`.
- `page_24_rendered.png`.
- `sample_report.pdf`.
- `sample_report2.pdf`.
- `test_vyas_thesis_38_pages.pdf`.
- `VYAS_Report.pdf`.
- `VYAS_Thesis_Report.pdf`.
- `VYAS_Executive_Publication_Thesis.pdf`.
- `vyas-astra-release-1.0.0.apk` if not the release artifact source.
- `vyas_mobile_hostinger.zip` if deployment archive is no longer used.
- `ngrok.exe` and `ngrok.zip` if no local tunnel workflow uses them.
- `cloudflared.exe` if no tunnel workflow uses it.
- Generated files under `artifacts/`.
- Generated `dist/` output if CI/build recreates it.

## Review before removal

- Root logo variants: `logo.jpg`, `logo.png`, `logo_icon.png`, `logo_v2.png`, `logo_option1.png`, `logo_option2.png`, `logo_option3.png`.
- Root inspection/debug scripts: `inspect_*.py`, `trace_*.py`, `scratch_transcript.py`.
- One-off repair scripts under `scripts/` such as `fix_*.py`, `overhaul_*.py`, and `patch_*.py`.
- Duplicate mobile HTML/JS/CSS bundles under `mobile/` and `static/mobile/`.
- `tv-ai-assistant/` duplicate/platform-specific files.
- Old PDF/test assets referenced by documentation or release scripts.

## Do not remove

Do not delete core modules merely because they contain defects:

- `src/vyas/ephem.py`.
- `src/vyas/chart.py`.
- `src/vyas/dasha.py`.
- `src/vyas/varga.py`.
- `src/vyas/kp.py`.
- `src/vyas/gochar.py`.
- `src/vyas/ashtakavarga.py`.
- `src/vyas/predictive_engine.py`.
- `src/vyas/forensic_predictor.py`.
- `src/vyas/daivagya_engine.py`.

Fix or replace formulas first.

# Non-Astrology Findings

- `scripts/push_to_origin.ps1` and `scripts/push_to_inikhil.ps1` contain credential-bearing Git URLs. Move credentials to secure environment/credential manager; rotate exposed tokens.
- `.gitignore` contains malformed entry `"old">`.
- `.venv311/` and `AndroidDevsdk/` are tracked vendor/environment trees.
- Android CI workflow does not appear to build a real APK/AAB artifact.
- Mobile Android release path uses debug signing.
- Android WebView configuration includes risky universal file access/mixed-content settings.
- Multiple mobile bundles can drift from each other.
- Generated PDFs, APKs, archives, screenshots, and binaries are mixed with source code.

# Required Antigravity Fix Plan

## Phase 1 - Establish truth

1. Add/enable Swiss Ephemeris dependency or an approved authoritative equivalent.
2. Implement one calculation adapter with explicit ayanamsha and node model.
3. Store calculation metadata: ephemeris, ayanamsha, node model, timezone, UTC instant, precision.
4. Remove silent approximate fallbacks.
5. Make all public date inputs timezone-aware.

## Phase 2 - Rebuild verification

Add independent tests for:

- Dates: 1900, 1956, 2000, 2020, 2050, 2100.
- Planets: Sun, Moon, Mars, Jupiter, Saturn, Rahu, Ketu.
- Ascendant at northern, tropical, and southern latitudes.
- IST, UTC, US DST, half-hour timezone.
- Nakshatra, pada, KP sub-lord boundaries.
- Sign boundary at 0° and 30°.
- D30 and D60 boundaries.
- Retrograde and station dates.
- Mean versus true node output.

Every golden value must come from an independent reference, not the same project function.

## Phase 3 - Prediction safety

1. Split factual chart calculation from interpretation.
2. Split natal promise, timing, and transit trigger.
3. Add negative evidence and contradiction penalties.
4. Prevent correlated evidence double-counting.
5. Replace fake percentages with calibrated evidence grades.
6. Suppress C3 when birth time, ephemeris, or required varga data is uncertain.
7. Replace guarantee/destiny wording with conditional wording.

## Phase 4 - Repository cleanup

1. Confirm references.
2. Remove local environments, SDK copies, generated outputs, debug artifacts, duplicate assets.
3. Add proper ignore rules.
4. Keep only source, reproducible build config, tests, and intentional release artifacts.
5. Rotate any exposed deployment credentials.

# Expanded Implementation Phases A-G

## Phase A - Authoritative calculations

1. Add/enable Swiss Ephemeris or an approved authoritative equivalent.
2. Implement one adapter with explicit ayanamsha, node model, house system, ephemeris version, and precision metadata.
3. Normalize every public datetime to an aware local instant, IANA timezone, coordinates, and one internal aware UTC instant.
4. Replace linear/shortened astronomy approximations or label them as unsupported; never claim Swiss compatibility without comparison tests.
5. Remove silent hard-coded, year-based, and empty-data fallbacks.

## Phase B - Normalized chart context

1. Build one immutable calculation context used by chart, dasha, varga, KP, Jaimini, Panchanga, transit, and prediction modules.
2. Keep D1 whole-sign, Chalit, and KP cusp data in separate fields.
3. Attach quality flags for missing modules, boundary proximity, birth-time uncertainty, and ephemeris failure.
4. Make all public calculation errors typed and visible to the caller.

## Phase C - Strength and aspect engines

1. Repair Shadbala first: `is_benefic` classification, real sunrise/sunset temporal strength, Drik Bala, node/aspect handling, dignity buckets, and Bhavabala aspect components.
2. Implement exact, documented Parashari aspect rules and keep Jaimini Rashi Drishti separate.
3. Build planet and house dossiers with dignity, lordship, strength, affliction, conjunction, aspect, avastha, combustion, retrogression, nakshatra chain, and relevant varga data.
4. Add independent golden tests for strength components, aspect edge cases, combustion, retrograde/station, dignity, and boundary positions.

## Phase D - Evidence graph and contradiction scoring

1. Add an evidence ledger with source system, raw fact, interpretation, polarity, weight, dependency group, and rule ID.
2. Deduplicate correlated KP/D60/transit/TCR/house evidence.
3. Add negative evidence, missing-data penalties, and explicit contradiction states.
4. Use C1/C2/C3 evidence grades; do not emit calibrated-looking percentages without a held-out dataset.

## Phase E - Domain-specific predictors

Define the event houses, lords, karakas, yogas, relevant varga, and obstruction houses before writing scoring logic. At minimum cover career/status, marriage/relationships, children, education, parents/lineage, health, finance, and spirituality. Treat these as domain schemas, not simple house-counting rules. Every domain must pass through planet/house dossiers and the contradiction engine.

## Phase F - Independent validation and backtesting

Add reference tests for dates 1900, 1956, 2000, 2020, 2050, and 2100; multiple latitudes; IST, UTC, US DST, and half-hour zones; mean/true nodes; nakshatra/pada/KP sub-lord/sign/D27/D30/D60 boundaries; dasha balance and recursion; Shadbala/aspect components; KP significators; Jaimini rules; and BAV/SAV contributor tables plus 337 SAV total. Every golden value must come from an independent reference. Backtest only after calculation correctness is established, then report false positives, false negatives, calibration, and domain limitations.

## Phase G - Controlled cleanup and release hardening

1. Confirm references for every cleanup candidate before deletion.
2. Remove local environments, SDK copies, generated outputs, debug artifacts, duplicate assets, and obsolete bundles from Git only after runtime/build checks.
3. Add proper ignore rules for environments, caches, generated reports, archives, binaries, and local secrets.
4. Keep source, reproducible build configuration, tests, and intentional release artifacts only.
5. Remove credential-bearing Git URLs/scripts and rotate any exposed tokens.
6. Build from a clean checkout and verify Python, JS, Android, and deployment paths independently.

# Acceptance Criteria

The project is not considered astrologically complete until:

- Swiss comparison stays within agreed tolerance for the full supported date range.
- Mean/true node errors meet the same documented tolerance.
- Ascendant comparison passes across representative latitudes and historical dates.
- Naive datetime input is rejected consistently at every public boundary.
- No hard-coded current-year transit fallback remains.
- Sunrise/sunset-dependent calculations use actual location/date astronomy.
- Planet dossiers expose lordship, dignity, strength, aspects, conjunctions, avastha, combustion, retrogression, nakshatra chain, dasha role, and relevant varga confirmation.
- House dossiers expose occupants, lord condition, benefic/malefic influence, Bhavabala, Chalit/KP distinction, BAV/SAV, and contradictions.
- Natal promise is evaluated before dasha, varga, transit, or secondary-system timing.
- MD/AD/PD/SD/PrD never override a missing natal promise.
- D1 remains primary; relevant vargas confirm or qualify but do not create unsupported events.
- Parashari, KP, Jaimini, Tajika, Nadi, and Lal Kitab evidence is method-tagged and never silently mixed.
- Unresolved contradictions produce a mixed/conditional result.
- Prediction confidence is evidence-based and can decrease for contradictions.
- C3 cannot be produced from a single rule family or correlated duplicate evidence.
- C3 is suppressed for uncertain birth time, boundary-sensitive data, missing ephemeris, missing required varga, or silent fallback.
- Output includes supports, weaknesses, timing, alternatives, confidence grade, assumptions, and required disclaimer.
- Tests run from a clean checkout with documented setup.
- No credentials are embedded in Git remotes/scripts.
- Generated/vendor files are either ignored or intentionally versioned.

# Message To Give Antigravity

> Audit VYAS end-to-end in phases. Do not blindly delete files, rewrite formulas, or add more prediction rules before the calculation layer is trusted. First replace or clearly isolate the approximate astronomy in `src/vyas/ephem.py`: independent comparisons show up to about 40 arcsec ayanamsha drift, true-node errors up to about 0.4 degrees, and historical ascendant error around 9 arcminutes. Normalize every public datetime to an aware local instant plus IANA timezone and coordinates, then one aware UTC instant. Remove silent 2026/year-based transit fallbacks and expose calculation errors.
>
> Implement the Jyotishi reasoning blueprint: immutable normalized chart context; separate D1, Chalit, KP cusps, and method tags; planet dossiers; house dossiers; exact dignity, lordship, Shadbala, Bhavabala, aspect, conjunction, combustion, retrograde, avastha, nakshatra-chain, dasha, and varga analysis; an evidence ledger with dependency groups; correlation caps; negative evidence; contradiction scoring; and C1/C2/C3 grades. Prediction order must be natal promise, event houses/lords/karakas, strength and condition, dasha activation, relevant varga confirmation, transit trigger, Ashtakavarga/Tara/Vedha modification, contradiction review, then a conditional timing window. MD/AD/PD/SD/PrD refine timing only; they cannot create a missing natal promise. D60 only confirms an already-supported theme when birth-time precision passes stability checks.
>
> Keep Parashari, KP, Jaimini, Tajika, Nadi, and Lal Kitab rules separate and visible in output. Do not silently combine KP cusps with Parashari whole-sign logic or Jaimini Rashi Drishti with Parashari graha drishti. Replace arbitrary 75-96% percentages and guarantee/destiny language. Output final conditional judgment, supporting evidence, weakening evidence, timing, alternative interpretation, confidence grade, calculation assumptions, method, quality flags, and health/legal/financial disclaimer where relevant.
>
> Add independent golden tests for 1900, 1956, 2000, 2020, 2050, and 2100; IST/UTC/US DST/half-hour zones; latitudes; mean/true nodes; nakshatra/pada/KP sub-lord/sign/D27/D30/D60 boundaries; dasha balance and recursion; Shadbala/aspect components; KP significators; Jaimini rules; and BAV/SAV totals. Every golden value must come from an independent reference. Backtest only after calculation correctness is established.
>
> Cleanup candidates are listed in this report. Before removal, verify references and runtime/build use. Strong candidates include `.venv311/`, `AndroidDevsdk/`, generated PDFs/screenshots/APK/ZIPs, tunnel binaries, backup files, debug scripts, duplicate logo/mobile bundles, and generated `artifacts/`/`dist/`. Do not delete core astrology modules merely because they contain defects. Remove credential-bearing Git URLs/scripts and rotate exposed tokens.

# Final Note

Current test pass status does not mean prediction accuracy is correct. The primary blocker is authoritative astronomy plus confidence design. Fix those before polishing UI or adding more astrology rules.

## Mobile/UI Audit & Remediation

**Current state:** The mobile surface is not production-ready. It mixes a fixed Streamlit iframe, a separate static bundle, hard-coded profile/chart data, and a simulated chatbot.

### Verified findings

- `pages/01_mobile.py` embeds `mobile/src/index.html` in a fixed `920px` iframe. Nested `100vh`/`100dvh` containers create double scrolling, keyboard overlap, and safe-area failures.
- `mobile/src/js/app-core.js` contains hard-coded birth data, Lagna, Rashi, Nakshatra, dasha, and SVG chart geometry. The visible chart is not connected to the authoritative calculation engine.
- The mobile chatbot is a `setTimeout` demo with canned answers. It has no backend request, chart context, book retrieval, authentication, or error state.
- Chat rendering uses `innerHTML` with dynamic text. Replace with text nodes or sanitized rendering before accepting user/model content.
- PDF and language controls in `mobile/src/index.html` have no working handlers, while the UI promises a “56-page PDF”.
- `mobile/src/` and `static/mobile/` have different raw hashes because of line-ending differences; normalized content is currently equivalent. There is still no enforced sync/build check, so future semantic drift remains possible.
- CSS uses global `user-select: none`, fixed viewport heights, fixed chat height, absolute bottom navigation, and only a `min-width: 480px` breakpoint. Small phones, landscape, zoom, and virtual keyboards are not covered.
- Navigation items are `div` elements rather than buttons/links and lack meaningful focus, keyboard, and ARIA behavior.

### Required fix

1. Use one source bundle and one deterministic sync/build command for `mobile/src` to `static/mobile`.
2. Replace the demo chatbot with an authenticated API call carrying a normalized chart/context ID and a compact evidence packet.
3. Remove the fixed iframe height. Use responsive sizing with safe-area padding and keyboard-aware layout.
4. Make navigation semantic buttons/links; add focus states, labels, reduced-motion support, and touch targets of at least 44px.
5. Render chat content safely without raw `innerHTML`.
6. Wire PDF download, language selection, loading, retry, offline, and backend-error states.
7. Add real-device checks for 320px, 360px, 390px, 430px widths; portrait/landscape; iOS Safari; Android Chrome; keyboard open; dark/light contrast.

## Chatbot, Reasoning & Token Budget

**Current state:** The prompt is doing calculation, retrieval, memory, marketing, and prose generation at once. This causes high token use and machine-like answers.

### Verified findings

- `src/vyas/chatbot.py` rebuilds a very large static prompt containing chart facts, astrology rules, marketing language, formula-bank text, books, curiosity hooks, and conversation history.
- Memory is keyword/topic detection plus the last four raw questions. It lacks a compact chart-state summary, unresolved questions, evidence memory, and prior conclusions.
- Provider calls repeatedly carry the same chart and rule context instead of using a cached chart packet or question-specific dossier.
- Book retrieval is capped to a small number of results and falls back from the full query to only the first two words. There is no authority rank, query decomposition, citation trace, or “not used” signal.
- Guarantee-style hooks such as “सटीक”, “अचूक”, “मेरिट सुनिश्चित”, and “पूर्ण विजय” undermine calibrated prediction and can create unsafe expectations.

### Target architecture

1. Classify each question as calculation, interpretation, timing, comparison, general education, or report generation.
2. Run deterministic calculations first. The model must not invent sign, house, dignity, strength, aspect, dasha, varga, or transit values.
3. Build a compact question-specific evidence packet: relevant planet/house dossiers, timing factors, contradictions, assumptions, and source IDs.
4. Retrieve books only when the question needs textual authority. Use hybrid lexical/semantic ranking with primary classical sources ahead of summaries.
5. Require structured output: judgment, supporting evidence, weakening evidence, timing, alternatives, confidence grade, assumptions, method, sources, and disclaimer.
6. Store compressed memory: chart hash, selected facts, prior judgments, unresolved questions, user preferences, and source citations. Do not resend raw history by default.
7. Cache chart, dasha, transit, varga, and retrieval packets by normalized input hash. Log prompt tokens, output tokens, retrieval hits, and fallback use.

### Efficiency target

- Stable chart context sent once per session or referenced by ID.
- Question packet normally below 1,500 input tokens before the answer.
- Retrieval snippets limited to the few passages that actually support the judgment.
- Output budget selected by task: short answer, consultation, or full dossier. Never truncate a required evidence section silently.

## Books, RAG & Citation Trace

**Current state:** The books folder is mostly a file collection, not a reliable knowledge system.

### Verified findings

- `src/vyas/book_reader.py` searches PDF/TXT/MD only. JSON/JSONL and DOCX inventory exists but is not included in chatbot book search.
- PDFs are opened and scanned on every query. There is no persistent index, chunking, OCR route, hash manifest, deduplication, or durable relevance score.
- Matching is exact/case-insensitive phrase matching. Hindi, English, Sanskrit, and transliteration variants are not normalized or expanded.
- `src/vyas/knowledge_engine.py` loads structured data but does not provide a persistent retrieval index or source-quality model. Its malformed sutra glob can ignore normal `.txt` sutra files.
- Search results do not reliably carry book, edition, page, chapter, line, language, or tradition metadata into the final answer.
- The prompt can imply classical-book alignment even when no book passage was retrieved. That is a traceability defect.

### Required book pipeline

1. Create an ingestion manifest with path, SHA-256, format, language, tradition, edition, page count, extraction status, and source authority.
2. Ingest PDF/MD/TXT/JSON/JSONL/DOCX. Add OCR only for pages with missing/poor text extraction.
3. Normalize Unicode, Devanagari, transliteration, punctuation, and common Hindi/English/Sanskrit aliases.
4. Chunk by chapter/section/page, retaining stable source coordinates.
5. Build a persistent hybrid index. Deduplicate repeated editions and near-identical chunks.
6. Return citations with every retrieved passage: book, chapter/page, edition, method/tradition, and relevance score.
7. Add a retrieval trace: which source passage influenced which conclusion. If none was used, say `No book evidence used for this conclusion`.
8. Add a test corpus with known queries and expected top sources. Measure recall, citation correctness, and latency.

## PDF & Publication Audit

**Current state:** Two competing PDF engines and hard-coded pagination produce inconsistent, poorly designed reports.

### Verified findings

- `src/vyas/pdf_builder.py` is a fixed ReportLab report with fixed Letter dimensions and weak overflow/splitting guarantees.
- `src/vyas/publication_engine.py` is a separate HTML/Chrome publication path with a hard-coded “56-page” footer. Actual page count is not authoritative.
- The ReportLab builder relies on Windows font paths and does not consistently use bundled fonts under `src/vyas/fonts/`. This fails or changes layout outside the development machine.
- Sample PDFs are six-page Letter documents with weak metadata and no reliable evidence ledger/citation/contradiction sections.
- Rendered pages show excessive whitespace and crowded chart grids with unreadable labels. The fallback renderer can materially change fonts and layout without a visible failure.
- Temporary HTML/profile files are written into the project root; output hygiene and cleanup are not guaranteed.

### Required publication standard

1. Select one canonical renderer: HTML/CSS plus headless Chrome using bundled fonts.
2. Offer `consultation` mode and `full dossier` mode. Page count must be dynamic.
3. Include chart assumptions, calculation quality, method tags, evidence ledger, contradictions, timing windows, book citations, and disclaimer.
4. Use repeatable table headers, controlled page breaks, safe chart sizing, and embedded Devanagari fonts.
5. Fail loudly when the primary renderer or fonts are unavailable. Do not silently substitute a materially different layout.
6. Keep temp artifacts outside the repository and delete them after successful export.
7. Preflight every PDF: open it, extract text, verify page count, verify fonts, detect blank pages, render thumbnails, inspect clipping/overflow, and compare required headings.

## Product-Level Next Features

Prioritize reliability before feature volume:

1. Calculation transparency: every displayed planet/house/dasha value links to its calculation inputs and method.
2. Expert reasoning view: planet dossiers, house dossiers, dignity/bala/aspect tables, varga confirmation, dasha activation, transit trigger, contradiction review, and confidence grade.
3. Question modes: quick answer, consultation, research-backed answer, and full report.
4. Timeline explorer: Vimshottari/Chara dasha, gochar, Ashtakavarga, Tara/Vedha, and event windows on one timeline.
5. Comparison tools: two birth times, two charts, D1 vs relevant varga, and method-separated KP/Parashari/Jaimini views.
6. Source-aware books panel: retrieved passages, page locations, relevance, and “used in conclusion” trace.
7. Report builder: preview, section selection, language, citation style, and export validation status.
8. Mobile-first PWA: offline shell, resumable requests, accessible navigation, safe-area support, and installable manifest.
9. Quality dashboard: astronomy confidence, birth-time sensitivity, missing ephemeris, fallback count, retrieval quality, and prediction backtest metrics.

## Verified Removal / Quarantine List

Do not delete by filename alone. First run reference/build/runtime checks and quarantine outside the release path.

- `.venv311/`: environment/vendor files; keep out of Git, recreate from a lock/requirements file.
- `AndroidDevsdk/`: remove only if no Android build/deployment path uses it.
- Generated PDFs, screenshots, APK/ZIP outputs, tunnel binaries, `artifacts/`, and `dist/`: remove from source control only after confirming they are not release inputs or user deliverables.
- Backup/temp files and duplicate generated mobile bundles: remove only after verifying the canonical source and build copy.
- Debug/inspection scripts: retain only those used by CI, release checks, or documented operations; archive the rest.
- Credential-bearing URLs, tokens, and old tunnel configuration: remove and rotate secrets immediately.

Do not remove core astrology modules, book files, or calculation code merely because they are incomplete or currently failing. Mark them as broken, add tests, or quarantine only after dependency tracing.

## Mobile Acceptance Criteria

- One source bundle produces identical served assets after normalization; CI rejects semantic drift and normalizes line endings before hashing.
- No fixed-height outer iframe or nested viewport scroll trap.
- Real chart/profile data loads from the backend; no hard-coded birth profile in shipped JS.
- Chat sends a real request, shows loading/retry/error states, and safely renders the response.
- PDF and language controls work on mobile.
- 320/360/390/430px widths, landscape, keyboard-open state, iOS Safari, and Android Chrome pass.
- Navigation is keyboard/focus accessible; touch targets are at least 44px; contrast and reduced-motion checks pass.

## Antigravity Addendum

Give Google Antigravity this order: first make astronomy and deterministic chart facts authoritative; then build expert reasoning and confidence; then build indexed books with citations; then replace the chatbot with compact evidence packets and cached memory; then consolidate PDF rendering and add preflight; then repair mobile integration and responsive accessibility; finally add product features. Do not optimize prose, add more rules, or delete files before these dependencies are verified.

## Fresh Desktop & Mobile UI Re-Audit (Current Baseline)

This section is based on the current working files after the recent interface changes. It supersedes earlier visual observations where the code has changed.

### P1 - Navigation is duplicated and too flat

- `app.py:4123` renders the primary research-suite selector in the sidebar.
- `app.py:4215` renders the same selector again in the main content area.
- `app.py:4074` exposes eleven primary suites as a single flat radio group.

**Why it still fails:** the visitor must understand eleven specialist categories before seeing value. The same navigation appears in two places, creates two state keys, and makes mobile/desktop behavior harder to keep aligned.

**Fix:** retain one primary navigation source only. Use this information architecture:

| Level | Desktop | Mobile | Contents |
|---|---|---|---|
| Primary | Left rail, grouped | Bottom navigation, five items max | Home, Kundli, Ask Vyas, Timing, More |
| Secondary | Context subnav under page title | Full-screen sheet | group-specific pages |
| Tertiary | Tabs up to five or an overflow menu | Segmented control or list | only the current task's views |

**Recommended groups:**

1. **Home:** Daily Horoscope, Panchang, alerts.
2. **My Kundli:** Birth chart, D1/D9, Vargas, strengths, remedies.
3. **Predictions:** Life forecast, dasha, transit, varshphal, timelines.
4. **Research:** KP, Jaimini, Nadi, Lal Kitab, chakras, books.
5. **Tools:** Prashna, compatibility, BTR, PDF, settings.

Do not put a tab inside a tab when a route/page can express the hierarchy. For example, `Research > KP > Planet/House Significators` may use an in-page segmented control; `Kundli > Vargas` should be a secondary page, not a permanently loaded nested tab tree.

### P1 - Large specialist tab strips remain unsuitable for small screens

- `app.py:4781` has five timing tabs.
- `app.py:5476`, `app.py:5755`, `app.py:5918`, and `app.py:6058` each have four or five specialist tabs.
- `app.py:6643` has ten forecast tabs, some with very long bilingual labels.
- `app.py:6197` and `app.py:6430` add nested tab/segment groups.

**Why it still fails:** long bilingual labels wrap, force horizontal scanning, and make comparison difficult. The radio-based `lazy_sections` improves performance but does not solve navigation density.

**Fix:** show at most four visible labels. Place overflow items in `More` / `All analyses`. Shorten labels; use a one-line Hindi label with optional English only on hover/settings, not in every tab. Keep tab selection in the URL/query state so a shared link opens the same analysis.

### P1 - Mobile route is still an embedded desktop-style surface

- `pages/01_mobile.py:43` loads the mobile UI in `components.html` at fixed height `920` with scrolling enabled.
- `app.py:806` has a second `components.html` mobile embed at the same fixed height.
- `mobile/src/js/app-core.js:120`, `mobile/src/js/app-core.js:134`, and `mobile/src/js/app-core.js:146` use `innerHTML`; the last one handles dynamic chat text.
- `mobile/src/js/app-core.js:23` still identifies the “Mobile Elite Engine” only in a browser console; it is not evidence of backend integration.

**Fix:** use one mobile entry point. Do not nest a full app in a fixed iframe. If Streamlit remains the shell, render responsive native components; if the PWA is retained, deploy it as a real route and call typed backend APIs. Render user/model text with `textContent` or a sanitiser. Provide skeleton/loading, no-data, retry, offline, permission, and calculation-error states.

### P1 - UI implementation is too coupled and difficult to maintain

- `app.py` combines routing, CSS, authentication, forms, calculators, chat, payment, notification JavaScript, dashboards, reports, and footer rendering in one file.
- It contains more than one hundred `unsafe_allow_html=True` calls plus many inline style strings.
- CSS overrides are distributed across large blocks, including global font-size overrides at `app.py:2514` through `app.py:2518`.

**Risk:** small visual edits can break unrelated screens, theme behavior differs by page, and accessibility/locale regressions are difficult to test.

**Fix:** split into `ui/theme.py` (tokens only), `ui/components/`, `ui/pages/`, and `ui/navigation.py`. Put CSS in one versioned stylesheet. Replace repeated HTML cards with a small, tested component set: `PageHeader`, `Metric`, `EvidenceCard`, `ChartPanel`, `EmptyState`, `ErrorState`, `SectionNav`, and `SourceCitation`.

### P2 - Current visual language is busy rather than premium-minimal

- The primary type size defaults to `19.5px` at `app.py:2518`, then globally overrides `p`, `div`, `span`, and labels. Dense data tables and long Hindi labels become over-large.
- Gold gradients, glass cards, shadows, borders, alert banners, badges, and marketing blocks appear together across the dashboard.
- The sidebar includes language, theme, font size, notifications, subscriptions, chart switching, creator contact, and research navigation before core task content.

**Fix:** use one restrained theme: warm ivory background, charcoal text, one saffron/copper accent, muted teal for verified/calculation status, and red only for errors. Use 16px body copy, 14px metadata, 20/28px section title, 32/40px page title. Restrict shadows to floating overlays; ordinary cards use a 1px neutral border. Reserve accent color for primary action, active navigation, and calculation quality status.

### Specific emoji removal / replacement list

Decorative emoji should be removed from persistent navigation, headings, CTA labels, status messages, and notification cards. Use the existing SVG icon mechanism from `app.py:400` only where an icon improves recognition; otherwise use text.

| File | Current location | Replace with |
|---|---|---|
| `app.py:2438` | Guest-mode button `✨` | Plain “Continue as guest” text |
| `app.py:2521-2523` | Notification heading and tab labels `🔔`, `📜`, `⚙️` | One bell/gear SVG in the heading; plain tab labels |
| `app.py:2529`, `app.py:2539`, `app.py:2552`, `app.py:2562` | Alert card emojis `🌟`, `🐄`, `🪔`, `🪐` | Category icon component or no icon |
| `app.py:2586`, `app.py:2607`, `app.py:2613`, `app.py:2618`, `app.py:2645` | Notification CTA/status emojis | Native status icon plus accessible text |
| `app.py:2741`, `app.py:2755` | Subscription/trial symbols `⚡`, `⭐` | Text badge (`Trial`, `Pro`) |
| `app.py:3073`, `app.py:3085`, `app.py:3088` | Admin/AI status symbols | Status dot + words; do not expose admin status in customer UI |
| `app.py:4248` | Refresh button `🔄` | SVG refresh icon with `aria-label` |
| `app.py:4443` | Birthday banner `✨` | Remove; banner already has hierarchy |
| `app.py:5510` | Data-lock heading `🔒` | Lock SVG only if it represents real lock state |
| `app.py:7636`, `app.py:7651`, `app.py:7663`, `app.py:7682`, `app.py:7685`, `app.py:7693`, `app.py:7708`, `app.py:7723`, `app.py:7727`, `app.py:7745`, `app.py:7760`, `app.py:7829`, `app.py:7845`, `app.py:7988` | Chat/avatar/prompts/VIP/mic emojis | Avatar image or SVG icons; plain prompt and plan labels |
| `mobile/src/js/app-core.js:23` | Console `🌟` | Remove; logs should not contain presentation symbols |

**Exception:** culturally meaningful symbols may remain in editorial festival content, such as a festival banner created from calendar data. They must not appear as fake status, navigation decoration, or as a substitute for accessible controls.

### International-grade theme implementation

Do not copy an arbitrary external theme wholesale. Reuse a small token system and maintain the Vedic identity through typography, illustration, and chart presentation rather than glitter/gradients.

```css
:root {
  --bg: #f8f6f1;
  --surface: #ffffff;
  --surface-subtle: #f1eee7;
  --text: #1c2420;
  --muted: #64706a;
  --border: #ded8cc;
  --accent: #a94f1f;
  --accent-strong: #7f3514;
  --verified: #146c62;
  --danger: #b3261e;
  --radius: 12px;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
}
```

Use a serif display face only for the VYAS wordmark and report headings. Use one highly legible Devanagari/Latin text family for all interface controls and data. Bundle required fonts for reports and offline/mobile use; do not rely on a network font request for functional text.

### Layout blueprint

**Desktop (>= 1024px):** fixed 240px navigation rail; 1,280px max content canvas; page title + chart selector + one primary action in a compact header; two-column content only for overview pages; one-column reading mode for reports; right-side contextual evidence drawer only when requested.

**Tablet (768-1023px):** collapsible navigation drawer; no permanent right rail; one main column with two-column metric cards only when they retain 280px minimum width.

**Mobile (< 768px):** compact top bar; five-item bottom navigation; no sidebar; one column; sticky primary action only for an active task; chart tables convert to labelled rows or horizontally scrollable tables with an explicit hint; analysis sections open as sheets/accordions instead of tab strips.

### Required UI quality gates

1. Keyboard-only navigation works through nav, all tabs/segments, chart selector, chat, PDF export, and settings.
2. Every control has a visible label; icon-only controls have an accessible name and tooltip.
3. All mobile targets are at least 44 by 44 CSS px; no horizontal page scroll at 320px width.
4. Light, dark, and high-contrast themes meet WCAG AA contrast; chart colors also have text/pattern labels.
5. Each page has loading, empty, error, and stale-calculation states.
6. UI screenshots are tested at 320, 360, 390, 430, 768, 1024, 1280, and 1440px before release.
7. Customer UI never exposes internal auto-update/admin controls, raw confidence percentages, hard-coded profile data, or unsupported precision claims.

## Live Website vs Repository Audit (2026-11-18)

The production website was fetched directly from `https://vyasastro.in/` and `https://vyasastro.in/mobile/`. Browser-based visual interaction was unavailable in this audit session, so these findings are based on the live HTML, assets, and local source comparison.

### P0 - Four independently versioned product surfaces

| Surface | Current artifact | Approximate size | Result |
|---|---|---:|---|
| Public desktop | `https://vyasastro.in/` | 670K characters | Independent static HTML application |
| Public mobile | `https://vyasastro.in/mobile/` | 557K characters | Independent static HTML application |
| Local desktop source | `index.html` | 698K characters | Does not match live root |
| Android offline bundle | `android_app/app/src/main/assets/mobile/index.html` | 567K characters | Does not match public mobile |
| Streamlit product | `app.py` and `pages/01_mobile.py` | separate runtime | Different UI and calculation flow |

This confirms the reported “code has one thing, web has another” problem. There is no single source of truth or verified deployment contract.

**Required fix:** choose one canonical client application and one backend API. Delete or quarantine duplicate clients only after the canonical path has production parity. Add CI release checks that fetch the deployed root/mobile artifact after deployment, calculate a normalized SHA-256 hash, compare it with the release artifact, and fail when they differ. Version the release with a visible build ID (for example, `2026.11.18+gitsha`) in both UI and API responses.

### P0 - Browser-side AI provider fallback is a credential-exposure risk

The live root and mobile HTML both contain a direct `fetch` path to `https://api.groq.com/openai/v1/chat/completions`, alongside the intended `/api/ai_chat.php` proxy.

**Risk:** a browser cannot safely keep an AI-provider secret. A bearer credential in JavaScript is accessible to every visitor, browser extension, cache, page source viewer, and network inspector. Even if the fallback is rarely used, the secret must be considered exposed.

**Required fix now:** remove every direct provider call from all public HTML and Android assets; make `/api/ai_chat.php` the only AI route; keep provider credentials only in server secrets; rotate the current Groq key; impose server-side rate limits, origin checks, request schema validation, auth/anonymous quotas, prompt-size limits, and audit logging. Do not place a replacement key in `localStorage`, a service worker, a source map, or a mobile bundle.

### P1 - Production contains hard-coded identity and privilege state

- The live root contains `nikhilvyas007@gmail.com` five times; the live mobile page contains it twice.
- Local `index.html` includes founder quick-login/default profile logic and an `authorizedPro` email list.
- The Android bundle includes the same type of Pro authorization logic.

**Risk:** hard-coded founder identities and client-side membership checks create impersonation, privilege-bypass, privacy, and trust problems. Client-side entitlement is not access control.

**Required fix:** remove personal accounts and allow-lists from all shipped clients. Resolve session identity and plan/entitlement only on the server from a signed session. The client may display an entitlement returned by the API but must never decide it. Use a separate non-production fixture for demos.

### P1 - Live claims remain materially stronger than the audited calculation layer supports

The production metadata and UI repeatedly claim `100%`, `0.001`, `NASA`, `Swiss Ephemeris`, and a fixed `56-page` report. These claims appear in OpenGraph, Twitter, FAQ structured data, shared-text generation, and visible UI.

**Required fix:** replace marketing absolutes with verifiable method language. Example: “Calculations use the configured ephemeris and ayanamsha; report shows inputs, method, and calculation timestamp.” Only state accuracy or rating values that can be documented, reproduced, and independently verified. Remove unverified `aggregateRating` / `ratingCount` structured data; search engines can treat misleading review markup as spam.

### P1 - Live pages are monolithic, client-heavy, and stateful without a stable data contract

The live root contains 77 direct `innerHTML` assignments, 49 `localStorage` references, 77 buttons, and 7 script blocks; live mobile contains 71 `innerHTML` assignments and 31 `localStorage` references. Both are large standalone documents rather than API-backed application shells.

**Required fix:** separate static layout from data/state. Adopt a small state model: authenticated user, selected chart ID, chart calculation result/version, active page, and cached API query keys. Every dynamic text path must use safe DOM APIs or an audited sanitizer. Persist only non-sensitive preferences locally; store profiles, charts, plans, and chat history server-side with explicit consent and deletion controls.

### P1 - Web/mobile/API functional parity is not demonstrable

Both public surfaces share some phrases and direct chat code, but their hashes, sizes, and embedded feature sets differ. The Android bundle is also separate. A bug fixed in one path can remain live in the others.

**Required fix:** define a feature matrix and test it per release:

| Capability | Desktop web | Mobile web | Android | Streamlit admin/research |
|---|---|---|---|---|
| Create/edit chart | required | required | required | optional/internal |
| Calculation source/method | required | required | required | required |
| AI answer with citations | required | required | required | required |
| PDF export | required | required | required | required |
| Authentication/entitlement | server-backed | server-backed | server-backed | server-backed |
| Analytics/admin controls | no | no | no | restricted |

Ship a feature only when it passes on every intended public surface. Otherwise hide it, show its status, or keep it internal.

### Deployment plan

1. Freeze public releases long enough to identify the actual hosting source and deployment command.
2. Choose the canonical web source (recommended: modular web app; keep Streamlit for internal research/admin only).
3. Extract a versioned calculation API and a versioned AI/PDF API; no public browser code may calculate secret/provider/auth decisions.
4. Rebuild desktop, mobile, and Android from shared components/API contracts, not copied HTML files.
5. Add staging; run desktop/mobile viewport, login, chart, chat, PDF, and security smoke tests there.
6. Deploy one immutable release; verify live URL hashes/build IDs; purge only the intended cache; retain rollback artifacts.

## Book-Based AI Plan

Do not pretrain a foundation model directly on the entire book collection. First build a traceable retrieval system, then fine-tune only on licensed, reviewed, structured examples.

1. **Ingestion:** keep original file ID, title, path, edition, language, OCR status, page number, source hash, and extraction quality for every Markdown file.
2. **Index:** chunk content by chapter/page; index Hindi, English, Sanskrit, and transliterated terms; retrieve primary sources before commentary and duplicate editions.
3. **Answering:** deterministic astrology engine produces positions, houses, strength, aspects, dasha, varga, and transit facts. Retrieval supplies only relevant source passages. The LLM explains the evidence; it does not create calculations.
4. **Citation:** every book-backed conclusion shows book, edition, page, excerpt ID, and whether it affected the final judgment. If no passage was used, say so.
5. **Fine-tuning:** create reviewed examples in an instruction/evidence/answer/citation schema after the RAG system is trusted. Exclude OCR-noisy, copyrighted-without-rights, contradictory, medical/legal/financial guarantee, and unverified prediction text.
6. **Evaluation:** test factual citation accuracy, retrieval recall, Hindi OCR quality, rule-method separation, refusal/disclaimer behavior, token cost, and response latency before serving any fine-tuned model.
