import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

tabs = re.findall(r'id=["\']view-([^"\']+)["\']', text)
print('Website Views/Tabs:', tabs)

# Look for KP and Horary tabs
print('KP in website:', 'kp' in text.lower())
print('Horary in website:', 'horary' in text.lower())

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    mtext = f.read()
mtabs = re.findall(r'id=["\']view-([^"\']+)["\']', mtext)
print('Mobile Views/Tabs:', mtabs)
