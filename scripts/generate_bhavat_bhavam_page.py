import os

page_html = '''<!DOCTYPE html>
<html lang="hi" data-theme="dark">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>भावात् भावम् (12×12 = 144 संयोजन) • सूक्ष्म भाव एवं जीवन-क्षेत्र विश्लेषण | VYAS ASTRA</title>
    <meta name="description"
        content="भावात् भावम् महा-सिद्धांत - 12×12 = 144 भाव संयोजन, सापेक्ष भाव गणित (Z = ((Y-1+X-1) mod 12)+1), 12 मूल X-से-X सूत्र, 6-स्तरीय सूक्ष्म परीक्षण एवं जातक कुण्डली संरेखण।">
    <link rel="icon" type="image/png" href="/logo_icon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link
        href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"
        rel="stylesheet">

    <style>
        :root {
            --bg-deep: #050811;
            --bg-card: rgba(13, 20, 36, 0.88);
            --bg-card-hover: rgba(22, 33, 58, 0.95);
            --gold: #d4af37;
            --gold-light: #f3e5ab;
            --gold-dim: #997d26;
            --sky: #38bdf8;
            --sky-deep: #0284c7;
            --emerald: #10b981;
            --rose: #f43f5e;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border-subtle: rgba(212, 175, 55, 0.16);
            --border-gold: rgba(212, 175, 55, 0.4);
            --font-serif: 'Cinzel', serif;
            --font-sans: 'Plus Jakarta Sans', sans-serif;
            --font-dev: 'Noto Sans Devanagari', sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-deep);
            color: var(--text-primary);
            font-family: var(--font-dev), var(--font-sans), sans-serif;
            background-image:
                radial-gradient(circle at 18% 12%, rgba(212, 175, 55, 0.07) 0%, transparent 40%),
                radial-gradient(circle at 82% 88%, rgba(56, 189, 248, 0.05) 0%, transparent 40%);
            min-height: 100vh;
            padding-bottom: 70px;
        }

        /* Master Header */
        .master-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 28px;
            background: rgba(5, 8, 17, 0.95);
            border-bottom: 1px solid var(--border-gold);
            backdrop-filter: blur(12px);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .brand-box {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }

        .brand-logo {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            border: 1px solid var(--gold);
        }

        .brand-title {
            font-family: var(--font-serif);
            font-size: 1.28rem;
            font-weight: 800;
            color: var(--gold-light);
            letter-spacing: 1px;
        }

        .brand-subtitle {
            font-size: 0.72rem;
            color: var(--sky);
            letter-spacing: 0.5px;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .btn-gold {
            background: linear-gradient(135deg, var(--gold), var(--gold-dim));
            color: #050811;
            font-weight: 700;
            padding: 7px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.82rem;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-gold:hover {
            filter: brightness(1.15);
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.4);
        }

        /* Pill Bar */
        .vyas-portal-pill-strip {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 10px 24px;
            background: rgba(8, 14, 29, 0.85);
            border-bottom: 1px solid var(--border-subtle);
            scrollbar-width: none;
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
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.24), rgba(56, 189, 248, 0.18));
            color: var(--gold-light);
            border-color: var(--gold);
            font-weight: 700;
        }

        .container {
            max-width: 1300px;
            margin: 0 auto;
            padding: 24px 20px;
        }

        .hero-banner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 24px;
            padding: 22px 28px;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.12), rgba(13, 20, 36, 0.95));
            border: 1px solid var(--border-gold);
        }

        .hero-banner h1 {
            font-size: 1.55rem;
            font-weight: 800;
            color: var(--gold-light);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .hero-banner p {
            font-size: 0.88rem;
            color: var(--text-secondary);
            margin-top: 6px;
            line-height: 1.5;
        }

        .active-profile-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 20px;
            background: rgba(212, 175, 55, 0.12);
            border: 1px solid var(--border-gold);
            color: var(--gold-light);
            font-size: 0.85rem;
            font-weight: 700;
        }

        /* 2-Column Main Section */
        .grid-2 {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            margin-bottom: 30px;
        }

        @media (max-width: 960px) {
            .grid-2 {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 22px;
            backdrop-filter: blur(12px);
        }

        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-subtle);
        }

        .card-title {
            font-size: 1.12rem;
            font-weight: 700;
            color: var(--gold-light);
            display: flex;
            align-items: center;
            gap: 9px;
        }

        /* Synthesizer Controls */
        .synth-controls {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            gap: 14px;
            background: rgba(0, 0, 0, 0.35);
            padding: 16px;
            border-radius: 12px;
            border: 1px solid var(--border-subtle);
            margin-bottom: 20px;
        }

        .synth-select {
            width: 100%;
            padding: 10px 14px;
            background: rgba(13, 20, 36, 0.95);
            border: 1px solid var(--border-gold);
            border-radius: 8px;
            color: #fff;
            font-size: 0.92rem;
            font-weight: 600;
            font-family: inherit;
        }

        .synth-symbol {
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--sky);
            text-align: center;
        }

        /* Resultant Display Box */
        .result-box {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.08), rgba(212, 175, 55, 0.08));
            border: 1px solid var(--border-gold);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 20px;
        }

        .result-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 14px;
        }

        .result-bhava-badge {
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--gold-light);
            background: rgba(212, 175, 55, 0.18);
            border: 1px solid var(--gold);
            padding: 4px 14px;
            border-radius: 8px;
        }

        .result-formula {
            font-family: var(--font-sans);
            font-size: 0.85rem;
            color: var(--sky);
            background: rgba(56, 189, 248, 0.1);
            padding: 4px 10px;
            border-radius: 6px;
        }

        .six-level-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-top: 14px;
        }

        @media (max-width: 640px) {
            .six-level-grid {
                grid-template-columns: 1fr;
            }
        }

        .level-card {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 12px;
        }

        .level-num {
            font-size: 0.72rem;
            font-weight: 800;
            color: var(--sky);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }

        .level-title {
            font-size: 0.86rem;
            font-weight: 700;
            color: var(--gold-light);
            margin-bottom: 4px;
        }

        .level-desc {
            font-size: 0.82rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        /* 12 Anchor Table */
        table.anchor-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.84rem;
        }

        table.anchor-table th,
        table.anchor-table td {
            padding: 10px 12px;
            border: 1px solid var(--border-subtle);
            text-align: left;
        }

        table.anchor-table th {
            background: rgba(212, 175, 55, 0.12);
            color: var(--gold-light);
            font-weight: 700;
        }

        table.anchor-table tr:hover {
            background: rgba(255, 255, 255, 0.02);
            cursor: pointer;
        }

        .badge-z {
            display: inline-block;
            background: rgba(56, 189, 248, 0.15);
            color: var(--sky);
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 4px;
        }

        /* 144 Grid Matrix */
        .matrix-wrap {
            overflow-x: auto;
            margin-top: 14px;
        }

        table.matrix-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.78rem;
            text-align: center;
        }

        table.matrix-table th,
        table.matrix-table td {
            padding: 8px 6px;
            border: 1px solid var(--border-subtle);
            min-width: 44px;
        }

        table.matrix-table th {
            background: rgba(8, 14, 29, 0.95);
            color: var(--gold);
            font-weight: 700;
        }

        table.matrix-table td {
            cursor: pointer;
            transition: all 0.15s;
        }

        table.matrix-table td:hover {
            background: rgba(212, 175, 55, 0.25);
            color: #fff;
            transform: scale(1.08);
            font-weight: 800;
        }

        table.matrix-table td.active-cell {
            background: linear-gradient(135deg, var(--gold), var(--sky-deep)) !important;
            color: #000 !important;
            font-weight: 900;
            box-shadow: 0 0 10px rgba(212, 175, 55, 0.6);
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
            color: var(--gold-light);
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
    <header class="master-header">
        <a href="/" class="brand-box">
            <img src="/logo_icon.png" class="brand-logo" alt="VYAS ASTRA">
            <div>
                <div class="brand-title">VYAS ASTRA</div>
                <div class="brand-subtitle">भावात् भावम् • 144 सूक्ष्म भाव गणित</div>
            </div>
        </a>
        <div class="header-actions">
            <a href="/kp-astrology/" class="btn-gold" style="background:transparent; border:1px solid var(--sky); color:var(--sky);">✦ KP ज्योतिष</a>
            <a href="/" class="btn-gold">लग्न कुण्डली ➔</a>
        </div>
    </header>

    <!-- Top Navigation Pill Strip -->
    <nav class="vyas-portal-pill-strip">
        <a href="/" class="portal-pill"><span>☸</span><span>मुख्य कुण्डली</span></a>
        <a href="/kp-astrology/" class="portal-pill"><span>✦</span><span>KP ज्योतिष व होरारी</span></a>
        <a href="/bhavat-bhavam/" class="portal-pill active"><span>⚡</span><span>भावात् भावम् (144)</span></a>
        <a href="/jaimini-astrology/" class="portal-pill"><span>🏛</span><span>जैमिनी व कारकांश</span></a>
        <a href="/dasha/" class="portal-pill"><span>⏳</span><span>विंशोत्तरी दशा</span></a>
        <a href="/panchang/" class="portal-pill"><span>📅</span><span>दृक पंचांग</span></a>
        <a href="/horary/" class="portal-pill"><span>❓</span><span>प्रश्न कुण्डली</span></a>
    </nav>

    <div class="container">
        <!-- Hero Banner -->
        <div class="hero-banner">
            <div>
                <h1>⚡ भावात् भावम् (12×12 = 144 संयोजन) महा-सिद्धांत</h1>
                <p>
                    पाराशरीय ज्योतिष का सर्वोच्च सूक्ष्म विश्लेषण सूत्र: <i>"भावाद भावम् भावस्य..."</i>। किसी भी भाव से उसकी स्वयं की दूरी उस भाव का आंतरिक बीज व वास्तविक फल निर्धारित करती है।
                </p>
            </div>
            <div id="activeProfileBox" class="active-profile-pill">
                <span>👤</span>
                <span id="activeProfileText">लोड हो रहा है...</span>
            </div>
        </div>

        <!-- 2-Column Main Section -->
        <div class="grid-2">
            <!-- Left: Interactive 144 Synthesizer -->
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <span>✦ 144 भाव संयोजन विश्लेषक (Interactive Synthesizer)</span>
                    </div>
                    <span style="font-size:0.78rem; color:var(--sky);">गणित: Z = ((Y-1 + X-1) mod 12) + 1</span>
                </div>

                <!-- Selectors -->
                <div class="synth-controls">
                    <div>
                        <label style="font-size:0.75rem; color:var(--text-muted); display:block; margin-bottom:5px;">आधार भाव (Base House Y):</label>
                        <select id="baseHouseSelect" class="synth-select" onchange="runBhavatBhavam()">
                            <option value="1">1. प्रथम (तनु / लग्न - स्वयं)</option>
                            <option value="2">2. द्वितीय (धन / कुटुम्ब / वाणी)</option>
                            <option value="3">3. तृतीय (सहज / पराक्रम / भ्राता)</option>
                            <option value="4">4. चतुर्थ (सुख / मातृ / गृह / वाहन)</option>
                            <option value="5">5. पंचम (सुत / बुद्धि / पूर्वपुण्य)</option>
                            <option value="6">6. षष्ठ (रिपु / रोग / ऋण / सेवा)</option>
                            <option value="7" selected>7. सप्तम (कलत्र / जाया / साझेदारी)</option>
                            <option value="8">8. अष्टम (आयु / रंध्र / आकस्मिक)</option>
                            <option value="9">9. नवम (धर्म / भाग्य / गुरु / तीर्थ)</option>
                            <option value="10">10. दशम (कर्म / आजीविका / मान)</option>
                            <option value="11">11. एकादश (आय / लाभ / सिद्धि)</option>
                            <option value="12">12. द्वादश (व्यय / मोक्ष / विदेश)</option>
                        </select>
                    </div>

                    <div class="synth-symbol">➔ का ➔</div>

                    <div>
                        <label style="font-size:0.75rem; color:var(--text-muted); display:block; margin-bottom:5px;">सापेक्ष भाव (Relative House X):</label>
                        <select id="relHouseSelect" class="synth-select" onchange="runBhavatBhavam()">
                            <option value="1">1. 1ला (स्वयं का अस्तित्व)</option>
                            <option value="2" selected>2. 2रा (का धन, वाणी व कुटुम्ब)</option>
                            <option value="3">3. 3रा (का पराक्रम व प्रयास)</option>
                            <option value="4">4. 4था (का सुख, वाहन व गृह)</option>
                            <option value="5">5. 5वाँ (की बुद्धि, संतान व विवेक)</option>
                            <option value="6">6. 6ठा (के शत्रु, रोग व सेवा)</option>
                            <option value="7">7. 7वाँ (का जीवनसाथी व साझेदारी)</option>
                            <option value="8">8. 8वाँ (की आयु, गुप्त धन व संकट)</option>
                            <option value="9">9. 9वाँ (का धर्म, भाग्य व पिता)</option>
                            <option value="10">10. 10वाँ (का कर्म, व्यवसाय व प्रतिष्ठा)</option>
                            <option value="11">11. 11वाँ (का लाभ, मित्र व सिद्धि)</option>
                            <option value="12">12. 12वाँ (का व्यय, हानि व मोक्ष)</option>
                        </select>
                    </div>
                </div>

                <!-- Result Box -->
                <div class="result-box">
                    <div class="result-header">
                        <div>
                            <span style="font-size:0.82rem; color:var(--text-muted);">परिणामी भाव (Resultant House):</span>
                            <div id="resultBhavaTitle" class="result-bhava-badge">भाव 8 (अष्टम भाव)</div>
                        </div>
                        <div id="resultFormulaText" class="result-formula">7 का 2रा भाव = 8वाँ भाव</div>
                    </div>
                    <div id="resultDomainSummary" style="font-size:0.92rem; color:var(--gold-light); line-height:1.6; font-weight:600;">
                        जीवनसाथी का धन (7वें का 2रा भाव = 8वाँ भाव): यह जीवनसाथी की संचित निधि, ससुराल पक्ष से प्राप्त धन, पैतृक संपत्ति एवं वैवाहिक जीवन के आर्थिक स्थायित्व को प्रकट करता है।
                    </div>

                    <!-- 6-Level Micro Synthesis -->
                    <div class="six-level-grid">
                        <div class="level-card">
                            <div class="level-num">स्तर 1: भाव व केपी कस्पल सब-लॉर्ड</div>
                            <div id="lvl1Title" class="level-title">भाव 8 स्थिति</div>
                            <div id="lvl1Desc" class="level-desc">जातक कुण्डली में 8वें भाव की राशि, कस्पल सब-लॉर्ड एवं SAV बिंदु।</div>
                        </div>
                        <div class="level-card">
                            <div class="level-num">स्तर 2: भावेश की स्थिति</div>
                            <div id="lvl2Title" class="level-title">भावेश (Z-Lord) स्थिति</div>
                            <div id="lvl2Desc" class="level-desc">भावेश किस भाव व राशि में स्थित है और किन शुभ/अशुभ ग्रहों से दृष्ट है।</div>
                        </div>
                        <div class="level-card">
                            <div class="level-num">स्तर 3: नक्षत्र व उप-स्वामी</div>
                            <div id="lvl3Title" class="level-title">सूक्ष्म नक्षत्र-पद</div>
                            <div id="lvl3Desc" class="level-desc">भावेश का नक्षत्र, 4 पद, नवांश अधिपति एवं केपी उप-स्वामी (Sub-Lord)।</div>
                        </div>
                        <div class="level-card">
                            <div class="level-num">स्तर 4: स्थित ग्रहों का प्रभाव</div>
                            <div id="lvl4Title" class="level-title">भावस्थ ग्रह</div>
                            <div id="lvl4Desc" class="level-desc">परिणामी भाव में स्थित ग्रहों का प्रत्यक्ष प्रभाव व उनकी दृष्टियाँ।</div>
                        </div>
                        <div class="level-card">
                            <div class="level-num">स्तर 5: पंचधा मैत्री व संबंध</div>
                            <div id="lvl5Title" class="level-title">Y-Lord एवं Z-Lord मैत्री</div>
                            <div id="lvl5Desc" class="level-desc">मूल भावेश और परिणामी भावेश के मध्य नैसर्गिक व तात्कालिक पंचधा मैत्री।</div>
                        </div>
                        <div class="level-card">
                            <div class="level-num">स्तर 6: शास्त्रीय निर्णय व उपाय</div>
                            <div id="lvl6Title" class="level-title">सात्विक दैवज्ञ उपाय</div>
                            <div id="lvl6Desc" class="level-desc">संबंधित जीवन-क्षेत्र के दोष शमन व ऊर्जा वर्धन हेतु वैदिक उपाय।</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right: 12 Anchor "X from X" Table -->
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <span>🏛 12 मूल शास्त्रीय "X से X" भावात् भावम् सूत्र</span>
                    </div>
                </div>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:12px;">
                    किसी भाव के स्वयं से उसकी दूरी का प्रत्यक्ष शास्त्रीय प्रभाव (क्लिक करके विश्लेषक में देखें):
                </div>
                <div class="table-wrap">
                    <table class="anchor-table">
                        <thead>
                            <tr>
                                <th>मूल भाव (X)</th>
                                <th>X से X भाव</th>
                                <th>परिणामी भाव (Z)</th>
                                <th>शास्त्रीय जीवन-क्षेत्र</th>
                            </tr>
                        </thead>
                        <tbody id="anchorTableBody">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Full 144 Combinations Grid Matrix (12x12) -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">
                    <span>▦ 144 भाव मैट्रिक्स (12×12 Grid Matrix)</span>
                </div>
                <span style="font-size:0.8rem; color:var(--gold);">किसी भी सेल पर क्लिक करें ➔ वह संयोजन विश्लेषक में लोड होगा</span>
            </div>
            <div class="matrix-wrap">
                <table class="matrix-table" id="matrixTable">
                    <!-- Populated by JS -->
                </table>
            </div>
        </div>
    </div>

    <!-- Mobile Bottom Navigation -->
    <nav class="mobile-app-nav">
        <a href="/">
            <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="9" stroke-width="2" />
                <path d="M12 3v18M3 12h18" stroke-width="2" />
            </svg>
            <span>लग्न</span>
        </a>
        <a href="/kp-astrology/">
            <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 2l3 7h7l-5.5 4.5 2 7.5L12 17l-6.5 4 2-7.5L2 9h7l3-7z" stroke-width="2" />
            </svg>
            <span>KP</span>
        </a>
        <a href="/bhavat-bhavam/" class="active">
            <svg viewBox="0 0 24 24" fill="none">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" stroke-width="2" />
            </svg>
            <span>भावात् भावम्</span>
        </a>
        <a href="/dasha/">
            <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke-width="2" />
                <polyline points="12 6 12 12 16 14" stroke-width="2" />
            </svg>
            <span>दशा</span>
        </a>
        <a href="/panchang/">
            <svg viewBox="0 0 24 24" fill="none">
                <rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2" />
                <line x1="16" y1="2" x2="16" y2="6" stroke-width="2" />
                <line x1="8" y1="2" x2="8" y2="6" stroke-width="2" />
                <line x1="3" y1="10" x2="21" y2="10" stroke-width="2" />
            </svg>
            <span>पंचांग</span>
        </a>
    </nav>

    <script>
        var BHAVA_NAMES = {
            1: "प्रथम (तनु / लग्न)",
            2: "द्वितीय (धन / कुटुम्ब)",
            3: "तृतीय (सहज / पराक्रम)",
            4: "चतुर्थ (सुख / मातृ)",
            5: "पंचम (सुत / बुद्धि)",
            6: "षष्ठ (रिपु / रोग)",
            7: "सप्तम (कलत्र / जाया)",
            8: "अष्टम (आयु / रंध्र)",
            9: "नवम (धर्म / भाग्य)",
            10: "दशम (कर्म / प्रतिष्ठा)",
            11: "एकादश (आय / लाभ)",
            12: "द्वादश (व्यय / मोक्ष)"
        };

        var ANCHORS_12 = [
            { y: 1, z: 1, name: "1 से 1 (1ला)", domain: "स्वयं का मूल अस्तित्व, देह सौष्ठव व आत्मा का तेज।" },
            { y: 2, z: 3, name: "2 से 2 (3रा)", domain: "धन का पोषण, निरंतर प्रयास, लेखन, संवाद व वाणिज्य।" },
            { y: 3, z: 5, name: "3 से 3 (5वाँ)", domain: "पराक्रम का सृजन, कलात्मक कौशल, रणनीतिक बुद्धि व विवेक।" },
            { y: 4, z: 7, name: "4 से 4 (7वाँ)", domain: "गृहस्थ सुख का सामाजिक विस्तार, जीवनसाथी व साझेदारी।" },
            { y: 5, z: 9, name: "5 से 5 (9वाँ)", domain: "बुद्धि व पूर्व पुण्य से भाग्योदय, उच्च दर्शन, धर्म व गुरु कृपा।" },
            { y: 6, z: 11, name: "6 से 6 (11वाँ)", domain: "रोग-रिपु-ऋण पर विजय, प्रतियोगिता में सफलता व अभीष्ट लाभ।" },
            { y: 7, z: 1, name: "7 से 7 (1ला)", domain: "जीवनसाथी का व्यक्तित्व पर प्रत्यक्ष प्रभाव व स्वयं का सामाजिक प्रतिबिंब।" },
            { y: 8, z: 3, name: "8 से 8 (3रा)", domain: "आयु-शक्ति, आंतरिक धैर्य, दीर्घायु बल व संकट में आकस्मिक साहस।" },
            { y: 9, z: 5, name: "9 से 9 (5वाँ)", domain: "धर्म व भाग्य से संतान सुख, विद्या, विवेक, मंत्र सिद्धि व ईश्वरीय कृपा।" },
            { y: 10, z: 7, name: "10 से 10 (7वाँ)", domain: "कर्म का लोक-संपर्क, व्यापारिक यश, जन-सहयोग व सामाजिक प्रतिष्ठा।" },
            { y: 11, z: 9, name: "11 से 11 (9वाँ)", domain: "लाभ की निरंतरता, नैतिक धनार्जन, धर्म-परायणता व गुरु अनुग्रह।" },
            { y: 12, z: 11, name: "12 से 12 (11वाँ)", domain: "व्यय व निवेश से सिद्धि, परोपकार व आध्यात्मिक/भौतिक फल प्राप्ति।" }
        ];

        var DOMAIN_INTERPRETATIONS = {
            "7_2": "जीवनसाथी का धन (7वें का 2रा = 8वाँ भाव): यह जीवनसाथी की संचित निधि, ससुराल पक्ष से प्राप्त धन, पैतृक संपत्ति एवं वैवाहिक जीवन के आर्थिक स्थायित्व को प्रकट करता है।",
            "7_10": "जीवनसाथी का कर्म (7वें का 10वाँ = 4था भाव): जीवनसाथी का कार्यक्षेत्र, व्यावसायिक प्रतिष्ठा व गृहस्थ सुख पर उसका प्रभाव।",
            "2_10": "धन का कर्म (2रे का 10वाँ = 11वाँ भाव): संचित धन किस कर्म या व्यवसाय से अर्जित होगा और निरंतर लाभ का क्या स्रोत रहेगा।",
            "5_7": "संतान का विवाह (5वें का 7वाँ = 11वाँ भाव): संतान का वैवाहिक जीवन, उनकी साझेदारी व पारिवारिक सिद्धि।",
            "9_10": "पिता/भाग्य का कर्म (9वें का 10वाँ = 6ठा भाव): पिता का कार्यक्षेत्र अथवा भाग्य जागृत करने हेतु आवश्यक सेवा, पुरुषार्थ व प्रतियोगिता।",
            "10_2": "कर्म का धन (10वें का 2रा = 11वाँ भाव): आजीविका और व्यवसाय से प्राप्त होने वाला नियमित नकद लाभ व आर्थिक प्रतिफल।",
            "4_4": "सुख का सुख (4थे का 4था = 7वाँ भाव): वाहन, अचल संपत्ति एवं दांपत्य जीवन के माध्यम से प्राप्त होने वाला आंतरिक आनंद।",
            "3_3": "पराक्रम का पराक्रम (3रे का 3रा = 5वाँ भाव): जातक का लेखन, कला, कौशल एवं रणनीतिक बुद्धि का क्रियान्वयन।"
        };

        var activeChart = null;

        function getActiveKundli() {
            try {
                var stored = localStorage.getItem('vyas_active_profile');
                if (stored) {
                    var parsed = JSON.parse(stored);
                    if (parsed && parsed.profile) return parsed;
                }
            } catch (e) { }
            return null;
        }

        function calculateResultantBhava(y, x) {
            return (((y - 1) + (x - 1)) % 12) + 1;
        }

        function runBhavatBhavam(forcedY, forcedX) {
            var y = forcedY || parseInt(document.getElementById('baseHouseSelect').value, 10);
            var x = forcedX || parseInt(document.getElementById('relHouseSelect').value, 10);

            if (forcedY) document.getElementById('baseHouseSelect').value = String(y);
            if (forcedX) document.getElementById('relHouseSelect').value = String(x);

            var z = calculateResultantBhava(y, x);

            // Update Result Header
            document.getElementById('resultBhavaTitle').innerText = 'भाव ' + z + ' (' + BHAVA_NAMES[z] + ')';
            document.getElementById('resultFormulaText').innerText = y + ' का ' + x + ' भाव = ' + z + 'वाँ भाव';

            // Key Interpretation
            var key = y + '_' + x;
            var summary = DOMAIN_INTERPRETATIONS[key];
            if (!summary) {
                summary = BHAVA_NAMES[y] + ' का ' + x + ' भाव (' + BHAVA_NAMES[z] + '): यह ' + BHAVA_NAMES[y] + ' के आंतरिक ' + BHAVA_NAMES[x] + ' तत्त्व को ' + z + 'वें भाव के माध्यम से सक्रिय करता है।';
            }
            document.getElementById('resultDomainSummary').innerText = summary;

            // Highlight Active Matrix Cell
            highlightMatrixCell(y, x);

            // Native Kundli Alignment
            updateNativeLevels(y, x, z);
        }

        function updateNativeLevels(y, x, z) {
            var chart = activeChart || getActiveKundli();
            var zSign = 'मेष', zLord = 'मंगल', zSAV = 28, zCSL = 'गुरु', zPlanets = [];

            if (chart && chart.charts && chart.charts.d1 && chart.charts.d1.houses) {
                var hData = chart.charts.d1.houses[String(z)] || [];
                if (hData.length > 0) {
                    var rashiNum = parseInt(hData[0], 10);
                    var RASHI_NAMES = ["", "मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
                    var RASHI_LORDS = ["", "मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];
                    if (rashiNum >= 1 && rashiNum <= 12) {
                        zSign = RASHI_NAMES[rashiNum];
                        zLord = RASHI_LORDS[rashiNum];
                    }
                    if (hData.length > 1) {
                        zPlanets = hData.slice(1);
                    }
                }
            }

            if (chart && chart.ashtakavarga && chart.ashtakavarga.sav && chart.ashtakavarga.sav.length >= z) {
                zSAV = chart.ashtakavarga.sav[z - 1];
            }

            if (chart && chart.kp && chart.kp.cusps && chart.kp.cusps.length >= z) {
                var cuspObj = chart.kp.cusps[z - 1];
                if (cuspObj) zCSL = cuspObj.sl || cuspObj.subLord || 'गुरु';
            }

            // Level 1
            document.getElementById('lvl1Title').innerText = 'भाव ' + z + ' (' + zSign + ' राशि)';
            document.getElementById('lvl1Desc').innerText = 'SAV बिंदु: ' + zSAV + ' (बल) • केपी कस्पल सब-लॉर्ड (CSL): ' + zCSL + '। ' + (zSAV >= 28 ? 'यह भाव सबल है।' : 'यह भाव सामान्य/संघर्षशील है।');

            // Level 2
            document.getElementById('lvl2Title').innerText = 'भावेश: ' + zLord;
            document.getElementById('lvl2Desc').innerText = zLord + ' इस परिणामी भाव के स्वामी हैं। भावेश की कुण्डली में शुभ स्थिति संबंधित फल को सहज व पुष्ट बनाती है।';

            // Level 3
            document.getElementById('lvl3Title').innerText = 'सूक्ष्म कस्पल कड़ियां';
            document.getElementById('lvl3Desc').innerText = 'कस्प सब-लॉर्ड ' + zCSL + ' की नक्षत्र एवं उप-स्वामी स्थिति से घटना की अनुमति व फल की गुणवत्ता निर्धारित होगी।';

            // Level 4
            document.getElementById('lvl4Title').innerText = 'भावस्थ ग्रह';
            document.getElementById('lvl4Desc').innerText = (zPlanets.length > 0 ? zPlanets.join(', ') : 'कोई ग्रह स्थित नहीं (रिक्त भाव)') + ' — भावेश एवं दृष्टियाँ इस भाव का कार्य संचालन करेंगी।';

            // Level 5
            var diff = Math.abs(z - y);
            if (diff > 6) diff = 12 - diff;
            var relType = (diff === 0 ? "1/1 (स्वयं)" : (diff === 1 ? "2/12 संबंध" : (diff === 2 ? "3/11 संबंध" : (diff === 3 ? "4/10 संबंध" : (diff === 4 ? "5/9 त्रिकोण" : "6/8 षडाष्टक")))));
            document.getElementById('lvl5Title').innerText = 'मूल व परिणामी भाव संबंध: ' + relType;
            document.getElementById('lvl5Desc').innerText = 'भाव ' + y + ' से भाव ' + z + ' का अंतर ' + relType + ' का निर्माण करता है। ' + (diff === 5 ? 'षडाष्टक होने से पुरुषार्थ व बाधा निवारण आवश्यक है।' : 'यह परस्पर सहयोगी संरेखण है।');

            // Level 6
            document.getElementById('lvl6Title').innerText = 'सात्विक दैवज्ञ उपाय';
            document.getElementById('lvl6Desc').innerText = 'भावेश ' + zLord + ' एवं कस्पल सब-लॉर्ड ' + zCSL + ' के बीज मंत्र जप, इष्ट साधना एवं सात्विक दान से ' + BHAVA_NAMES[z] + ' के अभीष्ट फल की पूर्ण प्राप्ति होती है।';
        }

        function highlightMatrixCell(y, x) {
            var cells = document.querySelectorAll('.matrix-table td');
            cells.forEach(function (c) { c.classList.remove('active-cell'); });

            var target = document.getElementById('cell_' + y + '_' + x);
            if (target) {
                target.classList.add('active-cell');
            }
        }

        function buildAnchorTable() {
            var tbody = document.getElementById('anchorTableBody');
            var html = '';
            for (var i = 0; i < ANCHORS_12.length; i++) {
                var a = ANCHORS_12[i];
                html += '<tr onclick="runBhavatBhavam(' + a.y + ', ' + a.y + ')">' +
                    '<td><b>भाव ' + a.y + '</b></td>' +
                    '<td><span style="color:var(--gold-light); font-weight:700;">' + a.name + '</span></td>' +
                    '<td><span class="badge-z">भाव ' + a.z + '</span></td>' +
                    '<td>' + a.domain + '</td>' +
                    '</tr>';
            }
            tbody.innerHTML = html;
        }

        function buildMatrix() {
            var table = document.getElementById('matrixTable');
            var html = '<thead><tr><th>Y \\ X</th>';
            for (var x = 1; x <= 12; x++) {
                html += '<th>' + x + '</th>';
            }
            html += '</tr></thead><tbody>';

            for (var y = 1; y <= 12; y++) {
                html += '<tr><th>भाव ' + y + '</th>';
                for (var x = 1; x <= 12; x++) {
                    var z = calculateResultantBhava(y, x);
                    html += '<td id="cell_' + y + '_' + x + '" onclick="runBhavatBhavam(' + y + ', ' + x + ')">' + z + '</td>';
                }
                html += '</tr>';
            }
            html += '</tbody>';
            table.innerHTML = html;
        }

        window.onload = function () {
            buildAnchorTable();
            buildMatrix();

            activeChart = getActiveKundli();
            var profBox = document.getElementById('activeProfileText');
            if (activeChart && activeChart.profile) {
                var p = activeChart.profile;
                profBox.innerText = (p.name || 'सक्रिय जातक') + ' • ' + (p.asc_sign || 'मेष लग्न') + ' (' + (p.asc_dms || '') + ')';
            } else {
                profBox.innerText = 'आदर्श जातक कुण्डली सक्रिय';
            }

            runBhavatBhavam(7, 2);
        };
    </script>
</body>

</html>
'''

os.makedirs('bhavat-bhavam', exist_ok=True)
with open('bhavat-bhavam/index.html', 'w', encoding='utf-8') as f:
    f.write(page_html)

print("Generated bhavat-bhavam/index.html cleanly!")
