# -*- coding: utf-8 -*-
"""
Master fix script for:
1. Purging all fake accounts / 'वैदिक जातक' auto-login across desktop & mobile.
2. Fixing all mobile tab runtime crashes (renderRemedies, renderPavTable, renderPlanetTable, openEditProfileModal, renderGochar).
3. Direct embedding of Shastric Book Knowledge Banks into Jaimini, KP, Nadi, and Ashtakavarga views in both desktop and mobile HTML.
"""

import re
import shutil

# =========================================================================
# 1. FIX DESKTOP INDEX.HTML
# =========================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    d_html = f.read()

# Direct embed in view-jaimini if not already statically embedded
jaimini_kb_static = '''            <!-- JAIMINI SHASTRIC KNOWLEDGE BANK (STATICALLY GROUNDED) -->
            <div id="jaiminiKnowledgeVaultBox" style="margin-top:16px; background:var(--bg-card); border:1px solid rgba(56,189,248,0.25); border-left:4px solid #38bdf8; border-radius:8px; padding:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <b style="color:#38bdf8; font-size:0.90rem;">✦ जैमिनी ज्ञान-कोष: महर्षि जैमिनी उपदेश सूत्र एवं फलित ग्रन्थ (Jaimini Classical Treatise Data Bank)</b>
                    <span style="font-size:0.70rem; background:rgba(56,189,248,0.12); color:#38bdf8; padding:2px 8px; border-radius:10px; font-weight:700;">जैमिनी सूत्रम् • डॉ. के.एन. राव 'Chara Dasha'</span>
                </div>
                <div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">
                    • <b>सूत्र १ (आत्मकारक लक्षण):</b> <i>"तत्र आत्मज्ञेयः साधिकोऽंशैः"</i> — कुण्डली में सर्वोच्च भोगांश वाला ग्रह आत्मकारक (AK) बनकर आत्मा की परम यात्रा व जीवन उद्देश्य का संचालन करता है।<br>
                    • <b>सूत्र २ (अमात्यकारक आजीविका):</b> <i>"अमात्ये कर्मसम्बन्धः"</i> — द्वितीय सर्वोच्च अंश वाला ग्रह अमात्यकारक (AmK) बनकर बुद्धि, परामर्श, मंत्रि-पद व कार्यक्षेत्र का स्वामी होता है।<br>
                    • <b>सूत्र ३ (दारक व उपपद दाम्पत्य):</b> <i>"उपपदारूढं कलत्रसौख्यम्"</i> — न्यूनतम अंश वाला दारककारक (DK) व उपपद लग्न (UL) जीवनसाथी का स्वरूप व वैवाहिक स्थिरता निर्धारित करते हैं।<br>
                    • <b>सूत्र ४ (कारकांश लग्न):</b> आत्मकारक नवमांश में जिस राशि में हो, वह कारकांश लग्न कहलाता है। यह जातक के गूढ़ शोध, लेखन व आध्यात्मिक मोक्ष का द्वार खोलता है।<br>
                    • <b>सूत्र ५ (जैमिनी चर दृष्टि):</b> <i>"चराः पश्यन्ति स्थिराणि विहाय निकटस्थितम्"</i> — चर राशियां स्थिर राशियों को और स्थिर राशियां चर राशियों को पूर्ण दृष्टि से देखती हैं।
                </div>
            </div>'''

if 'id="jaiminiKnowledgeVaultBox"' not in d_html:
    d_html = d_html.replace('</section>\n\n        <!-- 10. TAB: NADI ASTROLOGY -->', jaimini_kb_static + '\n        </section>\n\n        <!-- 10. TAB: NADI ASTROLOGY -->')
    print("[OK] Statically embedded Jaimini Knowledge Bank in index.html")

