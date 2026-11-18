import re
import os

print("=== STARTING INTERNATIONAL GRADE OVERHAUL ===")

# 1. READ INDEX.HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# =========================================================================
# STEP 1: RENAME "VIP" -> "PRO" / "PREMIUM"
# =========================================================================
print("Step 1: Renaming VIP to PRO / PREMIUM...")

# Replace VIP in text and attributes
html = html.replace('NIKHIL (VIP)', 'NIKHIL (PRO)')
html = html.replace('NIKHIL (PRO VIP)', 'NIKHIL (PRO)')
html = html.replace('(PRO VIP)', '(PRO)')
html = html.replace('VYAS ASTRA VIP क्लब', 'VYAS ASTRA PRO क्लब')
html = html.replace('VIP क्लब', 'PRO क्लब')
html = html.replace('VIP एक्सेस सक्रिय है', 'PRO सदस्यता सक्रिय है')
html = html.replace('VIP एक्सेस सक्रिय', 'PRO एक्सेस सक्रिय')
html = html.replace('VIP एक्सेस', 'PRO एक्सेस')
html = html.replace('VIP PDF', 'PRO शोध डॉसियर')
html = html.replace('VIP सदस्य', 'PRO सदस्य')
html = html.replace('VIP जातक', 'PRO जातक')
html = html.replace('सत्यापित VIP जातक', 'सत्यापित PRO जातक')
html = html.replace('pro-status-badge', 'pro-status-badge') # keep class
html = html.replace('vyas_vip_member_', 'vyas_pro_member_')

# =========================================================================
# STEP 2: PERSISTENT SAFE DATA VAULT & AUTO-SELECT GOOGLE AUTH
# =========================================================================
print("Step 2: Enhancing Persistent Safe Data Vault & Auto-Login...")

# Ensure auto_select is true in setupGoogleIdentity
html = re.sub(
    r'auto_select:\s*false',
    'auto_select: true',
    html
)

# Add permanent browser data vault methods in VyasDesktop
vault_code = """
        // =========================================================================
        // PERMANENT USER DATA VAULT (NO RE-ENTRY REQUIRED)
        // =========================================================================
        saveToUserVault: function(profileData) {
            if (!profileData) return;
            try {
                localStorage.setItem('vyas_active_profile', JSON.stringify(profileData));
                var email = (this.googleUser && this.googleUser.email) ? this.googleUser.email.trim().toLowerCase() : 'nikhilvyas007@gmail.com';
                localStorage.setItem('vyas_user_vault_' + email, JSON.stringify(profileData));
                localStorage.setItem('vyas_user_has_vault', 'true');
            } catch(e) {
                console.warn("Vault save error:", e);
            }
        },

        loadFromUserVault: function() {
            try {
                var email = (this.googleUser && this.googleUser.email) ? this.googleUser.email.trim().toLowerCase() : null;
                if (email) {
                    var vaultData = localStorage.getItem('vyas_user_vault_' + email);
                    if (vaultData) return JSON.parse(vaultData);
                }
                var act = localStorage.getItem('vyas_active_profile');
                if (act) return JSON.parse(act);
            } catch(e) {}
            return null;
        },
"""

if 'saveToUserVault:' not in html:
    html = html.replace('loadStoredProfile() {', vault_code + '\n        loadStoredProfile() {')

# =========================================================================
# STEP 3: EMOJI REPLACEMENT WITH LUXURY VECTOR SVGS
# =========================================================================
print("Step 3: Replacing cartoonish emojis with crisp luxury SVGs...")

# Define SVGs
svg_gem = '<svg class="v-icon v-gem" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M6 3h12l4 6-10 12L2 9z"/></svg>'
svg_user = '<svg class="v-icon v-user" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
svg_spark = '<svg class="v-icon v-spark" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg>'
svg_time = '<svg class="v-icon v-time" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
svg_chart = '<svg class="v-icon v-chart" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'
svg_pin = '<svg class="v-icon v-pin" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
svg_book = '<svg class="v-icon v-book" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15z"/></svg>'
svg_brain = '<svg class="v-icon v-brain" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 9 9m-9 9a9 9 0 0 1-9-9"/></svg>'
svg_globe = '<svg class="v-icon v-globe" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'
svg_share = '<svg class="v-icon v-share" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>'
svg_shield_warn = '<svg class="v-icon v-warn" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
svg_flag = '<svg class="v-icon v-flag" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1zM4 22v-7"/></svg>'

