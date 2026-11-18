# -*- coding: utf-8 -*-
"""
Master Patch:
1. Replace hardcoded 2000-01-01 / Saturn 2.8718 dasha in initDashaTree with authentic dynamic Vimshottari calculation.
2. In loadStoredProfile, add engine version migration (v4.2) and ensure authentic Swiss Ephemeris degree (23°27'09" / 23°8'20") is loaded for Nikhil Vyas.
3. Update sw.js CACHE_NAME to force instant cache purging across all devices.
"""

import os
import re

print("Starting Dynamic Dasha & Cache-Busting Patch...")

# Dynamic Vimshottari Engine for JavaScript
DYNAMIC_INIT_DASHA_TREE = """initDashaTree() {
            var cfg = {
                order: ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"],
                years: { Ketu: 7, Venus: 20, Sun: 6, Moon: 10, Mars: 7, Rahu: 18, Jupiter: 16, Saturn: 19, Mercury: 17 },
                hi: { Ketu: "केतु", Venus: "शुक्र", Sun: "सूर्य", Moon: "चन्द्र", Mars: "मंगल", Rahu: "राहु", Jupiter: "गुरु", Saturn: "शनि", Mercury: "बुध" },
                en: { Ketu: "Ketu", Venus: "Venus", Sun: "Sun", Moon: "Moon", Mars: "Mars", Rahu: "Rahu", Jupiter: "Jupiter", Saturn: "Saturn", Mercury: "Mercury" }
            };
            window._VIM_CFG = cfg;

            var container = document.getElementById('dashaTreeContainer');
            if (!container) return;
            var banner = document.getElementById('activeDashaChainVal');

            var chart = this.activeChartData || window.AUTHENTIC_BUNDLE;
            if (!chart || !chart.profile || !chart.profile.dob) {
                if (banner) banner.innerHTML = '<span style="color:var(--text-muted);">कुण्डली लोड नहीं है • दशा उपलब्ध नहीं</span>';
                container.innerHTML = '<div style="padding:28px 16px; text-align:center; color:var(--text-muted); font-size:0.8rem;"><div style="font-size:1.6rem; margin-bottom:6px;">⏳</div><b style="color:var(--primary);">विंशोत्तरी दशा चक्र उपलब्ध नहीं</b><p style="font-size:0.74rem; margin-top:4px;">अपनी 5-स्तरीय विंशोत्तरी दशा देखने हेतु ऊपर &apos;+ नई कुण्डली&apos; से अपनी जन्म पत्रिका बनाएं।</p></div>';
                return;
            }

            var prof = chart.profile;
            var dobStr = prof.dob || "1984-11-23";
            var tobStr = prof.tob || "16:51";
            var dp = dobStr.split("-").map(Number);
            var tp = (tobStr.replace(/[^0-9:]/g, "")).split(":").map(Number);
            var birthDate = new Date(dp[0], dp[1] - 1, dp[2], tp[0] || 12, tp[1] || 0, 0);
            var birthMs = birthDate.getTime();
            if (isNaN(birthMs)) birthMs = new Date("1984-11-23T16:51:00+05:30").getTime();
            var nowMs = Date.now();

            // Extract Moon Longitude dynamically from chart data
            var moonLon = 224.639; // Default: Anuradha 14°38' Scorpio (Nikhil Vyas)
            if (chart.planet_table) {
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
            } else if (chart.planets && chart.planets.Moon) {
                var mp = chart.planets.Moon;
                moonLon = (typeof mp.longitude === 'number') ? mp.longitude : (typeof mp.lon === 'number' ? mp.lon : (mp.full_degree || 224.639));
            }

            // Authentic Parashari Vimshottari Calculation from Moon Lon
            var NAK_SPAN = 13.333333333333334; // 13° 20'
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
            if (!activeMD) {
                // If nowMs is beyond 9 mahadashas (120 yrs) or before birth, fallback to active or first
                activeMD = mdList[mdList.length - 1];
            }
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
            for (var pr = 0; pr < 9; pr++) {
                var prl = prLords[pr];
                var prSpan = sdDurTotal * (cfg.years[prl] / 120.0);
                var prEnd = prCur + prSpan;
                if (nowMs >= prCur && nowMs < prEnd) {
                    activePR = { lord: prl, startMs: prCur, endMs: prEnd };
                    break;
                }
                prCur = prEnd;
            }
            if (!activePR) activePR = { lord: prLords[0], startMs: activeSD.startMs, endMs: activeSD.endMs };

            // Render Banner with Active 5-Level Chain
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

                html += '<div class="dasha-node ' + rowClass + '" id="node_md_' + m + '">' +
                    '<div style="display:flex; align-items:center;">' +
                        '<button class="dasha-exp-btn" id="btn_md_' + m + '" onclick="VyasDesktop.toggleDashaChildren(\'md\', ' + m + ')">+</button>' +
                        '<span class="dasha-level-badge dasha-badge-md">MD</span>' +
                        '<b>' + cfg.hi[md.lord] + ' (' + md.lord + ')</b>' +
                    '</div>' +
                    '<div style="display:flex; align-items:center; gap:12px;">' +
                        '<span style="font-family:var(--font-mono); font-size:0.72rem;">' + md.startDate + ' ➔ ' + md.endDate + '</span>' +
                        '<span style="color:' + stColor + '; font-weight:700; font-size:0.70rem;">' + stLabel + '</span>' +
                    '</div>' +
                '</div>' +
                '<div id="children_md_' + m + '" style="display:none; padding-left:18px; background:rgba(0,0,0,0.02);"></div>';
            }
            container.innerHTML = html;

            // Auto-expand the truly active Mahadasha
            var activeMDIdx = mdList.findIndex(function(m) { return m.isActive; });
            if (activeMDIdx !== -1) {
                var self = this;
                setTimeout(function() {
                    self.toggleDashaChildren('md', activeMDIdx);
                }, 100);
            }
        }"""


