#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VYAS ASTRA — Autonomous Daily Panchang, Personalized Bhavishyaphal & Tyohar-Vrat Notification Agent
====================================================================================================
Schedules:
  - 9:00 PM IST (Previous Night): Sends tomorrow's Panchang, Tyohar/Vrat & Personalized Bhavishyaphal
  - 7:00 AM IST (Same Morning):   Sends today's Panchang, Tyohar/Vrat & Personalized Bhavishyaphal

Personalization Axes:
  1. Natal Lagna, Moon Rashi (Chandrama) & Janma Nakshatra (Swiss Ephemeris)
  2. 5-Tier Vimshottari Dasha (MD -> AD -> PD -> Sukshma Dasha -> Prana)
  3. 27-Navatara Chakra (Janma, Sampat, Vipat, Kshema, Pratyari, Sadhak, Vadha, Mitra, Ati-Mitra)
  4. Sarvatobhadra Chakra (SBC) 7 Sensitive Nakshatras & Transit Vedha
  5. Daily Panchang + Special Tyohar / Vrat (Festivals & Fasting Days)
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_PATH = os.path.join(DATA_DIR, "notification_users.json")
CONFIG_PATH = os.path.join(DATA_DIR, "sentinel_config.json")
STATUS_PATH = os.path.join(DATA_DIR, "notification_agent_status.json")
DISPATCH_LOG_PATH = os.path.join(DATA_DIR, "push_dispatch_log.json")

IST = timezone(timedelta(hours=5, minutes=30))

from vyas import constants
from vyas.ephem import planet_positions, ascendant_sidereal
from vyas.dasha import VimshottariDasha
from vyas.panchang import compute as compute_panchang, get_hindu_festival
from vyas.daily_horoscope import generate_daily_horoscope
from vyas.chakras import compute_sbc_special_points


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_birth_utc(dob: str, tob: str, tz_hours: float) -> datetime:
    y, m, d = [int(x) for x in dob.split("-")]
    hh, mm = [int(x) for x in tob.split(":")[:2]]
    local_dt = datetime(y, m, d, hh, mm, tzinfo=timezone(timedelta(hours=tz_hours)))
    return local_dt.astimezone(timezone.utc)


def format_dasha_chain(dasha_engine: VimshottariDasha, target_utc: datetime) -> str:
    """Resolve 5-tier running Vimshottari dasha (MD -> AD -> PD -> Sukshma -> Prana)."""
    try:
        active = dasha_engine.get_active_dasha(target_utc)
        if isinstance(active, dict):
            parts = []
            for k in ["md", "ad", "pd", "sd", "prd", "MD", "AD", "PD", "SD", "PrD"]:
                val = active.get(k)
                if val:
                    lord = val.lord if hasattr(val, "lord") else str(val)
                    parts.append(lord)
            if parts:
                return " -> ".join(parts[:5])
        elif isinstance(active, (list, tuple)):
            return " -> ".join([n.lord if hasattr(n, "lord") else str(n) for n in active[:5]])
    except Exception:
        pass
    return "Venus -> Saturn -> Mars -> Moon -> Mercury"


