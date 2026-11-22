with open('api/ai_chat.php', 'r', encoding='utf-8') as f:
    code = f.read()

# Verify matching braces
open_b = code.count('{')
close_b = code.count('}')
print(f"Braces check: open={open_b}, close={close_b}, match={open_b == close_b}")
print("Contains 8-second timeout:", 'CURLOPT_TIMEOUT, 8' in code)
print("Contains safeFallback:", '$safeFallback' in code)

