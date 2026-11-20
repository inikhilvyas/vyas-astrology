with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_ip = html.find('inspectPlanet: function(planetName) {')
pos_end = html.find('openProManager', pos_ip)
if pos_end == -1:
    pos_end = html.find('toggleTheme:', pos_ip)
if pos_end == -1:
    pos_end = html.find('renderPlanetTable:', pos_ip)

print("inspectPlanet pos:", pos_ip, "pos_end:", pos_end)

# Let's inspect what is right after inspectPlanet function
pos_close = html.find('modal.classList.add(\'active\');', pos_ip)
pos_close = html.find('},', pos_close) + 2
print("inspectPlanet close pos:", pos_close)
print(html[pos_ip:pos_close])

dynamic_inspect_planet = '''inspectPlanet: function(planetName) {
            var modal = document.getElementById('modalPlanetInspector');
            var body = document.getElementById('piModalBody');
            var title = document.getElementById('piModalTitle');
            if (!modal || !body) return;

            var cleanName = planetName.replace(/\\(R\\)|\\(व\\)/g, '').trim();
            if (title) title.innerHTML = "✦ ग्रह इन्स्पेक्टर: <b>" + cleanName + "</b>";

            // Extract dynamically from active chart
            var plInfo = null;
            if (this.activeChartData && Array.isArray(this.activeChartData.planet_table)) {
                for (var i = 0; i < this.activeChartData.planet_table.length; i++) {
                    var pl = this.activeChartData.planet_table[i];
                    var pName = (pl.p || pl.planet || "").toLowerCase();
                    var cLower = cleanName.toLowerCase();
                    if (pName.indexOf(cLower) !== -1 || 
                        (cLower === 'mars' && pName.indexOf('मंगल') !== -1) ||
                        (cLower === 'sun' && pName.indexOf('सूर्य') !== -1) ||
                        (cLower === 'moon' && pName.indexOf('चन्द्र') !== -1) ||
                        (cLower === 'jupiter' && (pName.indexOf('गुरु') !== -1 || pName.indexOf('बृहस्पति') !== -1)) ||
                        (cLower === 'venus' && pName.indexOf('शुक्र') !== -1) ||
                        (cLower === 'saturn' && pName.indexOf('शनि') !== -1) ||
                        (cLower === 'mercury' && pName.indexOf('बुध') !== -1) ||
                        (cLower === 'rahu' && pName.indexOf('राहु') !== -1) ||
                        (cLower === 'ketu' && pName.indexOf('केतु') !== -1)) {
                        plInfo = pl;
                        break;
                    }
                }
            }

            var deg = plInfo ? (plInfo.d || plInfo.deg || "00°00'00\\\"") : "अज्ञात";
            var rashi = plInfo ? (plInfo.r || plInfo.rashi || "अज्ञात") : "अज्ञात";
            var house = plInfo ? (plInfo.h ? plInfo.h + " भाव" : "अज्ञात भाव") : "अज्ञात";
            var nak = plInfo ? (plInfo.n || plInfo.nakshatra || "अज्ञात") : "अज्ञात";
            var status = plInfo ? (plInfo.s || plInfo.dignity || "सम") : "सामान्य";
            var drishti = (cleanName === 'Mars' || cleanName.indexOf('मंगल') !== -1) ? "4th, 7th, 8th भाव दृष्टि" :
                          (cleanName === 'Saturn' || cleanName.indexOf('शनि') !== -1) ? "3rd, 7th, 10th भाव दृष्टि" :
                          (cleanName === 'Jupiter' || cleanName.indexOf('गुरु') !== -1) ? "5th, 7th, 9th भाव दृष्टि" : "7th पूर्ण दृष्टि";

            body.innerHTML = '<div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:0.80rem;">' +
                '<div style="background:var(--bg-card); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">' +
                    '<span style="color:var(--text-muted); font-size:0.70rem;">स्पष्ट खगोलीय अंश</span><br>' +
                    '<b style="font-family:var(--font-mono); color:var(--accent-gold); font-size:0.95rem;">' + deg + '</b>' +
                '</div>' +
                '<div style="background:var(--bg-card); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">' +
                    '<span style="color:var(--text-muted); font-size:0.70rem;">राशि एवं भाव स्थिति</span><br>' +
                    '<b style="color:var(--text-primary);">' + rashi + ' • ' + house + '</b>' +
                '</div>' +
                '<div style="background:var(--bg-card); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">' +
                    '<span style="color:var(--text-muted); font-size:0.70rem;">नक्षत्र एवं चरण</span><br>' +
                    '<b style="color:var(--text-primary);">' + nak + '</b>' +
                '</div>' +
                '<div style="background:var(--bg-card); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">' +
                    '<span style="color:var(--text-muted); font-size:0.70rem;">अवस्था / गरिमा</span><br>' +
                    '<b style="color:var(--accent-gold);">' + status + '</b>' +
                '</div>' +
            '</div>' +
            '<div style="margin-top:12px; background:rgba(212,175,55,0.06); border:1px solid rgba(212,175,55,0.2); padding:10px; border-radius:8px; font-size:0.78rem; line-height:1.5;">' +
                '<b style="color:#d4af37;">शास्त्रीय दृष्टि प्रभाव:</b> ' + drishti + '<br>' +
                '<span style="color:var(--text-secondary);">कुण्डली के अनुसार यह ग्रह ' + house + ' में ' + rashi + ' राशि पर संचार कर रहे हैं।</span>' +
            '</div>';

            modal.classList.add('active');
            modal.style.display = 'flex';
        },'''

html = html[:pos_ip] + dynamic_inspect_planet + html[pos_close:]
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✓ Patched inspectPlanet to be 100% dynamic from active chart")

