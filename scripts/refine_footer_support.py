import os

for fp in ['index.html', 'mobile/index.html', 'static/mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html', 'admin.html']:
    if not os.path.exists(fp): continue
    with open(fp, 'r', encoding='utf-8') as f:
        t = f.read()

    # Clean tel:+91support@vyasastro.in
    t = t.replace('tel:+91support@vyasastro.in', 'mailto:support@vyasastro.in')
    t = t.replace('tel:support@vyasastro.in', 'mailto:support@vyasastro.in')
    t = t.replace('+91 support@vyasastro.in', 'support@vyasastro.in')
    t = t.replace('WhatsApp / कॉल:', 'आधिकारिक सहायता:')
    t = t.replace('📞 सम्पर्क: <a href="mailto:support@vyasastro.in" style="color:#38BDF8; font-weight:700; text-decoration:none;">support@vyasastro.in</a> • ✉️ ईमेल: <a href="mailto:support@vyasastro.in"', '✉️ आधिकारिक सहायता: <a href="mailto:support@vyasastro.in"')
    t = t.replace('📞 <a href="mailto:support@vyasastro.in" style="color:#38BDF8; font-weight:700; text-decoration:none;">support@vyasastro.in</a> • ✉️ <a href="mailto:support@vyasastro.in"', '✉️ सहायता: <a href="mailto:support@vyasastro.in"')
    t = t.replace('अथवा +91 support@vyasastro.in पर संपर्क करें', 'अथवा support@vyasastro.in पर संपर्क करें')
    t = t.replace("['support@vyasastro.in', 'admin@vyasastro.in', 'support@vyasastro.in']", "['support@vyasastro.in', 'admin@vyasastro.in']")
    t = t.replace("mailto:support@vyasastro.inनमस्ते", "mailto:support@vyasastro.in?subject=VYAS%20ASTRA%20PRO%20Inquiry&body=नमस्ते")
    t = t.replace("mailto:support@vyasastro.in?text=", "mailto:support@vyasastro.in?subject=VYAS%20ASTRA%20PRO%20Subscription&body=")
    t = t.replace('💬 WhatsApp पर संपर्क करें', '✉️ सहायता डेस्क पर संपर्क करें')
    t = t.replace('https://chat.whatsapp.com', '#')
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Refined {fp}")

