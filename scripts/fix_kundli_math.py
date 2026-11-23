import os

def fix_all():
    # 1. Fix index.html first
    with open('index.html', 'r', encoding='utf-8') as f:
        d_content = f.read()

    old_d60_end = '''                var d60_deity_idx = isOdd ? d60_part : (59 - d60_part);
                var deityName = D60_DEITIES[d60_deity_idx] + " (#" + (d60_deity_idx + 1) + ")";
                addV("D60", 60, d60_sign, (deg * 60.0) % 30.0, deityName);

                return v;
            }'''

    new_d60_end = '''                var d60_deity_idx = isOdd ? d60_part : (59 - d60_part);
                var deityName = D60_DEITIES[d60_deity_idx] + " (#" + (d60_deity_idx + 1) + ")";
                addV("D60", 60, d60_sign, (deg * 60.0) % 30.0, deityName);

                // D150 Nadiamsha (0°12' = 12 arcminutes = 150 parts per sign)
                var d150_part = Math.min(149, Math.floor(deg / 0.2));
                addV("D150", 150, (pSign + d150_part) % 12, (deg * 150.0) % 30.0, "Nadiamsha #" + (d150_part + 1));

                return v;
            }'''

    old_loop_guard = '''            for (var vkIdx = 0; vkIdx < vKeys.length; vkIdx++) {
                var vk = vKeys[vkIdx];
                var ascV = ascVargas[vk];
                var aSign = ascV.sign_index;'''

    new_loop_guard = '''            for (var vkIdx = 0; vkIdx < vKeys.length; vkIdx++) {
                var vk = vKeys[vkIdx];
                var ascV = ascVargas[vk];
                if (!ascV) continue;
                var aSign = ascV.sign_index;'''

    old_pv_guard = '''                for (var pi = 0; pi < order.length; pi++) {
                    var pn = order[pi];
                    var pv = planetVargas[pn][vk];
                    var hNum = ((pv.sign_index - aSign + 12) % 12) + 1;'''

    new_pv_guard = '''                for (var pi = 0; pi < order.length; pi++) {
                    var pn = order[pi];
                    var pv = planetVargas[pn][vk];
                    if (!pv) continue;
                    var hNum = ((pv.sign_index - aSign + 12) % 12) + 1;'''

    if old_d60_end in d_content:
        d_content = d_content.replace(old_d60_end, new_d60_end, 1)
        print("Updated D150 in index.html calcVargasDetailed!")
    else:
        print("old_d60_end not found in index.html")

    if old_loop_guard in d_content:
        d_content = d_content.replace(old_loop_guard, new_loop_guard, 1)
        print("Updated loop guard in index.html!")
    else:
        print("old_loop_guard not found in index.html")

    if old_pv_guard in d_content:
        d_content = d_content.replace(old_pv_guard, new_pv_guard, 1)
        print("Updated pv guard in index.html!")
    else:
        print("old_pv_guard not found in index.html")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(d_content)

    # Re-read index.html to extract updated computeMathematicalKundli
    with open('index.html', 'r', encoding='utf-8') as f:
        updated_d_lines = f.readlines()

    # Find computeMathematicalKundli bounds in index.html
    d_start = None
    d_end = None
    for i, l in enumerate(updated_d_lines):
        if 'computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon)' in l and '{' in l:
            d_start = i
            break
    for i in range(d_start, len(updated_d_lines)):
        if 'return finalBundle;' in updated_d_lines[i]:
            d_end = i
            break

    print(f"Extracted desktop computeMathematicalKundli from {d_start} to {d_end}")
    d_cmk = ''.join(updated_d_lines[d_start:d_end+1]) + '\n        },\n'

    # Now patch mobile/index.html with this updated computeMathematicalKundli
    with open('mobile/index.html', 'r', encoding='utf-8') as f:
        m_lines = f.readlines()

    m_start = None
    m_end = None
    for i, l in enumerate(m_lines):
        if 'computeMathematicalKundli(name, dobStr, tobStr,' in l and '{' in l:
            m_start = i
            break
    for i in range(m_start, len(m_lines)):
        if 'return finalBundle;' in m_lines[i] or 'return {' in m_lines[i]:
            # find end of function
            for j in range(i, min(i+50, len(m_lines))):
                if m_lines[j].strip() == '},':
                    m_end = j
                    break
            break

    print(f"Mobile computeMathematicalKundli is from {m_start} to {m_end}")

    new_m_lines = m_lines[:m_start] + [d_cmk] + m_lines[m_end+1:]
    m_content = ''.join(new_m_lines)

    with open('mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(m_content)

    with open('android_app/app/src/main/assets/mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(m_content)

    print("Patched mobile/index.html and assets/mobile/index.html with robust Swiss Ephemeris engine!")

if __name__ == '__main__':
    fix_all()

