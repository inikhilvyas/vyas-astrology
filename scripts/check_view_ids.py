# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for vidha in ['kp', 'jaimini', 'nadi', 'ashtakavarga', 'dasha', 'predictions']:
    target1 = 'id="view-' + vidha + '"'
    target2 = "id='view-" + vidha + "'"
    print("view-" + vidha + " in index.html:", target1 in text or target2 in text)

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    mtext = f.read()

for vidha in ['kp', 'jaimini', 'nadi', 'ashtakavarga', 'dasha', 'predictions']:
    target1 = 'id="view-' + vidha + '"'
    target2 = "id='view-" + vidha + "'"
    print("view-" + vidha + " in mobile/index.html:", target1 in mtext or target2 in mtext)
