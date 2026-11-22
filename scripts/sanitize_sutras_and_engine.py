import os, re, shutil

# 1. Clean js/vyas_daivagya_engine.js and android_app/app/src/main/assets/js/vyas_daivagya_engine.js
def clean_engine(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replacements
    text = text.replace("ज्योतिषाचार्य बृजेश गौतम 'धागा-तंत्र' एवं चेतना विज्ञान", "प्रायोगिक धागा-तंत्र एवं चेतना-विज्ञान सूत्र")
    text = text.replace("धागा-तंत्र एवं चेतना विज्ञान (बृजेश गौतम सूत्र)", "धागा-तंत्र एवं चेतना विज्ञान (दैहिक भाव-संरेखण सूत्र)")
    text = text.replace("ज्योतिषाचार्य बृजेश गौतम \\'धागा-तंत्र\\' व लाल किताब", "प्रायोगिक धागा-तंत्र व लाल किताब")
    text = text.replace("ज्योतिषाचार्य बृजेश गौतम 'धागा-तंत्र' व लाल किताब", "प्रायोगिक धागा-तंत्र व लाल किताब")
    text = text.replace("ज्योतिषाचार्य बृजेश गौतम", "प्रायोगिक शोध-पद्धति")
    text = text.replace("बृजेश गौतम सूत्र", "दैहिक भाव-संरेखण सूत्र")
    text = text.replace("बृजेश गौतम", "दैहिक धागा-तंत्र")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

clean_engine('js/vyas_daivagya_engine.js')
clean_engine('android_app/app/src/main/assets/js/vyas_daivagya_engine.js')

# 2. Sanitize and write the complete 50-sutras book to books/Dhaga_Tantra_and_Chetna_Vigyan_Mahagranth.md
# Read the user-supplied text from the user's prompt or books
raw_book_path = 'books/Brajesh_Gautam_Dhaga_Tantra_and_Chetna_Vigyan_Mahagranth.md'
if os.path.exists(raw_book_path):
    with open(raw_book_path, 'r', encoding='utf-8') as f:
        book_content = f.read()
else:
    book_content = ""

# Sanitize names out of book content
sanitized_book = book_content
sanitized_book = re.sub(r'# ज्योतिषाचार्य बृजेश गौतम \(Brajesh Gautamm\) —\s*', '# ', sanitized_book)
sanitized_book = re.sub(r'ज्योतिषाचार्य बृजेश गौतम \(\[Brajesh Gautamm\].*?\)', 'आधुनिक प्रायोगिक शोध-पद्धति', sanitized_book)
sanitized_book = re.sub(r'आचार्य बृजेश गौतम की शोध-प्रणाली में\s*', 'इस शोध-प्रणाली में ', sanitized_book)
sanitized_book = re.sub(r'आचार्य बृजेश गौतम के अनुसार\s*', 'प्रायोगिक चेतना-विज्ञान के अनुसार ', sanitized_book)
sanitized_book = re.sub(r'आचार्य बृजेश गौतम ने\s*', 'इस शोध में ', sanitized_book)
sanitized_book = re.sub(r'आचार्य बृजेश गौतम\s*', 'प्रायोगिक चेतना-विज्ञान ', sanitized_book)
sanitized_book = re.sub(r'बृजेश गौतम प्रणाली के स्वतंत्र/सह-स्वामी ग्रह', '12-ग्रह प्रणाली के स्वतंत्र/सह-स्वामी ग्रह', sanitized_book)
sanitized_book = re.sub(r'आचार्य बृजेश गौतम का एकीकृत मास्टर-सूत्र', 'एकीकृत सार्वभौमिक मास्टर-सूत्र', sanitized_book)
sanitized_book = re.sub(r'Brajesh Gautam|Brajesh Gautamm', 'Daivagya Shodh', sanitized_book, flags=re.I)

new_book_path = 'books/Dhaga_Tantra_and_Chetna_Vigyan_Mahagranth.md'
with open(new_book_path, 'w', encoding='utf-8') as f:
    f.write(sanitized_book)
print(f"Wrote sanitized book to {new_book_path}")

# Remove old book file if exists
if os.path.exists(raw_book_path) and raw_book_path != new_book_path:
    os.remove(raw_book_path)
    print(f"Removed {raw_book_path}")

# 3. Copy sanitized reference to skills
ref_destinations = [
    'skills/vyas-jyotisha/references',
    r'C:\Users\Administrator\.gemini\config\plugins\daivagya-astrology\skills\vyas-jyotisha\references',
    r'C:\Users\Administrator\.gemini\config\plugins\ecc\skills\vyas-jyotisha\references'
]

for d in ref_destinations:
    os.makedirs(d, exist_ok=True)
    # copy new
    shutil.copy2(new_book_path, os.path.join(d, 'dhaga-tantra-chetna-vigyan.md'))
    # remove old if exists
    old_f = os.path.join(d, 'brajesh-gautam-dhaga-tantra.md')
    if os.path.exists(old_f):
        os.remove(old_f)
    print(f"Updated references in {d}")

# 4. Update SKILL.md in skills/vyas-jyotisha and plugins
def update_skill_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        skill = f.read()

    skill = skill.replace('brajesh-gautam-dhaga-tantra.md', 'dhaga-tantra-chetna-vigyan.md')
    skill = skill.replace('Brajesh Gautam Dhaaga Tantra, body-house mapping', 'प्रायोगिक धागा-तंत्र, दैहिक भाव-मानचित्रण')
    skill = skill.replace('Brajesh Gautam Dhaaga Tantra', 'प्रायोगिक धागा-तंत्र')

    # Add anonymous sutras mandate in remedies bullet if not already present
    rule_text = "never name modern astrologers in sutras or remedies (present rules impersonally by systemic name, e.g. 'दैहिक धागा-तंत्र सूत्र', '12-ग्रह स्वामित्व प्रणाली', 'प्रतीकात्मक प्रारब्ध प्रतिस्थापन', 'दीपक व पंचतत्व चेतना विज्ञान');"
    if "never name modern astrologers" not in skill:
        skill = skill.replace("never invent mantras/seed syllables;", rule_text + " never invent mantras/seed syllables;")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(skill)
    print(f"Updated {filepath}")

skill_files = [
    'skills/vyas-jyotisha/SKILL.md',
    r'C:\Users\Administrator\.gemini\config\plugins\daivagya-astrology\skills\vyas-jyotisha\SKILL.md',
    r'C:\Users\Administrator\.gemini\config\plugins\ecc\skills\vyas-jyotisha\SKILL.md'
]
for sf in skill_files:
    update_skill_file(sf)

# 5. Update api/ai_chat.php system prompt to add explicit Sutra Anonymity directive
with open('api/ai_chat.php', 'r', encoding='utf-8') as f:
    php_text = f.read()

anon_instruction = "\\nSUTRA ANONYMITY & IMPERSONAL SYSTEMIC DIRECTIVE: Never attribute astrological sutras, remedies, or techniques to any modern astrologer by personal name. Always present all techniques purely by their systemic and functional names (e.g. 'दैहिक धागा-तंत्र सूत्र', '12-ग्रह स्वामित्व प्रणाली', 'प्रतीकात्मक प्रारब्ध प्रतिस्थापन', 'दीपक व पंचतत्व चेतना विज्ञान', 'दशमहाविद्या व ज्योतिर्लिंग कवच', 'औरा-रक्षा व नज़र निवारण सूत्र'). State the exact physical mechanisms, body-house mappings, and practical steps with zero personal branding."

if "SUTRA ANONYMITY & IMPERSONAL SYSTEMIC DIRECTIVE" not in php_text:
    target_pos = php_text.find("Never reverse this order merely to produce an attractive answer.")
    if target_pos != -1:
        insert_pos = target_pos + len("Never reverse this order merely to produce an attractive answer.")
        php_text = php_text[:insert_pos] + anon_instruction + php_text[insert_pos:]
        with open('api/ai_chat.php', 'w', encoding='utf-8') as f:
            f.write(php_text)
        print("Updated api/ai_chat.php with SUTRA ANONYMITY DIRECTIVE")
    else:
        print("Target position not found in api/ai_chat.php")
else:
    print("SUTRA ANONYMITY already in api/ai_chat.php")
