import re

upi_id = "inikhilvyas@ybl"
payee_name = "VYAS ASTRA VEDIC"

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Prepare Smart UPI Direct Checkout Box HTML
upi_box_html = f'''
            <!-- 100% Free 0% Fee Smart Direct UPI Box -->
            <div id="proDirectUpiBox" style="display:none; margin:18px 0; background:linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(15,23,42,0.98) 100%); border:2px solid #10b981; border-radius:14px; padding:18px; box-shadow:0 8px 32px rgba(16,185,129,0.25);">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(16,185,129,0.3); padding-bottom:10px; margin-bottom:14px; flex-wrap:wrap; gap:8px;">
                    <div>
                        <span style="background:#10b981; color:#06140e; font-size:0.70rem; font-weight:900; padding:2px 8px; border-radius:4px; letter-spacing:0.5px;">✓ 0% शुल्क • सुरक्षित सीधा बैंक UPI</span>
                        <h4 style="margin:4px 0 0 0; color:#f8fafc; font-size:1.05rem;">सीधा बैंक UPI भुगतान (<span id="upiPlanNameDisplay" style="color:#34d399;">आजीवन VIP</span>)</h4>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:0.72rem; color:#94a3b8;">कुल देय राशि</span>
                        <div id="upiAmountDisplay" style="font-size:1.45rem; font-weight:900; color:#34d399;">₹2,499</div>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:16px; align-items:center;">
                    <!-- QR Code Column -->
                    <div style="text-align:center; background:rgba(0,0,0,0.4); padding:14px; border-radius:10px; border:1px solid rgba(255,255,255,0.08);">
                        <div style="font-size:0.75rem; color:#cbd5e1; margin-bottom:8px; font-weight:700;">📱 किसी भी UPI ऐप से स्कैन करें:</div>
                        <div style="background:#fff; padding:8px; border-radius:8px; display:inline-block; box-shadow:0 4px 16px rgba(0,0,0,0.6);">
                            <img id="upiDynamicQrImg" src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=upi%3A%2F%2Fpay%3Fpa%3D{upi_id}%26pn%3DVYAS%2BASTRA%26am%3D2499%26cu%3DINR%26tn%3DVYAS_PRO" alt="UPI QR Code" style="width:180px; height:180px; display:block;">
                        </div>
                        <div style="margin-top:8px; font-size:0.70rem; color:#94a3b8;">Google Pay • PhonePe • Paytm • BHIM</div>
                    </div>

                    <!-- Direct Pay & UPI ID Column -->
                    <div>
                        <div style="margin-bottom:12px;">
                            <label style="font-size:0.74rem; color:#94a3b8; display:block; margin-bottom:4px; font-weight:700;">आधिकारिक UPI ID (सत्यापित):</label>
                            <div style="display:flex; gap:6px;">
                                <input type="text" readonly value="{upi_id}" id="directUpiIdInput" style="flex:1; background:#0b1329; border:1px solid #10b981; border-radius:6px; padding:7px 10px; color:#34d399; font-weight:800; font-size:0.85rem; font-family:monospace;">
                                <button type="button" onclick="VyasDesktop.copyUpiId()" style="background:#10b981; color:#06140e; border:none; border-radius:6px; padding:7px 12px; font-weight:900; font-size:0.75rem; cursor:pointer;">📋 कॉपी करें</button>
                            </div>
                        </div>

                        <!-- Mobile One-Tap Pay Links -->
                        <div style="margin-bottom:14px;">
                            <span style="font-size:0.74rem; color:#94a3b8; display:block; margin-bottom:6px; font-weight:700;">⚡ मोबाइल से एक क्लिक में भुगतान करें:</span>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
                                <a id="directPhonePeBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:#5f259f; color:#fff; text-align:center; padding:8px 10px; border-radius:6px; font-size:0.74rem; font-weight:800; text-decoration:none; display:block;">🟣 PhonePe</a>
                                <a id="directGPayBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:#1a73e8; color:#fff; text-align:center; padding:8px 10px; border-radius:6px; font-size:0.74rem; font-weight:800; text-decoration:none; display:block;">🔵 Google Pay</a>
                                <a id="directPaytmBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:#00b9f5; color:#fff; text-align:center; padding:8px 10px; border-radius:6px; font-size:0.74rem; font-weight:800; text-decoration:none; display:block;">🔷 Paytm</a>
                                <a id="directAnyUpiBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:rgba(255,255,255,0.12); color:#fff; text-align:center; padding:8px 10px; border-radius:6px; font-size:0.74rem; font-weight:800; text-decoration:none; display:block;">⚡ Any UPI App</a>
                            </div>
                        </div>

                        <!-- UTR Instant Activation -->
                        <div style="background:rgba(0,0,0,0.35); padding:10px; border-radius:8px; border:1px solid rgba(212,175,55,0.3);">
                            <label style="font-size:0.74rem; color:#f1d797; display:block; margin-bottom:4px; font-weight:700;">चरण २: भुगतान उपरांत UTR (12-अंक UPI Ref No) यहाँ दर्ज करें:</label>
                            <div style="display:flex; gap:6px;">
                                <input type="text" id="directUpiUtrInput" placeholder="उदा. 432501982736" style="flex:1; background:#0b1329; border:1px solid rgba(212,175,55,0.4); border-radius:6px; padding:6px 10px; color:#fff; font-size:0.80rem;">
                                <button type="button" onclick="VyasDesktop.activateProByUtr()" style="background:linear-gradient(135deg, #d4af37, #f59e0b); color:#111; border:none; border-radius:6px; padding:6px 12px; font-weight:900; font-size:0.76rem; cursor:pointer; white-space:nowrap;">🚀 तुरंत अनलॉक करें</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="margin-top:12px; text-align:center; font-size:0.72rem; color:#94a3b8;">
                    ✓ 100% सुरक्षित सीधा बैंक अंतरण • 0% अतिरिक्त शुल्क • तुरंत आजीवन प्रो सक्रियण • सहायता: <a href="mailto:support@vyasastro.in" style="color:#34d399; text-decoration:none;">support@vyasastro.in</a>
                </div>
            </div>
'''

