# -*- coding: utf-8 -*-
"""
Auditor script to embed static Treatise Knowledge Banks from ayushman1024/ASTROLOGY-BOOKS-DATABASE
directly into HTML for:
1. view-predictions (Vedic: BPHS, Phaladeepika, Sarvartha Chintamani, 300 Combinations)
2. view-kp (KP: Readers 1-6, Baskaran CIT, Khullar KCIL, 4-Step Theory)
3. view-jaimini (Jaimini: Upadesha Sutras, KN Rao Chara Dasha, Rangacharya)
4. view-nadi (Nadi: BNN RG Rao, Deva Keralam Chandra Kala Nadi, BSP Rules)

Also updates JS in renderKP(), renderJaimini(), renderNadi(), and renderPredictions()
to never bail out on early returns, updating spans dynamically when charts load!
"""

import sys

def run_patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # -------------------------------------------------------------
    # 1. STATIC HTML INJECTION IN view-predictions
    # -------------------------------------------------------------
    vedic_card_html = """
                    <!-- VEDIC SHASTRA KNOWLEDGE BANK & TREATISES (Brihat Parashara & Classical Treatises) -->
                    <div class="content-card" id="vedicKnowledgeVaultBox" style="margin-top:16px; border:1px solid rgba(217,119,6,0.3); border-left:4px solid #d97706; background:var(--bg-card); border-radius:8px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <b style="color:#d97706; font-size:0.92rem;">✦ वैदिक शास्त्र ज्ञान-कोष: बृहत् पराशर एवं प्रामाणिक क्लासिकल ग्रन्थ वेध</b>
                            <span style="font-size:0.70rem; background:rgba(217,119,6,0.12); color:#d97706; padding:2px 8px; border-radius:10px; font-weight:700;">BPHS • फलदीपिका • सर्वार्थ चिन्तामणि • 300 कॉम्बिनेशन्स</span>
                        </div>
                        <div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">
                            <div style="margin-bottom:8px; padding:8px; background:rgba(217,119,6,0.05); border-radius:6px;">
                                <b style="color:#d97706;">1. भाव-भावेश-कारक त्रिसूत्री मीमांसा (सर्वार्थ चिन्तामणि - व्यंकटेश शर्मा, अध्याय 2-5):</b><br>
                                <span id="vedicTriSutraReasoning">क्लासिकल सिद्धांत के अनुसार किसी भी भाव का फल केवल उस भाव में बैठे ग्रह से तय नहीं होता। (1) <b>भाव की स्थिति</b> (शुभ/पाप कर्तरी), (2) <b>भावेश का बल व स्थान</b> (केन्द्र/त्रिकोण अथवा त्रिक 6, 8, 12), तथा (3) <b>स्थिर कारक का बल</b> — जब तीनों का समवेत आकलन होता है तभी यथार्थ फल घटित होता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(217,119,6,0.05); border-radius:6px;">
                                <b style="color:#d97706;">2. राजयोग एवं फल प्राप्ति समय (बृहत् पराशर होरा शास्त्र अध्याय 34 व 41):</b><br>
                                <span id="vedicYogaTimingReasoning">केन्द्र (1, 4, 7, 10 - भगवान विष्णु) और त्रिकोण (1, 5, 9 - माँ लक्ष्मी) के स्वामियों का युति, दृष्टि अथवा राशि परिवर्तन योग 'लक्ष्मी-नारायण राजयोग' बनाता है। इसका पूर्ण फल योगकारक ग्रहों की विंशोत्तरी महादशा एवं अन्तर्दशा में ही प्राप्त होता है। दशा के बिना कुण्डली में स्थित योग निष्क्रिय बीज समान रहता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(217,119,6,0.05); border-radius:6px;">
                                <b style="color:#d97706;">3. गोचर वेध व अष्टकवर्ग समन्वय (फलदीपिका अध्याय 20 व 24 - मन्त्रेश्वर):</b><br>
                                <span id="vedicGocharReasoning">गोचरस्थ ग्रह तभी अपना शुभ फल दे पाते हैं जब संबंधित भाव में सर्वाष्टकवर्ग (SAV) के 28 से अधिक शुभ बिन्दु हों और तात्कालिक विंशोत्तरी दशा उस फल का समर्थन कर रही हो। दशा फल का वचन देती है और अनुकूल गोचर उस फल को प्रत्यक्ष जीवन में प्रकट करता है।</span>
                            </div>
                            <div style="margin-top:10px; font-size:0.72rem; color:var(--text-muted); border-top:1px solid rgba(217,119,6,0.15); padding-top:6px; display:flex; flex-wrap:wrap; gap:8px;">
                                <span>📚 <b>ग्रन्थ आधार:</b></span>
                                <span>• Brihat Parashara Hora Shastra (Santhanam Vol 1-2)</span>
                                <span>• Phaladeepika (Mantreshwara)</span>
                                <span>• Sarvartha Chintamani (B. Suryanarain Rao)</span>
                                <span>• 300 Important Combinations (Dr. B.V. Raman)</span>
                            </div>
                        </div>
                    </div>"""

    target_pred = '<div id="yogasAndDoshasBox" style="font-size:0.78rem; line-height:1.6;">\n                            <!-- Populated by JS -->\n                        </div>\n                    </div>\n                </div>'
    if target_pred in html and 'id="vedicKnowledgeVaultBox"' not in html:
        replacement_pred = '<div id="yogasAndDoshasBox" style="font-size:0.78rem; line-height:1.6;">\n                            <!-- Populated by JS -->\n                        </div>\n                    </div>' + vedic_card_html + '\n                </div>'
        html = html.replace(target_pred, replacement_pred, 1)
        print("✓ Embedded static Vedic Knowledge Vault in view-predictions")
    else:
        print("Notice: view-predictions target already patched or not found")

    # -------------------------------------------------------------
    # 2. STATIC HTML INJECTION IN view-kp
    # -------------------------------------------------------------
    kp_card_html = """
                    <!-- KP SHASTRA KNOWLEDGE BANK & TREATISES (KP Readers 1-6 & Cuspal Interlinks) -->
                    <div class="content-card" id="kpKnowledgeVaultBox" style="margin-top:16px; border:1px solid rgba(245,158,11,0.3); border-left:4px solid #f59e0b; background:var(--bg-card); border-radius:8px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <b style="color:#f59e0b; font-size:0.92rem;">✦ केपी ज्ञान-कोष: प्रो. के.एस. कृष्णमूर्ति कस्पल सब-लॉर्ड ग्रन्थ वेध</b>
                            <span style="font-size:0.70rem; background:rgba(245,158,11,0.12); color:#f59e0b; padding:2px 8px; border-radius:10px; font-weight:700;">KP Readers 1-6 • Baskaran CIT • Khullar KCIL • 4-Step Theory</span>
                        </div>
                        <div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">
                            <div style="margin-bottom:8px; padding:8px; background:rgba(245,158,11,0.05); border-radius:6px;">
                                <b style="color:#f59e0b;">1. दशम भाव कस्पल सब-लॉर्ड (10th CSL) - आजीविका, पद-प्रतिष्ठा व व्यवसाय:</b><br>
                                <span id="kpCsl10Val"><b>नियम (KP Reader 3 & CIT):</b> दशम भाव का कस्पल उप-स्वामी यदि 2, 6, 10, 11 भावों के नक्षत्र या उप-नक्षत्र में हो, तो जातक को स्वतंत्र व्यवसाय, उच्च पद अथवा सरकारी सेवा में स्थायी सफलता मिलती है। 5, 8, 12 भावों का सम्बंध रुकावट या परिवर्तन का संकेत देता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(245,158,11,0.05); border-radius:6px;">
                                <b style="color:#f59e0b;">2. सप्तम भाव कस्पल सब-लॉर्ड (7th CSL) - विवाह, साझेदारी व दांपत्य:</b><br>
                                <span id="kpCsl7Val"><b>नियम (KP Reader 4 Ch. 2):</b> सप्तम कस्पल सब-लॉर्ड 2, 7, 11 भावों का कार्येश (Significator) बनकर विवाह व लाभकारी अनुबंध सुनिश्चित करता है। यदि यह 1, 6, 10 से सम्बद्ध हो, तो वैवाहिक विलम्ब अथवा स्वतंत्र एकाकी जीवन का संकेत देता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(245,158,11,0.05); border-radius:6px;">
                                <b style="color:#f59e0b;">3. द्वितीय व एकादश कस्पल सब-लॉर्ड (2nd & 11th CSL) - धन संग्रह व अभीष्ट सिद्धि:</b><br>
                                <span id="kpCsl2Val"><b>नियम (Baskaran Cuspal Interlinks):</b> द्वितीय कस्पल सब-लॉर्ड धन संचय (Wealth Accumulation) तथा एकादश कस्पल सब-लॉर्ड इच्छा पूर्ति (Fulfillment of Desires) का निर्धारक है। 2-11 का परस्पर सम्बंध प्रचुर धन सम्पदा प्रदान करता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(245,158,11,0.05); border-radius:6px;">
                                <b style="color:#f59e0b;">4. प्रथम कस्पल सब-लॉर्ड (1st CSL) - स्वास्थ्य, दीर्घायु व मनोबल:</b><br>
                                <span id="kpCsl1Val"><b>नियम (KP Reader 3):</b> लग्न का कस्पल सब-लॉर्ड यदि बाधक अथवा मारक भावों (11/7/2) का उप-स्वामी न हो और 1, 3, 9, 11 से जुड़े, तो जातक दीर्घायु, निरोगी और तीव्र इच्छाशक्ति संपन्न होता है।</span>
                            </div>
                            <div style="margin-top:10px; font-size:0.72rem; color:var(--text-muted); border-top:1px solid rgba(245,158,11,0.15); padding-top:6px; display:flex; flex-wrap:wrap; gap:8px;">
                                <span>📚 <b>ग्रन्थ आधार:</b></span>
                                <span>• KP Readers Vol 1-6 (Prof. K.S. Krishnamurti)</span>
                                <span>• Applications of Cuspal Interlinks Part 1 (K. Baskaran)</span>
                                <span>• Kalamsa and Cuspal Interlinks (S.P. Khullar)</span>
                                <span>• 4 Step Theory in Stellar Astrology</span>
                            </div>
                        </div>
                    </div>"""

    target_kp = '<tbody id="kpPlanetsTableBody">\n                                <!-- Populated by JS -->\n                            </tbody>\n                        </table>\n                    </div>\n                </div>'
    if target_kp in html and 'id="kpKnowledgeVaultBox"' not in html:
        replacement_kp = '<tbody id="kpPlanetsTableBody">\n                                <!-- Populated by JS -->\n                            </tbody>\n                        </table>\n                    </div>' + kp_card_html + '\n                </div>'
        html = html.replace(target_kp, replacement_kp, 1)
        print("✓ Embedded static KP Knowledge Vault in view-kp")
    else:
        print("Notice: view-kp target already patched or not found")

    # -------------------------------------------------------------
    # 3. STATIC HTML INJECTION IN view-jaimini
    # -------------------------------------------------------------
    jaimini_card_html = """
                    <!-- JAIMINI SHASTRA KNOWLEDGE BANK & TREATISES (Upadesha Sutras & KN Rao Chara Dasha) -->
                    <div class="content-card" id="jaiminiKnowledgeVaultBox" style="margin-top:16px; border:1px solid rgba(16,185,129,0.3); border-left:4px solid #10b981; background:var(--bg-card); border-radius:8px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <b style="color:#10b981; font-size:0.92rem;">✦ जैमिनी ज्ञान-कोष: महर्षि जैमिनी उपदेश सूत्र एवं चर दशा वेध</b>
                            <span style="font-size:0.70rem; background:rgba(16,185,129,0.12); color:#10b981; padding:2px 8px; border-radius:10px; font-weight:700;">Jaimini Upadesha Sutras • Dr. K.N. Rao Chara Dasha • Rangacharya</span>
                        </div>
                        <div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">
                            <div style="margin-bottom:8px; padding:8px; background:rgba(16,185,129,0.05); border-radius:6px;">
                                <b style="color:#10b981;">1. आत्मकारक (AK) एवं कारकांश लग्न (KL) - आत्मा का मूल उद्देश्य (Upadesha Sutras 1.1.11 व 1.2.1):</b><br>
                                <span id="jmAkVal">कुण्डली में सर्वाधिक अंश भोगने वाला ग्रह <b>आत्मकारक (AK)</b> बनता है। नवमांश कुण्डली (D-9) में आत्मकारक जिस राशि में स्थित होता है, वह <b>कारकांश लग्न (KL)</b> कहलाता है। कारकांश लग्न से जातक के आंतरिक स्वभाव, प्रतिभा तथा आध्यात्मिक मुक्ति का साक्षात दर्शन होता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(16,185,129,0.05); border-radius:6px;">
                                <b style="color:#10b981;">2. अमात्यकारक (AmK) - करियर व आर्थिक सामर्थ्य (Dr. K.N. Rao Chara Dasha):</b><br>
                                <span id="jmAmkVal">द्वितीय सर्वाधिक अंश वाला ग्रह <b>अमात्यकारक (AmK)</b> होता है। जैमिनी सिद्धांत में AmK जातक के कर्म, पद और मंत्रीत्व का कारक है। यदि AK और AmK का 1, 5, 9, 10वें भाव में परस्पर सम्बंध बने तो व्यक्ति उच्चाधिकारी या शीर्ष नेतृत्वकर्ता बनता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(16,185,129,0.05); border-radius:6px;">
                                <b style="color:#10b981;">3. दाराकारक (DK) व उपपद आरूढ़ (UL) - दांपत्य व सम्बंध (Upadesha Sutras 1.4.1):</b><br>
                                <span id="jmDkVal">न्यूनतम अंश वाला ग्रह <b>दाराकारक (DK)</b> जीवनसाथी का स्वरूप निर्धारित करता है। द्वादश भाव का आरूढ़ पद <b>उपपद (UL)</b> विवाह की स्थिरता दर्शाता है। उपपद से द्वितीय भाव में शुभ ग्रह होने पर दांपत्य जीवन सुदृढ़ एवं समृद्ध रहता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(16,185,129,0.05); border-radius:6px;">
                                <b style="color:#10b981;">4. कारकांश से 12वां भाव - मोक्ष व आध्यात्मिक मुक्ति (Sutra 1.2.69):</b><br>
                                <span id="jmMokshaVal">कारकांश लग्न से द्वादश भाव में केतु अथवा बृहस्पति की उपस्थिति या दृष्टि जातक को इस जन्म के उपरांत परम मोक्ष (कैवल्य) की ओर अग्रसर करती है।</span>
                            </div>
                            <div style="margin-top:10px; font-size:0.72rem; color:var(--text-muted); border-top:1px solid rgba(16,185,129,0.15); padding-top:6px; display:flex; flex-wrap:wrap; gap:8px;">
                                <span>📚 <b>ग्रन्थ आधार:</b></span>
                                <span>• Jaimini Maharishi's Upadesa Sutras</span>
                                <span>• Predicting Through Jaimini's Chara Dasha (Dr. K.N. Rao)</span>
                                <span>• A Manual of Jaimini Astrology (Iranganti Rangacharya)</span>
                                <span>• The Significance of Jaimini Karakas</span>
                            </div>
                        </div>
                    </div>"""

    target_jm = 'A2): <b>कन्या राशि</b> • कर्म आरूढ़ (A10): <b>कर्क राशि</b>\n                                </div>\n                            </div>\n                        </div>\n                    </div>\n                </div>'
    if target_jm in html and 'id="jaiminiKnowledgeVaultBox"' not in html:
        replacement_jm = 'A2): <b>कन्या राशि</b> • कर्म आरूढ़ (A10): <b>कर्क राशि</b>\n                                </div>\n                            </div>\n                        </div>\n                    </div>' + jaimini_card_html + '\n                </div>'
        html = html.replace(target_jm, replacement_jm, 1)
        print("✓ Embedded static Jaimini Knowledge Vault in view-jaimini")
    else:
        print("Notice: view-jaimini target already patched or not found")

    # -------------------------------------------------------------
    # 4. STATIC HTML INJECTION IN view-nadi
    # -------------------------------------------------------------
    nadi_card_html = """
                    <!-- NADI SHASTRA KNOWLEDGE BANK & TREATISES (Bhrigu Nandi Nadi & Deva Keralam) -->
                    <div class="content-card" id="nadiKnowledgeVaultBox" style="margin-top:16px; border:1px solid rgba(59,130,246,0.3); border-left:4px solid #3b82f6; background:var(--bg-card); border-radius:8px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <b style="color:#3b82f6; font-size:0.92rem;">✦ नाड़ी ज्ञान-कोष: भृगु नंदी नाड़ी, चन्द्र कला नाड़ी एवं BSP नियम</b>
                            <span style="font-size:0.70rem; background:rgba(59,130,246,0.12); color:#3b82f6; padding:2px 8px; border-radius:10px; font-weight:700;">R.G. Rao BNN • Deva Keralam • Bhrigu Saral Paddhati • Meena Nadi</span>
                        </div>
                        <div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">
                            <div style="margin-bottom:8px; padding:8px; background:rgba(59,130,246,0.05); border-radius:6px;">
                                <b style="color:#3b82f6;">1. जीव-कर्म नाड़ी संगम (गुरु-शनि सम्बंध - R.G. Rao BNN):</b><br>
                                <span id="nadiJeevaKarmaVal">नाड़ी ज्योतिष में <b>बृहस्पति (गुरु) जीव कारक</b> है और <b>शनि कर्म कारक</b> है। गुरु और शनि का त्रिकोणीय (1-5-9) अथवा 2-12 सम्बंध जातक के जीवन उद्देश्य और कर्मक्षेत्र को एक दूसरे से सम्बद्ध करता है। यह योग जातक को समाजोपयोगी, प्रतिष्ठित तथा नैतिक कर्मों में प्रतिष्ठा दिलाता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(59,130,246,0.05); border-radius:6px;">
                                <b style="color:#3b82f6;">2. दिक-त्रिकोण संयोजन (Directional Conjunctions - 1-5-9 Trines):</b><br>
                                <span id="nadiDirectionalVal">नाड़ी में ग्रह जिस दिशा (पूर्व, दक्षिण, पश्चिम, उत्तर) में स्थित होते हैं, उसी दिशा के अन्य ग्रहों के साथ युति बनाते हैं। अग्नि त्रिकोण (1, 5, 9) आत्म-चेतना व धर्म, पृथ्वी त्रिकोण (2, 6, 10) अर्थ व कर्म, वायु त्रिकोण (3, 7, 11) संबंध व इच्छा, तथा जल त्रिकोण (4, 8, 12) अंतर्ज्ञान व मोक्ष का नियमन करते हैं।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(59,130,246,0.05); border-radius:6px;">
                                <b style="color:#3b82f6;">3. राहु-केतु कार्मिक अक्ष (Karmic Nodes Axis in BNN):</b><br>
                                <span id="nadiKarmicVal"><b>राहु</b> पूर्वजन्म के अवशिष्ट भोग व भौतिक आकर्षण का द्योतक है, जबकि <b>केतु</b> पूर्वजन्म के संचित ज्ञान, त्याग और मोक्ष का प्रतीक है। जिस ग्रह के आगे केतु स्थित होता है, वह ग्रह भौतिक स्तर पर विरक्ति और आध्यात्मिक स्तर पर पराकाष्ठा प्रदान करता है।</span>
                            </div>
                            <div style="margin-bottom:8px; padding:8px; background:rgba(59,130,246,0.05); border-radius:6px;">
                                <b style="color:#3b82f6;">4. देव केरलम् (चन्द्र कला नाड़ी) गोचर वेध:</b><br>
                                <span id="nadiGocharaVal">नाड़ी अंशों पर जब शनि या गुरु का गोचर होता है, तब जीवन में युगांतरकारी मोड़ (Karmic Turning Points) आते हैं। गोचरस्थ गुरु जब जन्मकालीन चन्द्रमा या शुक्र पर दृष्टि डालता है, तब वैवाहिक व आर्थिक विस्तार घटित होता है।</span>
                            </div>
                            <div style="margin-top:10px; font-size:0.72rem; color:var(--text-muted); border-top:1px solid rgba(59,130,246,0.15); padding-top:6px; display:flex; flex-wrap:wrap; gap:8px;">
                                <span>📚 <b>ग्रन्थ आधार:</b></span>
                                <span>• Bhrigu Nandi Nadi (R.G. Rao)</span>
                                <span>• Deva Keralam / Chandra Kala Nadi (Achyuta & Venkatesha)</span>
                                <span>• Bhrigu Saral Paddhati (BSP) 35 Rules</span>
                                <span>• Meena Nadi Part 1</span>
                            </div>
                        </div>
                    </div>"""

    target_nadi = '<div id="nadiCombinationsContainer" style="display:flex; flex-direction:column; gap:8px;">\n                            <!-- Populated by JS -->\n                        </div>\n                    </div>\n                </div>'
    if target_nadi in html and 'id="nadiKnowledgeVaultBox"' not in html:
        replacement_nadi = '<div id="nadiCombinationsContainer" style="display:flex; flex-direction:column; gap:8px;">\n                            <!-- Populated by JS -->\n                        </div>\n                    </div>' + nadi_card_html + '\n                </div>'
        html = html.replace(target_nadi, replacement_nadi, 1)
        print("✓ Embedded static Nadi Knowledge Vault in view-nadi")
    else:
        print("Notice: view-nadi target already patched or not found")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Step 1 HTML injection complete.")

if __name__ == '__main__':
    run_patch()