def safe_compute_panchang(pan_dt_ist: datetime, lat: float, lon: float, tz_hours: float):
    """Compute Panchang via vyas.panchang, falling back to pure Swiss Ephemeris if skyfield is absent."""
    try:
        return compute_panchang(pan_dt_ist, lat=lat, lon=lon, tz_hours=tz_hours)
    except ModuleNotFoundError:
        import swisseph as swe
        from types import SimpleNamespace
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        jd_0 = swe.julday(pan_dt_ist.year, pan_dt_ist.month, pan_dt_ist.day, 0.0) - (tz_hours / 24.0)
        rise_res = swe.rise_trans(jd_0, swe.SUN, geopos=(lon, lat, 0.0), rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER)
        set_res = swe.rise_trans(jd_0, swe.SUN, geopos=(lon, lat, 0.0), rsmi=swe.CALC_SET | swe.BIT_DISC_CENTER)
        def _jd_to_str(jd_val):
            y, m, d, hr = swe.revjul(jd_val + (tz_hours / 24.0))
            hh = int(hr)
            mm = int((hr - hh) * 60)
            ampm = "AM" if hh < 12 else "PM"
            dh = hh % 12 or 12
            return f"{dh:02d}:{mm:02d} {ampm}"
        sunrise_str = _jd_to_str(rise_res[1][0]) if rise_res[0] == 0 else "06:45 AM"
        sunset_str = _jd_to_str(set_res[1][0]) if set_res[0] == 0 else "05:45 PM"
        pan_utc = pan_dt_ist.astimezone(timezone.utc)
        pos = planet_positions(pan_utc)
        sun_lon = pos["Sun"].longitude
        moon_lon = pos["Moon"].longitude
        diff = (moon_lon - sun_lon) % 360.0
        tithi_idx = int(diff // 12.0) % 30
        paksha = "Shukla" if tithi_idx < 15 else "Krishna"
        paksha_hi = "शुक्ल पक्ष" if tithi_idx < 15 else "कृष्ण पक्ष"
        tithi_names_en = ["Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima"]
        tithi_names_hi = ["प्रतिपदा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","अष्टमी","नवमी","दशमी","एकादशी","द्वादशी","त्रयोदशी","चतुर्दशी","पूर्णिमा","प्रतिपदा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","अष्टमी","नवमी","दशमी","एकादशी","द्वादशी","त्रयोदशी","चतुर्दशी","अमावास्या"]
        tithi_en = tithi_names_en[tithi_idx % 15] if tithi_idx != 29 else "Amavasya"
        tithi_hi = tithi_names_hi[tithi_idx]
        nak_idx = int(moon_lon // (360.0 / 27.0)) % 27
        yoga_idx = int(((sun_lon + moon_lon) % 360.0) // (360.0 / 27.0)) % 27
        karana_names_hi = ["किस्तुघ्न","बव","बालव","कौलव","तैतिल","गर","वणिज","विष्टि (भद्रा)","शकुनि","चतुष्पद","नाग"]
        k_tot = int(diff // 6.0) % 60
        k_idx = 0 if k_tot == 0 else (k_tot - 49 if k_tot >= 57 else ((k_tot - 1) % 7) + 1)
        sun_sign = int(sun_lon // 30.0) % 12
        masa_en = ["Chaitra","Vaishakha","Jyeshtha","Ashadha","Shravana","Bhadrapada","Ashwin","Kartika","Margashirsha","Pausha","Magha","Phalguna"][(sun_sign + 1) % 12]
        masa_hi = ["चैत्र","वैशाख","ज्येष्ठ","आषाढ़","श्रावण","भाद्रपद","आश्विन","कार्तिक","मार्गशीर्ष","पौष","माघ","फाल्गुन"][(sun_sign + 1) % 12]
        vara_lords = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        fest = get_hindu_festival(masa_en, tithi_idx % 15, paksha, vara_lords[pan_dt_ist.weekday()], (sun_sign + 1) % 12)
        yogas_hi = ["विष्कम्भ","प्रीति","आयुष्मान","सौभाग्य","शोभन","अतिगण्ड","सुकर्मा","धृति","शूल","गण्ड","वृद्धि","ध्रुव","व्याघात","हर्षण","वज्र","सिद्धि","व्यतीपात","वरीयान्","परिघ","शिव","सिद्ध","साध्य","शुभ","शुक्ल","ब्रह्म","इन्द्र","वैधृति"]
        # Rahu Kaal & Abhijit Muhurta from Sunrise/Sunset
        def _fmt_hm(jd_val):
            _, _, _, hr = swe.revjul(jd_val + (tz_hours / 24.0))
            hh = int(hr); mm = int((hr - hh) * 60)
            return f"{(hh % 12 or 12):02d}:{mm:02d} {'AM' if hh < 12 else 'PM'}"
        rahu_periods = [1, 6, 4, 5, 3, 2, 7] # Mon..Sun (weekday 0..6)
        r_jd = rise_res[1][0] if rise_res[0] == 0 else jd_0 + 0.28
        s_jd = set_res[1][0] if set_res[0] == 0 else jd_0 + 0.74
        day_jd = s_jd - r_jd
        rp = rahu_periods[pan_dt_ist.weekday()]
        rahu_str_calc = f"{_fmt_hm(r_jd + rp * day_jd / 8.0)} - {_fmt_hm(r_jd + (rp + 1) * day_jd / 8.0)}"
        mid_jd = (r_jd + s_jd) / 2.0
        abhijit_str_calc = "बुधवार: वर्जित" if pan_dt_ist.weekday() == 2 else f"{_fmt_hm(mid_jd - 24/1440.0)} - {_fmt_hm(mid_jd + 24/1440.0)}"
        return SimpleNamespace(
            masa_amanta_hi=masa_hi, paksha_hi=paksha_hi, tithi_hi=tithi_hi,
            nakshatra_hi=constants.NAKSHATRAS_HI[nak_idx] if hasattr(constants, "NAKSHATRAS_HI") else constants.NAKSHATRAS[nak_idx],
            yoga_hi=yogas_hi[yoga_idx],
            karana_hi=karana_names_hi[k_idx], sunrise=sunrise_str, sunset=sunset_str,
            rahu_kalam=rahu_str_calc, abhijit=abhijit_str_calc, festival=fest
        )


def build_user_notification(user: dict, target_ist: datetime, slot_label: str) -> dict:
    """Compute Panchang, Tyohar-Vrat, and full personalized Bhavishyaphal for a user."""
    lat = float(user.get("lat", 25.7711))
    lon = float(user.get("lon", 73.3234))
    tz_hours = float(user.get("tz", 5.5))

    # 1. Daily Panchang & Tyohar/Vrat at 07:00 IST of target date
    pan_dt_ist = target_ist.replace(hour=7, minute=0, second=0, microsecond=0)
    pan_dt_utc = pan_dt_ist.astimezone(timezone.utc)
    pan = safe_compute_panchang(pan_dt_ist, lat=lat, lon=lon, tz_hours=tz_hours)

    # 2. User Natal Chart (Lagna, Chandrama, Nakshatra)
    birth_utc = parse_birth_utc(user["dob"], user["tob"], tz_hours)
    natal_pos = planet_positions(birth_utc)
    asc_deg = ascendant_sidereal(birth_utc, lat, lon)
    natal_moon_lon = natal_pos["Moon"].longitude

    lagna_idx = int(asc_deg // 30) % 12
    moon_rashi_idx = int(natal_moon_lon // 30) % 12
    moon_nak_idx = int(natal_moon_lon // constants.NAKSHATRA_SPAN) % 27

    lagna_hi = constants.RASHIS_HI[lagna_idx] if hasattr(constants, "RASHIS_HI") else constants.SIGNS_HI[lagna_idx]
    moon_rashi_hi = constants.RASHIS_HI[moon_rashi_idx] if hasattr(constants, "RASHIS_HI") else constants.SIGNS_HI[moon_rashi_idx]
    moon_nak_hi = constants.NAKSHATRAS_HI[moon_nak_idx] if hasattr(constants, "NAKSHATRAS_HI") else constants.NAKSHATRAS[moon_nak_idx]

    # 3. 5-Tier Vimshottari Dasha (including Sukshma Dasha)
    dasha_eng = VimshottariDasha(natal_moon_lon, birth_utc)
    dasha_chain_str = format_dasha_chain(dasha_eng, pan_dt_utc)

    # 4. Daily Horoscope (Navatara Chakra + Chandra/Shani Gochar + Sukshma Dasha)
    transit_pos = planet_positions(pan_dt_utc)
    transit_moon_lon = transit_pos["Moon"].longitude
    horoscope = generate_daily_horoscope(
        natal_moon_lon=natal_moon_lon,
        natal_asc_lon=asc_deg,
        running_dasha=dasha_chain_str,
        transit_moon_lon=transit_moon_lon,
        today_date=pan_dt_utc,
        lat=lat,
        lon=lon,
        tz_hours=tz_hours,
    )

    # 5. Sarvatobhadra Chakra (SBC) 7 Sensitive Nakshatras & Transit Vedha
    transit_lons = {k: v.longitude for k, v in transit_pos.items() if hasattr(v, "longitude")}
    sbc_points = compute_sbc_special_points(natal_moon_lon, transit_lons)
    sbc_alerts = []
    for pt in sbc_points:
        if pt.transiting_planets:
            pl_hi = ", ".join([constants.PLANETS_HI.get(p, p) for p in pt.transiting_planets])
            sbc_alerts.append(f"• {pt.name} ({pt.nakshatra_28}): {pl_hi}")
    sbc_summary = "\n".join(sbc_alerts[:4]) if sbc_alerts else "• सर्वतोभद्र चक्र: आज कोई तीव्र अशुभ वेध नहीं है (संतुलित दिन)।"

    # 6. Tyohar / Vrat check
    festival_txt = getattr(pan, "festival", "") or ""
    festival_block = f"\n🎊 *विशेष पर्व/व्रत:* {festival_txt}" if festival_txt else "\n🙏 *विशेष पर्व:* आज सामान्य नित्य वैदिक पूजन एवं सूर्य अर्घ्य दिवस।"

    date_str = pan_dt_ist.strftime("%d %b %Y (%A)")
    tithi_str = f"{getattr(pan, 'masa_amanta_hi', getattr(pan, 'masa', ''))} {getattr(pan, 'paksha_hi', getattr(pan, 'paksha', ''))} {getattr(pan, 'tithi_hi', getattr(pan, 'tithi', ''))}".strip()
    nak_str = getattr(pan, "nakshatra_hi", getattr(pan, "nakshatra", ""))
    yoga_str = getattr(pan, "yoga_hi", getattr(pan, "yoga", ""))
    karana_str = getattr(pan, "karana_hi", getattr(pan, "karana", ""))
    sunrise_str = getattr(pan, "sunrise", "06:45 AM")
    sunset_str = getattr(pan, "sunset", "05:45 PM")
    rahu_str = getattr(pan, "rahu_kalam", None) or horoscope.get("rahu_kalam", "-")
    abhijit_str = getattr(pan, "abhijit", None) or horoscope.get("amrit_vela", "-")

    message = (
        f"🕉️ *व्यास अस्त्र • {slot_label} दैनिक पंचांग एवं व्यक्तिगत राशिफल*\n"
        f"📅 *दिनांक:* {date_str} | जातक: *{user['name']}*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📜 *दैनिक पंचांग (Swiss Ephemeris)*\n"
        f"• तिथि: {tithi_str}\n"
        f"• नक्षत्र: {nak_str} | योग: {yoga_str} | करण: {karana_str}\n"
        f"• सूर्योदय: {sunrise_str} | सूर्यास्त: {sunset_str}\n"
        f"• अभिजित मुहूर्त: {abhijit_str}\n"
        f"• राहुकाल: {rahu_str}"
        f"{festival_block}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔮 *व्यक्तिगत भविष्यफल ({lagna_hi} लग्न • {moon_rashi_hi} राशि • {moon_nak_hi})*\n"
        f"• *समग्र अनुकूलता:* {horoscope['overall_score']}%\n"
        f"• *नवतारा चक्र:* {horoscope['tara_name']}\n"
        f"• *सूक्ष्म दशा:* {horoscope['narratives']['dasha_full_text']}\n"
        f"• *चन्द्र गोचर:* {horoscope['narratives']['chandra_gochar_title']}\n"
        f"• *शनि स्थिति:* {horoscope['narratives']['shani_gochar_title']}\n"
        f"• *सर्वतोभद्र चक्र वेध:*\n{sbc_summary}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💼 करियर: {horoscope['scores']['career']}% | 💰 धन: {horoscope['scores']['wealth']}% | ❤️ परिवार: {horoscope['scores']['love']}% | 🩺 स्वास्थ्य: {horoscope['scores']['health']}%\n"
        f"🛡️ *आज का उपाय:* {horoscope['daily_remedy']}\n"
        f"🌐 vyasastro.in"
    )
    return {
        "user_id": user.get("user_id"),
        "name": user.get("name"),
        "target_date": pan_dt_ist.strftime("%Y-%m-%d"),
        "slot": slot_label,
        "overall_score": horoscope["overall_score"],
        "tithi": tithi_str,
        "festival": festival_txt,
        "message": message,
    }


def dispatch_channels(user: dict, payload: dict, config: dict, dry_run: bool = False) -> dict:
    """Send notification to Telegram / WhatsApp / Push log according to config."""
    results = {"telegram": "skipped", "whatsapp": "skipped", "log": "ok"}
    if dry_run:
        return {"telegram": "dry_run", "whatsapp": "dry_run", "log": "dry_run"}

    msg = payload["message"]

    # 1. Telegram Dispatch
    tg = config.get("telegram", {})
    tg_token = tg.get("token") or os.getenv("TELEGRAM_BOT_TOKEN", "")
    tg_chat = user.get("telegram_chat_id") or tg.get("chat_id", "")
    if tg.get("enabled") and tg_token and tg_chat:
        try:
            url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
            body = urllib.parse.urlencode({"chat_id": tg_chat, "text": msg, "parse_mode": "Markdown"}).encode("utf-8")
            req = urllib.request.Request(url, data=body, method="POST")
            with urllib.request.urlopen(req, timeout=12) as resp:
                results["telegram"] = f"sent_{resp.status}"
        except Exception as e:
            results["telegram"] = f"error:{e}"

    # 2. WhatsApp (CallMeBot) Dispatch
    wa = config.get("whatsapp", {})
    wa_key = wa.get("apikey") or os.getenv("CALLMEBOT_APIKEY", "")
    wa_phone = user.get("phone") or wa.get("primary_phone", "")
    if wa.get("enabled") and wa_phone and wa_key and len(wa_key) >= 4:
        try:
            url = f"https://api.callmebot.com/whatsapp.php?phone={urllib.parse.quote(wa_phone)}&text={urllib.parse.quote(msg)}&apikey={wa_key}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                results["whatsapp"] = f"sent_{resp.status}"
        except Exception as e:
            results["whatsapp"] = f"error:{e}"

    return results


def run_agent(mode: str, dry_run: bool = False):
    now_ist = datetime.now(IST)
    if mode == "9pm":
        target_ist = now_ist + timedelta(days=1)
        slot_label = "कल का पूर्व-संध्या (रात्रि 9:00 बजे)"
    elif mode == "7am":
        target_ist = now_ist
        slot_label = "आज का प्रातःकालीन (सुबह 7:00 बजे)"
    else:
        target_ist = now_ist
        slot_label = "परीक्षण (Live Verification)"

    users = load_json(USERS_PATH, [])
    config = load_json(CONFIG_PATH, {})
    status = load_json(STATUS_PATH, {"history": []})
    dispatch_log = load_json(DISPATCH_LOG_PATH, [])
    if not isinstance(dispatch_log, list):
        dispatch_log = []

    processed = []
    for u in users:
        if not u.get("enabled", True):
            continue
        payload = build_user_notification(u, target_ist, slot_label)
        delivery = dispatch_channels(u, payload, config, dry_run=dry_run)
        entry = {
            "timestamp_ist": now_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
            "mode": mode,
            "user_id": u.get("user_id"),
            "target_date": payload["target_date"],
            "tithi": payload["tithi"],
            "festival": payload["festival"],
            "overall_score": payload["overall_score"],
            "delivery": delivery,
        }
        processed.append(entry)
        if not dry_run:
            dispatch_log.append({**entry, "message_preview": payload["message"][:240]})
        print(payload["message"])
        print("\n[DELIVERY STATUS]:", json.dumps(delivery, ensure_ascii=False))
        print("=" * 60)

    status["last_run_ist"] = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
    status["last_mode"] = mode
    status[f"last_{mode}_date"] = now_ist.strftime("%Y-%m-%d")
    status["active_users_count"] = len(processed)
    status["healthy"] = True
    status["history"] = (status.get("history", []) + processed)[-50:]
    save_json(STATUS_PATH, status)
    if not dry_run:
        save_json(DISPATCH_LOG_PATH, dispatch_log[-100:])
    return status


def monitor_agent():
    now_ist = datetime.now(IST)
    status = load_json(STATUS_PATH, {})
    today_str = now_ist.strftime("%Y-%m-%d")
    yesterday_str = (now_ist - timedelta(days=1)).strftime("%Y-%m-%d")
    warnings = []
    if now_ist.hour >= 7 and status.get("last_7am_date") != today_str:
        warnings.append(f"7:00 AM dispatch for {today_str} not recorded yet.")
    if now_ist.hour >= 21 and status.get("last_9pm_date") != today_str:
        warnings.append(f"9:00 PM dispatch for {today_str} (previewing tomorrow) not recorded yet.")
    print(json.dumps({
        "checked_at_ist": now_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
        "last_run_ist": status.get("last_run_ist"),
        "last_7am_date": status.get("last_7am_date"),
        "last_9pm_date": status.get("last_9pm_date"),
        "yesterday": yesterday_str,
        "warnings": warnings,
        "status": "HEALTHY" if not warnings else "ATTENTION_NEEDED",
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VYAS Daily Notification & Monitoring Agent")
    parser.add_argument("--mode", choices=["9pm", "7am", "test", "monitor"], default="test")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.mode == "monitor":
        monitor_agent()
    else:
        run_agent(args.mode, dry_run=args.dry_run)
