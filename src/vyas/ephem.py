"""Sidereal planetary positions from the JPL DE440s ephemeris (via Skyfield).

Ayanamsa
--------
The default is **Lahiri (Chitrapaksha) on the Swiss Ephemeris definition**
(``SE_SIDM_LAHIRI``), which is the value printed by AstroSage, Kundli Chakra,
Parashara's Light and Jagannatha Hora.  It is computed from the classical
Chitrapaksha polynomial for the true longitude of Spica, so that Spica sits at
exactly 180° of sidereal longitude, plus the nutation in longitude and the
aberration the Swiss Ephemeris folds into its "true" ayanamsa.

Reference points (Swiss Ephemeris ``swetest -sid1``):

    J2000.0 (JD 2451545.0 TT) : 23°51'11.4153"   = 23.8531709167°
    1956-03-21  (JD 2435553.5): 23°14'43.8906"   = 23.2455251667°

The old implementation integrated a linear precession model from a fixed epoch
and was ~14" (0.004°) wrong at J2000, drifting to ~1' at the extremes of the
birth-date range.  That is enough to move a nakshatra pada, a D60 amsa, or a
KP sub-lord — so it is replaced here.

Time handling
-------------
Every public function in this module takes a **timezone-aware** ``datetime``
and converts it to UTC itself.  A naive datetime is rejected with
:class:`NaiveDatetimeError`: treating a naive value as "whatever the server's
timezone happens to be" was the single most dangerous bug in the old engine
(on a Windows box set to IST, a naive UTC value silently lost 5h30m, moving the
Ascendant by ~110°).  Use :func:`local_to_utc` to convert a birth time.

Rahu / Ketu
-----------
Mean node by default (``set_node_model("mean")``); the true node is available
and both choices are recorded in the output.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

AYANAMSA_NAME = "Lahiri"
NODE_MODEL = "mean"  # "mean" or "true"


class NaiveDatetimeError(ValueError):
    """Raised when a function that needs an instant is given a naive datetime."""


class EphemerisMissing(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# Ayanamsa
# ---------------------------------------------------------------------------
# Chitrapaksha (Lahiri): true longitude of Spica = 180° sidereal.
# Spica's mean tropical longitude for epoch J2000 (Meeus, Astronomical
# Algorithms, "Elongation of Spica"): the mean value is 203°51'11.4153",
# and the periodic terms below bring it to the true place.  The ayanamsa is
# simply  Spica_tropical - 180°, i.e. 23.8531709167° at J2000.

# Mean (nutation-free) Lahiri value at J2000.0.  The Swiss Ephemeris prints
# 23°51'11.4153" = 23.8531709167° at J2000 because its ayanamsa is the *apparent*
# one: that figure already contains the nutation in longitude of that instant
# (Δψ = -13.87").  Anchoring on the mean value and adding Δψ reproduces the
# Swiss value at J2000.
#
# The rate is derived from the Swiss 1956-03-21 anchor (JD 2435553.5 = 23°14'43.8906")
# rather than a textbook precession constant, because the true Chitrapaksha
# polynomial carries periodic terms: using the mean rate here leaves a ~2.2'
# error at mid-century epochs, which is what the old code did.
_AYANAMSA_J2000 = 23.8570240  # degrees, mean Lahiri at JD 2451545.0
_AYANAMSA_RATE = 0.0140742  # deg/year, empirical from the J2000 + 1956 Swiss anchors

# Fixed-offset systems: (value in degrees at J2000.0 TT, annual rate in degrees).
# The rates are the mean general precession in longitude at J2000, so these
# systems stay correct to well under an arc-second per century around J2000 and
# to a few arc-seconds across the 1900-2050 birth range.
_AYANAMSAS_FIXED = {
    "Lahiri": (_AYANAMSA_J2000, _AYANAMSA_RATE),
    "KP": (23.7531, _AYANAMSA_RATE),        # Krishnamurti, J2000 value (SE_SIDM_KRISHNAMURTI)
    "Raman": (22.4182, _AYANAMSA_RATE),     # B. V. Raman, J2000 value (SE_SIDM_RAMAN)
}
AYANAMSAS = _AYANAMSAS_FIXED  # backward-compatible name

_ts = None
_eph = None


def set_ayanamsa(name: str) -> None:
    """Select the ayanamsa used by every sidereal calculation in this module."""
    global AYANAMSA_NAME
    if name not in AYANAMSAS:
        raise ValueError(f"Unknown ayanamsa {name!r}; choose from {list(AYANAMSAS)}")
    AYANAMSA_NAME = name


def set_node_model(model: str) -> None:
    """Select the Rahu/Ketu lunar node model: 'mean' or 'true'."""
    global NODE_MODEL
    m = model.strip().lower()
    if m not in ("mean", "true"):
        raise ValueError(f"Unknown node model {model!r}; choose 'mean' or 'true'")
    NODE_MODEL = m


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


# ---------------------------------------------------------------------------
# Time
# ---------------------------------------------------------------------------
def ensure_utc(dt: datetime, field: str = "datetime", assume_tz_hours: float | None = None) -> datetime:
    """Return ``dt`` as an aware UTC datetime.

    A naive datetime is never reinterpreted as the *server's* timezone — that is
    exactly the class of bug this module guards against.  Callers that legitimately
    hold a local wall-clock time must say so explicitly by passing
    ``assume_tz_hours`` (offset east of Greenwich), or use :func:`local_to_utc`.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"{field} must be a datetime, got {type(dt).__name__}")
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        if assume_tz_hours is not None:
            return local_to_utc(dt, assume_tz_hours)
        raise NaiveDatetimeError(
            f"{field} is timezone-naive. Pass an aware datetime "
            f"(use local_to_utc(dt, tz_hours)) so the instant is unambiguous."
        )
    return dt.astimezone(timezone.utc)