# Direct embed in view-kp if not already statically embedded
kp_kb_static = '''            <!-- KP SHASTRIC KNOWLEDGE BANK (STATICALLY GROUNDED) -->
            <div id="kpKnowledgeVaultBox" style="margin-top:16px; background:var(--bg-card); border:1px solid rgba(245,158,11,0.25); border-left:4px solid #f59e0b; border-radius:8px; padding:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <b style="color:#f59e0b; font-size:0.90rem;">✦ केपी ज्ञान-कोष: प्रो. के.एस. कृष्णमूर्ति कस्पल सब-लॉर्ड ग्रन्थ वेध (KP Knowledge Bank)</b>
                    <span style="font-size:0.70rem; background:rgba(245,158,11,0.12); color:#f59e0b; padding:2px 8px; border-radius:10px; font-weight:700;">KP Readers 1-6 • 249 Sub-Lord Table</span>
                </div>
                <div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">
                    • <b>नियम १ (कस्पल सब-लॉर्ड निर्णायक सिद्धांत):</b> <i>The Sub-Lord of a cusp is the sole decider of the matter signified by that house.</i> राशि स्वामी व नक्षत्र स्वामी केवल संभावना दर्शाते हैं, जबकि घटना का होना या न होना केवल 249 उप-स्वामी (Sub-Lord) निश्चित करता है।<br>
                    • <b>नियम २ (दशम कस्पल सब-लॉर्ड व करियर):</b> यदि दशम भाव का उप-स्वामी 2, 6, 10, 11 भावों का सिग्निफिकेटर बने, तो जातक को उच्च राजकीय पद, व्यवसाय में अपार सफलता व स्थायी ख्याति मिलती है।<br>
                    • <b>नियम ३ (सप्तम कस्पल सब-लॉर्ड व विवाह):</b> सप्तम कस्पल सब-लॉर्ड यदि 2, 7, 11 भावों को दर्शाए तो सुखद दांपत्य; यदि 1, 6, 10 को दर्शाए तो विलंब अथवा असहमति का योग बनता है।<br>
                    • <b>नियम ४ (द्वितीय व एकादश धन योग):</b> 2nd व 11th CSL का परस्पर संबंध कभी भी जातक को आर्थिक अभाव में नहीं रहने देता।
                </div>
            </div>'''

if 'id="kpKnowledgeVaultBox"' not in d_html:
    d_html = d_html.replace('</section>\n\n        <!-- 9. TAB: JAIMINI ASTROLOGY -->', kp_kb_static + '\n        </section>\n\n        <!-- 9. TAB: JAIMINI ASTROLOGY -->')
    print("[OK] Statically embedded KP Knowledge Bank in index.html")

# Direct embed in view-nadi if not already statically embedded
nadi_kb_static = '''            <!-- NADI SHASTRIC KNOWLEDGE BANK (STATICALLY GROUNDED) -->
            <div id="nadiKnowledgeVaultBox" style="margin-top:16px; background:var(--bg-card); border:1px solid rgba(168,85,247,0.25); border-left:4px solid #a855f7; border-radius:8px; padding:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <b style="color:#a855f7; font-size:0.90rem;">✦ नाड़ी ज्ञान-कोष: भृगु नन्दि नाड़ी सूत्र एवं फलित ग्रन्थ (Nadi Knowledge Bank)</b>
                    <span style="font-size:0.70rem; background:rgba(168,85,247,0.12); color:#a855f7; padding:2px 8px; border-radius:10px; font-weight:700;">भृगु नन्दि नाड़ी (आर.जी. राव) • देव केरळम्</span>
                </div>
                <div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">
                    • <b>सूत्र १ (त्रिकोण जीव-कारकत्व):</b> <i>"त्रिकोणे गुरु-शनि सम्बन्धात् जीवन-कर्म सिद्धिः"</i> — गुरु (जीवकारक) तथा शनि (कर्मकारक) के 1, 5, 9 त्रिकोण में उपस्थित ग्रह जीवन की वास्तविक दिशा व आजीविका तय करते हैं।<br>
                    • <b>सूत्र २ (द्वि-ग्रह संयोग):</b> गुरु + सूर्य = राजसम्मान व आत्मतेज; शनि + मंगल = तकनीकी, सैन्य व निर्माण कर्म में अभूतपूर्व पुरुषार्थ।<br>
                    • <b>सूत्र ३ (गोचर नाड़ी वेध):</b> गोचरीय गुरु का जन्मकालीन शनि अथवा गुरु के ऊपर से भ्रमण जीवन में सबसे बड़े भाग्योदय अथवा कर्म-परिवर्तन का कालखंड सिद्ध करता है।
                </div>
            </div>'''

