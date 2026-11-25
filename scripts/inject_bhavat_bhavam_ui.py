# -*- coding: utf-8 -*-
"""
scripts/inject_bhavat_bhavam_ui.py
Inject Bhavat Bhavam (144 Combinations) into index.html and mobile/index.html
"""

import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add tab button
tab_btn_target = '<button class="tab-nav-btn" onclick="VyasDesktop.switchTab(\'jaimini\', this)">जैमिनी ज्योतिष\n                    (Jaimini)</button>'
tab_btn_repl = '''<button class="tab-nav-btn" onclick="VyasDesktop.switchTab('jaimini', this)">जैमिनी ज्योतिष
                    (Jaimini)</button>
                <button class="tab-nav-btn" onclick="VyasDesktop.switchTab('bhavatbhavam', this)">भावात् भावम्
                    (144 संयोजन)</button>'''

if tab_btn_target in html and 'switchTab(\'bhavatbhavam\'' not in html:
    html = html.replace(tab_btn_target, tab_btn_repl, 1)
    print("Tab button added to index.html")
else:
    print("Tab button already present or target not found in index.html")

# 2. Add pillar item in pillars.systems
pillar_target = "{ key: 'kp', label: 'केपी पद्धति (1-249)', sub: 'KP Sub-Lord Horary' },"
pillar_repl = '''{ key: 'kp', label: 'केपी पद्धति (1-249)', sub: 'KP Sub-Lord Horary' },
                        { key: 'bhavatbhavam', label: 'भावात् भावम् (144 संयोजन)', sub: '12x12 Matrix & Shodh Granth' },'''

if pillar_target in html and "'bhavatbhavam'" not in html:
    html = html.replace(pillar_target, pillar_repl, 1)
    print("Pillar tab added to index.html")

# 3. Add view panel before view-jaimini
panel_target = '<!-- 8. TAB: JAIMINI ASTROLOGY -->\n                <div class="view-panel" id="view-jaimini">'

