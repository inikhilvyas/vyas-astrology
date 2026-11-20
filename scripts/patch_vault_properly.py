with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = "openSavedProfilesModal() {"
end_marker = "loadKalapurushaChart() {"

pos_start = html.find(start_marker)
pos_end = html.find(end_marker)

print("pos_start:", pos_start, "pos_end:", pos_end)
if pos_start != -1 and pos_end != -1 and pos_end > pos_start:
    vault_methods = '''// UNIFIED KUNDLI VAULT & MULTI-TENANT ISOLATION
        getUserProfilesList: function() {
            var list = [];
            var seen = {};

            function add(item, source) {
                if (!item || !item.name) return;
                var key = (item.name + "_" + (item.dob || "") + "_" + (item.tob || "")).toLowerCase();
                if (!seen[key]) {
                    seen[key] = true;
                    list.push({
                        name: item.name,
                        dob: item.dob || "",
                        tob: item.tob || "",
                        city: item.city || "",
                        gender: item.gender || "Male",
                        asc_sign: item.asc_sign || (item.profile ? item.profile.asc_sign : ""),
                        source: source,
                        raw: item
                    });
                }
            }

            // 1. Current active chart
            if (this.activeChartData && this.activeChartData.profile && this.activeChartData.profile.name && this.activeChartData.profile.name !== 'अतिथि जातक (Guest)') {
                add(this.activeChartData.profile, "सक्रिय (Active)");
            }

            // 2. User vault (email keyed)
            if (this.googleUser && this.googleUser.email) {
                var email = this.googleUser.email.trim().toLowerCase();
                try {
                    var uv = localStorage.getItem('vyas_user_vault_' + email);
                    if (uv) {
                        var parsed = JSON.parse(uv);
                        if (parsed && parsed.profile) add(parsed.profile, "क्लाउड वॉल्ट");
                    }
                } catch(e) {}

                try {
                    var fv = localStorage.getItem('vyas_family_vault_' + email);
                    if (fv) {
                        var parsedFam = JSON.parse(fv);
                        if (Array.isArray(parsedFam)) parsedFam.forEach(function(p) { add(p, "पारिवारिक वॉल्ट"); });
                    }
                } catch(e) {}
            }

            // 3. General family vault
            try {
                var gfam = localStorage.getItem('vyas_family_vault');
                if (gfam) {
                    var parsedGFam = JSON.parse(gfam);
                    if (Array.isArray(parsedGFam)) parsedGFam.forEach(function(p) { add(p, "पारिवारिक"); });
                }
            } catch(e) {}

            // 4. Custom profiles
            try {
                var cust = localStorage.getItem('vyas_custom_profiles');
                if (cust) {
                    var parsedCust = JSON.parse(cust);
                    if (Array.isArray(parsedCust)) parsedCust.forEach(function(p) { add(p, "सुरक्षित"); });
                }
            } catch(e) {}

            return list;
        },

        saveCurrentChartToVault: function() {
            if (!this.activeChartData || !this.activeChartData.profile || this.activeChartData.profile.name === 'अतिथि जातक (Guest)') {
                alert("कृपया पहले किसी जातक की कुण्डली बनाएं या विवरण दर्ज करें।");
                return;
            }
            var prof = this.activeChartData.profile;
            var custom = [];
            try {
                var c = localStorage.getItem('vyas_custom_profiles');
                if (c) custom = JSON.parse(c);
            } catch(e) {}

            var exists = custom.some(function(x) { return x.name === prof.name && x.dob === prof.dob; });
            if (!exists) {
                custom.push({
                    name: prof.name,
                    dob: prof.dob,
                    tob: prof.tob,
                    city: prof.city,
                    gender: prof.gender || 'Male',
                    asc_sign: prof.asc_sign
                });
                try { localStorage.setItem('vyas_custom_profiles', JSON.stringify(custom)); } catch(e) {}
            }
            if (this.googleUser && this.googleUser.email) {
                var email = this.googleUser.email.trim().toLowerCase();
                try { localStorage.setItem('vyas_user_vault_' + email, JSON.stringify(this.activeChartData)); } catch(e) {}
            }
            alert("✓ कुण्डली (" + prof.name + ") सफलतापूर्वक आपकी सुरक्षित वॉल्ट में सहेज ली गई है!");
            this.openSavedProfilesModal();
        },

        deleteProfileFromVault: function(idx) {
            if (!confirm("क्या आप इस कुण्डली को सूची से हटाना चाहते हैं?")) return;
            var list = this.getUserProfilesList();
            var item = list[idx];
            if (!item) return;

            try {
                var custom = JSON.parse(localStorage.getItem('vyas_custom_profiles') || '[]');
                custom = custom.filter(function(x) { return !(x.name === item.name && x.dob === item.dob); });
                localStorage.setItem('vyas_custom_profiles', JSON.stringify(custom));
            } catch(e) {}

            try {
                var fam = JSON.parse(localStorage.getItem('vyas_family_vault') || '[]');
                fam = fam.filter(function(x) { return !(x.name === item.name && x.dob === item.dob); });
                localStorage.setItem('vyas_family_vault', JSON.stringify(fam));
            } catch(e) {}

            this.openSavedProfilesModal();
        },

        loadVaultProfileByIndex: function(idx) {
            var list = this.getUserProfilesList();
            var item = list[idx];
            if (!item) return;

            var newChart = this.computeMathematicalKundli(item.name, item.dob, item.tob, item.city, item.gender);
            this.activeChartData = newChart;
            try { localStorage.setItem('vyas_active_profile', JSON.stringify(newChart)); } catch(e) {}

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
            alert("✓ जातक " + item.name + " की कुण्डली (" + newChart.profile.asc_sign + " लग्न) सक्रिय हो गई है।");
        },

        loadCustomProfile: function(index) {
            this.loadVaultProfileByIndex(index);
        },

        openSavedProfilesModal() {
            var modal = document.getElementById('modalSavedProfiles');
            var body = document.getElementById('savedProfilesListBody');
            if (!modal || !body) return;

            var list = this.getUserProfilesList();
            var html = '<div style="display:flex; flex-direction:column; gap:10px;">';

            html += '<div style="display:flex; justify-content:space-between; align-items:center; background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.25); border-radius:8px; padding:10px 14px; margin-bottom:8px;">' +
                        '<div>' +
                            '<b style="color:#d4af37; font-size:0.86rem;">सुरक्षित कुण्डली वॉल्ट (कुल: ' + list.length + ' चार्ट)</b><br>' +
                            '<span style="font-size:0.75rem; color:#94a3b8;">क्लाउड व लोकल वॉल्ट में सुरक्षित समस्त कुण्डलियाँ</span>' +
                        '</div>' +
                        '<button class="header-btn primary" onclick="VyasDesktop.saveCurrentChartToVault()" style="font-size:0.75rem; padding:6px 12px; white-space:nowrap;">💾 वर्तमान चार्ट सहेजें</button>' +
                    '</div>';

            if (list.length > 0) {
                for (var i = 0; i < list.length; i++) {
                    var p = list[i];
                    var isActive = (this.activeChartData && this.activeChartData.profile && this.activeChartData.profile.name === p.name && this.activeChartData.profile.dob === p.dob);
                    html += '<div style="background:' + (isActive ? 'rgba(16,185,129,0.1)' : 'var(--bg-card)') + '; border:1px solid ' + (isActive ? '#10b981' : 'var(--border-subtle)') + '; padding:12px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">' +
                        '<div>' +
                            '<b style="color:' + (isActive ? '#10b981' : 'var(--primary-navy)') + '; font-size:0.92rem;">' + (p.name || 'सुरक्षित जातक') + (isActive ? ' <span style="font-size:0.72rem; background:#10b981; color:#fff; padding:2px 6px; border-radius:10px; margin-left:6px;">सक्रिय (Active)</span>' : '') + '</b><br>' +
                            '<span style="font-size:0.78rem; color:var(--text-secondary);">' + (p.dob || '') + ' ' + (p.tob || '') + ' • ' + (p.city || '') + (p.asc_sign ? ' • ' + p.asc_sign + ' लग्न' : '') + '</span>' +
                        '</div>' +
                        '<div style="display:flex; gap:6px;">' +
                            (!isActive ? '<button class="header-btn" onclick="VyasDesktop.loadVaultProfileByIndex(' + i + ')" style="font-size:0.78rem; padding:4px 10px;">लोड करें</button>' : '<span style="font-size:0.78rem; color:#10b981; font-weight:700;">प्रदर्शित ✓</span>') +
                            '<button onclick="VyasDesktop.deleteProfileFromVault(' + i + ')" style="background:none; border:1px solid rgba(239,68,68,0.4); color:#ef4444; border-radius:6px; padding:4px 8px; font-size:0.75rem; cursor:pointer;" title="हटाएं">✕</button>' +
                        '</div>' +
                    '</div>';
                }
            } else {
                html += '<div style="padding:28px 16px; text-align:center; color:var(--text-muted); font-size:0.88rem;">' +
                    '<div style="font-size:1.8rem; margin-bottom:8px;">📜</div>' +
                    'अभी कोई सुरक्षित कुण्डली उपलब्ध नहीं है。<br>ऊपर <b>"💾 वर्तमान चार्ट सहेजें"</b> अथवा <b>"+ नई कुण्डली"</b> से नई जन्मपत्रिका जोड़ें।</div>';
            }
            html += '<div style="margin-top:12px;">' +
                '<button onclick="VyasDesktop.openNewProfileModal(); VyasDesktop.closeModals();" class="header-btn primary" style="width:100%; padding:10px; font-size:0.92rem; font-weight:700; border-radius:6px;">+ नई कुण्डली प्रविष्ट करें</button>' +
            '</div>';
            html += '</div>';
            body.innerHTML = html;
            modal.classList.add('active');
            modal.style.display = 'flex';
        },

        '''
    html = html[:pos_start] + vault_methods + html[pos_end:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Successfully patched openSavedProfilesModal and unified vault system into index.html")
else:
    print("ERROR: Markers not matched cleanly.")

