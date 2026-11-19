import shutil

path = 'mobile/index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
in_quick_login = False
in_hardcoded_swiss = False

for i, line in enumerate(lines):
    # 1. Skip quickLoginFounder block
    if 'quickLoginFounder: function()' in line:
        in_quick_login = True
        continue
    if in_quick_login:
        if 'isEnglishMode: false,' in line:
            in_quick_login = False
            new_lines.append(line)
        continue

    # 2. Skip hardcoded swiss ephemeris precision lock for founder in mobile computeMathematicalKundli
    if 'var isNikhilVyas = (dobStr === "1984-11-23")' in line:
        in_hardcoded_swiss = True
        continue
    if in_hardcoded_swiss:
        if 'var RAD = Math.PI / 180.0;' in line:
            in_hardcoded_swiss = False
            new_lines.append(line)
        continue

    # 3. Time fallback
    if 'if (!tob) tob = "16:51";' in line:
        new_lines.append('        if (!tob) tob = "12:00";\n')
        continue

    # 4. Dasha fallback
    if 'var dobStr = prof.dob || "1984-11-23";' in line:
        new_lines.append('            var dobStr = prof.dob || "2000-01-01";\n')
        continue
    if 'var tobStr = prof.tob || "16:51";' in line:
        new_lines.append('            var tobStr = prof.tob || "12:00";\n')
        continue
    if 'if (isNaN(birthMs)) birthMs = new Date("1984-11-23T16:51:00+05:30").getTime();' in line:
        new_lines.append('            if (isNaN(birthMs)) birthMs = new Date("2000-01-01T12:00:00+05:30").getTime();\n')
        continue
    if 'var moonLon = 224.639;' in line:
        new_lines.append('            var moonLon = 0.0;\n')
        continue

    # 5. Pro email display placeholder
    if 'nikhilvyas007@gmail.com' in line and 'proUserEmailText' in line:
        new_lines.append('                <b id="proUserEmailText" style="color:#f8fafc;">सदस्य</b>\n')
        continue

    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

# Copy to android asset
target_android = 'android_app/app/src/main/assets/mobile/index.html'
shutil.copyfile(path, target_android)
print(f"Successfully cleaned {path} and updated {target_android}")

