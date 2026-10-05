"""Gochar (transit) engine for VYAS.

Classical basis (Phaladeepika ch.26 / Muhurta Chintamani):
* Transit results are judged from the natal Moon sign (Chandra Lagna); the
  house from the natal Lagna is reported as a secondary reference.
* Each planet has favourable houses from the Moon, each cancelled by a planet
  transiting its *Vedha* house (Sun–Saturn and Moon–Mercury do not obstruct
  each other).
* Tara Bala: 9-fold count of the transit nakshatra from the janma nakshatra.
* Shani: Sade-Sati (12/1/2 from Moon), Kantaka/Ardha-ashtama (4th), Ashtama (8th).
* Sign ingress dates are found by bisection to the second.

A transit is a TRIGGER, never a promise by itself (VYAS codex §1.2).
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone

from . import constants as C
from . import ephem

# favourable house -> vedha house, counted from natal Moon
VEDHA = {
    "Sun": {3: 9, 6: 12, 10: 4, 11: 5},
    "Moon": {1: 5, 3: 9, 6: 12, 7: 2, 10: 4, 11: 8},
    "Mars": {3: 12, 6: 9, 11: 5},
    "Mercury": {2: 5, 4: 3, 6: 9, 8: 1, 10: 8, 11: 12},
    "Jupiter": {2: 12, 5: 4, 7: 3, 9: 10, 11: 8},
    "Venus": {1: 8, 2: 7, 3: 1, 4: 10, 5: 9, 8: 5, 9: 11, 11: 6, 12: 3},
    "Saturn": {3: 12, 6: 9, 11: 5},
    "Rahu": {3: 12, 6: 9, 11: 5},
    "Ketu": {3: 12, 6: 9, 11: 5},
}
_NO_VEDHA_PAIRS = {frozenset({"Sun", "Saturn"}), frozenset({"Moon", "Mercury"})}

TARAS = ["Janma", "Sampat", "Vipat", "Kshema", "Pratyari", "Sadhaka", "Vadha",
         "Mitra", "Ati-Mitra"]
TARA_GOOD = {"Sampat", "Kshema", "Sadhaka", "Mitra", "Ati-Mitra"}


def _house(from_sign: int, sign: int) -> int:
    return (sign - from_sign) % 12 + 1


@dataclass
class TransitRow:
    planet: str
    sign: str
    degree: str
    nakshatra: str
    pada: int
    retro: bool
    house_from_moon: int
    house_from_lagna: int
    tara: str
    favourable: bool
    vedha_by: str
    verdict: str
    next_ingress: str

    def as_dict(self):
        return asdict(self)


def _fmt_deg(lon: float) -> str:
    d = lon % 30
    return f"{int(d):02d}°{int((d % 1) * 60):02d}'"


def _sign_of(name: str, dt_utc: datetime) -> int:
    return int(ephem.sidereal_lon(name, dt_utc) // 30)


def next_ingress(name: str, start_utc: datetime, max_days: int = 1200) -> datetime | None:
    """Next sign change of *name* after *start_utc* (handles retrograde re-entry)."""
    s0 = _sign_of(name, start_utc)
    step = {"Moon": 0.25, "Sun": 2, "Mercury": 1, "Venus": 1, "Mars": 2}.get(name, 5)
    t = start_utc
    end = start_utc + timedelta(days=max_days)
    while t < end:
        t2 = t + timedelta(days=step)
        if _sign_of(name, t2) != s0:
            lo, hi = t, t2
            while (hi - lo).total_seconds() > 1:
                mid = lo + (hi - lo) / 2
                if _sign_of(name, mid) == s0:
                    lo = mid
                else:
                    hi = mid
            return hi
        t = t2
    return None


def transits(at_local: datetime, tz_hours: float, natal_moon_lon: float,
             natal_asc_lon: float, with_ingress: bool = True) -> list[TransitRow]:
    tz = timezone(timedelta(hours=tz_hours))
    if at_local.tzinfo is None:
        at_local = at_local.replace(tzinfo=tz)
    at_u = at_local.astimezone(timezone.utc)
    pos = ephem.planet_positions(at_u)

    moon_sign = int(natal_moon_lon // 30)
    asc_sign = int(natal_asc_lon // 30)
    janma_nak = int(natal_moon_lon // C.NAKSHATRA_SPAN) % 27

    houses = {n: _house(moon_sign, int(p.longitude // 30)) for n, p in pos.items()}
    rows: list[TransitRow] = []
    for name in C.PLANETS:
        p = pos[name]
        sign = int(p.longitude // 30)
        nak = int(p.longitude // C.NAKSHATRA_SPAN) % 27
        pada = int((p.longitude % C.NAKSHATRA_SPAN) // C.PADA_SPAN) + 1
        h = houses[name]
        tara = TARAS[(nak - janma_nak) % 9]
        fav = h in VEDHA[name]
        vedha_by = ""
        if fav:
            vh = VEDHA[name][h]
            blockers = [o for o, oh in houses.items()
                        if o != name and oh == vh
                        and frozenset({o, name}) not in _NO_VEDHA_PAIRS
                        and not (name in ("Rahu", "Ketu") and o in ("Rahu", "Ketu"))]
            vedha_by = ", ".join(blockers)
        if fav and not vedha_by:
            verdict = "Favourable"
        elif fav:
            verdict = "Favourable but obstructed (Vedha)"
        else:
            verdict = "Unfavourable"
        ing = ""
        if with_ingress and name != "Ketu":
            t = next_ingress(name, at_u)
            if t:
                dest = _sign_of(name, t + timedelta(minutes=1))
                ing = f"{C.SIGNS[dest]} on {t.astimezone(tz).strftime('%d/%m/%Y %H:%M')}"
        rows.append(TransitRow(
            planet=name, sign=C.SIGNS[sign], degree=_fmt_deg(p.longitude),
            nakshatra=C.NAKSHATRAS[nak], pada=pada,
            retro=p.speed < 0 and name not in ("Rahu", "Ketu"),
            house_from_moon=h, house_from_lagna=_house(asc_sign, sign),
            tara=tara, favourable=fav and not vedha_by, vedha_by=vedha_by,
            verdict=verdict, next_ingress=ing))
    return rows


def shani_status(at_local: datetime, tz_hours: float, natal_moon_lon: float) -> dict:
    """Sade-Sati / Dhaiya status with the phase and the window that contains *at_local*."""
    tz = timezone(timedelta(hours=tz_hours))
    if at_local.tzinfo is None:
        at_local = at_local.replace(tzinfo=tz)
    at_u = at_local.astimezone(timezone.utc)
    moon_sign = int(natal_moon_lon // 30)
    sat_sign = _sign_of("Saturn", at_u)
    h = _house(moon_sign, sat_sign)
    phase = {12: "Sade-Sati – Rising phase (12th from Moon)",
             1: "Sade-Sati – Peak phase (over Moon)",
             2: "Sade-Sati – Setting phase (2nd from Moon)",
             4: "Kantaka / Ardhashtama Shani (Dhaiya – 4th)",
             8: "Ashtama Shani (Dhaiya – 8th)"}.get(h, "No Sade-Sati / Dhaiya")
    nxt = next_ingress("Saturn", at_u, max_days=3 * 365)
    return {
        "saturn_sign": C.SIGNS[sat_sign],
        "house_from_moon": h,
        "status": phase,
        "saturn_next_sign_change": nxt.astimezone(tz).strftime("%d/%m/%Y %H:%M") if nxt else "-",
    }


def get_current_transit_positions(at_local: datetime = None, tz_hours: float = 5.5) -> dict:
    """Returns current real-time transit positions as a dict of PlanetState objects."""
    from .chart import PlanetState
    if at_local is None:
        at_local = datetime.now()
    tz = timezone(timedelta(hours=tz_hours))
    if at_local.tzinfo is None:
        at_local = at_local.replace(tzinfo=tz)
    at_u = at_local.astimezone(timezone.utc)
    pos = ephem.planet_positions(at_u)
    return {name: PlanetState(name=name, longitude=p.longitude, speed=p.speed) for name, p in pos.items()}

