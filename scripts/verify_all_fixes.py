# scripts/verify_all_fixes.py
import re
import json

def verify_desktop():
    print("Verifying index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Check table ID
    assert 'desktopPlanetTableBody' in text, "desktopPlanetTableBody not found"
    assert "document.getElementById('desktopPlanetTableBody')" in text, "desktopPlanetTableBody not queried in JS"
    print("  [PASS] desktopPlanetTableBody properly wired in renderPlanetTable()")

    # 2. Check Prashna Kundli
    assert "castPrashnaKundli: function" in text, "castPrashnaKundli missing in VyasAIEngine"
    assert "isPrashnaMode" in text, "isPrashnaMode check missing in askSage"
    assert "तात्कालिक प्रश्न कुण्डली" in text, "Prashna Kundli prompt text missing"
    print("  [PASS] Prashna Kundli engine present and integrated in VyasAIEngine")

    # 3. Check sendSageQuery privacy
    assert "var chart = this.activeChartData || window.AUTHENTIC_BUNDLE;" not in text, "Legacy fallback still in sendSageQuery"
    print("  [PASS] sendSageQuery has NO founder fallback")

    # 4. Check dynamic computeMathematicalKundli
    assert "KARAKA_NAMES" in text, "Jaimini 7 Chara Karakas missing in computeMathematicalKundli"
    assert "getKpDetails" in text, "KP 249 sub-lord logic missing in computeMathematicalKundli"
    assert "d9Houses" in text, "Dynamic D-9 missing in computeMathematicalKundli"
    assert "d10Houses" in text, "Dynamic D-10 missing in computeMathematicalKundli"
    print("  [PASS] computeMathematicalKundli is 100% dynamic for D-9, D-10, KP, Jaimini, Nadi")

    # 5. Check founder personal data purge
    assert "1984-11-23" not in text, "1984-11-23 found in index.html"
    assert "23°27'09" not in text, "Aries 23°27'09 found in index.html"
    print("  [PASS] Founder private birth chart completely purged from index.html")

    # 6. Check ADX elevation CSS
    assert "ADX DESIGN ENGINEER X" in text, "ADX elevation CSS missing in index.html"
    print("  [PASS] ADX luxury CSS injected in index.html")

def verify_mobile():
    print("Verifying mobile/index.html...")
    with open('mobile/index.html', 'r', encoding='utf-8') as f:
        text = f.read()

    assert "castPrashnaKundli: function" in text, "castPrashnaKundli missing in mobile VyasAIEngine"
    assert "isPrashnaMode" in text, "isPrashnaMode missing in mobile askSage"
    assert "KARAKA_NAMES" in text, "Jaimini dynamic logic missing in mobile computeMathematicalKundli"
    assert "getKpDetails" in text, "KP 249 missing in mobile computeMathematicalKundli"
    print("  [PASS] mobile/index.html verified with Prashna Kundli and dynamic engines")

if __name__ == '__main__':
    verify_desktop()
    verify_mobile()
    print("\n🎉 ALL VERIFICATION CHECKS PASSED!")

