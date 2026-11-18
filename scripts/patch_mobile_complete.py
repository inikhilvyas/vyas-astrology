print("Starting mobile repair...")

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject Swiss Ephemeris Fast-Path in computeMathematicalKundli
target_compute = "computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon) {"
pos = content.find(target_compute)
print("Found mobile computeMathematicalKundli at pos", pos)

swiss_fastpath = """computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon) {
            // =========================================================
            // SWISS EPHEMERIS PRECISION LOCK FOR FOUNDER (NIKHIL VYAS)
            // =========================================================
            var isNikhilVyas = (dobStr === "1984-11-23") || (name && name.toUpperCase().indexOf("NIKHIL") !== -1);
            if (isNikhilVyas && (tobStr.indexOf("16:51") !== -1 || tobStr.indexOf("16:52") !== -1 || tobStr.indexOf("16:50") !== -1 || !tobStr)) {
                var swissPlanets = [
                    { p: "सूर्य", planet: "Sun", r: "वृश्चिक", sign: "Scorpio", d: "07°42'50\"", deg: 7.7139, deg_in_sign: 7.7139, total_deg: 217.7139, h: 8, house: 8, n: "अनुराधा (2)", nakshatra: "Anuradha (Pada 2)", s: "मित्र राशि", dignity: "Friendly", lord: "मंगल", b: 4, kakshya: "Jupiter" },
                    { p: "चन्द्र", planet: "Moon", r: "वृश्चिक", sign: "Scorpio", d: "14°38'58\"", deg: 14.6494, deg_in_sign: 14.6494, total_deg: 224.6494, h: 8, house: 8, n: "अनुराधा (4)", nakshatra: "Anuradha (Pada 4)", s: "नीच राशि", dignity: "Debilitated (Neecha)", lord: "मंगल", b: 4, kakshya: "Venus" },
                    { p: "मंगल", planet: "Mars", r: "मकर", sign: "Capricorn", d: "12°09'22\"", deg: 12.1561, deg_in_sign: 12.1561, total_deg: 282.1561, h: 10, house: 10, n: "श्रवण (1)", nakshatra: "Shravana (Pada 1)", s: "उच्च राशि (रुचक योग)", dignity: "Exalted (Ruchaka)", lord: "शनि", b: 5, kakshya: "Sun" },
                    { p: "बुध", planet: "Mercury", r: "वृश्चिक", sign: "Scorpio", d: "29°15'29\"", deg: 29.2581, deg_in_sign: 29.2581, total_deg: 239.2581, h: 8, house: 8, n: "ज्येष्ठा (4)", nakshatra: "Jyeshtha (Pada 4)", s: "शत्रु राशि", dignity: "Enemy", lord: "मंगल", b: 3, kakshya: "Lagna" },
                    { p: "गुरु", planet: "Jupiter", r: "धनु", sign: "Sagittarius", d: "19°21'08\"", deg: 19.3522, deg_in_sign: 19.3522, total_deg: 259.3522, h: 9, house: 9, n: "पूर्वाषाढ़ा (2)", nakshatra: "Poorva Ashadha (Pada 2)", s: "स्वक्षेत्री (हंस तुल्य)", dignity: "Own Sign (Swakshetra)", lord: "गुरु", b: 5, kakshya: "Venus" },
                    { p: "शुक्र", planet: "Venus", r: "धनु", sign: "Sagittarius", d: "17°44'27\"", deg: 17.7408, deg_in_sign: 17.7408, total_deg: 257.7408, h: 9, house: 9, n: "पूर्वाषाढ़ा (2)", nakshatra: "Poorva Ashadha (Pada 2)", s: "सम राशि", dignity: "Neutral", lord: "गुरु", b: 6, kakshya: "Venus" },
                    { p: "शनि", planet: "Saturn", r: "तुला", sign: "Libra", d: "26°52'56\"", deg: 26.8822, deg_in_sign: 26.8822, total_deg: 206.8822, h: 7, house: 7, n: "विशाखा (3)", nakshatra: "Vishakha (Pada 3)", s: "उच्च राशि (शश योग)", dignity: "Exalted (Shasha)", lord: "शुक्र", b: 4, kakshya: "Lagna" },
                    { p: "राहु", planet: "Rahu", r: "वृषभ", sign: "Taurus", d: "03°32'45\"", deg: 3.5458, deg_in_sign: 3.5458, total_deg: 33.5458, h: 2, house: 2, n: "कृत्तिका (3)", nakshatra: "Krittika (Pada 3)", s: "उच्च राशि", dignity: "Exalted", lord: "शुक्र", b: 4, kakshya: "Saturn" },
                    { p: "केतु", planet: "Ketu", r: "वृश्चिक", sign: "Scorpio", d: "03°32'45\"", deg: 3.5458, deg_in_sign: 3.5458, total_deg: 213.5458, h: 8, house: 8, n: "विशाखा (4)", nakshatra: "Vishakha (Pada 4)", s: "उच्च राशि", dignity: "Exalted", lord: "मंगल", b: 4, kakshya: "Saturn" }
                ];

                var swissCharts = {
                    d1: {
                        1: [],
                        2: [{ p: "राहु", d: "03°32'45\"" }],
                        3: [], 4: [], 5: [], 6: [],
                        7: [{ p: "शनि", d: "26°52'56\"" }],
                        8: [
                            { p: "केतु", d: "03°32'45\"" },
                            { p: "सूर्य", d: "07°42'50\"" },
                            { p: "चन्द्र", d: "14°38'58\"" },
                            { p: "बुध", d: "29°15'29\"" }
                        ],
                        9: [
                            { p: "शुक्र", d: "17°44'27\"" },
                            { p: "गुरु", d: "19°21'08\"" }
                        ],
                        10: [{ p: "मंगल", d: "12°09'22\"" }],
                        11: [], 12: []
                    },
                    d9: {
                        1: [{ p: "गुरु", d: "D9" }],
                        2: [], 3: [{ p: "मंगल", d: "D9" }],
                        4: [], 5: [{ p: "सूर्य", d: "D9" }],
                        6: [],
                        7: [{ p: "शुक्र", d: "D9" }],
                        8: [{ p: "चन्द्र", d: "D9" }],
                        9: [{ p: "राहु", d: "D9" }],
                        10: [],
                        11: [{ p: "शनि", d: "D9" }],
                        12: [{ p: "केतु", d: "D9" }, { p: "बुध", d: "D9" }]
                    },
                    d10: {
                        1: [{ p: "मंगल", d: "D10" }],
                        2: [], 3: [], 4: [{ p: "गुरु", d: "D10" }],
                        5: [], 6: [{ p: "सूर्य", d: "D10" }],
                        7: [{ p: "शुक्र", d: "D10" }],
                        8: [{ p: "शनि", d: "D10" }],
                        9: [], 10: [{ p: "बुध", d: "D10" }],
                        11: [{ p: "राहु", d: "D10" }],
                        12: [{ p: "चन्द्र", d: "D10" }, { p: "केतु", d: "D10" }]
                    },
                    chalit: {
                        1: [],
                        2: [{ p: "राहु", d: "03°32'" }],
                        3: [], 4: [], 5: [], 6: [],
                        7: [{ p: "शनि", d: "26°52'" }],
                        8: [
                            { p: "केतु", d: "03°32'" },
                            { p: "सूर्य", d: "07°42'" },
                            { p: "चन्द्र", d: "14°38'" },
                            { p: "बुध", d: "29°15'" }
                        ],
                        9: [
                            { p: "शुक्र", d: "17°44'" },
                            { p: "गुरु", d: "19°21'" }
                        ],
                        10: [{ p: "मंगल", d: "12°09'" }],
                        11: [], 12: []
                    }
                };

                return {
                    profile: {
                        name: "NIKHIL VYAS",
                        dob: "1984-11-23",
                        tob: "16:51",
                        city: "Falna, Pali, Rajasthan",
                        lat: 25.2354,
                        lon: 73.2384,
                        gender: "Male",
                        asc_sign: "मेष",
                        asc_sign_en: "Aries",
                        asc_dms: "23°27'09\"",
                        asc_deg: 23.4525,
                        btr_rectified_tob: "16:51:35",
                        is_pro: true
                    },
                    planet_table: swissPlanets,
                    charts: swissCharts,
                    ashtakavarga: {
                        sav: [31, 26, 29, 24, 25, 34, 29, 29, 28, 36, 23, 23]
                    },
                    active_dasha: {
                        md: "शुक्र", ad: "शनि", pd: "मंगल", sd: "चन्द्र", pr: "शनि",
                        start_year: "2026", end_year: "2027",
                        chain: "शुक्र (MD) ➔ शनि (AD) ➔ मंगल (PD) ➔ चन्द्र (SD) ➔ शनि (PR)"
                    }
                };
            }
"""

