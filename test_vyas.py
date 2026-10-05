from datetime import datetime, timezone
import sys
import os

# Add src to path so we can import vyas
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vyas.ephem import planet_positions, ascendant_sidereal
from vyas.chart import Chart, PlanetState
from vyas.dasha import VimshottariDasha
from vyas.engine import ForensicEngine

def main():
    dt = datetime(1990, 1, 1, 12, 0, tzinfo=timezone.utc)
    lat, lon = 28.6139, 77.2090 # New Delhi
    
    # Get positions
    raw_pos = planet_positions(dt)
    asc_lon = ascendant_sidereal(dt, lat, lon)
    
    # Create chart
    planets = {name: PlanetState(name, p.longitude, p.speed) for name, p in raw_pos.items()}
    chart = Chart(asc_lon, planets)
    
    print(f"Ascendant Sign: {chart.ascendant_sign}")
    for name, p in chart.planets.items():
        print(f"{name}: {p.sign_name} ({p.longitude:.2f}°) - Nakshatra: {p.nakshatra_name} (Lord: {p.nakshatra_lord})")
        
    print("\n--- Nakshatra Chain for Moon ---")
    engine = ForensicEngine(chart)
    chain = engine.trace_nakshatra_chain("Moon")
    for link in chain:
        print(f"{link.planet_name} -> {link.nakshatra} -> Lord: {link.lord_name} (in {link.lord_sign}, H{link.lord_house})")
        
    print("\n--- Dasha ---")
    dasha = VimshottariDasha(chart.planets["Moon"].longitude, dt)
    mds = dasha.calculate_mahadashas()
    for md in mds:
        print(md)
        
if __name__ == "__main__":
    main()
