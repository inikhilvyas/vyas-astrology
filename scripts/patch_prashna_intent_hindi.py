# scripts/patch_prashna_intent_hindi.py

for path in ['index.html', 'mobile/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    old_intent = """            if (/mla|mp|chunav|chunaw|neta|rajneeti|politics|election|career|naukri|job|promotion|pad|adhikar|shasan|sarkar|ias|ips/.test(q)) {
                karyaHouse = 10;
                karyaDesc = "दशम भाव (राज्य पद, चुनाव, शासन सत्ता व कर्म सिद्धि)";
            } else if (/vivah|shadi|marriage|patni|pati|prem|love|rishta|sambandh|jeewansaathi/.test(q)) {
                karyaHouse = 7;
                karyaDesc = "सप्तम भाव (विवाह, दांपत्य व जीवनसाथी)";
            } else if (/paisa|dhan|sampatti|labh|wealth|money|business|vyapar|profit|kamai|karz|loan|loss/.test(q)) {
                karyaHouse = 11;
                karyaDesc = "एकादश व द्वितीय भाव (धन, लाभ, व्यापारिक वृद्धि व संचित कोष)";
            } else if (/santan|bacha|garbh|pregnancy|child|padhai|exam|upsc|pariksha|education|study/.test(q)) {
                karyaHouse = 5;
                karyaDesc = "पंचम भाव (संतान सुख, परीक्षा व विद्या अर्जन)";
            } else if (/court|case|mukadma|police|shatru|rog|bimar|bimari|health|swasthya/.test(q)) {
                karyaHouse = 6;
                karyaDesc = "षष्ठ भाव (रोग, ऋण, विवाद व शत्रु विजय)";
            } else if (/yatra|videsh|foreign|travel|visa|sthanantaran|transfer/.test(q)) {
                karyaHouse = 9;
                karyaDesc = "नवम व द्वादश भाव (विदेश यात्रा, भाग्य व स्थान परिवर्तन)";
            }"""

    new_intent = """            if (/mla|mp|chunav|chunaw|neta|rajneeti|politics|election|career|naukri|job|promotion|pad|adhikar|shasan|sarkar|ias|ips|चुनाव|राजनीति|नेता|विधायक|सांसद|नौकरी|करियर|पदोन्नति|प्रमोशन|पद|अधिकार|शासन|सरकार|प्रशासन|मंत्री|इलेक्शन/i.test(q)) {
                karyaHouse = 10;
                karyaDesc = "दशम भाव (राज्य पद, चुनाव, शासन सत्ता व कर्म सिद्धि)";
            } else if (/vivah|shadi|marriage|patni|pati|prem|love|rishta|sambandh|jeewansaathi|विवाह|शादी|पत्नी|पति|प्रेम|प्यार|रिश्ता|सम्बन्ध|जीवनसाथी|दांपत्य|सगाई/i.test(q)) {
                karyaHouse = 7;
                karyaDesc = "सप्तम भाव (विवाह, दांपत्य व जीवनसाथी)";
            } else if (/paisa|dhan|sampatti|labh|wealth|money|business|vyapar|profit|kamai|karz|loan|loss|पैसा|धन|संपत्ति|सम्पत्ति|लाभ|व्यापार|कमाइ|कमाई|कर्ज|ऋण|मुनाफा|नुकसान|लॉटरी/i.test(q)) {
                karyaHouse = 11;
                karyaDesc = "एकादश व द्वितीय भाव (धन, लाभ, व्यापारिक वृद्धि व संचित कोष)";
            } else if (/santan|bacha|garbh|pregnancy|child|padhai|exam|upsc|pariksha|education|study|संतान|बच्चा|गर्भ|गर्भावस्था|पढ़ाई|शिक्षा|परीक्षा|एग्जाम|रिजल्ट|विद्या/i.test(q)) {
                karyaHouse = 5;
                karyaDesc = "पंचम भाव (संतान सुख, परीक्षा व विद्या अर्जन)";
            } else if (/court|case|mukadma|police|shatru|rog|bimar|bimari|health|swasthya|कोर्ट|कचहरी|केस|मुकदमा|पुलिस|शत्रु|रोग|बीमारी|तबीयत|स्वास्थ्य|दवा/i.test(q)) {
                karyaHouse = 6;
                karyaDesc = "षष्ठ भाव (रोग, ऋण, विवाद व शत्रु विजय)";
            } else if (/yatra|videsh|foreign|travel|visa|sthanantaran|transfer|यात्रा|विदेश|सफर|वीजा|स्थान परिवर्तन|तबादला/i.test(q)) {
                karyaHouse = 9;
                karyaDesc = "नवम व द्वादश भाव (विदेश यात्रा, भाग्य व स्थान परिवर्तन)";
            }"""

    if old_intent in text:
        text = text.replace(old_intent, new_intent)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✓ Successfully upgraded Prashna regex in {path}")
    else:
        print(f"! Old intent not found in {path}")
