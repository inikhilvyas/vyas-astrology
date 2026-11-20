with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clean handleGoogleCredentialResponse (remove isNikhil hardcoding)
old_hgcr = """            // STRICT MULTI-TENANT PRIVACY & ISOLATION:
            // 1. Immediately reset in-memory chart to prevent cross-session contamination
            this.activeChartData = null;

            var email = this.googleUser.email ? this.googleUser.email.trim().toLowerCase() : '';
            var isNikhil = (email.indexOf('nikhil') !== -1) ||
                           (this.googleUser.name && this.googleUser.name.toUpperCase().indexOf('NIKHIL') !== -1);

            if (isNikhil) {
                // Founder login: load founder vault or compute canonical Mesha Lagna chart
                var fromVault = this.loadFromUserVault();
                if (!fromVault || !fromVault.profile || fromVault.profile.asc_sign === 'कन्या' || (fromVault.profile.asc_dms && fromVault.profile.asc_dms.indexOf("26°55") !== -1)) {
                    fromVault = this.computeMathematicalKundli('Nikhil Vyas', '1984-11-23', '16:51', 'Pali, Rajasthan', 'Male', 25.7711, 73.3234);
                    this.saveToUserVault(fromVault);
                }
                this.activeChartData = fromVault;
                try { localStorage.setItem('vyas_active_profile', JSON.stringify(fromVault)); } catch(e) {}
            } else {
                // Regular logged-in user:
                // Purge any stale active profile belonging to someone else
                var curAct = localStorage.getItem('vyas_active_profile');
                if (curAct) {
                    try {
                        var cp = JSON.parse(curAct);
                        if (cp && cp.profile && (cp.profile.dob === '1984-11-23' || (cp.profile.name && cp.profile.name.toUpperCase().indexOf('NIKHIL') !== -1))) {
                            localStorage.removeItem('vyas_active_profile');
                        }
                    } catch(e) {
                        localStorage.removeItem('vyas_active_profile');
                    }
                }

                // Check THIS user's personal vault specifically: vyas_user_vault_<email>
                var userVault = this.loadFromUserVault();
                if (userVault && userVault.profile && userVault.profile.name && userVault.profile.name !== 'अतिथि जातक (Guest)') {
                    var isN = (userVault.profile.dob === '1984-11-23' || (userVault.profile.name && userVault.profile.name.toUpperCase().indexOf('NIKHIL') !== -1));
                    if (!isN) {
                        this.activeChartData = userVault;
                        try { localStorage.setItem('vyas_active_profile', JSON.stringify(this.activeChartData)); } catch(e) {}
                    } else {
                        // Purge contaminated vault
                        try { localStorage.removeItem('vyas_user_vault_' + email); } catch(e) {}
                        this.activeChartData = null;
                    }
                } else {
                    // No saved chart for this user yet
                    this.activeChartData = null;
                    try { localStorage.removeItem('vyas_active_profile'); } catch(e) {}
                }
            }"""

new_hgcr = """            // STRICT USER PRIVACY & ZERO HARDCODED SERVER DATA:
            // 1. Immediately reset in-memory chart
            this.activeChartData = null;

            var email = this.googleUser.email ? this.googleUser.email.trim().toLowerCase() : '';

            // 2. Load THIS user's personal vault: vyas_user_vault_<email>
            var userVault = this.loadFromUserVault();
            if (userVault && userVault.profile && userVault.profile.name && userVault.profile.name !== 'अतिथि जातक (Guest)') {
                // Auto-correct any legacy Kanya 26°55 calculation dynamically from user's own birth details
                if (userVault.profile.asc_sign === 'कन्या' || (userVault.profile.asc_dms && userVault.profile.asc_dms.indexOf("26°55") !== -1)) {
                    if (userVault.profile.dob) {
                        userVault = this.computeMathematicalKundli(
                            userVault.profile.name,
                            userVault.profile.dob,
                            userVault.profile.tob || '12:00',
                            userVault.profile.city || '',
                            userVault.profile.gender || 'Male',
                            userVault.profile.lat,
                            userVault.profile.lon
                        );
                        this.saveToUserVault(userVault);
                    }
                }
                this.activeChartData = userVault;
                try { localStorage.setItem('vyas_active_profile', JSON.stringify(this.activeChartData)); } catch(e) {}
            } else {
                // If user doesn't have an active chart in their vault, check if they have any saved profile in their list
                var list = (typeof this.getUserProfilesList === 'function') ? this.getUserProfilesList() : [];
                if (list.length > 0 && list[0].dob) {
                    var p0 = list[0];
                    var computed0 = this.computeMathematicalKundli(p0.name, p0.dob, p0.tob || '12:00', p0.city || '', p0.gender || 'Male');
                    if (computed0 && computed0.profile) {
                        this.activeChartData = computed0;
                        try { localStorage.setItem('vyas_active_profile', JSON.stringify(computed0)); } catch(e) {}
                        this.saveToUserVault(computed0);
                    }
                } else {
                    this.activeChartData = null;
                    try { localStorage.removeItem('vyas_active_profile'); } catch(e) {}
                }
            }"""