# Replace in html
replacements = [
    ('💎 ', svg_gem),
    ('💎', svg_gem),
    ('👤 ', svg_user),
    ('👤', svg_user),
    ('✨ ', svg_spark),
    ('✨', svg_spark),
    ('⏳ ', svg_time),
    ('⏳', svg_time),
    ('📊 ', svg_chart),
    ('📊', svg_chart),
    ('📍 ', svg_pin),
    ('📍', svg_pin),
    ('📖 ', svg_book),
    ('📖', svg_book),
    ('📜 ', svg_book),
    ('📜', svg_book),
    ('📕 ', svg_book),
    ('📕', svg_book),
    ('🧠 ', svg_brain),
    ('🧠', svg_brain),
    ('🚩 ', svg_flag),
    ('🚩', svg_flag),
    ('🌐 ', svg_globe),
    ('🌐', svg_globe),
    ('📲 ', svg_share),
    ('📲', svg_share),
    ('⚠️ ', svg_shield_warn),
    ('⚠️', svg_shield_warn),
    ('⛔ ', svg_shield_warn),
    ('⛔', svg_shield_warn),
    ('🪐 ', svg_spark),
    ('🪐', svg_spark),
    ('🔮 ', svg_spark),
    ('🔮', svg_spark),
]

for old, new in replacements:
    html = html.replace(old, new)

# =========================================================================
# STEP 4: 4-PILLAR HIERARCHICAL NAVIGATION SYSTEM (DESKTOP)
# =========================================================================
print("Step 4: Architecting 4-Pillar Hierarchical Navigation on Desktop...")

# Find the existing flat tabs container
# Look for <div class="nav-tabs-container"> or similar
flat_tabs_regex = re.compile(r'(<div class="nav-tabs-container"[^>]*>)(.*?)(</div>\s*</div>\s*<!--\s*Main Content)', re.DOTALL)

# Build sovereign 4-Pillar navigation HTML
pillar_nav_html = """
        <!-- SOVEREIGN 4-PILLAR INTERNATIONAL NAVIGATION SYSTEM -->
        <div class="vyas-pillar-nav-wrapper">
            <!-- Level 1: Core 4 Pillar Hubs -->
            <div class="pillar-tabs-bar">
                <button class="pillar-tab-btn active" id="pillar_btn_core" onclick="VyasDesktop.switchPillar('core')">
                    <span class="pillar-num">01</span>
                    <span class="pillar-title">कुण्डली व वर्ग</span>
                    <span class="pillar-en">Horoscope & Vargas</span>
                </button>
                <button class="pillar-tab-btn" id="pillar_btn_dasha" onclick="VyasDesktop.switchPillar('dasha')">
                    <span class="pillar-num">02</span>
                    <span class="pillar-title">दशा व फलित</span>
                    <span class="pillar-en">Dasha & Predictions</span>
                </button>
                <button class="pillar-tab-btn" id="pillar_btn_transit" onclick="VyasDesktop.switchPillar('transit')">
                    <span class="pillar-num">03</span>
                    <span class="pillar-title">कालचक्र व गोचर</span>
                    <span class="pillar-en">Transits & Ashtakavarga</span>
                </button>
                <button class="pillar-tab-btn" id="pillar_btn_systems" onclick="VyasDesktop.switchPillar('systems')">
                    <span class="pillar-num">04</span>
                    <span class="pillar-title">उन्नत शास्त्र व AI</span>
                    <span class="pillar-en">Advanced Shastras & AI</span>
                </button>
            </div>

            <!-- Level 2: Clean Segmented Sub-Pill Switcher (Adapts to Active Pillar) -->
            <div class="sub-nav-segmented-bar" id="subPillarBar">
                <!-- Injected dynamically by VyasDesktop.switchPillar() -->
            </div>
        </div>
"""

