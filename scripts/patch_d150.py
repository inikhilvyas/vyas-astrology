def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Target 1: D60 end
    target1 = '''                    var d60_deity_idx = isOdd ? d60_part : (59 - d60_part);
                    var deityName = D60_DEITIES[d60_deity_idx] + " (#" + (d60_deity_idx + 1) + ")";
                    addV("D60", 60, d60_sign, (deg * 60.0) % 30.0, deityName);

                    return v;'''

    repl1 = '''                    var d60_deity_idx = isOdd ? d60_part : (59 - d60_part);
                    var deityName = D60_DEITIES[d60_deity_idx] + " (#" + (d60_deity_idx + 1) + ")";
                    addV("D60", 60, d60_sign, (deg * 60.0) % 30.0, deityName);

                    // D150 Nadiamsha (0°12' = 12 arcminutes = 150 parts per sign)
                    var d150_part = Math.min(149, Math.floor(deg / 0.2));
                    addV("D150", 150, (pSign + d150_part) % 12, (deg * 150.0) % 30.0, "Nadiamsha #" + (d150_part + 1));

                    return v;'''

    # Target 2: loop guard
    target2 = '''                for (var vkIdx = 0; vkIdx < vKeys.length; vkIdx++) {
                    var vk = vKeys[vkIdx];
                    var ascV = ascVargas[vk];
                    var aSign = ascV.sign_index;'''

    repl2 = '''                for (var vkIdx = 0; vkIdx < vKeys.length; vkIdx++) {
                    var vk = vKeys[vkIdx];
                    var ascV = ascVargas[vk];
                    if (!ascV) continue;
                    var aSign = ascV.sign_index;'''

    # Target 3: pv guard
    target3 = '''                    var pn = order[pi];
                    var pv = planetVargas[pn][vk];
                    var hNum = ((pv.sign_index - aSign + 12) % 12) + 1;'''

    repl3 = '''                    var pn = order[pi];
                    var pv = planetVargas[pn][vk];
                    if (!pv) continue;
                    var hNum = ((pv.sign_index - aSign + 12) % 12) + 1;'''

    modified = False
    if target1 in content:
        content = content.replace(target1, repl1, 1)
        print(f"Patched target1 in {filepath}")
        modified = True
    else:
        print(f"target1 NOT matched in {filepath}")

    if target2 in content:
        content = content.replace(target2, repl2, 1)
        print(f"Patched target2 in {filepath}")
        modified = True
    else:
        print(f"target2 NOT matched in {filepath}")

    if target3 in content:
        content = content.replace(target3, repl3, 1)
        print(f"Patched target3 in {filepath}")
        modified = True
    else:
        print(f"target3 NOT matched in {filepath}")

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully saved {filepath}")

patch_file('index.html')
patch_file('mobile/index.html')
patch_file('android_app/app/src/main/assets/mobile/index.html')

