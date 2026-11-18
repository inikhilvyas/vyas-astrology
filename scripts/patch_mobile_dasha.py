# -*- coding: utf-8 -*-
with open('mobile_dasha_full.js', 'r', encoding='utf-8') as f:
    orig = f.read()

replacement = """renderDashaTree() {
            var cfg = {
                order: ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"],
                years: { Ketu: 7, Venus: 20, Sun: 6, Moon: 10, Mars: 7, Rahu: 18, Jupiter: 16, Saturn: 19, Mercury: 17 },
                hi: { Ketu: "केतु", Venus: "शुक्र", Sun: "सूर्य", Moon: "चन्द्र", Mars: "मंगल", Rahu: "राहु", Jupiter: "गुरु", Saturn: "शनि", Mercury: "बुध" },
                en: { Ketu: "Ketu", Venus: "Venus", Sun: "Sun", Moon: "Moon", Mars: "Mars", Rahu: "Rahu", Jupiter: "Jupiter", Saturn: "Saturn", Mercury: "Mercury" }
            };
            window._VIM_CFG = cfg;

            var container = document.getElementById('mDashaTreeContainer');
            if (!container) return;

            var chart = this.activeChartData || window.AUTHENTIC_BUNDLE;
            var prof = (chart && chart.profile) ? chart.profile : {};
            var dobStr = prof.dob || "1984-11-23";
            var tobStr = prof.tob || "16:51";
            var birthMs = this.safeParseBirthMs(dobStr, tobStr);
            if (isNaN(birthMs)) birthMs = new Date("1984-11-23T16:51:00+05:30").getTime();
            var nowMs = Date.now();

            // Extract Moon Longitude dynamically from chart data
            var moonLon = 224.639; // Default: Anuradha 14°38' Scorpio (Nikhil Vyas)
            if (chart && chart.planet_table) {
                var rashiList = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
                var rashiEn = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"];
                for (var p = 0; p < chart.planet_table.length; p++) {
                    var pl = chart.planet_table[p];
                    var pName = (pl.p || pl.planet || '').toLowerCase();
                    if (pName.indexOf("चन्द्र") !== -1 || pName.indexOf("moon") !== -1) {
                        var rSign = pl.r || pl.sign || pl.rashi || '';
                        var rIdx = rashiList.indexOf(rSign);
                        if (rIdx === -1) rIdx = rashiEn.indexOf(rSign.toLowerCase());
                        if (rIdx !== -1) {
                            var dStr = pl.d || pl.degree || pl.dms || '0';
                            var mMatch = dStr.match(/([0-9]+)\s*°\s*([0-9]+)?\s*'?\s*([0-9]+)?/);
                            if (mMatch) {
                                var deg = parseFloat(mMatch[1] || 0);
                                var min = parseFloat(mMatch[2] || 0);
                                var sec = parseFloat(mMatch[3] || 0);
                                moonLon = (rIdx * 30.0) + deg + (min / 60.0) + (sec / 3600.0);
                            }
                        }
                        break;
                    }
                }
            } else if (chart && chart.planets && chart.planets.Moon) {
                var mp = chart.planets.Moon;
                moonLon = (typeof mp.longitude === 'number') ? mp.longitude : (typeof mp.lon === 'number' ? mp.lon : (mp.full_degree || 224.639));
            }

            // Authentic Parashari Vimshottari Calculation from Moon Lon
            var NAK_SPAN = 13.333333333333334;
            var nakIdx = Math.floor(moonLon / NAK_SPAN) % 27;
            var degPassed = moonLon - (nakIdx * NAK_SPAN);
            var degRemaining = NAK_SPAN - degPassed;
            if (degRemaining < 0) degRemaining = 0.001;
            var fracRemaining = degRemaining / NAK_SPAN;

            var VIM_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"];
            var startLord = VIM_LORDS[nakIdx % 9];
            var startLordTotalYrs = cfg.years[startLord];
            var startBalanceYrs = fracRemaining * startLordTotalYrs;

            var mdLords = this.getSubLords(startLord);
            var cur = birthMs;
            var mdList = [];
            for (var i = 0; i < mdLords.length; i++) {
                var l = mdLords[i];
                var y = (i === 0) ? startBalanceYrs : cfg.years[l];
                var dur = y * 365.2425 * 86400000;
                var end = cur + dur;
                mdList.push({
                    lord: l,
                    startMs: cur,
                    endMs: end,
                    spanYears: y,
                    startDate: this.safeFmtDate(cur),
                    endDate: this.safeFmtDate(end),
                    isActive: (nowMs >= cur && nowMs < end)
                });
                cur = end;
            }
            window._MD_SCHEDULE = mdList;

            // Compute current active 5-level chain dynamically
            var activeMD = mdList.find(function(m) { return m.isActive; });
            if (!activeMD) activeMD = mdList[mdList.length - 1];

            var adLords = this.getSubLords(activeMD.lord);
            var mdDur = activeMD.endMs - activeMD.startMs;
            var adCur = activeMD.startMs;
            var activeAD = null;
            for (var j = 0; j < 9; j++) {
                var al = adLords[j];
                var adSpan = mdDur * (cfg.years[al] / 120.0);
                var adEnd = adCur + adSpan;
                if (nowMs >= adCur && nowMs < adEnd) {
                    activeAD = { lord: al, startMs: adCur, endMs: adEnd };
                    break;
                }
                adCur = adEnd;
            }
            if (!activeAD) activeAD = { lord: adLords[0], startMs: activeMD.startMs, endMs: activeMD.endMs };

            var pdLords = this.getSubLords(activeAD.lord);
            var adDurTotal = activeAD.endMs - activeAD.startMs;
            var pdCur = activeAD.startMs;
            var activePD = null;
            for (var k = 0; k < 9; k++) {
                var pl = pdLords[k];
                var pdSpan = adDurTotal * (cfg.years[pl] / 120.0);
                var pdEnd = pdCur + pdSpan;
                if (nowMs >= pdCur && nowMs < pdEnd) {
                    activePD = { lord: pl, startMs: pdCur, endMs: pdEnd };
                    break;
                }
                pdCur = pdEnd;
            }
            if (!activePD) activePD = { lord: pdLords[0], startMs: activeAD.startMs, endMs: activeAD.endMs };

            var sdLords = this.getSubLords(activePD.lord);
            var pdDurTotal = activePD.endMs - activePD.startMs;
            var sdCur = activePD.startMs;
            var activeSD = null;
            for (var s = 0; s < 9; s++) {
                var sl = sdLords[s];
                var sdSpan = pdDurTotal * (cfg.years[sl] / 120.0);
                var sdEnd = sdCur + sdSpan;
                if (nowMs >= sdCur && nowMs < sdEnd) {
                    activeSD = { lord: sl, startMs: sdCur, endMs: sdEnd };
                    break;
                }
                sdCur = sdEnd;
            }
            if (!activeSD) activeSD = { lord: sdLords[0], startMs: activePD.startMs, endMs: activePD.endMs };

            var prLords = this.getSubLords(activeSD.lord);
            var sdDurTotal = activeSD.endMs - activeSD.startMs;
            var prCur = activeSD.startMs;
            var activePR = null;
            for (var r = 0; r < 9; r++) {
                var prl = prLords[r];
                var prSpan = sdDurTotal * (cfg.years[prl] / 120.0);
                var prEnd = prCur + prSpan;
                if (nowMs >= prCur && nowMs < prEnd) {
                    activePR = { lord: prl, startMs: prCur, endMs: prEnd };
                    break;
                }
                prCur = prEnd;
            }
            if (!activePR) activePR = { lord: prLords[0], startMs: activeSD.startMs, endMs: activeSD.endMs };

            // Render Banner
            var banner = document.getElementById('activeDashaChainVal');
            if (banner) {
                banner.innerHTML = '<span style="color:#d4af37; font-weight:800;">' + cfg.hi[activeMD.lord] + ' (MD)</span> ➔ ' +
                    '<span style="color:#60a5fa; font-weight:800;">' + cfg.hi[activeAD.lord] + ' (AD)</span> ➔ ' +
                    '<span style="color:#f87171; font-weight:800;">' + cfg.hi[activePD.lord] + ' (PD)</span> ➔ ' +
                    '<span style="color:#a78bfa; font-weight:800;">' + cfg.hi[activeSD.lord] + ' (SD)</span> ➔ ' +
                    '<span style="color:#34d399; font-weight:800;">' + cfg.hi[activePR.lord] + ' (PR)</span> ' +
                    '<span style="font-size:0.70rem; color:#10b981; font-weight:800; background:rgba(16,185,129,0.15); padding:2px 6px; border-radius:4px; margin-left:6px;">सक्रिय 5-स्तरीय चक्र</span>';
            }

            var html = '';
            for (var m = 0; m < mdList.length; m++) {
                var md = mdList[m];
                var isActive = md.isActive;
                var rowClass = isActive ? 'active-row' : '';
                var stLabel = isActive ? 'सक्रिय (Active Right Now)' : (md.endMs < nowMs ? 'सम्पूर्ण' : 'आगामी');
                var stColor = isActive ? '#10b981' : (md.endMs < nowMs ? 'var(--text-muted)' : '#60a5fa');

                html += '<div class="dasha-node ' + rowClass + '" id="m_node_md_' + m + '">' +
                    '<div style="display:flex; align-items:center;">' +
                        '<button class="dasha-exp-btn" id="m_btn_md_' + m + '" onclick="VyasMobile.toggleDashaChildren(\\'md\\', ' + m + ')">+</button>' +
                        '<span class="dasha-level-badge dasha-badge-md">MD</span>' +
                        '<b>' + cfg.hi[md.lord] + ' (' + md.lord + ')</b>' +
                    '</div>' +
                    '<div style="display:flex; align-items:center; gap:8px;">' +
                        '<span style="font-family:var(--font-mono); font-size:0.68rem;">' + md.startDate + ' ➔ ' + md.endDate + '</span>' +
                        '<span style="color:' + stColor + '; font-weight:700; font-size:0.68rem;">' + stLabel + '</span>' +
                    '</div>' +
                '</div>' +
                '<div id="m_children_md_' + m + '" style="display:none; padding-left:14px; background:rgba(0,0,0,0.02);"></div>';
            }
            container.innerHTML = html;

            // Auto-expand truly active Mahadasha
            var activeMDIdx = mdList.findIndex(function(m) { return m.isActive; });
            if (activeMDIdx !== -1) {
                var self = this;
                setTimeout(function() {
                    self.toggleDashaChildren('md', activeMDIdx);
                }, 100);
            }
        }"""

for path in ['mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    if orig in c:
        c = c.replace(orig, replacement.strip(), 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'✓ Successfully updated {path}')
    else:
        print(f'Original block not found in {path}')
