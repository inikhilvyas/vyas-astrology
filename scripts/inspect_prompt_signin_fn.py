with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('promptGoogleSignIn: function')
if pos == -1:
    pos = text.find('promptGoogleSignIn')
    # find function
    pos = text.find('promptGoogleSignIn', pos+20)

if pos != -1:
    print(text[pos-50:pos+1200])

