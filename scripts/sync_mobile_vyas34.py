# -*- coding: utf-8 -*-
"""
Sync mobile/index.html with:
1. VyasDaivagyaVision.synthesizeConsolidatedPhalitEssay
2. renderPredictions using synthesizeConsolidatedPhalitEssay
3. Vidha-specific knowledge banks in renderKP, renderJaimini, renderNadi
4. window.VyasAIEngine.MASTER_SYSTEM_PROMPT with VYAS 34.0 framework
Then copy mobile/index.html to android_app/app/src/main/assets/mobile/index.html.
"""

import re
import shutil

# Read index.html to extract synthesizeConsolidatedPhalitEssay and MASTER_SYSTEM_PROMPT
with open('index.html', 'r', encoding='utf-8') as f:
    desktop_html = f.read()

# Extract synthesizeConsolidatedPhalitEssay
essay_match = re.search(r'(synthesizeConsolidatedPhalitEssay:\s*function\(chart\)\s*\{[\s\S]*?\n\s*\},)(?=\s*analyzeChartTruth)', desktop_html)
if not essay_match:
    print("[ERROR] Could not extract synthesizeConsolidatedPhalitEssay from index.html")
    exit(1)
essay_fn_code = essay_match.group(1)

# Extract MASTER_SYSTEM_PROMPT
prompt_match = re.search(r"MASTER_SYSTEM_PROMPT:\s*'[^\r\n]*?'", desktop_html)
if not prompt_match:
    print("[ERROR] Could not extract MASTER_SYSTEM_PROMPT from index.html")
    exit(1)
master_prompt_code = prompt_match.group(0)

# Read mobile/index.html
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    mobile_html = f.read()

# 1. Inject synthesizeConsolidatedPhalitEssay into VyasDaivagyaVision
if 'synthesizeConsolidatedPhalitEssay' not in mobile_html:
    mobile_html = mobile_html.replace(
        'var VyasDaivagyaVision = {\n\n        // 1. Core Chart Assessment\n        analyzeChartTruth: function(chart) {',
        'var VyasDaivagyaVision = {\n\n        // 1. Core Chart Assessment\n        ' + essay_fn_code + '\n\n        analyzeChartTruth: function(chart) {'
    )
    print("[OK] Injected synthesizeConsolidatedPhalitEssay into mobile/index.html")

# 2. Update renderPredictions in mobile/index.html
old_render_preds = '''        renderPredictions: function() {
            var container = document.getElementById('mBhavaAccordionContainer') || document.getElementById('bhavasForensicAccordion');
            if (!container) return;'''

new_render_preds = '''        renderPredictions: function() {
            var container = document.getElementById('mBhavaAccordionContainer') || document.getElementById('bhavasForensicAccordion');
            if (!container) return;

            if (!this.activeChartData || !this.activeChartData.profile || !this.activeChartData.profile.name) {
                container.innerHTML = '<div style="padding:28px 16px; text-align:center; color:var(--text-muted); font-size:0.85rem;"><b style="color:var(--accent-gold);">12 भावों का फलादेश उपलब्ध नहीं</b><p style="font-size:0.75rem; margin-top:4px;">व्यास 34.0 संश्लेषित जीवन फलादेश महा-निबंध देखने हेतु कृपया अपनी जन्म कुण्डली बनाएं।</p></div>';
                return;
            }

            // Render VYAS 34.0 Master Consolidated Phalit Essay (वृहद् संश्लेषित जीवन फलादेश महा-निबंध)
            if (window.VyasDaivagyaVision && window.VyasDaivagyaVision.synthesizeConsolidatedPhalitEssay) {
                container.innerHTML = window.VyasDaivagyaVision.synthesizeConsolidatedPhalitEssay(this.activeChartData);
                return;
            }'''

if old_render_preds in mobile_html:
    mobile_html = mobile_html.replace(old_render_preds, new_render_preds)
    print("[OK] Updated renderPredictions in mobile/index.html to use Consolidated Phalit Essay")

