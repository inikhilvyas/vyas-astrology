import re

def fix_css():
    print("Fixing styles/adx_elevation.css...")
    with open('styles/adx_elevation.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Remove the previous faulty block if present
    css = re.sub(r'/\* =========================================================================\s+ANIMATED COSMIC LIVING WALLPAPER.*', '', css, flags=re.DOTALL)

    # Clean, correct elevation:
    # 1. Canvas MUST be z-index: -1 so it stays strictly in the background!
    # 2. Body background is transparent so canvas shines through
    # 3. All content remains in front and completely visible!
    clean_cosmic_css = """
/* =========================================================================
   ANIMATED COSMIC LIVING WALLPAPER (NON-INTRUSIVE BACKGROUND)
   ========================================================================= */
html {
    background-color: #060913 !important;
}

body {
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
}

#cosmicVoidCanvas, #cosmicVoidCanvasMobile {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    pointer-events: none !important;
    z-index: -1 !important;
    opacity: 0.95 !important;
}

.cockpit-container {
    position: relative;
    z-index: 1;
}

.cockpit-col {
    background: rgba(10, 16, 30, 0.78) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(229, 193, 88, 0.18) !important;
}

.content-card {
    background: rgba(14, 22, 42, 0.72) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
}
"""
    css = css.strip() + "\n" + clean_cosmic_css
    with open('styles/adx_elevation.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("  ✓ Corrected styles/adx_elevation.css")

def get_living_cosmic_js(is_mobile=False):
    canvas_id = 'cosmicVoidCanvasMobile' if is_mobile else 'cosmicVoidCanvas'
    fn_name = 'initMobileCosmicWallpaper' if is_mobile else 'initCosmicWallpaper'
    star_count = 120 if is_mobile else 200

    return f"""
    <!-- =========================================================================
         COSMIC LIVING WALLPAPER & SHOOTING STARS (NON-INTRUSIVE BACKGROUND)
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
        canvas.style.zIndex = '-1'; // Strictly in background

        var ctx = canvas.getContext('2d');
        var width, height;

        function resize() {{
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }}
        window.addEventListener('resize', resize);
        resize();

        // 1. Multi-layered Stars with Visible Twinkling
        var stars = [];
        var STAR_PALETTE = ['#FFFFFF', '#E0F2FE', '#BAE6FD', '#FDE68A', '#FEF08A', '#FBCFE8'];
        for (var i = 0; i < {star_count}; i++) {{
            stars.push({{
                x: Math.random() * width,
                y: Math.random() * height,
                r: Math.random() < 0.12 ? (Math.random() * 1.5 + 1.5) : (Math.random() * 1.0 + 0.5),
                color: STAR_PALETTE[Math.floor(Math.random() * STAR_PALETTE.length)],
                alpha: Math.random(),
                twinkleSpeed: Math.random() * 0.05 + 0.02, // Active, noticeable twinkle
                vx: (Math.random() - 0.5) * 0.25,          // Gentle drift
                vy: (Math.random() - 0.5) * 0.25,
                hasSpike: Math.random() < 0.10
            }});
        }}

        // 2. Cosmic Constellation Asterisms
        var constellationPairs = [];
        for (var c = 0; c < 16; c++) {{
            var idx1 = Math.floor(Math.random() * (stars.length - 1));
            var idx2 = idx1 + 1;
            constellationPairs.push([idx1, idx2]);
        }}

        // 3. Shifting Atmospheric Cosmic Nebulae
        var nebulae = [
            {{ x: width * 0.15, y: height * 0.25, r: 280, col: 'rgba(30, 58, 138, 0.28)', phase: 0, speed: 0.015 }},
            {{ x: width * 0.85, y: height * 0.20, r: 260, col: 'rgba(180, 83, 9, 0.18)', phase: 2.0, speed: 0.012 }},
            {{ x: width * 0.50, y: height * 0.80, r: 300, col: 'rgba(88, 28, 135, 0.20)', phase: 4.0, speed: 0.018 }}
        ];

        // 4. Frequent Blazing Shooting Stars (Meteors)
        var meteors = [];
        function spawnMeteor() {{
            var startX = Math.random() * (width * 0.8) + (width * 0.1);
            var startY = Math.random() * (height * 0.4);
            var angle = Math.PI / 4 + (Math.random() - 0.5) * 0.25; // 45 degree streak
            var speed = Math.random() * 9 + 9; // Fast and dramatic
            var len = Math.random() * 120 + 80;

            meteors.push({{
                x: startX,
                y: startY,
                len: len,
                speed: speed,
                angle: angle,
                alpha: 1.0,
                fade: 0.020,
                width: Math.random() * 1.5 + 1.2
            }});
        }}

        var meteorTimer = 0;
        var nextMeteorInterval = 40 + Math.floor(Math.random() * 60); // Spawns every 1 to 2 seconds!

        // Initial spawn so a shooting star is seen right away
        spawnMeteor();

        function animate() {{
            if (document.hidden) {{
                requestAnimationFrame(animate);
                return;
            }}

            // Draw deep space background
            ctx.fillStyle = '#060913';
            ctx.fillRect(0, 0, width, height);

            // A. Draw Breathing Nebulae
            for (var n = 0; n < nebulae.length; n++) {{
                var neb = nebulae[n];
                neb.phase += neb.speed;
                var currentR = neb.r + Math.sin(neb.phase) * 35;

                var nGrad = ctx.createRadialGradient(neb.x, neb.y, 10, neb.x, neb.y, currentR);
                nGrad.addColorStop(0, neb.col);
                nGrad.addColorStop(1, 'rgba(6, 9, 19, 0)');

                ctx.fillStyle = nGrad;
                ctx.beginPath();
                ctx.arc(neb.x, neb.y, currentR, 0, Math.PI * 2);
                ctx.fill();
            }}

            // B. Draw Constellation Lines
            ctx.lineWidth = 0.8;
            for (var k = 0; k < constellationPairs.length; k++) {{
                var pair = constellationPairs[k];
                var s1 = stars[pair[0]];
                var s2 = stars[pair[1]];
                if (s1 && s2) {{
                    var dist = Math.hypot(s2.x - s1.x, s2.y - s1.y);
                    if (dist < 180) {{
                        var lineAlpha = (1 - dist / 180) * 0.22 * Math.abs(Math.sin(s1.alpha));
                        ctx.strokeStyle = 'rgba(212, 175, 55, ' + lineAlpha + ')';
                        ctx.beginPath();
                        ctx.moveTo(s1.x, s1.y);
                        ctx.lineTo(s2.x, s2.y);
                        ctx.stroke();
                    }}
                }}
            }}

            // C. Draw Twinkling & Floating Stars
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

                if (st.hasSpike && bAlpha > 0.6) {{
                    ctx.strokeStyle = st.color;
                    ctx.lineWidth = 0.6;
                    ctx.globalAlpha = (bAlpha - 0.5) * 0.7;
                    var spikeLen = st.r * 4.0;
                    ctx.beginPath();
                    ctx.moveTo(st.x - spikeLen, st.y);
                    ctx.lineTo(st.x + spikeLen, st.y);
                    ctx.moveTo(st.x, st.y - spikeLen);
                    ctx.lineTo(st.x, st.y + spikeLen);
                    ctx.stroke();
                }}
            }}
            ctx.globalAlpha = 1.0;

            // D. Shooting Stars (Meteors)
            meteorTimer++;
            if (meteorTimer > nextMeteorInterval) {{
                spawnMeteor();
                meteorTimer = 0;
                nextMeteorInterval = 40 + Math.floor(Math.random() * 70); // Very frequent!
            }}

            for (var mIdx = meteors.length - 1; mIdx >= 0; mIdx--) {{
                var met = meteors[mIdx];
                met.x += Math.cos(met.angle) * met.speed;
                met.y += Math.sin(met.angle) * met.speed;
                met.alpha -= met.fade;

                if (met.alpha <= 0 || met.x > width + 200 || met.y > height + 200) {{
                    meteors.splice(mIdx, 1);
                    continue;
                }}

                var tailX = met.x - Math.cos(met.angle) * met.len;
                var tailY = met.y - Math.sin(met.angle) * met.len;

                var mGrad = ctx.createLinearGradient(tailX, tailY, met.x, met.y);
                mGrad.addColorStop(0, 'rgba(255, 255, 255, 0)');
                mGrad.addColorStop(0.5, 'rgba(56, 189, 248, ' + (met.alpha * 0.6) + ')');
                mGrad.addColorStop(0.85, 'rgba(253, 224, 71, ' + (met.alpha * 0.9) + ')');
                mGrad.addColorStop(1, 'rgba(255, 255, 255, ' + met.alpha + ')');

                ctx.strokeStyle = mGrad;
                ctx.lineWidth = met.width;
                ctx.lineCap = 'round';
                ctx.beginPath();
                ctx.moveTo(tailX, tailY);
                ctx.lineTo(met.x, met.y);
                ctx.stroke();

                ctx.fillStyle = 'rgba(255, 255, 255, ' + met.alpha + ')';
                ctx.beginPath();
                ctx.arc(met.x, met.y, met.width * 1.8, 0, Math.PI * 2);
                ctx.fill();
            }}

            requestAnimationFrame(animate);
        }}

        requestAnimationFrame(animate);
    }})();
    </script>
    """

def update_file(filepath, is_mobile=False):
    print(f"Updating {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Clean previous canvas & scripts
    pattern = r'<!-- =========================================================================\s+COSMIC LIVING WALLPAPER.*?<\/script>\s*'
    c = re.sub(pattern, '', c, flags=re.DOTALL)
    c = re.sub(r'<canvas id="cosmicVoidCanvas[^"]*"><\/canvas>', '', c)

    new_engine = get_living_cosmic_js(is_mobile=is_mobile)

    last_body = c.rfind('</body>')
    if last_body != -1:
        c = c[:last_body] + new_engine + "\n" + c[last_body:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"  ✓ Cleanly injected into {filepath}")
    else:
        print(f"  ✗ </body> not found in {filepath}")

if __name__ == '__main__':
    fix_css()
    update_file('index.html', is_mobile=False)
    update_file('mobile/index.html', is_mobile=True)

