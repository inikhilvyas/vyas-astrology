# -*- coding: utf-8 -*-
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add tab button to horizontal tab layout bar
# Find where kp button is
kp_btn = '''<button class="tab-btn" data-tab="kp" onclick="VyasMobile.switchTab('kp')">
                <span>केपी कृष्णमूर्ति पद्धति</span>
            </button>'''

bb_btn = '''<button class="tab-btn" data-tab="kp" onclick="VyasMobile.switchTab('kp')">
                <span>केपी कृष्णमूर्ति पद्धति</span>
            </button>
            <button class="tab-btn" data-tab="bhavatbhavam" onclick="VyasMobile.switchTab('bhavatbhavam')">
                <span>भावात् भावम् (144 संयोजन)</span>
            </button>'''

if kp_btn in html and 'data-tab="bhavatbhavam"' not in html:
    html = html.replace(kp_btn, bb_btn, 1)
    print("Added bhavatbhavam tab button to mobile/index.html")
else:
    print("Tab button check:", 'data-tab="bhavatbhavam"' in html)

# 2. Add view-bhavatbhavam section before view-jaimini
target_sec = '<!-- TAB 10: JAIMINI CHARA KARAKAS -->\n            <section class="tab-view-container" id="view-jaimini">'
bb_section = '''<!-- TAB 9.5: BHAVAT BHAVAM (12x12 = 144 COMBINATIONS) & SHODH GRANTH -->
            <section class="tab-view-container" id="view-bhavatbhavam">
                <div style="margin-top:12px; padding:14px; background:rgba(10,17,34,0.7); border:1px solid rgba(212,175,55,0.4); border-left:4px solid #d4af37; border-radius:8px;">
                    <b style="color:var(--accent-gold); font-size:0.92rem; display:block; margin-bottom:4px;">✦ भावात् भावम् (144 संयोजन) महा-सिंथेसिस इंजन</b>
                    <div style="font-size:0.75rem; color:var(--text-secondary); line-height:1.5; margin-bottom:10px;">
                        शास्त्रीय सूत्र: <code style="color:#38bdf8; font-weight:700;">Z = ((Y - 1 + X - 1) mod 12) + 1</code> • निखिल व्यास महा-शोधग्रंथ
                    </div>

                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:10px;">
                        <div>
                            <label style="font-size:0.72rem; color:var(--accent-gold); display:block; margin-bottom:4px; font-weight:700;">आधार भाव (Y):</label>
                            <select id="m_bbBaseY" class="m-select" style="width:100%; font-size:0.78rem; padding:6px 8px; background:#0f172a; color:#fff; border:1px solid rgba(212,175,55,0.3); border-radius:6px;" onchange="VyasMobile.evalBhavatBhavamUI()">
                                <option value="1">1st • तनु (शरीर)</option>
                                <option value="2">2nd • धन (संपत्ति)</option>
                                <option value="3">3rd • सहज (पराक्रम)</option>
                                <option value="4">4th • सुख (माता/गृह)</option>
                                <option value="5">5th • पुत्र (बुद्धि/संतान)</option>
                                <option value="6">6th • रिपु (रोग/ऋण)</option>
                                <option value="7">7th • जाया (दांपत्य)</option>
                                <option value="8">8th • रंध्र (आयु/संकट)</option>
                                <option value="9">9th • धर्म (भाग्य/गुरु)</option>
                                <option value="10" selected>10th • कर्म (आजीविका)</option>
                                <option value="11">11th • लाभ (आय/सिद्धि)</option>
                                <option value="12">12th • व्यय (मोक्ष/व्यय)</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size:0.72rem; color:var(--accent-gold); display:block; margin-bottom:4px; font-weight:700;">सापेक्ष भाव (X):</label>
                            <select id="m_bbRelX" class="m-select" style="width:100%; font-size:0.78rem; padding:6px 8px; background:#0f172a; color:#fff; border:1px solid rgba(212,175,55,0.3); border-radius:6px;" onchange="VyasMobile.evalBhavatBhavamUI()">
                                <option value="1">1st • का 1st</option>
                                <option value="2" selected>2nd • का 2nd (धन)</option>
                                <option value="3">3rd • का 3rd (पराक्रम)</option>
                                <option value="4">4th • का 4th (सुख)</option>
                                <option value="5">5th • का 5th (बुद्धि)</option>
                                <option value="6">6th • का 6th (बाधा)</option>
                                <option value="7">7th • का 7th (विपरीत)</option>
                                <option value="8">8th • का 8th (आयु)</option>
                                <option value="9">9th • का 9th (भाग्य)</option>
                                <option value="10">10th • का 10th (कर्म)</option>
                                <option value="11">11th • का 11th (लाभ)</option>
                                <option value="12">12th • का 12th (व्यय)</option>
                            </select>
                        </div>
                    </div>

                    <!-- Synthesis Output Box -->
                    <div id="m_bbResultCard" style="background:rgba(15,23,42,0.8); border:1px solid rgba(212,175,55,0.3); border-radius:8px; padding:10px 12px; margin-top:8px;">
                        <span style="font-size:0.75rem; color:var(--text-muted);">कुण्डली लोड होने पर भावात् भावम् सिंथेसिस यहाँ प्रकट होगा...</span>
                    </div>
                </div>

                <div class="m-card" style="margin-top:12px;">
                    <div class="m-card-title">
                        <span>✦ 12 प्रमुख "X का X भाव" शास्त्रीय संक्षेप सारणी</span>
                    </div>
                    <div class="m-table-wrap">
                        <table class="m-table" style="font-size:0.75rem;">
                            <thead>
                                <tr>
                                    <th>संयोजन</th>
                                    <th>परिणामी भाव (Z)</th>
                                    <th>शास्त्रीय नाम व फल</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td><b>2 का 2</b></td><td><b>3रा (सहज)</b></td><td>धन का संचय पराक्रम व छोटे भाई/बहनों के सहयोग से।</td></tr>
                                <tr><td><b>3 का 3</b></td><td><b>5वां (पुत्र)</b></td><td>बुद्धि, रचनात्मकता व गूढ़ चिंतन शक्ति।</td></tr>
                                <tr><td><b>4 का 4</b></td><td><b>7वां (जाया)</b></td><td>गृहस्थ सुख, वाहन लाभ व जीवनसाथी का सुख।</td></tr>
                                <tr><td><b>5 का 5</b></td><td><b>9वां (धर्म)</b></td><td>परम भाग्य, उच्च विद्या, तीर्थ व पूर्वपुण्य।</td></tr>
                                <tr><td><b>6 का 6</b></td><td><b>11वां (लाभ)</b></td><td>प्रतिस्पर्धा, ऋण-मुक्ति व मुकदमों में भारी विजय।</td></tr>
                                <tr><td><b>7 का 7</b></td><td><b>1ला (लग्न)</b></td><td>जातक का स्वयं का अस्तित्व, साझेदारी का केंद्र।</td></tr>
                                <tr><td><b>8 का 8</b></td><td><b>3रा (सहज)</b></td><td>दीर्घायु, गोपनीय अन्वेषण व कठिन समय में साहस।</td></tr>
                                <tr><td><b>9 का 9</b></td><td><b>5वां (पुत्र)</b></td><td>धार्मिक प्रज्ञा, मंत्र सिद्धि व गुरु कृपा।</td></tr>
                                <tr><td><b>10 का 10</b></td><td><b>7वां (जाया)</b></td><td>व्यापार, सार्वजनिक सम्मान व स्वतंत्र करियर।</td></tr>
                                <tr><td><b>11 का 11</b></td><td><b>9वां (धर्म)</b></td><td>अकूत आर्थिक विस्तार व धर्म-कार्यों से धन लाभ।</td></tr>
                                <tr><td><b>12 का 12</b></td><td><b>11वां (लाभ)</b></td><td>त्याग व दान से आत्म-तुष्टि, विदेशी स्रोतों से लाभ।</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- TAB 10: JAIMINI CHARA KARAKAS -->
            <section class="tab-view-container" id="view-jaimini">'''

