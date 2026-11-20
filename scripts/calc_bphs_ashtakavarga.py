# BPHS Standard Ashtakavarga Bindu points (1-indexed house from planet/lagna)

bphs_rules = {
    'Sun': {
        'Sun': [1, 2, 4, 7, 8, 9, 10, 11],
        'Moon': [3, 6, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [5, 6, 9, 11],
        'Venus': [6, 7, 12],
        'Saturn': [1, 2, 4, 7, 8, 9, 10, 11],
        'Lagna': [3, 4, 6, 10, 11, 12]
    },
    'Moon': {
        'Sun': [3, 6, 7, 8, 10, 11],
        'Moon': [1, 3, 6, 7, 10, 11],
        'Mars': [2, 3, 5, 6, 9, 10, 11],
        'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
        'Jupiter': [1, 4, 7, 8, 10, 11, 12],
        'Venus': [3, 4, 5, 7, 9, 10, 11],
        'Saturn': [3, 5, 6, 11],
        'Lagna': [3, 6, 10, 11]
    },
    'Mars': {
        'Sun': [3, 5, 6, 10, 11],
        'Moon': [3, 6, 11],
        'Mars': [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [3, 5, 6, 11],
        'Jupiter': [6, 10, 11, 12],
        'Venus': [6, 8, 11, 12],
        'Saturn': [1, 4, 7, 8, 9, 10, 11],
        'Lagna': [1, 3, 6, 10, 11]
    },
    'Mercury': {
        'Sun': [5, 6, 9, 11, 12],
        'Moon': [2, 4, 6, 8, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [6, 8, 11, 12],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 11],
        'Saturn': [1, 2, 4, 7, 8, 9, 10, 11],
        'Lagna': [1, 2, 4, 6, 8, 10, 11]
    },
    'Jupiter': {
        'Sun': [1, 2, 3, 4, 7, 8, 9, 10, 11],
        'Moon': [2, 5, 7, 9, 11],
        'Mars': [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
        'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
        'Venus': [2, 5, 6, 9, 10, 11],
        'Saturn': [3, 5, 6, 12],
        'Lagna': [1, 2, 4, 5, 6, 7, 9, 10, 11]
    },
    'Venus': {
        'Sun': [8, 11, 12],
        'Moon': [1, 2, 3, 4, 5, 8, 9, 11, 12],
        'Mars': [3, 5, 6, 9, 11, 12],
        'Mercury': [3, 5, 6, 9, 11],
        'Jupiter': [5, 8, 9, 10, 11],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 10, 11],
        'Saturn': [3, 4, 5, 8, 9, 10, 11],
        'Lagna': [1, 2, 3, 4, 5, 8, 9, 11]
    },
    'Saturn': {
        'Sun': [1, 2, 4, 7, 8, 10, 11],
        'Moon': [3, 6, 11],
        'Mars': [3, 5, 6, 10, 11, 12],
        'Mercury': [6, 8, 9, 10, 11, 12],
        'Jupiter': [5, 6, 11, 12],
        'Venus': [6, 11, 12],
        'Saturn': [3, 5, 6, 11],
        'Lagna': [1, 3, 4, 6, 10, 11]
    }
}

# Nikhil Vyas Planet Signs (0-indexed: Aries=0, Taurus=1, ..., Pisces=11):
# Lagna: Aries (0)
# Sun: Scorpio (7)
# Moon: Scorpio (7)
# Mars: Capricorn (9)
# Mercury: Scorpio (7)
# Jupiter: Sagittarius (8)
# Venus: Sagittarius (8)
# Saturn: Libra (6)

planet_signs = {
    'Sun': 7,
    'Moon': 7,
    'Mars': 9,
    'Mercury': 7,
    'Jupiter': 8,
    'Venus': 8,
    'Saturn': 6,
    'Lagna': 0
}

sav_by_sign = [0] * 12
bav_results = {}

for target_planet, contributors in bphs_rules.items():
    bav = [0] * 12
    for donor, houses in contributors.items():
        donor_sign = planet_signs[donor]
        for h in houses:
            # House h from donor_sign (1-indexed house: h=1 is donor_sign itself)
            benefic_sign = (donor_sign + h - 1) % 12
            bav[benefic_sign] += 1
            sav_by_sign[benefic_sign] += 1
    bav_results[target_planet] = bav

print("SAV by Sign (Aries=0 to Pisces=11):")
for s in range(12):
    print(f"Sign {s+1}: {sav_by_sign[s]} bindus")
print(f"Total SAV: {sum(sav_by_sign)}")

# Now SAV by Bhava from Lagna (Lagna = sign 0):
# Since Lagna is sign 0 (Aries), Bhava 1 = Sign 0 (Aries), Bhava 2 = Sign 1 (Taurus), etc.
print("\nBAV by Planet:")
for p, b in bav_results.items():
    print(f"{p:8s} sum={sum(b)}: {b}")

