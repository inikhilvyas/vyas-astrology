import re

PRO_METHODS = """        isProAccount: function(email) {
            if (!email) return false;
            var norm = email.trim().toLowerCase();
            try {
                var proList = JSON.parse(localStorage.getItem('vyas_pro_users') || '[]');
                if (proList.indexOf(norm) !== -1) return true;
                if (localStorage.getItem('vyas_pro_active') === 'true') return true;
                if (localStorage.getItem('vyas_vip_member_' + norm) === 'true') return true;
            } catch(e) {}
            var authorizedPro = ['inikhilvyas@gmail.com', 'nikhilvyas007@gmail.com', 'vyasbilawas@gmail.com'];
            if (authorizedPro.indexOf(norm) !== -1) return true;
            return false;
        },

        setProAccount: function(email, isPro) {
            if (!email) return;
            var norm = email.trim().toLowerCase();
            try {
                var proList = JSON.parse(localStorage.getItem('vyas_pro_users') || '[]');
                var idx = proList.indexOf(norm);
                if (isPro && idx === -1) {
                    proList.push(norm);
                } else if (!isPro && idx !== -1) {
                    proList.splice(idx, 1);
                }
                localStorage.setItem('vyas_pro_users', JSON.stringify(proList));
                localStorage.setItem('vyas_vip_member_' + norm, isPro ? 'true' : 'false');
            } catch(e) {}
            this.updateGoogleAuthUI();
        },
"""

# Patch index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'isProAccount: function' not in content:
    target = 'updateGoogleAuthUI: function() {'
    replacement = PRO_METHODS + '\n        ' + target
    content = content.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Added isProAccount & setProAccount to index.html")
else:
    print("index.html already has isProAccount")

# Patch mobile files
for path in ['mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        m_content = f.read()
    if 'isProAccount: function' not in m_content:
        target = 'updateGoogleAuthUI: function() {'
        replacement = PRO_METHODS + '\n        ' + target
        m_content = m_content.replace(target, replacement, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(m_content)
        print(f"✓ Added isProAccount & setProAccount to {path}")
    else:
        print(f"{path} already has isProAccount")
