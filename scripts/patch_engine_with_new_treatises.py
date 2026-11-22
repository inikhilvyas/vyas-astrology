import os, re

def patch_engine(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Locate Sub-card D
    marker_d = "// Sub-card D: 🔱 दशमहाविद्या, द्वादश ज्योतिर्लिंग एवं लाल किताब कवच"
    idx_d = text.find(marker_d)
    if idx_d == -1:
        print(f"Marker D not found in {filepath}")
        return False

    # Find the end of Sub-card D: `h += '</ul></div>';`
    target = "h += '</ul></div>';"
    idx_target = text.find(target, idx_d)
    if idx_target == -1:
        print(f"End of Sub-card D not found in {filepath}")
        return False

    cut_point = idx_target + len(target)

    # Prepare Sub-card E and Sub-card F
    injection = """

                // Sub-card E: 📜 नाड़ी भाव-समन्वय एवं भृगु सरल पद्धति (BSP/BCP) सूत्र
                var nadiBhriguText = '';
                if (/शासन|करियर|आजीविका|पद/i.test(queryDomain)) {
                    nadiBhriguText = '<b>नाड़ी निर्देशांक व BSP:</b> नौकरी हेतु २, ६, १०, ११ (शनि कारक) एवं स्वतंत्र व्यापार हेतु २, ७, १०, ११ (बुध कारक)। शनि से ४था भाव कर्म परिवर्तन तथा मंगल २७वें वर्ष में १०वें भाव को सक्रिय करता है।';
                } else if (/विवाह|दांपत्य|सम्बन्ध/i.test(queryDomain)) {
                    nadiBhriguText = '<b>नाड़ी निर्देशांक व BSP:</b> वैवाहिक संरेखण हेतु २, ७, ११ (पुष्टि) एवं १, ६, १० (उदासीनता)। शुक्र से १२वें भाव की पीड़ा शांति तथा पीड़ित भाव से ७वें भाव के कारकत्व से सम्मुख अर्गला शमन।';
                } else if (/धन|समृद्धि|कोष/i.test(queryDomain)) {
                    nadiBhriguText = '<b>नाड़ी निर्देशांक व BCP:</b> कोष संचय हेतु २, ११ भाव। भृगु चक्र (BCP) अनुसार चालू आयु से १२ का गुणज घटाकर सक्रिय भाव का आकलन करें; पीड़ित भाव से ७वां भाव ही उसका सच्चा ऊर्जा स्रोत है।';
                } else if (/आरोग्य|स्वास्थ्य|रोग/i.test(queryDomain)) {
                    nadiBhriguText = '<b>नाड़ी निर्देशांक व कर्म-विपाक:</b> साध्य रोग १, ६ भाव; दीर्घकालीन कष्ट १, ६, ८, १२ (शनि/राहु)। नवांश (D9) चंद्रमा अनुसार कर्म विपाक शांति व ६ठे भाव के टॉक्सिन शमन हेतु एंटीऑक्सीडेंट आहार।';
                } else if (/विदेश|यात्रा|व्यय/i.test(queryDomain)) {
                    nadiBhriguText = '<b>नाड़ी निर्देशांक व BSP:</b> विदेश व यात्रा हेतु ३, ९, १२ भाव सक्रियण। केतु २४वें वर्ष में १२वें भाव को तथा राहु ३८वें वर्ष में ६ठे भाव को सक्रिय करता है।';
                } else {
                    nadiBhriguText = '<b>नाड़ी व भृगु सरल सिद्धांत:</b> किसी भी भाव की बाधा उसके सम्मुख ७वें भाव से आती है; अतः सम्मुख भाव के अनुकूल सात्विक कर्म द्वारा मुख्य भाव स्वतः जाग्रत हो जाता है।';
                }

                h += '<div style=\"background:rgba(15,23,42,0.7); border:1px solid rgba(56,189,248,0.3); border-radius:8px; padding:12px 14px;\">';
                h += '<div style=\"display:flex; align-items:center; gap:6px; margin-bottom:8px;\">';
                h += '<span style=\"color:#38bdf8; font-size:1rem;\">📜</span>';
                h += '<b style=\"color:#38bdf8; font-size:0.88rem;\">नाड़ी भाव-समन्वय एवं भृगु सरल पद्धति (BSP/BCP)</b>';
                h += '</div>';
                h += '<div style=\"font-size:0.75rem; color:#94a3b8; margin-bottom:8px;\">कस्पल हिट थ्योरी, निश्चित वर्ष सक्रियण एवं अर्गला विज्ञान:</div>';
                h += '<ul style=\"margin:0; padding-left:16px; font-size:0.84rem; line-height:1.65; color:var(--text-secondary);\">';
                h += '<li style=\"margin-bottom:6px;\">' + nadiBhriguText + '</li>';
                h += '<li style=\"margin-bottom:6px;\"><b>भृगु चक्र (BCP) नियम:</b> चालू आयु में से १२ का गुणज घटाकर वर्तमान सक्रिय भाव का फल देखें; चर राशि सक्रिय होने पर प्रत्यक्ष सेवा कर्म फलित होता है।</li>';
                h += '</ul></div>';

                // Sub-card F: 🏛️ एस्ट्रो-वास्तु एवं लाल किताब सोए भाव जागृति
                var sleepingHouseText = 'यदि १०वां भाव खाली हो तो २रा सोया रहता है, और २रा खाली हो तो ९वां व १०वां सोया रहता है। १०वें भाव को जगाने हेतु सरकारी भवन के कोने में सौंफ रखें; २रे/४थे भाव हेतु ४३ दिन चावल व तांबा सिक्का धर्मस्थान में अर्पित करें।';
                var astroVastuText = 'उत्तर-पश्चिम (शुक्र दिशा) में गुलाब/सुगंध स्थापित करें; घर में टूटा शीशा या नल से पानी टपकना (लीकेज) तुरंत बंद करें; पश्चिम दिशा से तीखी धूप आने पर पर्दे लगाएं।';

                h += '<div style=\"background:rgba(15,23,42,0.7); border:1px solid rgba(244,114,182,0.3); border-radius:8px; padding:12px 14px;\">';
                h += '<div style=\"display:flex; align-items:center; gap:6px; margin-bottom:8px;\">';
                h += '<span style=\"color:#f472b6; font-size:1rem;\">🏛️</span>';
                h += '<b style=\"color:#f472b6; font-size:0.88rem;\">एस्ट्रो-वास्तु, नक्षत्र पूजा एवं सोए भाव जागृति</b>';
                h += '</div>';
                h += '<div style=\"font-size:0.75rem; color:#94a3b8; margin-bottom:8px;\">४३-दिवसीय ऊर्जा संतुलन, वास्तु पूर्व-लक्षण एवं नक्षत्र संरेखण:</div>';
                h += '<ul style=\"margin:0; padding-left:16px; font-size:0.84rem; line-height:1.65; color:var(--text-secondary);\">';
                h += '<li style=\"margin-bottom:6px;\"><b>सोए भाव जागृति:</b> ' + sleepingHouseText + '</li>';
                h += '<li style=\"margin-bottom:6px;\"><b>एस्ट्रो-वास्तु व २७ नक्षत्र:</b> ' + astroVastuText + ' (हस्त नक्षत्र में दान १५ दिन में फल देता है; रेवती में क्षमा-प्रार्थना)।</li>';
                h += '</ul></div>';
"""

    new_text = text[:cut_point] + injection + text[cut_point:]

    # Update footer note
    old_note = "वेध आधार: महर्षि पराशर, महर्षि जैमिनी, भृगु नन्दी नाड़ी, के.एस. कृष्णमूर्ति (KP), प्रायोगिक धागा-तंत्र व लाल किताब • व्यास अस्त्र वैदिक शोध संस्थान"
    new_note = "वेध आधार: महर्षि पराशर, महर्षि जैमिनी, भृगु नन्दी नाड़ी, कृष्णमूर्ति पद्धति (KP कस्पल हिट), भृगु सरल पद्धति (BSP/BCP), लाल किताब अमृत एवं प्रायोगिक धागा-तंत्र • व्यास अस्त्र वैदिक शोध संस्थान"
    new_text = new_text.replace(old_note, new_note)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_text)

    print(f"Patched {filepath} successfully with Sub-card E & F.")
    return True

patch_engine('js/vyas_daivagya_engine.js')
patch_engine('android_app/app/src/main/assets/js/vyas_daivagya_engine.js')

