#!/usr/bin/env python3
"""
VYAS deterministic calculation layer (interpretation-free).

Input: SIDEREAL longitudes already extracted from a verified chart (PDF / software / ephemeris).
This script never invents positions. It derives only what is pure arithmetic from a longitude:
sign, degree, nakshatra, pada, nakshatra lord, navamsha sign, pada/navamsha lord,
KP star/sub/sub-sub lord, Vimshottari dasha (maha/antar/...), Parashari graha drishti,
Jaimini rashi drishti, whole-sign house of a point.

Usage:
  python vyas_calc.py point --lon 123.4567 [--boundary-arcsec 2]
  python vyas_calc.py dasha --moon-lon 123.4567 --birth 1990-05-01T10:30:00 [--levels 2] [--year-days 365.25]
  python vyas_calc.py chart --file chart.json
  python vyas_calc.py selftest

chart.json: {"lagna": 215.3, "planets": {"Sun": 12.1, "Moon": 123.4, ...}, "cusps": [12 longitudes, optional]}
All output is JSON and echoes its inputs so the caller can attach provenance.
"""
import argparse, json, sys
from datetime import datetime, timedelta

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio",
         "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGN_LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars",
             "Jupiter", "Saturn", "Saturn", "Jupiter"]
NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
              "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
              "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
              "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
               "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
NAK = 360.0 / 27   # 13d20'
PADA = NAK / 4     # 3d20'
MOVABLE, FIXED, DUAL = {0, 3, 6, 9}, {1, 4, 7, 10}, {2, 5, 8, 11}


def norm(x):
    return x % 360.0


def dms(x):
    d = int(x)
    m = int((x - d) * 60)
    s = ((x - d) * 60 - m) * 60
    return f"{d}\u00b0{m:02d}'{s:05.2f}\""


def nak_lord(idx):
    return DASHA_ORDER[idx % 9]


