renderDashaTree() {
            var cfg = {
                order: ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"],
                years: { Ketu: 7, Venus: 20, Sun: 6, Moon: 10, Mars: 7, Rahu: 18, Jupiter: 16, Saturn: 19, Mercury: 17 },
                hi: { Ketu: "केतु", Venus: "शुक्र", Sun: "सूर्य", Moon: "चन्द्र", Mars: "मंगल", Rahu: "राहु", Jupiter: "गुरु", Saturn: "शनि", Mercury: "बुध" },
                en: { Ketu: "Ketu", Venus: "Venus", Sun: "Sun", Moon: "Moon", Mars: "Mars", Rahu: "Rahu", Jupiter: "Jupiter", Saturn: "Saturn", Mercury: "Mercury" }
            };
            window._VIM_CFG = cfg;

            var container = document.getElementById('mDashaTreeContainer');
            if (!container) return;

            // Safe parsing of birthMs - NEVER NaN in any mobile browser
            var prof = (this.activeChartData && this.activeChartData.profile) ? this.activeChartData.profile : {};
            var dobStr = prof.dob || "2000-01-01";
            var tobStr = prof.tob || "16:51";
            var birthMs = this.safeParseBirthMs(dobStr, tobStr);
            var saturnBalanceYrs = 2.8718;
            var nowMs = Date.now();

            var mdLords = this.getSubLords("Saturn");
            var cur = birthMs;
            var mdList = [];
            for (var i = 0; i < mdLords.length; i++) {
                var l = mdLords[i];
                var y = (i === 0) ? saturnBalanceYrs : cfg.years[l];
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
            var activeMD = mdList.find(function(m) { return m.isActive; }) || mdList[3];
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
            if (!activeAD) activeAD = { lord: "Saturn", startMs: activeMD.startMs, endMs: activeMD.endMs };

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
            if (!activePD) activePD = { lord: "Mars", startMs: activeAD.startMs, endMs: activeAD.endMs };

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
            if (!activeSD) activeSD = { lord: "Moon", startMs: activePD.startMs, endMs: activePD.endMs };

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
            if (!activePR) activePR = { lord: "Mercury", startMs: activeSD.startMs, endMs: activeSD.endMs };

            // Render Banner
            var banner = document.getElementById('activeDashaChainVal');
            if (banner) {
                banner.innerHTML = '<span style="color:#d4af37;">' + cfg.hi[activeMD.lord] + ' (MD)</span> ➔ ' +
                    '<span style="color:#60a5fa;">' + cfg.hi[activeAD.lord] + ' (AD)</span> ➔ ' +
                    '<span style="color:#f87171;">' + cfg.hi[activePD.lord] + ' (PD)</span> ➔ ' +
                    '<span style="color:#a78bfa;">' + cfg.hi[activeSD.lord] + ' (SD)</span> ➔ ' +
                    '<span style="color:#34d399;">' + cfg.hi[activePR.lord] + ' (PR)</span> ' +
                    '<span style="font-size:0.70rem; color:#10b981; font-weight:800; background:rgba(16,185,129,0.15); padding:2px 8px; border-radius:10px;">सक्रिय 5-स्तरीय चक्र</span>';
            }

            var html = '';
            for (var i = 0; i < mdList.length; i++) {
                var md = mdList[i];
                var isActive = md.isActive;
                var rowClass = isActive ? 'active-row' : '';
                var stLabel = isActive ? 'सक्रिय (Active)' : (md.endMs < nowMs ? 'सम्पूर्ण' : 'आगामी');
                var stColor = isActive ? '#10b981' : (md.endMs < nowMs ? 'var(--text-muted)' : '#60a5fa');

                html += '<div class="dasha-node ' + rowClass + '" id="m_node_md_' + i + '">' +
                    '<div style="display:flex; align-items:center;">' +
                        '<button class="dasha-exp-btn" id="m_btn_md_' + i + '" onclick="VyasMobile.toggleDashaChildren(\'md\', ' + i + ')">+</button>' +
                        '<span class="dasha-level-badge dasha-badge-md">MD</span>' +
                        '<b>' + cfg.hi[md.lord] + ' (' + md.lord + ')</b>' +
                    '</div>' +
                    '<div style="display:flex; align-items:center; gap:12px;">' +
                        '<span style="font-family:var(--font-mono); font-size:0.72rem;">' + md.startDate + ' ➔ ' + md.endDate + '</span>' +
                        '<span style="color:' + stColor + '; font-weight:700; font-size:0.70rem;">' + stLabel + '</span>' +
                    '</div>' +
                '</div>' +
                '<div id="m_children_md_' + i + '" style="display:none; padding-left:12px; margin-left:8px; border-left:2px solid var(--border-gold-soft); margin-bottom:8px;"></div>';
            }
            container.innerHTML = html;

            // Auto-expand active Venus MD safely
            var self = this;
            setTimeout(function() {
                self.toggleDashaChildren('md', 3);
            }, 100);
        }