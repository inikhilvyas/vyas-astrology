import re, os

def patch_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Head scripts with versioning
    head_old = '<script src="js/vyas_sutras_bank.js" defer></script>\n    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>\n    <script src="js/vyas_daivagya_engine.js"></script>\n    <script src="js/vyas_chart_renderers.js"></script>'
    head_new = '<script src="js/vyas_sutras_bank.js?v=5.2.0"></script>\n    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>\n    <script src="js/vyas_daivagya_engine.js?v=5.2.0"></script>\n    <script src="js/vyas_chart_renderers.js?v=5.2.0"></script>\n    <script src="js/vyas_bhavat_bhavam.js?v=5.2.0"></script>\n    <script src="js/vyas_kp_horary_solver.js?v=5.2.0"></script>\n    <script src="js/vyas_treatise_sutras.js?v=5.2.0"></script>\n    <script src="js/vyas_treatise_engine.js?v=5.2.0"></script>'
    if head_old in c:
        c = c.replace(head_old, head_new)
        print('Updated head scripts in index.html')
    else:
        print('Warning: head_old not found in index.html')

    # 2. Add evalBhavatBhavamUI to VyasDesktop
    target_render_kp = 'kpBox.innerHTML = htmlKp;\n                }\n            },'
    bhavat_method = '''kpBox.innerHTML = htmlKp;
                }
            },

            evalBhavatBhavamUI() {
                var baseY = document.getElementById('bbBaseYSelect') ? document.getElementById('bbBaseYSelect').value : 2;
                var relX = document.getElementById('bbRelativeXSelect') ? document.getElementById('bbRelativeXSelect').value : 10;
                var resBox = document.getElementById('bbResultCard');
                if (!resBox) return;
                if (typeof window !== 'undefined' && window.VyasBhavatBhavam && typeof window.VyasBhavatBhavam.synthesizeBhavatBhavam === 'function') {
                    var syn = window.VyasBhavatBhavam.synthesizeBhavatBhavam(this.activeChartData, baseY, relX);
                    var html = '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:6px;">' +
                        '<div>' +
                        '<b style="color:#d4af37; font-size:1.05rem;">🎯 परिणामी भाव: ' + syn.calc.resultName + '</b>' +
                        '<code style="color:#38bdf8; font-size:0.80rem; margin-left:8px; background:rgba(56,189,248,0.1); padding:2px 6px; border-radius:4px;">' + syn.calc.formula + '</code>' +
                        '</div>' +
                        '<span style="background:rgba(212,175,55,0.15); color:#d4af37; padding:3px 10px; border-radius:12px; font-weight:800; font-size:0.75rem;">' + (syn.isXfromX ? 'X से X प्रभाव' : 'सापेक्ष भाव सिद्धि') + '</span>' +
                        '</div>' +
                        '<div style="font-size:0.82rem; color:var(--text-secondary); margin:10px 0; line-height:1.7;">' +
                        '<b>राशि:</b> <span style="color:var(--text-primary); font-weight:700;">' + syn.zSign + '</span> • ' +
                        '<b>भावेश:</b> <span style="color:var(--text-primary); font-weight:700;">' + syn.zLord + '</span> • ' +
                        '<b>प्लेसिडस CSL:</b> <b style="color:#f59e0b; background:rgba(245,158,11,0.15); padding:2px 8px; border-radius:4px;">' + syn.csl + '</b> (कस्प भोगांश: ' + syn.cDeg + ')<br>' +
                        '<b>शास्त्रीय सम्बन्ध व प्रभाव:</b> ' + syn.relation + '<br>' +
                        '<p style="margin:8px 0 0 0; font-size:0.84rem; color:var(--text-primary); line-height:1.6; background:rgba(15,23,42,0.5); padding:10px 12px; border-radius:6px; border-left:3px solid #d4af37;">' + syn.synthesis + '</p>' +
                        '</div>';
                    if (syn.isXfromX && syn.xFromXDetail) {
                        html += '<div style="margin-top:10px; padding:10px 12px; background:rgba(56,189,248,0.08); border-left:3px solid #38bdf8; border-radius:6px; font-size:0.80rem; line-height:1.6;">' +
                            '<b style="color:#38bdf8;">✦ विशेष शास्त्रीय सूत्र (X से X प्रभाव): ' + syn.xFromXDetail.rule + '</b><br>' +
                            '<span style="color:var(--text-secondary);">' + syn.xFromXDetail.desc + '</span><br>' +
                            '<span style="color:#94a3b8; font-size:0.74rem;">(संदर्भ ग्रन्थ: ' + syn.xFromXDetail.shastra + ')</span>' +
                            '</div>';
                    }
                    resBox.innerHTML = html;
                } else {
                    resBox.innerHTML = '<div style="color:var(--text-muted); font-size:0.82rem; padding:12px; text-align:center;">भावात् भावम् इंजन लोड हो रहा है...</div>';
                }
            },'''
    if target_render_kp in c:
        c = c.replace(target_render_kp, bhavat_method)
        print('Added evalBhavatBhavamUI to VyasDesktop in index.html')
    else:
        print('Warning: target_render_kp not found in index.html')

    # 3. Add auto-recompute for stale/legacy localStorage in index.html
    old_store_check = '''var stored = localStorage.getItem('vyas_active_profile');
                    if (stored) {
                        var data = JSON.parse(stored);
                        if (data && data.profile && data.profile.name && data.profile.name !== 'अतिथि जातक (Guest)' && data.profile.dob) {
                            if (data.profile.asc_sign === 'कन्या' || (data.profile.asc_dms && data.profile.asc_dms.indexOf("26°55") !== -1)) {
                                data = this.computeMathematicalKundli(data.profile.name, data.profile.dob, data.profile.tob || '12:00', data.profile.city || '', data.profile.gender || 'Male', data.profile.lat, data.profile.lon);
                            }'''

    new_store_check = '''var stored = localStorage.getItem('vyas_active_profile');
                    if (stored) {
                        var data = JSON.parse(stored);
                        if (data && data.profile && data.profile.name && data.profile.name !== 'अतिथि जातक (Guest)' && data.profile.dob) {
                            var needsRecomp = false;
                            if (!data._engine_ver || data._engine_ver < 5.2) needsRecomp = true;
                            if (data.kp && data.kp.cusps && data.kp.cusps.length >= 2) {
                                if (data.kp.cusps[0].deg === data.kp.cusps[1].deg || !data.kp.cusps[0].longitude) needsRecomp = true;
                            }
                            if (needsRecomp || data.profile.asc_sign === 'कन्या' || (data.profile.asc_dms && data.profile.asc_dms.indexOf("26°55") !== -1)) {
                                data = this.computeMathematicalKundli(data.profile.name, data.profile.dob, data.profile.tob || '12:00', data.profile.city || '', data.profile.gender || 'Male', data.profile.lat, data.profile.lon);
                            }'''

    if old_store_check in c:
        c = c.replace(old_store_check, new_store_check)
        print('Updated vyas_active_profile cache invalidation in index.html')
    else:
        print('Warning: old_store_check not found')

    # Priority 2: fromVault cache check
    old_vault_check = '''if (fromVault.profile.asc_sign === 'कन्या' || (fromVault.profile.asc_dms && fromVault.profile.asc_dms.indexOf("26°55") !== -1)) {
                                fromVault = this.computeMathematicalKundli(fromVault.profile.name, fromVault.profile.dob, fromVault.profile.tob || '12:00', fromVault.profile.city || '', fromVault.profile.gender || 'Male', fromVault.profile.lat, fromVault.profile.lon);
                            }'''
    new_vault_check = '''var needsRecompV = false;
                            if (!fromVault._engine_ver || fromVault._engine_ver < 5.2) needsRecompV = true;
                            if (fromVault.kp && fromVault.kp.cusps && fromVault.kp.cusps.length >= 2) {
                                if (fromVault.kp.cusps[0].deg === fromVault.kp.cusps[1].deg || !fromVault.kp.cusps[0].longitude) needsRecompV = true;
                            }
                            if (needsRecompV || fromVault.profile.asc_sign === 'कन्या' || (fromVault.profile.asc_dms && fromVault.profile.asc_dms.indexOf("26°55") !== -1)) {
                                fromVault = this.computeMathematicalKundli(fromVault.profile.name, fromVault.profile.dob, fromVault.profile.tob || '12:00', fromVault.profile.city || '', fromVault.profile.gender || 'Male', fromVault.profile.lat, fromVault.profile.lon);
                            }'''
    if old_vault_check in c:
        c = c.replace(old_vault_check, new_vault_check)
        print('Updated fromVault cache invalidation in index.html')

    # userVault check in init()
    old_init_vault = '''if (userVault.profile.asc_sign === 'कन्या' || (userVault.profile.asc_dms && userVault.profile.asc_dms.indexOf("26°55") !== -1)) {
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
                    }'''
    new_init_vault = '''var needsRecompU = false;
                    if (!userVault._engine_ver || userVault._engine_ver < 5.2) needsRecompU = true;
                    if (userVault.kp && userVault.kp.cusps && userVault.kp.cusps.length >= 2) {
                        if (userVault.kp.cusps[0].deg === userVault.kp.cusps[1].deg || !userVault.kp.cusps[0].longitude) needsRecompU = true;
                    }
                    if (needsRecompU || userVault.profile.asc_sign === 'कन्या' || (userVault.profile.asc_dms && userVault.profile.asc_dms.indexOf("26°55") !== -1)) {
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
                    }'''
    if old_init_vault in c:
        c = c.replace(old_init_vault, new_init_vault)
        print('Updated init userVault cache invalidation in index.html')

    # 4. In computeMathematicalKundli: stamp _engine_ver: 5.2, set 1-based indexing on kpCusps, and evaluate bhavat_bhavam
    old_final_bundle = '''                        kp: {
                        cusps: kpCusps,
                        planets: kpPlanets
                    },'''
    new_final_bundle = '''                        _engine_ver: 5.2,
                    kp: {
                        cusps: kpCusps,
                        planets: kpPlanets
                    },
                    bhavat_bhavam: (typeof window !== 'undefined' && window.VyasBhavatBhavam && typeof window.VyasBhavatBhavam.evaluateAll === 'function') ? window.VyasBhavatBhavam.evaluateAll({ charts: charts, planet_table: planetTable, kp: { cusps: kpCusps, planets: kpPlanets } }) : null,'''
    if old_final_bundle in c:
        c = c.replace(old_final_bundle, new_final_bundle)
        print('Updated finalBundle in index.html with _engine_ver 5.2 and bhavat_bhavam')

    # In kpCusps push:
    old_kp_push = '''                    kpCusps.push({
                        cusp: String(c),
                        sign: kpL.sign,
                        deg: cDms,
                        rl: kpL.rl,
                        nl: kpL.nl,
                        sl: kpL.sl,
                        ssl: kpL.ssl,
                        longitude: cLon
                    });'''
    new_kp_push = '''                    var cuspItem = {
                        cusp: String(c),
                        house: c,
                        sign: kpL.sign,
                        deg: cDms,
                        rl: kpL.rl,
                        nl: kpL.nl,
                        sl: kpL.sl,
                        ssl: kpL.ssl,
                        star: kpL.nl,
                        subLord: kpL.sl,
                        longitude: cLon
                    };
                    kpCusps.push(cuspItem);
                    kpCusps[c] = cuspItem;'''
    if old_kp_push in c:
        c = c.replace(old_kp_push, new_kp_push)
        print('Updated kpCusps push with 1-based indexing and star/subLord in index.html')

    # Pre-populate bhavatbhavam and prashna in init()
    old_init_render = '''this.renderKP();
                    this.renderJaimini();'''
    new_init_render = '''this.renderKP();
                    this.renderJaimini();
                    this.evalBhavatBhavamUI();
                    this.calculatePrashna();'''
    if old_init_render in c:
        c = c.replace(old_init_render, new_init_render)
        print('Pre-populated bhavatbhavam and prashna in index.html init()')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)

