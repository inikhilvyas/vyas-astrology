with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace all unescaped single quotes inside the injected text
replacements = [
    ("<i>'तत्र", '<i>"तत्र'),
    ("साधिकोऽंशैः'</i>", 'साधिकोऽंशैः"</i>'),
    ("<i>'अमात्ये", '<i>"अमात्ये'),
    ("कर्मसम्बन्धः'</i>", 'कर्मसम्बन्धः"</i>'),
    ("<i>'उपपदारूढं", '<i>"उपपदारूढं'),
    ("कलत्रसौख्यम्'</i>", 'कलत्रसौख्यम्"</i>'),
    ("<i>'चराः", '<i>"चराः'),
    ("निकटस्थितम्'</i>", 'निकटस्थितम्"</i>'),
    ("<i>'The Sub-Lord", '<i>"The Sub-Lord'),
    ("that house.'</i>", 'that house."</i>'),
    ("<i>'दशा ददाति", '<i>"दशा ददाति'),
    ("प्रकाशयति'</i>", 'प्रकाशयति"</i>'),
    ("<i>'दीर्घास्यो", '<i>"दीर्घास्यो'),
    ("रुचकयोगे।'</i>", 'रुचकयोगे।"</i>'),
    ("<i>'नीचस्थितो", '<i>"नीचस्थितो'),
    ("नृपतिप्रतीतः।'</i>", 'नृपतिप्रतीतः।"</i>'),
    ("<i>'शशयोगोद्भवो", '<i>"शशयोगोद्भवो'),
    ("लोकपूजितः।'</i>", 'लोकपूजितः।"</i>'),
    ("<b>'+ नई कुण्डली'</b>", '<b>"+ नई कुण्डली"</b>')
]

for old, new in replacements:
    if old in c:
        c = c.replace(old, new)
        print(f"Replaced: {old[:20]} -> {new[:20]}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Quotes cleanly sanitized in index.html!")

