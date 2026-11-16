# scripts/apply_complete_solution.py
import re

def update_desktop():
    print("Updating index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add id="personalizedDailyCard" and specific IDs in static HTML
    old_card_head = '<div class="content-card">\n                        <div class="card-heading">'
    new_card_head = '<div class="content-card" id="personalizedDailyCard">\n                        <div class="card-heading" id="personalizedDailyHeading">'
    if old_card_head in html:
        html = html.replace(old_card_head, new_card_head, 1)
        print("  ✓ Added id='personalizedDailyCard' to content-card in index.html")

    # 2. Add IDs to Today's Tara in static HTML
    old_tara_block = """                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">TODAY'S TARA INSIGHT</div>
                                <div style="font-size:0.82rem; font-weight:800; color:var(--primary-navy);">Sadhak (साधक तारा - पर्याय 1)</div>
                                <div style="font-size:0.70rem; color:var(--text-secondary); margin-top:2px;">महत्वपूर्ण वार्ता, निर्णय व सिद्धि हेतु श्रेष्ठ दिन।</div>"""

    new_tara_block = """                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">TODAY'S TARA INSIGHT</div>
                                <div style="font-size:0.82rem; font-weight:800; color:var(--primary-navy);" id="vTodayTaraVal">नवतारा चक्र (अज्ञात)</div>
                                <div style="font-size:0.70rem; color:var(--text-secondary); margin-top:2px;" id="vTodayTaraDesc">व्यक्तिगत तारा वेध हेतु कृपया ऊपर '+ नई कुण्डली' बनाएं।</div>"""

    if old_tara_block in html:
        html = html.replace(old_tara_block, new_tara_block, 1)
        print("  ✓ Updated static Tara block to blank state in index.html")

    # 3. Replace updateDailyHoroscopeUI with the comprehensive dynamic Navatara calculation
    old_update_fn_start = "updateDailyHoroscopeUI() {"
    pos = html.find(old_update_fn_start)
    if pos != -1:
        # find the end of this method
        # It ends at 'renderDashaTree' or 'inspectPlanet' or similar
        pos_inspect = html.find('inspectPlanet: function', pos)
        if pos_inspect != -1:
            old_fn_block = html[pos:pos_inspect]

            new_update_fn = """updateDailyHoroscopeUI() {
            var vVal = document.getElementById('vIndexVal');
            var vSub = document.getElementById('vIndexSub');
            var taraVal = document.getElementById('vTodayTaraVal');
            var taraDesc = document.getElementById('vTodayTaraDesc');
            var heading = document.getElementById('personalizedDailyHeading');

            if (!this.activeChartData || !this.activeChartData.profile || !this.activeChartData.profile.name) {
                if (vVal) vVal.textContent = '--';
                if (vSub) { vSub.textContent = 'कुण्डली आवश्यक'; vSub.style.color = 'var(--text-muted)'; }
                if (taraVal) { taraVal.textContent = 'नवतारा चक्र (अज्ञात)'; taraVal.style.color = 'var(--primary-navy)'; }
                if (taraDesc) taraDesc.textContent = "व्यक्तिगत तारा वेध हेतु कृपया ऊपर '+ नई कुण्डली' बनाएं।";
                if (heading) heading.innerHTML = '<span>✦ जातक का व्यक्तिगत दैनिक राशिफल (Personalized Daily Horoscope)</span><span style="font-size:0.75rem; color:#f59e0b; font-weight:700;">(कुण्डली लोड नहीं है)</span>';
                return;
            }

            var prof = this.activeChartData.profile;
            if (heading) {
                heading.innerHTML = '<span>✦ ' + prof.name + ' का व्यक्तिगत दैनिक राशिफल (Personalized Daily Horoscope)</span><span style="font-size:0.75rem; color:#10b981; font-weight:700;">नवतारा चक्र + गोचर + चालू दशा</span>';
            }

            // Real Navatara Calculation based on native's Moon
            var nakList = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"];
            var birthNakIdx = 0;
            if (this.activeChartData.planet_table) {
                for (var p = 0; p < this.activeChartData.planet_table.length; p++) {
                    var pl = this.activeChartData.planet_table[p];
                    if ((pl.p && pl.p.indexOf("चन्द्र") !== -1) || (pl.planet && pl.planet.indexOf("Moon") !== -1)) {
                        var nakStr = pl.n || pl.nakshatra || pl.nak || '';
                        for (var ni = 0; ni < nakList.length; ni++) {
                            if (nakStr.indexOf(nakList[ni]) !== -1) { birthNakIdx = ni; break; }
                        }
                        break;
                    }
                }
            }

            // Real transit Moon Nakshatra right now
            var now = new Date();
            var yr = now.getFullYear(), mo = now.getMonth() + 1, dy = now.getDate();
            var hr = now.getHours(), mn = now.getMinutes();
            var y2 = mo <= 2 ? yr - 1 : yr, m2 = mo <= 2 ? mo + 12 : mo;
            var A = Math.floor(y2 / 100), B = 2 - A + Math.floor(A / 4);
            var jd = Math.floor(365.25 * (y2 + 4716)) + Math.floor(30.6001 * (m2 + 1)) + dy + B - 1524.5 + (hr + mn / 60.0 - 5.5) / 24.0;
            var d = jd - 2451543.5;
            var T_j2000 = (jd - 2451545.0) / 36525.0;
            var ayanamsa = 23.857 + 1.39697 * T_j2000;
            function norm(x) { x = x % 360.0; return x < 0 ? x + 360.0 : x; }
            var moonSid = norm(norm(125.1228 + 115.3654 + 13.0649929509 * d) - ayanamsa);
            var todayNakIdx = Math.floor(moonSid / (360.0 / 27.0)) % 27;

            var diff = ((todayNakIdx - birthNakIdx + 27) % 27) % 9;
            var TARA_INFO = [
                { name: "जन्म तारा (Janma Tara)", score: "72%", color: "#38bdf8", desc: "शारीरिक ऊर्जा व आत्मचिंतन हेतु अनुकूल। मानसिक संतुलन बनाए रखें।" },
                { name: "सम्पत तारा (Sampat Tara)", score: "94%", color: "#10b981", desc: "धन लाभ, आर्थिक विस्तार, नए अनुबंध व ऐश्वर्य प्राप्ति का श्रेष्ठ दिन।" },
                { name: "विपत तारा (Vipat Tara)", score: "42%", color: "#ef4444", desc: "सावधानी, धैर्य व अनपेक्षित जोखिम से बचने की आवश्यकता। वाहन संभलकर चलाएं।" },
                { name: "क्षेम तारा (Kshema Tara)", score: "88%", color: "#10b981", desc: "कल्याण, आरोग्य, सुरक्षा एवं पारिवारिक सुख-शांति हेतु अति शुभ।" },
                { name: "प्रत्यरि तारा (Pratyari Tara)", score: "48%", color: "#f59e0b", desc: "शत्रु-प्रतिस्पर्धा व मतभेद से बचें। महत्वपूर्ण निर्णय टालें।" },
                { name: "साधक तारा (Sadhak Tara)", score: "96%", color: "#10b981", desc: "महत्वपूर्ण वार्ता, पदोन्नति, राजकार्य व सभी अभीष्ट कार्यों में सफलता।" },
                { name: "वध/निधन तारा (Vadha Tara)", score: "35%", color: "#ef4444", desc: "अत्यंत सतर्क रहें। वाद-विवाद से दूर रहें व महामृत्युंजय जप करें।" },
                { name: "मित्र तारा (Mitra Tara)", score: "85%", color: "#38bdf8", desc: "मित्रों, वरिष्ठों व सहयोगियों से पूर्ण समर्थन एवं सौहार्द प्राप्त होगा।" },
                { name: "परम मित्र तारा (Param Mitra)", score: "92%", color: "#10b981", desc: "सर्वकार्य सिद्धि, प्रतिष्ठा में वृद्धि एवं आनंददायक वातावरण।" }
            ];

            var info = TARA_INFO[diff] || TARA_INFO[0];
            if (vVal) vVal.textContent = info.score;
            if (vSub) {
                vSub.textContent = info.name.split(' ')[0] + " (अनुकूल)";
                vSub.style.color = info.color;
            }
            if (taraVal) {
                taraVal.textContent = info.name;
                taraVal.style.color = info.color;
            }
            if (taraDesc) taraDesc.textContent = info.desc;
        },

        renderDashaTree: function() {
            if (typeof this.initDashaTree === 'function') {
                return this.initDashaTree();
            }
        },

        """
            html = html[:pos] + new_update_fn + html[pos_inspect:]
            print("  ✓ Replaced updateDailyHoroscopeUI with dynamic Navatara & added renderDashaTree alias")

    # 4. Add render crash guards for Ashtakavarga, KP, Jaimini
    old_kp_start = "renderKP() {\n            var kp = this.activeChartData.kp || AUTHENTIC_BUNDLE.kp;"
    new_kp_start = """renderKP() {
            var kp = (this.activeChartData && this.activeChartData.kp) ? this.activeChartData.kp : null;
            if (!kp) {
                var cBody = document.getElementById('kpCuspsTableBody');
                if (cBody) cBody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 12 कस्प सब-लॉर्ड्स प्रदर्शित होंगे।</td></tr>';
                return;
            }"""

    if old_kp_start in html:
        html = html.replace(old_kp_start, new_kp_start, 1)
        print("  ✓ Added null guard in renderKP")

    old_jm_start = "renderJaimini() {\n            var jm = this.activeChartData.jaimini || AUTHENTIC_BUNDLE.jaimini;"
    new_jm_start = """renderJaimini() {
            var jm = (this.activeChartData && this.activeChartData.jaimini) ? this.activeChartData.jaimini : null;
            if (!jm) {
                var tbody = document.getElementById('jaiminiKarakasTableBody');
                if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 7 चर कारक प्रदर्शित होंगे।</td></tr>';
                return;
            }"""

    if old_jm_start in html:
        html = html.replace(old_jm_start, new_jm_start, 1)
        print("  ✓ Added null guard in renderJaimini")

    old_av_start = "renderAshtakavarga() {\n            var av = this.activeChartData.ashtakavarga || AUTHENTIC_BUNDLE.ashtakavarga;"
    new_av_start = """renderAshtakavarga() {
            var av = (this.activeChartData && this.activeChartData.ashtakavarga) ? this.activeChartData.ashtakavarga : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.ashtakavarga : null);
            if (!av) return;"""

    if old_av_start in html:
        html = html.replace(old_av_start, new_av_start, 1)
        print("  ✓ Added null guard in renderAshtakavarga")

    # 5. Inject the Living Cosmic Canvas & Shooting Stars Engine
    cosmic_script = """
    <!-- =========================================================================
         COSMIC VOID CANVAS: ANIMATED LIVING CELESTIAL BACKGROUND & SHOOTING STARS
         ========================================================================= -->
    <script>
    (function initCosmicWallpaper() {
        if (document.getElementById('cosmicVoidCanvas')) return;
        var canvas = document.createElement('canvas');
        canvas.id = 'cosmicVoidCanvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '-1';
        canvas.style.opacity = '0.9';
        document.body.prepend(canvas);

        var ctx = canvas.getContext('2d');
        var width, height;

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        // 1. Drifting Twinkling Stars (140 stars)
        var stars = [];
        var STAR_COLORS = ['#FFFFFF', '#FFE8A3', '#93C5FD', '#FDE047', '#E0F2FE'];
        for (var i = 0; i < 140; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.6 + 0.4,
                color: STAR_COLORS[Math.floor(Math.random() * STAR_COLORS.length)],
                alpha: Math.random(),
                speed: Math.random() * 0.02 + 0.005,
                vx: (Math.random() - 0.5) * 0.15,
                vy: (Math.random() - 0.5) * 0.15
            });
        }

        // 2. Slow Orbiting Cosmic Halos (Jupiter / Golden Surya Aura)
        var planets = [
            { x: width * 0.85, y: height * 0.25, r: 50, color1: 'rgba(229, 193, 88, 0.22)', color2: 'rgba(229, 193, 88, 0)', vx: -0.04, vy: 0.02 },
            { x: width * 0.12, y: height * 0.75, r: 70, color1: 'rgba(59, 130, 246, 0.16)', color2: 'rgba(59, 130, 246, 0)', vx: 0.03, vy: -0.03 }
        ];

        // 3. Shooting Stars / Meteors (तारे गुजरते हुए)
        var meteors = [];
        function spawnMeteor() {
            meteors.push({
                x: Math.random() * width * 0.8 + width * 0.1,
                y: Math.random() * height * 0.4,
                len: Math.random() * 110 + 80,
                speed: Math.random() * 6 + 7,
                angle: Math.PI / 4 + (Math.random() - 0.5) * 0.2, // ~45 degrees downward
                alpha: 1,
                fade: Math.random() * 0.015 + 0.012,
                width: Math.random() * 1.5 + 1
            });
        }

        var meteorTimer = 0;
        var nextMeteorInterval = 120 + Math.floor(Math.random() * 180);

        function animate() {
            if (document.hidden) {
                requestAnimationFrame(animate);
                return;
            }

            ctx.clearRect(0, 0, width, height);

            // Draw Cosmic Planetary Halos
            for (var p = 0; p < planets.length; p++) {
                var pl = planets[p];
                pl.x += pl.vx;
                pl.y += pl.vy;
                if (pl.x < -100) pl.x = width + 100;
                if (pl.x > width + 100) pl.x = -100;
                if (pl.y < -100) pl.y = height + 100;
                if (pl.y > height + 100) pl.y = -100;

                var grad = ctx.createRadialGradient(pl.x, pl.y, 0, pl.x, pl.y, pl.r * 2);
                grad.addColorStop(0, pl.color1);
                grad.addColorStop(1, pl.color2);
                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.arc(pl.x, pl.y, pl.r * 2, 0, Math.PI * 2);
                ctx.fill();
            }

            // Draw Twinkling Stars
            for (var i = 0; i < stars.length; i++) {
                var s = stars[i];
                s.x += s.vx;
                s.y += s.vy;
                if (s.x < 0) s.x = width;
                if (s.x > width) s.x = 0;
                if (s.y < 0) s.y = height;
                if (s.y > height) s.y = 0;

                s.alpha += s.speed;
                var currentAlpha = Math.abs(Math.sin(s.alpha));

                ctx.fillStyle = s.color;
                ctx.globalAlpha = currentAlpha * 0.85 + 0.15;
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
                ctx.fill();
            }

            // Handle Shooting Stars (Meteors)
            meteorTimer++;
            if (meteorTimer > nextMeteorInterval) {
                spawnMeteor();
                meteorTimer = 0;
                nextMeteorInterval = 140 + Math.floor(Math.random() * 200);
            }

            for (var m = meteors.length - 1; m >= 0; m--) {
                var met = meteors[m];
                met.x += Math.cos(met.angle) * met.speed;
                met.y += Math.sin(met.angle) * met.speed;
                met.alpha -= met.fade;

                if (met.alpha <= 0 || met.x > width + 200 || met.y > height + 200) {
                    meteors.splice(m, 1);
                    continue;
                }

                var tailX = met.x - Math.cos(met.angle) * met.len;
                var tailY = met.y - Math.sin(met.angle) * met.len;

                var mGrad = ctx.createLinearGradient(tailX, tailY, met.x, met.y);
                mGrad.addColorStop(0, 'rgba(255, 255, 255, 0)');
                mGrad.addColorStop(0.6, 'rgba(147, 197, 253, ' + (met.alpha * 0.4) + ')');
                mGrad.addColorStop(1, 'rgba(255, 243, 191, ' + met.alpha + ')');

                ctx.strokeStyle = mGrad;
                ctx.lineWidth = met.width;
                ctx.lineCap = 'round';
                ctx.beginPath();
                ctx.moveTo(tailX, tailY);
                ctx.lineTo(met.x, met.y);
                ctx.stroke();

                ctx.fillStyle = 'rgba(255, 255, 255, ' + met.alpha + ')';
                ctx.beginPath();
                ctx.arc(met.x, met.y, met.width * 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.globalAlpha = 1;
            requestAnimationFrame(animate);
        }

        requestAnimationFrame(animate);
    })();
    </script>
    """

    if 'initCosmicWallpaper' not in html:
        pos_body_end = html.find('</body>')
        if pos_body_end != -1:
            html = html[:pos_body_end] + cosmic_script + "\n" + html[pos_body_end:]
            print("  ✓ Injected Cosmic Wallpaper & Shooting Stars Engine into index.html")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("  ✓ Saved updated index.html")

def update_mobile():
    print("Updating mobile/index.html...")
    with open('mobile/index.html', 'r', encoding='utf-8') as f:
        m_html = f.read()

    # Inject the Cosmic Wallpaper into mobile/index.html as well!
    cosmic_script = """
    <!-- =========================================================================
         COSMIC VOID CANVAS: ANIMATED LIVING CELESTIAL BACKGROUND & SHOOTING STARS (MOBILE)
         ========================================================================= -->
    <script>
    (function initMobileCosmicWallpaper() {
        if (document.getElementById('cosmicVoidCanvasMobile')) return;
        var canvas = document.createElement('canvas');
        canvas.id = 'cosmicVoidCanvasMobile';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '-1';
        canvas.style.opacity = '0.85';
        document.body.prepend(canvas);

        var ctx = canvas.getContext('2d');
        var width, height;

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        var stars = [];
        var STAR_COLORS = ['#FFFFFF', '#FFE8A3', '#93C5FD', '#FDE047'];
        for (var i = 0; i < 90; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.5 + 0.4,
                color: STAR_COLORS[Math.floor(Math.random() * STAR_COLORS.length)],
                alpha: Math.random(),
                speed: Math.random() * 0.02 + 0.006,
                vx: (Math.random() - 0.5) * 0.12,
                vy: (Math.random() - 0.5) * 0.12
            });
        }

        var meteors = [];
        function spawnMeteor() {
            meteors.push({
                x: Math.random() * width * 0.8 + width * 0.1,
                y: Math.random() * height * 0.35,
                len: Math.random() * 90 + 60,
                speed: Math.random() * 5 + 6,
                angle: Math.PI / 4 + (Math.random() - 0.5) * 0.2,
                alpha: 1,
                fade: Math.random() * 0.018 + 0.014,
                width: 1.2
            });
        }

        var meteorTimer = 0;
        var nextMeteorInterval = 140 + Math.floor(Math.random() * 180);

        function animate() {
            if (document.hidden) {
                requestAnimationFrame(animate);
                return;
            }

            ctx.clearRect(0, 0, width, height);

            for (var i = 0; i < stars.length; i++) {
                var s = stars[i];
                s.x += s.vx;
                s.y += s.vy;
                if (s.x < 0) s.x = width;
                if (s.x > width) s.x = 0;
                if (s.y < 0) s.y = height;
                if (s.y > height) s.y = 0;

                s.alpha += s.speed;
                var currentAlpha = Math.abs(Math.sin(s.alpha));

                ctx.fillStyle = s.color;
                ctx.globalAlpha = currentAlpha * 0.85 + 0.15;
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
                ctx.fill();
            }

            meteorTimer++;
            if (meteorTimer > nextMeteorInterval) {
                spawnMeteor();
                meteorTimer = 0;
                nextMeteorInterval = 160 + Math.floor(Math.random() * 200);
            }

            for (var m = meteors.length - 1; m >= 0; m--) {
                var met = meteors[m];
                met.x += Math.cos(met.angle) * met.speed;
                met.y += Math.sin(met.angle) * met.speed;
                met.alpha -= met.fade;

                if (met.alpha <= 0 || met.x > width + 200 || met.y > height + 200) {
                    meteors.splice(m, 1);
                    continue;
                }

                var tailX = met.x - Math.cos(met.angle) * met.len;
                var tailY = met.y - Math.sin(met.angle) * met.len;

                var mGrad = ctx.createLinearGradient(tailX, tailY, met.x, met.y);
                mGrad.addColorStop(0, 'rgba(255, 255, 255, 0)');
                mGrad.addColorStop(0.6, 'rgba(147, 197, 253, ' + (met.alpha * 0.4) + ')');
                mGrad.addColorStop(1, 'rgba(255, 243, 191, ' + met.alpha + ')');

                ctx.strokeStyle = mGrad;
                ctx.lineWidth = met.width;
                ctx.lineCap = 'round';
                ctx.beginPath();
                ctx.moveTo(tailX, tailY);
                ctx.lineTo(met.x, met.y);
                ctx.stroke();

                ctx.fillStyle = 'rgba(255, 255, 255, ' + met.alpha + ')';
                ctx.beginPath();
                ctx.arc(met.x, met.y, met.width * 1.5, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.globalAlpha = 1;
            requestAnimationFrame(animate);
        }

        requestAnimationFrame(animate);
    })();
    </script>
    """

    if 'initMobileCosmicWallpaper' not in m_html:
        pos_body_end = m_html.find('</body>')
        if pos_body_end != -1:
            m_html = m_html[:pos_body_end] + cosmic_script + "\n" + m_html[pos_body_end:]
            print("  ✓ Injected Cosmic Wallpaper & Shooting Stars into mobile/index.html")

    with open('mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(m_html)
    print("  ✓ Saved updated mobile/index.html")

if __name__ == '__main__':
    update_desktop()
    update_mobile()
