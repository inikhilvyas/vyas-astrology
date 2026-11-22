import os, shutil

new_ref_rows = """| `references/dhaga-tantra-chetna-vigyan.md` | प्रायोगिक धागा-तंत्र, दैहिक भाव-मानचित्रण, 12-ग्रह स्वामित्व, दीपक व पंचतत्व चेतना विज्ञान, वास्तु व औरा-रक्षा |
| `references/jyotish-upay-mahasangrah.md` | सर्व-दोष निवारण महायंत्र: तांत्रोक्त, मंत्रोक्त, यंत्रोक्त, दशमहाविद्या, द्वादश ज्योतिर्लिंग, 27 नक्षत्र मूल व लाल किताब |
| `references/nadi-hit-theory-lalkitab.md` | नाड़ी ज्योतिष, कस्पल सब-लॉर्ड हिट थ्योरी (विवाह 2,7,11, करियर 2,6,10,11), एस्ट्रो-वास्तु व सोए ग्रह |
| `references/bhrigu-saral-bcp-nadi.md` | भृगु सरल पद्धति (BSP 1-31 ग्रह दृष्टि व सक्रियण वर्ष), भृगु चक्र पद्धति (BCP 12-वर्षीय चक्र), कर्म विपाक |
| `references/lalkitab-amrit-teen-rina.md` | लाल किताब अमृत, तीन ऋण (पितृ, मातृ, स्त्री), सोए भाव 2/4/10 जगाना, अंधा टेवा, 43-दिवसीय विज्ञान |
| `references/karma-alignment-27nakshatra-bnn.md` | कर्म-संरेखण, तत्व-समय-स्थान, 27 नक्षत्र 27 पूजा विधियां, BNN 3-5-10 सक्रियण, वैकल्पिक भाव उपाय |"""

def update_skill(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out_lines = []
    in_ref_table = False
    ref_table_added = False

    for line in lines:
        if line.strip().startswith('| `references/output-templates.md`'):
            out_lines.append(line)
            # Add all references right after output-templates.md
            out_lines.append(new_ref_rows + '\n')
            ref_table_added = True
        elif ('dhaga-tantra-chetna-vigyan.md' in line or
              'jyotish-upay-mahasangrah.md' in line or
              'nadi-hit-theory-lalkitab.md' in line or
              'bhrigu-saral-bcp-nadi.md' in line or
              'lalkitab-amrit-teen-rina.md' in line or
              'karma-alignment-27nakshatra-bnn.md' in line):
            # Skip existing duplicates if re-running
            continue
        else:
            out_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
    print(f"Updated {filepath}")

skill_files = [
    'skills/vyas-jyotisha/SKILL.md',
    r'C:\Users\Administrator\.gemini\config\plugins\daivagya-astrology\skills\vyas-jyotisha\SKILL.md',
    r'C:\Users\Administrator\.gemini\config\plugins\ecc\skills\vyas-jyotisha\SKILL.md'
]
for sf in skill_files:
    update_skill(sf)
