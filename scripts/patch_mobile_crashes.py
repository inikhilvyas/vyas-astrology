# -*- coding: utf-8 -*-
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add renderRemedies to VyasMobile
if 'renderRemedies:' not in text:
    target = 'renderMatch: function() {'
    replacement = '''renderRemedies: function() {
            var rView = document.getElementById('view-remedies');
            if (!rView) return;
        },

        renderMatch: function() {'''
    text = text.replace(target, replacement, 1)
    print("[OK] Added renderRemedies to mobile/index.html")

# 2. Fix renderAshtakavarga
old_av = '''        renderAshtakavarga: function() {
            var av = (this.activeChartData && this.activeChartData.ashtakavarga) ? this.activeChartData.ashtakavarga : AUTHENTIC_BUNDLE.ashtakavarga;
            var sav = av.sav || [33, 25, 25, 30, 31, 39, 29, 26, 19, 31, 27, 22];'''

new_av = '''        renderAshtakavarga: function() {
            var av = (this.activeChartData && this.activeChartData.ashtakavarga) ? this.activeChartData.ashtakavarga : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.ashtakavarga : null);
            if (!av) av = { sav: [33, 25, 25, 30, 31, 39, 29, 26, 19, 31, 27, 22] };
            var sav = av.sav || [33, 25, 25, 30, 31, 39, 29, 26, 19, 31, 27, 22];'''

if old_av in text:
    text = text.replace(old_av, new_av, 1)
    print("[OK] Fixed renderAshtakavarga in mobile/index.html")

# Also fix BAV summary in renderAshtakavarga
text = text.replace('if (bavTable && av.bav) {', 'if (bavTable && av && av.bav) {')

# 3. Fix renderGochar
old_gochar = '''        renderGochar: function() {
            var wrap = document.getElementById('mGocharSvgWrap');
            if (wrap && GOCHAR_BUNDLE && GOCHAR_BUNDLE.transit_houses) {
                wrap.innerHTML = this.generateDiamondSVG(GOCHAR_BUNDLE.transit_houses, 250, 'तात्कालिक गोचर चक्र');
            }

            var tbody = document.getElementById('mGocharTableBody');
            if (tbody && GOCHAR_BUNDLE) {
                var rows = GOCHAR_BUNDLE.transit_rows || GOCHAR_BUNDLE.transit_planets || [];'''

new_gochar = '''        renderGochar: function() {
            var gb = window.GOCHAR_BUNDLE || null;
            var wrap = document.getElementById('mGocharSvgWrap');
            if (wrap && gb && gb.transit_houses) {
                wrap.innerHTML = this.generateDiamondSVG(gb.transit_houses, 250, 'तात्कालिक गोचर चक्र');
            }

            var tbody = document.getElementById('mGocharTableBody');
            if (tbody && gb) {
                var rows = gb.transit_rows || gb.transit_planets || [];'''

if old_gochar in text:
    text = text.replace(old_gochar, new_gochar, 1)
    print("[OK] Fixed renderGochar in mobile/index.html")

# Replace remaining bare GOCHAR_BUNDLE in renderGochar
text = text.replace('if (mdBox && GOCHAR_BUNDLE && GOCHAR_BUNDLE.varshphal', 'if (mdBox && gb && gb.varshphal')
text = text.replace('for (var j = 0; j < GOCHAR_BUNDLE.varshphal.mudda_dasha.length; j++) {', 'for (var j = 0; j < (gb.varshphal.mudda_dasha ? gb.varshphal.mudda_dasha.length : 0); j++) {')
text = text.replace('var mu = GOCHAR_BUNDLE.varshphal.mudda_dasha[j];', 'var mu = gb.varshphal.mudda_dasha[j];')