def navamsha_sign(lon):
    lon = norm(lon)
    sign = int(lon // 30)
    part = int((lon % 30) // (30 / 9))
    # fire->Aries, earth->Capricorn, air->Libra, water->Cancer
    start = {0: 0, 1: 9, 2: 6, 3: 3}[sign % 4]
    return (start + part) % 12


def subdivide(start_lon, span, first_lord, target_lon):
    """Vimshottari-proportional subdivision of [start_lon, start_lon+span) beginning with first_lord.
    Returns (lord, sub_start, sub_span) of the part containing target_lon."""
    i = DASHA_ORDER.index(first_lord)
    pos = start_lon
    for k in range(9):
        lord = DASHA_ORDER[(i + k) % 9]
        sub_span = span * DASHA_YEARS[lord] / 120.0
        if target_lon < pos + sub_span - 1e-12 or k == 8:
            return lord, pos, sub_span
        pos += sub_span


def point(lon, boundary_arcsec=2.0):
    lon = norm(lon)
    s = int(lon // 30)
    deg = lon - s * 30
    n = int(lon // NAK)
    in_nak = lon - n * NAK
    p = int(in_nak // PADA) + 1
    nav = navamsha_sign(lon)
    star = nak_lord(n)
    sub, sub_start, sub_span = subdivide(n * NAK, NAK, star, lon)
    subsub, ss_start, ss_span = subdivide(sub_start, sub_span, sub, lon)
    edges = {
        "nakshatra": min(in_nak, NAK - in_nak),
        "pada": min(in_nak % PADA, PADA - (in_nak % PADA)),
        "kp_sub": min(lon - sub_start, sub_start + sub_span - lon),
        "kp_sub_sub": min(lon - ss_start, ss_start + ss_span - lon),
    }
    warn = {k: round(v * 3600, 2) for k, v in edges.items() if v * 3600 <= boundary_arcsec}
    return {
        "input_longitude": lon, "longitude_dms": dms(lon),
        "sign": SIGNS[s], "sign_index": s + 1, "sign_lord": SIGN_LORD[s],
        "degree_in_sign": round(deg, 6), "degree_in_sign_dms": dms(deg),
        "nakshatra": NAKSHATRAS[n], "nakshatra_index": n + 1, "nakshatra_lord": star, "pada": p,
        "navamsha_sign": SIGNS[nav], "pada_navamsha_lord": SIGN_LORD[nav],
        "vargottama": nav == s,
        "kp": {"star_lord": star, "sub_lord": sub, "sub_sub_lord": subsub},
        "boundary_warning_arcsec": warn or None,
        "note": "pada_navamsha_lord = lord of the navamsha sign (no independent 'Pada Swami' assumed)",
    }


def vimshottari(moon_lon, birth_iso, levels=2, year_days=365.25):
    moon_lon = norm(moon_lon)
    n = int(moon_lon // NAK)
    lord0 = nak_lord(n)
    elapsed_frac = (moon_lon - n * NAK) / NAK
    birth = datetime.fromisoformat(birth_iso)
    bal_years = DASHA_YEARS[lord0] * (1 - elapsed_frac)

    def days(y):
        return y * year_days

    def expand(lord, start, years, depth):
        out = []
        i = DASHA_ORDER.index(lord)
        t = start
        for k in range(9):
            l = DASHA_ORDER[(i + k) % 9]
            yrs = years * DASHA_YEARS[l] / 120.0
            end = t + timedelta(days=days(yrs))
            node = {"lord": l, "start": t.isoformat(timespec="minutes"), "end": end.isoformat(timespec="minutes")}
            if depth > 1:
                node["sub"] = expand(l, t, yrs, depth - 1)
            out.append(node)
            t = end
        return out

    maha = []
    t = birth - timedelta(days=days(DASHA_YEARS[lord0] - bal_years))  # notional start of first maha
    i = DASHA_ORDER.index(lord0)
    for k in range(9):
        l = DASHA_ORDER[(i + k) % 9]
        yrs = DASHA_YEARS[l]
        end = t + timedelta(days=days(yrs))
        node = {"lord": l, "start": t.isoformat(timespec="minutes"), "end": end.isoformat(timespec="minutes"),
                "balance_at_birth_years": round(bal_years, 4) if k == 0 else None}
        if levels > 1:
            node["antardasha"] = expand(l, t, yrs, levels - 1)
        maha.append(node)
        t = end
    return {
        "convention": f"year={year_days} days; Vimshottari 120y; start from Moon nakshatra lord",
        "moon_nakshatra": NAKSHATRAS[n], "moon_nakshatra_lord": lord0,
        "balance_at_birth_years": round(bal_years, 6), "mahadasha": maha,
        "warning": "Dates shift by days between software (365.25 / 365.2425 / 360-day year). State the convention.",
    }


SPECIAL = {"Mars": [4, 8], "Jupiter": [5, 9], "Saturn": [3, 10]}  # plus 7th for all


def graha_drishti(planets):
    """Parashari sign-based full aspects. Rahu/Ketu special aspects are NOT assumed (school-dependent)."""
    res = {}
    for a, la in planets.items():
        sa = int(norm(la) // 30)
        targets = [7] + SPECIAL.get(a, [])
        tsigns = {SIGNS[(sa + h - 1) % 12]: h for h in targets}
        hits = [b for b, lb in planets.items() if b != a and SIGNS[int(norm(lb) // 30)] in tsigns]
        res[a] = {"aspects_signs": tsigns, "aspects_planets": hits}
    return {"system": "Parashari graha drishti, sign-based (full aspects only)", "aspects": res}


def rashi_drishti(planets):
    """Jaimini: movable->fixed (not adjacent), fixed->movable (not adjacent), dual->other duals."""
    def sign_aspects(s):
        if s in MOVABLE:
            return {x for x in FIXED if x != (s + 1) % 12}
        if s in FIXED:
            return {x for x in MOVABLE if x != (s - 1) % 12}
        return DUAL - {s}

    res = {}
    for a, la in planets.items():
        sa = int(norm(la) // 30)
        tg = sign_aspects(sa)
        res[a] = {"aspects_signs": [SIGNS[x] for x in sorted(tg)],
                  "aspects_planets": [b for b, lb in planets.items() if b != a and int(norm(lb) // 30) in tg]}
    return {"system": "Jaimini rashi drishti (sign-to-sign)", "aspects": res}


def chart(data):
    lag = norm(data["lagna"])
    ls = int(lag // 30)
    out = {"lagna": point(lag), "planets": {}}
    for name, lon in data["planets"].items():
        p = point(lon)
        p["whole_sign_house_from_lagna"] = (p["sign_index"] - 1 - ls) % 12 + 1
        out["planets"][name] = p
    if data.get("cusps"):
        out["kp_cusps"] = {f"C{i + 1}": point(c) for i, c in enumerate(data["cusps"])}
    out["graha_drishti"] = graha_drishti(data["planets"])
    out["rashi_drishti"] = rashi_drishti(data["planets"])
    out["house_system_note"] = ("whole_sign_house_from_lagna is Parashari-style; kp_cusps are a separate "
                                "representation (e.g. Placidus). Never merge them.")
    return out


def selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok &= bool(cond)
        print(("PASS " if cond else "FAIL ") + name)

    p = point(0.0)
    chk("0 Aries = Ashwini pada1, Ketu", p["nakshatra"] == "Ashwini" and p["pada"] == 1 and p["nakshatra_lord"] == "Ketu")
    p = point(13.3334)
    chk("13d20' = Bharani, Venus", p["nakshatra"] == "Bharani" and p["nakshatra_lord"] == "Venus")
    p = point(359.99)
    chk("Revati pada4, Mercury", p["nakshatra"] == "Revati" and p["pada"] == 4 and p["nakshatra_lord"] == "Mercury")
    chk("Aries 1d navamsha Aries", point(1.0)["navamsha_sign"] == "Aries")
    chk("Taurus 0d navamsha Capricorn", point(30.0)["navamsha_sign"] == "Capricorn")
    chk("Gemini 0d navamsha Libra", point(60.0)["navamsha_sign"] == "Libra")
    chk("Cancer 0d navamsha Cancer", point(90.0)["navamsha_sign"] == "Cancer")
    chk("Pisces last part navamsha Pisces", point(359.99)["navamsha_sign"] == "Pisces")
    chk("KP first sub of Ashwini = Ketu", point(0.0)["kp"]["sub_lord"] == "Ketu")
    chk("KP last sub of Ashwini = Mercury", point(13.33)["kp"]["sub_lord"] == "Mercury")
    chk("Aries 0.5d vargottama", point(0.5)["vargottama"] is True)
    chk("boundary warning near 13d20'", point(13.3333)["boundary_warning_arcsec"] is not None)
    d = vimshottari(0.0, "2000-01-01T00:00:00", levels=1)
    chk("Moon 0 Aries -> Ketu balance 7y", d["moon_nakshatra_lord"] == "Ketu" and abs(d["balance_at_birth_years"] - 7) < 1e-9)
    chk("Maha sequence Ketu,Venus", [m["lord"] for m in d["mahadasha"][:2]] == ["Ketu", "Venus"])
    gd = graha_drishti({"Mars": 0.0, "Venus": 210.0, "Saturn": 90.0})
    chk("Mars(Aries) 8th aspect hits Scorpio planet", "Venus" in gd["aspects"]["Mars"]["aspects_planets"])
    rd = rashi_drishti({"A": 0.0, "B": 120.0, "C": 30.0})
    chk("Aries aspects Leo, not adjacent Taurus",
        "B" in rd["aspects"]["A"]["aspects_planets"] and "C" not in rd["aspects"]["A"]["aspects_planets"])
    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("point")
    a.add_argument("--lon", type=float, required=True)
    a.add_argument("--boundary-arcsec", type=float, default=2.0)
    b = sp.add_parser("dasha")
    b.add_argument("--moon-lon", type=float, required=True)
    b.add_argument("--birth", required=True)
    b.add_argument("--levels", type=int, default=2)
    b.add_argument("--year-days", type=float, default=365.25)
    c = sp.add_parser("chart")
    c.add_argument("--file", required=True)
    sp.add_parser("selftest")
    args = ap.parse_args()
    if args.cmd == "selftest":
        sys.exit(selftest())
    if args.cmd == "point":
        r = point(args.lon, args.boundary_arcsec)
    elif args.cmd == "dasha":
        r = vimshottari(args.moon_lon, args.birth, args.levels, args.year_days)
    else:
        with open(args.file) as f:
            r = chart(json.load(f))
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
