# Test high-precision JS ephemeris against Skyfield
import math
from datetime import datetime, timezone, timedelta
import sys
sys.path.insert(0, 'src')

# Real values from Skyfield:
# Ascendant: 97.9999 (Cancer 7°59')
# Sun: 30.390 (Taurus 0°23')
# Moon: 269.843 (Sagittarius 29°50')
# Mars: 324.392 (Aquarius 24°23')
# Mercury: 14.326 (Aries 14°19')
# Jupiter: 75.761 (Gemini 15°45')
# Venus: 348.761 (Pisces 18°45')
# Saturn: 271.529 (Capricorn 1°31')
# Rahu: 287.626 (Capricorn 17°37')
# Ketu: 107.626 (Cancer 17°37')

print("Skyfield baseline loaded.")

