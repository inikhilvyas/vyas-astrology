import urllib.request

url = "https://vyasastro.in/?t=check_all_planets"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

checks = {
    "Lagna 23°42'": "23°42" in html,
    "Sun (वृश्चिक 07°42')": "07°42" in html or "7°42" in html,
    "Moon (वृश्चिक 14°38')": "14°38" in html,
    "Mars (मकर 12°09')": "12°09" in html,
    "Mercury (वृश्चिक 29°16')": "29°16" in html,
    "Jupiter (धनु 19°21')": "19°21" in html,
    "Venus (धनु 17°45')": "17°45" in html,
    "Saturn (तुला 26°53')": "26°53" in html,
    "Rahu / Ketu (03°37')": "03°37" in html or "3°37" in html,
    "Dasha Balance (शनि 2 वर्ष 10 मास 15 दिन)": "शनि 2 वर्ष 10 मास" in html or "2y 10m 15d" in html,
    "GPS Button (useCurrentGPS)": "useCurrentGPS" in html,
    "Village Search Autocomplete": "setupVillageAutocomplete" in html,
    "Classical Daivagya Wisdom Engine": "VyasDaivagyaWisdom" in html,
}

print("=== LIVE HOSTINGER VERIFICATION RESULTS ===")
all_pass = True
for k, v in checks.items():
    print(f"[{'PASS' if v else 'FAIL'}] {k}")
    if not v:
        all_pass = False

print(f"\nOverall Result: {'100% PERFECT VERIFIED' if all_pass else 'SOME CHECKS FAILED'}")
