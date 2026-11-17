# -*- coding: utf-8 -*-
for path in ['mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    target = "sendQuickQuery('धन एवं आकस्मिक लाभ हेतु कौन से ग्रह अनुकूल हैं?')"
    idx = c.find(target)
    if idx != -1:
        end_btn = c.find('</button>', idx) + 9
        insert_btn = '\n                    <button onclick="VyasMobile.sendQuickQuery(\'मेरी कुण्डली के अनुसार मेरी अवचेतन आदतें, मनोवैज्ञानिक कमियां और उन्हें सुधारने के व्यावहारिक उपाय क्या हैं?\')">🧠 सूक्ष्म आदतें व मनोवैज्ञानिक सुधार</button>'
        if 'सूक्ष्म आदतें व मनोवैज्ञानिक सुधार' not in c:
            c = c[:end_btn] + insert_btn + c[end_btn:]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            print("✓ Added psychology button in:", path)
