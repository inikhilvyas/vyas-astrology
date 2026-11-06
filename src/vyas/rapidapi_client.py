"""RapidAPI Hub and Free Global Astronomical & Geocoding Client for VYAS.

Provides:
1. Global City Search & Geocoding (RapidAPI GeoDB Cities with OpenStreetMap Photon free fallback).
2. Worldwide Timezone & DST Offset Detection (TimeAPI / WorldTimeAPI).
3. Solar Astronomical Metrics (Sunrise-Sunset.org API for verified Dinamana / Solar Noon).
"""
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Optional RapidAPI Key from environment or Streamlit secrets
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")
_CACHE_GEO: Dict[str, List[Dict]] = {}
_CACHE_TZ: Dict[Tuple[float, float], float] = {}


def search_global_cities(query: str, limit: int = 15) -> List[Dict]:
    """
    Searches worldwide cities using RapidAPI GeoDB if key is set,
    or OpenStreetMap Photon API (100% free, zero-key, ultra-fast fallback).
    """
    q = (query or "").strip()
    if len(q) < 2:
        return []

    q_key = q.lower()
    if q_key in _CACHE_GEO:
        return _CACHE_GEO[q_key]

    results = []

    # 1. Try RapidAPI GeoDB Cities if RAPIDAPI_KEY configured
    if RAPIDAPI_KEY:
        try:
            url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/cities?namePrefix={urllib.parse.quote(q)}&limit={limit}&sort=-population"
            req = urllib.request.Request(
                url,
                headers={
                    "X-RapidAPI-Key": RAPIDAPI_KEY,
                    "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
                    "User-Agent": "VYAS-Astra/2.0"
                }
            )
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for c in data.get("data", []):
                    city_name = c.get("city", c.get("name", ""))
                    region = c.get("region", "")
                    country = c.get("country", "")
                    display = f"{city_name}, {region}, {country}".replace(", ,", ",")
                    results.append({
                        "label": display,
                        "name": city_name,
                        "state": region or country,
                        "lat": round(float(c.get("latitude", 0.0)), 4),
                        "lon": round(float(c.get("longitude", 0.0)), 4),
                        "pop": c.get("population", 0),
                        "source": "RapidAPI GeoDB"
                    })
                if results:
                    _CACHE_GEO[q_key] = results
                    return results
        except Exception:
            pass

    # 2. Free OpenStreetMap Photon API (Zero-cost, worldwide, no-key required)
    try:
        url = f"https://photon.komoot.io/api/?q={urllib.parse.quote(q)}&limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "VYAS-Astra-Astrology/2.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for feat in data.get("features", []):
                props = feat.get("properties", {})
                osm_type = props.get("osm_value", "")
                if osm_type in ("city", "town", "village", "administrative", "municipality", "hamlet", ""):
                    city_name = props.get("name", "")
                    state = props.get("state", props.get("country", ""))
                    country = props.get("country", "")
                    coords = feat.get("geometry", {}).get("coordinates", [0.0, 0.0])
                    lon, lat = coords[0], coords[1]
                    display = f"{city_name}, {state}, {country}".replace(", ,", ",").strip(", ")
                    results.append({
                        "label": display,
                        "name": city_name,
                        "state": state,
                        "lat": round(float(lat), 4),
                        "lon": round(float(lon), 4),
                        "pop": 100000,
                        "source": "OpenStreetMap Photon"
                    })
    except Exception:
        pass

    _CACHE_GEO[q_key] = results
    return results


def get_timezone_for_coordinates(lat: float, lon: float) -> Optional[float]:
    """
    Fetches exact UTC timezone offset (e.g. 5.5 for IST, -5.0 for EST, 1.0 for CET)
    using TimeAPI coordinate endpoint (100% free, no key required).
    """
    cache_key = (round(lat, 2), round(lon, 2))
    if cache_key in _CACHE_TZ:
        return _CACHE_TZ[cache_key]

    try:
        url = f"https://timeapi.io/api/time/current/coordinate?latitude={lat}&longitude={lon}"
        req = urllib.request.Request(url, headers={"User-Agent": "VYAS-Astra/2.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # Parse offset or seconds
            if "standardUtcOffset" in data and "seconds" in data["standardUtcOffset"]:
                sec = data["standardUtcOffset"]["seconds"]
                tz_hours = round(sec / 3600.0, 2)
                _CACHE_TZ[cache_key] = tz_hours
                return tz_hours
    except Exception:
        pass

    return None


def get_solar_times(lat: float, lon: float, date_iso: str) -> Optional[Dict[str, str]]:
    """
    Fetches official astronomical sunrise, sunset, and solar noon from sunrise-sunset.org.
    100% free, no key required, highly accurate for Panchang Dinamana validation.
    """
    try:
        url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date_iso}&formatted=0"
        req = urllib.request.Request(url, headers={"User-Agent": "VYAS-Astra/2.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("status") == "OK":
                res = data.get("results", {})
                return {
                    "sunrise_utc": res.get("sunrise", ""),
                    "sunset_utc": res.get("sunset", ""),
                    "solar_noon_utc": res.get("solar_noon", ""),
                    "day_length_sec": res.get("day_length", 0)
                }
    except Exception:
        pass
    return None
