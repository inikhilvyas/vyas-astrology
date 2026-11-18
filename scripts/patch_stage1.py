import re

print("Starting master repair of index.html...")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. FIX RAW CODE LEAKS IN TRANSLATION DICTIONARY (Line 412700 approx)
# 'prashna': { hi: '<svg ...>1-249 प्रश्न कुण्डली', en: '<svg ...>1-249 Horary Prashna' }
# Replace with clean strings without SVG markup
prashna_leak_pattern = re.compile(r"'prashna':\s*\{\s*hi:\s*'[^']*?1-249 प्रश्न कुण्डली',\s*en:\s*'[^']*?1-249 Horary Prashna'\s*\}")
if prashna_leak_pattern.search(content):
    content = prashna_leak_pattern.sub(
        "'prashna': { hi: '1-249 प्रश्न कुण्डली', en: '1-249 Horary Prashna' }",
        content
    )
    print("✓ Fixed prashna translation dictionary leak")
else:
    print("! prashna regex did not match, using substring replace")
    old_prashna = """'prashna': { hi: '<svg class="v-icon v-spark" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg>1-249 प्रश्न कुण्डली', en: '<svg class="v-icon v-spark" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg>1-249 Horary Prashna' }"""
    if old_prashna in content:
        content = content.replace(old_prashna, "'prashna': { hi: '1-249 प्रश्न कुण्डली', en: '1-249 Horary Prashna' }")
        print("✓ Substring replaced prashna translation")

# 2. FIX LANGUAGE SWITCHER BUTTON IN HEADER
# Make sure langSwitchBtn contains SVG in an icon container and langSwitchText contains only text
old_lang_btn = """<button class="luxury-nav-btn" id="langSwitchBtn" onclick="VyasDesktop.toggleLanguage()" title="Change Language / भाषा बदलें">
                <svg class="v-icon v-globe" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg><span id="langSwitchText">EN</span>
            </button>"""

new_lang_btn = """<button class="luxury-nav-btn" id="langSwitchBtn" onclick="VyasDesktop.toggleLanguage()" title="Change Language / भाषा बदलें">
                <span id="langSwitchIcon" style="display:inline-flex; align-items:center; margin-right:4px;"><svg class="v-icon v-globe" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></span><span id="langSwitchText">EN</span>
            </button>"""

if old_lang_btn in content:
    content = content.replace(old_lang_btn, new_lang_btn)
    print("✓ Replaced langSwitchBtn cleanly")
else:
    # Regex fallback
    content = re.sub(
        r'<button class="luxury-nav-btn" id="langSwitchBtn"[^>]*>.*?<\/button>',
        new_lang_btn,
        content,
        count=1,
        flags=re.DOTALL
    )
    print("✓ Regex replaced langSwitchBtn")

# 3. FIX HEADER PANCHANG TICKER: Replace static HTML with dynamic IDs
old_ticker = """<span class="panchang-ticker" id="headerPanchangTicker">
                शुक्ल पक्ष तृतीया • अनुराधा • अभिजित: 11:58 AM - 12:44 PM
            </span>"""
new_ticker = """<span class="panchang-ticker" id="headerPanchangTicker">
                <span id="htDate">18 नवंबर 2026</span> • <span id="htTithi">शुक्ल नवमी</span> • <span id="htNak">शतभिषा</span> • <span id="htAbhijit" style="color:#ef4444; font-weight:700;">बुधवार: अभिजित मुहूर्त वर्जित</span>
            </span>"""
if old_ticker in content:
    content = content.replace(old_ticker, new_ticker)
    print("✓ Replaced headerPanchangTicker")
else:
    content = re.sub(
        r'<span class="panchang-ticker" id="headerPanchangTicker">.*?<\/span>',
        new_ticker,
        content,
        count=1,
        flags=re.DOTALL
    )
    print("✓ Regex replaced headerPanchangTicker")

