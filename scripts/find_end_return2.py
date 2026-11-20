with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 660989
idx2 = text.find('return {', pos + 100)
print("Return after 660989 found at", idx2)
if idx2 != -1:
    print(text[idx2:idx2+1500])