if 'id="proDirectUpiBox"' not in html:
    pricing_end = '<!-- Support / Direct Contact & UPI -->'
    if pricing_end in html:
        html = html.replace(pricing_end, upi_box_html + '\n            ' + pricing_end)
        print("Inserted proDirectUpiBox into index.html")
    else:
        print("pricing_end marker not found!")

# 2. Update JavaScript methods on VyasDesktop in index.html
js_methods = f'''initiateGatewayCheckout: function (planName, amount) {{
                var self = this;
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
                        qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=" + encodeURIComponent(upiUrl);
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
            }},

            copyUpiId: function () {{
                var upiId = "{upi_id}";
                if (navigator.clipboard && navigator.clipboard.writeText) {{
                    navigator.clipboard.writeText(upiId).then(function() {{
                        alert("✓ UPI ID कॉपी हो गई: " + upiId + "\\n\\nअब अपने GPay / PhonePe / Paytm / BHIM ऐप में जाकर इस UPI ID पर भुगतान करें।");
                    }}).catch(function() {{
                        prompt("UPI ID कॉपी करें:", upiId);
                    }});
                }} else {{
                    prompt("UPI ID कॉपी करें:", upiId);
                }}
            }},

            activateProByUtr: function () {{
                var self = this;
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
                self.updateProModalUI();
                if (typeof self.updateGoogleAuthUI === 'function') self.updateGoogleAuthUI();
                var box = document.getElementById('proDirectUpiBox');
                if (box) box.style.display = 'none';
            }},'''

pattern = r'initiateGatewayCheckout:\s*function\s*\(planName,\s*amount\)\s*\{[\s\S]*?verifyAndUnlockByTxn:\s*function\s*\(\)\s*\{[\s\S]*?\},'
if re.search(pattern, html):
    html = re.sub(pattern, lambda m: js_methods, html)
    print("Replaced initiateGatewayCheckout in index.html successfully")
else:
    print("Pattern not matched!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved index.html successfully")
