import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from vyas.pdf_builder import build_pdf_report

ast_json = """
{
  "native_meta": {
    "name": "Piyush Sharma",
    "dob": "24/03/1989",
    "tob": "10:15:39",
    "pob": "Pali, Rajasthan, India",
    "ayanamsha_type": "KP_New",
    "ayanamsha_deg": "023:36:59"
  },
  "planetary_positions": {
    "Lagna": { "sign": "Taurus", "degree": 48.9055, "dms": "048:54:20", "rl": "Venus", "nl": "Moon", "sl": "Mercury", "ssl": "Rahu", "nakshatra": "Rohini", "pada": 1 },
    "Sun": { "sign": "Pisces", "degree": 339.9186, "dms": "339:55:07", "rl": "Jupiter", "nl": "Saturn", "sl": "Venus", "ssl": "Mercury", "nakshatra": "Uttara Bhadrapada", "pada": 2 }
  },
  "dasha_hierarchy": {
    "current_running": {
      "md": "Jupiter",
      "ad": "Rahu",
      "pd": "Saturn",
      "period_end": "2027-02-19"
    }
  }
}
"""
ast_data = json.loads(ast_json)
build_pdf_report("G:/software/simpa/VYAS/sample_report2.pdf", ast_data)
print("PDF generated successfully.")
