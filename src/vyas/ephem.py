"""Sidereal planetary positions from the JPL DE440s ephemeris (via Skyfield).

Ayanamsa: Lahiri (Chitrapaksha), fixed for the whole analysis (codex §4).
Rahu: mean node (Ketu exactly opposite). Both choices are recorded in output.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

AYANAMSA_NAME = "Lahiri"
NODE_MODEL = "mean"
_LAHIRI_T0_JD = 2435553.5          # 1956-09-22, Lahiri reference epoch
_LAHIRI_AT_T0 = 23.245524743       # degrees at that epoch (Swiss Ephemeris definition)

# Selectable ayanamsas: (reference JD, value in degrees at that epoch) – Swiss Ephemeris definitions.
AYANAMSAS = {
    "Lahiri": (_LAHIRI_T0_JD, _LAHIRI_AT_T0),
    "KP": (2415020.0, 22.363889),        # Krishnamurti, epoch 1900-01-00.5
    "Raman": (2415020.0, 21.014444),     # B.V. Raman, epoch 1900-01-00.5
}


def set_ayanamsa(name: str) -> None:
    """Select the ayanamsa used by every sidereal calculation in this module."""
    global AYANAMSA_NAME
    if name not in AYANAMSAS:
        raise ValueError(f"Unknown ayanamsa {name!r}; choose from {list(AYANAMSAS)}")
    AYANAMSA_NAME = name

_ts = None
_eph = None


class EphemerisMissing(RuntimeError):
    pass


def _data_dir() -> Path:
    env = os.environ.get("VYAS_DATA_DIR")
    return Path(env) if env else Path(__file__).resolve().parents[2] / "data"


def _load():
    global _ts, _eph
    if _eph is None:
        from skyfield.api import Loader
        f = _data_dir() / "de440s.bsp"
        if not f.is_file() or f.stat().st_size < 30_000_000:
            raise EphemerisMissing(
                f"Ephemeris file missing/incomplete: {f}. Download "
                "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp"
            )
        load = Loader(str(_data_dir()), verbose=False)
        _ts = load.timescale(builtin=True)
        _eph = load("de440s.bsp")
    return _ts, _eph


def julian_day_ut(dt_utc: datetime) -> float:
    ts, _ = _load()
    d = dt_utc.astimezone(timezone.utc)
    return ts.utc(d.year, d.month, d.day, d.hour, d.minute,
                  d.second + d.microsecond / 1e6).ut1 if False else \
        ts.utc(d.year, d.month, d.day, d.hour, d.minute,
               d.second + d.microsecond / 1e6).tt - 0.0  # TT days, see note


def _t(dt_utc: datetime):
    ts, _ = _load()
    d = dt_utc.astimezone(timezone.utc)
    return ts.utc(d.year, d.month, d.day, d.hour, d.minute,
                  d.second + d.microsecond / 1e6)


def precession_arcsec(T: float) -> float:
    """General precession in longitude, arcsec, T = Julian centuries from J2000."""
    return 5029.0966 * T + 1.11113 * T * T


def ayanamsa_deg(jd_tt: float, name: str | None = None) -> float:
    """Ayanamsa in degrees at the given Julian day for the selected (or given) system."""
    jd0, val0 = AYANAMSAS[name or AYANAMSA_NAME]
    t0 = (jd0 - 2451545.0) / 36525.0
    t = (jd_tt - 2451545.0) / 36525.0
    return val0 + (precession_arcsec(t) - precession_arcsec(t0)) / 3600.0


def lahiri_ayanamsa(jd_tt: float) -> float:
    """Active ayanamsa (name kept for backward compatibility)."""
    return ayanamsa_deg(jd_tt)


def obliquity_deg(jd_tt: float) -> float:
    T = (jd_tt - 2451545.0) / 36525.0
    return 23.439291111 - 0.0130042 * T - 1.64e-7 * T * T + 5.04e-7 * T ** 3


def ascendant_tropical(ramc_deg: float, lat_deg: float, eps_deg: float) -> float:
    r, phi, e = map(math.radians, (ramc_deg, lat_deg, eps_deg))
    y = math.cos(r)
    x = -(math.sin(r) * math.cos(e) + math.tan(phi) * math.sin(e))
    return math.degrees(math.atan2(y, x)) % 360.0


def mean_node_tropical(jd_tt: float) -> float:
    T = (jd_tt - 2451545.0) / 36525.0
    return (125.0445479 - 1934.1362891 * T + 0.0020754 * T * T
            + T ** 3 / 467441.0) % 360.0


@dataclass(frozen=True)
class RawPosition:
    longitude: float      # sidereal, degrees 0-360
    speed: float          # deg/day, negative => retrograde
    latitude: float = 0.0


_BODIES = {"Sun": "sun", "Moon": "moon", "Mars": "mars barycenter",
           "Mercury": "mercury barycenter", "Jupiter": "jupiter barycenter",
           "Venus": "venus barycenter", "Saturn": "saturn barycenter"}


def _tropical_lon(name: str, t) -> float:
    _, eph = _load()
    from skyfield.framelib import ecliptic_frame
    obs = eph["earth"].at(t).observe(eph[_BODIES[name]]).apparent()
    lat, lon, _ = obs.frame_latlon(ecliptic_frame)   # true ecliptic of date
    return lon.degrees % 360.0


def planet_positions(dt_utc: datetime) -> dict[str, RawPosition]:
    """Sidereal longitudes + daily speed for the nine grahas."""
    from datetime import timedelta
    t = _t(dt_utc)
    jd = t.tt
    ay = lahiri_ayanamsa(jd)
    t2 = _t(dt_utc + timedelta(hours=12))
    jd2 = t2.tt
    ay2 = lahiri_ayanamsa(jd2)
    out: dict[str, RawPosition] = {}
    for name in _BODIES:
        l1 = (_tropical_lon(name, t) - ay) % 360.0
        l2 = (_tropical_lon(name, t2) - ay2) % 360.0
        d = ((l2 - l1 + 180.0) % 360.0) - 180.0
        out[name] = RawPosition(l1, d * 2.0)
    n1 = (mean_node_tropical(jd) - ay) % 360.0
    n2 = (mean_node_tropical(jd2) - ay2) % 360.0
    dn = (((n2 - n1) + 180.0) % 360.0 - 180.0) * 2.0
    out["Rahu"] = RawPosition(n1, dn)
    out["Ketu"] = RawPosition((n1 + 180.0) % 360.0, dn)
    return out


def sidereal_lon(name: str, dt_utc: datetime) -> float:
    """Sidereal longitude of a single graha (fast path for searches)."""
    t = _t(dt_utc)
    ay = lahiri_ayanamsa(t.tt)
    if name in ("Rahu", "Ketu"):
        n = (mean_node_tropical(t.tt) - ay) % 360.0
        return n if name == "Rahu" else (n + 180.0) % 360.0
    return (_tropical_lon(name, t) - ay) % 360.0


def ascendant_sidereal(dt_utc: datetime, lat: float, lon: float) -> float:
    t = _t(dt_utc)
    ramc = (t.gast * 15.0 + lon) % 360.0       # apparent sidereal time -> degrees
    asc = ascendant_tropical(ramc, lat, obliquity_deg(t.tt))
    return (asc - lahiri_ayanamsa(t.tt)) % 360.0
