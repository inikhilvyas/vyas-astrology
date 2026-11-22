import re

def patch_varshphal():
    fpath = 'varshphal/index.html'
    with open(fpath, 'r', encoding='utf-8') as f:
        code = f.read()

    # Update showEmptyKundliNotice
    old_empty = """        function showEmptyKundliNotice() {
            var bar = document.getElementById('activeProfileBar');
            if (bar) {
                bar.innerHTML = '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; width:100%;">' +
                    '<div><span style="color:#ef4444; font-weight:700;">⚠️ कोई जन्मपत्रिका लोड नहीं है</span><br><span style="font-size:0.8rem; color:#94a3b8;">' + 'वर्षफल' + ' विश्लेषण देखने हेतु कृपया अपनी जन्म कुण्डली बनाएं अथवा वॉल्ट से लोड करें।</span></div>' +
                    '<div style="display:flex; gap:8px;">' +
                    '<a href="/#kundli-calc" class="action-btn" style="text-decoration:none;">+ नई कुण्डली बनाएं</a>' +
                    '<a href="/saved-kundli/" class="action-btn" style="text-decoration:none;">📂 वॉल्ट से लोड करें</a>' +
                    '</div></div>';
            }
        }"""

    new_empty = """        function showEmptyKundliNotice() {
            var bar = document.getElementById('activeProfileBar');
            if (bar) {
                bar.innerHTML = '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; width:100%;">' +
                    '<div><span style="color:#fbbf24; font-weight:800;">⚠️ कोई सक्रिय जन्मपत्रिका लोड नहीं है</span><br><span style="font-size:0.82rem; color:#94a3b8;">ताजिक वर्षफल, मुंथा एवं वर्षेश चक्र देखने हेतु कृपया जन्म कुण्डली चुनें अथवा वॉल्ट से लोड करें।</span></div>' +
                    '<div style="display:flex; gap:8px;">' +
                    '<a href="/#kundli-calc" class="action-btn" style="text-decoration:none; background:linear-gradient(135deg,#f59e0b,#d97706); color:#fff; font-weight:700; padding:8px 14px; border-radius:6px;">+ नई कुण्डली बनाएं</a>' +
                    '<a href="/saved-kundli/" class="action-btn" style="text-decoration:none; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); color:#fde68a; font-weight:700; padding:8px 14px; border-radius:6px;">📂 वॉल्ट से लोड करें</a>' +
                    '</div></div>';
            }
            var cWrap = document.getElementById('varshChartWrap');
            if (cWrap) {
                cWrap.innerHTML = '<div style="text-align:center; padding:50px 20px; color:var(--text-secondary);">' +
                    '<div style="width:60px; height:60px; margin:0 auto 16px; border-radius:50%; background:rgba(245,158,11,0.12); border:1px solid #f59e0b; display:flex; align-items:center; justify-content:center;">' +
                    '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#f59e0b" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="12 2 22 12 12 22 2 12"/></svg>' +
                    '</div>' +
                    '<div style="font-size:1.1rem; font-weight:800; color:#fbbf24; margin-bottom:8px;">वर्ष प्रवेश चक्र (Solar Return Chart) प्रतीक्षारत</div>' +
                    '<div style="font-size:0.86rem; color:var(--text-muted); max-width:340px; margin:0 auto 16px; line-height:1.6;">कुण्डली लोड होने के उपरांत इस वर्ष का सटीक वर्ष प्रवेश चक्र, मुंथा स्थिति एवं वर्षेश यहाँ प्रदर्शित होंगे।</div>' +
                    '<a href="/saved-kundli/" style="display:inline-flex; align-items:center; gap:6px; padding:8px 16px; background:rgba(245,158,11,0.18); border:1px solid #f59e0b; border-radius:8px; color:#fde68a; font-size:0.85rem; font-weight:700; text-decoration:none;">📂 वॉल्ट से जातक चुनें</a>' +
                    '</div>';
            }
            var pWrap = document.getElementById('varshPhalitWrap');
            if (pWrap) {
                pWrap.innerHTML = '<div style="text-align:center; padding:40px 20px; color:var(--text-muted); font-size:0.9rem; line-height:1.7;">' +
                    '✦ कृपया ऊपर दिए गए विकल्प से कुण्डली चुनें। कुण्डली लोड होते ही <b>मुंथा फल, वर्षेश पंचवर्गीय बल, ताजिक सहम एवं १२-मासिक सौर वर्षफल घटनाक्रम</b> स्वतः सक्रिय हो जाएगा।' +
                    '</div>';
            }
        }"""

    if old_empty in code:
        code = code.replace(old_empty, new_empty)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(code)
        print("Updated varshphal/index.html with graceful empty state")
    else:
        print("Warning: old_empty not found in varshphal/index.html")

