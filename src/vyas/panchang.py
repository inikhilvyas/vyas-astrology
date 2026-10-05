"""Panchang & Avakhada engine for VYAS.

Everything is computed from the JPL ephemeris – nothing is hard-coded per chart.

Conventions (same as AstroSage / Parashara's Light defaults):
* Sunrise/sunset: upper limb of the Sun on the horizon with standard refraction
  (-0°50'), i.e. Skyfield's ``almanac.sunrise_sunset``.
* Hindu day (vara) runs sunrise -> next sunrise.
* Tithi = (Moon - Sun) / 12°, Yoga = (Sun + Moon sidereal) / 13°20',
  Karana = half tithi, Nakshatra from sidereal Moon.
* Lunar month: Amanta (new-moon ending), named by the Sun's sidereal sign at the
  preceding new moon; Purnimanta name also returned.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone

from . import constants as C
from . import ephem

TITHIS = ["Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
          "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
          "Trayodashi", "Chaturdashi", "Purnima"]
TITHIS_HI = ["प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", "षष्ठी", "सप्तमी",
             "अष्टमी", "नवमी", "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा"]
YOGAS = ["Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
         "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata",
         "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
         "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"]
KARANA_MOVABLE = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti (Bhadra)"]
VARAS = ["Ravivar (Sun)", "Somvar (Mon)", "Mangalvar (Tue)", "Budhvar (Wed)",
         "Guruvar (Thu)", "Shukravar (Fri)", "Shanivar (Sat)"]
VARA_LORD = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
MASAS = ["Chaitra", "Vaishakha", "Jyeshtha", "Ashadha", "Shravana", "Bhadrapada",
         "Ashwin", "Kartika", "Margashirsha", "Pausha", "Magha", "Phalguna"]

# ---- Avakhada tables (Moon based) -------------------------------------------
_VARNA_BY_SIGN = ["Kshatriya", "Vaishya", "Shudra", "Brahmin"] * 3  # Aries.. by element
_YONI = ["Ashwa", "Gaja", "Mesha", "Sarpa", "Sarpa", "Shwan", "Marjar", "Mesha",
         "Marjar", "Mushak", "Mushak", "Gau", "Mahish", "Vyaghra", "Mahish",
         "Vyaghra", "Mrig", "Mrig", "Shwan", "Vanar", "Nakul", "Vanar", "Simha",
         "Ashwa", "Simha", "Gau", "Gaja"]
_GANA = ["Deva", "Manushya", "Rakshasa", "Manushya", "Deva", "Manushya", "Deva",
         "Deva", "Rakshasa", "Rakshasa", "Manushya", "Manushya", "Deva", "Rakshasa",
         "Deva", "Rakshasa", "Deva", "Rakshasa", "Rakshasa", "Manushya", "Manushya",
         "Deva", "Rakshasa", "Rakshasa", "Manushya", "Manushya", "Deva"]
_NADI_CYCLE = ["Adi", "Madhya", "Antya", "Antya", "Madhya", "Adi"]
_TATVA_BY_SIGN = ["Agni", "Prithvi", "Vayu", "Jal"] * 3
# Vashya: (sign index) -> (first 15°, last 15°)
_VASHYA = {0: ("Chatushpad",) * 2, 1: ("Chatushpad",) * 2, 2: ("Manav",) * 2,
           3: ("Jalchar",) * 2, 4: ("Vanchar",) * 2, 5: ("Manav",) * 2,
           6: ("Manav",) * 2, 7: ("Keet",) * 2, 8: ("Manav", "Chatushpad"),
           9: ("Chatushpad", "Jalchar"), 10: ("Manav",) * 2, 11: ("Jalchar",) * 2}
# Naam akshar: 4 syllables per nakshatra (pada 1..4), traditional Hoda Chakra.
_AKSHAR = [
    "Chu Che Cho La", "Li Lu Le Lo", "A I U E", "O Va Vi Vu", "Ve Vo Ka Ki",
    "Ku Gha Ng Chha", "Ke Ko Ha Hi", "Hu He Ho Da", "Di Du De Do", "Ma Mi Mu Me",
    "Mo Ta Ti Tu", "Te To Pa Pi", "Pu Sha Na Tha", "Pe Po Ra Ri", "Ru Re Ro Ta",
    "Ti Tu Te To", "Na Ni Nu Ne", "No Ya Yi Yu", "Ye Yo Bha Bhi", "Bhu Dha Pha Dha",
    "Bhe Bho Ja Ji", "Ju Je Jo Gha", "Ga Gi Gu Ge", "Go Sa Si Su", "Se So Da Di",
    "Du Tha Jha Na", "De Do Cha Chi"]


def _utc(dt: datetime) -> datetime:
    return dt.astimezone(timezone.utc)


def _sid(name: str, dt_utc: datetime) -> float:
    return ephem.sidereal_lon(name, dt_utc)


def _sun_moon(dt_utc: datetime) -> tuple[float, float]:
    return ephem.sidereal_lon("Sun", dt_utc), ephem.sidereal_lon("Moon", dt_utc)


def _elong(dt_utc):
    s, m = _sun_moon(dt_utc)
    return (m - s) % 360.0


def _yoga_sum(dt_utc):
    s, m = _sun_moon(dt_utc)
    return (s + m) % 360.0


def _moon(dt_utc):
    return _sid("Moon", dt_utc)


def _index(fn, span, dt):
    return int(fn(dt) // span)


def _next_boundary(fn, span: float, start: datetime, step_h: float = 2.0,
                   max_days: float = 3.0) -> datetime | None:
    """First instant after *start* where floor(fn/span) changes (bisection to ~1 s)."""
    i0 = _index(fn, span, start)
    t = start
    end = start + timedelta(days=max_days)
    while t < end:
        t2 = t + timedelta(hours=step_h)
        if _index(fn, span, t2) != i0:
            lo, hi = t, t2
            while (hi - lo).total_seconds() > 1:
                mid = lo + (hi - lo) / 2
                if _index(fn, span, mid) == i0:
                    lo = mid
                else:
                    hi = mid
            return hi
        t = t2
    return None


def _prev_boundary(fn, span, start, step_h=2.0, max_days=3.0):
    i0 = _index(fn, span, start)
    t = start
    end = start - timedelta(days=max_days)
    while t > end:
        t2 = t - timedelta(hours=step_h)
        if _index(fn, span, t2) != i0:
            lo, hi = t2, t
            while (hi - lo).total_seconds() > 1:
                mid = lo + (hi - lo) / 2
                if _index(fn, span, mid) == i0:
                    hi = mid
                else:
                    lo = mid
            return hi
        t = t2
    return None


def sun_rise_set(date_local: datetime, lat: float, lon: float, tz_hours: float):
    """Sunrise and sunset (local, tz-aware) for the civil date of *date_local*."""
    from skyfield import almanac
    from skyfield.api import wgs84
    ts, eph = ephem._load()
    tz = timezone(timedelta(hours=tz_hours))
    day0 = datetime(date_local.year, date_local.month, date_local.day, tzinfo=tz)
    t0 = ts.from_datetime(day0)
    t1 = ts.from_datetime(day0 + timedelta(days=1))
    f = almanac.sunrise_sunset(eph, wgs84.latlon(lat, lon))
    times, events = almanac.find_discrete(t0, t1, f)
    rise = sset = None
    for t, e in zip(times, events):
        if e == 1 and rise is None:
            rise = t.utc_datetime().astimezone(tz)
        elif e == 0 and sset is None:
            sset = t.utc_datetime().astimezone(tz)
    return rise, sset


@dataclass
class Panchang:
    vara: str
    vara_lord: str
    tithi: str
    tithi_hi: str
    paksha: str
    tithi_end: str
    nakshatra: str
    nakshatra_hi: str
    nakshatra_pada: int
    nakshatra_lord: str
    nakshatra_end: str
    yoga: str
    yoga_end: str
    karana: str
    karana_end: str
    sunrise: str
    sunset: str
    day_length: str
    masa_amanta: str
    masa_purnimanta: str
    vikram_samvat: int
    shaka_samvat: int
    ayanamsa: str
    ayanamsa_value: str
    avakhada: dict = field(default_factory=dict)

    def as_dict(self):
        return asdict(self)


def _dms(x: float) -> str:
    d = int(x)
    m_f = (x - d) * 60
    m = int(m_f)
    s = int(round((m_f - m) * 60))
    if s == 60:
        m, s = m + 1, 0
    return f"{d:02d}°{m:02d}'{s:02d}\""


def karana_name(elong: float) -> str:
    k = int(elong // 6.0)          # 0..59
    if k == 0:
        return "Kimstughna"
    if k == 57:
        return "Shakuni"
    if k == 58:
        return "Chatushpada"
    if k == 59:
        return "Naga"
    return KARANA_MOVABLE[(k - 1) % 7]


def avakhada(moon_lon: float, asc_lon: float | None = None) -> dict:
    sign = int(moon_lon // 30)
    nak = int(moon_lon // C.NAKSHATRA_SPAN) % 27
    pada = int((moon_lon % C.NAKSHATRA_SPAN) // C.PADA_SPAN) + 1
    deg_in_sign = moon_lon % 30
    out = {
        "Varna": _VARNA_BY_SIGN[sign] if sign % 4 != 3 else "Brahmin",
        "Vashya": _VASHYA[sign][0 if deg_in_sign < 15 else 1],
        "Yoni": _YONI[nak],
        "Gana": _GANA[nak],
        "Nadi": _NADI_CYCLE[nak % 6],
        "Tatva": _TATVA_BY_SIGN[sign],
        "Rashi": C.SIGNS[sign],
        "Rashi Lord": C.SIGN_LORD[sign],
        "Nakshatra": f"{C.NAKSHATRAS[nak]} - {pada}",
        "Nakshatra Lord": C.VIMSHOTTARI_ORDER[nak % 9],
        "Naam Akshar": _AKSHAR[nak].split()[pada - 1],
    }
    if asc_lon is not None:
        a = int(asc_lon // 30)
        out["Lagna"] = C.SIGNS[a]
        out["Lagna Lord"] = C.SIGN_LORD[a]
    return out


def compute(dt_local: datetime, lat: float, lon: float, tz_hours: float,
            asc_lon: float | None = None) -> Panchang:
    """Full panchang for a tz-aware or naive local datetime."""
    tz = timezone(timedelta(hours=tz_hours))
    if dt_local.tzinfo is None:
        dt_local = dt_local.replace(tzinfo=tz)
    dt_u = _utc(dt_local)

    rise, sset = sun_rise_set(dt_local, lat, lon, tz_hours)
    # Hindu day starts at sunrise; before sunrise belongs to the previous vara.
    vara_date = dt_local if (rise is None or dt_local >= rise) else dt_local - timedelta(days=1)
    wd = (vara_date.weekday() + 1) % 7         # Python Mon=0 -> Sun=0

    e = _elong(dt_u)
    t_idx = int(e // 12.0)
    paksha = "Shukla" if t_idx < 15 else "Krishna"
    tn = t_idx % 15
    tithi = "Amavasya" if t_idx == 29 else TITHIS[tn]
    tithi_hi = "अमावस्या" if t_idx == 29 else TITHIS_HI[tn]

    moon = _moon(dt_u)
    nak = int(moon // C.NAKSHATRA_SPAN) % 27
    pada = int((moon % C.NAKSHATRA_SPAN) // C.PADA_SPAN) + 1
    y = int(_yoga_sum(dt_u) // C.NAKSHATRA_SPAN) % 27

    def fmt(t):
        return t.astimezone(tz).strftime("%d/%m/%Y %H:%M:%S") if t else "-"

    t_end = _next_boundary(_elong, 12.0, dt_u)
    n_end = _next_boundary(_moon, C.NAKSHATRA_SPAN, dt_u)
    y_end = _next_boundary(_yoga_sum, C.NAKSHATRA_SPAN, dt_u)
    k_end = _next_boundary(_elong, 6.0, dt_u)

    # Lunar month: Sun's sidereal sign at the preceding new moon (Amanta).
    nm = _prev_boundary(_elong, 360.0, dt_u, step_h=12.0, max_days=31.0) or dt_u
    sun_sign_nm = int(_sid("Sun", nm) // 30)
    masa = (sun_sign_nm + 1) % 12
    masa_p = (masa + 1) % 12 if paksha == "Krishna" else masa

    yr = dt_local.year
    # New samvat begins at Chaitra Shukla Pratipada.
    before_new_year = dt_local.month <= 4 and masa in (9, 10, 11)
    vs = yr + (56 if before_new_year else 57)
    shaka = yr - (79 if before_new_year else 78)

    day_len = (sset - rise) if (rise and sset) else None
    jd = ephem._t(dt_u).tt

    return Panchang(
        vara=VARAS[wd], vara_lord=VARA_LORD[wd],
        tithi=f"{paksha} {tithi}", tithi_hi=tithi_hi, paksha=paksha, tithi_end=fmt(t_end),
        nakshatra=C.NAKSHATRAS[nak], nakshatra_hi=C.NAKSHATRAS_HI[nak],
        nakshatra_pada=pada, nakshatra_lord=C.VIMSHOTTARI_ORDER[nak % 9],
        nakshatra_end=fmt(n_end),
        yoga=YOGAS[y], yoga_end=fmt(y_end),
        karana=karana_name(e), karana_end=fmt(k_end),
        sunrise=rise.strftime("%H:%M:%S") if rise else "-",
        sunset=sset.strftime("%H:%M:%S") if sset else "-",
        day_length=str(day_len).split(".")[0] if day_len else "-",
        masa_amanta=MASAS[masa], masa_purnimanta=MASAS[masa_p],
        vikram_samvat=vs, shaka_samvat=shaka,
        ayanamsa=ephem.AYANAMSA_NAME, ayanamsa_value=_dms(ephem.ayanamsa_deg(jd)),
        avakhada=avakhada(moon, asc_lon),
    )
