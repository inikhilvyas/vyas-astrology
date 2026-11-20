with open('api/ai_chat.php', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"<i>"{$nak[\'shloka\']}"</i><br>"', '"<i>\\"" . $nak[\'shloka\'] . "\\"</i><br>"')
text = text.replace('"<i>"{$ras[\'shloka\']}"</i><br>"', '"<i>\\"" . $ras[\'shloka\'] . "\\"</i><br>"')
text = text.replace('होराशास्त्र)</i>\\";', 'होराशास्त्र)</i>";')

with open('api/ai_chat.php', 'w', encoding='utf-8') as f:
    f.write(text)

print("Properly escaped all PHP shloka quotes!")