if old_hgcr in html:
    html = html.replace(old_hgcr, new_hgcr, 1)
    print("✓ Replaced handleGoogleCredentialResponse block")
else:
    print("! old_hgcr not found directly, checking normalized...")

# 2. Clean loadFromUserVault (remove isCurrentNikhil check)
old_lfuv = """        loadFromUserVault: function() {
            try {
                if (this.googleUser && this.googleUser.email) {
                    var email = this.googleUser.email.trim().toLowerCase();
                    var isCurrentNikhil = (email.indexOf('nikhil') !== -1) ||
                                          (this.googleUser.name && this.googleUser.name.toUpperCase().indexOf('NIKHIL') !== -1);
                    var vaultData = localStorage.getItem('vyas_user_vault_' + email);
                    if (vaultData) {
                        var parsed = JSON.parse(vaultData);
                        if (!isCurrentNikhil && parsed && parsed.profile && (parsed.profile.dob === '1984-11-23' || (parsed.profile.name && parsed.profile.name.toUpperCase().indexOf('NIKHIL') !== -1))) {
                            localStorage.removeItem('vyas_user_vault_' + email);
                            return null;
                        }
                        return parsed;
                    }
                }
            } catch(e) {}
            return null;
        },"""

new_lfuv = """        loadFromUserVault: function() {
            try {
                if (this.googleUser && this.googleUser.email) {
                    var email = this.googleUser.email.trim().toLowerCase();
                    var vaultData = localStorage.getItem('vyas_user_vault_' + email);
                    if (vaultData) {
                        return JSON.parse(vaultData);
                    }
                }
            } catch(e) {}
            return null;
        },"""

if old_lfuv in html:
    html = html.replace(old_lfuv, new_lfuv, 1)
    print("✓ Replaced loadFromUserVault block")

# 3. Clean loadStoredProfile (remove hardcoded 1984-11-23)
old_lsp_clean = """                                if (item && (item.asc_sign === 'कन्या' || (item.asc_dms && item.asc_dms.indexOf("26°55") !== -1))) {
                                    if (item.dob === '1984-11-23' || (item.name && item.name.toUpperCase().indexOf('NIKHIL') !== -1)) {
                                        item.asc_sign = 'मेष';
                                        item.asc_dms = "23°42'00\\\"";
                                        item.tob = item.tob || '16:51';
                                        item.city = item.city || 'Pali, Rajasthan';
                                        changed = true;
                                    } else if (item.dob) {
                                        var recomputed = VyasDesktop.computeMathematicalKundli(item.name, item.dob, item.tob || '12:00', item.city || '', item.gender || 'Male', item.lat, item.lon);
                                        if (recomputed && recomputed.profile) {
                                            item.asc_sign = recomputed.profile.asc_sign;
                                            item.asc_dms = recomputed.profile.asc_dms;
                                            changed = true;
                                        }
                                    }
                                }"""

