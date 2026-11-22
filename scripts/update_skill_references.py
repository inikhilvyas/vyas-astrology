import shutil, os

with open('skills/vyas-jyotisha/SKILL.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'output-templates.md' in line and '|' in line:
        new_lines.append(line)
        new_lines.append('| `references/brajesh-gautam-dhaga-tantra.md` | Brajesh Gautam Dhaaga Tantra, body-house mapping, 12-planet lordship, cotton-ghee diya rules, Vastu & Chetna Vigyan |\n')
        new_lines.append('| `references/jyotish-upay-mahasangrah.md` | Omni-remedies: Tantrokt, Mantrokt, Yantrokt, 10 Mahavidyas, 12 Jyotirlingas, 27 Nakshatras roots & samputa, Lal Kitab 10 rules |\n')
    elif line.strip().startswith('- Remedies (`references/research-and-learning.md`):'):
        new_lines.append('- Remedies (`references/research-and-learning.md`, `references/brajesh-gautam-dhaga-tantra.md`, `references/jyotish-upay-mahasangrah.md`): diagnosis → mechanism → remedy; optional, tradition-labelled, non-coercive; includes Vardhana vs Shaman distinction, Body-House Dhaaga Tantra (wrist, waist, ankle, bicep), Cotton-Ghee Diya mechanics, Vastu North-East/Brahmasthan, 10 Mahavidyas for afflicted planets/dashas, 12 Jyotirlingas, and Lal Kitab 10 cardinal rules; never invent mantras/seed syllables; no guarantees; no costly gemstone push without functional-lordship/affliction/contraindication analysis.\n')
    else:
        new_lines.append(line)

with open('skills/vyas-jyotisha/SKILL.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Successfully wrote skills/vyas-jyotisha/SKILL.md')

plugins = [
    r'C:\Users\Administrator\.gemini\config\plugins\daivagya-astrology\skills\vyas-jyotisha\SKILL.md',
    r'C:\Users\Administrator\.gemini\config\plugins\ecc\skills\vyas-jyotisha\SKILL.md'
]
for p in plugins:
    shutil.copy2('skills/vyas-jyotisha/SKILL.md', p)
    print('Synced to', p)

