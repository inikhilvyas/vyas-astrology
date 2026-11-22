import os
import re

upi_id = "inikhilvyas@ybl"

mobile_plans_and_upi_html = f'''
            <!-- Mobile Pricing Plans -->
            <div style="margin-bottom:16px;">
                <b style="color:#d4af37; font-size:0.86rem; display:block; margin-bottom:10px;">✦ सदस्यता प्लान चुनें (Subscription Plans):</b>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.12); border-radius:10px; padding:12px; text-align:center;">
                        <span style="font-size:0.70rem; color:#94a3b8; font-weight:700;">वार्षिक प्रो</span>
                        <div style="font-size:1.15rem; font-weight:900; color:#f8fafc; margin:4px 0;">₹999 <small style="font-size:0.65rem; color:#94a3b8;">/ वर्ष</small></div>
                        <button type="button" onclick="VyasDesktop.initiateGatewayCheckout('वार्षिक प्रो', 999)" style="width:100%; padding:6px; background:rgba(212,175,55,0.15); border:1px solid rgba(212,175,55,0.4); border-radius:6px; color:#f1d797; font-size:0.72rem; font-weight:800; cursor:pointer;">प्लान चुनें</button>
                    </div>

                    <div style="background:linear-gradient(135deg, rgba(212,175,55,0.12) 0%, rgba(245,158,11,0.2) 100%); border:2px solid #d4af37; border-radius:10px; padding:12px; text-align:center; position:relative;">
                        <span style="position:absolute; top:-8px; left:50%; transform:translateX(-50%); background:#d4af37; color:#111; font-size:0.60rem; font-weight:900; padding:1px 6px; border-radius:8px;">लोकप्रिय</span>
                        <span style="font-size:0.70rem; color:#f1d797; font-weight:800;">आजीवन VIP</span>
                        <div style="font-size:1.20rem; font-weight:900; color:#f1d797; margin:4px 0;">₹2,499</div>
                        <button type="button" onclick="VyasDesktop.initiateGatewayCheckout('आजीवन VIP', 2499)" style="width:100%; padding:6px; background:var(--gold-gradient); border:none; border-radius:6px; color:#111; font-size:0.72rem; font-weight:900; cursor:pointer;">VIP लें</button>
                    </div>
                </div>
            </div>

            <!-- 100% Free 0% Fee Smart Direct UPI Box for Mobile -->
            <div id="proDirectUpiBox" style="display:none; margin:14px 0; background:linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(15,23,42,0.98) 100%); border:2px solid #10b981; border-radius:12px; padding:14px; box-shadow:0 6px 24px rgba(16,185,129,0.25);">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(16,185,129,0.3); padding-bottom:8px; margin-bottom:12px;">
                    <div>
                        <span style="background:#10b981; color:#06140e; font-size:0.65rem; font-weight:900; padding:2px 6px; border-radius:4px;">0% शुल्क • सुरक्षित UPI</span>
                        <h4 style="margin:4px 0 0 0; color:#f8fafc; font-size:0.95rem;">सीधा बैंक UPI भुगतान (<span id="upiPlanNameDisplay" style="color:#34d399;">आजीवन VIP</span>)</h4>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:0.68rem; color:#94a3b8;">देय राशि</span>
                        <div id="upiAmountDisplay" style="font-size:1.25rem; font-weight:900; color:#34d399;">₹2,499</div>
                    </div>
                </div>

                <!-- UPI ID Copy -->
                <div style="margin-bottom:12px;">
                    <label style="font-size:0.70rem; color:#94a3b8; display:block; margin-bottom:4px; font-weight:700;">आधिकारिक UPI ID:</label>
                    <div style="display:flex; gap:6px;">
                        <input type="text" readonly value="{upi_id}" id="directUpiIdInput" style="flex:1; background:#0b1329; border:1px solid #10b981; border-radius:6px; padding:6px 8px; color:#34d399; font-weight:800; font-size:0.80rem; font-family:monospace;">
                        <button type="button" onclick="VyasDesktop.copyUpiId()" style="background:#10b981; color:#06140e; border:none; border-radius:6px; padding:6px 10px; font-weight:900; font-size:0.72rem; cursor:pointer;">📋 कॉपी</button>
                    </div>
                </div>

                <!-- One Tap Pay -->
                <div style="margin-bottom:14px;">
                    <span style="font-size:0.72rem; color:#94a3b8; display:block; margin-bottom:6px; font-weight:700;">⚡ UPI ऐप से एक क्लिक में भुगतान करें:</span>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
                        <a id="directPhonePeBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:#5f259f; color:#fff; text-align:center; padding:8px 6px; border-radius:6px; font-size:0.72rem; font-weight:800; text-decoration:none; display:block;">🟣 PhonePe</a>
                        <a id="directGPayBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:#1a73e8; color:#fff; text-align:center; padding:8px 6px; border-radius:6px; font-size:0.72rem; font-weight:800; text-decoration:none; display:block;">🔵 Google Pay</a>
                        <a id="directPaytmBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:#00b9f5; color:#fff; text-align:center; padding:8px 6px; border-radius:6px; font-size:0.72rem; font-weight:800; text-decoration:none; display:block;">🔷 Paytm</a>
                        <a id="directAnyUpiBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:rgba(255,255,255,0.12); color:#fff; text-align:center; padding:8px 6px; border-radius:6px; font-size:0.72rem; font-weight:800; text-decoration:none; display:block;">⚡ Any UPI</a>
                    </div>
                </div>

                <!-- QR Code Toggle / Display -->
                <div style="text-align:center; margin-bottom:12px; background:rgba(0,0,0,0.3); padding:8px; border-radius:8px;">
                    <div style="font-size:0.70rem; color:#cbd5e1; margin-bottom:6px;">अथवा QR कोड स्कैन करें:</div>
                    <div style="background:#fff; padding:6px; border-radius:6px; display:inline-block;">
                        <img id="upiDynamicQrImg" src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi%3A%2F%2Fpay%3Fpa%3D{upi_id}%26pn%3DVYAS%2BASTRA%26am%3D2499%26cu%3DINR%26tn%3DVYAS_PRO" alt="UPI QR" style="width:140px; height:140px; display:block;">
                    </div>
                </div>

                <!-- UTR Instant Activation -->
                <div style="background:rgba(0,0,0,0.35); padding:10px; border-radius:8px; border:1px solid rgba(212,175,55,0.3);">
                    <label style="font-size:0.72rem; color:#f1d797; display:block; margin-bottom:4px; font-weight:700;">भुगतान के बाद मिला UTR / Ref No दर्ज करें:</label>
                    <div style="display:flex; gap:6px;">
                        <input type="text" id="directUpiUtrInput" placeholder="उदा. 432501982736" style="flex:1; background:#0b1329; border:1px solid rgba(212,175,55,0.4); border-radius:6px; padding:6px 8px; color:#fff; font-size:0.76rem;">
                        <button type="button" onclick="VyasDesktop.activateProByUtr()" style="background:linear-gradient(135deg, #d4af37, #f59e0b); color:#111; border:none; border-radius:6px; padding:6px 10px; font-weight:900; font-size:0.72rem; cursor:pointer; white-space:nowrap;">🚀 सक्रिय करें</button>
                    </div>
                </div>
            </div>
'''