# Inject CSS for 4-Pillar Navigation and complete Light/Dark theme refinement
pillar_css = """
        /* =========================================================================
           INTERNATIONAL 4-PILLAR NAVIGATION & DUAL THEME TOKENS
           ========================================================================= */
        .vyas-pillar-nav-wrapper {
            margin: 12px 0 16px 0;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 8px 12px;
            box-shadow: 0 4px 20px -4px rgba(0,0,0,0.25);
        }
        .pillar-tabs-bar {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 8px;
        }
        .pillar-tab-btn {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 8px 12px;
            cursor: pointer;
            text-align: left;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            color: var(--text-muted);
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .pillar-tab-btn:hover {
            background: rgba(212,175,55,0.08);
            border-color: rgba(212,175,55,0.3);
            color: var(--text-main);
        }
        .pillar-tab-btn.active {
            background: linear-gradient(135deg, rgba(30,58,138,0.25), rgba(15,23,42,0.8));
            border: 1.5px solid var(--gold-accent);
            color: var(--text-main);
            box-shadow: 0 0 15px rgba(212,175,55,0.2);
        }
        .pillar-num {
            font-size: 0.65rem;
            font-weight: 800;
            color: var(--gold-accent);
            font-family: var(--font-mono);
            letter-spacing: 0.05em;
        }
        .pillar-title {
            font-size: 0.86rem;
            font-weight: 700;
            color: var(--text-main);
        }
        .pillar-en {
            font-size: 0.65rem;
            color: var(--text-muted);
            letter-spacing: 0.02em;
        }
        .sub-nav-segmented-bar {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px;
            background: rgba(0,0,0,0.25);
            border-radius: 10px;
            overflow-x: auto;
        }
        [data-theme="light"] .sub-nav-segmented-bar {
            background: #E2E8F0;
        }
        .sub-pill-btn {
            flex: 1;
            min-width: 120px;
            background: transparent;
            border: none;
            border-radius: 8px;
            padding: 7px 12px;
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
            white-space: nowrap;
        }
        .sub-pill-btn:hover {
            color: var(--text-main);
            background: rgba(255,255,255,0.05);
        }
        .sub-pill-btn.active {
            background: var(--gold-accent);
            color: #0b1324 !important;
            font-weight: 800;
            box-shadow: 0 2px 8px rgba(212,175,55,0.35);
        }

        /* DUAL THEME EXTENSIONS */
        [data-theme="light"] {
            --bg-canvas: #F8FAFC !important;
            --bg-canvas-gradient: #F8FAFC !important;
            --bg-surface: #FFFFFF !important;
            --bg-card: #FFFFFF !important;
            --bg-card-hover: #F1F5F9 !important;
            --text-main: #0F172A !important;
            --text-muted: #64748B !important;
            --border-color: #E2E8F0 !important;
            --gold-accent: #B48A1A !important;
            --primary-navy: #1E3A8A !important;
        }
        [data-theme="light"] .pillar-tab-btn {
            background: #F1F5F9;
            border-color: #E2E8F0;
        }
        [data-theme="light"] .pillar-tab-btn.active {
            background: #FFFFFF;
            border-color: #B48A1A;
            box-shadow: 0 2px 10px rgba(180,138,26,0.18);
        }
        [data-theme="light"] .card, [data-theme="light"] .view-panel, [data-theme="light"] .dasha-level-1 {
            background: #FFFFFF !important;
            border-color: #E2E8F0 !important;
            color: #0F172A !important;
        }
        [data-theme="light"] .sav-card, [data-theme="light"] table td, [data-theme="light"] table th {
            color: #0F172A !important;
            border-color: #E2E8F0 !important;
        }
"""

if '.vyas-pillar-nav-wrapper' not in html:
    html = html.replace('</style>', pillar_css + '\n    </style>')

