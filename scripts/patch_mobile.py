import re
import os

def run_patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        d_lines = f.readlines()

    d_cmk_lines = d_lines[13839:14925]
    d_cmk = ''.join(d_cmk_lines) + '\n        },\n'

    with open('mobile/index.html', 'r', encoding='utf-8') as f:
        m_lines = f.readlines()

    # 1. Prepare new block for profile modals & computeMathematicalKundli
    new_profile_and_cmk = '''        openEditProfileModal() {
            var m = document.getElementById('mEditProfileModal');
            if (!m) return;
            document.getElementById('mEditModalTitle').innerText = "जन्म विवरण सम्पादित करें";
            var prof = (this.activeChartData && this.activeChartData.profile) ? this.activeChartData.profile : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.profile : {});
            document.getElementById('m_inp_name').value = prof.name || "";
            document.getElementById('m_inp_dob').value = prof.dob || "";

            var tobVal = prof.tob || "";
            var mMatch = tobVal.match(/^(\\d+:\\d+(?::\\d+)?)\\s*(AM|PM)?$/i);
            if (mMatch) {
                document.getElementById('m_inp_tob').value = mMatch[1] || "";
                if (mMatch[2]) {
                    document.getElementById('m_inp_ampm').value = mMatch[2].toUpperCase();
                }
            } else {
                document.getElementById('m_inp_tob').value = tobVal;
            }

            var cityInp = document.getElementById('m_inp_city');
            if (cityInp) {
                cityInp.value = prof.city || "";
                if (typeof prof.lat === 'number' && !isNaN(prof.lat)) cityInp.setAttribute('data-lat', prof.lat);
                if (typeof prof.lon === 'number' && !isNaN(prof.lon)) cityInp.setAttribute('data-lon', prof.lon);
            }
            document.getElementById('m_inp_gender').value = prof.gender || "Male";
            m.classList.add('active');
        },

        openNewProfileModal() {
            this.openEditProfileModal();
            document.getElementById('mEditModalTitle').innerText = "नई कुण्डली विवरण दर्ज करें";
            document.getElementById('m_inp_name').value = "";
            document.getElementById('m_inp_dob').value = "";
            document.getElementById('m_inp_tob').value = "";
            var cityInp = document.getElementById('m_inp_city');
            if (cityInp) {
                cityInp.value = "";
                cityInp.removeAttribute('data-lat');
                cityInp.removeAttribute('data-lon');
            }
            document.getElementById('m_inp_ampm').value = "PM";
        },

        useCurrentGPS(targetInputId) {
            var inp = document.getElementById(targetInputId);
            if (!navigator.geolocation) {
                alert("इस डिवाइस में GPS सपोर्ट उपलब्ध नहीं है।");
                return;
            }
            navigator.geolocation.getCurrentPosition(function(pos) {
                var lat = pos.coords.latitude;
                var lon = pos.coords.longitude;
                if (inp) {
                    inp.value = "GPS (" + lat.toFixed(4) + ", " + lon.toFixed(4) + ")";
                    inp.setAttribute('data-lat', lat);
                    inp.setAttribute('data-lon', lon);
                }
                alert("GPS स्थान सफलतापूर्वक सेट किया गया: " + lat.toFixed(4) + ", " + lon.toFixed(4));
            }, function(err) {
                alert("GPS लोकेशन प्राप्त नहीं हो सकी: " + err.message);
            }, { timeout: 10000, enableHighAccuracy: true });
        },

        submitProfileForm() {
            var name = document.getElementById('m_inp_name').value.trim() || "जातक";
            var dob = document.getElementById('m_inp_dob').value.trim();
            var tobRaw = document.getElementById('m_inp_tob').value.trim();
            var ampmEl = document.getElementById('m_inp_ampm');
            var tob = tobRaw;
            if (tob && !tob.match(/AM|PM/i) && ampmEl) {
                tob = tob + " " + ampmEl.value;
            }
            if (!tob) tob = "12:00 PM";
            var cityEl = document.getElementById('m_inp_city');
            var city = (cityEl && cityEl.value) ? cityEl.value.trim() : "नई दिल्ली";
            var gender = document.getElementById('m_inp_gender').value;

            var customLat = cityEl ? parseFloat(cityEl.getAttribute('data-lat')) : NaN;
            var customLon = cityEl ? parseFloat(cityEl.getAttribute('data-lon')) : NaN;

            if (!dob) {
                alert("कृपया जन्म दिनांक दर्ज करें।");
                return;
            }

            // Pure-JS Mathematical Ephemeris recalculation
            var newChart = this.computeMathematicalKundli(name, dob, tob, city, gender, customLat, customLon);
            if (!newChart || !newChart.profile) {
                alert("कुण्डली गणना विफल रही। कृपया जन्म विवरण पुनः जाँचें।");
                return;
            }

            this.activeChartData = newChart;
            this.activeChart = newChart;
            localStorage.setItem('vyas_active_profile', JSON.stringify(newChart));

            try {
                var saved = JSON.parse(localStorage.getItem('vyas_custom_profiles') || '[]');
                saved.push(newChart.profile);
                localStorage.setItem('vyas_custom_profiles', JSON.stringify(saved));
            } catch(e) {}

            this.loadProfile();
            this.renderChart('d1');
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderAshtakavarga();
            this.closeModals();
            alert("जातक " + name + " की जन्म कुण्डली (" + newChart.profile.asc_sign + " लग्न " + (newChart.profile.asc_dms || '') + ") की वास्तविक वैदिक गणना पूर्ण हो गई है!");
        },

''' + d_cmk

    # Replace lines 9039 to 10046 (inclusive)
    new_lines = m_lines[:9039] + [new_profile_and_cmk] + m_lines[10047:]
    content = ''.join(new_lines)

    # 2. Update CSS for app-main-viewport, m-card, m-table-wrap, and Ashtakavarga
    content = content.replace(
'''        /* 3. Main Viewport & Dedicated Separate Tab Views */
        .app-main-viewport {
            flex: 1;
            padding: 6px 8px calc(58px + env(safe-area-inset-bottom)) 8px;
            overflow-y: auto;
        }''',
'''        /* 3. Main Viewport & Dedicated Separate Tab Views */
        .app-main-viewport {
            flex: 1;
            padding: 6px 8px calc(58px + env(safe-area-inset-bottom)) 8px;
            overflow-y: auto;
            overflow-x: hidden;
            max-width: 100vw;
            box-sizing: border-box;
        }'''
    )

    content = content.replace(
'''        /* Mobile Card Design */
        .m-card {
            background: var(--bg-card);
            border: 1px solid var(--border-gold-soft);
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 10px;
            box-shadow: var(--card-shadow);
        }''',
'''        /* Mobile Card Design */
        .m-card {
            background: var(--bg-card);
            border: 1px solid var(--border-gold-soft);
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 10px;
            box-shadow: var(--card-shadow);
            max-width: 100%;
            overflow: hidden;
            box-sizing: border-box;
        }'''
    )

    old_table_css = '''        /* Tables & Lists */
        .m-table-wrap {
            width: 100%;
            overflow-x: auto;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
            margin-top: 6px;
        }
        .m-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.74rem;
            text-align: left;
        }
        .m-table th {
            background: var(--bg-surface);
            color: var(--primary);
            padding: 8px 6px;
            font-weight: 800;
            border-bottom: 1px solid var(--border-gold-soft);
            white-space: nowrap;
        }
        .m-table td {
            padding: 7px 6px;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-primary);
            white-space: nowrap;
        }

        /* Ashtakavarga Grids */
        .sav-grid-mobile {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            margin-bottom: 10px;
        }
        .sav-cell {
            background: var(--bg-card-alt);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 8px 4px;
            text-align: center;
        }
        .sav-cell.high { border-color: #10b981; }
        .sav-cell.good { border-color: var(--border-gold); }
        .sav-cell.low { border-color: #ef4444; }
        .sav-num {
            font-size: 1.25rem;
            font-weight: 900;
            line-height: 1.2;
        }'''

    new_table_css = '''        /* Tables & Lists */
        .m-table-wrap {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            display: block !important;
            box-sizing: border-box !important;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
            margin-top: 6px;
        }
        .m-table, .astronomy-table {
            width: 100%;
            min-width: 440px;
            border-collapse: collapse;
            font-size: 0.68rem;
            text-align: center;
        }
        .m-table th, .astronomy-table th {
            background: var(--bg-surface);
            color: var(--primary);
            padding: 6px 3px !important;
            font-weight: 800;
            border-bottom: 1px solid var(--border-gold-soft);
            white-space: nowrap;
            text-align: center !important;
            font-size: 0.68rem !important;
        }
        .m-table td, .astronomy-table td {
            padding: 5px 3px !important;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-primary);
            white-space: nowrap;
            text-align: center !important;
            font-size: 0.68rem !important;
        }

        /* Ashtakavarga Grids */
        .sav-grid-mobile {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            margin-bottom: 10px;
        }
        .sav-card, .sav-cell {
            background: var(--bg-card-alt);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 8px 4px;
            text-align: center;
        }
        .sav-card.sav-high, .sav-cell.high { border-color: #10b981; }
        .sav-card.sav-good, .sav-cell.good { border-color: var(--border-gold); }
        .sav-card.sav-low, .sav-cell.low { border-color: #ef4444; }
        .sav-score, .sav-num {
            font-size: 1.18rem;
            font-weight: 900;
            line-height: 1.2;
        }
        .sav-score.sav-high { color: #10b981; }
        .sav-score.sav-good { color: var(--accent-gold); }
        .sav-score.sav-low { color: #ef4444; }'''

    content = content.replace(old_table_css, new_table_css)

    # 3. Update Google Auth Prompt & Launch
    old_google_auth = '''        promptGoogleSignIn: function() {
            // If already verified and logged in, toggle profile popover/modal
            if (this.googleUser) {
                var pop = document.getElementById('userProfilePopover');
                if (pop) {
                    pop.style.display = (pop.style.display === 'none' || !pop.style.display) ? 'block' : 'none';
                    return;
                }
                var modal = document.getElementById('modalGoogleAuthMobile');
                if (modal) {
                    var unauth = document.getElementById('mGoogleUnauth');
                    var auth = document.getElementById('mGoogleAuth');
                    if (unauth) unauth.style.display = 'none';
                    if (auth) auth.style.display = 'block';
                    var nameEl = document.getElementById('mAuthName');
                    var emailEl = document.getElementById('mAuthEmail');
                    if (nameEl) nameEl.textContent = this.googleUser.name || 'सत्यापित PRO जातक';
                    if (emailEl) emailEl.textContent = this.googleUser.email || '';
                    modal.classList.add('active');
                    modal.style.setProperty('display', 'flex', 'important');
                }
                return;
            }

            // If not logged in: IMMEDIATELY launch real Google OAuth!
            this.launchGoogleOAuth();
        },

        launchGoogleOAuth: function() {
            var self = this;

            // Tier 1: Try GIS Token Client popup
            if (this.gisTokenClient) {
                try {
                    this.gisTokenClient.requestAccessToken({ prompt: 'select_account' });
                    return;
                } catch(e) {
                    console.warn("GIS TokenClient launch failed, falling back to OAuth window:", e);
                }
            }

            // Tier 2: Launch Google OAuth 2.0 Web Popup Window directly to accounts.google.com
            var redirectUri = window.location.origin + window.location.pathname;
            var state = "vyas_oauth_" + Math.random().toString(36).substring(2);
            try { sessionStorage.setItem("vyas_oauth_state", state); } catch(e) {}

            var authUrl = "https://accounts.google.com/o/oauth2/v2/auth?" +
                "client_id=" + encodeURIComponent(self.GOOGLE_CLIENT_ID) +
                "&redirect_uri=" + encodeURIComponent(redirectUri) +
                "&response_type=token%20id_token" +
                "&scope=" + encodeURIComponent("openid email profile") +
                "&state=" + encodeURIComponent(state) +
                "&nonce=" + encodeURIComponent(state) +
                "&prompt=select_account";

            var w = 520, h = 650;
            var left = Math.max(0, (window.screen.width - w) / 2);
            var top = Math.max(0, (window.screen.height - h) / 2);
            var popup = window.open(authUrl, "VyasGoogleAuthPopup", "width=" + w + ",height=" + h + ",top=" + top + ",left=" + left + ",status=no,resizable=yes");

            // If browser blocks popups, redirect directly to Google Sign-In
            if (!popup || popup.closed || typeof popup.closed === 'undefined') {
                window.location.href = authUrl;
            }
        },'''

    new_google_auth = '''        promptGoogleSignIn: function() {
            var modal = document.getElementById('modalGoogleAuthMobile');
            if (modal) {
                var unauth = document.getElementById('mGoogleUnauth');
                var auth = document.getElementById('mGoogleAuth');
                if (this.googleUser) {
                    if (unauth) unauth.style.display = 'none';
                    if (auth) auth.style.display = 'block';
                    var nameEl = document.getElementById('mAuthName');
                    var emailEl = document.getElementById('mAuthEmail');
                    if (nameEl) nameEl.textContent = this.googleUser.name || 'सत्यापित PRO जातक';
                    if (emailEl) emailEl.textContent = this.googleUser.email || '';
                } else {
                    if (unauth) unauth.style.display = 'block';
                    if (auth) auth.style.display = 'none';
                }
                modal.classList.add('active');
                modal.style.setProperty('display', 'flex', 'important');
            }
        },

        launchGoogleOAuth: function() {
            var self = this;
            var redirectUri = "https://vyasastro.in/mobile/";
            var state = "vyas_oauth_" + Math.random().toString(36).substring(2);
            try { sessionStorage.setItem("vyas_oauth_state", state); } catch(e) {}

            var authUrl = "https://accounts.google.com/o/oauth2/v2/auth?" +
                "client_id=" + encodeURIComponent(self.GOOGLE_CLIENT_ID) +
                "&redirect_uri=" + encodeURIComponent(redirectUri) +
                "&response_type=token%20id_token" +
                "&scope=" + encodeURIComponent("openid email profile") +
                "&state=" + encodeURIComponent(state) +
                "&nonce=" + encodeURIComponent(state) +
                "&prompt=select_account";

            // If running inside Android Native App WebView, launch system browser
            if (window.Android && typeof window.Android.openExternalUrl === 'function') {
                window.Android.openExternalUrl(authUrl);
                return;
            }

            // Tier 1: Try GIS Token Client popup in browser
            if (this.gisTokenClient) {
                try {
                    this.gisTokenClient.requestAccessToken({ prompt: 'select_account' });
                    return;
                } catch(e) {
                    console.warn("GIS TokenClient launch failed:", e);
                }
            }

            // Tier 2: Web popup window
            var w = 520, h = 650;
            var left = Math.max(0, (window.screen.width - w) / 2);
            var top = Math.max(0, (window.screen.height - h) / 2);
            var popup = window.open(authUrl, "VyasGoogleAuthPopup", "width=" + w + ",height=" + h + ",top=" + top + ",left=" + left + ",status=no,resizable=yes");

            // Only redirect in regular web browsers, NOT inside WebViews
            if (!popup || popup.closed || typeof popup.closed === 'undefined') {
                if (!window.Android && location.protocol !== 'file:') {
                    window.location.href = authUrl;
                }
            }
        },'''

    content = content.replace(old_google_auth, new_google_auth)

    # 4. Add Guest Mode button in modalGoogleAuthMobile
    old_modal_btn = '''                <!-- Primary Official Google OAuth Launch Button -->
                <button type="button" onclick="VyasMobile.launchGoogleOAuth()" style="width:100%; display:flex; align-items:center; justify-content:center; gap:10px; background:#FFFFFF; border:1px solid #DADCE0; border-radius:24px; padding:11px 16px; color:#3C4043; font-weight:600; font-size:0.88rem; font-family:'Roboto', system-ui, -apple-system, sans-serif; cursor:pointer; box-shadow:0 2px 6px rgba(0,0,0,0.18);">
                    <svg viewBox="0 0 24 24" width="18" height="18">
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                    </svg>
                    <span>Google खाते से साइन-इन करें</span>
                </button>'''

    new_modal_btn = '''                <!-- Primary Official Google OAuth Launch Button -->
                <button type="button" onclick="VyasMobile.launchGoogleOAuth()" style="width:100%; display:flex; align-items:center; justify-content:center; gap:10px; background:#FFFFFF; border:1px solid #DADCE0; border-radius:24px; padding:11px 16px; color:#3C4043; font-weight:600; font-size:0.88rem; font-family:'Roboto', system-ui, -apple-system, sans-serif; cursor:pointer; box-shadow:0 2px 6px rgba(0,0,0,0.18);">
                    <svg viewBox="0 0 24 24" width="18" height="18">
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                    </svg>
                    <span>Google खाते से साइन-इन करें</span>
                </button>
                <button type="button" onclick="VyasMobile.closeModals()" style="width:100%; margin-top:10px; background:rgba(212,175,55,0.12); border:1px solid rgba(212,175,55,0.3); border-radius:24px; padding:10px 16px; color:#d4af37; font-weight:600; font-size:0.84rem; cursor:pointer;">
                    अतिथि मोड में जारी रखें (Continue as Guest)
                </button>'''

    content = content.replace(old_modal_btn, new_modal_btn)

    with open('mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    with open('android_app/app/src/main/assets/mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print('Successfully patched mobile/index.html and android_app/.../mobile/index.html!')

if __name__ == '__main__':
    run_patch()

