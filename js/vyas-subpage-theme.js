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
