print("=== VERIFICATION 2: Checking Google fake alert removal ===")

files_to_check = ['mobile/index.html', 'index.html', 'js/vyas_daivagya_vision.js']
for fpath in files_to_check:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    count = content.count('Google साइन-इन सफल')
    print(f"{fpath}: {count} occurrences of 'Google साइन-इन सफल'")
    assert count == 0, f"Found fake Google alert in {fpath}"

print("✓ VERIFICATION 2 PASSED: Fake Google alert completely eradicated from all surfaces!")

