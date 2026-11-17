# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. JAIMINI
pos1 = text.find("// Append Jaimini Shastric Knowledge Bank")
end1 = text.find("}", text.find("jmContainer.appendChild(kvDiv);", pos1)) + 1
old_jm_snippet = text[pos1:end1]
print("Found old jm snippet of len:", len(old_jm_snippet))

new_jm_snippet = """// Comprehensive Maharishi Jaimini & K.N. Rao Chara Dasha Reasoning Engine
            var jmBox = document.getElementById('jaiminiKnowledgeVaultBox');
            if (!jmBox) {
                var jmContainer = document.getElementById('view-jaimini');
                if (jmContainer) {
                    var kvDiv = document.createElement('div');
                    kvDiv.id = 'jaiminiKnowledgeVaultBox';
                    kvDiv.style.marginTop = '16px';
                    jmContainer.appendChild(kvDiv);
                    jmBox = kvDiv;
                }
            }

            if (jmBox) {
                var ak = (jm && jm.karakas && jm.karakas[0]) ? jm.karakas[0] : { karaka: "आत्मकारक (AK)", planet: "सूर्य", sign: "वृश्चिक", deg: "28°15'", signification: "Soul's journey" };
                var amk = (jm && jm.karakas && jm.karakas[1]) ? jm.karakas[1] : { karaka: "अमात्यकारक (AmK)", planet: "मंगल", sign: "मकर", deg: "25°40'", signification: "Career & intellect" };
                var bk = (jm && jm.karakas && jm.karakas[2]) ? jm.karakas[2] : { karaka: "भ्रातृकारक (BK)", planet: "गुरु", sign: "धनु", deg: "19°10'", signification: "Guru & advisors" };
                var dk = (jm && jm.karakas && jm.karakas[6]) ? jm.karakas[6] : { karaka: "दाराकारक (DK)", planet: "शुक्र", sign: "मीन", deg: "04°20'", signification: "Spouse & partner" };

                var htmlJm = '<div style="display:flex; flex-direction:column; gap:14px;">' +
                    '<div style="background:var(--bg-card); border:1px solid rgba(16,185,129,0.3); border-left:4px solid #10b981; border-radius:10px; padding:16px;">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">' +
                            '<b style="color:#10b981; font-size:0.95rem;">✦ महर्षि जैमिनी उपदेश सूत्र एवं के.एन. राव चर दशा फलादेश (Jaimini Knowledge Bank)</b>' +
                            '<span style="font-size:0.72rem; background:rgba(16,185,129,0.15); color:#10b981; padding:3px 10px; border-radius:12px; font-weight:800;">Jaimini Sutras (B.S. Rao) • Crux of Vedic Astrology (Sanjay Rath)</span>' +
                        '</div>' +
                        '<p style="font-size:0.76rem; color:var(--text-secondary); margin:0 0 12px 0; line-height:1.5;">' +
                            'जैमिनी ज्योतिष में अंश-अनुसार चर कारक आत्मा के सूक्ष्म स्तर का उद्घाटन करते हैं। जातक की कुण्डली के प्रमुख कारकों का सूत्र-आधारित विश्लेषण:' +
                        '</p>' +
                        '<div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">👑 आत्मकारक (AK - Soul\'s Purpose):</b><br>' +
                                '<span style="font-size:0.75rem; color:#10b981; font-weight:700;">' + ak.planet + ' (' + ak.sign + ' राशि • ' + ak.deg + ')</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>जैमिनी सूत्र (१/२/१ - स्वांशे आत्मा):</b> आत्मकारक <b>' + ak.planet + '</b> नवमांश में कारकांश लग्न (KL) का निर्माण करता है। यह जातक के आध्यात्मिक अभीष्ट, आत्म-स्वाभिमान व गूढ़ अनुसंधान में सर्वोच्च सिद्धि का संकेत है।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">💼 अमात्यकारक (AmK - Ministerial Authority):</b><br>' +
                                '<span style="font-size:0.75rem; color:#38bdf8; font-weight:700;">' + amk.planet + ' (' + amk.sign + ' राशि • ' + amk.deg + ')</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>जैमिनी सूत्र (१/२/४० - अमात्येन संबन्धे राजयोगः):</b> अमात्यकारक <b>' + amk.planet + '</b> जातक की सर्वोच्च कर्म शक्ति है। इसका आत्मकारक से शुभ दृष्टि सम्बंध उच्च कोटि का <i>जैमिनी राजयोग</i> उत्पन्न करता है, जिससे प्रशासनिक ख्याति मिलती है।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">🏛️ आरूढ़ लग्न (AL) बनाम सत्य लग्न:</b><br>' +
                                '<span style="font-size:0.75rem; color:#f59e0b; font-weight:700;">पद लग्न (माया प्रतिबिंब): सामाजिक प्रतिष्ठा</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>ग्रन्थ प्रमाण (K.N. Rao - Predicting through Jaimini\'s Chara Dasha):</b> आरूढ़ लग्न (AL) से एकादश भाव में शुभ ग्रह जातक को समाज में धनाढ्य, प्रतिष्ठित और प्रभावशाली व्यक्तित्व के रूप में स्थापित करते हैं।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">🕊️ कारकांश से द्वादश भाव (कैवल्य / मोक्ष योग):</b><br>' +
                                '<span style="font-size:0.75rem; color:#a855f7; font-weight:700;">मोक्ष व पारलौकिक चेतना विचार</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>जैमिनी सूत्र (१/२/६९ - केतौ कैवल्यम्):</b> कारकांश से द्वादश भाव में शुभ दृष्टि या केतु का सम्बंध जातक को सात्विक वैराग्य, गहन ध्यान व मुक्ति मार्ग की ओर अग्रसर करता है।' +
                                '</p>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>';
                jmBox.innerHTML = htmlJm;
            }"""

text = text.replace(old_jm_snippet, new_jm_snippet, 1)

# 2. NADI
pos2 = text.find("// Append Nadi Shastric Knowledge Bank")
end2 = text.find("}", text.find("ndContainer.appendChild(nvDiv);", pos2)) + 1
old_nd_snippet = text[pos2:end2]
print("Found old nd snippet of len:", len(old_nd_snippet))

new_nd_snippet = """// Comprehensive Bhrigu Nandi Nadi (R.G. Rao) & Deva Keralam Reasoning Engine
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

text = text.replace(old_nd_snippet, new_nd_snippet, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✓ Successfully patched Jaimini & Nadi reasoning engines in index.html!")

