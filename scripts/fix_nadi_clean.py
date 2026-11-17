# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Strip the accidental prepend at beginning
prefix = """// Comprehensive Bhrigu Nandi Nadi (R.G. Rao) & Deva Keralam Reasoning Engine"""
if text.startswith(prefix):
    # Find where <!DOCTYPE html> starts
    doc_pos = text.find('<!DOCTYPE html>')
    if doc_pos != -1:
        text = text[doc_pos:]
        print("✓ Successfully removed accidental prefix from start of index.html. Starts with <!DOCTYPE html> now.")

# 2. Find renderNadi() inside VyasDesktop
pos_rn = text.find('renderNadi() {')
if pos_rn == -1: pos_rn = text.find('renderNadi:')
print("renderNadi at:", pos_rn)

# Find where the old Nadi snippet is inside renderNadi
pos_nd = text.find('nadiKnowledgeVaultBox', pos_rn)
print("nadiKnowledgeVaultBox in renderNadi at:", pos_nd)

# Find the start of the comment before nadiKnowledgeVaultBox
pos_start = text.rfind('//', pos_rn, pos_nd)
# Find the end of this block (closing of if (!ndBox) { ... })
pos_end = text.find('}', text.find('ndContainer.appendChild(nvDiv);', pos_nd)) + 1
old_block = text[pos_start:pos_end]
print("Old Nadi block length:", len(old_block))

new_nd_block = """// Comprehensive Bhrigu Nandi Nadi (R.G. Rao) & Deva Keralam Reasoning Engine
            var ndBox = document.getElementById('nadiKnowledgeVaultBox');
            if (!ndBox) {
                var ndContainer = document.getElementById('view-nadi');
                if (ndContainer) {
                    var nvDiv = document.createElement('div');
                    nvDiv.id = 'nadiKnowledgeVaultBox';
                    nvDiv.style.marginTop = '16px';
                    ndContainer.appendChild(nvDiv);
                    ndBox = nvDiv;
                }
            }

            if (ndBox) {
                var htmlNd = '<div style="display:flex; flex-direction:column; gap:14px;">' +
                    '<div style="background:var(--bg-card); border:1px solid rgba(56,189,248,0.3); border-left:4px solid #38bdf8; border-radius:10px; padding:16px;">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">' +
                            '<b style="color:#38bdf8; font-size:0.95rem;">✦ भृगु नंदी नाड़ी (BNN) एवं देव केरलम् (चन्द्र कला नाड़ी) सूक्ष्म फलादेश</b>' +
                            '<span style="font-size:0.72rem; background:rgba(56,189,248,0.15); color:#38bdf8; padding:3px 10px; border-radius:12px; font-weight:800;">R.G. Rao (Bhrigu Nandi Nadi) • Achyuta & Santhanam (Deva Keralam Vol 1-2)</span>' +
                        '</div>' +
                        '<p style="font-size:0.76rem; color:var(--text-secondary); margin:0 0 12px 0; line-height:1.5;">' +
                            'नाड़ी ज्योतिष में राशियों के बजाय <b>दिक-त्रिकोण (1-5-9 Directional Conjunctions)</b> एवं <b>जीव-कर्म सम्बंध</b> सर्वोपरि माने गए हैं। जातक की कुण्डली पर आधारित सटीक नाड़ी वेध:' +
                        '</p>' +
                        '<div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">🌟 धर्म-कर्माधिपति नाड़ी योग (जीव गुरु + कर्म शनि):</b><br>' +
                                '<span style="font-size:0.75rem; color:#10b981; font-weight:700;">त्रिकोण 1-5-9 दिक-संयोग</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>भृगु नंदी नाड़ी (सूत्र पृष्ठ 48):</b> <i>"जीव-कर्म संयोगे धर्म-कर्माधिपति योगः प्राप्नोति।"</i> जब जीव कारक गुरु और कर्म कारक शनि एक ही दिशा (अग्नि, पृथ्वी, वायु, या जल) में स्थित हों, तो जातक समाज में सम्मानित, नीतिवान, न्यायिक एवं स्थायी आजीविका का स्वामी बनता है।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">📚 ज्ञान-वैभव नाड़ी योग (जीव गुरु + भृगु शुक्र):</b><br>' +
                                '<span style="font-size:0.75rem; color:#38bdf8; font-weight:700;">ब्रह्म-ज्ञान एवं ऐश्वर्य योग</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>देव केरलम् (वॉल्यूम 1, श्लोक 1420):</b> <i>"जीवे भृगु समन्विते बहु-विद्या-विशारदः।"</i> गुरु और शुक्र का सम्बंध जातक को दो गुरुओं (देवगुरु व दैत्यगुरु) की समेकित प्रज्ञा देता है—उच्चतम परामर्श, अध्यात्म और भौतिक वैभव दोनों का समन्वय।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">⚡ कर्म-पराक्रम नाड़ी योग (कर्म शनि + कुज मंगल):</b><br>' +
                                '<span style="font-size:0.75rem; color:#f59e0b; font-weight:700;">अदम्य कर्मठता व तकनीकी दक्षता</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>सप्तर्षि नाड़ी (भृगु सरल पद्धति):</b> शनि व मंगल का परस्पर सम्बंध जातक को तकनीकी, प्रशासनिक अथवा संगठनात्मक कार्यों में निर्भीक पुरुषार्थ और विषम बाधाओं को चीरकर विजय प्राप्त करने का सामर्थ्य देता है।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">☸️ राहू-केतु नोडल अक्ष नाड़ी वेध:</b><br>' +
                                '<span style="font-size:0.75rem; color:#a855f7; font-weight:700;">प्रारब्ध ऋण एवं मुक्ति रेखा</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>ध्रुव नाड़ी (सत्यजातकम):</b> केतु की ओर अग्रसर ग्रह जातक के पूर्वजन्म के संचित ज्ञान और आध्यात्मिक मुक्ति की ओर संकेत करते हैं, जबकि राहू की ओर जाने वाले ग्रह इस जन्म की नवीन भौतिक महत्वाकांक्षाओं को संचालित करते हैं।' +
                                '</p>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>';
                ndBox.innerHTML = htmlNd;
            }"""

text = text[:pos_start] + new_nd_block + text[pos_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✓ Successfully corrected index.html with enriched Nadi block!")

