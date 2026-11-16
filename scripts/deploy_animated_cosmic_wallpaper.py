import re

def update_css():
    print("Updating styles/adx_elevation.css...")
    with open('styles/adx_elevation.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Ensure body is transparent and canvas is at z-index: 0, content at z-index: 1
    cosmic_css = """
/* =========================================================================
   ANIMATED COSMIC LIVING WALLPAPER & GLASS SURFACE ELEVATION
   ========================================================================= */
html, body {
    background: #050814 !important;
    background-color: #050814 !important;
    background-image: none !important;
}

#cosmicVoidCanvas, #cosmicVoidCanvasMobile {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    pointer-events: none !important;
    z-index: 0 !important;
    opacity: 1 !important;
}

.master-header, .cockpit-container, .modal-backdrop, .toast-container,
.tab-view-container, .mobile-view-container, .m-header, .m-bottom-nav {
    position: relative !important;
    z-index: 1 !important;
}

.cockpit-col {
    background: rgba(8, 14, 28, 0.72) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(229, 193, 88, 0.22) !important;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
}

.content-card {
    background: rgba(13, 20, 38, 0.70) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(212, 175, 55, 0.18) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
}

.master-header {
    background: rgba(5, 9, 18, 0.78) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid rgba(212, 175, 55, 0.24) !important;
}
"""
    if "ANIMATED COSMIC LIVING WALLPAPER" not in css:
        css = css + "\n" + cosmic_css
        with open('styles/adx_elevation.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("  ✓ Appended cosmic glassmorphism elevation rules to styles/adx_elevation.css")
    else:
        print("  ✓ Already present in styles/adx_elevation.css")

def get_cosmic_engine_js(is_mobile=False):
    canvas_id = 'cosmicVoidCanvasMobile' if is_mobile else 'cosmicVoidCanvas'
    fn_name = 'initMobileCosmicWallpaper' if is_mobile else 'initCosmicWallpaper'
    num_stars = 110 if is_mobile else 220
    star_speed_mult = 1.0

    return f"""
    <!-- =========================================================================
         COSMIC LIVING WALLPAPER & SHOOTING METEORS ENGINE (60FPS HARDWARE ACCELERATED)
         ========================================================================= -->
    <canvas id="{canvas_id}"></canvas>
    <script>
    (function {fn_name}() {{
        var canvas = document.getElementById('{canvas_id}');
        if (!canvas) return;

        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '0';
        canvas.style.display = 'block';

        var ctx = canvas.getContext('2d');
        var width, height;

        function resize() {{
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }}
        window.addEventListener('resize', resize);
        resize();

        // 1. Celestial Starfield (Multi-depth & Colors)
        var stars = [];
        var STAR_PALETTE = [
            '#FFFFFF', '#FFFFFF', '#E0F2FE', '#BAE6FD', '#FDE68A', '#FEF08A', '#FBCFE8'
        ];
        for (var i = 0; i < {num_stars}; i++) {{
            stars.push({{
                x: Math.random() * width,
                y: Math.random() * height,
                r: Math.random() < 0.08 ? (Math.random() * 1.5 + 2.0) : (Math.random() * 1.2 + 0.4),
                color: STAR_PALETTE[Math.floor(Math.random() * STAR_PALETTE.length)],
                alpha: Math.random(),
                twinkleSpeed: Math.random() * 0.03 + 0.008,
                vx: (Math.random() - 0.5) * 0.12 * {star_speed_mult},
                vy: (Math.random() - 0.5) * 0.12 * {star_speed_mult},
                hasSpike: Math.random() < 0.08 // Cross flare diffraction spike
            }});
        }}

        // 2. Cosmic Constellation Links (Sacred Asterisms)
        var constellationPairs = [];
        for (var c = 0; c < 14; c++) {{
            var idx1 = Math.floor(Math.random() * (stars.length - 1));
            var idx2 = idx1 + 1;
            constellationPairs.push([idx1, idx2]);
        }}

        // 3. Volumetric Living Nebulae
        var nebulae = [
            {{ x: width * 0.2, y: height * 0.25, r: 240, r1: 10, col1: 'rgba(30, 58, 138, 0.32)', col2: 'rgba(15, 23, 42, 0)', vx: 0.03, vy: 0.02, phase: 0 }},
            {{ x: width * 0.8, y: height * 0.35, r: 280, r1: 15, col1: 'rgba(180, 83, 9, 0.22)', col2: 'rgba(217, 119, 6, 0)', vx: -0.02, vy: 0.03, phase: 2.1 }},
            {{ x: width * 0.5, y: height * 0.85, r: 260, r1: 10, col1: 'rgba(88, 28, 135, 0.25)', col2: 'rgba(76, 29, 149, 0)', vx: 0.02, vy: -0.02, phase: 4.2 }}
        ];

        // 4. Moving Celestial Orbs (Surya & Chandra)
        var celestialOrbs = [
            // Surya (Sun) Aura
            {{ x: width * 0.88, y: height * 0.18, r: 42, col: 'rgba(245, 158, 11, ', pulse: 0, vx: -0.02, vy: 0.015, type: 'sun' }},
            // Chandra (Moon) Aura
            {{ x: width * 0.12, y: height * 0.72, r: 35, col: 'rgba(147, 197, 253, ', pulse: 3.14, vx: 0.025, vy: -0.018, type: 'moon' }}
        ];

        // 5. High-Velocity Shooting Meteors (तारे गुजरते हुए)
        var meteors = [];
        function spawnMeteor() {{
            var startX = Math.random() * (width * 0.85) + (width * 0.1);
            var startY = Math.random() * (height * 0.35);
            var angle = Math.PI / 4 + (Math.random() - 0.5) * 0.3; // ~45 deg downward streak
            var speed = Math.random() * 8 + 8; // fast & dramatic
            var len = Math.random() * 140 + 90;
            var widthThick = Math.random() * 1.6 + 1.2;

            meteors.push({{
                x: startX,
                y: startY,
                len: len,
                speed: speed,
                angle: angle,
                alpha: 1.0,
                fade: Math.random() * 0.018 + 0.012,
                width: widthThick,
                sparks: []
            }});
        }}

        var meteorTimer = 0;
        var nextMeteorInterval = 60 + Math.floor(Math.random() * 100); // Rapid & frequent (every ~1.5 - 3 seconds)

        // Animation Loop
        function animate() {{
            if (document.hidden) {{
                requestAnimationFrame(animate);
                return;
            }}

            // Deep Space Background Canvas Fill
            ctx.fillStyle = '#050814';
            ctx.fillRect(0, 0, width, height);

            // A. Draw Shifting Cosmic Nebulae
            for (var n = 0; n < nebulae.length; n++) {{
                var neb = nebulae[n];
                neb.x += neb.vx;
                neb.y += neb.vy;
                if (neb.x < -150) neb.x = width + 150;
                if (neb.x > width + 150) neb.x = -150;
                if (neb.y < -150) neb.y = height + 150;
                if (neb.y > height + 150) neb.y = -150;

                neb.phase += 0.008;
                var currentR = neb.r + Math.sin(neb.phase) * 25;

                var nGrad = ctx.createRadialGradient(neb.x, neb.y, neb.r1, neb.x, neb.y, currentR);
                nGrad.addColorStop(0, neb.col1);
                nGrad.addColorStop(1, neb.col2);

                ctx.fillStyle = nGrad;
                ctx.beginPath();
                ctx.arc(neb.x, neb.y, currentR, 0, Math.PI * 2);
                ctx.fill();
            }}

            // B. Draw Celestial Orbs (Surya & Chandra)
            for (var o = 0; o < celestialOrbs.length; o++) {{
                var orb = celestialOrbs[o];
                orb.x += orb.vx;
                orb.y += orb.vy;
                if (orb.x < -80) orb.x = width + 80;
                if (orb.x > width + 80) orb.x = -80;
                if (orb.y < -80) orb.y = height + 80;
                if (orb.y > height + 80) orb.y = -80;

                orb.pulse += 0.02;
                var glowSize = orb.r + Math.sin(orb.pulse) * 6;

                // Multi-layered corona
                var oGrad = ctx.createRadialGradient(orb.x, orb.y, 2, orb.x, orb.y, glowSize * 2.5);
                oGrad.addColorStop(0, orb.col + '0.8)');
                oGrad.addColorStop(0.35, orb.col + '0.35)');
                oGrad.addColorStop(0.7, orb.col + '0.12)');
                oGrad.addColorStop(1, orb.col + '0)');

                ctx.fillStyle = oGrad;
                ctx.beginPath();
                ctx.arc(orb.x, orb.y, glowSize * 2.5, 0, Math.PI * 2);
                ctx.fill();

                // Core orb body
                ctx.fillStyle = orb.type === 'sun' ? '#FFFBEB' : '#F0F9FF';
                ctx.beginPath();
                ctx.arc(orb.x, orb.y, orb.r * 0.35, 0, Math.PI * 2);
                ctx.fill();
            }}

            // C. Draw Constellation Connectors
            ctx.lineWidth = 0.6;
            for (var k = 0; k < constellationPairs.length; k++) {{
                var pair = constellationPairs[k];
                var s1 = stars[pair[0]];
                var s2 = stars[pair[1]];
                if (s1 && s2) {{
                    var dist = Math.hypot(s2.x - s1.x, s2.y - s1.y);
                    if (dist < 180) {{
                        var lineAlpha = (1 - dist / 180) * 0.16 * Math.sin(s1.alpha);
                        if (lineAlpha > 0) {{
                            ctx.strokeStyle = 'rgba(212, 175, 55, ' + lineAlpha + ')';
                            ctx.beginPath();
                            ctx.moveTo(s1.x, s1.y);
                            ctx.lineTo(s2.x, s2.y);
                            ctx.stroke();
                        }}
                    }}
                }}
            }}

            // D. Draw Twinkling Starfield
            for (var sIdx = 0; sIdx < stars.length; sIdx++) {{
                var st = stars[sIdx];
                st.x += st.vx;
                st.y += st.vy;
                if (st.x < 0) st.x = width;
                if (st.x > width) st.x = 0;
                if (st.y < 0) st.y = height;
                if (st.y > height) st.y = 0;

                st.alpha += st.twinkleSpeed;
                var bAlpha = Math.abs(Math.sin(st.alpha)) * 0.8 + 0.2;

                ctx.fillStyle = st.color;
                ctx.globalAlpha = bAlpha;
                ctx.beginPath();
                ctx.arc(st.x, st.y, st.r, 0, Math.PI * 2);
                ctx.fill();

                // Bright stars cross flare diffraction spikes
                if (st.hasSpike && bAlpha > 0.6) {{
                    ctx.strokeStyle = st.color;
                    ctx.lineWidth = 0.5;
                    ctx.globalAlpha = (bAlpha - 0.5) * 0.6;
                    var spikeLen = st.r * 3.5;
                    ctx.beginPath();
                    ctx.moveTo(st.x - spikeLen, st.y);
                    ctx.lineTo(st.x + spikeLen, st.y);
                    ctx.moveTo(st.x, st.y - spikeLen);
                    ctx.lineTo(st.x, st.y + spikeLen);
                    ctx.stroke();
                }}
            }}
            ctx.globalAlpha = 1.0;

            // E. Spawn and Render Shooting Meteors (उल्कापिंड)
            meteorTimer++;
            if (meteorTimer > nextMeteorInterval) {{
                spawnMeteor();
                meteorTimer = 0;
                nextMeteorInterval = 60 + Math.floor(Math.random() * 110);
            }}

            for (var mIdx = meteors.length - 1; mIdx >= 0; mIdx--) {{
                var met = meteors[mIdx];
                met.x += Math.cos(met.angle) * met.speed;
                met.y += Math.sin(met.angle) * met.speed;
                met.alpha -= met.fade;

                if (met.alpha <= 0 || met.x > width + 250 || met.y > height + 250) {{
                    meteors.splice(mIdx, 1);
                    continue;
                }}

                var tailX = met.x - Math.cos(met.angle) * met.len;
                var tailY = met.y - Math.sin(met.angle) * met.len;

                // Luminous Gradient Tail (Transparent -> Electric Cyan -> Blazing White/Gold)
                var mGrad = ctx.createLinearGradient(tailX, tailY, met.x, met.y);
                mGrad.addColorStop(0, 'rgba(255, 255, 255, 0)');
                mGrad.addColorStop(0.5, 'rgba(56, 189, 248, ' + (met.alpha * 0.5) + ')');
                mGrad.addColorStop(0.85, 'rgba(253, 224, 71, ' + (met.alpha * 0.85) + ')');
                mGrad.addColorStop(1, 'rgba(255, 255, 255, ' + met.alpha + ')');

                ctx.strokeStyle = mGrad;
                ctx.lineWidth = met.width;
                ctx.lineCap = 'round';
                ctx.beginPath();
                ctx.moveTo(tailX, tailY);
                ctx.lineTo(met.x, met.y);
                ctx.stroke();

                // Blazing Meteor Core Head
                ctx.fillStyle = 'rgba(255, 255, 255, ' + met.alpha + ')';
                ctx.beginPath();
                ctx.arc(met.x, met.y, met.width * 1.8, 0, Math.PI * 2);
                ctx.fill();

                // Sparkles shedding off head
                if (Math.random() < 0.4) {{
                    met.sparks.push({{
                        x: met.x - (Math.random() - 0.5) * 4,
                        y: met.y - (Math.random() - 0.5) * 4,
                        alpha: met.alpha,
                        size: Math.random() * 1.2 + 0.6
                    }});
                }}

                for (var sp = met.sparks.length - 1; sp >= 0; sp--) {{
                    var spark = met.sparks[sp];
                    spark.alpha -= 0.05;
                    if (spark.alpha <= 0) {{
                        met.sparks.splice(sp, 1);
                        continue;
                    }}
                    ctx.fillStyle = 'rgba(253, 224, 71, ' + spark.alpha + ')';
                    ctx.beginPath();
                    ctx.arc(spark.x, spark.y, spark.size, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}

            requestAnimationFrame(animate);
        }}

        requestAnimationFrame(animate);
    }})();
    </script>
    """

def update_html(filepath, is_mobile=False):
    print(f"Updating cosmic engine in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Remove any existing cosmic scripts/canvases
    pattern = r'<!-- =========================================================================\s+COSMIC VOID CANVAS:.*?<\/script>\s*'
    c = re.sub(pattern, '', c, flags=re.DOTALL)
    pattern2 = r'<!-- =========================================================================\s+COSMIC LIVING WALLPAPER.*?<\/script>\s*'
    c = re.sub(pattern2, '', c, flags=re.DOTALL)
    c = re.sub(r'<canvas id="cosmicVoidCanvas[^"]*"><\/canvas>', '', c)

    new_engine = get_cosmic_engine_js(is_mobile=is_mobile)

    # Insert right before </body>
    last_body_pos = c.rfind('</body>')
    if last_body_pos != -1:
        c_final = c[:last_body_pos] + new_engine + "\n" + c[last_body_pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c_final)
        print(f"  ✓ Injected high-performance Cosmic Living Engine before </body> in {filepath}")
    else:
        print(f"  ✗ </body> not found in {filepath}!")

if __name__ == '__main__':
    update_css()
    update_html('index.html', is_mobile=False)
    update_html('mobile/index.html', is_mobile=True)
