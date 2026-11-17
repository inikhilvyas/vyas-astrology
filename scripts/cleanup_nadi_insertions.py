# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Remove the one after container.innerHTML = html; in Dasha
dasha_bad = '''            container.innerHTML = html;

            // Append Nadi Shastric Knowledge Bank
            var ndBox = document.getElementById('nadiKnowledgeVaultBox');
            if (!ndBox) {
                var ndContainer = document.getElementById('view-nadi');
                if (ndContainer) {
                    var kvDiv = document.createElement('div');
                    kvDiv.id = 'nadiKnowledgeVaultBox';
                    kvDiv.style.marginTop = '16px';
                    kvDiv.innerHTML = '<div style="background:var(--bg-card); border:1px solid rgba(168,85,247,0.25); border-left:4px solid #a855f7; border-radius:8px; padding:14px;">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">' +
                            '<b style="color:#a855f7; font-size:0.90rem;">✦ नाड़ी ज्ञान-कोष: भृगु नन्दि नाड़ी सूत्र एवं फलित ग्रन्थ (Nadi Knowledge Bank)</b>' +
                            '<span style="font-size:0.70rem; background:rgba(168,85,247,0.12); color:#a855f7; padding:2px 8px; border-radius:10px; font-weight:700;">भृगु नन्दि नाड़ी • देव केरळम्</span>' +
                        '</div>' +
                        '<div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">' +
                            '• <b>सूत्र १ (त्रिकोण जीव-कारकत्व):</b> <i>"त्रिकोणे गुरु-शनि सम्बन्धात् जीवन-कर्म सिद्धिः"</i> — गुरु (जीवकारक) तथा शनि (कर्मकारक) के 1, 5, 9 त्रिकोण में उपस्थित ग्रह जीवन की वास्तविक दिशा व आजीविका तय करते हैं。<br>' +
                            '• <b>सूत्र २ (द्वि-ग्रह संयोग):</b> गुरु + सूर्य = राजसम्मान व आत्मतेज; शनि + मंगल = तकनीकी, सैन्य व निर्माण कर्म में अभूतपूर्व पुरुषार्थ。<br>' +
                            '• <b>सूत्र ३ (गोचर नाड़ी वेध):</b> गोचरीय गुरु का जन्मकालीन शनि अथवा गुरु के ऊपर से भ्रमण जीवन में सबसे बड़े भाग्योदय अथवा कर्म-परिवर्तन का कालखंड सिद्ध करता है。' +
                        '</div>' +
                    '</div>';
                    ndContainer.appendChild(kvDiv);
                }
            }

            // Auto-expand active Venus MD'''

dasha_good = '''            container.innerHTML = html;

            // Auto-expand active Venus MD'''

# Remove from Ashtakavarga
ashtaka_bad = '''            html += '</tbody></table>';

            container.innerHTML = html;

            // Append Nadi Shastric Knowledge Bank
            var ndBox = document.getElementById('nadiKnowledgeVaultBox');
            if (!ndBox) {
                var ndContainer = document.getElementById('view-nadi');
                if (ndContainer) {
                    var kvDiv = document.createElement('div');
                    kvDiv.id = 'nadiKnowledgeVaultBox';
                    kvDiv.style.marginTop = '16px';
                    kvDiv.innerHTML = '<div style="background:var(--bg-card); border:1px solid rgba(168,85,247,0.25); border-left:4px solid #a855f7; border-radius:8px; padding:14px;">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">' +
                            '<b style="color:#a855f7; font-size:0.90rem;">✦ नाड़ी ज्ञान-कोष: भृगु नन्दि नाड़ी सूत्र एवं फलित ग्रन्थ (Nadi Knowledge Bank)</b>' +
                            '<span style="font-size:0.70rem; background:rgba(168,85,247,0.12); color:#a855f7; padding:2px 8px; border-radius:10px; font-weight:700;">भृगु नन्दि नाड़ी • देव केरळम्</span>' +
                        '</div>' +
                        '<div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">' +
                            '• <b>सूत्र १ (त्रिकोण जीव-कारकत्व):</b> <i>"त्रिकोणे गुरु-शनि सम्बन्धात् जीवन-कर्म सिद्धिः"</i> — गुरु (जीवकारक) तथा शनि (कर्मकारक) के 1, 5, 9 त्रिकोण में उपस्थित ग्रह जीवन की वास्तविक दिशा व आजीविका तय करते हैं。<br>' +
                            '• <b>सूत्र २ (द्वि-ग्रह संयोग):</b> गुरु + सूर्य = राजसम्मान व आत्मतेज; शनि + मंगल = तकनीकी, सैन्य व निर्माण कर्म में अभूतपूर्व पुरुषार्थ。<br>' +
                            '• <b>सूत्र ३ (गोचर नाड़ी वेध):</b> गोचरीय गुरु का जन्मकालीन शनि अथवा गुरु के ऊपर से भ्रमण जीवन में सबसे बड़े भाग्योदय अथवा कर्म-परिवर्तन का कालखंड सिद्ध करता है。' +
                        '</div>' +
                    '</div>';
                    ndContainer.appendChild(kvDiv);
                }
            }'''

ashtaka_good = '''            html += '</tbody></table>';

            container.innerHTML = html;'''

print('dasha_bad in c:', dasha_bad in c)
print('ashtaka_bad in c:', ashtaka_bad in c)

c = c.replace(dasha_bad, dasha_good).replace(ashtaka_bad, ashtaka_good)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Cleaned up!')

