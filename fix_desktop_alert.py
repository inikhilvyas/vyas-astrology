with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad_alert = 'alert("नमस्ते " + name + " जी! आपका Google साइन-इन सफल हुआ। अपनी कुण्डली देखने हेतु ऊपर \'नई कुण्डली\' बटन पर क्लिक करके अपना जन्म विवरण दर्ज करें।");'
new_clean_code = '// Signed in smoothly without fake alert\n            console.log("User session active:", name);'

assert bad_alert in text, "bad_alert not found in index.html"
text = text.replace(bad_alert, new_clean_code)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed fake Google alert from index.html successfully!")

