# CHART_STATE, Data Lock, Handoffs

## Contents
1. Two-pass processing
2. CHART_STATE / KUNDLI DATA LOCK schema
3. Data confidence grading
4. Case state & agent handoff
5. Failure states

## 1. Two-pass processing (mandatory when a document has both chart data and prose)
**Pass 1 — blind reconstruction.** Extract data only; skip interpretation text entirely. Cross-check table vs chart image; compute what is derivable (nakshatra, pada, navamsha, KP lords, dasha) with `scripts/vyas_calc.py` and compare against the document's printed values. Any mismatch -> `DATA_CONFLICT` with both values listed; do not pick the one that suits a prediction.
**Pass 2 — source interpretation.** Only now read the prose. Classify every claim (see `source-audit.md`). Test against the frozen state.

## 2. Schema (write this out, in compact form, in the analysis for FULL/AUDIT)
```
CHART_STATE
  identity: name/ref (optional), source document, software + version if printed
  birth: date, time, time_accuracy (exact/±min/approx/unknown), place, lat, lon, tz, dst
  per_method_settings:
    parashari: {ayanamsha, house_system, aspect_rule, dasha_year_convention}
    kp:        {ayanamsha (e.g. KP New), house_system (e.g. Placidus), cusp_source}
    jaimini:   {ayanamsha, karaka_scheme (7 or 8), drishti: rashi}
  lagna: {longitude, sign, nakshatra, pada, kp_lords}
  cusps: [C1..C12 longitude, sign, star lord, sub lord, sub-sub lord]     # KP only
  planets: [name, longitude (d m s), sign, house_ws, house_cusp, retro, nakshatra, pada, star_lord,
            navamsha_sign, pada_navamsha_lord, kp_sub, kp_subsub, combust?, source_of_value]
  dasha: [system, maha/antar/pratyantar with dates, convention]
  vargas: {D9, D10, D7, D24, ...: placements as printed}  # only those present
  ashtakavarga: {SAV, BAV per planet, methodology used by source}
  data_confidence: {birth_time, positions, cusps, dasha, vargas}
  provenance: for each numeric value: document field / calculation / user statement
```
Rules: immutable once frozen. Corrections create a new version with reason. Unknown stays `UNKNOWN`.

## 3. Data confidence grading
- **A** birth time documented (hospital record) and positions consistent with recomputation.
- **B** time from family memory ±5-15 min; Lagna-sensitive layers usable with caution; KP sub-lords of cusps and D10+ vargas flagged.
- **C** approximate time (hour or "morning"); only Moon-based, sign-level, whole-sign-planet layers; recommend rectification before event timing.
- **D** unknown time; Moon/planet-sign-level reading only (Moon sign, dasha from Moon with caveat); no cusp/lagna/varga-lagna conclusions.
Sensitivity test: shift birth time by ±5/±10/±15 min; if Lagna degree, cusp sub-lord, or D9/D10 lagna changes, mark the dependent conclusion time-fragile.

## 4. Case state and handoff (keep critical state in written structures, not only in context)
Handoff record: `sender, receiver, purpose, question, inputs, evidence_ids, assumptions, requested_output, confidence, unresolved`.
CASE_STATE holds: identity, birth data, settings, chart, nakshatras, vargas, dasha, transits (with reference date/location), ledger, predictions, contradictions, research hypotheses, sutras, output status.
Agent authority: Calculation computes, never interprets. Method specialists interpret within their own method only. Research retrieves, cannot change policy. Red-team challenges, cannot invent chart data. Arbitration ranks evidence, cannot alter calculations. Synthesis states only authorised conclusions.

## 5. Failure states
`DATA_INVALID` (impossible values) · `CALCULATION_INVALID` · `DATA_CONFLICT` · `INSUFFICIENT_DATA` · `SOURCE_AMBIGUOUS` · `HOUSE_SYSTEM_CONFLICT` · `AYANAMSHA_CONFLICT` · `EVENT_DENIED` · `TIMING_UNRESOLVED` · `CONTRADICTION_UNRESOLVED` · `RESEARCH_REQUIRED` · `TOOL_FAILURE` · `BIRTH_RECTIFICATION_REQUIRED` · `HUMAN_REVIEW`.
State the failure, what was affected, what would resolve it. Then continue only with the unaffected parts.