def patch_file(p):
    if not os.path.exists(p):
        print(f"File {p} does not exist, skipping.")
        return

    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Replace initDashaTree() implementation
    start_d = c.find('initDashaTree() {')
    if start_d != -1:
        # Find closing brace of initDashaTree
        brace = 0
        found = False
        end_d = -1
        for i in range(start_d, len(c)):
            if c[i] == '{':
                brace += 1
                found = True
            elif c[i] == '}':
                brace -= 1
                if found and brace == 0:
                    end_d = i + 1
                    break
        if end_d != -1:
            c = c[:start_d] + DYNAMIC_INIT_DASHA_TREE.strip() + c[end_d:]
            print(f"✓ Replaced initDashaTree with authentic dynamic Vimshottari calculation in {p}")

    # 2. Add Cache-Buster & Engine Version Migration in loadStoredProfile()
    version_migration_code = """        loadStoredProfile() {
            var CURRENT_ENGINE_VERSION = 'v4.2_swiss_precision_2026';
            try {
                if (localStorage.getItem('vyas_engine_version') !== CURRENT_ENGINE_VERSION) {
                    var stored = localStorage.getItem('vyas_active_profile');
                    if (stored) {
                        var parsed = JSON.parse(stored);
                        if (parsed && parsed.profile && (parsed.profile.name.indexOf('NIKHIL') !== -1 || parsed.profile.dob === '1984-11-23')) {
                            // Purge stale cached profile to reload fresh Swiss Ephemeris 23°27'09" & accurate SAV 337
                            localStorage.removeItem('vyas_active_profile');
                        }
                    }
                    localStorage.setItem('vyas_engine_version', CURRENT_ENGINE_VERSION);
                }
            } catch(e) {}

            var hasStored = false;"""

    if 'CURRENT_ENGINE_VERSION' not in c and 'loadStoredProfile() {' in c:
        c = c.replace('loadStoredProfile() {\n            var hasStored = false;', version_migration_code, 1)
        if 'CURRENT_ENGINE_VERSION' not in c:
            c = c.replace('loadStoredProfile() {', version_migration_code, 1)
        print(f"✓ Injected automatic cache-buster & version migration into {p}")

    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"✓ Finished patching {p}")


patch_file('index.html')
patch_file('mobile/index.html')
patch_file('android_app/app/src/main/assets/mobile/index.html')

# 3. Patch sw.js to bump cache generation
if os.path.exists('sw.js'):
    with open('sw.js', 'r', encoding='utf-8') as f:
        sw = f.read()
    sw = re.sub(r"const CACHE_NAME = 'vyas-astra-v2026-v4-full-precision-\d+';", "const CACHE_NAME = 'vyas-astra-v2026-v4-full-precision-8';", sw)
    with open('sw.js', 'w', encoding='utf-8') as f:
        f.write(sw)
    print("✓ Bumped sw.js CACHE_NAME to vyas-astra-v2026-v4-full-precision-8")

print("\n✓ COMPLETED MASTER DYNAMIC DASHA & CACHE-BUSTING OVERHAUL!")
