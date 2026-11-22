import re

def enrich_ashtakavarga():
    fpath = 'ashtakavarga/index.html'
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Add dedicated Prastara Full Section right before </main>
    prastara_full_section = """
        <!-- FULL-WIDTH DEDICATED PRASTARASHTAKAVARGA SECTION -->
        <div class="card" style="margin-top:24px; border:1px solid rgba(212,175,55,0.4); background:linear-gradient(180deg, rgba(12,19,36,0.95) 0%, rgba(5,8,17,0.98) 100%);">
            <div class="card-header" style="border-bottom:1px solid rgba(212,175,55,0.25); padding-bottom:12px;">
                <div class="card-title" style="font-size:1.15rem; color:var(--gold);">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 1 0 10 10"/><polygon points="12 6 12 12 16 14"/></svg>
                    <span>✦ संपूर्ण प्रस्ताराष्टकवर्ग ८ कक्षा चक्र, गोचर वेध एवं शोध्य पिण्ड फलित</span>
                </div>
                <span style="font-size:0.78rem; background:rgba(212,175,55,0.18); border:1px solid var(--gold); color:var(--gold-light); padding:3px 10px; border-radius:12px; font-weight:800;">बृहत्पाराशर प्रामाणिक पद्धति</span>
            </div>

            <div style="font-size:0.88rem; line-height:1.7; color:var(--text-secondary); margin-top:14px; margin-bottom:16px;">
                <b>प्रस्ताराष्टकवर्ग का मूल शास्त्रीय रहस्य:</b> महर्षि पराशर अनुसार राशि के ३० अंशों को ३° ४५' के ८ समान भागों (कक्षाओं) में विभक्त किया जाता है। प्रत्येक राशि में क्रमशः <b>शनि (१), गुरु (२), मंगल (३), सूर्य (४), शुक्र (५), बुध (६), चन्द्र (७) एवं लग्न (८)</b> की कक्षा होती है। जिस कक्षा को १ शुभ बिन्दु प्राप्त होता है, गोचरस्थ ग्रह उस ३° ४५' में भ्रमण करते समय अपने कारकत्वों का सर्वोच्च अनुकूल फल प्रदान करता है; शून्य कक्षा में संयम अपेक्षित होता है।
            </div>

            <!-- 8 Kakshya Grid Cards -->
            <div id="fullPrastaraGridWrap" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:12px; margin-bottom:20px;">
                <!-- Populated dynamically -->
            </div>

            <!-- 7 Planets Prastara Capacity Table -->
            <div style="margin-top:20px; border-top:1px solid rgba(255,255,255,0.08); padding-top:16px;">
                <div style="font-size:1rem; font-weight:800; color:#38bdf8; margin-bottom:10px; display:flex; align-items:center; gap:8px;">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/></svg>
                    <span>सप्त-ग्रह प्रस्ताराष्टकवर्ग क्षमता एवं शुभाशुभ फल विधान (Total 337 Bindus)</span>
                </div>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:10px;" id="planetPrastaraGridWrap">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <!-- Shodhya Pinda & Shodhana Principles -->
            <div style="margin-top:20px; border-top:1px solid rgba(255,255,255,0.08); padding-top:16px;">
                <div style="font-size:1rem; font-weight:800; color:#c084fc; margin-bottom:10px; display:flex; align-items:center; gap:8px;">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 22 22 22 12 2"/></svg>
                    <span>शोध्याष्टकवर्ग, त्रिकोण शोधन, एकाधिपत्य शोधन एवं शोध्य पिण्ड रहस्य</span>
                </div>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:10px;" id="shodhanaGridWrap">
                    <!-- Populated dynamically -->
                </div>
            </div>
        </div>
"""

    if 'id="fullPrastaraGridWrap"' not in html:
        target = '</main>'
        html = html.replace(target, prastara_full_section + '\n    ' + target)

    # Now update renderAll in ashtakavarga/index.html to populate fullPrastaraGridWrap, planetPrastaraGridWrap, shodhanaGridWrap
    render_prastara_code = """
            // 7. Render Comprehensive Full-Width Prastarashtakavarga
            if (window.VyasAshtakavargaEngine && window.VyasAshtakavargaEngine.generateComprehensivePrastaraPhalkathan) {
                var pData = window.VyasAshtakavargaEngine.generateComprehensivePrastaraPhalkathan(chart);
                if (pData) {
                    var gridWrap = document.getElementById('fullPrastaraGridWrap');
                    if (gridWrap && pData.kakshyas) {
                        var gHtml = '';
                        pData.kakshyas.forEach(function(k) {
                            gHtml += '<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:12px; border-left:3px solid var(--gold);">' +
                                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">' +
                                '<b style="color:#fbbf24; font-size:0.92rem;">कक्षा ' + (k.idx + 1) + ': ' + k.lord + ' (' + k.range + ')</b>' +
                                '<span style="font-size:0.75rem; background:rgba(212,175,55,0.15); color:var(--gold-light); padding:2px 8px; border-radius:10px;">३° ४५\'</span>' +
                                '</div>' +
                                '<div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:4px;"><b>अधिपति कारकत्व:</b> ' + k.kark + '</div>' +
                                '<div style="font-size:0.83rem; line-height:1.6; color:var(--text-secondary);">' + k.rule + '</div>' +
                                '</div>';
                        });
                        gridWrap.innerHTML = gHtml;
                    }

                    var pGridWrap = document.getElementById('planetPrastaraGridWrap');
                    if (pGridWrap && pData.planetPrastara) {
                        var plHtml = '';
                        pData.planetPrastara.forEach(function(pl) {
                            plHtml += '<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:10px 12px; border-left:3px solid #38bdf8;">' +
                                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">' +
                                '<b style="color:#38bdf8; font-size:0.92rem;">' + pl.name + ' प्रस्ताराष्टकवर्ग</b>' +
                                '<span style="font-size:0.78rem; font-weight:800; color:var(--emerald);">' + pl.total + ' बिन्दु</span>' +
                                '</div>' +
                                '<div style="font-size:0.76rem; color:var(--text-muted); margin-bottom:3px;"><b>औसत:</b> ' + pl.avg + ' प्रति राशि • ' + pl.significance + '</div>' +
                                '<div style="font-size:0.82rem; line-height:1.55; color:var(--text-secondary);">' + pl.eval + '</div>' +
                                '</div>';
                        });
                        pGridWrap.innerHTML = plHtml;
                    }

                    var sGridWrap = document.getElementById('shodhanaGridWrap');
                    if (sGridWrap && pData.shodhanaRules) {
                        var shHtml = '';
                        pData.shodhanaRules.forEach(function(sr) {
                            shHtml += '<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:10px 12px; border-left:3px solid #c084fc;">' +
                                '<div style="color:#c084fc; font-weight:800; font-size:0.88rem; margin-bottom:4px;">✦ ' + sr.title + '</div>' +
                                '<div style="font-size:0.82rem; line-height:1.6; color:var(--text-secondary);">' + sr.desc + '</div>' +
                                '</div>';
                        });
                        sGridWrap.innerHTML = shHtml;
                    }
                }
            }
"""

    if 'pData.kakshyas' not in html:
        target = 'dWrap.innerHTML = kHtml;'
        html = html.replace(target, target + '\n' + render_prastara_code)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated ashtakavarga/index.html with full-width Prastarashtakavarga section and logic")

if __name__ == '__main__':
    enrich_ashtakavarga()

