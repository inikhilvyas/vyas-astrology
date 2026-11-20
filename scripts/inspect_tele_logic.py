with open('scripts/vyas_telegram_bot.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Total lines:", len(lines))
# Let's see handle_command and answer_with_acharya_vyas
for i, l in enumerate(lines):
    if 'def handle_command' in l or 'def answer_with_acharya_vyas' in l:
        print(f"--- Line {i+1} ---")
        print("".join(lines[i:i+45]))

