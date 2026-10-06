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
    rahu_kalam: str = "-"
    yamaganda: str = "-"
    gulika_kalam: str = "-"
    abhijit_muhurta: str = "-"
    chaughadiya_day: list = field(default_factory=list)
    chaughadiya_night: list = field(default_factory=list)

    def as_dict(self):
        return asdict(self)


def get_muhurta_and_chaughadiya(date_local: datetime, lat: float, lon: float, tz_hours: float) -> dict:
    """Computes exact location-based Rahu Kaal, Yamaganda, Gulika, Abhijit and 8-period Day & Night Chaughadiyas."""
    rise, sset = sun_rise_set(date_local, lat, lon, tz_hours)
    tz = timezone(timedelta(hours=tz_hours))
    if rise is None or sset is None:
        return {
            "rahu_kalam": "-", "yamaganda": "-", "gulika_kalam": "-", "abhijit_muhurta": "-",
            "chaughadiya_day": [], "chaughadiya_night": []
        }
    
    # Next day sunrise for accurate night division
    next_day = date_local + timedelta(days=1)
    next_rise, _ = sun_rise_set(next_day, lat, lon, tz_hours)
    if next_rise is None:
        next_rise = sset + timedelta(hours=12)

    day_secs = (sset - rise).total_seconds()
    day_part = day_secs / 8.0
    night_secs = (next_rise - sset).total_seconds()
    night_part = night_secs / 8.0

    # Hindu vara based on sunrise
    vara_date = date_local if date_local >= rise else date_local - timedelta(days=1)
    wd = (vara_date.weekday() + 1) % 7  # 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday

    # Classical 8-part daytime indices (0-indexed):
    # Rahu Kaal: Sun=7 (8th part), Mon=1 (2nd), Tue=6 (7th), Wed=4 (5th), Thu=5 (6th), Fri=3 (4th), Sat=2 (3rd)
    rahu_parts = {0: 7, 1: 1, 2: 6, 3: 4, 4: 5, 5: 3, 6: 2}
    yamaganda_parts = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0, 5: 6, 6: 5}
    gulika_parts = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 0}

    r_idx = rahu_parts[wd]
    y_idx = yamaganda_parts[wd]
    g_idx = gulika_parts[wd]

    def _fmt_span(start_dt, end_dt):
        return f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"

    rahu_str = _fmt_span(rise + timedelta(seconds=r_idx * day_part), rise + timedelta(seconds=(r_idx + 1) * day_part))
    yama_str = _fmt_span(rise + timedelta(seconds=y_idx * day_part), rise + timedelta(seconds=(y_idx + 1) * day_part))
    guli_str = _fmt_span(rise + timedelta(seconds=g_idx * day_part), rise + timedelta(seconds=(g_idx + 1) * day_part))

    # Abhijit Muhurta: 8th Muhurta of the day (day length / 15 * 7th to 8th)
    muhurta_span = day_secs / 15.0
    abhijit_s = rise + timedelta(seconds=7 * muhurta_span)
    abhijit_e = rise + timedelta(seconds=8 * muhurta_span)
    # Note: On Wednesday, Abhijit is traditionally avoided, but window exists astronomical
    abhijit_str = _fmt_span(abhijit_s, abhijit_e)

    # 7 Chaughadiya types: Udveg (Sun), Char (Ven), Labh (Mer), Amrit (Moon), Kaal (Sat), Shubh (Jup), Rog (Mars)
    # Cycle order: Udveg -> Char -> Labh -> Amrit -> Kaal -> Shubh -> Rog
    ch_names = [
        {"name": "Udveg", "name_hi": "उद्वेग", "nature": "अशुभ (Sun)", "color": "#ff7675"},
        {"name": "Char", "name_hi": "चल", "nature": "सामान्य/शुभ (Ven)", "color": "#74b9ff"},
        {"name": "Labh", "name_hi": "लाभ", "nature": "अति शुभ (Mer)", "color": "#55efc4"},
        {"name": "Amrit", "name_hi": "अमृत", "nature": "सर्वश्रेष्ठ (Moon)", "color": "#ffeaa7"},
        {"name": "Kaal", "name_hi": "काल", "nature": "हानिकारक (Sat)", "color": "#d63031"},
        {"name": "Shubh", "name_hi": "शुभ", "nature": "उत्तम (Jup)", "color": "#00b894"},
        {"name": "Rog", "name_hi": "रोग", "nature": "कष्टप्रद (Mars)", "color": "#e17055"}
    ]
    # First day Chaughadiya starting index per weekday:
    # Sun(0)=Udveg(0), Mon(1)=Amrit(3), Tue(2)=Rog(6), Wed(3)=Labh(2), Thu(4)=Shubh(5), Fri(5)=Char(1), Sat(6)=Kaal(4)
    day_first = {0: 0, 1: 3, 2: 6, 3: 2, 4: 5, 5: 1, 6: 4}
    # Night Chaughadiya starting index per weekday:
    # Sun(0)=Shubh(5), Mon(1)=Char(1), Tue(2)=Kaal(4), Wed(3)=Udveg(0), Thu(4)=Amrit(3), Fri(5)=Rog(6), Sat(6)=Labh(2)
    night_first = {0: 5, 1: 1, 2: 4, 3: 0, 4: 3, 5: 6, 6: 2}

    d_start_idx = day_first[wd]
    n_start_idx = night_first[wd]

    day_ch = []
    for i in range(8):
        c_obj = ch_names[(d_start_idx + i) % 7]
        c_s = rise + timedelta(seconds=i * day_part)
        c_e = rise + timedelta(seconds=(i + 1) * day_part)
        day_ch.append({
            "name": c_obj["name"],
            "name_hi": c_obj["name_hi"],
            "nature": c_obj["nature"],
            "color": c_obj["color"],
            "start": c_s.strftime("%I:%M %p"),
            "end": c_e.strftime("%I:%M %p")
        })

    night_ch = []
    for i in range(8):
        c_obj = ch_names[(n_start_idx + i) % 7]
        c_s = sset + timedelta(seconds=i * night_part)
        c_e = sset + timedelta(seconds=(i + 1) * night_part)
        night_ch.append({
            "name": c_obj["name"],
            "name_hi": c_obj["name_hi"],
            "nature": c_obj["nature"],
            "color": c_obj["color"],
            "start": c_s.strftime("%I:%M %p"),
            "end": c_e.strftime("%I:%M %p")
        })

    return {
        "rahu_kalam": rahu_str,
        "yamaganda": yama_str,
        "gulika_kalam": guli_str,
        "abhijit_muhurta": abhijit_str,
        "chaughadiya_day": day_ch,
        "chaughadiya_night": night_ch
    }


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
    """Full panchang for a tz-aware or naive local datetime with exact location-based Chaughadiyas & Rahu Kaal."""
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

    muh_ch = get_muhurta_and_chaughadiya(dt_local, lat, lon, tz_hours)

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
        rahu_kalam=muh_ch["rahu_kalam"],
        yamaganda=muh_ch["yamaganda"],
        gulika_kalam=muh_ch["gulika_kalam"],
        abhijit_muhurta=muh_ch["abhijit_muhurta"],
        chaughadiya_day=muh_ch["chaughadiya_day"],
        chaughadiya_night=muh_ch["chaughadiya_night"]
    )
