# Vedic Yield Astrology Systems (VYAS)

**Designed by:** Nikhil Vyas (MAJY)

## 1. मूल उद्देश्य (Core Objective)
VYAS is an advanced, forensic astrology engine designed to synthesize multiple astrological systems (D1, Dasha, Transit, Nakshatra, Divisional charts, KP, Jaimini, Ashtakavarga, etc.) into a controlled, rules-based, and confirmation-driven prediction framework. 

It specifically avoids simplistic "one yoga = one event" logic, instead demanding multi-layered confirmation across D1, Vargas, Dasha timelines, and transit activations.

## 2. Core Architecture
*   **Ephemeris Engine:** Pure Python NASA JPL (DE440s) for high-precision planetary coordinates (Sidereal, Lahiri Ayanamsa).
*   **Nakshatra Core Engine:** Traces deeper significations via Planet -> Nakshatra -> Nakshatra Lord -> Placement.
*   **Dasha Engine:** Precision Vimshottari Mahadasha and Sub-dasha (Antar, Pratyantar) proportional calculation engine.
*   **Forensic Rule Evaluation:** A custom multi-layered evaluation engine built in `engine.py`.

## Directory Structure
- `src/vyas/`: Core Python library for astrology calculations.
- `data/`: Ephemeris data files (like DE440s.bsp).
- `test_vyas.py`: Integration test showing basic chart, dasha, and nakshatra-chain evaluations.
