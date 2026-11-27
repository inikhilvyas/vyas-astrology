/**
 * VYAS ASTRA — Universal Sub-Page Light/Dark Theme Controller
 * Syncs with Home Page (`vyas_desktop_theme`), adds a Theme Toggle button
 * to every sub-page, and adapts hardcoded dark surfaces in Light Mode.
 */
(function () {
    'use strict';
    var STORAGE_KEY = 'vyas_desktop_theme';
    var _timer = null;

    function getTheme() {
        try {
            return localStorage.getItem(STORAGE_KEY) || 'dark';
        } catch (e) {
            return 'dark';
        }
    }

    function parseRgb(str) {
        if (!str) return null;
        var m = str.match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\s*\)/i);
        if (!m) return null;
        return { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] };
    }

    function lum(c) {
        return (0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b) / 255;
    }

    function syncSurfaces() {
        var isLight = document.documentElement.getAttribute('data-theme') === 'light';
        var nodes = document.querySelectorAll('section, div, table, thead, tbody, tr, th, td, nav, header, footer, aside, article, p, span, b, strong, h1, h2, h3, h4, label, li, button, a, input, select, textarea');
        for (var i = 0; i < nodes.length; i++) {
            var el = nodes[i];
            if (el.closest && el.closest('svg')) continue;
            if (el.id === 'vyasSubpageThemeBtn') continue;
            if (el.classList && (el.classList.contains('gold-btn') || el.classList.contains('badge-tag') || el.classList.contains('badge-exalted'))) continue;

            if (isLight) {
                var cs = window.getComputedStyle(el);
                var bg = parseRgb(cs.backgroundColor);
                if (bg && bg.a > 0.35 && lum(bg) < 0.24) {
                    if (!el.hasAttribute('data-vyas-orig-bg')) {
                        el.setAttribute('data-vyas-orig-bg', el.style.background || '');
                        el.setAttribute('data-vyas-orig-bgc', el.style.backgroundColor || '');
                    }
                    var tag = el.tagName;
                    var targetBg = (tag === 'TH' || tag === 'THEAD') ? '#F1EDE2' : ((tag === 'TD' || tag === 'TR') ? 'transparent' : '#FFFFFF');
                    el.style.setProperty('background', targetBg, 'important');
                    el.style.setProperty('background-color', targetBg, 'important');
                    if (el.style.borderColor || cs.borderTopWidth !== '0px') {
                        el.style.setProperty('border-color', 'rgba(180, 134, 11, 0.25)', 'important');
                    }
                }
                var fg = parseRgb(cs.color);
                if (fg && fg.a > 0.4 && lum(fg) > 0.65) {
                    if (!el.hasAttribute('data-vyas-orig-col')) {
                        el.setAttribute('data-vyas-orig-col', el.style.color || '');
                    }
                    el.style.setProperty('color', '#0F172A', 'important');
                }
            } else {
                if (el.hasAttribute('data-vyas-orig-bg')) {
                    el.style.background = el.getAttribute('data-vyas-orig-bg');
                    el.style.backgroundColor = el.getAttribute('data-vyas-orig-bgc');
                    el.style.removeProperty('border-color');
                    el.removeAttribute('data-vyas-orig-bg');
                    el.removeAttribute('data-vyas-orig-bgc');
                }
                if (el.hasAttribute('data-vyas-orig-col')) {
                    el.style.color = el.getAttribute('data-vyas-orig-col');
                    el.removeAttribute('data-vyas-orig-col');
                }
            }
        }

        // Also adapt Kundli SVGs on sub-pages between Dark & Light themes
        var svgs = document.querySelectorAll('svg');
        for (var s = 0; s < svgs.length; s++) {
            var svg = svgs[s];
            if (svg.getAttribute('width') && parseInt(svg.getAttribute('width'), 10) < 120) continue;
            var stops = svg.querySelectorAll('stop');
            for (var st = 0; st < stops.length; st++) {
                var stopEl = stops[st];
                if (isLight) {
                    var sc = (stopEl.getAttribute('stop-color') || '').toLowerCase();
                    if (/^#0[0-9a-f]{5}$|^#1[0-9a-f]{5}$/.test(sc)) {
                        if (!stopEl.hasAttribute('data-vyas-orig-stop')) stopEl.setAttribute('data-vyas-orig-stop', sc);
                        stopEl.setAttribute('stop-color', st === 0 ? '#FCFAF6' : '#EFECE4');
                    }
                } else if (stopEl.hasAttribute('data-vyas-orig-stop')) {
                    stopEl.setAttribute('stop-color', stopEl.getAttribute('data-vyas-orig-stop'));
                    stopEl.removeAttribute('data-vyas-orig-stop');
                }
            }
            var svgEls = svg.querySelectorAll('rect, line, text, tspan');
            for (var se = 0; se < svgEls.length; se++) {
                var sel = svgEls[se];
                if (isLight) {
                    var fl = (sel.getAttribute('fill') || '').toLowerCase();
                    if (sel.tagName === 'rect' && /^#0[0-9a-f]{5}$|^#1[0-9a-f]{5}$/.test(fl)) {
                        if (!sel.hasAttribute('data-vyas-orig-fill')) sel.setAttribute('data-vyas-orig-fill', fl);
                        sel.setAttribute('fill', '#FCFAF6');
                    } else if ((sel.tagName === 'text' || sel.tagName === 'tspan') && (fl === '#f0f9ff' || fl === '#f8fafc' || fl === '#e2e8f0' || fl === '#ffffff' || fl === '#fff' || fl === '#38bdf8' || fl === '#94a3b8')) {
                        if (!sel.hasAttribute('data-vyas-orig-fill')) sel.setAttribute('data-vyas-orig-fill', fl);
                        sel.setAttribute('fill', fl === '#38bdf8' ? '#B45309' : (fl === '#94a3b8' ? '#475569' : '#1B2E4B'));
                    }
                    var sk = (sel.getAttribute('stroke') || '').toLowerCase();
                    if (sk === '#38bdf8' || sk === '#0284c7') {
                        if (!sel.hasAttribute('data-vyas-orig-stroke')) sel.setAttribute('data-vyas-orig-stroke', sk);
                        sel.setAttribute('stroke', sk === '#0284c7' ? '#B58A45' : '#243A59');
                    }
                } else {
                    if (sel.hasAttribute('data-vyas-orig-fill')) {
                        sel.setAttribute('fill', sel.getAttribute('data-vyas-orig-fill'));
                        sel.removeAttribute('data-vyas-orig-fill');
                    }
                    if (sel.hasAttribute('data-vyas-orig-stroke')) {
                        sel.setAttribute('stroke', sel.getAttribute('data-vyas-orig-stroke'));
                        sel.removeAttribute('data-vyas-orig-stroke');
                    }
                }
            }
        }
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        try { localStorage.setItem(STORAGE_KEY, theme); } catch (e) {}
        var btn = document.getElementById('vyasSubpageThemeBtn');
        if (btn) {
            btn.innerHTML = (theme === 'light') ? '🌙 डार्क मोड' : '☀️ लाइट मोड';
            btn.style.background = (theme === 'light') ? '#0F172A' : 'rgba(212,175,55,0.16)';
            btn.style.color = (theme === 'light') ? '#FFFFFF' : '#FDE68A';
            btn.style.borderColor = (theme === 'light') ? '#0F172A' : 'rgba(212,175,55,0.45)';
        }
        syncSurfaces();
    }

    function injectToggleButton() {
        if (document.getElementById('vyasSubpageThemeBtn')) return;
        var btn = document.createElement('button');
        btn.id = 'vyasSubpageThemeBtn';
        btn.type = 'button';
        btn.style.cssText = 'padding:6px 12px; border-radius:999px; border:1px solid rgba(212,175,55,0.45); font-size:0.8rem; font-weight:700; cursor:pointer; white-space:nowrap; transition:all 0.2s ease;';
        btn.onclick = function () {
            var cur = document.documentElement.getAttribute('data-theme') || 'dark';
            applyTheme(cur === 'dark' ? 'light' : 'dark');
        };

        var headerRight = document.querySelector('.top-header > div:last-child, header > div:last-child, .header-actions');
        if (headerRight) {
            headerRight.style.display = 'flex';
            headerRight.style.alignItems = 'center';
            headerRight.style.gap = '8px';
            headerRight.insertBefore(btn, headerRight.firstChild);
        } else {
            btn.style.position = 'fixed';
            btn.style.top = '12px';
            btn.style.right = '12px';
            btn.style.zIndex = '9999';
            document.body.appendChild(btn);
        }
        applyTheme(getTheme());
    }

    // Apply immediately to avoid dark flash
    document.documentElement.setAttribute('data-theme', getTheme());

    window.addEventListener('DOMContentLoaded', function () {
        injectToggleButton();
        setTimeout(syncSurfaces, 120);
        var obs = new MutationObserver(function () {
            clearTimeout(_timer);
            _timer = setTimeout(syncSurfaces, 100);
        });
        if (document.body) {
            obs.observe(document.body, { childList: true, subtree: true });
        }
    });

    window.vyasSyncThemeSurfaces = syncSurfaces;
})();
