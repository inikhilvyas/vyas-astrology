# -*- coding: utf-8 -*-
"""
Patch mobile/index.html with GPS and Precision Values
"""
import re

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update degrees in mobile
content = content.replace('asc_dms: "23°27\'09\\""', 'asc_dms: "23°42\'00\\""')
content = content.replace('asc_dms: "23°27\'"', 'asc_dms: "23°42\'"')
content = content.replace('ascSign: "मेष लग्न (23°27\')"', 'ascSign: "मेष लग्न (23°42\')"')
content = content.replace('city: "Falna, Pali, Rajasthan"', 'city: "Pali, India (25.77°, 73.32°)"')
content = content.replace('lat: 25.2354', 'lat: 25.7700')
content = content.replace('lon: 73.2384', 'lon: 73.3200')

# Update Dasha
content = content.replace('"शुक्र (MD) ➔ शनि (AD) ➔ मंगल (PD)"', '"शुक्र (MD) ➔ शनि (AD) ➔ मंगल (PD) ➔ बुध (SD)"')
content = content.replace('"शुक्र ➔ शनि ➔ मंगल"', '"शुक्र ➔ शनि ➔ मंगल ➔ बुध"')

# Add useCurrentGPS in mobile
gps_code = """
    window.useCurrentMobileGPS = function(targetInputId) {
        var input = document.getElementById(targetInputId);
        if (!navigator.geolocation) {
            alert("आपके मोबाइल में GPS उपलब्ध नहीं है।");
            return;
        }
        if (input) input.placeholder = "GPS उपग्रह से लोकेशन प्राप्त हो रही है...";
        navigator.geolocation.getCurrentPosition(async function(pos) {
            var lat = pos.coords.latitude;
            var lon = pos.coords.longitude;
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
            alert("GPS अनुमति आवश्यक है।");
        }, { enableHighAccuracy: true, timeout: 12000 });
    };
"""

if "window.useCurrentMobileGPS" not in content:
    content = content.replace("</script>", gps_code + "\n</script>", 1)
    print("Injected window.useCurrentMobileGPS in mobile/index.html")

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated mobile/index.html successfully!")

