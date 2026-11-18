with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('computeMathematicalKundli(name, dobStr')
# search for 'd1:' after pos + 2500
p = text.find('d1:', pos + 2500)
while p != -1 and p < pos + 10000:
    print(text[p-50:p+300])
    print("="*40)
    p = text.find('d1:', p + 20)

