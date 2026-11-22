with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print("mobile/index.html total lines:", len(lines))
for i, l in enumerate(lines):
    if any(k in l for k in ['handleGoogleCredentialResponse', 'applyAuthenticatedGoogleUser', 'google.accounts', 'vyas_google_user', 'loadFromUserVault']):
        print(f"{i+1}: {l.strip()[:100]}")

