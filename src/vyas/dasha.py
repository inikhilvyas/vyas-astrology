"""Vimshottari Dasha Engine with 5-Level Micro Precision (MD, AD, PD, SD, PrD).

Calculates exact Vimshottari dasha hierarchy from birth down to:
- Level 1: Mahadasha (MD)
- Level 2: Antardasha (AD)
- Level 3: Pratyantardasha (PD)
- Level 4: Sookshma Dasha (SD)
- Level 5: Praana Dasha (PrD)

Provides precise timing down to the minute/second, and resolves the running 5-fold
dasha active at any given moment in time.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple

from vyas import constants

@dataclass
class DashaNode:
    lord: str
    start_date: datetime
    end_date: datetime
    level: int  # 1=MD, 2=AD, 3=PD, 4=SD, 5=PrD
    level_name: str
    duration_days: float
    sub_dashas: List[DashaNode] = field(default_factory=list)

    @property
    def start_str(self) -> str:
        return self.start_date.strftime("%d/%m/%Y %H:%M:%S")

    @property
    def end_str(self) -> str:
        return self.end_date.strftime("%d/%m/%Y %H:%M:%S")

LEVEL_NAMES = {
    1: "Mahadasha (MD)",
    2: "Antardasha (AD)",
    3: "Pratyantardasha (PD)",
    4: "Sookshma Dasha (SD)",
    5: "Praana Dasha (PrD)"
}

class VimshottariDasha:
    def __init__(self, moon_longitude: float, birth_date: datetime):
        self.moon_longitude = moon_longitude % 360.0
        self.birth_date = birth_date
        
        # Calculate birth nakshatra and balance
        nakshatra_idx = int(self.moon_longitude // constants.NAKSHATRA_SPAN) % 27
        nakshatra_start_deg = nakshatra_idx * constants.NAKSHATRA_SPAN
        deg_passed = self.moon_longitude - nakshatra_start_deg
        deg_remaining = constants.NAKSHATRA_SPAN - deg_passed
        
        self.starting_lord_idx = nakshatra_idx % 9
        self.birth_lord = constants.VIMSHOTTARI_ORDER[self.starting_lord_idx]
        self.proportion_remaining = deg_remaining / constants.NAKSHATRA_SPAN
        
        # Dasha balance at birth (Years, Months, Days)
        total_lord_years = constants.VIMSHOTTARI_YEARS[self.birth_lord]
        bal_years_float = total_lord_years * self.proportion_remaining
        self.balance_years = int(bal_years_float)
        rem_months = (bal_years_float - self.balance_years) * 12.0
        self.balance_months = int(rem_months)
        rem_days = (rem_months - self.balance_months) * 30.4375
        self.balance_days = int(round(rem_days))
        self.balance_str = f"{self.birth_lord}: {self.balance_years}Y {self.balance_months}M {self.balance_days}D"

    def _add_years(self, dt: datetime, years: float) -> datetime:
        return dt + timedelta(days=years * constants.YEAR_DAYS)

    def calculate_mahadashas(self, num_cycles: int = 1) -> List[DashaNode]:
        """Calculates Mahadashas (MD)."""
        dashas: List[DashaNode] = []
        current_date = self.birth_date
        
        # First Mahadasha (partial)
        first_lord = self.birth_lord
        first_actual_years = constants.VIMSHOTTARI_YEARS[first_lord] * self.proportion_remaining
        end_date = self._add_years(current_date, first_actual_years)
        
        dur_days = (end_date - current_date).total_seconds() / 86400.0
        dashas.append(DashaNode(
            lord=first_lord,
            start_date=current_date,
            end_date=end_date,
            level=1,
            level_name=LEVEL_NAMES[1],
            duration_days=dur_days
        ))
        current_date = end_date
        
        total_lords = 9 * num_cycles
        for i in range(1, total_lords):
            lord = constants.VIMSHOTTARI_ORDER[(self.starting_lord_idx + i) % 9]
            years = constants.VIMSHOTTARI_YEARS[lord]
            end_date = self._add_years(current_date, years)
            dur_days = (end_date - current_date).total_seconds() / 86400.0
            
            dashas.append(DashaNode(
                lord=lord,
                start_date=current_date,
                end_date=end_date,
                level=1,
                level_name=LEVEL_NAMES[1],
                duration_days=dur_days
            ))
            current_date = end_date
            
        return dashas

    def expand_sub_dashas(self, parent_node: DashaNode, target_level: int = 2) -> List[DashaNode]:
        """
        Expands the next level of sub-dashas (AD, PD, SD, PrD) inside parent_node.
        """
        if parent_node.level >= 5 or parent_node.level >= target_level:
            return parent_node.sub_dashas

        parent_seconds = (parent_node.end_date - parent_node.start_date).total_seconds()
        start_idx = constants.VIMSHOTTARI_ORDER.index(parent_node.lord)
        
        sub_nodes: List[DashaNode] = []
        curr_dt = parent_node.start_date
        next_level = parent_node.level + 1
        
        for i in range(9):
            lord = constants.VIMSHOTTARI_ORDER[(start_idx + i) % 9]
            prop = constants.VIMSHOTTARI_YEARS[lord] / 120.0
            span_seconds = parent_seconds * prop
            
            if i == 8:
                next_dt = parent_node.end_date
            else:
                next_dt = curr_dt + timedelta(seconds=span_seconds)
                
            dur_days = (next_dt - curr_dt).total_seconds() / 86400.0
            child = DashaNode(
                lord=lord,
                start_date=curr_dt,
                end_date=next_dt,
                level=next_level,
                level_name=LEVEL_NAMES[next_level],
                duration_days=dur_days
            )
            sub_nodes.append(child)
            curr_dt = next_dt
            
        parent_node.sub_dashas = sub_nodes
        return sub_nodes

    def get_running_dasha(self, target_date: datetime = None, max_depth: int = 5) -> Dict[str, dict]:
        """
        Pinpoints the active MD, AD, PD, SD, PrD running at target_date down to the second.
        """
        if target_date is None:
            target_date = datetime.now()
        
        # Harmonize timezone awareness between target_date and self.birth_date
        if hasattr(self.birth_date, 'tzinfo') and self.birth_date.tzinfo is not None:
            if target_date.tzinfo is None:
                target_date = target_date.replace(tzinfo=self.birth_date.tzinfo)
            else:
                target_date = target_date.astimezone(self.birth_date.tzinfo)
        else:
            if target_date.tzinfo is not None:
                target_date = target_date.replace(tzinfo=None)

        md_list = self.calculate_mahadashas(num_cycles=2)
        
        active_chain: Dict[str, dict] = {}
        curr_node = None
        
        # 1. Find active MD
        for node in md_list:
            if node.start_date <= target_date < node.end_date:
                curr_node = node
                break
                
        if not curr_node:
            curr_node = md_list[-1]
            
        active_chain["MD"] = {
            "lord": curr_node.lord,
            "start": curr_node.start_str,
            "end": curr_node.end_str,
            "node": curr_node
        }
        
        # 2. Drill down through levels AD, PD, SD, PrD
        level_keys = ["AD", "PD", "SD", "PrD"]
        for lvl_idx in range(2, max_depth + 1):
            subs = self.expand_sub_dashas(curr_node, target_level=lvl_idx)
            found_sub = None
            for s in subs:
                if s.start_date <= target_date < s.end_date:
                    found_sub = s
                    break
            if not found_sub:
                found_sub = subs[-1]
                
            key = level_keys[lvl_idx - 2]
            active_chain[key] = {
                "lord": found_sub.lord,
                "start": found_sub.start_str,
                "end": found_sub.end_str,
                "node": found_sub
            }
            curr_node = found_sub
            
        return active_chain

    def get_dasha_at(self, target_date: datetime, max_depth: int = 5) -> Dict[str, dict]:
        """Alias for get_running_dasha."""
        return self.get_running_dasha(target_date, max_depth=max_depth)
