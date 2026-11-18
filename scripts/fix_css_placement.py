with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the incorrectly placed pillar_css from inside JS
marker = "/* =========================================================================\n           INTERNATIONAL 4-PILLAR NAVIGATION & DUAL THEME TOKENS"
end_marker = "border-color: #E2E8F0 !important;\n        }"

if marker in content:
    idx1 = content.find(marker)
    idx2 = content.find(end_marker, idx1)
    if idx1 != -1 and idx2 != -1:
        bad_block = content[idx1:idx2 + len(end_marker)]
        content = content.replace(bad_block, '')
        print("Removed bad injection from JS string!")

# Now place pillar_css inside the real <style> tag in <head>
# Find the first </style>
first_style_close = content.find('</style>')
if first_style_close != -1:
    pillar_css_clean = """
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
    content = content[:first_style_close] + pillar_css_clean + '\n' + content[first_style_close:]
    print("Placed pillar_css in head <style>!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