# 4. Fix renderVarga
old_varga = '''        renderVarga: function(vargaKey) {
            var box = document.getElementById('mVargaSvgBox');
            if (!box) return;

            var vMap = {
                'D1': { name: 'लग्न कुण्डली (D-1)', data: this.activeChartData || AUTHENTIC_BUNDLE },
                'D9': { name: 'नवमांश चक्र (D-9)', data: (this.activeChartData && this.activeChartData.vargas && this.activeChartData.vargas.D9) ? this.activeChartData.vargas.D9 : AUTHENTIC_BUNDLE.vargas.D9 },
                'D10': { name: 'दशमांश चक्र (D-10)', data: (this.activeChartData && this.activeChartData.vargas && this.activeChartData.vargas.D10) ? this.activeChartData.vargas.D10 : (AUTHENTIC_BUNDLE.vargas ? AUTHENTIC_BUNDLE.vargas.D10 : AUTHENTIC_BUNDLE.vargas.D9) }
            };

            var target = vMap[vargaKey] || vMap['D9'];
            var houses = (target.data && target.data.houses) ? target.data.houses : ((this.activeChartData && this.activeChartData.houses) ? this.activeChartData.houses : AUTHENTIC_BUNDLE.houses);

            box.innerHTML = this.generateDiamondSVG(houses, 260, target.name);
        },'''

new_varga = '''        renderVarga: function(vargaKey) {
            var box = document.getElementById('mVargaSvgBox');
            if (!box) return;

            var d1Data = this.activeChartData || (window.AUTHENTIC_BUNDLE || null);
            var d9Data = (this.activeChartData && this.activeChartData.vargas && this.activeChartData.vargas.D9) ? this.activeChartData.vargas.D9 : (window.AUTHENTIC_BUNDLE && window.AUTHENTIC_BUNDLE.vargas ? window.AUTHENTIC_BUNDLE.vargas.D9 : null);
            var d10Data = (this.activeChartData && this.activeChartData.vargas && this.activeChartData.vargas.D10) ? this.activeChartData.vargas.D10 : (window.AUTHENTIC_BUNDLE && window.AUTHENTIC_BUNDLE.vargas ? window.AUTHENTIC_BUNDLE.vargas.D10 : d9Data);

            var vMap = {
                'D1': { name: 'लग्न कुण्डली (D-1)', data: d1Data },
                'D9': { name: 'नवमांश चक्र (D-9)', data: d9Data },
                'D10': { name: 'दशमांश चक्र (D-10)', data: d10Data }
            };

            var target = vMap[vargaKey] || vMap['D9'];
            var houses = (target && target.data && target.data.houses) ? target.data.houses : ((this.activeChartData && this.activeChartData.houses) ? this.activeChartData.houses : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.houses : null));

            if (houses) {
                box.innerHTML = this.generateDiamondSVG(houses, 260, target.name);
            } else {
                box.innerHTML = '<div style="padding:24px; text-align:center; color:var(--text-muted); font-size:0.82rem;">' + (target ? target.name : 'वर्ग चक्र') + ' देखने हेतु कृपया अपनी कुण्डली बनाएं।</div>';
            }
        },'''

if old_varga in text:
    text = text.replace(old_varga, new_varga, 1)
    print("[OK] Fixed renderVarga in mobile/index.html")

# 5. Fix renderKP
old_kp = '''            var kp = (this.activeChartData && this.activeChartData.kp && this.activeChartData.kp.cusps) ? this.activeChartData.kp : AUTHENTIC_BUNDLE.kp;
            var cBody = document.getElementById('mKpCuspsBody') || document.getElementById('kpCuspsTableBody');
            if (cBody && kp && kp.cusps) {'''

new_kp = '''            var kp = (this.activeChartData && this.activeChartData.kp && this.activeChartData.kp.cusps) ? this.activeChartData.kp : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.kp : null);
            var cBody = document.getElementById('mKpCuspsBody') || document.getElementById('kpCuspsTableBody');
            if (cBody) {
                if (kp && kp.cusps) {'''

if old_kp in text:
    text = text.replace(old_kp, new_kp, 1)
    print("[OK] Fixed renderKP cusp table in mobile/index.html")

# Safe check for kp.planets
old_kp_p = '''            var pBody = document.getElementById('mKpPlanetsBody') || document.getElementById('kpPlanetsTableBody');
            if (pBody && kp.planets) {'''