# 3. Inject Vidha-specific knowledge banks into renderKP, renderJaimini, renderNadi
kp_kb_mobile = '''
            // Append KP Shastric Knowledge Bank
            var kpBox = document.getElementById('kpKnowledgeVaultBoxMobile');
            if (!kpBox) {
                var kpContainer = document.getElementById('view-kp') || document.getElementById('kpCuspsSubLordsTbody');
                if (kpContainer) {
                    var parentCard = kpContainer.closest ? kpContainer.closest('.content-card, .tab-pane, div') : kpContainer.parentElement;
                    if (parentCard) {
                        var kvDiv = document.createElement('div');
                        kvDiv.id = 'kpKnowledgeVaultBoxMobile';
                        kvDiv.style.marginTop = '14px';
                        kvDiv.innerHTML = '<div style="background:var(--bg-card); border:1px solid rgba(245,158,11,0.25); border-left:4px solid #f59e0b; border-radius:8px; padding:12px;">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                                '<b style="color:#f59e0b; font-size:0.86rem;">✦ केपी ज्ञान-कोष: 249 उप-स्वामी सिद्धांत (KP Knowledge Bank)</b>' +
                                '<span style="font-size:0.68rem; background:rgba(245,158,11,0.12); color:#f59e0b; padding:2px 6px; border-radius:8px; font-weight:700;">KP Readers I-VI</span>' +
                            '</div>' +
                            '<div style="font-size:0.75rem; line-height:1.55; color:var(--text-secondary);">' +
                                '• <b>सिद्धांत १ (कस्पल सब-लॉर्ड अनुमति):</b> ग्रह परिणाम देने का सामर्थ्य अपने नक्षत्र स्वामी से पाता है, किन्तु घटना घटित होगी अथवा नहीं, यह संबंधित भाव का उप-स्वामी (Sub-Lord) निश्चित करता है।<br>' +
                                '• <b>सिद्धांत २ (249 उप-विभाजन):</b> 12 राशियों के 27 नक्षत्रों को विंशोत्तरी अनुपातों में 249 सूक्ष्म खंडों में विभाजित कर कल्पित समय का सटीक गणितीय वेध किया जाता है।<br>' +
                                '• <b>सिद्धांत ३ (कार्यकत्व निर्धारण):</b> भाव 1, 2, 3, 6, 10, 11 भौतिक व व्यावसायिक सिद्धि देते हैं, जबकि 5, 8, 12 अवरोध व व्यय के कारक बनते हैं।' +
                            '</div>' +
                        '</div>';
                        parentCard.appendChild(kvDiv);
                    }
                }
            }
'''

jaimini_kb_mobile = '''
            // Append Jaimini Shastric Knowledge Bank
            var jmBox = document.getElementById('jaiminiKnowledgeVaultBoxMobile');
            if (!jmBox) {
                var jmContainer = document.getElementById('view-jaimini') || document.getElementById('jaiminiKarakaTbody');
                if (jmContainer) {
                    var parentCard = jmContainer.closest ? jmContainer.closest('.content-card, .tab-pane, div') : jmContainer.parentElement;
                    if (parentCard) {
                        var kvDiv = document.createElement('div');
                        kvDiv.id = 'jaiminiKnowledgeVaultBoxMobile';
                        kvDiv.style.marginTop = '14px';
                        kvDiv.innerHTML = '<div style="background:var(--bg-card); border:1px solid rgba(56,189,248,0.25); border-left:4px solid #38bdf8; border-radius:8px; padding:12px;">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                                '<b style="color:#38bdf8; font-size:0.86rem;">✦ जैमिनी ज्ञान-कोष: महर्षि जैमिनी उपदेश सूत्र (Jaimini Knowledge Bank)</b>' +
                                '<span style="font-size:0.68rem; background:rgba(56,189,248,0.12); color:#38bdf8; padding:2px 6px; border-radius:8px; font-weight:700;">जैमिनी सूत्रम् • डॉ. के.एन. राव</span>' +
                            '</div>' +
                            '<div style="font-size:0.75rem; line-height:1.55; color:var(--text-secondary);">' +
                                '• <b>सूत्र १ (आत्मकारक लक्षण):</b> <i>"तत्र आत्मज्ञेयः साधिकोऽंशैः"</i> — सर्वोच्च भोगांश वाला ग्रह आत्मकारक (AK) बनकर आत्मा के परम अभीष्ट का संचालन करता है।<br>' +
                                '• <b>सूत्र २ (अमात्यकारक आजीविका):</b> <i>"अमात्ये कर्मसम्बन्धः"</i> — द्वितीय सर्वोच्च अंश वाला ग्रह अमात्यकारक (AmK) बनकर बुद्धि व कार्यक्षेत्र का स्वामी होता है।<br>' +
                                '• <b>सूत्र ३ (कारकांश लग्न):</b> आत्मकारक नवमांश में जिस राशि में हो, वह कारकांश बनकर जातक के आध्यात्मिक व बौद्धिक पराक्रम को उद्घाटित करता है।' +
                            '</div>' +
                        '</div>';
                        parentCard.appendChild(kvDiv);
                    }
                }
            }
'''

