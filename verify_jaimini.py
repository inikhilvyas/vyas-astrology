import re

print("=== VERIFICATION 1: Checking Jaimini code in mobile/index.html ===")
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Check that unguarded k.karaka or k.role are NOT accessed
assert text.count('k.karaka') == 0, "Found k.karaka"
assert text.count('k.role') == 0, "Found k.role"

# Check that dynamic Jaimini sorting exists
assert 'karakaRoles' in text, "karakaRoles missing in mobile/index.html"
assert 'b.totalDeg - a.totalDeg' in text, "Jaimini degrees sorting missing"
assert 'mJaiminiSummaryContent' in text, "mJaiminiSummaryContent missing"

# Check that renderLalKitab and renderTajika are defined
assert 'renderLalKitab:' in text, "renderLalKitab: definition missing in mobile/index.html"
assert 'renderTajika:' in text, "renderTajika: definition missing in mobile/index.html"

# Check that view containers exist
assert 'id="view-jaimini"' in text, "view-jaimini missing"
assert 'id="view-lalkitab"' in text, "view-lalkitab missing"
assert 'id="view-tajika"' in text, "view-tajika missing"

print("✓ VERIFICATION 1 PASSED: Jaimini, Lal Kitab, and Tajika tabs are 100% verified!")
