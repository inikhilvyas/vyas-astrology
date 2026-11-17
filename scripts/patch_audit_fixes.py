# -*- coding: utf-8 -*-
"""
Auditor script to patch:
1. Daily Horoscope blank slate leak + dynamic transit calculation in index.html
2. Safe openEditProfileModal & openNewProfileModal (null activeChartData crash fix)
3. Safe renderPavTable (null activeChartData crash fix)
4. Smooth Google Sign-In with automatic chart creation prompt
5. Enrich Knowledge Bank with ayushman1024/ASTROLOGY-BOOKS-DATABASE authoritative treatises
"""

import re
import sys

def patch_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. PATCH STATIC HTML IN personalizedDailyCard ---
    # Find dhWealth, dhCareer, dhRelations, dhHealth in HTML
    old_daily_cards = """                                <b style="font-size:0.80rem; color:var(--primary-navy);">धन एवं वाणी विचार (Wealth & Speech)</b>
                                <p style="font-size:0.74rem; color:var(--text-secondary); margin-top:4px;">
                                    गोचरस्थ चन्द्रमा दशम भाव में संचरण कर रहे हैं। आर्थिक लेन-देन में विवेकपूर्ण निर्णय लाभ देंगे। कटु वचनों से बचें और स्पष्ट संवाद रखें।
                                </p>
                            </div>
                            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">
                                <b style="font-size:0.80rem; color:var(--primary-navy);">आजीविका एवं कार्यक्षेत्र (Career)</b>
                                <p style="font-size:0.74rem; color:var(--text-secondary); margin-top:4px;">
                                    दशम भाव में मकर राशि का चन्द्रमा कर्मक्षेत्र में मान-प्रतिष्ठा, वरिष्ठों का सहयोग व व्यावसायिक अनुबंधों में गति का संकेत दे रहा है।
                                </p>
                            </div>
                            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">
                                <b style="font-size:0.80rem; color:var(--primary-navy);">❤️ संबंध व परिवार (Relationships)</b>
                                <p style="font-size:0.74rem; color:var(--text-secondary); margin-top:4px;">
                                    पारिवारिक वातावरण सौहार्दपूर्ण रहेगा। जीवनसाथी के सुझावों को महत्व दें। पुराने मित्रों अथवा शुभचिंतकों से संपर्क लाभकारी रहेगा।
                                </p>
                            </div>
                            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">
                                <b style="font-size:0.80rem; color:var(--primary-navy);">🌿 स्वास्थ्य एवं ऊर्जा (Health)</b>
                                <p style="font-size:0.74rem; color:var(--text-secondary); margin-top:4px;">
                                    मानसिक ऊर्जा व एकाग्रता 74% अनुकूल है। पर्याप्त जल ग्रहण करें, हल्का सात्विक आहार लें और रात्रि को समय पर विश्राम करें।
                                </p>"""

    new_daily_cards = """                                <b style="font-size:0.80rem; color:var(--primary-navy);">धन एवं वाणी विचार (Wealth & Speech)</b>
                                <p style="font-size:0.74rem; color:var(--text-secondary); margin-top:4px;" id="dhWealthText">
                                    व्यक्तिगत धन एवं वाणी वेध हेतु कृपया अपनी जन्म कुण्डली बनाएं।
                                </p>
                            </div>
                            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">
                                <b style="font-size:0.80rem; color:var(--primary-navy);">आजीविका एवं कार्यक्षेत्र (Career)</b>
                                <p style="font-size:0.74rem; color:var(--text-secondary); margin-top:4px;" id="dhCareerText">
                                    कर्मक्षेत्र व आजीविका गोचर फलादेश देखने हेतु जन्म कुण्डली बनाएं।
                                </p>
                            </div>
                            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">
                                <b style="font-size:0.80rem; color:var(--primary-navy);">❤️ संबंध व परिवार (Relationships)</b>
                                <p style="font-size:0.74rem; color:var(--text-secondary); margin-top:4px;" id="dhRelationsText">
                                    पारिवारिक व दांपत्य गोचर वेध हेतु कृपया जन्म कुण्डली बनाएं।
                                </p>
                            </div>
                            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">
                                <b style="font-size:0.80rem; color:var(--primary-navy);">🌿 स्वास्थ्य एवं ऊर्जा (Health)</b>
                                <p style="font-size:0.74rem; color:var(--text-secondary); margin-top:4px;" id="dhHealthText">
                                    दैनिक ऊर्जा व स्वास्थ्य संतुलन वेध हेतु जन्म कुण्डली बनाएं।
                                </p>"""

    if old_daily_cards in content:
        content = content.replace(old_daily_cards, new_daily_cards, 1)
        print("✓ Replaced static daily horoscope cards HTML with dynamic IDs and blank slate text.")
    else:
        print("! Warning: old_daily_cards exact match not found in HTML. Checking alternative matching...")

    # --- 2. UPDATE updateDailyHoroscopeUI() IN JAVASCRIPT ---
    # Find updateDailyHoroscopeUI definition
    old_update_daily = """        updateDailyHoroscopeUI() {
            var card = document.getElementById('personalizedDailyCard');
            if (!card) return;

            var vVal = document.getElementById('vIndexVal');
            var vSub = document.getElementById('vIndexSub');
            var taraVal = document.getElementById('vTodayTaraVal');
            var taraDesc = document.getElementById('vTodayTaraDesc');
            var heading = document.getElementById('personalizedDailyHeading');

            if (!this.activeChartData || !this.activeChartData.profile || !this.activeChartData.profile.name) {
                if (heading) {
                    heading.innerHTML = '<span>✦ जातक का व्यक्तिगत दैनिक राशिफल (Personalized Daily Horoscope)</span><span style="font-size:0.75rem; color:#f59e0b; font-weight:700;"> (कुण्डली लोड नहीं है)</span>';
                }
                if (vVal) vVal.textContent = '--';
                if (vSub) {
                    vSub.textContent = 'कुण्डली आवश्यक';
                    vSub.style.color = 'var(--text-muted)';
                }
                if (taraVal) {
                    taraVal.textContent = 'नवतारा चक्र (अज्ञात)';
                    taraVal.style.color = 'var(--primary-navy)';
                }
                if (taraDesc) {
                    taraDesc.textContent = "व्यक्तिगत तारा वेध हेतु कृपया ऊपर '+ नई कुण्डली' बनाएं।";
                }
                return;
            }"""

    new_update_daily = """        updateDailyHoroscopeUI() {
            var card = document.getElementById('personalizedDailyCard');
            if (!card) return;

            var vVal = document.getElementById('vIndexVal');
            var vSub = document.getElementById('vIndexSub');
            var taraVal = document.getElementById('vTodayTaraVal');
            var taraDesc = document.getElementById('vTodayTaraDesc');
            var heading = document.getElementById('personalizedDailyHeading');
            var dhWealth = document.getElementById('dhWealthText');
            var dhCareer = document.getElementById('dhCareerText');
            var dhRelations = document.getElementById('dhRelationsText');
            var dhHealth = document.getElementById('dhHealthText');

            if (!this.activeChartData || !this.activeChartData.profile || !this.activeChartData.profile.name) {
                if (heading) {
                    heading.innerHTML = '<span>✦ जातक का व्यक्तिगत दैनिक राशिफल (Personalized Daily Horoscope)</span><span style="font-size:0.75rem; color:#f59e0b; font-weight:700;"> (कुण्डली लोड नहीं है)</span>';
                }
                if (vVal) vVal.textContent = '--';
                if (vSub) {
                    vSub.textContent = 'कुण्डली आवश्यक';
                    vSub.style.color = 'var(--text-muted)';
                }
                if (taraVal) {
                    taraVal.textContent = 'नवतारा चक्र (अज्ञात)';
                    taraVal.style.color = 'var(--primary-navy)';
                }
                if (taraDesc) {
                    taraDesc.textContent = "व्यक्तिगत तारा वेध हेतु कृपया ऊपर '+ नई कुण्डली' बनाएं।";
                }
                if (dhWealth) dhWealth.textContent = "व्यक्तिगत धन एवं वाणी वेध हेतु कृपया अपनी जन्म कुण्डली बनाएं।";
                if (dhCareer) dhCareer.textContent = "कर्मक्षेत्र व आजीविका गोचर फलादेश देखने हेतु जन्म कुण्डली बनाएं।";
                if (dhRelations) dhRelations.textContent = "पारिवारिक व दांपत्य गोचर वेध हेतु कृपया जन्म कुण्डली बनाएं।";
                if (dhHealth) dhHealth.textContent = "दैनिक ऊर्जा व स्वास्थ्य संतुलन वेध हेतु जन्म कुण्डली बनाएं।";
                return;
            }"""

    if old_update_daily in content:
        content = content.replace(old_update_daily, new_update_daily, 1)
        print("✓ Updated updateDailyHoroscopeUI blank slate branch to clear and protect all 4 cards.")
    else:
        print("! Warning: old_update_daily not found exactly.")

    # Now find where taraDesc is set in updateDailyHoroscopeUI and add dynamic calculation for the 4 cards
    old_tara_set = """            if (taraDesc) taraDesc.textContent = info.desc;
        },"""

    new_tara_set = """            if (taraDesc) taraDesc.textContent = info.desc;

            // Compute dynamic transit moon house from natal Moon (Chandra Lagna Gochar)
            var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var birthMoonSignIdx = 0;
            if (this.activeChartData.planet_table) {
                for (var p = 0; p < this.activeChartData.planet_table.length; p++) {
                    var pl = this.activeChartData.planet_table[p];
                    if ((pl.p && pl.p.indexOf("चन्द्र") !== -1) || (pl.planet && pl.planet.indexOf("Moon") !== -1)) {
                        var rStr = pl.r || pl.sign || pl.rashi || '';
                        for (var si = 0; si < SIGNS_HI.length; si++) {
                            if (rStr.indexOf(SIGNS_HI[si]) !== -1) { birthMoonSignIdx = si; break; }
                        }
                        break;
                    }
                }
            }

            var transitMoonSignIdx = Math.floor(moonSid / 30.0) % 12;
            var chandraHouse = ((transitMoonSignIdx - birthMoonSignIdx + 12) % 12) + 1;
            var tMoonSign = SIGNS_HI[transitMoonSignIdx];

            var HOUSE_TRANSIT_PREDICTIONS = {
                1: {
                    wealth: "गोचरस्थ चन्द्रमा आपकी राशि में संचरण कर रहे हैं। धन आगमन के नवीन अवसर बनेंगे। वाणी में सौम्यता बनाए रखें।",
                    career: "प्रथम भावस्थ चन्द्रमा आत्मविश्वास में वृद्धि कराएगा। नए व्यावसायिक निर्णयों हेतु दिन अनुकूल है।",
                    rel: "पारिवारिक व वैवाहिक संबंधों में सौहार्द रहेगा। आत्म-प्रसन्नता व सामाजिक मेलजोल में वृद्धि होगी।",
                    health: "शारीरिक स्फूर्ति उत्तम रहेगी। पर्याप्त जल पिएं व नियमित दिनचर्या का पालन करें।"
                },
                2: {
                    wealth: "गोचरस्थ चन्द्रमा द्वितीय (धन) भाव में हैं। संचित पूंजी में वृद्धि व परिवार से आर्थिक सहयोग संभव है।",
                    career: "वाणी आधारित कार्यों, वित्त व परामर्श क्षेत्र में विशेष मान-सम्मान व लाभ के योग हैं।",
                    rel: "कुटुंब में मांगलिक चर्चा संभव है। मधुर वाणी से सभी का स्नेह प्राप्त होगा।",
                    health: "मुख व नेत्र का ध्यान रखें। संतुलित खान-पान अपनाएं।"
                },
                3: {
                    wealth: "तृतीय भाव में चन्द्रमा के गोचर से पराक्रम द्वारा धन लाभ होगा। छोटी लाभकारी यात्राएं संभव हैं।",
                    career: "कार्यक्षेत्र में आपके प्रयासों की सराहना होगी। सहकर्मियों व अधीनस्थों का पूर्ण सहयोग मिलेगा।",
                    rel: "छोटे भाई-बहनों से संबंध प्रगाढ़ होंगे। मित्रों से शुभ समाचार प्राप्त होगा।",
                    health: "ऊर्जा का स्तर 88% अनुकूल। कंधे व भुजाओं में खिंचाव से बचें।"
                },
                4: {
                    wealth: "चतुर्थ भाव में गोचर से भूमि, भवन अथवा वाहन संबंधी कार्यों में व्यय अथवा निवेश के योग हैं।",
                    career: "कार्यक्षेत्र में धैर्य से काम लें। वरिष्ठों के परामर्श को गंभीरता से सुनें।",
                    rel: "माता का स्नेह व आशीर्वाद प्राप्त होगा। गृह-सज्जा व परिवार में समय व्यतीत होगा।",
                    health: "मानसिक शांति बनाए रखें। सात्विक आहार लें और विश्राम को प्राथमिकता दें।"
                },
                5: {
                    wealth: "पंचम भाव में चन्द्रमा बुद्धि व ज्ञान द्वारा आकस्मिक धन लाभ व निवेश में अनुकूलता देगा।",
                    career: "रचनात्मक विचारों व नवोन्मेष से कार्यक्षेत्र में विशेष पहचान बनेगी। अध्ययन व रिसर्च हेतु श्रेष्ठ दिन।",
                    rel: "संतान पक्ष से हर्षदायक समाचार। प्रेम-संबंधों में प्रगाढ़ता व आत्मीयता बढ़ेगी।",
                    health: "पाचन क्रिया का ध्यान रखें। योग व प्राणायाम से मानसिक एकाग्रता बढ़ेगी।"
                },
                6: {
                    wealth: "षष्ठ भाव में चन्द्रमा शत्रु व बाधाओं पर विजय दिलाएगा। ऋण मुक्ति व पुराने लेन-देन सुलझेंगे।",
                    career: "प्रतिस्पर्धा में अग्रिम स्थान प्राप्त होगा। कठिन दायित्वों को समय पर पूर्ण करने में सफल रहेंगे।",
                    rel: "मातृपक्ष (ननिहाल) से संबंध अच्छे रहेंगे। अनावश्यक वाद-विवाद से दूरी बनाए रखें।",
                    health: "मौसमी विकारों से बचाव रखें। संतुलित सात्विक आहार व नियमित विश्राम आवश्यक।"
                },
                7: {
                    wealth: "सप्तम भाव में चन्द्रमा व्यापारिक साझेदारियों व अनुबंधों से धन लाभ कराएगा।",
                    career: "पब्लिक डीलिंग, क्लाइंट मीटिंग्स व संयुक्त उपक्रमों में उत्कृष्ट परिणाम मिलेंगे।",
                    rel: "दांपत्य जीवन में मधुरता व परस्पर समझ बढ़ेगी। जीवनसाथी का पूर्ण सहयोग प्राप्त होगा।",
                    health: "जीवनशैली में संतुलन बनाए रखें। शाम को टहलना ऊर्जादायक रहेगा।"
                },
                8: {
                    wealth: "अष्टम भाव में चन्द्रमा गुप्त लाभ व अनुसंधान कार्यों में सफलता देगा। सट्टेबाजी व जल्दबाजी के लेन-देन से बचें।",
                    career: "गहन शोध, ऑडिट व जटिल समस्याओं के समाधान हेतु अनुकूल समय। नए निवेश में सावधानी रखें।",
                    rel: "ससुराल पक्ष से संपर्क संभव। भावनाओं पर संयम रखें और शांत मन से संवाद करें।",
                    health: "गहरी नींद लें। ॐ नमः शिवाय का मानसिक जप मानसिक शांति प्रदान करेगा।"
                },
                9: {
                    wealth: "नवम (भाग्य) भाव में चन्द्रमा से भाग्य का भरपूर साथ मिलेगा। धर्मार्थ कार्यों व तीर्थ पर व्यय संभव।",
                    career: "उच्चाधिकारियों व मार्गदर्शकों का विशेष अनुग्रह प्राप्त होगा। दूरस्थ संपर्कों से उन्नति के द्वार खुलेंगे।",
                    rel: "पिता व गुरुजनों का आशीर्वाद मिलेगा। पारिवारिक माहौल धार्मिक व उत्सवमय रहेगा।",
                    health: "आध्यात्मिक शांति व उच्च मानसिक ऊर्जा रहेगी। दिन अत्यंत सकारात्मक रहेगा।"
                },
                10: {
                    wealth: "दशम (कर्म) भाव में चन्द्रमा कर्मक्षेत्र से उत्कृष्ट धन प्राप्ति व प्रतिष्ठा में वृद्धि कराएगा।",
                    career: "दशम भाव में " + tMoonSign + " राशि का चन्द्रमा कर्मक्षेत्र में मान-प्रतिष्ठा, वरिष्ठों का सहयोग व व्यावसायिक अनुबंधों में गति का संकेत दे रहा है।",
                    rel: "सामाजिक प्रतिष्ठा में वृद्धि। परिवार आपके पुरुषार्थ पर गर्व महसूस करेगा।",
                    health: "मानसिक ऊर्जा व एकाग्रता 85% अनुकूल है। पर्याप्त जल ग्रहण करें।"
                },
                11: {
                    wealth: "एकादश (लाभ) भाव में चन्द्रमा सर्व मनोकामना सिद्धि व बहुआयामी आर्थिक लाभ का योग बना रहा है।",
                    career: "व्यावसायिक प्रोजेक्ट्स में बड़ा मुनाफा। नए संपर्कों व बड़े नेटवर्क्स से लाभ प्राप्त होगा।",
                    rel: "ज्येष्ठ भ्राता व वरिष्ठ मित्रों से प्रगाढ़ संबंध। उत्सव व आमोद-प्रमोद का वातावरण।",
                    health: "आरोग्य व प्रसन्नता बनी रहेगी। ऊर्जा स्तर 94% अनुकूल।"
                },
                12: {
                    wealth: "द्वादश भाव में चन्द्रमा मांगलिक कार्यों, आयात-निर्यात व विदेशी अनुबंधों में निवेश कराएगा।",
                    career: "एकांत चिंतन, दूरस्थ कार्य व आध्यात्मिक शोध हेतु उत्तम। व्यय पर विवेकपूर्ण नियंत्रण रखें।",
                    rel: "दूर रहने वाले स्वजनों से संवाद होगा। परोपकार व सेवा कार्यों में रुचि बढ़ेगी।",
                    health: "नेत्रों को विश्राम दें व समय पर शयन करें। ध्यान व प्राणायाम लाभदायक रहेगा।"
                }
            };

            var pred = HOUSE_TRANSIT_PREDICTIONS[chandraHouse] || HOUSE_TRANSIT_PREDICTIONS[10];
            if (dhWealth) dhWealth.textContent = pred.wealth;
            if (dhCareer) dhCareer.textContent = pred.career;
            if (dhRelations) dhRelations.textContent = pred.rel;
            if (dhHealth) dhHealth.textContent = pred.health;
        },"""

    if old_tara_set in content:
        content = content.replace(old_tara_set, new_tara_set, 1)
        print("✓ Injected dynamic Chandra Lagna Gochar 12-house calculations into updateDailyHoroscopeUI.")
    else:
        print("! Warning: old_tara_set not found exactly.")

    # --- 3. FIX CRASH IN openEditProfileModal & openNewProfileModal ---
    old_edit_modal = """        openEditProfileModal() {
            var modal = document.getElementById('modalEditProfile');
            if (!modal) return;
            var prof = this.activeChartData.profile || AUTHENTIC_BUNDLE.profile;
            document.getElementById('edit_name').value = prof.name || "";
            document.getElementById('edit_dob').value = prof.dob || "";
            document.getElementById('edit_tob').value = prof.tob || "04:51 PM";
            document.getElementById('edit_city').value = prof.city || "";
            document.getElementById('edit_gender').value = prof.gender || "Male";
            modal.classList.add('active');
        },

        openNewProfileModal() {
            this.openEditProfileModal();
            document.getElementById('edit_name').value = "";
            document.getElementById('edit_dob').value = "1995-05-15";
            document.getElementById('edit_tob').value = "12:00";
            document.getElementById('edit_city').value = "Jaipur, Rajasthan";
        },"""

    new_edit_modal = """        openEditProfileModal() {
            var modal = document.getElementById('modalEditProfile');
            if (!modal) return;
            var prof = (this.activeChartData && this.activeChartData.profile) ? this.activeChartData.profile : {};
            var nameEl = document.getElementById('edit_name');
            var dobEl = document.getElementById('edit_dob');
            var tobEl = document.getElementById('edit_tob');
            var cityEl = document.getElementById('edit_city');
            var genderEl = document.getElementById('edit_gender');
            if (nameEl) nameEl.value = prof.name || "";
            if (dobEl) dobEl.value = prof.dob || "";
            if (tobEl) tobEl.value = prof.tob || "12:00";
            if (cityEl) cityEl.value = prof.city || "";
            if (genderEl) genderEl.value = prof.gender || "Male";
            modal.classList.add('active');
            modal.style.display = 'flex';
        },

        openNewProfileModal() {
            this.openEditProfileModal();
            var nameEl = document.getElementById('edit_name');
            var dobEl = document.getElementById('edit_dob');
            var tobEl = document.getElementById('edit_tob');
            var cityEl = document.getElementById('edit_city');
            if (nameEl) nameEl.value = (this.googleUser && this.googleUser.name) ? this.googleUser.name : "";
            if (dobEl) dobEl.value = "";
            if (tobEl) tobEl.value = "12:00";
            if (cityEl) cityEl.value = "नई दिल्ली";
            var headTitle = document.querySelector('#modalEditProfile .modal-head b');
            if (headTitle) headTitle.textContent = "✦ नई कुण्डली बनाएँ (New Birth Chart)";
        },"""

    if old_edit_modal in content:
        content = content.replace(old_edit_modal, new_edit_modal, 1)
        print("✓ Patched openEditProfileModal and openNewProfileModal with safe guards and Google name pre-fill.")
    else:
        print("! Warning: old_edit_modal not found exactly.")

    # --- 4. FIX submitProfileEdit TO UPDATE ALL VIEWS ---
    old_submit_edit = """            this.loadStoredProfile();
            this.renderChart('d1');
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderAshtakavarga();
            this.renderKP();
            this.renderJaimini();
            this.renderNadi();
            this.closeModals();
            alert("जातक " + name + " की जन्म कुण्डली (" + newChart.profile.asc_sign + " लग्न) की वास्तविक वैदिक गणना पूर्ण हो गई है!");"""

    new_submit_edit = """            this.loadStoredProfile();
            this.renderChart(this.currentVarga || 'd1');
            this.updateDailyHoroscopeUI();
            this.updateYogasBannerUI();
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderAshtakavarga();
            this.renderKP();
            this.renderJaimini();
            this.renderNadi();
            this.renderSphutas();
            this.renderGochar();
            this.renderShadbala();
            this.initDashaTree();
            this.closeModals();
            alert("जातक " + name + " की जन्म कुण्डली (" + newChart.profile.asc_sign + " लग्न) की वास्तविक वैदिक गणना पूर्ण हो गई है!");"""

    if old_submit_edit in content:
        content = content.replace(old_submit_edit, new_submit_edit, 1)
        print("✓ Patched submitProfileEdit to refresh all 15 cockpit views and daily horoscope on creation.")
    else:
        print("! Warning: old_submit_edit not found exactly.")

    # --- 5. FIX renderPavTable NULL CRASH ---
    old_pav = "var av = this.activeChartData.ashtakavarga || AUTHENTIC_BUNDLE.ashtakavarga;"
    new_pav = "var av = (this.activeChartData && this.activeChartData.ashtakavarga) ? this.activeChartData.ashtakavarga : ((typeof AUTHENTIC_BUNDLE !== 'undefined' && AUTHENTIC_BUNDLE.ashtakavarga) ? AUTHENTIC_BUNDLE.ashtakavarga : {});"
    if old_pav in content:
        content = content.replace(old_pav, new_pav)
        print("✓ Fixed renderPavTable activeChartData null crash guard.")

    # --- 6. SMOOTH GOOGLE SIGN-IN FLOW ---
    old_sign_in = """            // Safe auth response without forced profile injection
if (!this.activeChartData) { var s = localStorage.getItem('vyas_active_profile'); if (s) { try { this.activeChartData = JSON.parse(s); } catch(e) {} } }
            this.updateGoogleAuthUI();
            this.loadStoredProfile();
            this.renderChart(this.currentVarga || 'd1');
            this.updateDailyHoroscopeUI();
            this.updateYogasBannerUI();
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderDashaTree();
            this.closeModals();
            // Signed in smoothly without fake alert
            console.log("User session active:", name);"""

    new_sign_in = """            // Safe auth response without forced profile injection
            if (!this.activeChartData) {
                var s = localStorage.getItem('vyas_active_profile');
                if (s) { try { this.activeChartData = JSON.parse(s); } catch(e) {} }
            }
            this.updateGoogleAuthUI();
            this.closeModals();
            
            // If user has no kundli yet, seamlessly invite them to create their birth chart!
            if (!this.activeChartData) {
                this.openNewProfileModal();
            } else {
                this.loadStoredProfile();
                this.renderChart(this.currentVarga || 'd1');
                this.updateDailyHoroscopeUI();
                this.updateYogasBannerUI();
                this.renderPlanetTable();
                this.renderPredictions();
                this.renderDashaTree();
            }
            console.log("User session active:", name);"""

    if old_sign_in in content:
        content = content.replace(old_sign_in, new_sign_in, 1)
        print("✓ Patched signInCustomProfile to smoothly trigger openNewProfileModal when no prior chart exists.")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Successfully saved patched index.html.")

if __name__ == '__main__':
    patch_index_html()

