def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # replace 'धागा-तंत्र' with \'धागा-तंत्र\' or "धागा-तंत्र" inside JS single quotes
    bad = "ज्योतिषाचार्य बृजेश गौतम 'धागा-तंत्र' व लाल किताब"
    good = 'ज्योतिषाचार्य बृजेश गौतम \\\'धागा-तंत्र\\\' व लाल किताब'
    if bad in text:
        text = text.replace(bad, good)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Fixed {filepath}")
    else:
        print(f"Bad string not found in {filepath}")

fix_file('js/vyas_daivagya_engine.js')
fix_file('android_app/app/src/main/assets/js/vyas_daivagya_engine.js')

