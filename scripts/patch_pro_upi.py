with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

upi_box_html = """
            <!-- INSTANT DYNAMIC UPI PAYMENT BOX (Web & Mobile Checkout) -->
            <div id="proUpiCheckoutBox" style="background:linear-gradient(135deg, rgba(16,185,129,0.12) 0%, rgba(6,78,59,0.2) 100%); border:1.5px solid #10b981; border-radius:12px; padding:16px; margin-bottom:20px; display:none;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:1.3rem;">⚡</span>
                        <b id="upiCheckoutTitle" style="color:#34d399; font-size:1rem;">तत्काल UPI भुगतान (Instant Checkout)</b>
                    </div>
                    <span id="upiAmountBadge" style="background:#10b981; color:#000; font-weight:900; padding:2px 10px; border-radius:12px; font-size:0.82rem;">₹999</span>
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:16px; align-items:center; justify-content:center;">
                    <div style="text-align:center; background:#fff; padding:10px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.3);">
                        <img id="dynamicUpiQrImg" src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=upi%3A%2F%2Fpay%3Fpa%3D9414121172%40upi%26pn%3DVyasAstra%26am%3D999%26cu%3DINR%26tn%3DVyasAstraPro" alt="UPI QR Code" style="width:140px; height:140px; display:block;">
                        <small style="color:#000; font-weight:800; font-size:0.7rem; display:block; margin-top:4px;">GPay • PhonePe • Paytm</small>
                    </div>
                    <div style="flex:1; min-width:220px; font-size:0.82rem; line-height:1.6; color:#cbd5e1;">
                        <div style="margin-bottom:6px;"><b>UPI ID:</b> <code style="background:rgba(0,0,0,0.4); color:#38bdf8; padding:3px 8px; border-radius:4px; font-weight:800;">9414121172@upi</code></div>
                        <div style="margin-bottom:10px; color:#94a3b8; font-size:0.75rem;">मोबाइल पर सीधे भुगतान हेतु नीचे दिए गए बटन पर टैप करें अथवा किसी भी UPI ऐप से QR स्कैन करें।</div>
                        <div style="display:flex; gap:8px; flex-wrap:wrap;">
                            <a id="mobileUpiPayBtn" href="upi://pay?pa=9414121172@upi&pn=VyasAstra&am=999&cu=INR&tn=VyasAstraPro" class="header-btn" style="flex:1; text-align:center; padding:8px 12px; background:linear-gradient(135deg, #10b981, #059669); color:#fff; font-weight:800; text-decoration:none; border-radius:6px; font-size:0.8rem; box-shadow:0 4px 12px rgba(16,185,129,0.35);">
                                📲 मोबाइल से सीधा भुगतान करें
                            </a>
                        </div>
                    </div>
                </div>
            </div>
"""

old_plan_section = """            <!-- Subscription Pricing Plans -->
            <div style="margin-bottom:22px;">"""

new_plan_section = upi_box_html + """            <!-- Subscription Pricing Plans -->
            <div style="margin-bottom:22px;">"""

if old_plan_section in code and 'id="proUpiCheckoutBox"' not in code:
    code = code.replace(old_plan_section, new_plan_section)
    
    # Add JS helper selectPlanAndShowUpi
    js_helper = """
            selectPlanAndShowUpi: function(planName, amount) {
                var box = document.getElementById('proUpiCheckoutBox');
                if (!box) return;
                box.style.display = 'block';
                var title = document.getElementById('upiCheckoutTitle');
                var badge = document.getElementById('upiAmountBadge');
                var img = document.getElementById('dynamicUpiQrImg');
                var btn = document.getElementById('mobileUpiPayBtn');
                if (title) title.textContent = 'तत्काल ' + planName + ' UPI भुगतान';
                if (badge) badge.textContent = '₹' + amount;
                var upiUri = 'upi://pay?pa=9414121172@upi&pn=VyasAstra&am=' + amount + '&cu=INR&tn=VyasAstra_' + encodeURIComponent(planName);
                if (btn) btn.href = upiUri;
                if (img) img.src = 'https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=' + encodeURIComponent(upiUri);
                box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            },
"""
    # Insert helper inside VyasDesktop
    target_pos = 'openProModal() {'
    code = code.replace(target_pos, js_helper + '\n            ' + target_pos)

    # Change plan buttons to call selectPlanAndShowUpi
    code = code.replace(
        '<a href="https://wa.me/919414121172?text=नमस्ते,%20मुझे%20VYAS%20ASTRA%20वार्षिक%20PRO%20प्लान%20(₹999)%20लेना%20है।"',
        '<button type="button" onclick="VyasDesktop.selectPlanAndShowUpi(\'वार्षिक प्रो\', 999)"'
    )
    code = code.replace(
        '<a href="https://wa.me/919414121172?text=नमस्ते,%20मुझे%20VYAS%20ASTRA%20आजीवन%20VIP%20सदस्यता%20(₹2499)%20सक्रिय%20करनी%20है।"',
        '<button type="button" onclick="VyasDesktop.selectPlanAndShowUpi(\'आजीवन VIP\', 2499)"'
    )
    code = code.replace(
        '<a href="https://wa.me/919414121172?text=नमस्ते,%20मुझे%20VYAS%20ASTRA%20ज्योतिषी%20प्रो%20प्लान%20(₹4999)%20चाहिए।"',
        '<button type="button" onclick="VyasDesktop.selectPlanAndShowUpi(\'ज्योतिषी प्रो\', 4999)"'
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("SUCCESS: Injected dynamic UPI QR & instant mobile checkout into index.html!")
else:
    print("Warning: old_plan_section not found or already injected")