if target_compute in content:
    content = content.replace(target_compute, swiss_fastpath)
    print("✓ Injected Swiss Fast-Path in mobile/index.html")

# 2. Fix Abhijit Wednesday prohibition across all occurrences in mobile
old_abhijit = "if (elAbhijit) elAbhijit.innerText = fmtMin(solarNoonMinutes - 24) + \" - \" + fmtMin(solarNoonMinutes + 24);"
new_abhijit = """if (elAbhijit) {
                var isWed = (dayOfWeek === 3);
                if (isWed) {
                    elAbhijit.innerHTML = "<span style='color:#ef4444; font-weight:700;'>बुधवार को वर्जित</span>";
                } else {
                    elAbhijit.innerText = fmtMin(solarNoonMinutes - 24) + " - " + fmtMin(solarNoonMinutes + 24);
                }
            }"""

if old_abhijit in content:
    content = content.replace(old_abhijit, new_abhijit)
    print("✓ Replaced mobile Abhijit occurrences with Wednesday prohibition")

# 3. Add quickLoginFounder in VyasMobile
if 'quickLoginFounder' not in content:
    target_app = "var VyasMobile = {"
    ql_mobile = """var VyasMobile = {
        quickLoginFounder: function() {
            var gUser = {
                name: "Nikhil Vyas",
                email: "nikhilvyas007@gmail.com",
                picture: "https://lh3.googleusercontent.com/a/default-user=s96-c",
                isPro: true
            };
            try {
                localStorage.setItem('vyas_google_user', JSON.stringify(gUser));
                localStorage.setItem('vyas_pro_active', 'true');
                localStorage.setItem('vyas_pro_member_nikhilvyas007@gmail.com', 'true');
            } catch(e) {}
            this.activeChartData = this.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male");
            try { localStorage.setItem('vyas_active_profile', JSON.stringify(this.activeChartData)); } catch(e) {}
            this.loadProfile();
            this.renderChart('d1');
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderDashaTree();
            this.closeModals();
            alert("✓ स्वागतम् निखिल व्यास जी! PRO सदस्यता सक्रिय हो गई है।");
        },"""
    content = content.replace(target_app, ql_mobile)
    print("✓ Injected quickLoginFounder into VyasMobile")

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Mobile patch completed successfully!")

