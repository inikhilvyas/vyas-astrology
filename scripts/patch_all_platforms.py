import os
import re

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist.")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix solveExactPlacidus call: jd_ut -> jd
    old_call = "solveExactPlacidus(ascSid, lat, ayanamsa, jd_ut)"
    new_call = "solveExactPlacidus(ascSid, lat, ayanamsa, (typeof jd !== 'undefined' ? jd : 2451545.0))"
    if old_call in content:
        content = content.replace(old_call, new_call)
        print(f"[{filepath}] Replaced jd_ut with jd")

    # 2. Fix duplicate kpCusps[c] = cuspItem
    content = re.sub(
        r'kpCusps\.push\(cuspItem\);[\r\n\s]+kpCusps\[c\]\s*=\s*cuspItem;',
        'kpCusps.push(cuspItem);',
        content
    )

    # 3. Bump engine version
    content = content.replace(
        "var CURRENT_ENGINE_VERSION = 'v5.0_pure_math_parashari_2026';",
        "var CURRENT_ENGINE_VERSION = 'v6.0_placidus_bhavatbhavam_2026';"
    )
    content = content.replace("_engine_ver: 5.2,", "_engine_ver: 6.0,")
    content = content.replace("userVault._engine_ver < 5.2", "userVault._engine_ver < 6.0")
    content = content.replace("data._engine_ver < 5.2", "data._engine_ver < 6.0")
    content = content.replace("fromVault._engine_ver < 5.2", "fromVault._engine_ver < 6.0")

    # 4. Add multi-cusp equality check to force recomputation of old equal-house cusps
    old_eq_check = "if (userVault.kp.cusps[0].deg === userVault.kp.cusps[1].deg || !userVault.kp.cusps[0].longitude) needsRecompU = true;"
    new_eq_check = """if (!userVault.kp.cusps[0].longitude || userVault.kp.cusps.length !== 12) needsRecompU = true;
                    if (!needsRecompU && userVault.kp.cusps.length >= 2) {
                        for (var ci = 0; ci < userVault.kp.cusps.length - 1; ci++) {
                            if (userVault.kp.cusps[ci] && userVault.kp.cusps[ci+1] && userVault.kp.cusps[ci].deg === userVault.kp.cusps[ci+1].deg) {
                                needsRecompU = true; break;
                            }
                        }
                    }"""
    if old_eq_check in content:
        content = content.replace(old_eq_check, new_eq_check)

    old_data_check = "if (data.kp.cusps[0].deg === data.kp.cusps[1].deg || !data.kp.cusps[0].longitude) needsRecomp = true;"
    new_data_check = """if (!data.kp.cusps[0].longitude || data.kp.cusps.length !== 12) needsRecomp = true;
                            if (!needsRecomp && data.kp.cusps.length >= 2) {
                                for (var ci = 0; ci < data.kp.cusps.length - 1; ci++) {
                                    if (data.kp.cusps[ci] && data.kp.cusps[ci+1] && data.kp.cusps[ci].deg === data.kp.cusps[ci+1].deg) {
                                        needsRecomp = true; break;
                                    }
                                }
                            }"""
    if old_data_check in content:
        content = content.replace(old_data_check, new_data_check)

    old_from_vault = "if (fromVault.kp.cusps[0].deg === fromVault.kp.cusps[1].deg || !fromVault.kp.cusps[0].longitude) needsRecompV = true;"
    new_from_vault = """if (!fromVault.kp.cusps[0].longitude || fromVault.kp.cusps.length !== 12) needsRecompV = true;
                            if (!needsRecompV && fromVault.kp.cusps.length >= 2) {
                                for (var ci = 0; ci < fromVault.kp.cusps.length - 1; ci++) {
                                    if (fromVault.kp.cusps[ci] && fromVault.kp.cusps[ci+1] && fromVault.kp.cusps[ci].deg === fromVault.kp.cusps[ci+1].deg) {
                                        needsRecompV = true; break;
                                    }
                                }
                            }"""
    if old_from_vault in content:
        content = content.replace(old_from_vault, new_from_vault)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{filepath}] Patched successfully.")

for target in ['index.html', 'mobile/index.html', 'static/mobile/index.html']:
    patch_file(target)
