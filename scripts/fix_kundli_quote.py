with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad_str = 'ऊपर <b>"+ नई कुण्डली"</b> विकल्प'
good_str = 'ऊपर <b>&apos;+ नई कुण्डली&apos;</b> विकल्प'

if bad_str in text:
    text = text.replace(bad_str, good_str)
    print("✓ Successfully fixed broken string quote at 312974!")
else:
    print("! bad_str not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

