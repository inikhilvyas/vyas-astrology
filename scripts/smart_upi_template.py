import re

upi_id = "inikhilvyas@ybl"
payee_name = "VYAS ASTRA VEDIC"

# HTML for the Direct 0% Commission Smart UPI Checkout Box
smart_upi_html = f'''
            <!-- 100% Free 0% Fee Smart Direct UPI Box -->
            <div id="proDirectUpiBox" style="display:none; margin:16px 0; background:linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(15,23,42,0.95) 100%); border:2px solid #10b981; border-radius:14px; padding:18px; box-shadow:0 8px 30px rgba(16,185,129,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(16,185,129,0.3); padding-bottom:10px; margin-bottom:14px;">
                    <div>
                        <span style="background:#10b981; color:#06140e; font-size:0.70rem; font-weight:900; padding:2px 8px; border-radius:4px; letter-spacing:0.5px;">0% कमीशन • सुरक्षित सीधा UPI</span>
                        <h4 style="margin:4px 0 0 0; color:#f8fafc; font-size:1.05rem;">सीधा बैंक UPI भुगतान (<span id="upiPlanNameDisplay" style="color:#34d399;">आजीवन VIP</span>)</h4>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:0.75rem; color:#94a3b8;">कुल देय राशि</span>
                        <div id="upiAmountDisplay" style="font-size:1.45rem; font-weight:900; color:#34d399;">₹2,499</div>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:16px; align-items:center;">
                    <!-- QR Code Column -->
                    <div style="text-align:center; background:rgba(0,0,0,0.35); padding:14px; border-radius:10px; border:1px solid rgba(255,255,255,0.08);">
                        <div style="font-size:0.76rem; color:#cbd5e1; margin-bottom:8px; font-weight:700;">📱 किसी भी UPI ऐप से स्कैन करें:</div>
                        <div style="background:#fff; padding:8px; border-radius:8px; display:inline-block; box-shadow:0 4px 15px rgba(0,0,0,0.5);">
                            <img id="upiDynamicQrImg" src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=upi%3A%2F%2Fpay%3Fpa%3D{upi_id}%26pn%3DVYAS%2BASTRA%26am%3D2499%26cu%3DINR%26tn%3DVYAS_PRO" alt="UPI QR Code" style="width:180px; height:180px; display:block;">
                        </div>
                        <div style="margin-top:8px; font-size:0.72rem; color:#94a3b8;">Google Pay • PhonePe • Paytm • BHIM</div>
                    </div>

                    <!-- Direct Pay & UPI ID Column -->
                    <div>
                        <div style="margin-bottom:12px;">
                            <label style="font-size:0.74rem; color:#94a3b8; display:block; margin-bottom:4px;">आधिकारिक UPI ID:</label>
                            <div style="display:flex; gap:6px;">
                                <input type="text" readonly value="{upi_id}" id="directUpiIdInput" style="flex:1; background:#0b1329; border:1px solid #10b981; border-radius:6px; padding:7px 10px; color:#34d399; font-weight:800; font-size:0.85rem; font-family:monospace;">
                                <button type="button" onclick="VyasDesktop.copyUpiId()" style="background:#10b981; color:#06140e; border:none; border-radius:6px; padding:7px 12px; font-weight:900; font-size:0.75rem; cursor:pointer;">📋 कॉपी करें</button>
                            </div>
                        </div>

                        <!-- Mobile One-Tap Pay Links -->
                        <div style="margin-bottom:14px;">
                            <span style="font-size:0.74rem; color:#94a3b8; display:block; margin-bottom:6px; font-weight:700;">⚡ मोबाइल से एक क्लिक में भुगतान करें:</span>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
                                <a id="directPhonePeBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:#5f259f; color:#fff; text-align:center; padding:7px 10px; border-radius:6px; font-size:0.74rem; font-weight:800; text-decoration:none; display:block;">🟣 PhonePe</a>
                                <a id="directGPayBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:#1a73e8; color:#fff; text-align:center; padding:7px 10px; border-radius:6px; font-size:0.74rem; font-weight:800; text-decoration:none; display:block;">🔵 Google Pay</a>
                                <a id="directPaytmBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:#00b9f5; color:#fff; text-align:center; padding:7px 10px; border-radius:6px; font-size:0.74rem; font-weight:800; text-decoration:none; display:block;">🔷 Paytm</a>
                                <a id="directAnyUpiBtn" href="upi://pay?pa={upi_id}&pn=VYAS+ASTRA&am=2499&cu=INR&tn=VYAS_PRO_VIP" style="background:rgba(255,255,255,0.12); color:#fff; text-align:center; padding:7px 10px; border-radius:6px; font-size:0.74rem; font-weight:800; text-decoration:none; display:block;">⚡ Any UPI App</a>
                            </div>
                        </div>

                        <!-- UTR Instant Activation -->
                        <div style="background:rgba(0,0,0,0.3); padding:10px; border-radius:8px; border:1px solid rgba(212,175,55,0.3);">
                            <label style="font-size:0.74rem; color:#f1d797; display:block; margin-bottom:4px; font-weight:700;">चरण २: भुगतान उपरांत UTR / Ref No दर्ज कर तुरंत प्रो अनलॉक करें:</label>
                            <div style="display:flex; gap:6px;">
                                <input type="text" id="directUpiUtrInput" placeholder="उदा. 432501982736" style="flex:1; background:#0b1329; border:1px solid rgba(212,175,55,0.4); border-radius:6px; padding:6px 10px; color:#fff; font-size:0.80rem;">
                                <button type="button" onclick="VyasDesktop.activateProByUtr()" style="background:linear-gradient(135deg, #d4af37, #f59e0b); color:#111; border:none; border-radius:6px; padding:6px 12px; font-weight:900; font-size:0.76rem; cursor:pointer; white-space:nowrap;">🚀 अनलॉक करें</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="margin-top:12px; text-align:center; font-size:0.72rem; color:#94a3b8;">
                    ✓ 100% सुरक्षित • 0% अतिरिक्त शुल्क • तुरंत सक्रियण • सहायता: <a href="mailto:support@vyasastro.in" style="color:#34d399; text-decoration:none;">support@vyasastro.in</a>
                </div>
            </div>
'''

print("Length of HTML:", len(smart_upi_html))
