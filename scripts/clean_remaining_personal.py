import os
import re

# Clean index.html
with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('name: "निखिल व्यास (संस्थापक)",', 'name: "जातक",')
text = text.replace('alert("☁️ क्लाउड कुण्डली सिंक स्थिति:\\n\\n• जन्म कुण्डली: निखिल व्यास (सफल)\\n• कुल सुरक्षित चार्ट: 4\\n• सर्वर स्टेटस: 100% ऑनलाइन (AWS/Hostinger)");', 'alert("☁️ क्लाउड कुण्डली सिंक स्थिति: सफल (100% ऑनलाइन)");')
text = text.replace('var age = parseInt(yr) - 1984;', 'var age = parseInt(yr) - (prof.dob ? parseInt(prof.dob.split("-")[0]) : 2000);')
text = text.replace('if (!m) { this.loadAuthenticNikhilProfile(); return; }', 'if (!m) return;')
text = text.replace('document.getElementById(\'edit_name\').value = prof.name || "Nikhil Vyas";', 'document.getElementById(\'edit_name\').value = prof.name || "";')
text = text.replace('document.getElementById(\'edit_dob\').value = prof.dob || "1984-11-23";', 'document.getElementById(\'edit_dob\').value = prof.dob || "";')
text = text.replace('document.getElementById(\'edit_city\').value = prof.city || "Pali, Rajasthan";', 'document.getElementById(\'edit_city\').value = prof.city || "";')
text = text.replace('// Micro-astronomical schedule: 23 Nov 1984 04:51 PM Pali, Saturn balance 2.8718y', '')
text = re.sub(r'var isNikhil = \(gUser && gUser\.name && gUser\.name\.toLowerCase\(\)\.indexOf\(\'nikhil\'\) !== -1\) \|\|\s*\(gUser && gUser\.email && gUser\.email\.toLowerCase\(\)\.indexOf\(\'nikhil\'\) !== -1\);', '', text)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)
print("✓ index.html clean complete")

# Clean mobile/index.html
with open("mobile/index.html", "r", encoding="utf-8") as f:
    m_text = f.read()

m_text = m_text.replace('name: "निखिल व्यास (संस्थापक)",', 'name: "जातक",')
m_text = m_text.replace('document.getElementById(\'m_inp_name\').value = (prof.name && prof.name.indexOf("Nikhil") === -1) ? prof.name : "";', 'document.getElementById(\'m_inp_name\').value = prof.name || "";')
m_text = m_text.replace('document.getElementById(\'m_inp_dob\').value = (prof.name && prof.name.indexOf("Nikhil") === -1) ? (prof.dob || "") : "";', 'document.getElementById(\'m_inp_dob\').value = prof.dob || "";')
m_text = m_text.replace('document.getElementById(\'m_inp_tob\').value = (prof.name && prof.name.indexOf("Nikhil") === -1) ? (prof.tob || "") : "";', 'document.getElementById(\'m_inp_tob\').value = prof.tob || "";')
m_text = m_text.replace('document.getElementById(\'m_inp_city\').value = (prof.name && prof.name.indexOf("Nikhil") === -1) ? (prof.city || "") : "";', 'document.getElementById(\'m_inp_city\').value = prof.city || "";')

with open("mobile/index.html", "w", encoding="utf-8") as f:
    f.write(m_text)
print("✓ mobile/index.html clean complete")

# Copy mobile/index.html to Android APK assets
with open("android_app/app/src/main/assets/mobile/index.html", "w", encoding="utf-8") as f:
    f.write(m_text)
print("✓ Synchronized to android_app/app/src/main/assets/mobile/index.html")

