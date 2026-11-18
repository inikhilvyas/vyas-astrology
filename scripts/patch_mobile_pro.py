with open('mobile/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace VIP in text
html = html.replace('NIKHIL (VIP)', 'NIKHIL (PRO)')
html = html.replace('NIKHIL (PRO VIP)', 'NIKHIL (PRO)')
html = html.replace('(PRO VIP)', '(PRO)')
html = html.replace('VIP क्लब', 'PRO क्लब')
html = html.replace('VIP एक्सेस', 'PRO एक्सेस')
html = html.replace('VIP PDF', 'PRO शोध डॉसियर')
html = html.replace('VIP सदस्य', 'PRO सदस्य')
html = html.replace('VIP जातक', 'PRO जातक')
html = html.replace('vyas_vip_member_', 'vyas_pro_member_')

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Safely replaced VIP with PRO in mobile/index.html!")

