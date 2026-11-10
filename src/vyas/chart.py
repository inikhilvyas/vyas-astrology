from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional

from vyas import constants

@dataclass(frozen=True)
class PlanetState:
    name: str
    longitude: float
    speed: float
    
    @property
    def sign_index(self) -> int:
        return int(self.longitude // 30.0) % 12
        
    @property
    def sign_name(self) -> str:
        return constants.SIGNS[self.sign_index]
        
    @property
    def sign_lord(self) -> str:
        return constants.SIGN_LORD[self.sign_index]
        
    @property
    def nakshatra_index(self) -> int:
        return int(self.longitude // constants.NAKSHATRA_SPAN) % 27
        
    @property
    def nakshatra_name(self) -> str:
        return constants.NAKSHATRAS[self.nakshatra_index]
        
    @property
    def nakshatra_lord(self) -> str:
        # The lords follow Vimshottari order starting from Ketu for Ashwini (index 0)
        return constants.VIMSHOTTARI_ORDER[self.nakshatra_index % 9]
        
    @property
    def pada(self) -> int:
        # Pada is 1 to 4
        return int((self.longitude % constants.NAKSHATRA_SPAN) // constants.PADA_SPAN) + 1
        
    @property
    def is_retrograde(self) -> bool:
        return self.speed < 0 and self.name not in ("Rahu", "Ketu")
        
    def d9_sign(self) -> int:
        """Calculates the Navamsha (D9) sign index."""
        # 1 pada = 1 navamsha. Total 108 navamshas in 360 deg.
        # Ashwini 1st pada is Aries. Ashwini 2nd pada is Taurus...
        total_padas = int(self.longitude // constants.PADA_SPAN)
        # Signs cycle every 12 padas. Aries starts at 0.
        return total_padas % 12
        
    def d10_sign(self) -> int:
        """Dashamsha (D10) sign index.

        Delegates to the single authoritative varga table so the two copies of
        this rule can never drift apart again (they did: this method and
        varga.py had independent implementations).
        """
        from vyas.varga import calculate_vargas_detailed
        return calculate_vargas_detailed(self.longitude)["D10"].sign_index


@dataclass(frozen=True)
class HouseState:
    house_num: int # 1 to 12
    sign_index: int
    
    @property
    def sign_name(self) -> str:
        return constants.SIGNS[self.sign_index]
        
    @property
    def lord(self) -> str:
        return constants.SIGN_LORD[self.sign_index]

@dataclass
class Chart:
    ascendant_longitude: float
    planets: Dict[str, PlanetState]
    
    @property
    def ascendant_sign(self) -> int:
        return int(self.ascendant_longitude // 30.0) % 12
        
    @property
    def ascendant_sign_index(self) -> int:
        return self.ascendant_sign
        
    @property
    def ascendant_nakshatra(self) -> int:
        return int(self.ascendant_longitude // constants.NAKSHATRA_SPAN) % 27
        
    @property
    def ascendant_pada(self) -> int:
        return int((self.ascendant_longitude % constants.NAKSHATRA_SPAN) // constants.PADA_SPAN) + 1
        
    def get_whole_sign_houses(self) -> Dict[int, HouseState]:
        """Returns houses 1-12 mapped to their signs using Whole Sign Houses."""
        houses = {}
        asc_sign = self.ascendant_sign
        for h in range(1, 13):
            sign_idx = (asc_sign + h - 1) % 12
            houses[h] = HouseState(house_num=h, sign_index=sign_idx)
        return houses
        
    def get_house_of_planet(self, planet_name: str) -> int:
        """Returns the house number (1-12) of a planet using Whole Sign Houses."""
        p_sign = self.planets[planet_name].sign_index
        asc_sign = self.ascendant_sign
        return (p_sign - asc_sign + 12) % 12 + 1
        
    def get_planets_in_house(self, house_num: int) -> List[str]:
        return [p.name for p in self.planets.values() if self.get_house_of_planet(p.name) == house_num]

    def get_houses_ruled_by_planet(self, planet_name: str) -> List[int]:
        """Returns the house numbers (1-12) ruled by the given planet."""
        asc_sign = self.ascendant_sign
        ruled = []
        for h in range(1, 13):
            sign_idx = (asc_sign + h - 1) % 12
            if constants.SIGN_LORD[sign_idx] == planet_name:
                ruled.append(h)
        return ruled

    def get_special_navamsha_summary(self) -> Dict[str, Any]:
        """Computes Pushkar Navamsha, Pushkar Bhaga, and Vargottama for Lagna and all planets."""
        items = {"Lagna": get_navamsha_analysis(self.ascendant_longitude)}
        for p_name, p in self.planets.items():
            items[p_name] = get_navamsha_analysis(p.longitude)
        return items


def get_navamsha_analysis(lon: float) -> Dict[str, Any]:
    """
    Computes D9 Navamsha sign, Pushkar Navamsha, Pushkar Bhaga, and Vargottama.
    Based on Brihat Parashara Hora Shastra, Jataka Parijata & Vidyamadhaveeyam.
    """
    from typing import Dict, Any
    total_padas = int(lon // constants.PADA_SPAN)
    nav_sign_idx = total_padas % 12
    sign_idx = int(lon // 30.0) % 12
    deg_in_sign = lon % 30.0
    nav_num_in_sign = int(deg_in_sign // constants.PADA_SPAN) + 1  # 1 to 9

    element = sign_idx % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water

    # 24 Pushkar Navamshas:
    is_pushkar_nav = False
    pushkar_desc = ""
    if element == 0:  # Agni / Fire: 7th (Libra - Venus) & 9th (Sagittarius - Jupiter)
        if nav_num_in_sign == 7:
            is_pushkar_nav = True
            pushkar_desc = "तुला नवांश (7वां नवांश, स्वामी: शुक्र)"
        elif nav_num_in_sign == 9:
            is_pushkar_nav = True
            pushkar_desc = "धनु नवांश (9वां नवांश, स्वामी: गुरु)"
    elif element == 1:  # Prithvi / Earth: 3rd (Pisces - Jupiter) & 5th (Taurus - Venus)
        if nav_num_in_sign == 3:
            is_pushkar_nav = True
            pushkar_desc = "मीन नवांश (3वां नवांश, स्वामी: गुरु)"
        elif nav_num_in_sign == 5:
            is_pushkar_nav = True
            pushkar_desc = "वृषभ नवांश (5वां नवांश, स्वामी: शुक्र)"
    elif element == 2:  # Vayu / Air: 6th (Pisces - Jupiter) & 8th (Taurus - Venus)
        if nav_num_in_sign == 6:
            is_pushkar_nav = True
            pushkar_desc = "मीन नवांश (6वां नवांश, स्वामी: गुरु)"
        elif nav_num_in_sign == 8:
            is_pushkar_nav = True
            pushkar_desc = "वृषभ नवांश (8वां नवांश, स्वामी: शुक्र)"
    elif element == 3:  # Jala / Water: 1st (Cancer - Moon) & 3rd (Virgo - Mercury)
        if nav_num_in_sign == 1:
            is_pushkar_nav = True
            pushkar_desc = "कर्क नवांश (1वां नवांश, स्वामी: चन्द्र)"
        elif nav_num_in_sign == 3:
            is_pushkar_nav = True
            pushkar_desc = "कन्या नवांश (3वां नवांश, स्वामी: बुध)"

    # 12 Pushkar Bhagas (exact sacred degrees):
    # Aries: 21°, Taurus: 14°, Gemini: 18°, Cancer: 8°, Leo: 19°, Virgo: 9°,
    # Libra: 24°, Scorpio: 11°, Sagittarius: 23°, Capricorn: 14°, Aquarius: 19°, Pisces: 9°
    pushkar_bhaga_degrees = [21.0, 14.0, 18.0, 8.0, 19.0, 9.0, 24.0, 11.0, 23.0, 14.0, 19.0, 9.0]
    pb_target = pushkar_bhaga_degrees[sign_idx]
    is_pushkar_bhaga = abs(deg_in_sign - pb_target) <= 1.0

    # Vargottama: Same sign in D1 (Rashi) and D9 (Navamsha)
    is_vargottama = (sign_idx == nav_sign_idx)

    return {
        "longitude": lon,
        "sign_idx": sign_idx,
        "sign_name": constants.SIGNS_HI[sign_idx],
        "sign_name_en": constants.SIGNS[sign_idx],
        "deg_in_sign": deg_in_sign,
        "nav_num": nav_num_in_sign,
        "nav_sign_idx": nav_sign_idx,
        "nav_sign_name": constants.SIGNS_HI[nav_sign_idx],
        "nav_sign_name_en": constants.SIGNS[nav_sign_idx],
        "nav_lord": constants.SIGN_LORD[nav_sign_idx],
        "nav_lord_hi": constants.PLANETS_HI.get(constants.SIGN_LORD[nav_sign_idx], constants.SIGN_LORD[nav_sign_idx]),
        "is_pushkar_nav": is_pushkar_nav,
        "pushkar_desc": pushkar_desc,
        "is_pushkar_bhaga": is_pushkar_bhaga,
        "pushkar_bhaga_deg": pb_target,
        "is_vargottama": is_vargottama
    }

