import re

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Original length:", len(content))

# 1. Update logo path from /logo_icon.png to logo_icon.png
content = content.replace('src="/logo_icon.png"', 'src="logo_icon.png"')

# 2. Update Header Profile Strip to Blank Slate State
old_strip = """        <!-- ACTIVE PROFILE STRIP -->
        <div class="profile-strip">
            <div class="profile-strip-name" id="mStripProfileName">
                <span>👤 NIKHIL VYAS</span>
                <span class="badge-tag badge-exalted">मेष लग्न 23°27'</span>
            </div>
            <div class="profile-strip-meta" id="mStripProfileMeta">
                23 Nov 1984 • Pali, RJ
            </div>
        </div>"""

new_strip = """        <!-- ACTIVE PROFILE STRIP (BLANK SLATE BY DEFAULT) -->
        <div class="profile-strip" onclick="VyasMobile.openNewProfileModal()" style="cursor:pointer;">
            <div class="profile-strip-name" id="mStripProfileName">
                <span>✨ अपनी कुण्डली बनाएं (निःशुल्क)</span>
                <span class="badge-tag badge-exalted">वैदिक खगोल</span>
            </div>
            <div class="profile-strip-meta" id="mStripProfileMeta">
                सटीक 1-249 KP, जैमिनी, नाड़ी व 5-स्तरीय विंशोत्तरी फलादेश
            </div>
        </div>"""

if old_strip in content:
    content = content.replace(old_strip, new_strip)
    print("Replaced active profile strip successfully!")
else:
    print("Warning: old_strip not found verbatim, searching regex...")
    content = re.sub(
        r'<div class="profile-strip-name" id="mStripProfileName">[\s\S]*?</div>\s*<div class="profile-strip-meta" id="mStripProfileMeta">[\s\S]*?</div>',
        '<div class="profile-strip-name" id="mStripProfileName"><span>✨ अपनी कुण्डली बनाएं (निःशुल्क)</span><span class="badge-tag badge-exalted">वैदिक खगोल</span></div>\n            <div class="profile-strip-meta" id="mStripProfileMeta">सटीक 1-249 KP, जैमिनी, नाड़ी व 5-स्तरीय विंशोत्तरी फलादेश</div>',
        content
    )
    print("Profile strip regex updated!")

# 3. Update Cosmic Score Card / Daily Horoscope HTML to eliminate static 74% and Mars in 10th
old_cosmic_card_part = """                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <div>
                            <div style="font-size:1.8rem; font-weight:900; color:var(--primary); font-family:var(--font-serif);" id="mDayIndex">--</div>
                            <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;" id="mDaySub">कुण्डली आवश्यक</div>
                        </div>
                        <div style="text-align:right; font-size:0.75rem; color:var(--text-secondary); line-height:1.4;">
                            सक्रिय दशा: <b>शुक्र ➔ शनि ➔ मंगल</b><br>
                            शुभ मुहूर्त: <b>अभिजित 11:58 AM - 12:44 PM</b>
                        </div>
                    </div>

                    <!-- 4 Stambh Grid -->
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-bottom:10px;">
                        <div style="background:var(--bg-card-alt); padding:8px; border-radius:8px; border:1px solid var(--border-subtle);">
                            <b style="color:var(--primary); font-size:0.75rem;">धन व वाणी विचार</b>
                            <p style="font-size:0.70rem; color:var(--text-secondary); margin-top:2px;">आर्थिक लेन-देन में विवेक रखें। स्पष्ट व मधुर वाणी लाभ देगी।</p>
                        </div>
                        <div style="background:var(--bg-card-alt); padding:8px; border-radius:8px; border:1px solid var(--border-subtle);">
                            <b style="color:var(--primary); font-size:0.75rem;">कर्मक्षेत्र व आजीविका</b>
                            <p style="font-size:0.70rem; color:var(--text-secondary); margin-top:2px;">दशम में उच्च का मंगल अधिकारियों व अनुबंधों में गति प्रदान करेगा।</p>
                        </div>
                        <div style="background:var(--bg-card-alt); padding:8px; border-radius:8px; border:1px solid var(--border-subtle);">
                            <b style="color:var(--primary); font-size:0.75rem;">❤️ संबंध व परिवार</b>
                            <p style="font-size:0.70rem; color:var(--text-secondary); margin-top:2px;">पारिवारिक सामंजस्य रहेगा। जीवनसाथी के परामर्श का सम्मान करें।</p>
                        </div>
                        <div style="background:var(--bg-card-alt); padding:8px; border-radius:8px; border:1px solid var(--border-subtle);">
                            <b style="color:var(--primary); font-size:0.75rem;">🌿 स्वास्थ्य एवं ऊर्जा</b>
                            <p style="font-size:0.70rem; color:var(--text-secondary); margin-top:2px;">मानसिक स्फूर्ति 74%। हल्का सात्विक भोजन व पर्याप्त जल ग्रहण करें।</p>
                        </div>
                    </div>"""

