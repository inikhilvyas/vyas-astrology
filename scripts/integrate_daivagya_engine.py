#!/usr/bin/env python3
"""
VYAS ASTRA — Daivagya Engine Integration Script
Integrates vyas_daivagya_engine.js into index.html:
  Step 1: Add <script src="js/vyas_daivagya_engine.js"> before </head>
  Step 2: Add yoga/natal query detection (isYogaOrNatalQuery) to bypass panchang route
  Step 3: Hook VyasDaivagyaCore.computeContext() into askSage systemPrompt
  Step 4: Verify no duplicate insertions
"""
import re, sys, shutil, os

HTML_PATH = r"g:\software\simpa\VYAS\index.html"
BACKUP_PATH = r"g:\software\simpa\VYAS\index.html.bak_preengine"

print("=== VYAS DAIVAGYA ENGINE INTEGRATION ===")

# Read file
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()
original_len = len(content)
print(f"Original size: {original_len:,} bytes")

# ---- STEP 1: Add script tag before </head> ----
SCRIPT_TAG = '<script src="js/vyas_daivagya_engine.js"></script>'
if 'vyas_daivagya_engine.js' in content:
    print("STEP 1: Script tag already present — SKIP")
else:
    target = '</head>'
    replacement = f'    {SCRIPT_TAG}\n</head>'
    if target in content:
        content = content.replace(target, replacement, 1)
        print(f"STEP 1: Added <script src='js/vyas_daivagya_engine.js'></script> before </head> ✓")
    else:
        print("STEP 1 ERROR: </head> not found!")
        sys.exit(1)

# ---- STEP 2: Add isYogaOrNatalQuery before isPanchangOrAxiomQuery ----
YOGA_DETECT = """var isYogaOrNatalQuery = /(केमद्रुम|गजकेसरी|राजयोग|मंगल दोष|बुधादित्य|विपरीत|काल सर्प|नीचभंग|गुरु चांडाल|दशा|महादशा|अंतर्दशा|भाव|लग्न|कुण्डली|योग|dosha|dasha|yoga|lagna|bhava|kundali|panchamahapurusha|neechabhanga|kaalsarpa|mangaladosha)/i.test(q);"""

TARGET_PANCHANG = 'var isPanchangOrAxiomQuery = /(एकादशी|ekadashi|'
if 'isYogaOrNatalQuery' in content:
    print("STEP 2: isYogaOrNatalQuery already present — SKIP")
elif TARGET_PANCHANG in content:
    replacement2 = YOGA_DETECT + '\n                ' + TARGET_PANCHANG
    content = content.replace(TARGET_PANCHANG, replacement2, 1)
    print("STEP 2: Added isYogaOrNatalQuery detection ✓")
else:
    print("STEP 2 WARNING: isPanchangOrAxiomQuery target not found — trying regex")
    m = re.search(r'(var isPanchangOrAxiomQuery = /\()', content)
    if m:
        pos = m.start()
        content = content[:pos] + YOGA_DETECT + '\n                ' + content[pos:]
        print("STEP 2: Added via regex fallback ✓")
    else:
        print("STEP 2 ERROR: Could not find isPanchangOrAxiomQuery")
        sys.exit(1)

# ---- STEP 2b: Modify isPanchangOrAxiomQuery to exclude yoga/natal queries ----
OLD_PANCHANG_ASSIGN = 'var isPanchangOrAxiomQuery = /(एकादशी|ekadashi|'
NEW_PANCHANG_ASSIGN = 'var isPanchangOrAxiomQuery = !isYogaOrNatalQuery && /(एकादशी|ekadashi|'

if NEW_PANCHANG_ASSIGN in content:
    print("STEP 2b: isPanchangOrAxiomQuery exclusion already set — SKIP")
elif OLD_PANCHANG_ASSIGN in content:
    content = content.replace(OLD_PANCHANG_ASSIGN, NEW_PANCHANG_ASSIGN, 1)
    print("STEP 2b: Modified isPanchangOrAxiomQuery to exclude yoga/natal queries ✓")