def patch_mobile_files():
    mobile_files = [
        'mobile/index.html',
        'static/mobile/index.html',
        'android_app/app/src/main/assets/mobile/index.html'
    ]
    for mf in mobile_files:
        if not os.path.exists(mf):
            print('File not found:', mf)
            continue
        with open(mf, 'r', encoding='utf-8') as f:
            mc = f.read()

        # Update cache check in loadProfile
        old_mob_lp = '''                if (!chart) {
                    try {
                        var saved = localStorage.getItem('vyas_active_profile');
                        if (saved) chart = JSON.parse(saved);
                    } catch (e) { }
                }'''
        new_mob_lp = '''                if (!chart) {
                    try {
                        var saved = localStorage.getItem('vyas_active_profile');
                        if (saved) {
                            chart = JSON.parse(saved);
                            if (chart && (!chart._engine_ver || chart._engine_ver < 5.2 || (chart.kp && chart.kp.cusps && chart.kp.cusps.length >= 2 && chart.kp.cusps[0].deg === chart.kp.cusps[1].deg))) {
                                if (chart.profile && chart.profile.dob && typeof this.computeMathematicalKundli === 'function') {
                                    chart = this.computeMathematicalKundli(chart.profile.name, chart.profile.dob, chart.profile.tob || '12:00', chart.profile.city || '', chart.profile.gender || 'Male', chart.profile.lat, chart.profile.lon);
                                }
                            }
                        }
                    } catch (e) { }
                }'''
        if old_mob_lp in mc:
            mc = mc.replace(old_mob_lp, new_mob_lp)
            print('Updated loadProfile cache check in', mf)

        # Update mobile kp push
        old_mkp_push = '''                    kpCusps.push({
                        cusp: String(c),
                        sign: kpL.sign,
                        deg: cDms,
                        rl: kpL.rl,
                        nl: kpL.nl,
                        sl: kpL.sl,
                        ssl: kpL.ssl,
                        longitude: cLon
                    });'''
        new_mkp_push = '''                    var cuspItem = {
                        cusp: String(c),
                        house: c,
                        sign: kpL.sign,
                        deg: cDms,
                        rl: kpL.rl,
                        nl: kpL.nl,
                        sl: kpL.sl,
                        ssl: kpL.ssl,
                        star: kpL.nl,
                        subLord: kpL.sl,
                        longitude: cLon
                    };
                    kpCusps.push(cuspItem);
                    kpCusps[c] = cuspItem;'''
        if old_mkp_push in mc:
            mc = mc.replace(old_mkp_push, new_mkp_push)
            print('Updated kpCusps in', mf)

        # Update finalBundle
        old_m_bundle = '''                        kp: {
                        cusps: kpCusps,
                        planets: kpPlanets
                    },'''
        new_m_bundle = '''                        _engine_ver: 5.2,
                    kp: {
                        cusps: kpCusps,
                        planets: kpPlanets
                    },
                    bhavat_bhavam: (typeof window !== 'undefined' && window.VyasBhavatBhavam && typeof window.VyasBhavatBhavam.evaluateAll === 'function') ? window.VyasBhavatBhavam.evaluateAll({ charts: charts, planet_table: planetTable, kp: { cusps: kpCusps, planets: kpPlanets } }) : null,'''
        if old_m_bundle in mc:
            mc = mc.replace(old_m_bundle, new_m_bundle)
            print('Updated finalBundle in', mf)

        with open(mf, 'w', encoding='utf-8') as f:
            f.write(mc)

if __name__ == '__main__':
    patch_index_html()
    patch_mobile_files()