nadi_kb_mobile = '''
            // Append Nadi Shastric Knowledge Bank
            var ndBox = document.getElementById('nadiKnowledgeVaultBoxMobile');
            if (!ndBox) {
                var ndContainer = document.getElementById('view-nadi') || document.getElementById('nadiCombinationsContainer');
                if (ndContainer) {
                    var parentCard = ndContainer.closest ? ndContainer.closest('.content-card, .tab-pane, div') : ndContainer.parentElement;
                    if (parentCard) {
                        var kvDiv = document.createElement('div');
                        kvDiv.id = 'nadiKnowledgeVaultBoxMobile';
                        kvDiv.style.marginTop = '14px';
                        kvDiv.innerHTML = '<div style="background:var(--bg-card); border:1px solid rgba(168,85,247,0.25); border-left:4px solid #a855f7; border-radius:8px; padding:12px;">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                                '<b style="color:#a855f7; font-size:0.86rem;">✦ नाड़ी ज्ञान-कोष: भृगु नन्दि नाड़ी सूत्र (Nadi Knowledge Bank)</b>' +
                                '<span style="font-size:0.68rem; background:rgba(168,85,247,0.12); color:#a855f7; padding:2px 6px; border-radius:8px; font-weight:700;">भृगु नन्दि नाड़ी • देव केरळम्</span>' +
                            '</div>' +
                            '<div style="font-size:0.75rem; line-height:1.55; color:var(--text-secondary);">' +
                                '• <b>सूत्र १ (त्रिकोण जीव-कारकत्व):</b> गुरु (जीवकारक) तथा शनि (कर्मकारक) के 1, 5, 9 त्रिकोण में उपस्थित ग्रह जीवन की वास्तविक दिशा व आजीविका तय करते हैं।<br>' +
                                '• <b>सूत्र २ (द्वि-ग्रह संयोग):</b> गुरु + सूर्य = राजसम्मान व आत्मतेज; शनि + मंगल = तकनीकी, सैन्य व निर्माण कर्म में अभूतपूर्व पुरुषार्थ।' +
                            '</div>' +
                        '</div>';
                        parentCard.appendChild(kvDiv);
                    }
                }
            }
'''

# Inject into renderKP
if 'kpKnowledgeVaultBoxMobile' not in mobile_html:
    mobile_html = mobile_html.replace(
        'renderKP: function() {',
        'renderKP: function() {' + kp_kb_mobile
    )
    print("[OK] Injected KP Knowledge Bank into mobile/index.html")

# Inject into renderJaimini
if 'jaiminiKnowledgeVaultBoxMobile' not in mobile_html:
    mobile_html = mobile_html.replace(
        'renderJaimini: function() {',
        'renderJaimini: function() {' + jaimini_kb_mobile
    )
    print("[OK] Injected Jaimini Knowledge Bank into mobile/index.html")

# Inject into renderNadi
if 'nadiKnowledgeVaultBoxMobile' not in mobile_html:
    mobile_html = mobile_html.replace(
        'renderNadi: function() {',
        'renderNadi: function() {' + nadi_kb_mobile
    )
    print("[OK] Injected Nadi Knowledge Bank into mobile/index.html")

# 4. Inject VYAS 34.0 Master Prompt into mobile VyasAIEngine
if 'VYAS 34.0 — AGENTIC JYOTISHA INTELLIGENCE SYSTEM' not in mobile_html:
    mobile_html = mobile_html.replace(
        'window.VyasAIEngine = {',
        'window.VyasAIEngine = {\n        ' + master_prompt_code + ',\n'
    )
    print("[OK] Injected VYAS 34.0 Master Prompt into mobile/index.html")

# Write updated mobile/index.html
with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(mobile_html)

# Copy to android_app/app/src/main/assets/mobile/index.html
shutil.copyfile('mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html')
print("[OK] Copied mobile/index.html to android_app/app/src/main/assets/mobile/index.html")
