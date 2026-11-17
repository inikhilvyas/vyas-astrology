with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = text.find("localStorage.removeItem('vyas_active_profile')")
while m != -1:
    print(text[m-200:m+200])
    print('---')
    m = text.find("localStorage.removeItem('vyas_active_profile')", m+1)
