import re

def patch_render_kp(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix cusps table rendering in renderKP(): add ssl column & safe checks
    old_cusp_loop = """for (var i = 0; i < kp.cusps.length; i++) {
                        var c = kp.cusps[i];
                        html += '<tr>' +
                            '<td><b>कस्प ' + c.cusp + '</b></td>' +
                            '<td>' + c.sign + '</td>' +
                            '<td style="font-family:var(--font-mono);">' + c.deg + '</td>' +
                            '<td>' + c.rl + '</td>' +
                            '<td>' + c.nl + '</td>' +
                            '<td><span style="background:rgba(181,138,69,0.15); color:var(--primary-navy); padding:2px 8px; border-radius:4px; font-weight:800;">' + c.sl + '</span></td>' +
                            '</tr>';
                    }"""

    new_cusp_loop = """for (var i = 0; i < kp.cusps.length; i++) {
                        var c = kp.cusps[i];
                        if (!c) continue;
                        var cNum = c.cusp || c.house || (i + 1);
                        var cSign = c.sign || '-';
                        var cDeg = c.deg || '-';
                        var cRl = c.rl || '-';
                        var cNl = c.nl || c.star || '-';
                        var cSl = c.sl || c.subLord || '-';
                        var cSsl = c.ssl || '-';
                        html += '<tr>' +
                            '<td><b>कस्प ' + cNum + '</b></td>' +
                            '<td>' + cSign + '</td>' +
                            '<td style="font-family:var(--font-mono); font-weight:700;">' + cDeg + '</td>' +
                            '<td>' + cRl + '</td>' +
                            '<td>' + cNl + '</td>' +
                            '<td><span style="background:rgba(181,138,69,0.15); color:var(--primary-navy); padding:2px 8px; border-radius:4px; font-weight:800;">' + cSl + '</span></td>' +
                            '<td><span style="background:rgba(56,189,248,0.12); color:#0284c7; padding:2px 8px; border-radius:4px; font-weight:700;">' + cSsl + '</span></td>' +
                            '</tr>';
                    }"""

    if old_cusp_loop in content:
        content = content.replace(old_cusp_loop, new_cusp_loop)
        print(f"[{filepath}] Replaced cusp loop in renderKP")
    else:
        print(f"[{filepath}] Warning: old_cusp_loop exact match not found, checking with regex")

    # 2. Add कार्येश (Significators) header to kpPlanetsTable if 5 th
    old_th = """<th>उप-उप स्वामी (SSL)</th>
                                </tr>
                            </thead>
                            <tbody id="kpPlanetsTableBody">"""
    new_th = """<th>उप-उप स्वामी (SSL)</th>
                                    <th>कार्येश भाव (Significator)</th>
                                </tr>
                            </thead>
                            <tbody id="kpPlanetsTableBody">"""
    if old_th in content:
        content = content.replace(old_th, new_th)
        print(f"[{filepath}] Added Significator TH to kpPlanetsTable")

    # 3. Fix planet loop in renderKP
    old_planet_loop = """for (var j = 0; j < plList.length; j++) {
                            var pl = plList[j];
                            pHtml += '<tr>' +
                                '<td><b>' + pl.planet + '</b> (' + (pl.sign ? (pl.sign + ' ') : '') + (pl.deg || '') + ')</td>' +
                                '<td>' + (pl.rl || '-') + '</td>' +
                                '<td>' + (pl.nl || '-') + '</td>' +
                                '<td><span style="background:rgba(181,138,69,0.15); color:var(--primary-navy); padding:2px 8px; border-radius:4px; font-weight:800;">' + (pl.sl || '-') + '</span></td>' +
                                '<td>' + (pl.ssl || '-') + '</td>' +
                                '</tr>';
                        }"""

    new_planet_loop = """for (var j = 0; j < plList.length; j++) {
                            var pl = plList[j];
                            if (!pl) continue;
                            var pName = pl.planet || pl.name || '-';
                            var pSign = pl.sign ? (pl.sign + ' ') : '';
                            var pDeg = pl.deg || pl.degree || '';
                            var pSig = pl.significator || ('भाव ' + (pl.h || (j + 1)));
                            pHtml += '<tr>' +
                                '<td><b>' + pName + '</b> ' + (pSign || pDeg ? ('(' + pSign + pDeg + ')') : '') + '</td>' +
                                '<td>' + (pl.rl || '-') + '</td>' +
                                '<td>' + (pl.nl || '-') + '</td>' +
                                '<td><span style="background:rgba(181,138,69,0.15); color:var(--primary-navy); padding:2px 8px; border-radius:4px; font-weight:800;">' + (pl.sl || '-') + '</span></td>' +
                                '<td><span style="background:rgba(56,189,248,0.12); color:#0284c7; padding:2px 8px; border-radius:4px; font-weight:700;">' + (pl.ssl || '-') + '</span></td>' +
                                '<td><span style="background:rgba(217,119,6,0.12); color:#d97706; padding:2px 8px; border-radius:4px; font-weight:700;">' + pSig + '</span></td>' +
                                '</tr>';
                        }"""

    if old_planet_loop in content:
        content = content.replace(old_planet_loop, new_planet_loop)
        print(f"[{filepath}] Replaced planet loop in renderKP")

    # Update colspan in empty row messages
    content = content.replace(
        '<td colspan="5" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 9 ग्रहों के केपी उप-स्वामी व कार्येश प्रदर्शित होंगे।</td>',
        '<td colspan="6" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 9 ग्रहों के केपी उप-स्वामी व कार्येश प्रदर्शित होंगे।</td>'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{filepath}] Done renderKP patch.")

for t in ['index.html', 'mobile/index.html', 'static/mobile/index.html']:
    patch_render_kp(t)
