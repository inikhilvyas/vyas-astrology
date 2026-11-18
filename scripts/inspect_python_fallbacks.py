with open('src/vyas/chatbot.py', 'r', encoding='utf-8') as f:
    cb_lines = f.readlines()

print("--- src/vyas/chatbot.py:220-245 ---")
for i in range(218, min(len(cb_lines), 245)):
    print(f"L{i+1}: {cb_lines[i]}", end='')

with open('src/vyas/daivagya_engine.py', 'r', encoding='utf-8') as f:
    de_lines = f.readlines()

print("\n--- src/vyas/daivagya_engine.py:185-210 ---")
for i in range(185, min(len(de_lines), 210)):
    print(f"L{i+1}: {de_lines[i]}", end='')

