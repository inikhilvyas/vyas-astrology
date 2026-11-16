import re

def fix_file(filepath, canvas_id, fn_name, is_mobile=False):
    print(f"Fixing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Find the inserted script block and remove it if it was inside generateLivePdfReport
    # The cosmic block starts with '<!-- =========================================================================\n         COSMIC VOID CANVAS:'
    # and ends with '</script>'
    pattern = r'<!-- =========================================================================\s+COSMIC VOID CANVAS:.*?<\/script>\s*'
    c_clean = re.sub(pattern, '', c, flags=re.DOTALL)
    print(f"  Removed misplaced cosmic script blocks. Length change: {len(c)} -> {len(c_clean)}")

    # Cosmic script content
    num_stars = 90 if is_mobile else 140
    opacity = '0.85' if is_mobile else '0.90'
    planets_code = """
        // Slow Orbiting Cosmic Halos (Jupiter / Golden Surya Aura)
        var planets = [
            { x: width * 0.85, y: height * 0.25, r: 50, color1: 'rgba(229, 193, 88, 0.20)', color2: 'rgba(229, 193, 88, 0)', vx: -0.04, vy: 0.02 },
            { x: width * 0.12, y: height * 0.75, r: 70, color1: 'rgba(59, 130, 246, 0.15)', color2: 'rgba(59, 130, 246, 0)', vx: 0.03, vy: -0.03 }
        ];
    """ if not is_mobile else "var planets = [];"

    cosmic_script = f"""
    <!-- =========================================================================
         COSMIC VOID CANVAS: ANIMATED LIVING CELESTIAL BACKGROUND & SHOOTING STARS
         ========================================================================= -->
    <script>
    (function {fn_name}() {{
        if (document.getElementById('{canvas_id}')) return;
        var canvas = document.createElement('canvas');
        canvas.id = '{canvas_id}';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '-1';
        canvas.style.opacity = '{opacity}';
        document.body.prepend(canvas);

        var ctx = canvas.getContext('2d');
        var width, height;

        function resize() {{
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }}
        window.addEventListener('resize', resize);
        resize();

        // 1. Drifting Twinkling Stars
        var stars = [];
        var STAR_COLORS = ['#FFFFFF', '#FFE8A3', '#93C5FD', '#FDE047', '#E0F2FE'];
        for (var i = 0; i < {num_stars}; i++) {{
            stars.push({{
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.5 + 0.4,
                color: STAR_COLORS[Math.floor(Math.random() * STAR_COLORS.length)],
                alpha: Math.random(),
                speed: Math.random() * 0.02 + 0.005,
                vx: (Math.random() - 0.5) * 0.14,
                vy: (Math.random() - 0.5) * 0.14
            }});
        }}

        {planets_code}

        // 2. Shooting Stars / Meteors (तारे गुजरते हुए)
        var meteors = [];
        function spawnMeteor() {{
            meteors.push({{
                x: Math.random() * width * 0.8 + width * 0.1,
                y: Math.random() * height * 0.35,
                len: Math.random() * 100 + 70,
                speed: Math.random() * 6 + 6,
                angle: Math.PI / 4 + (Math.random() - 0.5) * 0.2, // ~45 deg downward
                alpha: 1,
                fade: Math.random() * 0.015 + 0.012,
                width: Math.random() * 1.4 + 1
            }});
        }}

        var meteorTimer = 0;
        var nextMeteorInterval = 120 + Math.floor(Math.random() * 180);

        function animate() {{
            if (document.hidden) {{
                requestAnimationFrame(animate);
                return;
            }}

            ctx.clearRect(0, 0, width, height);

            // Planetary Halos
            for (var p = 0; p < planets.length; p++) {{
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
            }}

            // Stars
            for (var i = 0; i < stars.length; i++) {{
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
            }}

            // Shooting Stars
            meteorTimer++;
            if (meteorTimer > nextMeteorInterval) {{
                spawnMeteor();
                meteorTimer = 0;
                nextMeteorInterval = 130 + Math.floor(Math.random() * 190);
            }}

            for (var m = meteors.length - 1; m >= 0; m--) {{
                var met = meteors[m];
                met.x += Math.cos(met.angle) * met.speed;
                met.y += Math.sin(met.angle) * met.speed;
                met.alpha -= met.fade;

                if (met.alpha <= 0 || met.x > width + 200 || met.y > height + 200) {{
                    meteors.splice(m, 1);
                    continue;
                }}

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
            }}

            ctx.globalAlpha = 1;
            requestAnimationFrame(animate);
        }}

        requestAnimationFrame(animate);
    }})();
    </script>
    """

    # Insert right before the FINAL </body> in the file
    last_body_pos = c_clean.rfind('</body>')
    if last_body_pos != -1:
        c_final = c_clean[:last_body_pos] + cosmic_script + "\n" + c_clean[last_body_pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c_final)
        print(f"  ✓ Inserted cosmic engine at real document end ({last_body_pos}) in {filepath}")
    else:
        print(f"  ✗ Closing </body> not found in {filepath}!")

if __name__ == '__main__':
    fix_file('index.html', 'cosmicVoidCanvas', 'initCosmicWallpaper', is_mobile=False)
    fix_file('mobile/index.html', 'cosmicVoidCanvasMobile', 'initMobileCosmicWallpaper', is_mobile=True)
