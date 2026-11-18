print("Stage 5: Adding 1-Click Founder Quick Login in modalGoogleAuth...")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = '<span>Google खाते से साइन-इन करें</span>\n                </button>'
if target not in content:
    target = '<span>Google खाते से साइन-इन करें</span>\r\n                </button>'

print("Target found?", target in content)

quick_button = """<span>Google खाते से साइन-इन करें</span>
                </button>

                <!-- 1-Click Instant Safe Founder/Pro Access -->
                <button type="button" onclick="VyasDesktop.quickLoginFounder()" style="width:100%; margin-top:12px; display:flex; align-items:center; justify-content:center; gap:8px; background:linear-gradient(135deg, #1e293b, #0f172a); border:1.5px solid #d4af37; border-radius:24px; padding:11px 16px; color:#d4af37; font-weight:700; font-size:0.88rem; cursor:pointer; box-shadow:0 2px 8px rgba(212,175,55,0.2); transition:all 0.2s ease;">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg>
                    <span>⚡ 1-क्लिक संस्थापक PRO लॉगिन (निखिल व्यास)</span>
                </button>"""

if target in content:
    content = content.replace(target, quick_button, 1)
    print("✓ Added 1-Click Founder Quick Login button in modalGoogleAuth")
else:
    print("! Target not found, searching with regex...")
    import re
    content = re.sub(
        r'(<span>Google खाते से साइन-इन करें<\/span>\s*<\/button>)',
        r'\1\n                <!-- 1-Click Instant Safe Founder/Pro Access -->\n                <button type="button" onclick="VyasDesktop.quickLoginFounder()" style="width:100%; margin-top:12px; display:flex; align-items:center; justify-content:center; gap:8px; background:linear-gradient(135deg, #1e293b, #0f172a); border:1.5px solid #d4af37; border-radius:24px; padding:11px 16px; color:#d4af37; font-weight:700; font-size:0.88rem; cursor:pointer; box-shadow:0 2px 8px rgba(212,175,55,0.2); transition:all 0.2s ease;">\n                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg>\n                    <span>⚡ 1-क्लिक संस्थापक PRO लॉगिन (निखिल व्यास)</span>\n                </button>',
        content,
        count=1
    )
    print("✓ Regex replaced target with 1-Click button")

# Also ensure quickLoginFounder is present in VyasDesktop
if 'quickLoginFounder: function()' not in content:
    qlf_code = """quickLoginFounder: function() {
            this.googleUser = {
                name: "Nikhil Vyas",
                email: "nikhilvyas007@gmail.com",
                picture: "https://lh3.googleusercontent.com/a/default-user=s96-c",
                isPro: true
            };
            try {
                localStorage.setItem('vyas_google_user', JSON.stringify(this.googleUser));
                localStorage.setItem('vyas_pro_active', 'true');
                localStorage.setItem('vyas_pro_member_nikhilvyas007@gmail.com', 'true');
            } catch(e) {}
            this.updateGoogleAuthUI();
            this.loadStoredProfile();
            this.renderChart(this.currentVarga || 'd1');
            this.updateDailyHoroscopeUI();
            this.updateYogasBannerUI();
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderDashaTree();
            this.closeModals();
            alert("✓ स्वागतम् निखिल व्यास जी! PRO सदस्यता सफलतापूर्वक 1-क्लिक में सक्रिय हो गई है।");
        },

        """
    content = content.replace("var VyasDesktop = {", "var VyasDesktop = {\n        " + qlf_code)
    print("✓ Injected quickLoginFounder method in VyasDesktop")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Stage 5 completed successfully!")