new_cosmic_card_part = """                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <div>
                            <div style="font-size:1.8rem; font-weight:900; color:var(--primary); font-family:var(--font-serif);" id="mDayIndex">--</div>
                            <div style="font-size:0.80rem; color:var(--text-muted); font-weight:700;" id="mDaySub">कुण्डली आवश्यक</div>
                        </div>
                        <div style="text-align:right; font-size:0.82rem; color:var(--text-secondary); line-height:1.5;">
                            सक्रिय दशा: <b id="mActiveDashaHeader" style="color:var(--primary);">कुण्डली बनाएं</b><br>
                            शुभ मुहूर्त: <b>अभिजित 11:58 AM - 12:44 PM</b>
                        </div>
                    </div>

                    <!-- 4 Stambh Grid (Live Astronomical & Natal Synthesis) -->
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:10px;" id="mDaily4Pillars">
                        <div style="background:var(--bg-card-alt); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">
                            <b style="color:var(--primary); font-size:0.84rem;">धन व वाणी विचार</b>
                            <p id="mDailyDhana" style="font-size:0.80rem; color:var(--text-secondary); margin-top:4px; line-height:1.5;">आर्थिक लेन-देन में विवेक रखें। स्पष्ट व मधुर वाणी लाभ देगी।</p>
                        </div>
                        <div style="background:var(--bg-card-alt); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">
                            <b style="color:var(--primary); font-size:0.84rem;">कर्मक्षेत्र व आजीविका</b>
                            <p id="mDailyKarma" style="font-size:0.80rem; color:var(--text-secondary); margin-top:4px; line-height:1.5;">वर्तमान गोचर अनुसार कर्मक्षेत्र में अनुशासन व सात्विक निष्ठा से सफलता मिलेगी।</p>
                        </div>
                        <div style="background:var(--bg-card-alt); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">
                            <b style="color:var(--primary); font-size:0.84rem;">❤️ संबंध व परिवार</b>
                            <p id="mDailyFamily" style="font-size:0.80rem; color:var(--text-secondary); margin-top:4px; line-height:1.5;">पारिवारिक सामंजस्य रहेगा। जीवनसाथी व परिजनों के परामर्श का सम्मान करें।</p>
                        </div>
                        <div style="background:var(--bg-card-alt); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">
                            <b style="color:var(--primary); font-size:0.84rem;">🌿 स्वास्थ्य एवं ऊर्जा</b>
                            <p id="mDailyHealth" style="font-size:0.80rem; color:var(--text-secondary); margin-top:4px; line-height:1.5;">हल्का सात्विक भोजन, पर्याप्त जल ग्रहण करें तथा सूर्य उपासना से आत्मबल बढ़ाएं।</p>
                        </div>
                    </div>"""

if old_cosmic_card_part in content:
    content = content.replace(old_cosmic_card_part, new_cosmic_card_part)
    print("Replaced cosmic card HTML successfully!")
else:
    print("Warning: old_cosmic_card_part not found verbatim")

# 4. Make Jaimini section dynamic with summary container
old_jaimini_section = """            <!-- TAB 10: JAIMINI CHARA KARAKAS -->
            <section class="tab-view-container" id="view-jaimini">

                    <div style="margin-top:12px; padding:12px; background:rgba(10,17,34,0.6); border:1px solid var(--border-gold-soft); border-radius:8px;">
                        <b style="color:var(--accent-gold); font-size:0.82rem; display:block; margin-bottom:6px;">जैमिनी चर कारक फल कथन:</b>
                        <p style="font-size:0.75rem; color:var(--text-secondary); line-height:1.5; margin-bottom:6px;">
                            • <b>आत्मकारक (AK) बुध (29°15′):</b> शास्त्र-लेखन, सॉफ्टवेयर आर्किटेक्चर एवं वैदिक ज्ञान के पुनरुत्थान का दिव्य दायित्व।<br>
                            • <b>अमात्यकारक (AmK) शनि (26°53′):</b> तुला में परम उच्च। न्याय, संगठनात्मक प्रबंधन तथा विशाल जनसमूह के कल्याण से जुड़ा कर्मक्षेत्र।
                        </p>
                    </div>
                <div class="m-card">
                    <div class="m-card-title">
                        <span>जैमिनी 7 चर कारक तालिका (Chara Karakas)</span>
                    </div>
                    <div class="m-table-wrap">
                        <table class="m-table">
                            <thead>
                                <tr>
                                    <th>कारक</th>
                                    <th>ग्रह</th>
                                    <th>राशि</th>
                                    <th>स्पष्ट अंश</th>
                                    <th>कारकत्व</th>
                                </tr>
                            </thead>
                            <tbody id="mJaiminiKarakasBody"></tbody>
                        </table>
                    </div>
                    <div style="background:var(--bg-card-alt); padding:8px; border-radius:6px; margin-top:8px; font-size:0.75rem;">
                        <b>कारकांश लग्न:</b> <span id="mKarakamshaVal" style="color:var(--primary); font-weight:800;">धनु (Atmakaraka गुरु)</span>
                    </div>
                </div>
            </section>"""

