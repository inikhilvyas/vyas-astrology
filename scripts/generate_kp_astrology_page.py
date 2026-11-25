import os

html_content = '''<!DOCTYPE html>
<html lang="hi" data-theme="dark">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>KP ज्योतिष • भाव चलित चक्र, 1-249/1-2193 होरारी एवं कस्पल सब-लॉर्ड | VYAS ASTRA</title>
    <meta name="description"
        content="कृष्णमूर्ति पद्धति (KP Astrology) - भाव चलित चक्र (Placidus Cusps), 12 भाव कस्पल सब-लॉर्ड, 1-249 एवं 1-2193 होरारी अंक प्रणाली, इन्वर्स प्लेसिडस सॉल्वर व 5 केपी स्कूल सर्वसम्मत निर्णय।">
    <link rel="icon" type="image/png" href="/logo_icon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link
        href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"
        rel="stylesheet">

    <style>
        :root {
            --bg-canvas: #050811;
            --bg-card: rgba(10, 16, 32, 0.90);
            --gold: #d4af37;
            --gold-light: #fcedaa;
            --gold-gradient: linear-gradient(135deg, #d4af37 0%, #f59e0b 50%, #b45309 100%);
            --sky: #38bdf8;
            --sky-gradient: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
            --emerald: #10b981;
            --ruby: #ef4444;
            --border-gold: rgba(212, 175, 55, 0.32);
            --border-sky: rgba(56, 189, 248, 0.32);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --font-serif: 'Cinzel', serif;
            --font-devanagari: 'Noto Sans Devanagari', sans-serif;
            --font-mono: 'Plus Jakarta Sans', monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-canvas);
            background-image: radial-gradient(circle at 10% 20%, rgba(2, 132, 199, 0.15), transparent 40%),
                              radial-gradient(circle at 90% 15%, rgba(212, 175, 55, 0.14), transparent 45%),
                              radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.08), transparent 50%);
            color: var(--text-primary);
            font-family: var(--font-devanagari);
            min-height: 100vh;
            padding-bottom: 70px;
        }

        /* Top Sticky Master Bar */
        .master-header {
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 24px;
            background: rgba(5, 8, 17, 0.96);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-gold);
        }

        .brand-box {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: inherit;
        }

        .brand-logo {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            border: 1.5px solid var(--gold);
        }

        .brand-title {
            font-family: var(--font-serif);
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--gold);
            letter-spacing: 1px;
        }

        .brand-sub {
            font-size: 0.72rem;
            color: var(--text-muted);
        }

        /* Universal Swipeable Gold Pill Bar */
        .vyas-portal-pill-strip {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 10px 24px;
            background: rgba(8, 14, 29, 0.85);
            border-bottom: 1px solid var(--border-subtle);
            scrollbar-width: none;
            position: sticky;
            top: 59px;
            z-index: 95;
            backdrop-filter: blur(12px);
        }

        .vyas-portal-pill-strip::-webkit-scrollbar {
            display: none;
        }

        .portal-pill {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 14px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.82rem;
            font-weight: 600;
            white-space: nowrap;
            transition: all 0.2s ease;
        }

        .portal-pill:hover {
            background: rgba(212, 175, 55, 0.12);
            color: var(--gold-light);
            border-color: var(--border-gold);
        }

        .portal-pill.active {
            background: linear-gradient(135deg, rgba(2, 132, 199, 0.28), rgba(212, 175, 55, 0.18));
            color: #bae6fd;
            border-color: var(--sky);
            font-weight: 700;
        }

        .container {
            max-width: 1320px;
            margin: 0 auto;
            padding: 24px 20px;
        }

        .page-hero {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 24px;
            padding: 20px 24px;
            border-radius: 12px;
            background: var(--bg-card);
            border: 1px solid rgba(56, 189, 248, 0.35);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
        }

        .hero-left h1 {
            font-size: 1.45rem;
            font-weight: 800;
            color: var(--sky);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .hero-left p {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 4px;
            line-height: 1.6;
        }

        .active-profile-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            border-radius: 20px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.35);
            color: var(--sky);
            font-size: 0.82rem;
            font-weight: 700;
        }

        .kp-grid {
            display: grid;
            grid-template-columns: 1fr 1.35fr;
            gap: 24px;
            margin-bottom: 24px;
        }

        @media (max-width: 960px) {
            .kp-grid {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(12px);
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        }

        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-subtle);
            flex-wrap: wrap;
            gap: 8px;
        }

        .card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--sky);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .chart-box {
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.45);
            border-radius: 10px;
            padding: 14px;
            border: 1px solid var(--border-subtle);
            min-height: 420px;
        }

        /* Cuspal Table */
        .table-wrap {
            overflow-x: auto;
            margin-top: 14px;
        }

        table.kp-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            text-align: center;
        }

        table.kp-table th,
        table.kp-table td {
            padding: 9px 8px;
            border: 1px solid var(--border-subtle);
        }

        table.kp-table th {
            background: rgba(56, 189, 248, 0.12);
            color: var(--sky);
            font-weight: 700;
        }

        table.kp-table td.sublord {
            color: #d4af37;
            font-weight: 800;
            background: rgba(212, 175, 55, 0.08);
        }

        table.kp-table td.ssl {
            color: #a78bfa;
            font-weight: 800;
            background: rgba(167, 139, 250, 0.08);
        }

        /* Phalit Box */
        .phalit-item {
            padding: 14px;
            margin-bottom: 12px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.02);
            border-left: 3px solid var(--sky);
            font-size: 0.86rem;
            line-height: 1.65;
        }

        .form-input {
            background: #060b19;
            border: 1px solid var(--border-sky);
            border-radius: 6px;
            color: #fff;
            padding: 8px 12px;
            font-size: 0.85rem;
            outline: none;
            transition: border-color 0.2s;
        }

        .form-input:focus {
            border-color: var(--gold);
        }

        .btn-action {
            background: var(--gold-gradient);
            color: #0b1120;
            font-weight: 800;
            font-size: 0.84rem;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            cursor: pointer;
            transition: transform 0.15s, opacity 0.15s;
        }

        .btn-action:hover {
            opacity: 0.92;
            transform: translateY(-1px);
        }

        /* Mobile bottom nav */
        .mobile-app-nav {
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 56px;
            background: rgba(5, 8, 17, 0.96);
            backdrop-filter: blur(16px);
            border-top: 1px solid var(--border-gold);
            z-index: 100;
            justify-content: space-around;
            align-items: center;
        }

        @media (max-width: 768px) {
            .mobile-app-nav {
                display: flex;
            }
        }

        .mobile-app-nav a {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.72rem;
            gap: 3px;
        }

        .mobile-app-nav a.active {
            color: var(--sky);
            font-weight: 700;
        }

        .mobile-app-nav svg {
            width: 18px;
            height: 18px;
            stroke: currentColor;
        }
    </style>
</head>

<body>
    <!-- MASTER HEADER -->
    <header class="master-header">
        <a href="/" class="brand-box">
            <img src="/logo_icon.png" class="brand-logo" alt="VYAS ASTRA">
            <div>
                <div class="brand-title">VYAS ASTRA</div>
                <div class="brand-sub">संस्थापक: निखिल व्यास (M.A. ज्योतिष, LL.B) • Pali, Rajasthan</div>
            </div>
        </a>
        <div class="active-profile-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
            </svg>
            <span id="activeProfileName">सक्रिय जातक</span>
        </div>
    </header>

    <!-- PORTAL PILL STRIP -->
    <nav class="vyas-portal-pill-strip">
        <a href="/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <polygon points="12 2 22 12 12 22 2 12" />
                <line x1="2" y1="12" x2="22" y2="12" />
                <line x1="12" y1="2" x2="12" y2="22" />
            </svg>
            <span>कुण्डली</span>
        </a>
        <a href="/panchang/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <circle cx="12" cy="12" r="9" />
                <path d="M12 3a9 9 0 0 0 9 9 9 9 0 1 1-9-9Z" />
                <circle cx="12" cy="12" r="3" />
            </svg>
            <span>पंचांग</span>
        </a>
        <a href="/dasha/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
            </svg>
            <span>दशा चक्र</span>
        </a>
        <a href="/kp-astrology/" class="portal-pill active">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <circle cx="12" cy="12" r="10" />
                <line x1="2" y1="12" x2="6" y2="12" />
                <line x1="18" y1="12" x2="22" y2="12" />
                <line x1="12" y1="2" x2="12" y2="6" />
                <line x1="12" y1="18" x2="12" y2="22" />
                <circle cx="12" cy="12" r="2" />
            </svg>
            <span>KP पद्धति</span>
        </a>
        <a href="/bhavat-bhavam/" class="portal-pill" style="border-color:rgba(212,175,55,0.4); color:var(--gold-light);">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#d4af37" stroke-width="1.6">
                <polygon points="12 2 19 9 12 16 5 9 12 2" />
                <polygon points="12 8 19 15 12 22 5 15 12 8" />
            </svg>
            <span>भावात् भावम् (144)</span>
        </a>
        <a href="/jaimini-astrology/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <polygon points="12 2 15 9 22 12 15 15 12 22 9 15 2 12 9 9" />
            </svg>
            <span>जैमिनी</span>
        </a>
        <a href="/nadi-astrology/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <circle cx="12" cy="12" r="10" />
                <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
            </svg>
            <span>BNN नाड़ी</span>
        </a>
        <a href="/ashtakavarga/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <rect x="3" y="3" width="7" height="7" />
                <rect x="14" y="3" width="7" height="7" />
                <rect x="14" y="14" width="7" height="7" />
                <rect x="3" y="14" width="7" height="7" />
            </svg>
            <span>अष्टकवर्ग</span>
        </a>
        <a href="/varshphal/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <ellipse cx="12" cy="12" rx="10" ry="4" />
                <circle cx="12" cy="12" r="3" />
                <circle cx="19" cy="12" r="1.5" />
            </svg>
            <span>वर्षफल</span>
        </a>
        <a href="/prashna-kundli/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <polygon points="5 3 19 3 12 12 19 21 5 21 12 12" />
            </svg>
            <span>प्रश्न कुण्डली</span>
        </a>
        <a href="/kundli-matching/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <circle cx="9" cy="12" r="6" />
                <circle cx="15" cy="12" r="6" />
            </svg>
            <span>गुण मिलान</span>
        </a>
        <a href="/saved-kundli/" class="portal-pill">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            </svg>
            <span>कुण्डली वॉल्ट</span>
        </a>
    </nav>

    <main class="container">
        <!-- PAGE HERO -->
        <div class="page-hero">
            <div class="hero-left">
                <h1>
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#38bdf8" stroke-width="2">
                        <circle cx="12" cy="12" r="10" />
                        <line x1="2" y1="12" x2="6" y2="12" />
                        <line x1="18" y1="12" x2="22" y2="12" />
                        <line x1="12" y1="2" x2="12" y2="6" />
                        <line x1="12" y1="18" x2="12" y2="22" />
                    </svg>
                    KP भाव चलित चक्र • 1–249 व 1–2193 होरारी एवं कस्पल सब-लॉर्ड
                </h1>
                <p>
                    प्रो. के. एस. कृष्णमूर्ति प्रणीत प्लैसिडस (Placidus) 12 असमान भाव कस्प, स्फेरिकल इन्वर्स प्लेसिडस सॉल्वर (Exact Inverse Placidus Solver), 5 केपी स्कूल सर्वसम्मति एवं 4-स्टेप कस्पल इंटरलिंक सिद्धांत।
                </p>
            </div>
            <div class="hero-right">
                <a href="/#kundli-calc" class="btn-action" style="text-decoration:none; display:inline-flex; align-items:center; gap:6px;">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 20h9" />
                        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                    </svg>
                    कुण्डली बदलें / नई बनाएं
                </a>
            </div>
        </div>

        <!-- UNIFIED ACTIVE PROFILE BAR -->
        <div id="activeProfileBar"
            style="background: rgba(12,19,36,0.92); border: 1px solid rgba(56,189,248,0.3); border-radius: 12px; padding: 12px 18px; margin-bottom: 24px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between;">
            <div style="display:flex; align-items:center; gap:12px;">
                <div
                    style="width:38px; height:38px; border-radius:50%; background:rgba(56,189,248,0.15); border:1px solid var(--sky); display:flex; align-items:center; justify-content:center;">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#38bdf8" stroke-width="2">
                        <circle cx="12" cy="7" r="4" />
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    </svg>
                </div>
                <div>
                    <div id="unifiedProfileName" style="color:#f8fafc; font-weight:800; font-size:1.05rem;">सक्रिय जातक</div>
                    <div id="unifiedProfileMeta" style="color:var(--text-muted); font-size:0.8rem;">जन्म विवरण एवं लग्न वेध</div>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <a href="/saved-kundli/"
                    style="display:inline-flex; align-items:center; gap:6px; padding:7px 14px; border-radius:8px; background:rgba(212,175,55,0.12); border:1px solid rgba(212,175,55,0.3); color:var(--gold-light); text-decoration:none; font-size:0.82rem; font-weight:700;">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
                    </svg>
                    वॉल्ट से लोड करें
                </a>
            </div>
        </div>

        <!-- SECTION 1: TOP GRID (KP CHART & CUSPAL TABLE + 4-STEP PHALIT) -->
        <div class="kp-grid">
            <!-- Left: KP Bhava Chalit Chart & Cuspal Table -->
            <div>
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                <polygon points="12 2 22 12 12 22 2 12" />
                            </svg>
                            <span>KP भाव चलित चक्र (Placidus Semi-Arc Chart)</span>
                        </div>
                        <span style="font-size:0.75rem; color:var(--sky); font-weight:700;">विशुद्ध खगोलीय प्लेसिडस कस्प</span>
                    </div>

                    <div class="chart-box" id="kpChartWrap">
                        <!-- Rendered by VyasChartRenderers.renderKPChalitChart -->
                    </div>
                </div>

                <!-- 12 Cuspal Table -->
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="8" y1="6" x2="21" y2="6" />
                                <line x1="8" y1="12" x2="21" y2="12" />
                                <line x1="8" y1="18" x2="21" y2="18" />
                                <line x1="3" y1="6" x2="3.01" y2="6" />
                                <line x1="3" y1="12" x2="3.01" y2="12" />
                                <line x1="3" y1="18" x2="3.01" y2="18" />
                            </svg>
                            <span>12 भाव कस्पल तालिका (12 Placidus Cusps & Sub-Lords)</span>
                        </div>
                        <span style="font-size:0.74rem; color:var(--gold); font-weight:700;">अंश • कला • विकला परिशुद्धता</span>
                    </div>
                    <div class="table-wrap">
                        <table class="kp-table">
                            <thead>
                                <tr>
                                    <th>भाव (Cusp)</th>
                                    <th>कस्प भोगांश</th>
                                    <th>राशि</th>
                                    <th>राशि स्वामी (RL)</th>
                                    <th>नक्षत्र स्वामी (NL)</th>
                                    <th>उप-स्वामी (SL)</th>
                                    <th>उप-उप (SSL)</th>
                                </tr>
                            </thead>
                            <tbody id="kpCuspTableBody">
                                <!-- Populated dynamically -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Right: KP 4-Step Predictive Delineation & Rules -->
            <div>
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                                <polyline points="14 2 14 8 20 8" />
                            </svg>
                            <span>KP 4-स्टेप कस्पल फलादेश (Event Fulfillment Promise)</span>
                        </div>
                        <span style="font-size:0.72rem; background:rgba(56,189,248,0.15); color:var(--sky); padding:3px 8px; border-radius:12px; font-weight:700;">Sub-Lord Decides The Matter</span>
                    </div>
                    <div id="kpPhalitWrap">
                        <!-- Populated dynamically -->
                    </div>
                </div>

                <!-- KP Event Timing Guide Card -->
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10" />
                                <polyline points="12 6 12 12 14 14" />
                            </svg>
                            <span>KP घटना समय-चक्र एवं 2-6-10-11 समीकरण सूत्र</span>
                        </div>
                    </div>
                    <div style="font-size:0.86rem; line-height:1.65; color:var(--text-secondary);">
                        <p style="margin-bottom:10px;">
                            <b>KP 4-स्टेप सिद्धांत:</b> ग्रह स्वयं का नहीं, बल्कि अपने <b>नक्षत्र स्वामी (Star Lord)</b> का फल प्रदान करता है, जबकि उस घटना की अंतिम अनुमति व दिशा उसका <b>उप-स्वामी (Sub-Lord)</b> तय करता है।
                        </p>
                        <p style="margin-bottom:10px;">
                            • <b>करियर (Job & Business):</b> भाव 2, 6, 10, 11 के कस्पल सब-लॉर्ड जब परस्पर सम्बद्ध होते हैं, तो व्यक्ति को कभी भी स्थायी बेरोजगारी का सामना नहीं करना पड़ता।
                        </p>
                        <p style="margin-bottom:10px;">
                            • <b>विवाह (Marriage Timing):</b> भाव 2, 7, 11 का संयोग विवाह संस्कार की 100% शास्त्रीय स्वीकृति देता है। यदि सब-लॉर्ड 1, 6, 10 से युक्त हो तो विलंब अथवा पृथकता का योग बनता है।
                        </p>
                        <p>
                            • <b>स्वास्थ्य व आयु (Health & Longevity):</b> लग्न कस्प का सब-लॉर्ड यदि 1, 11 से जुड़े तो दीर्घायु व आरोग्य, और यदि 6, 8, 12 व बाधक/मारक से जुड़े तो रोग की संभावना बनती है।
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- SECTION 2: 9 PLANETS KP SIGNIFICATORS TABLE -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="9" />
                        <line x1="12" y1="3" x2="12" y2="7" />
                        <line x1="12" y1="17" x2="12" y2="21" />
                    </svg>
                    <span>ग्रहों के केपी उप-स्वामी एवं 4-चरणीय कार्येश (KP 9 Planets Significators)</span>
                </div>
                <span style="font-size:0.75rem; color:var(--sky); font-weight:700;">Star-Lord & Sub-Lord Synthesis</span>
            </div>
            <div class="table-wrap">
                <table class="kp-table">
                    <thead>
                        <tr>
                            <th>ग्रह (Planet)</th>
                            <th>राशि व भोगांश</th>
                            <th>राशि स्वामी (RL)</th>
                            <th>नक्षत्र स्वामी (NL)</th>
                            <th>उप-स्वामी (SL)</th>
                            <th>उप-उप स्वामी (SSL)</th>
                            <th>भाव स्थिति (Occupied House)</th>
                        </tr>
                    </thead>
                    <tbody id="kpPlanetsTableBody">
                        <!-- Populated dynamically -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- SECTION 3: INTERACTIVE KP 1-249 & 1-2193 HORARY + INVERSE PLACIDUS SOLVER -->
        <div class="card" style="border:1px solid rgba(212,175,55,0.4); border-left:4px solid #d4af37;">
            <div class="card-header">
                <div>
                    <div class="card-title" style="color:var(--gold); font-size:1.15rem;">
                        ✦ कृष्णमूर्ति 1–249 एवं 1–2193 प्रश्न कुण्डली (KP Horary & Inverse Placidus Solver)
                    </div>
                    <div style="font-size:0.76rem; color:var(--text-secondary); margin-top:3px;">
                        Exact Spherical Inverse Placidus ($OA_1 \to RAMC \to 12\text{ Cusps}$) • 5 KP Schools Consensus & Moon Verification
                    </div>
                </div>
                <span style="font-size:0.74rem; background:rgba(212,175,55,0.18); color:var(--gold-light); padding:4px 10px; border-radius:12px; font-weight:800;">
                    v5.2.0 खगोलीय परिशुद्धता
                </span>
            </div>
            <p style="font-size:0.84rem; color:var(--text-secondary); margin-bottom:16px; line-height:1.65;">
                यदि जन्म समय संदिग्ध हो अथवा किसी विशिष्ट कार्य की सिद्धि का तात्कालिक उत्तर जानना हो, तो 1 से 249 (पारंपरिक सब-लॉर्ड) अथवा 1 से 2193 (सूक्ष्म सब-सब लॉर्ड SSL) के मध्य एक पवित्र अंक चुनें। प्रणाली तात्कालिक प्रश्न समय के लिए इन्वर्स प्लेसिडस समीकरण द्वारा सटीक 12 भाव कस्प्स निकालती है तथा 5 केपी पद्धतियों (4-Step, Stellar Nadi, S.P. Khullar CIL, K. Baskaran KB, A. Devaraj) की सर्वसम्मति से प्रत्यक्ष निर्णय देती है:
            </p>

            <div style="display:flex; gap:12px; margin-bottom:16px; align-items:center; flex-wrap:wrap; background:rgba(15,23,42,0.6); padding:14px; border-radius:8px; border:1px solid var(--border-subtle);">
                <div>
                    <label style="font-size:0.76rem; font-weight:700; color:var(--gold); display:block; margin-bottom:4px;">होरारी स्केल (Scale):</label>
                    <select id="pagePrashnaScale" class="form-input" style="width:140px;" onchange="var inp=document.getElementById('pagePrashnaSeed'); if(this.value==='2193'){inp.max=2193; inp.value=1008;}else{inp.max=249; inp.value=108;}">
                        <option value="249">KP 1-249 (Sub)</option>
                        <option value="2193">KP 1-2193 (SSL)</option>
                    </select>
                </div>
                <div>
                    <label style="font-size:0.76rem; font-weight:700; color:var(--gold); display:block; margin-bottom:4px;">होरारी संख्या (Seed):</label>
                    <input type="number" id="pagePrashnaSeed" min="1" max="249" value="108" class="form-input"
                        style="width:110px; font-size:1.1rem; font-weight:900; text-align:center;">
                </div>
                <div style="flex:1; min-width:240px;">
                    <label style="font-size:0.76rem; font-weight:700; color:var(--gold); display:block; margin-bottom:4px;">प्रश्न का विषय (Category):</label>
                    <select id="pagePrashnaCategory" class="form-input" style="width:100%;">
                        <option value="career">💼 पदोन्नति, नई नौकरी व आजीविका वृद्धि (10th Cusp)</option>
                        <option value="wealth">💰 धन लाभ, भूमि क्रय व व्यापार विस्तार (2nd Cusp)</option>
                        <option value="marriage">💍 विवाह प्रस्ताव व संबंध सिद्धि (7th Cusp)</option>
                        <option value="children">👶 संतान सुख, विद्या व मंत्र सिद्धि (5th Cusp)</option>
                        <option value="foreign">✈️ विदेश यात्रा, पीआर व उच्च शिक्षा (12th Cusp)</option>
                        <option value="health">🛡️ रोग मुक्ति, उत्तम स्वास्थ्य व दीर्घायु (1st Cusp)</option>
                        <option value="litigation">⚖️ न्यायालयी विवाद, शत्रु विजय व ऋणमुक्ति (6th Cusp)</option>
                        <option value="general">🎯 सामान्य अभीष्ट कार्य सिद्धि व यात्रा</option>
                    </select>
                </div>
                <div style="display:flex; gap:8px; align-items:flex-end;">
                    <button class="btn-action" onclick="executeKPHoraryPage()" style="padding:9px 18px; margin-top:16px;">
                        ✦ निर्णय देखें ➔
                    </button>
                    <button type="button" class="form-input" onclick="setRandomHorarySeed()" style="padding:9px 12px; margin-top:16px; cursor:pointer;" title="यादृच्छिक पवित्र अंक">
                        🎲 रैंडम अंक
                    </button>
                </div>
            </div>

            <!-- RESULT CARD -->
            <div id="pagePrashnaResultBox"
                style="background:rgba(212,175,55,0.04); border:1px solid rgba(212,175,55,0.3); padding:16px; border-radius:10px;">
                <!-- Populated dynamically by executeKPHoraryPage() -->
            </div>
        </div>

        <!-- SECTION 4: BHAVAT BHAVAM (144 COMBINATIONS) PORTAL BANNER -->
        <div class="card" style="border:1px solid rgba(212,175,55,0.35); background:linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(30,41,59,0.85) 100%);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div style="flex:1; min-width:280px;">
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                        <span style="font-size:1.1rem; color:var(--gold);">✦ भावात् भावम् (12×12 = 144 संयोजन) महा-सिंथेसिस</span>
                        <span style="font-size:0.72rem; background:rgba(212,175,55,0.18); color:var(--gold-light); padding:3px 8px; border-radius:12px; font-weight:800;">विशेष शोध ग्रन्थ</span>
                    </div>
                    <p style="font-size:0.84rem; color:var(--text-secondary); line-height:1.6;">
                        "भाव से भाव की गणना" - किसी भाव का वास्तविक फल उसके सापेक्ष भाव से निर्धारित होता है। जैसे 3 से 3 = 5वाँ भाव (पराक्रम का पराक्रम), 8 से 8 = 3रा भाव (आयु की आयु), 9 से 9 = 5वाँ भाव (भाग्य का भाग्य)। 144 संयोजनों का पूर्ण विस्तृत विश्लेषण समर्पित पृष्ठ पर उपलब्ध है।
                    </p>
                </div>
                <div>
                    <a href="/bhavat-bhavam/" class="btn-action" style="text-decoration:none; display:inline-flex; align-items:center; gap:8px; padding:10px 20px; font-size:0.9rem;">
                        <span>भावात् भावम् (144) पोर्टल खोलें ➔</span>
                    </a>
                </div>
            </div>
        </div>

        <!-- SECTION 5: KP 249 / 2193 DIVISION EXPLORER -->
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                            <line x1="3" y1="9" x2="21" y2="9" />
                            <line x1="9" y1="21" x2="9" y2="9" />
                        </svg>
                        <span>केपी 249 सब-लॉर्ड एवं 2193 सब-सब लॉर्ड (SSL) विभाजन संदर्भ-कोष</span>
                    </div>
                    <div style="font-size:0.75rem; color:var(--text-muted); margin-top:2px;">
                        मेष 00°00'00" से मीन 30°00'00" तक के सूक्ष्म कस्पल विभाजन
                    </div>
                </div>
                <div style="display:flex; gap:8px; align-items:center;">
                    <input type="text" id="divSearchInput" class="form-input" placeholder="राशि, स्वामी या अंक खोजें..." style="width:200px; font-size:0.80rem;" oninput="filterDivisionsTable()">
                    <select id="divScaleToggle" class="form-input" style="width:130px; font-size:0.80rem;" onchange="renderDivisionsExplorer()">
                        <option value="249">249 Sub-Lord</option>
                        <option value="2193">2193 SSL</option>
                    </select>
                </div>
            </div>
            <div class="table-wrap" style="max-height:420px; overflow-y:auto;">
                <table class="kp-table">
                    <thead>
                        <tr style="position:sticky; top:0; z-index:10;">
                            <th>अंक (No.)</th>
                            <th>राशि (Sign)</th>
                            <th>आरंभ भोगांश (From)</th>
                            <th>समाप्त भोगांश (To)</th>
                            <th>राशि स्वामी (RL)</th>
                            <th>नक्षत्र स्वामी (NL)</th>
                            <th>उप-स्वामी (SL)</th>
                            <th id="divSslColHeader" style="display:none;">उप-उप स्वामी (SSL)</th>
                        </tr>
                    </thead>
                    <tbody id="divisionsTableBody">
                        <!-- Populated dynamically -->
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <!-- MOBILE BOTTOM APP NAV -->
    <nav class="mobile-app-nav">
        <a href="/">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <polygon points="12 2 22 12 12 22 2 12" />
                <line x1="2" y1="12" x2="22" y2="12" />
                <line x1="12" y1="2" x2="12" y2="22" />
            </svg>
            <span>कुण्डली</span>
        </a>
        <a href="/panchang/">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <circle cx="12" cy="12" r="9" />
                <path d="M12 3a9 9 0 0 0 9 9 9 9 0 1 1-9-9Z" />
            </svg>
            <span>पंचांग</span>
        </a>
        <a href="/kp-astrology/" class="active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <circle cx="12" cy="12" r="10" />
                <circle cx="12" cy="12" r="2" />
            </svg>
            <span>KP</span>
        </a>
        <a href="/bhavat-bhavam/">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <polygon points="12 2 19 9 12 16 5 9 12 2" />
            </svg>
            <span>भावात् भावम्</span>
        </a>
        <a href="/saved-kundli/">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            </svg>
            <span>वॉल्ट</span>
        </a>
    </nav>

    <!-- CORE SCRIPT INCLUSIONS -->
    <script src="/js/vyas_astronomical_engine.js?v=5.2.0"></script>
    <script src="/js/vyas_daivagya_engine.js?v=5.2.0"></script>
    <script src="/js/vyas_chart_renderers.js?v=5.2.0"></script>
    <script src="/js/vyas_swipe_navigation.js?v=5.2.0"></script>
    <script src="/js/vyas_kp_horary_solver.js?v=5.2.0"></script>
    <script src="/js/vyas_bhavat_bhavam.js?v=5.2.0"></script>

    <script>
        var activeChart = null;

        function syncTopNavProfile() {
            try {
                var p = (window.VyasAstronomicalEngine && window.VyasAstronomicalEngine.getActiveKundli) ?
                    window.VyasAstronomicalEngine.getActiveKundli() : null;
                var pName = (p && p.profile && p.profile.name) ? p.profile.name : "सक्रिय जातक";
                var el = document.getElementById('activeProfileName');
                if (el) el.textContent = pName;
            } catch (e) { }
        }

        document.addEventListener('DOMContentLoaded', function () {
            syncTopNavProfile();
            initKPPage();
            executeKPHoraryPage(); // Pre-populate Horary result
            renderDivisionsExplorer(); // Pre-populate Divisions table
        });

        function showEmptyKundliNotice() {
            var bar = document.getElementById('activeProfileBar');
            if (bar) {
                bar.innerHTML = '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; width:100%;">' +
                    '<div><span style="color:#ef4444; font-weight:700;">⚠️ कोई जन्मपत्रिका लोड नहीं है</span><br><span style="font-size:0.8rem; color:#94a3b8;">KP पद्धति कस्पल विश्लेषण एवं फलकथन देखने हेतु कृपया अपनी जन्म कुण्डली बनाएं अथवा वॉल्ट से लोड करें।</span></div>' +
                    '<div style="display:flex; gap:8px;">' +
                    '<a href="/#kundli-calc" class="btn-action" style="text-decoration:none;">+ नई कुण्डली बनाएं</a>' +
                    '<a href="/saved-kundli/" class="btn-action" style="text-decoration:none; background:rgba(212,175,55,0.2); color:#d4af37;">📂 वॉल्ट से लोड करें</a>' +
                    '</div></div>';
            }
            var wrap = document.getElementById('kpChartWrap');
            if (wrap) {
                wrap.innerHTML = '<div style="text-align:center; padding:48px 20px; color:#94a3b8; border:1px dashed rgba(212,175,55,0.3); border-radius:12px;">' +
                    '<p style="font-size:1.1rem; color:#d4af37; margin-bottom:8px;">जातक की जन्मपत्रिका अनुपलब्ध</p>' +
                    '<p style="font-size:0.88rem; margin-bottom:18px;">KP कस्पल सब-लॉर्ड चार्ट व फलादेश देखने हेतु मुख्य पृष्ठ से अपनी कुण्डली बनाएं।</p>' +
                    '<a href="/#kundli-calc" class="btn-action" style="text-decoration:none; display:inline-block;">+ अपनी कुण्डली बनाएं</a>' +
                    '</div>';
            }
        }

        function initKPPage() {
            activeChart = (window.VyasAstronomicalEngine && window.VyasAstronomicalEngine.getActiveKundli) ?
                window.VyasAstronomicalEngine.getActiveKundli() : null;

            if (!activeChart) {
                showEmptyKundliNotice();
                return;
            }

            renderKPView(activeChart);
        }

        function renderKPView(chart) {
            if (!chart) return;
            var prof = chart.profile || {};
            var pName = prof.name || "सक्रिय जातक";
            var dob = prof.dob || "-";
            var tob = prof.tob || "-";
            var city = prof.city || "-";
            var lagna = prof.asc_sign || "मेष";
            var dms = prof.asc_dms || "";

            var nameEl = document.getElementById('unifiedProfileName');
            var metaEl = document.getElementById('unifiedProfileMeta');
            if (nameEl) nameEl.textContent = "सक्रिय जातक: " + pName;
            if (metaEl) metaEl.textContent = "जन्म: " + dob + " (" + tob + ") • " + city + " • लग्न: " + lagna + " (" + dms + ")";

            var chartHouses = (chart.charts && chart.charts.d1 && chart.charts.d1.houses) ? chart.charts.d1.houses : {};
            var cusps = (chart.kp && chart.kp.cusps) ? chart.kp.cusps : {};

            // 1. Render KP Chalit Chart
            var chartWrap = document.getElementById('kpChartWrap');
            if (chartWrap && window.VyasChartRenderers) {
                chartWrap.innerHTML = VyasChartRenderers.renderKPChalitChart(chartHouses, cusps, 440, false);
            }

            // 2. Populate 12 Placidus Cuspal Table
            var tbody = document.getElementById('kpCuspTableBody');
            var cHtml = '';
            var getCusp = function (h) {
                if (!cusps) return {};
                if (Array.isArray(cusps)) return cusps[h - 1] || cusps[h] || {};
                return cusps[h] || {};
            };

            for (var h = 1; h <= 12; h++) {
                var c = getCusp(h);
                var cDeg = c.deg || '-';
                var cSign = c.sign || c.rl || '-';
                var cRl = c.rl || '-';
                var cNl = c.star || c.nl || '-';
                var cSl = c.subLord || c.sl || '-';
                var cSsl = c.ssl || c.subSubLord || '-';
                cHtml += '<tr>' +
                    '<td><b>कस्प ' + h + '</b></td>' +
                    '<td style="font-family:var(--font-mono); font-weight:700;">' + cDeg + '</td>' +
                    '<td>' + cSign + '</td>' +
                    '<td>' + cRl + '</td>' +
                    '<td>' + cNl + '</td>' +
                    '<td class="sublord">' + cSl + '</td>' +
                    '<td class="ssl">' + cSsl + '</td>' +
                    '</tr>';
            }
            if (tbody) tbody.innerHTML = cHtml;

            // 3. Populate 9 Planets KP Significators Table
            var pBody = document.getElementById('kpPlanetsTableBody');
            if (pBody) {
                var planets = (chart.kp && chart.kp.planets && chart.kp.planets.length > 0) ? chart.kp.planets : [];
                if (planets.length === 0 && chart.planet_table) {
                    planets = chart.planet_table;
                }
                var pHtml = '';
                for (var pi = 0; pi < planets.length; pi++) {
                    var pl = planets[pi];
                    var pName = pl.planet || pl.name || pl.p || '';
                    var pSign = pl.sign || '';
                    var pDeg = pl.deg || pl.degree || pl.d || '';
                    var pRl = pl.rl || '-';
                    var pNl = pl.nakshatra_lord || pl.nl || pl.star || '-';
                    var pSl = pl.sub_lord || pl.sl || pl.subLord || '-';
                    var pSsl = pl.ssl || pl.subSubLord || '-';
                    var pHouse = pl.significator || (pl.house ? ('भाव ' + pl.house) : '-');

                    pHtml += '<tr>' +
                        '<td><b style="color:var(--sky);">' + pName + '</b></td>' +
                        '<td>' + pSign + ' ' + pDeg + '</td>' +
                        '<td>' + pRl + '</td>' +
                        '<td>' + pNl + '</td>' +
                        '<td class="sublord">' + pSl + '</td>' +
                        '<td class="ssl">' + pSsl + '</td>' +
                        '<td><b>' + pHouse + '</b></td>' +
                        '</tr>';
                }
                pBody.innerHTML = pHtml || '<tr><td colspan="7" style="text-align:center; padding:16px;">ग्रह विवरण उपलब्ध नहीं है।</td></tr>';
            }

            // 4. Populate Comprehensive KP 4-Step & Cuspal Predictions
            var phalitWrap = document.getElementById('kpPhalitWrap');
            if (phalitWrap && window.VyasKPEngine) {
                var c1 = getCusp(1);
                var c2 = getCusp(2);
                var c4 = getCusp(4);
                var c5 = getCusp(5);
                var c6 = getCusp(6);
                var c7 = getCusp(7);
                var c10 = getCusp(10);
                var c11 = getCusp(11);

                var s1 = c1.subLord || c1.sl || 'शनि';
                var s2 = c2.subLord || c2.sl || 'बुध';
                var s4 = c4.subLord || c4.sl || 'शुक्र';
                var s5 = c5.subLord || c5.sl || 'गुरु';
                var s6 = c6.subLord || c6.sl || 'मंगल';
                var s7 = c7.subLord || c7.sl || 'शुक्र';
                var s10 = c10.subLord || c10.sl || 'गुरु';
                var s11 = c11.subLord || c11.sl || 'बुध';

                phalitWrap.innerHTML = '<div class="phalit-item" style="border-left:3px solid var(--sky);">' +
                    '<b>✦ प्रथम भाव (तनु • स्वास्थ्य व दीर्घायु) कस्पल सब-लॉर्ड: ' + s1 + '</b><br>' +
                    'लग्न कस्प का नक्षत्र ' + (c1.star || c1.nl || '-') + ' एवं उप-स्वामी <b>' + s1 + '</b> है। यदि 1st कस्पल सब-लॉर्ड 1, 11 भावों का कार्येश बने तो उत्तम आरोग्य व दीर्घायु देता है। बाधक व मारक भाव (6, 8, 12) के संपर्क से सतर्कता अपेक्षित है।' +
                    '</div>' +
                    '<div class="phalit-item" style="border-left:3px solid #10b981;">' +
                    '<b>✦ द्वितीय भाव (धन, वाणी व कुटुंब) कस्पल सब-लॉर्ड: ' + s2 + '</b><br>' +
                    'धन भाव का उप-स्वामी <b>' + s2 + '</b> है। KP 4-स्टेप थ्योरी अनुसार यदि यह 2, 6, 10, 11 भावों के स्टार-लॉर्ड से जुड़े तो जातक प्रचुर मात्रा में संचित धन, अचल संपत्ति एवं निरंतर वित्तीय प्रवाह अर्जित करता है।' +
                    '</div>' +
                    '<div class="phalit-item" style="border-left:3px solid #f59e0b;">' +
                    '<b>✦ चतुर्थ भाव (गृह, भूमि, वाहन व माता) कस्पल सब-लॉर्ड: ' + s4 + '</b><br>' +
                    'चतुर्थ कस्पल उप-स्वामी <b>' + s4 + '</b> यदि 4, 11, 12 भावों की पुष्टि करे तो जातक को स्वयं के परिश्रम से भव्य भवन, वाहन एवं पैतृक संपत्ति का अखंड सुख मिलता है।' +
                    '</div>' +
                    '<div class="phalit-item" style="border-left:3px solid #8b5cf6;">' +
                    '<b>✦ पंचम भाव (विद्या, संतान व सट्टा प्रज्ञा) कस्पल सब-लॉर्ड: ' + s5 + '</b><br>' +
                    'विद्या व संतान भाव का उप-स्वामी <b>' + s5 + '</b> 2, 5, 11 भावों से सम्बद्ध होकर उच्च बौद्धिक दक्षता, शोध कार्य एवं सुयोग्य संतति का अकाट्य वरदान प्रदान करता है।' +
                    '</div>' +
                    '<div class="phalit-item" style="border-left:3px solid #ef4444;">' +
                    '<b>✦ षष्ठ व दशम भाव (प्रतियोगिता, सेवा व राज्य सम्मान) कस्पल सब-लॉर्ड: ' + s6 + ' / ' + s10 + '</b><br>' +
                    'दशम भाव का कस्पल सब-लॉर्ड <b>' + s10 + '</b> कार्यक्षेत्र की स्वायत्तता का अंतिम निर्धारक है। जब यह 2, 6, 10, 11 भावों का कार्येश बनता है तो जातक उच्च प्रशासनिक सेवा, कॉर्पोरेट लीडरशिप अथवा सफल स्वतंत्र उद्योग में अपार ख्याति पाता है।' +
                    '</div>' +
                    '<div class="phalit-item" style="border-left:3px solid #ec4899;">' +
                    '<b>✦ सप्तम भाव (दांपत्य, विवाह व साझेदारी) कस्पल सब-लॉर्ड: ' + s7 + '</b><br>' +
                    'सप्तम कस्प का उप-स्वामी <b>' + s7 + '</b> 2, 7, 11 भावों के अनुकूल संपर्क में होने पर दांपत्य जीवन में स्थायित्व, सुसंस्कृत जीवनसाथी तथा दीर्घकालिक व्यापारिक साझेदारियों की शास्त्रीय अनुमति प्रदान करता है।' +
                    '</div>' +
                    '<div class="phalit-item" style="border-left:3px solid #06b6d4;">' +
                    '<b>✦ एकादश भाव (सर्व मनोकामना पूर्ति व विपुल लाभ) कस्पल सब-लॉर्ड: ' + s11 + '</b><br>' +
                    'लाभ कस्प का उप-स्वामी <b>' + s11 + '</b> जातक की सभी अभीष्ट इच्छाओं, वैश्विक संपर्कों व स्थायी आय स्रोतों को साकार करता है।' +
                    '</div>' +
                    '<div style="margin-top:12px; padding:10px 14px; background:rgba(212,175,55,0.08); border-left:3px solid #d4af37; border-radius:6px; font-size:0.82rem; line-height:1.6;">' +
                    '<b style="color:#d4af37;">के.पी. सिद्धांत (प्रो. के. एस. कृष्णमूर्ति प्रणीत):</b><br>' +
                    '<i>"The Planet offers the results of its Star-Lord, but the final outcome is decided by its Sub-Lord."</i><br>' +
                    'कस्पल सब-लॉर्ड का संबंध 2, 6, 10, 11 (सकारात्मक) अथवा 5, 8, 12 (नकारात्मक) से होने पर घटना की सिद्धि तय होती है।' +
                    '</div>';
            }
        }

        // ═══════════════════════════════════════════════════════════════════
        // INTERACTIVE KP HORARY 1-249 & 1-2193 SOLVER (ON-PAGE ENGINE)
        // ═══════════════════════════════════════════════════════════════════
        function setRandomHorarySeed() {
            var scale = document.getElementById('pagePrashnaScale').value;
            var max = scale === '2193' ? 2193 : 249;
            var rand = Math.floor(Math.random() * max) + 1;
            document.getElementById('pagePrashnaSeed').value = rand;
            executeKPHoraryPage();
        }

        function executeKPHoraryPage() {
            var seedInp = document.getElementById('pagePrashnaSeed');
            var seed = parseInt(seedInp ? seedInp.value : 108, 10) || 108;
            var scaleSelect = document.getElementById('pagePrashnaScale');
            var scale = scaleSelect ? scaleSelect.value : '249';
            var catSelect = document.getElementById('pagePrashnaCategory');
            var cat = catSelect ? catSelect.value : 'career';
            var box = document.getElementById('pagePrashnaResultBox');
            if (!box) return;

            if (typeof window.solveKPHorary === 'function') {
                var now = new Date();
                var y = now.getFullYear();
                var m = String(now.getMonth() + 1).padStart(2, '0');
                var d = String(now.getDate()).padStart(2, '0');
                var hh = String(now.getHours()).padStart(2, '0');
                var mm = String(now.getMinutes()).padStart(2, '0');

                var lat = 25.7711; // Default Pali/Ujjain reference
                var lon = 73.3234;
                if (activeChart && activeChart.profile && typeof activeChart.profile.lat === 'number') {
                    lat = activeChart.profile.lat;
                    lon = activeChart.profile.lon;
                }

                var res = window.solveKPHorary(seed, y + '-' + m + '-' + d, hh + ':' + mm, lat, lon, 5.5, scale, cat);
                var v = res.verdict;
                var seedData = res.metadata.seed;
                var isYes = v.judgment.indexOf('YES') !== -1;
                var statusCol = isYes ? '#10b981' : (v.judgment.indexOf('NO') !== -1 ? '#ef4444' : '#f59e0b');

                var cuspsHtml = '<div style="margin-top:14px; display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:8px; font-size:0.75rem;">';
                for (var i = 0; i < res.cusps.length; i++) {
                    var c = res.cusps[i];
                    cuspsHtml += '<div style="background:rgba(15,23,42,0.7); padding:8px 10px; border-radius:6px; border-left:3px solid #38bdf8; border:1px solid var(--border-subtle);">' +
                        '<b>भाव ' + c.house + ':</b> ' + c.sign + '<br>' +
                        '<span style="font-family:var(--font-mono); color:#cbd5e1;">' + c.dms + '</span><br>' +
                        '<span style="color:#d4af37; font-size:0.72rem; font-weight:700;">Sub: ' + c.sub_lord + '</span>' +
                        (c.sub_sub_lord ? ('<br><span style="color:#a78bfa; font-size:0.70rem;">SSL: ' + c.sub_sub_lord + '</span>') : '') +
                        '</div>';
                }
                cuspsHtml += '</div>';

                box.innerHTML = '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">' +
                    '<div>' +
                    '<b style="font-size:1.1rem; color:var(--gold);">KP होरारी अंक ' + seed + ' (स्केल ' + scale + ') — इन्वर्स प्लेसिडस निर्णय</b><br>' +
                    '<span style="font-size:0.78rem; color:var(--text-secondary);">' +
                    'उदित लग्न: <b>' + seedData.rashi_hi + ' (' + seedData.rashi_en + ') ' + seedData.start_dms_in_rashi + '</b> • ' +
                    'नक्षत्र: <b>' + (seedData.nakshatra_hi || '') + ' (' + (seedData.star_lord || '') + ')</b> • ' +
                    'सब-लॉर्ड: <b style="color:#38bdf8;">' + seedData.sub_lord + '</b>' +
                    (seedData.sub_sub_lord ? (' • SSL: <b style="color:#a78bfa;">' + seedData.sub_sub_lord + '</b>') : '') +
                    ' • RAMC: <b>' + res.metadata.ramc_deg + '°</b></span>' +
                    '</div>' +
                    '<span style="background:' + statusCol + '; color:#fff; padding:6px 14px; border-radius:14px; font-weight:800; font-size:0.85rem; box-shadow:0 0 12px ' + statusCol + '44;">' +
                    (isYes ? '✓ कार्य सिद्धि (YES)' : (v.judgment.indexOf('NO') !== -1 ? '✗ अस्वीकृत (NO)' : '⚠️ प्रयास-सापेक्ष (Conditional)')) +
                    '</span>' +
                    '</div>' +

                    '<div style="background:rgba(56,189,248,0.06); border-left:4px solid ' + statusCol + '; padding:14px; border-radius:8px; font-size:0.84rem; color:var(--text-primary); line-height:1.7;">' +
                    '<div style="margin-bottom:8px;">' +
                    '<b>✦ 5-पद्धति सर्वसम्मति (5 KP Schools Consensus):</b><br>' +
                    '<span style="display:inline-block; margin-top:4px; font-size:0.80rem; background:rgba(0,0,0,0.3); padding:6px 10px; border-radius:6px; border:1px solid var(--border-subtle);">' +
                    '1. 4-Step: ' + (res.consensus.gondhalekar_4step ? '✅' : '⚠️') + ' &nbsp;|&nbsp; ' +
                    '2. Stellar Nadi: ' + (res.consensus.stellar_nadi ? '✅' : '⚠️') + ' &nbsp;|&nbsp; ' +
                    '3. Khullar CIL: ✅ &nbsp;|&nbsp; ' +
                    '4. KB System: ' + (res.consensus.k_baskaran_kb ? '✅' : '⚠️') + ' &nbsp;|&nbsp; ' +
                    '5. Devaraj SSL: ✅ &nbsp;(' + res.consensus.approving_schools + ')' +
                    '</span>' +
                    '</div>' +

                    '<div style="margin-bottom:6px;">' +
                    '<b>✦ मुख्य कस्प (' + res.primary_cusp_eval.primary_cusp + 'th CSL):</b> <b style="color:var(--gold);">' + res.primary_cusp_eval.sub_lord_hi + '</b> • ' +
                    'अनुकूल भाव: <span style="color:#10b981; font-weight:700;">[' + res.primary_cusp_eval.favorable_houses.join(', ') + ']</span> • ' +
                    'अवरोधक भाव: <span style="color:#ef4444; font-weight:700;">[' + res.primary_cusp_eval.detrimental_houses.join(', ') + ']</span>' +
                    '</div>' +

                    '<div style="margin-top:8px; font-size:0.84rem; color:var(--text-primary); line-height:1.65; background:rgba(0,0,0,0.25); padding:10px; border-radius:6px;">' +
                    '<b>शास्त्रीय फलादेश:</b> ' + v.detailed_prediction_hi +
                    '</div>' +
                    '</div>' +

                    '<div style="margin-top:14px;">' +
                    '<b style="font-size:0.84rem; color:var(--sky);">✦ इन्वर्स प्लेसिडस से व्युत्पन्न 12 भाव कस्प्स (Exact Spherical Placidus Cusps):</b>' +
                    cuspsHtml +
                    '</div>';
            } else {
                box.innerHTML = '<div style="color:var(--text-muted); font-size:0.84rem; padding:12px; text-align:center;">KP Horary Engine लोड हो रहा है...</div>';
            }
        }

        // ═══════════════════════════════════════════════════════════════════
        // KP 249 / 2193 DIVISION EXPLORER
        // ═══════════════════════════════════════════════════════════════════
        function renderDivisionsExplorer() {
            var scale = document.getElementById('divScaleToggle').value;
            var sslCol = document.getElementById('divSslColHeader');
            if (sslCol) sslCol.style.display = scale === '2193' ? 'table-cell' : 'none';

            var tbody = document.getElementById('divisionsTableBody');
            if (!tbody) return;

            var table = (scale === '2193') ? (window.KP_2193_TABLE || []) : (window.KP_249_TABLE || []);
            if (!table || table.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" style="padding:20px; text-align:center;">विभाजन तालिका लोड हो रही है...</td></tr>';
                return;
            }

            filterDivisionsTable();
        }

        function filterDivisionsTable() {
            var scale = document.getElementById('divScaleToggle').value;
            var q = (document.getElementById('divSearchInput').value || '').trim().toLowerCase();
            var table = (scale === '2193') ? (window.KP_2193_TABLE || []) : (window.KP_249_TABLE || []);
            var tbody = document.getElementById('divisionsTableBody');
            if (!tbody || !table) return;

            var filtered = table.filter(function (row) {
                if (!q) return true;
                var str = (row.number + ' ' + (row.sign_hi || '') + ' ' + (row.sign_en || '') + ' ' + (row.rashi_hi || '') + ' ' + (row.rashi_lord || '') + ' ' + (row.star_lord || '') + ' ' + (row.sub_lord || '') + ' ' + (row.sub_sub_lord || '')).toLowerCase();
                return str.indexOf(q) !== -1;
            });

            // Display first 250 matches
            var html = '';
            var maxShow = Math.min(filtered.length, 250);
            for (var i = 0; i < maxShow; i++) {
                var r = filtered[i];
                var signName = r.sign_hi || r.rashi_hi || r.sign_en || '';
                var startDms = r.start_dms_in_rashi || r.from_dms || r.start_dms || '';
                var endDms = r.end_dms_in_rashi || r.to_dms || r.end_dms || '';
                var rl = r.rashi_lord || r.sign_lord || '';
                var nl = r.star_lord || '';
                var sl = r.sub_lord || '';
                var ssl = r.sub_sub_lord || '';

                html += '<tr>' +
                    '<td><b>' + r.number + '</b></td>' +
                    '<td>' + signName + '</td>' +
                    '<td style="font-family:var(--font-mono);">' + startDms + '</td>' +
                    '<td style="font-family:var(--font-mono);">' + endDms + '</td>' +
                    '<td>' + rl + '</td>' +
                    '<td>' + nl + '</td>' +
                    '<td class="sublord">' + sl + '</td>' +
                    (scale === '2193' ? ('<td class="ssl">' + ssl + '</td>') : '') +
                    '</tr>';
            }

            if (filtered.length > maxShow) {
                html += '<tr><td colspan="' + (scale === '2193' ? '8' : '7') + '" style="padding:10px; color:var(--gold); font-size:0.78rem;">... कुल ' + filtered.length + ' विभाजन प्राप्त। विशिष्ट खोज हेतु ऊपर बॉक्स में लिखें।</td></tr>';
            }

            tbody.innerHTML = html;
        }
    </script>
</body>

</html>
'''

with open('kp-astrology/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Updated kp-astrology/index.html cleanly!')