new_lsp_clean = """                                if (item && (item.asc_sign === 'कन्या' || (item.asc_dms && item.asc_dms.indexOf("26°55") !== -1))) {
                                    if (item.dob) {
                                        var recomputed = VyasDesktop.computeMathematicalKundli(item.name, item.dob, item.tob || '12:00', item.city || '', item.gender || 'Male', item.lat, item.lon);
                                        if (recomputed && recomputed.profile) {
                                            item.asc_sign = recomputed.profile.asc_sign;
                                            item.asc_dms = recomputed.profile.asc_dms;
                                            changed = true;
                                        }
                                    }
                                }"""

if old_lsp_clean in html:
    html = html.replace(old_lsp_clean, new_lsp_clean, 1)
    print("✓ Replaced item auto-heal in loadStoredProfile")

old_p_clean = """                            if (p.asc_sign === 'कन्या' || (p.asc_dms && p.asc_dms.indexOf("26°55") !== -1)) {
                                if (p.dob === '1984-11-23' || (p.name && p.name.toUpperCase().indexOf('NIKHIL') !== -1)) {
                                    var recomputedNikhil = VyasDesktop.computeMathematicalKundli(p.name || 'Nikhil Vyas', '1984-11-23', '16:51', 'Pali', 'Male', 25.7711, 73.3234);
                                    if (recomputedNikhil) localStorage.setItem(k, JSON.stringify(recomputedNikhil));
                                } else if (p.dob) {
                                    var recomputedGen = VyasDesktop.computeMathematicalKundli(p.name, p.dob, p.tob || '12:00', p.city || '', p.gender || 'Male', p.lat, p.lon);
                                    if (recomputedGen) localStorage.setItem(k, JSON.stringify(recomputedGen));
                                }
                            }"""

new_p_clean = """                            if (p.asc_sign === 'कन्या' || (p.asc_dms && p.asc_dms.indexOf("26°55") !== -1)) {
                                if (p.dob) {
                                    var recomputedGen = VyasDesktop.computeMathematicalKundli(p.name, p.dob, p.tob || '12:00', p.city || '', p.gender || 'Male', p.lat, p.lon);
                                    if (recomputedGen) localStorage.setItem(k, JSON.stringify(recomputedGen));
                                }
                            }"""

if old_p_clean in html:
    html = html.replace(old_p_clean, new_p_clean, 1)
    print("✓ Replaced parsed.profile auto-heal in loadStoredProfile")

# 4. Clean pData in loadStoredProfile
old_pdata = """                            var pData = JSON.parse(stored);
                            if (pData && pData.profile && pData.profile.dob) {
                                var isN = (pData.profile.dob === '1984-11-23' || (pData.profile.name && pData.profile.name.toUpperCase().indexOf('NIKHIL') !== -1));
                                var fresh = isN
                                    ? this.computeMathematicalKundli(pData.profile.name, '1984-11-23', '16:51', 'Pali', 'Male', 25.7711, 73.3234)
                                    : this.computeMathematicalKundli(
                                        pData.profile.name,
                                        pData.profile.dob,
                                        pData.profile.tob || '12:00',
                                        pData.profile.city || '',
                                        pData.profile.gender || 'Male',
                                        pData.profile.lat || 25.0,
                                        pData.profile.lon || 73.0
                                    );
                                if (fresh) {
                                    localStorage.setItem('vyas_active_profile', JSON.stringify(fresh));
                                }"""

new_pdata = """                            var pData = JSON.parse(stored);
                            if (pData && pData.profile && pData.profile.dob) {
                                var fresh = this.computeMathematicalKundli(
                                    pData.profile.name,
                                    pData.profile.dob,
                                    pData.profile.tob || '12:00',
                                    pData.profile.city || '',
                                    pData.profile.gender || 'Male',
                                    pData.profile.lat || 25.0,
                                    pData.profile.lon || 73.0
                                );
                                if (fresh) {
                                    localStorage.setItem('vyas_active_profile', JSON.stringify(fresh));
                                }"""

if old_pdata in html:
    html = html.replace(old_pdata, new_pdata, 1)
    print("✓ Replaced pData in loadStoredProfile")

