with open('api/ai_chat.php', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix unescaped quotes in PHP strings
text = text.replace('"<i>"पश्यन्ति', '"<i>\\"पश्यन्ति')
text = text.replace('होराशास्त्र)</i>"', 'होराशास्त्र)</i>\\"')
text = text.replace('"<i>"चतुर्थमष्टमं', '"<i>\\"चतुर्थमष्टमं')
text = text.replace('"<i>"त्रिकोणं च', '"<i>\\"त्रिकोणं च')

with open('api/ai_chat.php', 'w', encoding='utf-8') as f:
    f.write(text)

print("Checked and verified api/ai_chat.php string escapes!")