else:
    print("STEP 2b WARNING: Could not find exact isPanchangOrAxiomQuery string to modify")

# ---- STEP 3: Hook VyasDaivagyaCore.computeContext into natal chart systemPrompt ----
# Target: the else branch where natal chart data is built, just after planets string is built
# We'll insert after "var drishtiLines = [];"  which appears in natal branch
# and before "activeChart.planet_table.forEach" which builds drishti

HOOK_INSERT = """
                    // ═══════════════════════════════════════════════════════════════
                    // DAIVAGYA ENGINE: Pre-computed Jyotish Context Injection
                    // VyasDaivagyaCore computes yogas, dasha, bala, house analysis
                    // before the AI prompt is sent — zero hallucination pre-computation
                    // ═══════════════════════════════════════════════════════════════
                    var daivagyaContext = '';
                    if (window.VyasDaivagyaCore && typeof VyasDaivagyaCore.computeContext === 'function') {
                        try {
                            daivagyaContext = VyasDaivagyaCore.computeContext(query, activeChart);
                        } catch(e) {
                            console.warn('VyasDaivagyaCore error:', e);
                        }
                    }
"""

TARGET_DRISHTI = 'var drishtiLines = [];'
if 'VyasDaivagyaCore' in content and 'computeContext' in content:
    print("STEP 3: VyasDaivagyaCore hook already present — SKIP")
elif TARGET_DRISHTI in content:
    content = content.replace(TARGET_DRISHTI, HOOK_INSERT + '\n                    ' + TARGET_DRISHTI, 1)
    print("STEP 3: Added VyasDaivagyaCore.computeContext() hook before drishtiLines ✓")
else:
    print("STEP 3 WARNING: drishtiLines target not found — skipping hook")

# ---- STEP 3b: Append daivagyaContext to systemPrompt array before API call ----
# Find the systemPrompt join for natal branch and append daivagyaContext
# Target: the last item in the natal systemPrompt array before ].join
# We'll find the unique string near the end of the natal systemPrompt

SYSTEMPROMPT_INJECTION_MARKER = '"4. भाषा अत्यंत आदरपूर्ण, विद्वतापूर्ण, शास्त्रीय एवं निर्भीक हो। सत्य का दर्पण दिखाएं किंतु जातक को आशा एवं आध्यात्मिक संबल दें।"'
DAIVAGYA_APPEND = '''
                        "\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                        "🔮 PRE-COMPUTED DAIVAGYA ENGINE ANALYSIS (Zero-Hallucination Block):",
                        daivagyaContext || "चार्ट डेटा उपलब्ध है।",
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"'''

if 'PRE-COMPUTED DAIVAGYA ENGINE' in content:
    print("STEP 3b: daivagyaContext injection in systemPrompt already present — SKIP")
elif SYSTEMPROMPT_INJECTION_MARKER in content:
    content = content.replace(
        SYSTEMPROMPT_INJECTION_MARKER,
        SYSTEMPROMPT_INJECTION_MARKER + ',' + DAIVAGYA_APPEND,
        1
    )
    print("STEP 3b: Appended daivagyaContext to natal systemPrompt array ✓")
else:
    print("STEP 3b WARNING: Could not find systemPrompt injection marker — skipping")

# ---- Verify no double replacement ----
count1 = content.count('vyas_daivagya_engine.js')
count2 = content.count('isYogaOrNatalQuery')
count3 = content.count('VyasDaivagyaCore')
print(f"\nVerification counts:")
print(f"  vyas_daivagya_engine.js references: {count1}")
print(f"  isYogaOrNatalQuery references: {count2}")
print(f"  VyasDaivagyaCore references: {count3}")

# ---- Write backup then write new file ----
shutil.copy2(HTML_PATH, BACKUP_PATH)
print(f"\nBackup written to: {BACKUP_PATH}")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"New size: {new_len:,} bytes (delta: +{new_len - original_len:,})")
print("\n=== INTEGRATION COMPLETE ===")