if target_sec in html and 'id="view-bhavatbhavam"' not in html:
    html = html.replace(target_sec, bb_section, 1)
    print("Injected view-bhavatbhavam section into mobile/index.html")
else:
    print("Section injection check:", 'id="view-bhavatbhavam"' in html)

# 3. Ensure switchTab hooks bhavatbhavam
switch_target = "else if (tabKey === 'lalkitab') {\n                        this.renderLalKitab();\n                    }"
switch_repl = """else if (tabKey === 'lalkitab') {
                        this.renderLalKitab();
                    } else if (tabKey === 'bhavatbhavam') {
                        this.evalBhavatBhavamUI();
                    }"""

if switch_target in html and "tabKey === 'bhavatbhavam'" not in html:
    html = html.replace(switch_target, switch_repl, 1)
    print("Hooked bhavatbhavam into switchTab in mobile/index.html")
else:
    print("switchTab hook check:", "tabKey === 'bhavatbhavam'" in html)

# 4. Add scripts before </body>
script_target = '<script src="../js/vyas_kp_horary_solver.js"></script>'
script_repl = '''<script src="../js/vyas_bhavat_bhavam.js"></script>
    <script src="../js/vyas_treatise_sutras.js"></script>
    <script src="../js/vyas_kp_horary_solver.js"></script>'''

if script_target in html and 'vyas_bhavat_bhavam.js' not in html:
    html = html.replace(script_target, script_repl, 1)
    print("Added scripts to mobile/index.html")
else:
    print("Script tags check:", 'vyas_bhavat_bhavam.js' in html)

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("mobile/index.html update complete!")
