from __future__ import annotations

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from vyas.chart import Chart, PlanetState
from vyas import constants

@dataclass
class NakshatraLink:
    planet_name: str
    nakshatra: str
    lord_name: str
    lord_sign: str
    lord_house: int
    lord_nakshatra: str

class ForensicEngine:
    """
    Vedic Yield Astrology Systems (VYAS)
    Designed by Nikhil Vyas (MAJY)
    
    The VYAS Forensic Astrology Engine for multi-layered confirmation.
    """
    
    def __init__(self, chart: Chart):
        self.chart = chart
        
    def trace_nakshatra_chain(self, planet_name: str, depth: int = 3) -> List[NakshatraLink]:
        """
        Traces the nakshatra dispositor chain: 
        Planet -> Nakshatra -> Nakshatra Lord -> Lord's Placement
        """
        chain = []
        current_planet = planet_name
        
        for _ in range(depth):
            if current_planet not in self.chart.planets:
                break
                
            p_state = self.chart.planets[current_planet]
            n_lord = p_state.nakshatra_lord
            
            if n_lord not in self.chart.planets:
                break
                
            lord_state = self.chart.planets[n_lord]
            lord_house = self.chart.get_house_of_planet(n_lord)
            
            link = NakshatraLink(
                planet_name=current_planet,
                nakshatra=p_state.nakshatra_name,
                lord_name=n_lord,
                lord_sign=lord_state.sign_name,
                lord_house=lord_house,
                lord_nakshatra=lord_state.nakshatra_name
            )
            chain.append(link)
            
            # The next planet in the chain is the lord of the current nakshatra
            current_planet = n_lord
            
            # Cycle detection (e.g. mutual nakshatra exchange)
            if any(l.planet_name == current_planet for l in chain):
                break
                
        return chain

    def evaluate_planet_strength(self, planet_name: str) -> Dict[str, Any]:
        """Evaluates basic dignity (Exaltation, Moolatrikona, Own Sign, Debilitation)."""
        if planet_name not in self.chart.planets:
            return {}
            
        p = self.chart.planets[planet_name]
        sign_idx = p.sign_index
        deg_in_sign = p.longitude % 30.0
        
        dignity = "Neutral"
        score = 0
        
        if planet_name in constants.EXALTATION:
            ex_sign, ex_deg = constants.EXALTATION[planet_name]
            deb_sign = (ex_sign + 6) % 12
            if sign_idx == ex_sign:
                dignity = "Exalted" if abs(deg_in_sign - ex_deg) <= 3 else "Exalted (Sign)"
                score = 100
            elif sign_idx == deb_sign:
                dignity = "Debilitated" if abs(deg_in_sign - ex_deg) <= 3 else "Debilitated (Sign)"
                score = -100
                
        if dignity == "Neutral" and planet_name in constants.MOOLATRIKONA:
            mt_sign, mt_start, mt_end = constants.MOOLATRIKONA[planet_name]
            if sign_idx == mt_sign and mt_start <= deg_in_sign <= mt_end:
                dignity = "Moolatrikona"
                score = 80
                
        if dignity == "Neutral" and planet_name in constants.OWN_SIGNS:
            if sign_idx in constants.OWN_SIGNS[planet_name]:
                dignity = "Own Sign"
                score = 60
                
        return {
            "dignity": dignity,
            "score": score,
            "is_retrograde": p.is_retrograde
        }

    def verify_event_promise(self, planet_name: str, house_num: int) -> Dict[str, Any]:
        """
        Implements Rule: Multi-layered confirmation.
        Check if planet promises event related to house_num via:
        1. Placement in house
        2. Lordship of house
        3. Nakshatra lord's connection to house
        """
        p_house = self.chart.get_house_of_planet(planet_name)
        in_house = (p_house == house_num)
        
        # Check lordship
        asc_sign = self.chart.ascendant_sign
        house_sign = (asc_sign + house_num - 1) % 12
        house_lord = constants.SIGN_LORD[house_sign]
        is_lord = (planet_name == house_lord)
        
        # Check nakshatra lord
        n_lord = self.chart.planets[planet_name].nakshatra_lord
        n_lord_house = self.chart.get_house_of_planet(n_lord)
        n_lord_is_house_lord = (n_lord == house_lord)
        
        nak_connection = (n_lord_house == house_num) or n_lord_is_house_lord
        
        return {
            "planet": planet_name,
            "target_house": house_num,
            "in_house": in_house,
            "is_lord": is_lord,
            "nakshatra_connection": nak_connection,
            "overall_promise": in_house or is_lord or nak_connection
        }
