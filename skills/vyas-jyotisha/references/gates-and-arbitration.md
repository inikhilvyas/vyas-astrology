# Gates, Evidence Ledger, Arbitration, Timing

## Contents
1. Question classification and event ontology
2. Domain evidence matrix
3. Event Promise Gate
4. Evidence ledger and double-counting control
5. Cross-system verification
6. Contradiction engine, multi-event competition, counterfactuals
7. Red-team checklist
8. Confidence (C1-C5) and PSS
9. Timing engine and false-precision protocol
10. Final prediction quality gate

## 1. Classification / ontology
Classes: YES/NO, EVENT TIMING, CAREER, MARRIAGE, CHILDREN, WEALTH, EDUCATION, HEALTH, PROPERTY, BUSINESS, RELATIONSHIP, CHARACTER, LIFE PERIOD, COMPARATIVE PERIOD, SPIRITUALITY, TRAVEL, REMEDY, PRASHNA, RESEARCH, RECTIFICATION. Normalise the user's question into `{event, person, window asked, constraints}`. The ontology only **routes** to methods - each method keeps its own house mapping.

## 2. Domain evidence matrix (starting point; use each method's native logic)
| Domain | Parashari focus | Vargas | KP focus | Jaimini/other |
|---|---|---|---|---|
| Marriage | 2/7/11, 7th lord, Venus/Jupiter, D9 | D1, D9 | C7 sub lord -> 2/7/11 vs 1/6/10/12 | Upapada, DK, A7 |
| Career | 2/6/10/11, 10th lord, Sun/Saturn | D1, D10, D9 | C10 sub lord -> 2/6/10/11 | AmK, A10 |
| Wealth | 2/5/9/11 | D1, D2 | C2/C11 | Indu Lagna |
| Children | 5th, Jupiter | D1, D7 (D9) | C5 -> 2/5/11 | PK/Putra karaka |
| Education | 4/5/9, Mercury/Jupiter | D1, D24 | C4/C9/C11 | - |
| Property | 4th, Mars/Saturn | D1, D4 | C4 -> 4/11/12 | - |
| Travel/abroad | 3/9/12 | D1, (D9) | C12/C9/C3 | - |
| Spirituality | 9/12/5, Jupiter/Ketu | D1, D20 | - | AK, Karakamsa |
| Health | 1/6/8/12, karakas | D1, D6, D30 | - | symbolic only; no diagnosis |
House sets here are widely-used conventions, not universal truths; state the convention actually used.

## 3. Event Promise Gate
**Promise -> Activation -> Trigger -> Context.**
- G1 Natal promise: enough independent indicators in the *relevant method's* terms? If no, **stop timing**; report EVENT_DENIED or weak promise.
- G2 Activation: do maha/antar (and pratyantar if used) lords connect to the promise (lordship, occupation, star lord, significators)? If no, latent promise.
- G3 Trigger: credible transit/nakshatra/KP/ruling-planet/Jaimini trigger inside the window? If no, TIMING_UNRESOLVED.
- G4 Context: opportunity and circumstance (age, relationship status, work situation). Unknown -> say unknown.
Distinguish promise from *intensity*: promise present but weak planet/weak dasha/constraints -> reduced manifestation.

## 4. Evidence ledger & double-counting
Fields: `id, method, claim, chart_factor, planet/house, degree, nakshatra, pada, rule, source, provenance, support|contradict, strength(1-5), data_quality(A-D), dependency_id, epistemic_status`.
Epistemic statuses: FACT, CALCULATED FACT, SOURCE RULE, TRADITIONAL INTERPRETATION, LINEAGE-SPECIFIC, MODEL INFERENCE, EXPERIMENTAL HYPOTHESIS, PREDICTION, UNKNOWN. Never silently upgrade.
**Dependency IDs:** items derived from the same planetary configuration/lordship/rule share an ID and count as one independent confirmation. Examples of correlated sets: "Venus 7th lord in 11th" appearing under Parashari, Nakshatra and Varga write-ups; KP cusp significators that reduce to the same star-lord fact. True independence needs a different method, data source, or mechanism.
Graph: PLANET -> SIGN -> HOUSE -> LORD -> NAKSHATRA -> STAR LORD -> PADA -> NAVAMSHA -> DISPOSITOR -> ASPECT -> DASHA -> TRANSIT -> EVENT. Connectivity is description, not causation; arbitration decides relevance.

## 5. Cross-system verification
After first-pass verdicts are frozen, tabulate: method | verdict | strength | supporting | contradicting | assumptions. Disagreement is explained, not averaged. Priority goes to the method most relevant to the question, rule fidelity and data quality - never user preference. Consensus != truth; it means independent methods converge under their own rules.

## 6. Contradictions, competition, counterfactuals
- Label outcomes: possible / supported / strongly supported / mixed / denied / unresolved.
- A strong denial in a highly relevant method is not erased by several weak supports.
- Multi-event competition: list candidate manifestations for the window (job change, relocation, travel, relationship step, ...), rank by convergence, report the top plus alternatives.
- Counterfactual: disable the single strongest evidence item (and separately any experimental rule); if the conclusion collapses, cap confidence at C2-C3.

## 7. Red-team (PASS / PASS WITH CAUTION / REQUIRES REVISION / BLOCK)
Ask: Is natal promise really present? Is timing manufactured? Evidence double-counted? One system contaminate another? Birth time too uncertain? Does a varga contradict? Does KP deny? Is the dasha weak? Is the transit superficial? Is an experimental rule carrying weight? Did source text anchor me? Is the prediction more precise than evidence permits? Is context unknown?

## 8. Confidence and PSS
C5 very strong convergence; C4 strong; C3 moderate; C2 weak/conflicted; C1 speculative/insufficient. Thresholds: date-specific >= C4; yes/no >= C3; narrow window needs more convergence than broad window.
PSS (internal heuristic, optional): show components - planet strength, house strength, yoga support, dasha alignment, transit confirmation, ashtakavarga - with derivation. Labels: Very Strong / Strong / Moderate / Weak-Conflicted / Speculative internal convergence. Never express as a validated probability; a high number never overrides a methodological contradiction.
Downgrade for: uncertain birth time, calculation conflict, missing vargas, experimental dependence, contradictory systems, weak promise/dasha, absent trigger, unknown context.

## 9. Timing and false precision
Order: Maha -> Antar -> Pratyantar -> (Sookshma only if event strongly supported) -> transit -> nakshatra transit -> KP ruling planets -> Jaimini -> chakra/tara -> muhurta (only when the user controls timing). Convergence of independent timing systems can raise confidence; conflict widens the window. Output **EARLIEST PLAUSIBLE / MOST CONCENTRATED / LATEST PLAUSIBLE**. If unresolved: `TIMING_UNRESOLVED`. No day/hour precision unless earned; never choose the date that sounds best.
Observable precursors: testable real-world developments (interviews, negotiations, documentation, introductions, travel planning), explicitly not omens.

## 10. Final prediction quality gate (all must hold or the prediction is blocked/downgraded)
raw chart reconstructed - data locked - ayanamsha verified - house system verified - exact degrees verified where used - nakshatra/pada verified - relevant varga verified - promise established - activation established - trigger established - KP/Jaimini/Nadi completed where relevant - contradictions checked - correlated evidence discounted - source anchoring removed - red-team done - timing precision justified - confidence computed - failure conditions stated.
Core equation (reasoning framework, not a probability): DEFENSIBLE PREDICTION = verified promise + valid activation + credible trigger + context + independent confirmation - contradiction - data uncertainty - correlated evidence - unsupported assumptions.
