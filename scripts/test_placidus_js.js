function computeSphericalPlacidusCusps(ascNir, latitude, ayan, jd) {
    var ascTrop = (ascNir + ayan) % 360.0;
    if (ascTrop < 0) ascTrop += 360.0;
    var T = (jd - 2451545.0) / 36525.0;
    var epsDeg = 23.43929111 - (46.8150 * T) / 3600.0;
    var eps = epsDeg * Math.PI / 180.0;
    var phi = Math.max(Math.min(latitude, 66.0), -66.0) * Math.PI / 180.0;
    var lam1 = ascTrop * Math.PI / 180.0;

    var alpha1 = (Math.atan2(Math.sin(lam1) * Math.cos(eps), Math.cos(lam1)) * 180.0 / Math.PI + 360.0) % 360.0;
    var sinDecl1 = Math.sin(eps) * Math.sin(lam1);
    var tanDecl1 = sinDecl1 / Math.sqrt(Math.max(1e-12, 1.0 - sinDecl1 * sinDecl1));
    var ad1 = Math.asin(Math.max(-0.999999, Math.min(0.999999, Math.tan(phi) * tanDecl1))) * 180.0 / Math.PI;
    var oa1 = (alpha1 - ad1 + 360.0) % 360.0;
    var ramcDeg = (oa1 - 90.0 + 360.0) % 360.0;
    var ramc = ramcDeg * Math.PI / 180.0;
    var mcDeg = (Math.atan2(Math.sin(ramc), Math.cos(ramc) * Math.cos(eps)) * 180.0 / Math.PI + 360.0) % 360.0;

    function placidusIter(offsetDeg, factor, diurnal) {
        var ra0 = (ramcDeg + offsetDeg) % 360.0;
        var raCurr = ra0;
        for (var iter = 0; iter < 35; iter++) {
            var raRad = raCurr * Math.PI / 180.0;
            var lam = Math.atan2(Math.sin(raRad), Math.cos(raRad) * Math.cos(eps));
            var sinDecl = Math.sin(eps) * Math.sin(lam);
            var tanDecl = sinDecl / Math.sqrt(Math.max(1e-12, 1.0 - sinDecl * sinDecl));
            var arg = Math.max(-0.999999, Math.min(0.999999, Math.tan(phi) * tanDecl));
            var adDeg = Math.asin(arg) * 180.0 / Math.PI;
            var raNext = diurnal ? ((ra0 + factor * adDeg) % 360.0 + 360.0) % 360.0 : ((ra0 - factor * adDeg) % 360.0 + 360.0) % 360.0;
            if (Math.abs((raNext - raCurr + 180.0) % 360.0 - 180.0) < 1e-7) {
                raCurr = raNext;
                break;
            }
            raCurr = raNext;
        }
        var raFin = raCurr * Math.PI / 180.0;
        return (Math.atan2(Math.sin(raFin), Math.cos(raFin) * Math.cos(eps)) * 180.0 / Math.PI + 360.0) % 360.0;
    }

    var c11 = placidusIter(30.0, 1.0 / 3.0, true);
    var c12 = placidusIter(60.0, 2.0 / 3.0, true);
    var c2 = placidusIter(120.0, 2.0 / 3.0, false);
    var c3 = placidusIter(150.0, 1.0 / 3.0, false);

    var trop = {
        1: ascTrop, 2: c2, 3: c3, 4: (mcDeg + 180.0) % 360.0,
        5: (c11 + 180.0) % 360.0, 6: (c12 + 180.0) % 360.0,
        7: (ascTrop + 180.0) % 360.0, 8: (c2 + 180.0) % 360.0, 9: (c3 + 180.0) % 360.0,
        10: mcDeg, 11: c11, 12: c12
    };

    var res = {};
    for (var h = 1; h <= 12; h++) {
        res[h] = (trop[h] - ayan + 360.0) % 360.0;
    }
    return res;
}

var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
var cusps = computeSphericalPlacidusCusps(23.47, 25.77, 23.64, 2461370.0);
console.log("=== VERIFYING PLACIDUS DEGREES ===");
for (var h = 1; h <= 12; h++) {
    var lon = cusps[h];
    var sIdx = Math.floor(lon / 30.0) % 12;
    var degIn = lon % 30.0;
    var d = Math.floor(degIn);
    var m = Math.floor((degIn - d) * 60);
    var s = Math.round(((degIn - d) * 60 - m) * 60);
    console.log("Cusp " + h + ": " + SIGNS_HI[sIdx] + " " + d + "°" + m + "'" + s + "\" (" + lon.toFixed(4) + "°)");
}
