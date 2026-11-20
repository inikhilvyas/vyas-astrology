with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 358211
start = text.rfind('function', 0, pos)
print("Function before 358211 is at", start)
print(text[start:start+400])