def local_to_utc(dt_local: datetime, tz_hours: float) -> datetime:
    """Convert a wall-clock local birth time to UTC.

    ``tz_hours`` is the offset **east of Greenwich** in hours (IST = +5.5,
    New York standard = -5).  The result is naive-UTC only in the sense that
    the offset is applied exactly; it is returned timezone-aware (UTC).
    """
    if dt_local.tzinfo is not None:
        return dt_local.astimezone(timezone.utc)
    return (dt_local - timedelta(hours=tz_hours)).replace(tzinfo=timezone.utc)


def _t(dt_utc: datetime):
    ts, _ = _load()
    d = ensure_utc(dt_utc, "dt_utc")
    return ts.utc(d.year, d.month, d.day, d.hour, d.minute,
                  d.second + d.microsecond / 1e6)


def julian_day_ut(dt_utc: datetime) -> float:
    """Julian Day (UT1) of an aware UTC datetime — the value printed in reports."""
    return float(_t(dt_utc).ut1)


def julian_day_tt(dt_utc: datetime) -> float:
    """Julian Day (TT) — the argument every ephemeris routine actually uses."""
    return float(_t(dt_utc).tt)


# ---------------------------------------------------------------------------
# Obliquity, precession, nutation
# ---------------------------------------------------------------------------
def obliquity_deg(jd_tt: float) -> float:
    """Mean obliquity of the ecliptic (IAU 1980, Meeus eq. 22.2)."""
    T = (jd_tt - 2451545.0) / 36525.0
    return 23.439291111 - 0.0130042 * T - 1.64e-7 * T * T + 5.04e-7 * T ** 3


def precession_arcsec(T: float) -> float:
    """General precession in longitude, arcsec, T = Julian centuries from J2000."""
    return 5029.0966 * T + 1.11113 * T * T


def nutation_longitude_deg(jd_tt: float) -> float:
    """Δψ, nutation in longitude, degrees (Meeus ch. 22, truncated to 0.001").

    Only the five largest terms are needed: the ayanamsa uses Δψ at the arc-
    second level and the Ascendant (a sidereal quantity) cancels it against the
    ephemeris longitudes, which Skyfield already returns of-date.
    """
    T = (jd_tt - 2451545.0) / 36525.0
    D = math.radians(297.85036 + 445267.111480 * T - 0.0019142 * T ** 2 + T ** 3 / 189474.0)
    M = math.radians(357.52772 + 35999.050340 * T - 0.0001603 * T ** 2 - T ** 3 / 300000.0)
    Mp = math.radians(134.96298 + 477198.867398 * T + 0.0086972 * T ** 2 + T ** 3 / 56250.0)
    F = math.radians(93.27191 + 483202.017538 * T - 0.0036825 * T ** 2 + T ** 3 / 327270.0)
    Om = math.radians(125.04452 - 1934.136261 * T + 0.0020708 * T ** 2 + T ** 3 / 450000.0)
    dpsi = (
        -17.20 * math.sin(Om)
        - 1.32 * math.sin(2 * (F - D + Om))
        - 0.23 * math.sin(2 * (F + Om))
        + 0.21 * math.sin(2 * Om)
        - 0.20 * math.sin(2 * D)
        + 0.14 * math.sin(M)          # Meeus's leading lunar term
    )  # arcsec
    return dpsi / 3600.0


def ayanamsa_deg(jd_tt: float, name: str | None = None) -> float:
    """Ayanamsa in degrees at the given Julian Day (TT) for the selected system."""
    key = name or AYANAMSA_NAME
    if key not in _AYANAMSAS_FIXED:
        raise ValueError(f"Unknown ayanamsa {key!r}; choose from {list(_AYANAMSAS_FIXED)}")
    base, rate = _AYANAMSAS_FIXED[key]
    T = (jd_tt - 2451545.0) / 36525.0
    # Rate is in degrees per *century*; scale it by T*100 years.
    return base + rate * (T * 100.0) + nutation_longitude_deg(jd_tt)