new_jaimini_section = """            <!-- TAB 10: JAIMINI CHARA KARAKAS -->
            <section class="tab-view-container" id="view-jaimini">
                <div style="margin-top:12px; padding:14px; background:rgba(10,17,34,0.6); border:1px solid var(--border-gold-soft); border-radius:8px;">
                    <b style="color:var(--accent-gold); font-size:0.90rem; display:block; margin-bottom:6px;">✦ जैमिनी चर कारक फल कथन (Jaimini Sutras):</b>
                    <p id="mJaiminiSummaryContent" style="font-size:0.84rem; color:var(--text-secondary); line-height:1.6; margin:0;">
                        कुण्डली लोड होने पर आत्मकारक एवं अमात्यकारक का विशद शास्त्रीय फलादेश यहाँ प्रदर्शित होगा।
                    </p>
                </div>
                <div class="m-card">
                    <div class="m-card-title">
                        <span>जैमिनी 7 चर कारक तालिका (Chara Karakas - अंश अवरोही क्रम)</span>
                    </div>
                    <div class="m-table-wrap">
                        <table class="m-table">
                            <thead>
                                <tr>
                                    <th>कारक</th>
                                    <th>ग्रह</th>
                                    <th>राशि</th>
                                    <th>स्पष्ट अंश</th>
                                    <th>कारकत्व</th>
                                </tr>
                            </thead>
                            <tbody id="mJaiminiKarakasBody"></tbody>
                        </table>
                    </div>
                    <div style="background:var(--bg-card-alt); padding:10px 14px; border-radius:8px; margin-top:10px; font-size:0.86rem; border:1px solid var(--border-subtle);">
                        <b>कारकांश लग्न (Karakamsha Lagna):</b> <span id="mKarakamshaVal" style="color:var(--primary); font-weight:800;">--</span>
                    </div>
                </div>
            </section>"""

if old_jaimini_section in content:
    content = content.replace(old_jaimini_section, new_jaimini_section)
    print("Replaced Jaimini section HTML successfully!")
else:
    print("Warning: old_jaimini_section not found verbatim")

# 5. Add Lal Kitab & Tajika View Containers
old_lalkitab_section = """            <!-- TAB 12: LAL KITAB -->
            <section class="tab-view-container" id="view-lalkitab">
                <div class="m-card">
                    <div class="m-card-title">
                        <span>📖 लाल किताब 1952 फरमान व सोये ग्रह</span>
                    </div>
                    <div style="font-size:0.76rem; line-height:1.6; color:var(--text-secondary);">
                        <b style="color:var(--primary);">सोया हुआ घर / सोया ग्रह:</b> पंचम एवं एकादश भाव दृष्टि संबंध से जागृत होते हैं।<br>
                        <b style="color:var(--primary);">विशेष हिदायत:</b> शनि उच्च के सप्तम में होने के कारण पराई स्त्री से दूरी रखें, शराब व मांसाहार से पूर्ण परहेज रखें। ऐसा करने से शनि देव राजा समान वैभव प्रदान करते हैं।
                    </div>
                </div>
            </section>"""

new_lalkitab_and_tajika_sections = """            <!-- TAB 12: LAL KITAB 1952 -->
            <section class="tab-view-container" id="view-lalkitab">
                <div id="mLalKitabContent"></div>
            </section>

            <!-- TAB 13: TAJIKA VARSHPHAL -->
            <section class="tab-view-container" id="view-tajika">
                <div id="mTajikaContent"></div>
            </section>"""

if old_lalkitab_section in content:
    content = content.replace(old_lalkitab_section, new_lalkitab_and_tajika_sections)
    print("Replaced Lal Kitab and added Tajika sections successfully!")
else:
    print("Warning: old_lalkitab_section not found verbatim")

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated HTML sections in mobile/index.html!")
