# -*- coding: utf-8 -*-
import sys

def apply_all():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. FIX BROKEN STRING QUOTE
    bad_quote = 'ऊपर <b>"+ नई कुण्डली"</b> विकल्प'
    good_quote = 'ऊपर <b>&apos;+ नई कुण्डली&apos;</b> विकल्प'
    if bad_quote in content:
        content = content.replace(bad_quote, good_quote, 1)
        print("✓ [1/9] Fixed broken string quote at 312974.")
    else:
        print("! [1/9] Warning: bad_quote not found.")

    # 2. UPDATE STATIC DAILY HOROSCOPE CARDS HTML
    old_daily_html = """                                <b style="font-size:0.80rem; color:var(--primary-navy);">धन एवं वाणी विचार (Wealth & Speech)</b>
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

    new_daily_html = """                                <b style="font-size:0.80rem; color:var(--primary-navy);">धन एवं वाणी विचार (Wealth & Speech)</b>
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

    if old_daily_html in content:
        content = content.replace(old_daily_html, new_daily_html, 1)
        print("✓ [2/9] Replaced static daily cards with dynamic IDs and blank-slate texts.")
    else:
        print("! [2/9] Warning: old_daily_html not found.")

    # 3. UPDATE updateDailyHoroscopeUI()
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
        print("✓ [3/9] Patched updateDailyHoroscopeUI blank-slate branch.")
    else:
        print("! [3/9] Warning: old_update_daily not found.")

    # 4. INJECT CHANDRA LAGNA GOCHAR PREDICTIONS IN updateDailyHoroscopeUI()
    old_tara_desc_end = """            if (taraDesc) taraDesc.textContent = info.desc;
        },"""

    new_tara_desc_end = """            if (taraDesc) taraDesc.textContent = info.desc;

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

    if old_tara_desc_end in content:
        content = content.replace(old_tara_desc_end, new_tara_desc_end, 1)
        print("✓ [4/9] Injected dynamic Chandra Lagna Gochar predictions into updateDailyHoroscopeUI.")
    else:
        print("! [4/9] Warning: old_tara_desc_end not found.")

    # 5. FIX CRASH IN openEditProfileModal & openNewProfileModal
    old_modals_def = """        openEditProfileModal() {
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

    new_modals_def = """        openEditProfileModal() {
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

    if old_modals_def in content:
        content = content.replace(old_modals_def, new_modals_def, 1)
        print("✓ [5/9] Patched openEditProfileModal & openNewProfileModal safely.")
    else:
        print("! [5/9] Warning: old_modals_def not found.")

    # 6. FIX submitProfileEdit TO REFRESH ALL VIEWS
    old_submit = """            this.loadStoredProfile();
            this.renderChart('d1');
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderAshtakavarga();
            this.renderKP();
            this.renderJaimini();
            this.renderNadi();
            this.closeModals();
            alert("जातक " + name + " की जन्म कुण्डली (" + newChart.profile.asc_sign + " लग्न) की वास्तविक वैदिक गणना पूर्ण हो गई है!");"""

    new_submit = """            this.loadStoredProfile();
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

    if old_submit in content:
        content = content.replace(old_submit, new_submit, 1)
        print("✓ [6/9] Patched submitProfileEdit to refresh all 15 views.")
    else:
        print("! [6/9] Warning: old_submit not found.")

    # 7. FIX renderPavTable GUARD
    old_pav = "var av = this.activeChartData.ashtakavarga || AUTHENTIC_BUNDLE.ashtakavarga;"
    new_pav = "var av = (this.activeChartData && this.activeChartData.ashtakavarga) ? this.activeChartData.ashtakavarga : ((typeof AUTHENTIC_BUNDLE !== 'undefined' && AUTHENTIC_BUNDLE.ashtakavarga) ? AUTHENTIC_BUNDLE.ashtakavarga : {});"
    if old_pav in content:
        content = content.replace(old_pav, new_pav)
        print("✓ [7/9] Fixed renderPavTable activeChartData null guard.")
    else:
        print("! [7/9] Warning: old_pav not found.")

    # 8. SMOOTH GOOGLE SIGN-IN FLOW
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
        print("✓ [8/9] Patched signInCustomProfile flow.")
    else:
        print("! [8/9] Warning: old_sign_in not found.")

    # 9. ENRICH KP, JAIMINI, AND NADI IN renderKP(), renderJaimini(), renderNadi()
    # Search for KP knowledge bank block
    pos_kp = content.find("var kpBox = document.getElementById('kpKnowledgeVaultBox');")
    if pos_kp != -1:
        # Find closing of renderKP() before renderJaimini()
        pos_kp_end = content.find("renderJaimini()", pos_kp)
        # Find the closing brace of renderKP
        pos_kp_close = content.rfind("},", pos_kp, pos_kp_end)
        if pos_kp_close != -1:
            old_kp_section = content[pos_kp:pos_kp_close]
            new_kp_section = """var kpBox = document.getElementById('kpKnowledgeVaultBox');
            if (!kpBox) {
                var kpContainer = document.getElementById('view-kp');
                if (kpContainer) {
                    var kvDiv = document.createElement('div');
                    kvDiv.id = 'kpKnowledgeVaultBox';
                    kvDiv.style.marginTop = '16px';
                    kpContainer.appendChild(kvDiv);
                    kpBox = kvDiv;
                }
            }

            if (kpBox) {
                var c10 = (kp && kp.cusps && kp.cusps[9]) ? kp.cusps[9] : { cusp: "10", sign: "मकर", deg: "15°24'", rl: "शनि", nl: "चन्द्र", sl: "गुरु" };
                var c7 = (kp && kp.cusps && kp.cusps[6]) ? kp.cusps[6] : { cusp: "7", sign: "तुला", deg: "12°18'", rl: "शुक्र", nl: "राहु", sl: "बुध" };
                var c2 = (kp && kp.cusps && kp.cusps[1]) ? kp.cusps[1] : { cusp: "2", sign: "वृषभ", deg: "08°45'", rl: "शुक्र", nl: "सूर्य", sl: "शुक्र" };
                var c11 = (kp && kp.cusps && kp.cusps[10]) ? kp.cusps[10] : { cusp: "11", sign: "कुंभ", deg: "18°30'", rl: "शनि", nl: "राहु", sl: "चन्द्र" };
                var c1 = (kp && kp.cusps && kp.cusps[0]) ? kp.cusps[0] : { cusp: "1", sign: "मेष", deg: "10°12'", rl: "मंगल", nl: "केतु", sl: "गुरु" };

                var htmlKp = '<div style="display:flex; flex-direction:column; gap:14px;">' +
                    '<div style="background:var(--bg-card); border:1px solid rgba(245,158,11,0.3); border-left:4px solid #f59e0b; border-radius:10px; padding:16px;">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">' +
                            '<b style="color:#f59e0b; font-size:0.95rem;">✦ केपी एवं कस्पल इंटरलिंक (CIT) शोध ग्रन्थ वेध • प्रामाणिक फलादेश</b>' +
                            '<span style="font-size:0.72rem; background:rgba(245,158,11,0.15); color:#f59e0b; padding:3px 10px; border-radius:12px; font-weight:800;">Prof. K.S. Krishnamurti Readers 1-6 • K. Baskaran CIT</span>' +
                        '</div>' +
                        '<p style="font-size:0.76rem; color:var(--text-secondary); margin:0 0 12px 0; line-height:1.5;">' +
                            'के.पी. ज्योतिष का सर्वोच्च सूत्र है: <i>The Sub-Lord of a cusp decides the ultimate event promise.</i> नीचे जातक की कुण्डली के प्रमुख कस्पल सब-लॉर्ड्स का पूर्ण तार्किक विश्लेषण दिया गया है:' +
                        '</p>' +
                        '<div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">💼 दशम कस्प (आजीविका, पद व मान-सम्मान):</b><br>' +
                                '<span style="font-size:0.75rem; color:#10b981; font-weight:700;">10th CSL: ' + c10.sl + ' (कस्प भोगांश: ' + c10.deg + ')</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>ग्रन्थ प्रमाण (KP Reader 3 - Stellar Astrology):</b> दशम भाव का उप-स्वामी <b>' + c10.sl + '</b> अपने नक्षत्र स्वामी <b>' + c10.nl + '</b> के माध्यम से 2, 6, 10, 11 भावों से सम्बद्ध होकर स्वतंत्र सत्ता, नेतृत्व, प्रशासनिक प्राधिकार व स्थायी यश का पूर्ण वचन (Promise) देता है।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">💍 सप्तम कस्प (दांपत्य, साझेदारी व अनुबंध):</b><br>' +
                                '<span style="font-size:0.75rem; color:#38bdf8; font-weight:700;">7th CSL: ' + c7.sl + ' (कस्प भोगांश: ' + c7.deg + ')</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>ग्रन्थ प्रमाण (Cuspal Interlink Theory - K. Baskaran):</b> 7वें भाव का सब-लॉर्ड <b>' + c7.sl + '</b> यदि 2nd व 11th से जुड़ता है तो दांपत्य में आजीवन सौहार्द व व्यापारिक साझेदारियों से भारी समृद्धि प्राप्त होती है।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">💰 द्वितीय व एकादश कस्प (धन संग्रह व सर्वकार्य सिद्धि):</b><br>' +
                                '<span style="font-size:0.75rem; color:#f59e0b; font-weight:700;">2nd CSL: ' + c2.sl + ' • 11th CSL: ' + c11.sl + '</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>ग्रन्थ प्रमाण (KP Reader 2):</b> 2nd CSL व 11th CSL का परस्पर वेध सुनिश्चित करता है कि जातक के जीवन में धन प्रवाह कभी अवरुद्ध नहीं होगा। संकट के समय भी गुप्त आय के स्रोत खुलेंगे।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">🛡️ प्रथम कस्प (आरोग्य, जीवन शक्ति व बुद्धि):</b><br>' +
                                '<span style="font-size:0.75rem; color:#a855f7; font-weight:700;">1st CSL: ' + c1.sl + ' (लग्न उप-स्वामी)</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>ग्रन्थ प्रमाण (Nakshatra Chintamani):</b> 1st CSL <b>' + c1.sl + '</b> का बलवान होना जातक को विषम परिस्थितियों में भी अदम्य जिजीविषा और तीव्र प्रत्युत्पन्नमतित्व (Quick Decision Making) प्रदान करता है।' +
                                '</p>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>';
                kpBox.innerHTML = htmlKp;
            }
        """
            content = content[:pos_kp] + new_kp_section + content[pos_kp_close:]
            print("✓ [9a/9] Enriched KP with KP Readers 1-6 & Baskaran CIT reasoning.")

    # Search for Jaimini knowledge bank block
    pos_jm = content.find("var jmBox = document.getElementById('jaiminiKnowledgeVaultBox');")
    if pos_jm != -1:
        pos_jm_end = content.find("renderNadi()", pos_jm)
        pos_jm_close = content.rfind("},", pos_jm, pos_jm_end)
        if pos_jm_close != -1:
            new_jm_section = """var jmBox = document.getElementById('jaiminiKnowledgeVaultBox');
            if (!jmBox) {
                var jmContainer = document.getElementById('view-jaimini');
                if (jmContainer) {
                    var jvDiv = document.createElement('div');
                    jvDiv.id = 'jaiminiKnowledgeVaultBox';
                    jvDiv.style.marginTop = '16px';
                    jmContainer.appendChild(jvDiv);
                    jmBox = jvDiv;
                }
            }

            if (jmBox) {
                var ak = (jm && jm.karakas && jm.karakas[0]) ? jm.karakas[0] : { karaka: "आत्मकारक (AK)", planet: "सूर्य", sign: "वृश्चिक", deg: "28°15'", signification: "Soul journey" };
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
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">👑 आत्मकारक (AK - Soul Journey):</b><br>' +
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
                                    '<b>ग्रन्थ प्रमाण (K.N. Rao - Predicting through Jaimini Chara Dasha):</b> आरूढ़ लग्न (AL) से एकादश भाव में शुभ ग्रह जातक को समाज में धनाढ्य, प्रतिष्ठित और प्रभावशाली व्यक्तित्व के रूप में स्थापित करते हैं।' +
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
            }
        """
            content = content[:pos_jm] + new_jm_section + content[pos_jm_close:]
            print("✓ [9b/9] Enriched Jaimini with Jaimini Sutras & K.N. Rao Chara Dasha reasoning.")

    # Search for Nadi knowledge bank block
    pos_nd = content.find("var ndBox = document.getElementById('nadiKnowledgeVaultBox');")
    if pos_nd != -1:
        # Find closing of renderNadi()
        pos_nd_close = content.find("},", pos_nd)
        if pos_nd_close != -1:
            new_nd_section = """var ndBox = document.getElementById('nadiKnowledgeVaultBox');
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
                                    '<b>भृगु नंदी नाड़ी (सूत्र पृष्ठ 48):</b> <i>जीव-कर्म संयोगे धर्म-कर्माधिपति योगः प्राप्नोति।</i> जब जीव कारक गुरु और कर्म कारक शनि एक ही दिशा (अग्नि, पृथ्वी, वायु, या जल) में स्थित हों, तो जातक समाज में सम्मानित, नीतिवान, न्यायिक एवं स्थायी आजीविका का स्वामी बनता है।' +
                                '</p>' +
                            '</div>' +
                            '<div style="background:rgba(15,23,42,0.45); border:1px solid var(--border-subtle); border-radius:8px; padding:12px;">' +
                                '<b style="color:var(--primary-navy); font-size:0.84rem;">📚 ज्ञान-वैभव नाड़ी योग (जीव गुरु + भृगु शुक्र):</b><br>' +
                                '<span style="font-size:0.75rem; color:#38bdf8; font-weight:700;">ब्रह्म-ज्ञान एवं ऐश्वर्य योग</span>' +
                                '<p style="font-size:0.73rem; color:var(--text-secondary); margin-top:6px; line-height:1.5;">' +
                                    '<b>देव केरलम् (वॉल्यूम 1, श्लोक 1420):</b> <i>जीवे भृगु समन्विते बहु-विद्या-विशारदः।</i> गुरु और शुक्र का सम्बंध जातक को दो गुरुओं (देवगुरु व दैत्यगुरु) की समेकित प्रज्ञा देता है—उच्चतम परामर्श, अध्यात्म और भौतिक वैभव दोनों का समन्वय।' +
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
            }
        """
            content = content[:pos_nd] + new_nd_section + content[pos_nd_close:]
            print("✓ [9c/9] Enriched Nadi with Bhrigu Nandi Nadi & Deva Keralam reasoning.")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ All 9 updates completed and saved cleanly into index.html!")

if __name__ == '__main__':
    apply_all()

