# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('personalizedDailyCard')
if idx != -1:
    print(c[idx-50:idx+2500])
else:
    print("Not found")