def patch_nadi():
    fpath = 'nadi-astrology/index.html'
    with open(fpath, 'r', encoding='utf-8') as f:
        code = f.read()

    new_notice = """        function showEmptyKundliNotice() {
            var bar = document.getElementById('activeProfileBar');
            if (bar) {
                bar.innerHTML = '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; width:100%;">' +
                    '<div><span style="color:#fbbf24; font-weight:800;">⚠️ कोई सक्रिय जन्मपत्रिका लोड नहीं है</span><br><span style="font-size:0.82rem; color:#94a3b8;">भृगु नन्दी नाड़ी ४-दिशा तत्त्व चक्र, जीव-कर्म वेध एवं १२-वर्षीय चक्र देखने हेतु कृपया जन्म कुण्डली चुनें।</span></div>' +
                    '<div style="display:flex; gap:8px;">' +
                    '<a href="/#kundli-calc" class="action-btn" style="text-decoration:none; background:linear-gradient(135deg,#f59e0b,#d97706); color:#fff; font-weight:700; padding:8px 14px; border-radius:6px;">+ नई कुण्डली बनाएं</a>' +
                    '<a href="/saved-kundli/" class="action-btn" style="text-decoration:none; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); color:#fde68a; font-weight:700; padding:8px 14px; border-radius:6px;">📂 वॉल्ट से लोड करें</a>' +
                    '</div></div>';
            }
            var cWrap = document.getElementById('nadiChartWrap');
            if (cWrap) {
                cWrap.innerHTML = '<div style="text-align:center; padding:50px 20px; color:var(--text-secondary);">' +
                    '<div style="width:60px; height:60px; margin:0 auto 16px; border-radius:50%; background:rgba(212,175,55,0.12); border:1px solid var(--gold); display:flex; align-items:center; justify-content:center;">' +
                    '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="var(--gold)" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="2" x2="12" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/></svg>' +
                    '</div>' +
                    '<div style="font-size:1.1rem; font-weight:800; color:var(--gold); margin-bottom:8px;">भृगु नन्दी नाड़ी ४-दिशा चक्र प्रतीक्षारत</div>' +
                    '<div style="font-size:0.86rem; color:var(--text-muted); max-width:340px; margin:0 auto 16px; line-height:1.6;">कुण्डली लोड होने के उपरांत पूर्व (अग्नि), दक्षिण (पृथ्वी), पश्चिम (वायु) एवं उत्तर (जल) दिशाओं का ग्रह संरेखण चक्र यहाँ प्रदर्शित होगा।</div>' +
                    '<a href="/saved-kundli/" style="display:inline-flex; align-items:center; gap:6px; padding:8px 16px; background:rgba(212,175,55,0.18); border:1px solid var(--gold); border-radius:8px; color:var(--gold-light); font-size:0.85rem; font-weight:700; text-decoration:none;">📂 वॉल्ट से जातक चुनें</a>' +
                    '</div>';
            }
            var pWrap = document.getElementById('nadiPhalitWrap');
            if (pWrap) {
                pWrap.innerHTML = '<div style="text-align:center; padding:40px 20px; color:var(--text-muted); font-size:0.9rem; line-height:1.7;">' +
                    '✦ कृपया कुण्डली वॉल्ट से जातक लोड करें अथवा नई कुण्डली बनाएं। लोड होते ही <b>देवगुरु जीवकारक, कर्मकारक शनि, शुक्र कलत्र वेध, वास्तु चिह्न, सहोदर, मानस संतान एवं भृगु बिन्दु महा-वेध</b> स्वतः सक्रिय हो जाएगा।' +
                    '</div>';
            }
        }
"""

    if 'function showEmptyKundliNotice' not in code:
        target = 'function loadAndRenderNadi()'
        code = code.replace(target, new_notice + '\n        ' + target)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(code)
        print("Updated nadi-astrology/index.html with showEmptyKundliNotice")
    else:
        print("nadi-astrology/index.html already has showEmptyKundliNotice")