new_kp_p = '''            var pBody = document.getElementById('mKpPlanetsBody') || document.getElementById('kpPlanetsTableBody');
            if (pBody) {
                if (kp && kp.planets) {'''

if old_kp_p in text:
    text = text.replace(old_kp_p, new_kp_p, 1)
    print("[OK] Fixed renderKP planets table in mobile/index.html")

# 6. Fix renderPlanetTable
old_planet_tbl = '''        renderPlanetTable: function() {
            var tbodies = [
                document.getElementById('mPlanetTableBody'),
                document.getElementById('mQuickPlanetTableBody')
            ];

            var list = (this.activeChartData && this.activeChartData.planet_table) ? this.activeChartData.planet_table : AUTHENTIC_BUNDLE.planet_table;
            if (!list || !list.length) return;'''

new_planet_tbl = '''        renderPlanetTable: function() {
            var tbodies = [
                document.getElementById('mPlanetTableBody'),
                document.getElementById('mQuickPlanetTableBody')
            ];

            var list = (this.activeChartData && this.activeChartData.planet_table) ? this.activeChartData.planet_table : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.planet_table : null);
            if (!list || !list.length) {
                for (var t = 0; t < tbodies.length; t++) {
                    if (tbodies[t]) tbodies[t].innerHTML = '<tr><td colspan="6" style="text-align:center; padding:16px; color:var(--text-muted);">कुण्डली लोड होने पर स्पष्ट ग्रह स्थिति प्रदर्शित होगी।</td></tr>';
                }
                return;
            }'''

if old_planet_tbl in text:
    text = text.replace(old_planet_tbl, new_planet_tbl, 1)
    print("[OK] Fixed renderPlanetTable in mobile/index.html")

# 7. Fix renderMobileKundliPlanets
old_mkp = '''        renderMobileKundliPlanets: function() {
            this.renderPlanetTable();
        },'''

new_mkp = '''        renderMobileKundliPlanets: function() {
            this.renderPlanetTable();
            var svgWrap = document.getElementById('mMainKundliSvgWrap');
            if (svgWrap) {
                var houses = (this.activeChartData && this.activeChartData.houses) ? this.activeChartData.houses : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.houses : null);
                if (houses) {
                    svgWrap.innerHTML = this.generateDiamondSVG(houses, 280, 'D-1 लग्न कुण्डली');
                } else {
                    svgWrap.innerHTML = this.generateDiamondSVG({
                        1: { rashi: 1, sign: 'मेष', planets: [] }, 2: { rashi: 2, sign: 'वृषभ', planets: [] },
                        3: { rashi: 3, sign: 'मिथुन', planets: [] }, 4: { rashi: 4, sign: 'कर्क', planets: [] },
                        5: { rashi: 5, sign: 'सिंह', planets: [] }, 6: { rashi: 6, sign: 'कन्या', planets: [] },
                        7: { rashi: 7, sign: 'तुला', planets: [] }, 8: { rashi: 8, sign: 'वृश्चिक', planets: [] },
                        9: { rashi: 9, sign: 'धनु', planets: [] }, 10: { rashi: 10, sign: 'मकर', planets: [] },
                        11: { rashi: 11, sign: 'कुंभ', planets: [] }, 12: { rashi: 12, sign: 'मीन', planets: [] }
                    }, 280, 'D-1 लग्न कुण्डली (रिक्त खाका)');
                }
            }
        },'''

if old_mkp in text:
    text = text.replace(old_mkp, new_mkp, 1)
    print("[OK] Fixed renderMobileKundliPlanets in mobile/index.html")

# 8. Set window.VyasMobile = VyasMobile; explicitly
if 'window.VyasMobile = VyasMobile;' not in text:
    text = text.replace('VyasMobile.init();', 'window.VyasMobile = VyasMobile;\n    VyasMobile.init();')
    print("[OK] Explicitly set window.VyasMobile = VyasMobile;")

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done patching mobile/index.html.")