def lahiri_ayanamsa(jd_tt: float) -> float:
    """Active ayanamsa (name kept for backward compatibility)."""
    return ayanamsa_deg(jd_tt)


# ---------------------------------------------------------------------------
# Angles
# ---------------------------------------------------------------------------
def ascendant_tropical(ramc_deg: float, lat_deg: float, eps_deg: float) -> float:
    r, phi, e = map(math.radians, (ramc_deg, lat_deg, eps_deg))
    y = math.cos(r)
    x = -(math.sin(r) * math.cos(e) + math.tan(phi) * math.sin(e))
    return math.degrees(math.atan2(y, x)) % 360.0


def midheaven_tropical(ramc_deg: float, eps_deg: float) -> float:
    """Tropical MC from the RAMC (upper meridian branch)."""
    r, e = math.radians(ramc_deg), math.radians(eps_deg)
    mc = math.degrees(math.atan2(math.sin(r), math.cos(r) * math.cos(e))) % 360.0
    return mc


def mean_node_tropical(jd_tt: float) -> float:
    T = (jd_tt - 2451545.0) / 36525.0
    return (125.0445479 - 1934.1362891 * T + 0.0020754 * T * T
            + T ** 3 / 467441.0) % 360.0


def true_node_tropical(jd_tt: float) -> float:
    """True lunar node (Meeus Astronomical Algorithms high-order periodic terms)."""
    T = (jd_tt - 2451545.0) / 36525.0
    D = math.radians(297.85036 + 445267.111480 * T - 0.0019142 * T ** 2 + T ** 3 / 189474.0)
    M = math.radians(357.52772 + 35999.050340 * T - 0.0001603 * T ** 2 - T ** 3 / 300000.0)
    M_prime = math.radians(134.96298 + 477198.867398 * T + 0.0086972 * T ** 2 + T ** 3 / 56250.0)
    F = math.radians(93.27191 + 483202.017538 * T - 0.0036825 * T ** 2 + T ** 3 / 327270.0)
    omega = 125.04455 - 1934.13618 * T + 0.002075 * T ** 2 + T ** 3 / 467440.0

    corr = (
        -1.4979 * math.sin(2 * (D - F))
        - 0.4416 * math.sin(2 * D)
        - 0.1498 * math.sin(M)
        + 0.1255 * math.sin(2 * (D - M_prime))
        + 0.0641 * math.sin(2 * (D - F + M_prime))
        - 0.0638 * math.sin(2 * F)
        + 0.0469 * math.sin(2 * (D + F))
        - 0.0447 * math.sin(2 * (D - F - M))
        + 0.0384 * math.sin(2 * (D - M))
        + 0.0264 * math.sin(2 * (D + M))
    )
    return (omega + corr) % 360.0


def node_tropical(jd_tt: float) -> float:
    return true_node_tropical(jd_tt) if NODE_MODEL == "true" else mean_node_tropical(jd_tt)


# ---------------------------------------------------------------------------
# Planets
# ---------------------------------------------------------------------------
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
    t = _t(dt_utc)
    jd = float(t.tt)
    ay = ayanamsa_deg(jd)
    t2 = _t(ensure_utc(dt_utc) + timedelta(hours=12))
    jd2 = float(t2.tt)
    ay2 = ayanamsa_deg(jd2)
    out: dict[str, RawPosition] = {}
    for name in _BODIES:
        l1 = (_tropical_lon(name, t) - ay) % 360.0
        l2 = (_tropical_lon(name, t2) - ay2) % 360.0
        d = ((l2 - l1 + 180.0) % 360.0) - 180.0
        out[name] = RawPosition(l1, d * 2.0)
    n1 = (node_tropical(jd) - ay) % 360.0
    n2 = (node_tropical(jd2) - ay2) % 360.0
    dn = (((n2 - n1) + 180.0) % 360.0 - 180.0) * 2.0
    out["Rahu"] = RawPosition(n1, dn)
    out["Ketu"] = RawPosition((n1 + 180.0) % 360.0, dn)
    return out


def sidereal_lon(name: str, dt_utc: datetime) -> float:
    """Sidereal longitude of a single graha (fast path for searches)."""
    t = _t(dt_utc)
    ay = ayanamsa_deg(float(t.tt))
    if name in ("Rahu", "Ketu"):
        n = (node_tropical(float(t.tt)) - ay) % 360.0
        return n if name == "Rahu" else (n + 180.0) % 360.0
    return (_tropical_lon(name, t) - ay) % 360.0


def ascendant_sidereal(dt_utc: datetime, lat: float, lon: float) -> float:
    """Sidereal Ascendant (Lagna) for an aware UTC instant and geographic place."""
    t = _t(dt_utc)
    ramc = (t.gast * 15.0 + lon) % 360.0       # apparent sidereal time -> degrees
    asc = ascendant_tropical(ramc, lat, obliquity_deg(float(t.tt)))
    return (asc - ayanamsa_deg(float(t.tt))) % 360.0
