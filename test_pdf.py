import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from vyas.pdf_builder import build_pdf_report

ast_json = """
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "system_id": "urn:simpa:astro:ast_v3",
  "native_meta": {
    "name": "Piyush Sharma",
    "gender": "Male",
    "dob": "1989-03-24",
    "tob": "10:15:39",
    "pob": "Pali, Rajasthan, India",
    "lat": 25.85,
    "lon": 76.55,
    "timezone": 5.5,
    "julian_day": 2447610.0,
    "ayanamsha_type": "KP_New",
    "ayanamsha_deg": "023:36:59"
  },
  "panchang": {
    "tithi": "Krishna Dwitiya",
    "vara": "Friday",
    "nakshatra": "Chitra-2",
    "yoga": "Dhruva",
    "karana": "Gara",
    "sunrise": "06:23:34",
    "sunset": "18:36:43"
  },
  "planetary_positions": {
    "Lagna": { "sign": "Taurus", "degree": 48.9055, "dms": "048:54:20", "rl": "Venus", "nl": "Moon", "sl": "Mercury", "ssl": "Rahu" },
    "Sun": { "sign": "Pisces", "degree": 339.9186, "dms": "339:55:07", "rl": "Jupiter", "nl": "Saturn", "sl": "Venus", "ssl": "Mercury", "is_retro": false },
    "Moon": { "sign": "Virgo", "degree": 179.2358, "dms": "179:14:09", "rl": "Mercury", "nl": "Mars", "sl": "Saturn", "ssl": "Moon", "is_retro": false },
    "Mars": { "sign": "Taurus", "degree": 44.2136, "dms": "044:12:49", "rl": "Venus", "nl": "Moon", "sl": "Jupiter", "ssl": "Saturn", "is_retro": false },
    "Mercury": { "sign": "Aquarius", "degree": 329.0472, "dms": "329:02:50", "rl": "Saturn", "nl": "Jupiter", "sl": "Sun", "ssl": "Jupiter", "is_retro": false },
    "Jupiter": { "sign": "Taurus", "degree": 38.4519, "dms": "038:27:07", "rl": "Venus", "nl": "Sun", "sl": "Venus", "ssl": "Mars", "is_retro": false },
    "Venus": { "sign": "Pisces", "degree": 336.9258, "dms": "336:55:33", "rl": "Jupiter", "nl": "Saturn", "sl": "Mercury", "ssl": "Jupiter", "is_retro": false },
    "Saturn": { "sign": "Sagittarius", "degree": 259.5931, "dms": "259:35:35", "rl": "Jupiter", "nl": "Venus", "sl": "Rahu", "ssl": "Venus", "is_retro": false },
    "Rahu": { "sign": "Aquarius", "degree": 309.8131, "dms": "309:48:47", "rl": "Saturn", "nl": "Rahu", "sl": "Jupiter", "ssl": "Venus", "is_retro": true },
    "Ketu": { "sign": "Leo", "degree": 129.8131, "dms": "129:48:47", "rl": "Sun", "nl": "Ketu", "sl": "Saturn", "ssl": "Mercury", "is_retro": true }
  },
  "placidus_cusps": [
    { "cusp": 1, "degree": "048:54:20", "sign": "Taurus", "rl": "Venus", "nl": "Moon", "sl": "Mercury", "ssl": "Rahu" },
    { "cusp": 2, "degree": "073:22:19", "sign": "Gemini", "rl": "Mercury", "nl": "Rahu", "sl": "Mercury", "ssl": "Moon" },
    { "cusp": 10, "degree": "303:46:59", "sign": "Aquarius", "rl": "Saturn", "nl": "Mars", "sl": "Venus", "ssl": "Rahu" }
  ],
  "dasha_hierarchy": {
    "current_running": {
      "md": "Jupiter",
      "ad": "Rahu",
      "pd": "Saturn",
      "sd": "Mercury",
      "prd": "Venus",
      "period_end": "2027-02-19"
    }
  },
  "shadbala_summary": {
    "Sun": { "total_virupas": 457.58, "rupas": 7.63, "ratio": 1.53, "rank": 2 },
    "Moon": { "total_virupas": 399.81, "rupas": 6.66, "ratio": 1.11, "rank": 6 },
    "Jupiter": { "total_virupas": 602.89, "rupas": 10.05, "ratio": 1.55, "rank": 1 }
  },
  "ashtakavarga": {
    "sav_scores": [24, 24, 27, 32, 24, 22, 35, 25, 30, 28, 33, 33]
  }
}
"""
ast_data = json.loads(ast_json)
build_pdf_report("G:/software/simpa/VYAS/sample_report.pdf", ast_data)
print("PDF generated successfully.")