def patch_ashtakavarga():
    fpath = 'ashtakavarga/index.html'
    with open(fpath, 'r', encoding='utf-8') as f:
        code = f.read()

    # Update showEmptyKundliNotice in ashtakavarga
    old_empty = """        function showEmptyKundliNotice() {
            var bar = document.getElementById('activeProfileBar');
            if (bar) {
                bar.innerHTML = '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; width:100%;">' +
                    '<div><span style="color:#ef4444; font-weight:700;">⚠️ कोई जन्मपत्रिका लोड नहीं है</span><br><span style="font-size:0.8rem; color:#94a3b8;">अष्टकवर्ग एवं प्रस्ताराष्टकवर्ग विश्लेषण देखने हेतु कृपया अपनी जन्म कुण्डली बनाएं अथवा वॉल्ट से लोड करें।</span></div>' +
                    '<div style="display:flex; gap:8px;">' +
                    '<a href="/#kundli-calc" class="action-btn" style="text-decoration:none;">+ नई कुण्डली बनाएं</a>' +
                    '<a href="/saved-kundli/" class="action-btn" style="text-decoration:none;">📂 वॉल्ट से लोड करें</a>' +
                    '</div></div>';
            }
        }"""

    new_empty = """        function showEmptyKundliNotice() {
            var bar = document.getElementById('activeProfileBar');
            if (bar) {
                bar.innerHTML = '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; width:100%;">' +
                    '<div><span style="color:#fbbf24; font-weight:800;">⚠️ कोई सक्रिय जन्मपत्रिका लोड नहीं है</span><br><span style="font-size:0.82rem; color:#94a3b8;">सर्वाष्टकवर्ग ३३७ बिंदु चक्र, भिन्नाष्टकवर्ग एवं प्रस्ताराष्टकवर्ग ८ कक्षा विश्लेषण देखने हेतु कुण्डली चुनें।</span></div>' +
                    '<div style="display:flex; gap:8px;">' +
                    '<a href="/#kundli-calc" class="action-btn" style="text-decoration:none; background:linear-gradient(135deg,#10b981,#059669); color:#fff; font-weight:700; padding:8px 14px; border-radius:6px;">+ नई कुण्डली बनाएं</a>' +
                    '<a href="/saved-kundli/" class="action-btn" style="text-decoration:none; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); color:#fde68a; font-weight:700; padding:8px 14px; border-radius:6px;">📂 वॉल्ट से लोड करें</a>' +
                    '</div></div>';
            }
            var cWrap = document.getElementById('ashtakChartWrap');
            if (cWrap) {
                cWrap.innerHTML = '<div style="text-align:center; padding:50px 20px; color:var(--text-secondary);">' +
                    '<div style="width:60px; height:60px; margin:0 auto 16px; border-radius:50%; background:rgba(16,185,129,0.12); border:1px solid var(--emerald); display:flex; align-items:center; justify-content:center;">' +
                    '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="var(--emerald)" stroke-width="2"><polygon points="12 2 22 12 12 22 2 12"/></svg>' +
                    '</div>' +
                    '<div style="font-size:1.1rem; font-weight:800; color:var(--emerald); margin-bottom:8px;">सर्वाष्टकवर्ग भाव बिंदु चक्र प्रतीक्षारत</div>' +
                    '<div style="font-size:0.86rem; color:var(--text-muted); max-width:340px; margin:0 auto 16px; line-height:1.6;">कुण्डली लोड होने के उपरांत सभी १२ भावों के ३३७ बिन्दुओं का शुद्ध विभाजन चक्र यहाँ प्रदर्शित होगा।</div>' +
                    '<a href="/saved-kundli/" style="display:inline-flex; align-items:center; gap:6px; padding:8px 16px; background:rgba(16,185,129,0.18); border:1px solid var(--emerald); border-radius:8px; color:var(--emerald); font-size:0.85rem; font-weight:700; text-decoration:none;">📂 वॉल्ट से जातक चुनें</a>' +
                    '</div>';
            }
            var pWrap = document.getElementById('ashtakPhalitWrap');
            if (pWrap) {
                pWrap.innerHTML = '<div style="text-align:center; padding:40px 20px; color:var(--text-muted); font-size:0.9rem; line-height:1.7;">' +
                    '✦ कृपया कुण्डली वॉल्ट से जातक लोड करें अथवा नई कुण्डली बनाएं। लोड होते ही <b>आय-व्यय महा-संतुलन, महर्षि पराशर त्रि-खंड जीवन फलादेश, द्वादश भाव विस्तृत फलादेश एवं प्रस्ताराष्टकवर्ग ८ कक्षा वेध</b> स्वतः सक्रिय हो जाएगा।' +
                    '</div>';
            }
        }"""

    if old_empty in code:
        code = code.replace(old_empty, new_empty)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(code)
        print("Updated ashtakavarga/index.html with graceful empty state")
    else:
        print("Warning: old_empty not found in ashtakavarga/index.html")

if __name__ == '__main__':
    patch_varshphal()
    patch_nadi()
    patch_ashtakavarga()

