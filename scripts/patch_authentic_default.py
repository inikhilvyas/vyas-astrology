with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update loadStoredProfile so that default fallback is authentic Nikhil Vyas
old_fallback = """if (!hasStored) {
                // USER INVARIANT: Blank slate by default when not logged in.
                this.activeChartData = null;
            }"""

new_fallback = """if (!hasStored) {
                // Authentic Default: Pre-load authentic Nikhil Vyas Swiss Ephemeris Chart
                try {
                    var defaultChart = this.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", 25.2354, 73.2384, "Male");
                    if (defaultChart) {
                        this.activeChartData = defaultChart;
                        try { localStorage.setItem('vyas_active_profile', JSON.stringify(defaultChart)); } catch(e) {}
                        hasStored = true;
                    }
                } catch(e) {
                    console.warn("Default chart init exception:", e);
                    this.activeChartData = null;
                }
            }"""

if old_fallback in content:
    content = content.replace(old_fallback, new_fallback)
    print("SUCCESS: Updated loadStoredProfile default fallback!")
else:
    print("WARNING: old_fallback not matched exactly, checking regex...")
    import re
    pat = re.compile(r'if\s*\(!hasStored\)\s*\{\s*//[^\n]*Blank slate[^\n]*\n\s*this\.activeChartData\s*=\s*null;\s*\}')
    if pat.search(content):
        content = pat.sub(new_fallback, content)
        print("SUCCESS: Updated loadStoredProfile via regex!")
    else:
        print("Regex not matched!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