panel_html = '''<!-- 7.5 TAB: BHAVAT BHAVAM (12x12 = 144 COMBINATIONS) & SHODH GRANTH -->
                <div class="view-panel" id="view-bhavatbhavam">
                    <!-- Bhavat Bhavam Interactive Synthesizer Card -->
                    <div class="content-card" style="border:1px solid rgba(212,175,55,0.4); border-left:4px solid #d4af37; background:var(--bg-card); border-radius:10px; padding:18px; margin-bottom:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
                            <div>
                                <b style="color:#d4af37; font-size:1.02rem;">✦ भावात् भावम् (12×12 = 144 संयोजन) महा-सिंथेसिस इंजन</b>
                                <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:2px;">
                                    शास्त्रीय सूत्र: <code style="color:#38bdf8; background:rgba(56,189,248,0.1); padding:2px 6px; border-radius:4px; font-weight:700;">Z = ((Y - 1 + X - 1) mod 12) + 1</code> • 6-स्तरीय सूक्ष्म परीक्षण
                                </div>
                            </div>
                            <span style="font-size:0.72rem; background:rgba(212,175,55,0.15); color:#d4af37; padding:4px 10px; border-radius:12px; font-weight:800;">
                                BPHS • जैमिनी • केपी कस्पल सब-लॉर्ड
                            </span>
                        </div>
                        <p style="font-size:0.78rem; color:var(--text-secondary); margin-bottom:14px; line-height:1.6;">
                            भावात् भावम् सिद्धांत के अनुसार, किसी भाव का यथार्थ कार्य-फल उस भाव से सापेक्ष भाव की स्थिति से निर्धारित होता है। नीचे दिए गए किसी भी आधार भाव (Y) तथा उससे गिने जाने वाले सापेक्ष भाव (X) का चयन करें, प्रणाली तात्कालिक कुण्डली के अनुसार परिणामी भाव (Z), उसकी राशि, भावेश, ऑथेंटिक प्लेसिडस भोगांश, CSL तथा शास्त्रीय फलादेश प्रकट करेगी:
                        </p>
                        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; margin-bottom:16px; background:rgba(15,23,42,0.5); padding:12px; border-radius:8px; border:1px solid var(--border-subtle);">
                            <div>
                                <label style="font-size:0.75rem; font-weight:700; color:#d4af37; display:block; margin-bottom:4px;">आधार भाव (Base Bhava Y):</label>
                                <select id="bbBaseYSelect" class="form-input" style="width:100%; font-size:0.80rem;" onchange="VyasDesktop.evalBhavatBhavamUI()">
                                    <option value="1">1st (तनु) • शरीर, आत्मबल व व्यक्तित्व</option>
                                    <option value="2">2nd (धन) • संचित संपत्ति, वाणी व कुटुंब</option>
                                    <option value="3">3rd (सहज) • पराक्रम, साहस व भाई-बहन</option>
                                    <option value="4">4th (सुख) • माता, भूमि, भवन, वाहन व शांति</option>
                                    <option value="5">5th (पुत्र) • बुद्धि, संतान, पूर्वपुण्य व विद्या</option>
                                    <option value="6">6th (रिपु) • रोग, ऋण, शत्रु व प्रतिस्पर्धा</option>
                                    <option value="7">7th (जाया) • जीवनसाथी, साझेदारी व लोक संपर्क</option>
                                    <option value="8">8th (रंध्र) • आयु, गूढ़ विद्या, आकस्मिक धन व शोध</option>
                                    <option value="9">9th (धर्म) • भाग्य, धर्म, उच्च शिक्षा व पिता</option>
                                    <option value="10">10th (कर्म) • आजीविका, पद, प्रतिष्ठा व राज्य सम्मान</option>
                                    <option value="11">11th (आय) • आय, मित्र, ज्येष्ठ भ्राता व सर्वकार्य सिद्धि</option>
                                    <option value="12">12th (व्यय) • विदेश यात्रा, मोक्ष, अध्यात्म व व्यय</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size:0.75rem; font-weight:700; color:#38bdf8; display:block; margin-bottom:4px;">सापेक्ष भाव (Relative Bhava X):</label>
                                <select id="bbRelativeXSelect" class="form-input" style="width:100%; font-size:0.80rem;" onchange="VyasDesktop.evalBhavatBhavamUI()">
                                    <option value="1">1 से 1 (मूल भाव प्रभाव)</option>
                                    <option value="2">का 2रा भाव (धन/पोषण/कुटुंब)</option>
                                    <option value="3">का 3रा भाव (पराक्रम/प्रयास/संचार)</option>
                                    <option value="4">का 4था भाव (सुख/वाहन/स्थिरता)</option>
                                    <option value="5">का 5वाँ भाव (सृजन/बुद्धि/मंत्र)</option>
                                    <option value="6">का 6ठा भाव (रोग/ऋण/शत्रु/सेवा)</option>
                                    <option value="7">का 7वाँ भाव (साझेदारी/लोक/विस्तार)</option>
                                    <option value="8">का 8वाँ भाव (आयु/संकट/आकस्मिकता)</option>
                                    <option value="9">का 9वाँ भाव (भाग्य/धर्म/गुरु कृपा)</option>
                                    <option value="10" selected>का 10वाँ भाव (कर्म/आजीविका/सत्ता)</option>
                                    <option value="11">का 11वाँ भाव (लाभ/इच्छापूर्ति/मित्र)</option>
                                    <option value="12">का 12वाँ भाव (व्यय/मोक्ष/विदेश)</option>
                                </select>
                            </div>
                            <div style="display:flex; align-items:flex-end;">
                                <button type="button" class="header-btn primary" onclick="VyasDesktop.evalBhavatBhavamUI()" style="width:100%; padding:9px; font-weight:800; font-size:0.80rem; background:var(--gold-gradient); color:#111; border:none; border-radius:6px; cursor:pointer;">
                                    ✦ संश्लेषण करें (Synthesize)
                                </button>
                            </div>
                        </div>

                        <!-- Result Display Box -->
                        <div id="bbResultCard" style="background:rgba(212,175,55,0.06); border:1px solid rgba(212,175,55,0.3); border-radius:8px; padding:14px;">
                            <!-- Populated dynamically by VyasDesktop.evalBhavatBhavamUI() -->
                        </div>
                    </div>

                    <!-- 12 X from X Master Table -->
                    <div class="content-card" style="margin-bottom:16px;">
                        <div class="card-heading">
                            <span>✦ 12 मूल भावात् भावम् ("X से X" महा-तालिका)</span>
                            <span style="font-size:0.72rem; color:var(--primary-navy); font-weight:700;">प्रामाणिक शास्त्रीय नियम</span>
                        </div>
                        <div class="table-wrap">
                            <table class="astronomy-table">
                                <thead>
                                    <tr>
                                        <th>संयोजन</th>
                                        <th>परिणामी भाव (Z)</th>
                                        <th>शास्त्रीय सिद्ध-सूत्र</th>
                                        <th>गूढ़ फलादेश व जीवन प्रभाव</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr><td><b>1 से 1</b></td><td><span style="color:#10b981; font-weight:800;">1st (तनु)</span></td><td>स्वयं का मूल अस्तित्व, प्राण-शक्ति व आत्मा</td><td>लग्न ही सम्पूर्ण कुण्डली का आधार है। तनु से तनु भाव स्वयं के अस्तित्व, आत्मबल और शारीरिक आरोग्यता का निर्धारण करता है।</td></tr>
                                    <tr><td><b>2 से 2</b></td><td><span style="color:#10b981; font-weight:800;">3rd (सहज)</span></td><td>धन का पोषण, पुरुषार्थ, संचित प्रयास व संवाद</td><td>द्वितीय (धन) से द्वितीय भाव तृतीय (सहज) है। यह दर्शाता है कि धन की वृद्धि जातक के निरंतर पराक्रम, लेखनी और व्यावसायिक संवाद से ही संभव है।</td></tr>
                                    <tr><td><b>3 से 3</b></td><td><span style="color:#10b981; font-weight:800;">5th (पुत्र)</span></td><td>पराक्रम का सृजन, कौशल, विवेक व प्रतिभा</td><td>तृतीय (पराक्रम) से तृतीय भाव पंचम (बुद्धि) है। अदम्य साहस केवल शारीरिक नहीं बल्कि जब विवेक और पूर्वपुण्य से युक्त होता है, तभी पराक्रम सिद्धि देता है।</td></tr>
                                    <tr><td><b>4 से 4</b></td><td><span style="color:#10b981; font-weight:800;">7th (जाया)</span></td><td>गृहस्थ सुख का विस्तार व लोक-साझेदारी</td><td>चतुर्थ (सुख) से चतुर्थ भाव सप्तम (जाया) है। घर की आंतरिक शांति का बाह्य विस्तार जीवनसाथी और लोक-व्यवहार की सामंजस्यता से होता है।</td></tr>
                                    <tr><td><b>5 से 5</b></td><td><span style="color:#10b981; font-weight:800;">9th (धर्म)</span></td><td>बुद्धि व पूर्वपुण्य से भाग्योदय, धर्म व ईश्वरीय कृपा</td><td>पंचम (संतान/ज्ञान) से पंचम भाव नवम (धर्म) है। जातक की बुद्धि और साधना जब धर्म से जुड़ती है, तभी चिरस्थायी भाग्योदय घटित होता है।</td></tr>
                                    <tr><td><b>6 से 6</b></td><td><span style="color:#10b981; font-weight:800;">11th (आय)</span></td><td>रोग, शत्रु व ऋण पर विजय और प्रचुर लाभ</td><td>षष्ठ (शत्रु/प्रतिस्पर्धा) से षष्ठ भाव एकादश (लाभ) है। कठिन संघर्षों, कर्जों और कानूनी वादों पर विजय प्राप्त कर जातक विपुल लाभ अर्जित करता है।</td></tr>
                                    <tr><td><b>7 से 7</b></td><td><span style="color:#10b981; font-weight:800;">1st (तनु)</span></td><td>जीवनसाथी का प्रभाव व स्वयं का यथार्थ प्रतिबिंब</td><td>सप्तम (साझेदार) से सप्तम भाव पुनः लग्न (1ला भाव) है। जीवनसाथी वस्तुतः जातक के अपने ही अंतर्मन और प्रारब्ध का भौतिक दर्पण होता है।</td></tr>
                                    <tr><td><b>8 से 8</b></td><td><span style="color:#10b981; font-weight:800;">3rd (सहज)</span></td><td>आयु-शक्ति, गूढ़ संकट में अदम्य धैर्य व साहस</td><td>अष्टम (आयु/संकट) से अष्टम भाव तृतीय (पराक्रम) है। जीवन-मरण के संकट और गंभीर विपत्तियों से उबरने की शक्ति जातक के 3रे भाव के जीवट से आती है।</td></tr>
                                    <tr><td><b>9 से 9</b></td><td><span style="color:#10b981; font-weight:800;">5th (पुत्र)</span></td><td>धर्म, साधना व गुरु कृपा से मंत्र-सिद्धि व संतान</td><td>नवम (भाग्य/गुरु) से नवम भाव पंचम (मंत्र/संतान) है। गुरु के आशीर्वाद और धर्म-पालन से इष्ट-कृपा व तीव्र मंत्र-सिद्धि फलित होती है।</td></tr>
                                    <tr><td><b>10 से 10</b></td><td><span style="color:#10b981; font-weight:800;">7th (जाया)</span></td><td>कर्म का लोक-विस्तार, व्यापारिक सत्ता व सामाजिक मान</td><td>दशम (कर्म/प्रतिष्ठा) से दशम भाव सप्तम (लोक-व्यवहार) है। कार्यक्षेत्र की सर्वोच्च सफलता जनता से संपर्क और बड़े व्यापारिक गठबंधनों से स्थापित होती है।</td></tr>
                                    <tr><td><b>11 से 11</b></td><td><span style="color:#10b981; font-weight:800;">9th (धर्म)</span></td><td>लाभ की निरंतरता, अक्षय समृद्धि व धर्म-परायणता</td><td>एकादश (आय) से एकादश भाव नवम (धर्म) है। संचित लाभ तभी स्थायी और पुण्यदायी बनता है जब वह धर्म, परोपकार और नीति-सम्मत मार्ग से अर्जित हो।</td></tr>
                                    <tr><td><b>12 से 12</b></td><td><span style="color:#10b981; font-weight:800;">11th (आय)</span></td><td>व्यय, त्याग व विदेशी निवेश से भौतिक-आध्यात्मिक लाभ</td><td>द्वादश (मोक्ष/व्यय) से द्वादश भाव एकादश (लाभ) है। विवेकपूर्ण त्याग, धर्मार्थ दान और सुदूर निवेश अंततः जातक को मान और आत्म-संतोष रूपी लाभ देता है।</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- 3x3 Magic Square Yantras (15 to 39) & 12 Kamna Yantras -->
                    <div class="content-card" style="margin-bottom:16px;">
                        <div class="card-heading">
                            <span>✦ संपूर्ण तांत्रिक व नवग्रह 3×3 अंकीय यंत्र (योग 15 से 39) एवं 12 कामना-यंत्र</span>
                            <span style="font-size:0.72rem; color:var(--accent-gold); font-weight:700;">मेरु तंत्र • भोजपत्र विधान</span>
                        </div>
                        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:14px; margin-top:12px;">
                            <!-- Surya Yantra (15) -->
                            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(245,158,11,0.3); border-radius:8px; padding:12px; text-align:center;">
                                <b style="color:#f59e0b; font-size:0.86rem;">1. सूर्य यंत्र (योग = 15) • पूर्व दिशा</b>
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; max-width:180px; margin:8px auto; background:rgba(245,158,11,0.1); padding:6px; border-radius:6px; font-weight:800; color:#fbbf24; font-family:var(--font-mono);">
                                    <div>6</div><div>1</div><div>8</div>
                                    <div>7</div><div>5</div><div>3</div>
                                    <div>2</div><div>9</div><div>4</div>
                                </div>
                                <span style="font-size:0.72rem; color:var(--text-secondary);">तांबा/स्वर्ण • मातंगी/श्रीराम • जप: 7,000</span>
                            </div>

                            <!-- Chandra Yantra (18) -->
                            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(56,189,248,0.3); border-radius:8px; padding:12px; text-align:center;">
                                <b style="color:#38bdf8; font-size:0.86rem;">2. चंद्र यंत्र (योग = 18) • वायव्य दिशा</b>
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; max-width:180px; margin:8px auto; background:rgba(56,189,248,0.1); padding:6px; border-radius:6px; font-weight:800; color:#7dd3fc; font-family:var(--font-mono);">
                                    <div>7</div><div>2</div><div>9</div>
                                    <div>8</div><div>6</div><div>4</div>
                                    <div>3</div><div>10</div><div>5</div>
                                </div>
                                <span style="font-size:0.72rem; color:var(--text-secondary);">चांदी • काली/श्रीकृष्ण • जप: 11,000</span>
                            </div>

                            <!-- Mangal Yantra (21) -->
                            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(239,68,68,0.3); border-radius:8px; padding:12px; text-align:center;">
                                <b style="color:#ef4444; font-size:0.86rem;">3. मंगल यंत्र (योग = 21) • दक्षिण दिशा</b>
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; max-width:180px; margin:8px auto; background:rgba(239,68,68,0.1); padding:6px; border-radius:6px; font-weight:800; color:#f87171; font-family:var(--font-mono);">
                                    <div>8</div><div>3</div><div>10</div>
                                    <div>9</div><div>7</div><div>5</div>
                                    <div>4</div><div>11</div><div>6</div>
                                </div>
                                <span style="font-size:0.72rem; color:var(--text-secondary);">तांबा • छिन्नमस्ता/नरसिंह • जप: 10,000</span>
                            </div>

                            <!-- Budha Yantra (24) -->
                            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(16,185,129,0.3); border-radius:8px; padding:12px; text-align:center;">
                                <b style="color:#10b981; font-size:0.86rem;">4. बुध यंत्र (योग = 24) • उत्तर दिशा</b>
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; max-width:180px; margin:8px auto; background:rgba(16,185,129,0.1); padding:6px; border-radius:6px; font-weight:800; color:#34d399; font-family:var(--font-mono);">
                                    <div>9</div><div>4</div><div>11</div>
                                    <div>10</div><div>8</div><div>6</div>
                                    <div>5</div><div>12</div><div>7</div>
                                </div>
                                <span style="font-size:0.72rem; color:var(--text-secondary);">कांसा/भोजपत्र • कमला/बुद्ध • जप: 9,000</span>
                            </div>

                            <!-- Guru Yantra (27) -->
                            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(234,179,8,0.3); border-radius:8px; padding:12px; text-align:center;">
                                <b style="color:#eab308; font-size:0.86rem;">5. गुरु यंत्र (योग = 27) • ईशान दिशा</b>
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; max-width:180px; margin:8px auto; background:rgba(234,179,8,0.1); padding:6px; border-radius:6px; font-weight:800; color:#fde047; font-family:var(--font-mono);">
                                    <div>10</div><div>5</div><div>12</div>
                                    <div>11</div><div>9</div><div>7</div>
                                    <div>6</div><div>13</div><div>8</div>
                                </div>
                                <span style="font-size:0.72rem; color:var(--text-secondary);">पीतल/स्वर्ण • भुवनेश्वरी/वामन • जप: 19,000</span>
                            </div>

                            <!-- Shukra Yantra (30) -->
                            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(236,72,153,0.3); border-radius:8px; padding:12px; text-align:center;">
                                <b style="color:#ec4899; font-size:0.86rem;">6. शुक्र यंत्र (योग = 30) • आग्नेय दिशा</b>
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; max-width:180px; margin:8px auto; background:rgba(236,72,153,0.1); padding:6px; border-radius:6px; font-weight:800; color:#f472b6; font-family:var(--font-mono);">
                                    <div>11</div><div>6</div><div>13</div>
                                    <div>12</div><div>10</div><div>8</div>
                                    <div>7</div><div>14</div><div>9</div>
                                </div>
                                <span style="font-size:0.72rem; color:var(--text-secondary);">चांदी/स्फटिक • षोडशी/परशुराम • जप: 16,000</span>
                            </div>

                            <!-- Shani Yantra (33) -->
                            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(148,163,184,0.3); border-radius:8px; padding:12px; text-align:center;">
                                <b style="color:#94a3b8; font-size:0.86rem;">7. शनि यंत्र (योग = 33) • पश्चिम दिशा</b>
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; max-width:180px; margin:8px auto; background:rgba(148,163,184,0.1); padding:6px; border-radius:6px; font-weight:800; color:#cbd5e1; font-family:var(--font-mono);">
                                    <div>12</div><div>7</div><div>14</div>
                                    <div>13</div><div>11</div><div>9</div>
                                    <div>8</div><div>15</div><div>10</div>
                                </div>
                                <span style="font-size:0.72rem; color:var(--text-secondary);">लोहा/अष्टधातु • बगलामुखी/कूर्म • जप: 23,000</span>
                            </div>

                            <!-- Rahu Yantra (36) -->
                            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(168,85,247,0.3); border-radius:8px; padding:12px; text-align:center;">
                                <b style="color:#a855f7; font-size:0.86rem;">8. राहु यंत्र (योग = 36) • नैऋत्य दिशा</b>
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; max-width:180px; margin:8px auto; background:rgba(168,85,247,0.1); padding:6px; border-radius:6px; font-weight:800; color:#c084fc; font-family:var(--font-mono);">
                                    <div>13</div><div>8</div><div>15</div>
                                    <div>14</div><div>12</div><div>10</div>
                                    <div>9</div><div>16</div><div>11</div>
                                </div>
                                <span style="font-size:0.72rem; color:var(--text-secondary);">सीसा/अष्टधातु • धूमावती/वराह • जप: 18,000</span>
                            </div>

                            <!-- Ketu Yantra (39) -->
                            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(249,115,22,0.3); border-radius:8px; padding:12px; text-align:center;">
                                <b style="color:#f97316; font-size:0.86rem;">9. केतु यंत्र (योग = 39) • ईशान/नैऋत्य</b>
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; max-width:180px; margin:8px auto; background:rgba(249,115,22,0.1); padding:6px; border-radius:6px; font-weight:800; color:#fb923c; font-family:var(--font-mono);">
                                    <div>14</div><div>9</div><div>16</div>
                                    <div>15</div><div>13</div><div>11</div>
                                    <div>10</div><div>17</div><div>12</div>
                                </div>
                                <span style="font-size:0.72rem; color:var(--text-secondary);">तांबा/अष्टधातु • तारा/मत्स्य • जप: 17,000</span>
                            </div>
                        </div>
                    </div>
                </div>

                '''