# 4. FIX DAILY HOROSCOPE STATIC HTML CARDS (CELESTIAL TRANSIT & TIMINGS)
old_transit_box = """<div style="background:var(--bg-card); border:1px solid var(--border-gold-soft); padding:10px; border-radius:8px;">
                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">CELESTIAL TRANSIT</div>
                                <div style="font-size:0.74rem; line-height:1.4;">
                                    सूर्य: वृश्चिक 21° • चन्द्र: मकर 04°<br>
                                    गुरु: धनु 19° • शनि: कुंभ 03°
                                </div>
                            </div>
                            <div style="background:var(--bg-card); border:1px solid var(--border-gold-soft); padding:10px; border-radius:8px;">
                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">TIMINGS & COLORS</div>
                                <div style="font-size:0.74rem; line-height:1.4;">
                                    <b>अभिजित:</b> 11:58 - 12:44 PM<br>
                                    <b>राहुकाल:</b> 01:30 PM - 03:00 PM<br>
                                    <b>शुभ रंग:</b> पीला / श्वेत
                                </div>
                            </div>"""

new_transit_box = """<div style="background:var(--bg-card); border:1px solid var(--border-gold-soft); padding:10px; border-radius:8px;">
                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">CELESTIAL TRANSIT (तात्कालिक गोचर)</div>
                                <div style="font-size:0.74rem; line-height:1.4;" id="dailyTransitInfo">
                                    सूर्य: वृश्चिक 02° • चन्द्र: कुंभ 14° (शतभिषा)<br>
                                    गुरु: कर्क 22° • शनि: मीन 18°
                                </div>
                            </div>
                            <div style="background:var(--bg-card); border:1px solid var(--border-gold-soft); padding:10px; border-radius:8px;">
                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">TIMINGS & COLORS (मुहूर्त व रंग)</div>
                                <div style="font-size:0.74rem; line-height:1.4;" id="dailyTimingsInfo">
                                    <b>अभिजित:</b> <span style="color:#ef4444; font-weight:700;">बुधवार को शास्त्रतः वर्जित (निषेध)</span><br>
                                    <b>राहुकाल:</b> 12:00 PM - 01:30 PM<br>
                                    <b>शुभ रंग:</b> स्वर्ण पीला / क्रीम
                                </div>
                            </div>"""

if old_transit_box in content:
    content = content.replace(old_transit_box, new_transit_box)
    print("✓ Replaced static CELESTIAL TRANSIT & TIMINGS in HTML")
else:
    print("! Could not direct replace transit box, checking pattern...")

# 5. FIX GOOGLE LOGIN: Add One-Tap Prompt and 1-Click Founder/Pro Login
old_google_oauth = """launchGoogleOAuth: function() {
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
            var popup = window.open("""

new_google_oauth = """launchGoogleOAuth: function() {
            var self = this;

            // Tier 1: Try GIS Google Identity Services One Tap prompt
            if (window.google && window.google.accounts && window.google.accounts.id) {
                try {
                    google.accounts.id.prompt(function(notification) {
                        if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
                            // If One Tap was not displayed, fall back to Google Auth Modal
                            self.openAuthModal();
                        }
                    });
                    return;
                } catch(e) {
                    console.warn("GIS One Tap prompt error:", e);
                }
            }

            // Tier 2: If GIS Token Client exists, request token
            if (this.gisTokenClient) {
                try {
                    this.gisTokenClient.requestAccessToken({ prompt: 'select_account' });
                    return;
                } catch(e) {
                    console.warn("GIS TokenClient launch failed:", e);
                }
            }

            // Tier 3: Open friendly Login Modal with 1-Click Instant Sign-In
            this.openAuthModal();
        },
        
        openAuthModal: function() {
            var m = document.getElementById('googleAuthModal');
            if (m) m.style.display = 'flex';
        },

        launchGoogleOAuth_deprecated: function() {
            var popup = window.open("""

if old_google_oauth in content:
    content = content.replace(old_google_oauth, new_google_oauth)
    print("✓ Fixed launchGoogleOAuth to use GIS One-Tap and prevent redirect_uri_mismatch")
else:
    print("! Old google oauth pattern not found for exact replacement")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Stage 1 of master repair completed!")

