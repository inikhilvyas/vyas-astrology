import json

SIGNS_HI = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']
SIGNS_EN = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def calc_vargas_detailed(lon):
    pSign = int(lon // 30.0) % 12
    deg = lon % 30.0
    isOdd = (pSign % 2 == 0) # 0-indexed: 0=Aries (Odd)
    v = {}
    
    def add_v(k, num, s, d):
        v[k] = {'key': k, 'num': num, 'sign_index': s, 'sign_name': SIGNS_HI[s], 'deg': d}
        
    add_v('D1', 1, pSign, deg)
    d2_sign = (4 if deg < 15.0 else 3) if isOdd else (3 if deg < 15.0 else 4)
    add_v('D2', 2, d2_sign, (deg * 2.0) % 30.0)
    add_v('D3', 3, (pSign + int(deg // 10.0) * 4) % 12, (deg * 3.0) % 30.0)
    add_v('D4', 4, (pSign + int(deg // 7.5) * 3) % 12, (deg * 4.0) % 30.0)
    d7_sign = (pSign + int(deg // (30.0/7.0))) % 12 if isOdd else (pSign + 6 + int(deg // (30.0/7.0))) % 12
    add_v('D7', 7, d7_sign, (deg * 7.0) % 30.0)
    
    # D9 Navamsha
    d9_element = pSign % 4
    d9_starts = [0, 9, 6, 3]
    add_v('D9', 9, (d9_starts[d9_element] + int(deg // (30.0/9.0))) % 12, (deg * 9.0) % 30.0)
    
    # D10 Dashamsha
    d10_start = pSign if isOdd else (pSign + 8) % 12
    add_v('D10', 10, (d10_start + int(deg // 3.0)) % 12, (deg * 10.0) % 30.0)
    
    add_v('D12', 12, (pSign + int(deg // 2.5)) % 12, (deg * 12.0) % 30.0)
    d16_start = 0 if (pSign % 3 == 0) else (4 if (pSign % 3 == 1) else 8)
    add_v('D16', 16, (d16_start + int(deg // 1.875)) % 12, (deg * 16.0) % 30.0)
    d20_start = 0 if (pSign % 3 == 0) else (8 if (pSign % 3 == 1) else 4)
    add_v('D20', 20, (d20_start + int(deg // 1.5)) % 12, (deg * 20.0) % 30.0)
    add_v('D24', 24, ((4 if isOdd else 3) + int(deg // 1.25)) % 12, (deg * 24.0) % 30.0)
    d27_starts = [0, 3, 6, 9]
    add_v('D27', 27, (d27_starts[pSign % 4] + int(deg // (30.0/27.0))) % 12, (deg * 27.0) % 30.0)
    
    if isOdd:
        d30_s = 0 if deg < 5.0 else (10 if deg < 10.0 else (8 if deg < 18.0 else (2 if deg < 25.0 else 6)))
    else:
        d30_s = 1 if deg < 5.0 else (5 if deg < 12.0 else (11 if deg < 20.0 else (9 if deg < 25.0 else 7)))
    add_v('D30', 30, d30_s, (deg * 30.0) % 30.0)
    
    add_v('D40', 40, ((0 if isOdd else 6) + int(deg // 0.75)) % 12, (deg * 40.0) % 30.0)
    d45_start = 0 if (pSign % 3 == 0) else (4 if (pSign % 3 == 1) else 8)
    add_v('D45', 45, (d45_start + int(deg // (30.0/45.0))) % 12, (deg * 45.0) % 30.0)
    add_v('D60', 60, (pSign + int(deg // 0.5)) % 12, (deg * 60.0) % 30.0)
    return v

# Test building full charts for Nikhil Vyas
asc_nikhil = 23.7
v_asc = calc_vargas_detailed(asc_nikhil)
print('Nikhil Vyas (Aries 23.7°):')
for vk in ['D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60']:
    print(f'  {vk}: {v_asc[vk]["sign_name"]} ({v_asc[vk]["sign_index"]+1})')

# Test building full charts for User 2 (Taurus Lagna 14.5°)
asc_u2 = 44.5
v_asc_u2 = calc_vargas_detailed(asc_u2)
print('\nUser 2 (Taurus 14.5°):')
for vk in ['D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60']:
    print(f'  {vk}: {v_asc_u2[vk]["sign_name"]} ({v_asc_u2[vk]["sign_index"]+1})')
