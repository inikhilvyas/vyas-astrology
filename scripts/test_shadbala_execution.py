import sys
sys.path.insert(0, "src")
import datetime as dt
from vyas.chart import Chart, PlanetState
from vyas.shadbala import compute_shadbala

# Sample birth chart
planets = {
    "Sun": PlanetState("Sun", 217.71, 1.0),
    "Moon": PlanetState("Moon", 224.63, 13.2),
    "Mars": PlanetState("Mars", 282.34, 0.7),
    "Mercury": PlanetState("Mercury", 239.28, 1.3),
    "Jupiter": PlanetState("Jupiter", 259.56, 0.2),
    "Venus": PlanetState("Venus", 257.81, 1.1),
    "Saturn": PlanetState("Saturn", 207.03, 0.05),
    "Rahu": PlanetState("Rahu", 33.54, -0.05),
    "Ketu": PlanetState("Ketu", 213.54, -0.05),
}
chart = Chart(ascendant_longitude=23.45, planets=planets)

birth_utc = dt.datetime(1990, 5, 15, 9, 5, tzinfo=dt.timezone.utc)
shadbala_res, bhavabala_res = compute_shadbala(chart, birth_utc=birth_utc)

print("=== SHADBALA RESULTS ===")
for p, s in shadbala_res.items():
    print(f"  {p:8s}: Total={s.total_virupas:6.2f} V ({s.total_rupas:4.2f} R) | Req={s.min_required:5.1f} | Ratio={s.strength_ratio:4.2f} | {s.verdict}")

print("\n=== BHAVABALA RESULTS ===")
for h, v in bhavabala_res.items():
    print(f"  House {h:2d}: {v:6.2f} Virupas")

