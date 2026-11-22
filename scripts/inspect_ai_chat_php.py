import os
if os.path.exists('api/ai_chat.php'):
    with open('api/ai_chat.php', 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read()[:1500])
else:
    print("api/ai_chat.php does not exist!")