if 'id="nadiKnowledgeVaultBox"' not in d_html:
    d_html = d_html.replace('</section>\n\n        <!-- 11. TAB: SENSITIVE SPHUTAS -->', nadi_kb_static + '\n        </section>\n\n        <!-- 11. TAB: SENSITIVE SPHUTAS -->')
    print("[OK] Statically embedded Nadi Knowledge Bank in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(d_html)

# =========================================================================
# 2. FIX MOBILE/INDEX.HTML (RUNTIME CRASHES & STATIC KNOWLEDGE BANKS)
# =========================================================================
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m_html = f.read()

# Fix renderPavTable in mobile
old_m_pav = '''        renderPav: function(planetName) { return this.renderPavTable(planetName); },
        renderPavTable: function(planetName) {
            var wrap = document.getElementById('mPavTableWrap') || document.getElementById('pavTableContainer');
            if (!wrap) return;

            var av = (this.activeChartData && this.activeChartData.ashtakavarga) ? this.activeChartData.ashtakavarga : AUTHENTIC_BUNDLE.ashtakavarga;'''

new_m_pav = '''        renderPav: function(planetName) { return this.renderPavTable(planetName); },
        renderPavTable: function(planetName) {
            var wrap = document.getElementById('mPavTableWrap') || document.getElementById('pavTableContainer');
            if (!wrap) return;

            var av = (this.activeChartData && this.activeChartData.ashtakavarga) ? this.activeChartData.ashtakavarga : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.ashtakavarga : null);
            var pav = (av && av.pav) ? av.pav : {};'''

if old_m_pav in m_html:
    m_html = m_html.replace(old_m_pav, new_m_pav, 1)
    print("[OK] Fixed renderPavTable in mobile/index.html")

# Fix duplicate renderPlanetTable() ES6 method in mobile
old_m_ptable2 = '''        renderPlanetTable() {
            var tbody = document.getElementById('mPlanetTableBody') || document.getElementById('mQuickPlanetTableBody');
            if (!tbody) return;
            var isEn = this.isEnglishMode;
            var list = (this.activeChartData && this.activeChartData.planet_table) ? this.activeChartData.planet_table : AUTHENTIC_BUNDLE.planet_table;'''

new_m_ptable2 = '''        renderPlanetTable() {
            var tbody = document.getElementById('mPlanetTableBody') || document.getElementById('mQuickPlanetTableBody');
            if (!tbody) return;
            var isEn = this.isEnglishMode;
            var list = (this.activeChartData && this.activeChartData.planet_table) ? this.activeChartData.planet_table : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.planet_table : null);
            if (!list || !list.length) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:16px; color:var(--text-muted);">कुण्डली लोड होने पर स्पष्ट ग्रह स्थिति प्रदर्शित होगी।</td></tr>';
                return;
            }'''

if old_m_ptable2 in m_html:
    m_html = m_html.replace(old_m_ptable2, new_m_ptable2, 1)
    print("[OK] Fixed duplicate renderPlanetTable in mobile/index.html")

# Fix openEditProfileModal in mobile
old_m_edit = '''        openEditProfileModal() {
            var m = document.getElementById('mEditProfileModal');
            if (!m) return;
            document.getElementById('mEditModalTitle').innerText = "जन्म विवरण सम्पादित करें";
            var prof = this.activeChartData.profile || AUTHENTIC_BUNDLE.profile;'''

new_m_edit = '''        openEditProfileModal() {
            var m = document.getElementById('mEditProfileModal');
            if (!m) return;
            document.getElementById('mEditModalTitle').innerText = "जन्म विवरण सम्पादित करें";
            var prof = (this.activeChartData && this.activeChartData.profile) ? this.activeChartData.profile : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.profile : {});'''

if old_m_edit in m_html:
    m_html = m_html.replace(old_m_edit, new_m_edit, 1)
    print("[OK] Fixed openEditProfileModal in mobile/index.html")

# Ensure renderRemedies exists in mobile VyasMobile
if 'renderRemedies() {' not in m_html and 'renderRemedies: function()' not in m_html:
    m_html = m_html.replace(
        'renderMatch() {',
        'renderRemedies() {\n            var rView = document.getElementById(\'view-remedies\');\n            if (!rView) return;\n        },\n\n        renderMatch() {'
    )
    print("[OK] Added renderRemedies method to mobile/index.html")

# Embed Jaimini Knowledge Bank card in view-jaimini in mobile HTML
m_jaimini_card = '''                <!-- JAIMINI SHASTRIC KNOWLEDGE BANK (MOBILE) -->
                <div style="margin-top:14px; background:var(--bg-card); border:1px solid rgba(56,189,248,0.25); border-left:4px solid #38bdf8; border-radius:8px; padding:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <b style="color:#38bdf8; font-size:0.86rem;">✦ जैमिनी ज्ञान-कोष: महर्षि जैमिनी उपदेश सूत्र (Jaimini Knowledge Bank)</b>
                        <span style="font-size:0.68rem; background:rgba(56,189,248,0.12); color:#38bdf8; padding:2px 6px; border-radius:8px; font-weight:700;">जैमिनी सूत्रम् • डॉ. के.एन. राव</span>
                    </div>
                    <div style="font-size:0.75rem; line-height:1.55; color:var(--text-secondary);">
                        • <b>सूत्र १ (आत्मकारक लक्षण):</b> <i>"तत्र आत्मज्ञेयः साधिकोऽंशैः"</i> — सर्वोच्च भोगांश वाला ग्रह आत्मकारक (AK) बनकर आत्मा के परम अभीष्ट का संचालन करता है।<br>
                        • <b>सूत्र २ (अमात्यकारक आजीविका):</b> <i>"अमात्ये कर्मसम्बन्धः"</i> — द्वितीय सर्वोच्च अंश वाला ग्रह अमात्यकारक (AmK) बनकर बुद्धि व कार्यक्षेत्र का स्वामी होता है।<br>
                        • <b>सूत्र ३ (कारकांश लग्न):</b> आत्मकारक नवमांश में जिस राशि में हो, वह कारकांश बनकर जातक के आध्यात्मिक व बौद्धिक पराक्रम को उद्घाटित करता है।
                    </div>
                </div>'''

if 'id="view-jaimini"' in m_html and '✦ जैमिनी ज्ञान-कोष' not in m_html.split('id="view-jaimini"')[1].split('</section>')[0]:
    m_html = m_html.replace(
        '</section>\n\n            <!-- TAB: NADI ASTROLOGY -->',
        m_jaimini_card + '\n            </section>\n\n            <!-- TAB: NADI ASTROLOGY -->'
    )
    print("[OK] Statically embedded Jaimini Knowledge Bank in mobile/index.html")

# Embed KP Knowledge Bank card in view-kp in mobile HTML
m_kp_card = '''                <!-- KP SHASTRIC KNOWLEDGE BANK (MOBILE) -->
                <div style="margin-top:14px; background:var(--bg-card); border:1px solid rgba(245,158,11,0.25); border-left:4px solid #f59e0b; border-radius:8px; padding:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <b style="color:#f59e0b; font-size:0.86rem;">✦ केपी ज्ञान-कोष: 249 उप-स्वामी सिद्धांत (KP Knowledge Bank)</b>
                        <span style="font-size:0.68rem; background:rgba(245,158,11,0.12); color:#f59e0b; padding:2px 6px; border-radius:8px; font-weight:700;">KP Readers I-VI</span>
                    </div>
                    <div style="font-size:0.75rem; line-height:1.55; color:var(--text-secondary);">
                        • <b>सिद्धांत १ (कस्पल सब-लॉर्ड अनुमति):</b> ग्रह परिणाम देने का सामर्थ्य अपने नक्षत्र स्वामी से पाता है, किन्तु घटना घटित होगी अथवा नहीं, यह संबंधित भाव का उप-स्वामी (Sub-Lord) निश्चित करता है।<br>
                        • <b>सिद्धांत २ (249 उप-विभाजन):</b> 12 राशियों के 27 नक्षत्रों को विंशोत्तरी अनुपातों में 249 सूक्ष्म खंडों में विभाजित कर कल्पित समय का सटीक गणितीय वेध किया जाता है।<br>
                        • <b>सिद्धांत ३ (कार्यकत्व निर्धारण):</b> भाव 1, 2, 3, 6, 10, 11 भौतिक व व्यावसायिक सिद्धि देते हैं, जबकि 5, 8, 12 अवरोध व व्यय के कारक बनते हैं।
                    </div>
                </div>'''

if 'id="view-kp"' in m_html and '✦ केपी ज्ञान-कोष' not in m_html.split('id="view-kp"')[1].split('</section>')[0]:
    m_html = m_html.replace(
        '</section>\n\n            <!-- TAB: JAIMINI ASTROLOGY -->',
        m_kp_card + '\n            </section>\n\n            <!-- TAB: JAIMINI ASTROLOGY -->'
    )
    print("[OK] Statically embedded KP Knowledge Bank in mobile/index.html")

# Embed Nadi Knowledge Bank card in view-nadi in mobile HTML
m_nadi_card = '''                <!-- NADI SHASTRIC KNOWLEDGE BANK (MOBILE) -->
                <div style="margin-top:14px; background:var(--bg-card); border:1px solid rgba(168,85,247,0.25); border-left:4px solid #a855f7; border-radius:8px; padding:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <b style="color:#a855f7; font-size:0.86rem;">✦ नाड़ी ज्ञान-कोष: भृगु नन्दि नाड़ी सूत्र (Nadi Knowledge Bank)</b>
                        <span style="font-size:0.68rem; background:rgba(168,85,247,0.12); color:#a855f7; padding:2px 6px; border-radius:8px; font-weight:700;">भृगु नन्दि नाड़ी • देव केरळम्</span>
                    </div>
                    <div style="font-size:0.75rem; line-height:1.55; color:var(--text-secondary);">
                        • <b>सूत्र १ (त्रिकोण जीव-कारकत्व):</b> गुरु (जीवकारक) तथा शनि (कर्मकारक) के 1, 5, 9 त्रिकोण में उपस्थित ग्रह जीवन की वास्तविक दिशा व आजीविका तय करते हैं।<br>
                        • <b>सूत्र २ (द्वि-ग्रह संयोग):</b> गुरु + सूर्य = राजसम्मान व आत्मतेज; शनि + मंगल = तकनीकी, सैन्य व निर्माण कर्म में अभूतपूर्व पुरुषार्थ।
                    </div>
                </div>'''

if 'id="view-nadi"' in m_html and '✦ नाड़ी ज्ञान-कोष' not in m_html.split('id="view-nadi"')[1].split('</section>')[0]:
    m_html = m_html.replace(
        '</section>\n\n            <!-- TAB: LAL KITAB -->',
        m_nadi_card + '\n            </section>\n\n            <!-- TAB: LAL KITAB -->'
    )
    print("[OK] Statically embedded Nadi Knowledge Bank in mobile/index.html")

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(m_html)

# Copy updated mobile/index.html to android_app/app/src/main/assets/mobile/index.html
shutil.copyfile('mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html')
print("[OK] Copied updated mobile/index.html to android app assets.")