# 5. Clean fromVault in loadStoredProfile Case 1
old_fv_clean = """                        if (fromVault.profile.asc_sign === 'कन्या' || (fromVault.profile.asc_dms && fromVault.profile.asc_dms.indexOf("26°55") !== -1)) {
                            if (fromVault.profile.dob === '1984-11-23' || (fromVault.profile.name && fromVault.profile.name.toUpperCase().indexOf('NIKHIL') !== -1)) {
                                fromVault = this.computeMathematicalKundli(fromVault.profile.name, '1984-11-23', '16:51', 'Pali', 'Male', 25.7711, 73.3234);
                            } else if (fromVault.profile.dob) {
                                fromVault = this.computeMathematicalKundli(fromVault.profile.name, fromVault.profile.dob, fromVault.profile.tob || '12:00', fromVault.profile.city || '', fromVault.profile.gender || 'Male', fromVault.profile.lat, fromVault.profile.lon);
                            }
                            try { localStorage.setItem('vyas_user_vault_' + this.googleUser.email.trim().toLowerCase(), JSON.stringify(fromVault)); } catch(e) {}
                        }"""

new_fv_clean = """                        if (fromVault.profile.asc_sign === 'कन्या' || (fromVault.profile.asc_dms && fromVault.profile.asc_dms.indexOf("26°55") !== -1)) {
                            if (fromVault.profile.dob) {
                                fromVault = this.computeMathematicalKundli(fromVault.profile.name, fromVault.profile.dob, fromVault.profile.tob || '12:00', fromVault.profile.city || '', fromVault.profile.gender || 'Male', fromVault.profile.lat, fromVault.profile.lon);
                            }
                            try { localStorage.setItem('vyas_user_vault_' + this.googleUser.email.trim().toLowerCase(), JSON.stringify(fromVault)); } catch(e) {}
                        }"""

if old_fv_clean in html:
    html = html.replace(old_fv_clean, new_fv_clean, 1)
    print("✓ Replaced fromVault in loadStoredProfile")

# 6. Clean data in loadStoredProfile Case 2
old_data_clean = """                            if (data.profile.asc_sign === 'कन्या' || (data.profile.asc_dms && data.profile.asc_dms.indexOf("26°55") !== -1)) {
                                if (data.profile.dob === '1984-11-23' || (data.profile.name && data.profile.name.toUpperCase().indexOf('NIKHIL') !== -1)) {
                                    data = this.computeMathematicalKundli(data.profile.name, '1984-11-23', '16:51', 'Pali', 'Male', 25.7711, 73.3234);
                                } else if (data.profile.dob) {
                                    data = this.computeMathematicalKundli(data.profile.name, data.profile.dob, data.profile.tob || '12:00', data.profile.city || '', data.profile.gender || 'Male', data.profile.lat, data.profile.lon);
                                }
                            }"""

new_data_clean = """                            if (data.profile.asc_sign === 'कन्या' || (data.profile.asc_dms && data.profile.asc_dms.indexOf("26°55") !== -1)) {
                                if (data.profile.dob) {
                                    data = this.computeMathematicalKundli(data.profile.name, data.profile.dob, data.profile.tob || '12:00', data.profile.city || '', data.profile.gender || 'Male', data.profile.lat, data.profile.lon);
                                }
                            }"""

if old_data_clean in html:
    html = html.replace(old_data_clean, new_data_clean, 1)
    print("✓ Replaced data in loadStoredProfile Case 2")

# 7. Clean getUserProfilesList sign === 'कन्या'
old_sign = """                    if (sign === 'कन्या' && (pDob === '1984-11-23' || pName.toUpperCase().indexOf('NIKHIL') !== -1)) {
                        sign = 'मेष';
                    }"""

new_sign = """                    if (sign === 'कन्या' && pDob) {
                        try {
                            var temp = VyasDesktop.computeMathematicalKundli(pName, pDob, pTob || '12:00', pCity, pGen);
                            if (temp && temp.profile) sign = temp.profile.asc_sign;
                        } catch(e) {}
                    }"""

if old_sign in html:
    html = html.replace(old_sign, new_sign, 1)
    print("✓ Replaced sign in getUserProfilesList")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html cleaned of all hardcoded kundli data!")

