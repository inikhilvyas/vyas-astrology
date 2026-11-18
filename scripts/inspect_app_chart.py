with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

m = text.find('chart = Chart(asc_lon, planets)')
print(text[m-800:m+1200])