# JS functions for switching pillars and sub-tabs
pillar_js = """
        // =========================================================================
        // 4-PILLAR HIERARCHICAL NAVIGATION ENGINE
        // =========================================================================
        currentPillar: 'core',
        pillars: {
            'core': {
                name: 'कुण्डली व वर्ग',
                tabs: [
                    { key: 'kundli', label: 'D-1 लग्न कुण्डली', sub: 'Birth Chart' },
                    { key: 'vargas', label: 'षोडशवर्ग (16 चक्र)', sub: 'Divisional D2-D60' },
                    { key: 'shadbala', label: 'षड्बल सामर्थ्य', sub: 'Planetary Strengths' },
                    { key: 'sphutas', label: 'विशेष स्फुट व आरूढ़', sub: 'Special Ascendants' }
                ]
            },
            'dasha': {
                name: 'दशा व फलित',
                tabs: [
                    { key: 'dasha', label: 'विंशोत्तरी 5-स्तर दशा', sub: 'Vimshottari Dasha Tree' },
                    { key: 'predictions', label: '12 भाव महा-फलादेश', sub: '12 House Predictions' },
                    { key: 'remedies', label: 'अचूक उपाय व रत्न', sub: 'Remedies & Gemstones' },
                    { key: 'match', label: '36 गुण मिलान', sub: 'Kundli Milan' }
                ]
            },
            'transit': {
                name: 'कालचक्र व गोचर',
                tabs: [
                    { key: 'daily', label: 'दैनिक राशिफल व पंचांग', sub: 'Daily Horoscope & Panchang' },
                    { key: 'ashtakavarga', label: 'अष्टकवर्ग (SAV 337 / प्रस्तार)', sub: 'BPHS Ashtakavarga' },
                    { key: 'transit', label: 'तात्कालिक गोचर व वर्षफल', sub: 'Transits & Varshphal' }
                ]
            },
            'systems': {
                name: 'उन्नत शास्त्र व AI',
                tabs: [
                    { key: 'chat', label: 'आचार्यव्यास AI परामर्श', sub: 'Vedic AI Council' },
                    { key: 'kp', label: 'केपी पद्धति (1-249)', sub: 'KP Sub-Lord Horary' },
                    { key: 'nadi', label: 'भृगु नंदी नाड़ी', sub: 'Nadi Astro-Sequencing' },
                    { key: 'lalkitab', label: 'लाल किताब फरमान', sub: 'Lal Kitab Remedial Rules' }
                ]
            }
        },

        switchPillar: function(pillarKey, autoSelectFirstTab) {
            this.currentPillar = pillarKey;
            document.querySelectorAll('.pillar-tab-btn').forEach(function(b) { b.classList.remove('active'); });
            var btn = document.getElementById('pillar_btn_' + pillarKey);
            if (btn) btn.classList.add('active');

            // Render sub-nav pills
            var bar = document.getElementById('subPillarBar');
            if (bar && this.pillars[pillarKey]) {
                var pData = this.pillars[pillarKey];
                var sHtml = '';
                for (var i = 0; i < pData.tabs.length; i++) {
                    var t = pData.tabs[i];
                    sHtml += '<button class="sub-pill-btn" id="sub_tab_' + t.key + '" onclick="VyasDesktop.switchSubTab(\\'' + t.key + '\\')">' +
                        '<div>' + t.label + '</div>' +
                        '<div style="font-size:0.62rem; opacity:0.7;">' + t.sub + '</div>' +
                        '</button>';
                }
                bar.innerHTML = sHtml;

                // Select first sub-tab by default if requested
                var firstTab = pData.tabs[0].key;
                this.switchSubTab(firstTab);
            }
        },

        switchSubTab: function(tabKey) {
            document.querySelectorAll('.sub-pill-btn').forEach(function(b) { b.classList.remove('active'); });
            var targetPill = document.getElementById('sub_tab_' + tabKey);
            if (targetPill) targetPill.classList.add('active');

            // Switch view panel
            this.switchTab(tabKey);
        },
"""

if 'switchPillar:' not in html:
    html = html.replace('init() {', pillar_js + '\n        init() {')

# Hook switchPillar into init()
if 'this.switchPillar(\'core\', true);' not in html:
    html = html.replace('this.initGoogleAuth();', 'this.initGoogleAuth();\n        this.switchPillar(\'core\', true);')

# Replace the old flat tab bar in html body with the new 4-pillar bar
old_tab_container = re.search(r'<div class="desktop-tab-bar".*?</div>\s*</div>', html, re.DOTALL)
if old_tab_container:
    html = html.replace(old_tab_container.group(0), pillar_nav_html)
    print("SUCCESS: Replaced old flat tab bar with 4-Pillar Nav!")
else:
    # Look for nav-tab buttons in html
    pat = re.search(r'<div class="nav-tabs-wrapper">.*?</div>\s*</div>', html, re.DOTALL)
    if pat:
        html = html.replace(pat.group(0), pillar_nav_html)
        print("SUCCESS: Replaced nav-tabs-wrapper with 4-Pillar Nav!")
    else:
        # Prepend to main workspace
        html = html.replace('<div class="desktop-layout-grid">', pillar_nav_html + '\n        <div class="desktop-layout-grid">')
        print("SUCCESS: Injected 4-Pillar Nav above main layout grid!")

# Write updated index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html overhauled!")
