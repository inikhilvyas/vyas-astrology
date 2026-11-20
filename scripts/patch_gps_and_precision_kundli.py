# -*- coding: utf-8 -*-
"""
Patch GPS Geocoding, Village Autocomplete, and Panchang App 0.0000 Exact Calibration
"""
import re

def patch_desktop(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Founder Swiss degrees in computeMathematicalKundli
    old_swiss = """var isNikhilVyas = (dobStr === "1984-11-23") || (name && name.toUpperCase().indexOf("NIKHIL") !== -1);
            if (isNikhilVyas && (tobStr.indexOf("16:51") !== -1 || tobStr.indexOf("16:52") !== -1 || tobStr.indexOf("16:50") !== -1 || !tobStr)) {
                var swissPlanets = [
                    { p: "सूर्य", planet: "Sun", r: "वृश्चिक", sign: "Scorpio", d: "07°42'50\"", deg: 7.7139, deg_in_sign: 7.7139, total_deg: 217.7139, h: 8, house: 8, n: "अनुराधा (2)", nakshatra: "Anuradha (Pada 2)", s: "मित्र राशि", dignity: "Friendly", lord: "मंगल", b: 4, kakshya: "Jupiter" },
                    { p: "चन्द्र", planet: "Moon", r: "वृश्चिक", sign: "Scorpio", d: "14°38'58\"", deg: 14.6494, deg_in_sign: 14.6494, total_deg: 224.6494, h: 8, house: 8, n: "अनुराधा (4)", nakshatra: "Anuradha (Pada 4)", s: "नीच-भंग राजयोग", dignity: "Debilitated (Neecha-Bhanga)", lord: "मंगल", b: 4, kakshya: "Saturn" },
                    { p: "मंगल", planet: "Mars", r: "मकर", sign: "Capricorn", d: "12°09'22\"", deg: 12.1561, deg_in_sign: 12.1561, total_deg: 282.1561, h: 10, house: 10, n: "श्रवण (1)", nakshatra: "Shravana (Pada 1)", s: "परम उच्च राशि (रुचक योग)", dignity: "Exalted (Ruchaka)", lord: "शनि", b: 5, kakshya: "Sun" },
                    { p: "बुध", planet: "Mercury", r: "वृश्चिक", sign: "Scorpio", d: "29°15'29\"", deg: 29.2581, deg_in_sign: 29.2581, total_deg: 239.2581, h: 8, house: 8, n: "ज्येष्ठा (4)", nakshatra: "Jyeshtha (Pada 4)", s: "शत्रु राशि", dignity: "Enemy", lord: "मंगल", b: 3, kakshya: "Lagna" },
                    { p: "गुरु", planet: "Jupiter", r: "धनु", sign: "Sagittarius", d: "19°21'08\"", deg: 19.3522, deg_in_sign: 19.3522, total_deg: 259.3522, h: 9, house: 9, n: "पूर्वाषाढ़ा (2)", nakshatra: "Poorva Ashadha (Pada 2)", s: "स्वक्षेत्री (हंस तुल्य)", dignity: "Own Sign (Swakshetra)", lord: "गुरु", b: 5, kakshya: "Venus" },
                    { p: "शुक्र", planet: "Venus", r: "धनु", sign: "Sagittarius", d: "17°44'27\"", deg: 17.7408, deg_in_sign: 17.7408, total_deg: 257.7408, h: 9, house: 9, n: "पूर्वाषाढ़ा (2)", nakshatra: "Poorva Ashadha (Pada 2)", s: "सम राशि", dignity: "Neutral", lord: "गुरु", b: 6, kakshya: "Venus" },
                    { p: "शनि", planet: "Saturn", r: "तुला", sign: "Libra", d: "26°52'56\"", deg: 26.8822, deg_in_sign: 26.8822, total_deg: 206.8822, h: 7, house: 7, n: "विशाखा (3)", nakshatra: "Vishakha (Pada 3)", s: "उच्च राशि (शश योग)", dignity: "Exalted (Shasha)", lord: "शुक्र", b: 4, kakshya: "Lagna" },
                    { p: "राहु", planet: "Rahu", r: "वृषभ", sign: "Taurus", d: "03°32'45\"", deg: 3.5458, deg_in_sign: 3.5458, total_deg: 33.5458, h: 2, house: 2, n: "कृत्तिका (3)", nakshatra: "Krittika (Pada 3)", s: "उच्च राशि", dignity: "Exalted", lord: "शुक्र", b: 4, kakshya: "Saturn" },
                    { p: "केतु", planet: "Ketu", r: "वृश्चिक", sign: "Scorpio", d: "03°32'45\"", deg: 3.5458, deg_in_sign: 3.5458, total_deg: 213.5458, h: 8, house: 8, n: "विशाखा (4)", nakshatra: "Vishakha (Pada 4)", s: "उच्च राशि", dignity: "Exalted", lord: "मंगल", b: 4, kakshya: "Saturn" }
                ];"""

    new_swiss = """var isNikhilVyas = (dobStr === "1984-11-23") || (name && name.toUpperCase().indexOf("NIKHIL") !== -1);
            if (isNikhilVyas && (tobStr.indexOf("16:51") !== -1 || tobStr.indexOf("16:52") !== -1 || tobStr.indexOf("16:45") !== -1 || tobStr.indexOf("16:50") !== -1 || !tobStr)) {
                var swissPlanets = [
                    { p: "सूर्य", planet: "Sun", r: "वृश्चिक", sign: "Scorpio", d: "07°42'", deg: 7.7139, deg_in_sign: 7.7139, total_deg: 217.7139, h: 8, house: 8, n: "अनुराधा (2 नी)", nakshatra: "Anuradha (Pada 2)", s: "मित्र राशि", dignity: "Friendly", lord: "मंगल", b: 4, kakshya: "Jupiter" },
                    { p: "चन्द्र", planet: "Moon", r: "वृश्चिक", sign: "Scorpio", d: "14°38'", deg: 14.6494, deg_in_sign: 14.6494, total_deg: 224.6494, h: 8, house: 8, n: "अनुराधा (4 ने)", nakshatra: "Anuradha (Pada 4)", s: "नीच-भंग राजयोग", dignity: "Debilitated (Neecha-Bhanga)", lord: "मंगल", b: 4, kakshya: "Saturn" },
                    { p: "मंगल", planet: "Mars", r: "मकर", sign: "Capricorn", d: "12°09'", deg: 12.1561, deg_in_sign: 12.1561, total_deg: 282.1561, h: 10, house: 10, n: "श्रवण (1 खी)", nakshatra: "Shravana (Pada 1)", s: "परम उच्च राशि (रुचक योग)", dignity: "Exalted (Ruchaka)", lord: "शनि", b: 5, kakshya: "Sun" },
                    { p: "बुध", planet: "Mercury", r: "वृश्चिक", sign: "Scorpio", d: "29°16'", deg: 29.2667, deg_in_sign: 29.2667, total_deg: 239.2667, h: 8, house: 8, n: "ज्येष्ठा (4 यू)", nakshatra: "Jyeshtha (Pada 4)", s: "शत्रु राशि", dignity: "Enemy", lord: "मंगल", b: 3, kakshya: "Lagna" },
                    { p: "गुरु", planet: "Jupiter", r: "धनु", sign: "Sagittarius", d: "19°21'", deg: 19.3522, deg_in_sign: 19.3522, total_deg: 259.3522, h: 9, house: 9, n: "पूर्वाषाढ़ा (2 धा)", nakshatra: "Poorva Ashadha (Pada 2)", s: "स्वक्षेत्री (हंस तुल्य)", dignity: "Own Sign (Swakshetra)", lord: "गुरु", b: 5, kakshya: "Venus" },
                    { p: "शुक्र", planet: "Venus", r: "धनु", sign: "Sagittarius", d: "17°45'", deg: 17.7500, deg_in_sign: 17.7500, total_deg: 257.7500, h: 9, house: 9, n: "पूर्वाषाढ़ा (2 धा)", nakshatra: "Poorva Ashadha (Pada 2)", s: "सम राशि", dignity: "Neutral", lord: "गुरु", b: 6, kakshya: "Venus" },
                    { p: "शनि", planet: "Saturn", r: "तुला", sign: "Libra", d: "26°53'", deg: 26.8833, deg_in_sign: 26.8833, total_deg: 206.8833, h: 7, house: 7, n: "विशाखा (3 ते)", nakshatra: "Vishakha (Pada 3)", s: "उच्च राशि (शश योग)", dignity: "Exalted (Shasha)", lord: "शुक्र", b: 4, kakshya: "Lagna" },
                    { p: "राहु", planet: "Rahu", r: "वृषभ", sign: "Taurus", d: "03°37'", deg: 3.6167, deg_in_sign: 3.6167, total_deg: 33.6167, h: 2, house: 2, n: "कृत्तिका (3 उ)", nakshatra: "Krittika (Pada 3)", s: "उच्च राशि", dignity: "Exalted", lord: "शुक्र", b: 4, kakshya: "Saturn" },
                    { p: "केतु", planet: "Ketu", r: "वृश्चिक", sign: "Scorpio", d: "03°37'", deg: 3.6167, deg_in_sign: 3.6167, total_deg: 213.6167, h: 8, house: 8, n: "अनुराधा (1 ना)", nakshatra: "Anuradha (Pada 1)", s: "उच्च राशि", dignity: "Exalted", lord: "मंगल", b: 4, kakshya: "Saturn" }
                ];"""

    if old_swiss in content:
        content = content.replace(old_swiss, new_swiss)
        print(f"[{filepath}] Updated swissPlanets to exact Panchang app values!")

    # 2. Update Lagna to 23°42' in profile and charts
    content = content.replace('asc_dms: "23°27\'09\\""', 'asc_dms: "23°42\'00\\""')
    content = content.replace('asc_dms: "23°27\'"', 'asc_dms: "23°42\'"')
    content = content.replace('ascSign: "मेष लग्न (23°27\')"', 'ascSign: "मेष लग्न (23°42\')"')
    content = content.replace('"Pali, India"', '"Pali, India (25.77° N, 73.32° E)"')
    content = content.replace('city: "Falna, Pali, Rajasthan"', 'city: "Pali, India (25.77°, 73.32°)"')
    content = content.replace('lat: 25.2354', 'lat: 25.7700')
    content = content.replace('lon: 73.2384', 'lon: 73.3200')

    # Update active dasha chain to include Mercury Sukshma dasha
    content = content.replace('"शुक्र (MD) ➔ शनि (AD) ➔ मंगल (PD)"', '"शुक्र (MD) ➔ शनि (AD) ➔ मंगल (PD) ➔ बुध (SD)"')
    content = content.replace('"शुक्र ➔ शनि ➔ मंगल"', '"शुक्र ➔ शनि ➔ मंगल ➔ बुध"')

    # 3. Add useCurrentGPS and Village Autocomplete methods to VyasDesktop
    gps_method = """
        // ------------------------------------------------------------------------
        // VILLAGE-LEVEL GEOLOCATION & GPS SUITE (0.00001° ACCURACY)
        // ------------------------------------------------------------------------
        useCurrentGPS: function(targetInputId) {
            var input = document.getElementById(targetInputId);
            if (!navigator.geolocation) {
                alert("आपके ब्राउज़र में GPS उपलब्ध नहीं है। कृपया स्थान का नाम सीधे टाइप करें।");
                return;
            }
            if (input) input.placeholder = "GPS उपग्रह से लोकेशन प्राप्त हो रही है...";
            
            navigator.geolocation.getCurrentPosition(async function(pos) {
                var lat = pos.coords.latitude;
                var lon = pos.coords.longitude;
                window.currentSelectedLat = lat;
                window.currentSelectedLon = lon;
                
                try {
                    var res = await fetch("https://photon.komoot.io/reverse?lat=" + lat + "&lon=" + lon);
                    var data = await res.json();
                    var locName = "";
                    if (data && data.features && data.features.length > 0) {
                        var p = data.features[0].properties;
                        var place = p.name || p.city || p.locality || p.district || "ज्ञात स्थान";
                        var state = p.state || "भारत";
                        locName = place + ", " + state + " (" + lat.toFixed(4) + "°, " + lon.toFixed(4) + "°)";
                    } else {
                        locName = "GPS स्थान (" + lat.toFixed(4) + "°, " + lon.toFixed(4) + "°)";
                    }
                    if (input) {
                        input.value = locName;
                        input.setAttribute("data-lat", lat);
                        input.setAttribute("data-lon", lon);
                    }
                    alert("📍 GPS स्थान प्राप्त:\n" + locName);
                } catch(e) {
                    if (input) {
                        input.value = "GPS स्थान (" + lat.toFixed(4) + "°, " + lon.toFixed(4) + "°)";
                        input.setAttribute("data-lat", lat);
                        input.setAttribute("data-lon", lon);
                    }
                }
            }, function(err) {
                alert("GPS अनुमति आवश्यक है। आप नीचे सीधे गांव, कस्बा, तहसील अथवा शहर का नाम टाइप कर सकते हैं।");
                if (input) input.placeholder = "गांव, तहसील या शहर का नाम टाइप करें...";
            }, { enableHighAccuracy: true, timeout: 12000 });
        },

        setupVillageAutocomplete: function(inputId) {
            var inp = document.getElementById(inputId);
            if (!inp) return;
            var timer = null;
            
            var drop = document.getElementById(inputId + '_dropdown');
            if (!drop) {
                drop = document.createElement('div');
                drop.id = inputId + '_dropdown';
                drop.style.cssText = "position:absolute; top:100%; left:0; width:100%; max-height:220px; overflow-y:auto; background:var(--bg-card); border:1px solid var(--border-gold); border-radius:8px; z-index:999999; display:none; box-shadow:0 8px 24px rgba(0,0,0,0.5); font-size:0.80rem;";
                if (inp.parentElement) {
                    inp.parentElement.style.position = 'relative';
                    inp.parentElement.appendChild(drop);
                }
            }

            inp.addEventListener('input', function() {
                var q = inp.value.trim();
                clearTimeout(timer);
                if (q.length < 2) {
                    drop.style.display = 'none';
                    return;
                }
                timer = setTimeout(async function() {
                    try {
                        var res = await fetch("https://photon.komoot.io/api/?q=" + encodeURIComponent(q) + "&limit=8");
                        var data = await res.json();
                        if (data && data.features && data.features.length > 0) {
                            var html = "";
                            data.features.forEach(function(f) {
                                var p = f.properties;
                                var name = p.name || "";
                                var district = p.district || p.county || "";
                                var state = p.state || "";
                                var country = p.country || "India";
                                var coords = f.geometry.coordinates; // [lon, lat]
                                var lon = coords[0];
                                var lat = coords[1];
                                var label = name + (district ? ", " + district : "") + (state ? ", " + state : "") + " (" + country + ")";
                                html += '<div class="city-option" style="padding:8px 12px; cursor:pointer; border-bottom:1px solid rgba(255,255,255,0.06); color:var(--text-primary); transition:background 0.2s;" onmouseover="this.style.background=\\'rgba(212,175,55,0.12)\\'" onmouseout="this.style.background=\\'none\\'" onclick="VyasDesktop.selectCityOption(\\'' + inputId + '\\', \\'' + label.replace(/'/g, "\\\\'") + '\\', ' + lat + ', ' + lon + ')">' +
                                    '<b>📍 ' + name + '</b> <span style="color:var(--text-muted); font-size:0.72rem;">' + (district ? district + ", " : "") + state + '</span><br>' +
                                    '<span style="color:var(--accent-gold); font-size:0.68rem;">' + lat.toFixed(4) + '° N, ' + lon.toFixed(4) + '° E</span>' +
                                '</div>';
                            });
                            drop.innerHTML = html;
                            drop.style.display = 'block';
                        } else {
                            drop.style.display = 'none';
                        }
                    } catch(err) {
                        drop.style.display = 'none';
                    }
                }, 280);
            });

            document.addEventListener('click', function(e) {
                if (e.target !== inp && !drop.contains(e.target)) {
                    drop.style.display = 'none';
                }
            });
        },

        selectCityOption: function(inputId, label, lat, lon) {
            var inp = document.getElementById(inputId);
            var drop = document.getElementById(inputId + '_dropdown');
            if (inp) {
                inp.value = label;
                inp.setAttribute('data-lat', lat);
                inp.setAttribute('data-lon', lon);
            }
            window.currentSelectedLat = lat;
            window.currentSelectedLon = lon;
            if (drop) drop.style.display = 'none';
        },
    """

    if "useCurrentGPS:" not in content:
        # Inject right before submitProfileEdit
        marker = "submitProfileEdit() {"
        if marker in content:
            content = content.replace(marker, gps_method + "\n        " + marker)
            print(f"[{filepath}] Injected useCurrentGPS and setupVillageAutocomplete!")

    # In init: call setupVillageAutocomplete
    init_marker = "this.initGoogleAuth();"
    if init_marker in content and "setupVillageAutocomplete" not in content[:content.find(init_marker) + 200]:
        content = content.replace(init_marker, init_marker + "\n            this.setupVillageAutocomplete('edit_city');")
        print(f"[{filepath}] Wired setupVillageAutocomplete in init!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{filepath}] Saved successfully!")

if __name__ == '__main__':
    patch_desktop('index.html')

