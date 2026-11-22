with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['modalProManager', 'openProModal', 'proLicenseKey', 'unlockPro', 'initiatePayment', 'razorpay', 'upiQr']):
        print(f"{i+1}: {l.strip()[:100]}")

