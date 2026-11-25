import os

all_refs_table = """| `references/chart-state.md` | Building CHART_STATE / data lock, handoff schema, failure states |
| `references/methodologies.md` | Running any specific method; method registry and traps |
| `references/gates-and-arbitration.md` | Event ontology, domain matrix, ledger, double-count control, red-team, PSS, timing |
| `references/source-audit.md` | User gives a software report/PDF/book excerpt; source-to-chart comparison |
| `references/research-and-learning.md` | Sutra discovery, backtesting, outcomes, rule registry, rectification, Prashna, remedies |
| `references/output-templates.md` | Final structure per mode and the final source-audit checklist |
| `references/dhaga-tantra-chetna-vigyan.md` | प्रायोगिक धागा-तंत्र, दैहिक भाव-मानचित्रण, 12-ग्रह स्वामित्व, दीपक व पंचतत्व चेतना विज्ञान, वास्तु व औरा-रक्षा |
| `references/jyotish-upay-mahasangrah.md` | सर्व-दोष निवारण महायंत्र: तांत्रोक्त, मंत्रोक्त, यंत्रोक्त, दशमहाविद्या, द्वादश ज्योतिर्लिंग, 27 नक्षत्र मूल व लाल किताब |
| `references/nadi-hit-theory-lalkitab.md` | नाड़ी ज्योतिष, कस्पल सब-लॉर्ड हिट थ्योरी (विवाह 2,7,11, करियर 2,6,10,11), एस्ट्रो-वास्तु व सोए ग्रह |
| `references/bhrigu-saral-bcp-nadi.md` | भृगु सरल पद्धति (BSP 1-31 ग्रह दृष्टि व सक्रियण वर्ष), भृगु चक्र पद्धति (BCP 12-वर्षीय चक्र), कर्म विपाक |
| `references/lalkitab-amrit-teen-rina.md` | लाल किताब अमृत, तीन ऋण (पितृ, मातृ, स्त्री), सोए भाव 2/4/10 जगाना, अंधा टेवा, 43-दिवसीय विज्ञान |
| `references/karma-alignment-27nakshatra-bnn.md` | कर्म-संरेखण, तत्व-समय-स्थान, 27 नक्षत्र 27 पूजा विधियां, BNN 3-5-10 सक्रियण, वैकल्पिक भाव उपाय |
| `references/yantra-shastra-sampurna-siddha-vidhan.md` | संपूर्ण तांत्रिक यंत्र-शास्त्र: भोजपत्र-अनार कलम, 3x3 अंकीय नवग्रह यंत्र ग्रिड (योग 15-39), 12 सिद्ध कामना यंत्र |
| `references/parivarik-sambandh-navagraha-shanti-and-lagna-maraka.md` | 4-आचरण रामबाण नियम, पारिवारिक संबंधों से निःशुल्क ग्रह शांति, 12 लग्न मारक-योगकारक, कालराहु दिशा-यात्रा निषेध |
| `references/tithi-ahar-vastu-and-rudraksha-panchang-vidhan.md` | तिथि-वार वर्जित आहार (प्रतिपदा-पूर्णिमा), पाक्वा मिरर-घड़ी वास्तु, 7 वार विशिष्ट उपाय, 1-14 मुखी रुद्राक्ष |
| `references/nava-jyotishiya-sutra-ayu-and-mantra-dhwani.md` | 9 धन-नाश योग, भाव-नाश, 9 दीर्घायु सूत्र, 6 से 6 (11वां) विजय, षष्ठेश वार औषधि, क्रूर बनाम सौम्य मंत्र ध्वनि |
| `references/kp-cuspal-sublord-249-horary-and-ruling-planets.md` | केपी 3-स्तरीय नियम, 249 होरारी, प्लेसिडस भाव, ABCD सिग्निफिकेटर, अयुक्त स्व-बल, वक्री RP बहिष्करण, BTR |
| `references/rajayoga-balarishta-bhanga-kuja-and-muhurtha-mahagranth.md` | षड्बल राजयोग, पंचमहापुरुष, बालारिष्ट व कालसर्प भंग, कुज दोष अपवाद, 12 कूट विवाह, 21 महादोष व गुणबाहुल्य |
| `references/homa-tarpana-tithi-pravesha-and-panchakosha-vargas.md` | अग्नि-अनुनाद होम, 3 तर्पण तीर्थ, सायन-निरयण तिथि प्रवेश (वारेश/होरेश), नारायण दशा, पंचकोश वर्ग D1-D60 |
| `references/jaimini-upapada-ishta-devata-and-badhaka-ganesha.md` | उपपद लग्न विवाह रक्षा, AL छवि, कारकांश इष्ट/पालन/धर्म देव, 12 बाधक गणेश मंत्र, सवितृ गायत्री, शूल दशा |
| `references/siddha-sutra-mahasangrah-sapta-pramana.md` | 43 सिद्ध-सूत्र महा-संग्रह (सप्त-प्रमाण समन्वय: पाराशरी, जैमिनी, केपी, नाड़ी, लाल किताब, यंत्र, कर्म-संरेखण) |
| `references/samyukta-paddhati-chara-dasha-sav-and-double-transit.md` | संयुक्त पद्धति (पाराशरी+जैमिनी), 7 चर कारक, शनि-गुरु दोहरा गोचर, SAV 25 बिंदु, विष्णु सहस्रनाम |
| `references/jamindar-astra-yoga-grahan-nivarana-and-totke.md` | जमींदार व अस्त्र योग, 21 रत्न ग्रहण निवारण, 3री रोटी व 4 मिर्च टोटका, 3 बाल्टी जल, चांदी मछली, शिवलिंग नवग्रह अभिषेक |
| `references/rahu-vishesh-drishti-d10-and-dashamsha-havan.md` | लग्नेश-भाग्येश, राहु राशिपति दृष्टि 3/10 व 4/8, चंद्र से 12वां राहु, D10 दशमांश, 1/10 दशांश हवन, चित्रगुप्त डायरी |"""

def update_skill_complete(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    ref_heading = "## Reference map\n\n| File | Read when |\n|---|---|\n"
    idx = text.find(ref_heading)
    if idx == -1:
        ref_heading = "## Reference map\r\n\r\n| File | Read when |\r\n|---|---|\r\n"
        idx = text.find(ref_heading)

    if idx != -1:
        # replace everything in table
        new_text = text[:idx + len(ref_heading)] + all_refs_table + '\n'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"Updated complete reference map in {filepath}")
    else:
        print(f"Reference heading not found in {filepath}")

skill_files = [
    'skills/vyas-jyotisha/SKILL.md',
    r'C:\Users\Administrator\.gemini\config\plugins\daivagya-astrology\skills\vyas-jyotisha\SKILL.md',
    r'C:\Users\Administrator\.gemini\config\plugins\ecc\skills\vyas-jyotisha\SKILL.md'
]
for sf in skill_files:
    update_skill_complete(sf)