if panel_target in html and 'id="view-bhavatbhavam"' not in html:
    html = html.replace(panel_target, panel_html + panel_target, 1)
    print("view-bhavatbhavam panel added to index.html")

# 4. Add script tag at bottom
script_target = '<script src="js/vyas_kp_horary_solver.js"></script>'
script_repl = '''<script src="js/vyas_bhavat_bhavam.js"></script>
    <script src="js/vyas_kp_horary_solver.js"></script>'''

if script_target in html and 'vyas_bhavat_bhavam.js' not in html:
    html = html.replace(script_target, script_repl, 1)
    print("Script tag added to index.html")

# 5. Add VyasDesktop.evalBhavatBhavamUI method
eval_target = "            // ACHARYA VYAS AI SAGE CHAT"
eval_code = '''            // 7.5 BHAVAT BHAVAM (12x12 = 144 COMBINATIONS) SYNTHESIS
            evalBhavatBhavamUI: function() {
                var baseY = document.getElementById('bbBaseYSelect') ? document.getElementById('bbBaseYSelect').value : 2;
                var relX = document.getElementById('bbRelativeXSelect') ? document.getElementById('bbRelativeXSelect').value : 10;
                var resBox = document.getElementById('bbResultCard');
                if (!resBox) return;

                if (typeof window !== 'undefined' && window.VyasBhavatBhavam && typeof window.VyasBhavatBhavam.synthesizeBhavatBhavam === 'function') {
                    var syn = window.VyasBhavatBhavam.synthesizeBhavatBhavam(this.activeChartData, baseY, relX);
                    var html = '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:6px;">' +
                        '<b style="color:#d4af37; font-size:0.95rem;">🎯 परिणामी भाव: ' + syn.calc.resultName + '</b>' +
                        '<code style="color:#38bdf8; background:rgba(56,189,248,0.12); padding:2px 8px; border-radius:4px; font-weight:700;">' + syn.calc.formula + '</code>' +
                        '</div>' +
                        '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px; font-size:0.78rem;">' +
                        '<div style="background:rgba(15,23,42,0.4); padding:8px; border-radius:6px;"><b>राशि:</b> <span style="color:#10b981;">' + syn.zSign + '</span> • <b>भावेश:</b> ' + syn.zLord + '</div>' +
                        '<div style="background:rgba(15,23,42,0.4); padding:8px; border-radius:6px;"><b>KP कस्पल सब-लॉर्ड:</b> <span style="color:#f59e0b; font-weight:800;">' + syn.csl + '</span> (' + syn.cDeg + ')</div>' +
                        '<div style="background:rgba(15,23,42,0.4); padding:8px; border-radius:6px;"><b>भावेश संबंध:</b> ' + syn.relation + '</div>' +
                        '</div>' +
                        '<p style="font-size:0.77rem; line-height:1.6; color:var(--text-secondary); margin:0;">' + syn.synthesis + '</p>';
                    if (syn.isXfromX && syn.xFromXDetail) {
                        html += '<div style="margin-top:10px; padding:8px; background:rgba(212,175,55,0.12); border-left:3px solid #d4af37; border-radius:4px; font-size:0.76rem;">' +
                            '<b style="color:#d4af37;">✦ मूल "X से X" भावात् भावम् सूत्र (' + syn.xFromXDetail.title + '):</b> ' + syn.xFromXDetail.sutra + '<br>' +
                            '<span style="color:var(--text-secondary);">' + syn.xFromXDetail.desc + '</span>' +
                            '</div>';
                    }
                    resBox.innerHTML = html;
                } else {
                    resBox.innerHTML = '<p style="color:var(--text-secondary); font-size:0.78rem;">भावात् भावम् इंजन लोड हो रहा है...</p>';
                }
            },

'''

if eval_target in html and 'evalBhavatBhavamUI' not in html:
    html = html.replace(eval_target, eval_code + eval_target, 1)
    print("evalBhavatBhavamUI method added to index.html")

# 6. Wire evalBhavatBhavamUI to switchTab('bhavatbhavam')
switch_target = "if (tabKey === 'kp') this.renderKP();"
switch_repl = """if (tabKey === 'kp') this.renderKP();
                if (tabKey === 'bhavatbhavam') this.evalBhavatBhavamUI();"""

if switch_target in html and 'tabKey === \'bhavatbhavam\'' not in html:
    html = html.replace(switch_target, switch_repl, 1)
    print("switchTab hook added for bhavatbhavam in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html updated successfully!")
