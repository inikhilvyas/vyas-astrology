import re

print("Patching security: Removing exposed Groq keys and direct client-side provider calls...")

for fp in ['index.html', 'mobile/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove keyPool definition
    content = re.sub(
        r'keyPool:\s*\[[^\]]*\],?\s*',
        '',
        content
    )

    # 2. In askSage, remove the client-side fetch("https://api.groq.com/openai/v1/chat/completions") fallback loop!
    # Let's inspect askSage structure in this file
    pos_ask = content.find('async askSage(')
    if pos_ask != -1:
        # Check where /api/ai_chat.php is called
        pos_php = content.find('/api/ai_chat.php', pos_ask)
        pos_groq = content.find('api.groq.com', pos_ask)
        print(f"{fp}: askSage at {pos_ask}, php at {pos_php}, groq at {pos_groq}")

        # Replace the direct groq fetch loop with a clean server-only fallback error
        groq_loop_pattern = re.compile(r'// Tier 2: Direct client-side attempt with key rotation.*?return "क्षमा करें, AI परामर्श सेवा वर्तमान में व्यस्त है। कृपया कुछ क्षण उपरांत पुनः प्रयास करें।";\s*\}', re.DOTALL)
        if groq_loop_pattern.search(content):
            content = groq_loop_pattern.sub(
                'return "क्षमा करें, AI परामर्श सर्वर से संपर्क नहीं हो सका। कृपया अपना इंटरनेट कनेक्शन जांचें अथवा कुछ क्षण उपरांत पुनः प्रयास करें।";\n        }',
                content
            )
            print(f"✓ Removed direct Groq loop from {fp}")
        else:
            # Fallback regex if comment differs
            content = re.sub(
                r'for\s*\(var attempt = 0;\s*attempt < this\.keyPool.*?return "क्षमा करें, AI परामर्श सेवा वर्तमान में व्यस्त है[^"]*";\s*\}',
                'return "क्षमा करें, AI परामर्श सर्वर से संपर्क नहीं हो सका। कृपया कुछ क्षण उपरांत पुनः प्रयास करें।";\n        }',
                content,
                flags=re.DOTALL
            )
            print(f"✓ Replaced Groq loop with safe error in {fp}")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

print("Security patch completed. Verifying remaining occurrences of gsk_ and api.groq.com:")
for fp in ['index.html', 'mobile/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        t = f.read()
    print(f"  {fp}: gsk_ count={t.count('gsk_')}, api.groq.com count={t.count('api.groq.com')}")

