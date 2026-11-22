import os, re, shutil

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find Sub-card B end
    target = "h += '</ul></div>';"
    sub_card_b_marker = "// Sub-card B: Shaman (Pacification)"
    
    idx_marker = text.find(sub_card_b_marker)
    if idx_marker == -1:
        print(f"Marker not found in {filepath}")
        return False

    idx_target = text.find(target, idx_marker)
    if idx_target == -1:
        print(f"Target not found after marker in {filepath}")
        return False

    cut_point = idx_target + len(target)

    # Let's inspect what follows immediately
    next_snippet = text[cut_point:cut_point+300]
    print(f"Snippet following cut_point in {filepath}:\n{next_snippet}")

    # Build injection code for Sub-card C and Sub-card D
    injection = """

                // Sub-card C: 🧵 ज्योतिषाचार्य बृजेश गौतम 'धागा-तंत्र' एवं चेतना विज्ञान
                var dhagaText = '';
                var queryDomain = (badge + ' ' + title).toLowerCase();
                if (/शासन|करियर|आजीविका|पद/i.test(queryDomain)) {
                    dhagaText = '<b>दाहिनी भुजा (Right Bicep/Arm):</b> लाल अथवा पीला सूती रक्षासूत्र ७ फेरे देकर अभिमंत्रित कर बाँधें (दशम भाव, आजीविका व पराक्रम संवर्धन)।';
                } else if (/विवाह|दांपत्य|सम्बन्ध/i.test(queryDomain)) {
                    dhagaText = '<b>कमर (Waist):</b> लाल अथवा नारंगी सूती धागा धारण करें (सप्तम भाव कलत्र रेखा, वीर्य/रज शुद्धि एवं आकर्षण समन्वय)।';
                } else if (/धन|समृद्धि|कोष/i.test(queryDomain)) {
                    dhagaText = '<b>गले में अथवा बायाँ टखना (Left Ankle):</b> पीला सूती धागा धारण करें (द्वितीय भाव संचित कोष व बृहस्पति-शुक्र ऊर्जा संरेखण)।';
                } else if (/आरोग्य|स्वास्थ्य|रोग/i.test(queryDomain)) {
                    dhagaText = '<b>दाहिना टखना या अंगूठा (Right Ankle/Toe):</b> काला सूती धागा बाँधें (षष्ठ भाव रोग-शत्रु-ऋण शमन एवं पृथ्वी तत्त्व ग्राउंडिंग)।';
                } else if (/संतान|विद्या/i.test(queryDomain)) {
                    dhagaText = '<b>दाहिनी कलाई (Right Wrist):</b> केसरिया अथवा पीला सूती धागा ५ फेरे देकर बाँधें (पंचम भाव देवगुरु व विद्या संवर्धन)।';
                } else if (/विदेश|यात्रा|व्यय/i.test(queryDomain)) {
                    dhagaText = '<b>दाहिने पैर का अंगूठा:</b> काला सूती धागा बाँधें व रात्रि सिरहाने जलपात्र रखें (द्वादश भाव व्यय नियंत्रण व निद्रा शुद्धि)।';
                } else {
                    dhagaText = '<b>दाहिनी कलाई (Right Wrist):</b> ' + (lagnaLord === 'शनि' || lagnaLord === 'राहु' ? 'नीला/काला' : 'पीला/लाल') + ' सूती धागा ५ फेरे देकर बाँधें (लग्नेश ' + lagnaLord + ' का आत्म-बल संरक्षण)।';
                }

                var deepakVastu = '<b>दीपक एवं वास्तु चेतना:</b> गोल (फूल) बत्ती सदैव समकोण पर प्रज्वलित करें। लम्बी बत्ती केवल देवियों व पितरों हेतु उपयोग करें। उत्तर-पूर्व (ईशान) व ब्रह्मस्थान को सदैव भार-मुक्त व निर्मल रखें।';

                h += '<div style=\"background:rgba(15,23,42,0.7); border:1px solid rgba(251,191,36,0.3); border-radius:8px; padding:12px 14px;\">';
                h += '<div style=\"display:flex; align-items:center; gap:6px; margin-bottom:8px;\">';
                h += '<span style=\"color:#fbbf24; font-size:1rem;\">🧵</span>';
                h += '<b style=\"color:#fbbf24; font-size:0.88rem;\">धागा-तंत्र एवं चेतना विज्ञान (बृजेश गौतम सूत्र)</b>';
                h += '</div>';
                h += '<div style=\"font-size:0.75rem; color:#94a3b8; margin-bottom:8px;\">शरीर-भाव संरेखण एवं पंचतत्व चेतना विज्ञान:</div>';
                h += '<ul style=\"margin:0; padding-left:16px; font-size:0.84rem; line-height:1.65; color:var(--text-secondary);\">';
                h += '<li style=\"margin-bottom:6px;\">' + dhagaText + '</li>';
                h += '<li style=\"margin-bottom:6px;\">' + deepakVastu + '</li>';
                h += '</ul></div>';

                // Sub-card D: 🔱 दशमहाविद्या, द्वादश ज्योतिर्लिंग एवं लाल किताब कवच
                var mdMatch = dashaChain.match(/(सूर्य|चन्द्र|मंगल|बुध|गुरु|शुक्र|शनि|राहु|केतु)/);
                var activePl = mdMatch ? mdMatch[1] : lagnaLord;
                var mvMap = {
                    'सूर्य': { mv: 'माँ मातंगी / तारा', jl: 'श्री सोमनाथ ज्योतिर्लिंग' },
                    'चन्द्र': { mv: 'माँ भुवनेश्वरी', jl: 'श्री मल्लिकार्जुन ज्योतिर्लिंग' },
                    'मंगल': { mv: 'माँ बगलामुखी', jl: 'श्री महाकालेश्वर ज्योतिर्लिंग' },
                    'बुध': { mv: 'माँ त्रिपुर भैरवी / षोडशी', jl: 'श्री ओंकारेश्वर ज्योतिर्लिंग' },
                    'गुरु': { mv: 'माँ तारा', jl: 'श्री वैद्यनाथ ज्योतिर्लिंग / केदारनाथ' },
                    'शुक्र': { mv: 'माँ कमला (महालक्ष्मी)', jl: 'श्री भीमाशंकर / काशी विश्वनाथ' },
                    'शनि': { mv: 'माँ दक्षिण कालिका', jl: 'श्री त्र्यंबकेश्वर ज्योतिर्लिंग' },
                    'राहु': { mv: 'माँ छिन्नमस्ता', jl: 'श्री नागेश्वर ज्योतिर्लिंग' },
                    'केतु': { mv: 'माँ धूमावती', jl: 'श्री रामेश्वरम / घृष्णेश्वर ज्योतिर्लिंग' }
                };
                var mvData = mvMap[activePl] || mvMap['गुरु'];
                var lkRule = 'छत पर जंग लगा लोहा, कबाड़ या टूटे कांच कभी एकत्रित न होने दें। नित्य पहली रोटी गौमाता को एवं अंतिम टुकड़ा श्वान (कुत्ते) को अर्पित करें।';

                h += '<div style=\"background:rgba(15,23,42,0.7); border:1px solid rgba(168,85,247,0.3); border-radius:8px; padding:12px 14px;\">';
                h += '<div style=\"display:flex; align-items:center; gap:6px; margin-bottom:8px;\">';
                h += '<span style=\"color:#c084fc; font-size:1rem;\">🔱</span>';
                h += '<b style=\"color:#c084fc; font-size:0.88rem;\">दशमहाविद्या, ज्योतिर्लिंग एवं लाल किताब</b>';
                h += '</div>';
                h += '<div style=\"font-size:0.75rem; color:#94a3b8; margin-bottom:8px;\">सक्रिय दशानाथ (' + activePl + ') अधिष्ठात्री शक्ति एवं अचूक व्यवहार-शुद्धि:</div>';
                h += '<ul style=\"margin:0; padding-left:16px; font-size:0.84rem; line-height:1.65; color:var(--text-secondary);\">';
                h += '<li style=\"margin-bottom:6px;\"><b>दशमहाविद्या व ज्योतिर्लिंग:</b> सक्रिय दशानाथ ' + activePl + ' हेतु अधिष्ठात्री <b>' + mvData.mv + '</b> की साधना व <b>' + mvData.jl + '</b> का मानसिक ध्यान/अभिषेक।</li>';
                h += '<li style=\"margin-bottom:6px;\"><b>लाल किताब अखंड नियम:</b> ' + lkRule + '</li>';
                h += '</ul></div>';
"""
    new_text = text[:cut_point] + injection + text[cut_point:]

    # Also update the footer note
    old_note = "वेध आधार: महर्षि पराशर, महर्षि जैमिनी, भृगु नन्दी नाड़ी, के.एस. कृष्णमूर्ति (KP) व आधुनिक शोध • व्यास अस्त्र वैदिक शोध संस्थान"
    new_note = "वेध आधार: महर्षि पराशर, महर्षि जैमिनी, भृगु नन्दी नाड़ी, के.एस. कृष्णमूर्ति (KP), ज्योतिषाचार्य बृजेश गौतम 'धागा-तंत्र' व लाल किताब • व्यास अस्त्र वैदिक शोध संस्थान"
    new_text = new_text.replace(old_note, new_note)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_text)

    print(f"Patched {filepath} successfully.")
    return True

patch_file('js/vyas_daivagya_engine.js')
patch_file('android_app/app/src/main/assets/js/vyas_daivagya_engine.js')