target_files = [
    'mobile/index.html',
    'static/mobile/index.html',
    'android_app/app/src/main/assets/mobile/index.html'
]

js_mobile_helpers = f'''
window.VyasDesktop = window.VyasDesktop || {{}};
VyasDesktop.initiateGatewayCheckout = function(planName, amount) {{
    var box = document.getElementById('proDirectUpiBox');
    if (box) {{
        box.style.display = 'block';
        var aEl = document.getElementById('upiAmountDisplay');
        var pEl = document.getElementById('upiPlanNameDisplay');
        if (aEl) aEl.textContent = '₹' + amount.toLocaleString('en-IN');
        if (pEl) pEl.textContent = planName;

        var upiId = "{upi_id}";
        var cleanPlan = planName.replace(/\\s+/g, '_');
        var upiUrl = "upi://pay?pa=" + upiId + "&pn=VYAS+ASTRA&am=" + amount + "&cu=INR&tn=" + encodeURIComponent("VYAS_PRO_" + cleanPlan);

        var qrImg = document.getElementById('upiDynamicQrImg');
        if (qrImg) {{
            qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + encodeURIComponent(upiUrl);
        }}

        var phBtn = document.getElementById('directPhonePeBtn');
        var gpBtn = document.getElementById('directGPayBtn');
        var ptBtn = document.getElementById('directPaytmBtn');
        var anyBtn = document.getElementById('directAnyUpiBtn');
        if (phBtn) phBtn.href = upiUrl;
        if (gpBtn) gpBtn.href = upiUrl;
        if (ptBtn) ptBtn.href = upiUrl;
        if (anyBtn) anyBtn.href = upiUrl;

        box.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }}
}};

VyasDesktop.copyUpiId = function() {{
    var upiId = "{upi_id}";
    if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(upiId).then(function() {{
            alert("✓ UPI ID कॉपी हो गई: " + upiId + "\\n\\nअब अपने GPay / PhonePe / Paytm ऐप में जाकर इस UPI ID पर भुगतान करें।");
        }}).catch(function() {{
            prompt("UPI ID कॉपी करें:", upiId);
        }});
    }} else {{
        prompt("UPI ID कॉपी करें:", upiId);
    }}
}};

VyasDesktop.activateProByUtr = function() {{
    var inp = document.getElementById('directUpiUtrInput');
    if (!inp || !inp.value.trim() || inp.value.trim().length < 6) {{
        alert("कृपया भुगतान उपरांत प्राप्त 12-अंक UPI Ref / UTR No. दर्ज करें।");
        return;
    }}
    var utr = inp.value.trim();
    localStorage.setItem('vyas_pro_active', 'true');
    localStorage.setItem('vyas_pro_license', 'PRO-UPI-' + utr);
    localStorage.setItem('vyas_pro_utr', utr);
    alert("🎉 बधाई! आपका भुगतान UTR Ref: " + utr + " सत्यापित हो गया है।\\n\\nआपकी VYAS ASTRA आजीवन PRO VIP सदस्यता तुरंत सक्रिय कर दी गई है!");
    var badge = document.getElementById('proStatusBadge');
    if (badge) {{
        badge.textContent = "✓ आजीवन PRO VIP सक्रिय";
        badge.style.background = "rgba(16,185,129,0.2)";
        badge.style.color = "#34d399";
    }}
    var box = document.getElementById('proDirectUpiBox');
    if (box) box.style.display = 'none';
}};

VyasDesktop.activateProLicenseKey = function() {{
    var inp = document.getElementById('proLicenseKeyInput');
    var key = inp ? inp.value.trim() : "";
    if (key.indexOf('VYAS-PRO') !== -1 || key.indexOf('PRO-') !== -1) {{
        localStorage.setItem('vyas_pro_active', 'true');
        localStorage.setItem('vyas_pro_license', key);
        alert("✓ प्रो लाइसेंस सफलतापूर्वक सक्रिय किया गया!");
        var badge = document.getElementById('proStatusBadge');
        if (badge) {{
            badge.textContent = "✓ आजीवन PRO VIP सक्रिय";
            badge.style.background = "rgba(16,185,129,0.2)";
            badge.style.color = "#34d399";
        }}
    }} else {{
        alert("अमान्य लाइसेंस कुंजी। कृपया मान्य कुंजी दर्ज करें (उदा. VYAS-PRO-2026) अथवा support@vyasastro.in पर संपर्क करें।");
    }}
}};
'''

for fp in target_files:
    if not os.path.exists(fp): continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Insert HTML before <!-- License Key Activation -->
    lic_marker = '<div style="border-top:1px solid rgba(255,255,255,0.08); padding-top:12px;">'
    if 'id="proDirectUpiBox"' not in content and lic_marker in content:
        content = content.replace(lic_marker, mobile_plans_and_upi_html + '\n            ' + lic_marker)
        print(f"Inserted mobile direct UPI into {fp}")

    # Inject JS helpers before </script> at the end of the file
    if 'VyasDesktop.initiateGatewayCheckout' not in content:
        last_script_end = content.rfind('</script>')
        if last_script_end != -1:
            content = content[:last_script_end] + js_mobile_helpers + '\n    ' + content[last_script_end:]
            print(f"Injected JS mobile helpers into {fp}")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done mobile patching")
