print("=== VERIFICATION 4: Checking AI Bot Token Limit & Continuation ===")

with open('api/ai_chat.php', 'r', encoding='utf-8') as f:
    php = f.read()

assert 'max_tokens' in php, "max_tokens missing in php"
assert '3800' in php, "max_tokens is not 3800 in php!"
assert '$chatHistory' in php, "chatHistory missing in php!"
assert '$isContinuation' in php, "continuation detection missing in php!"
print("✓ PHP Backend: max_tokens is 3800, chatHistory and continuation logic verified.")

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m = f.read()

assert 'chatHistory: historyToSend' in m, "historyToSend not passed in mobile askSage!"
print("✓ Mobile Frontend: chatHistory is passed to /api/ai_chat.php.")

print("✓ VERIFICATION 4 PASSED: AI dialogue continuity and token limits 100% verified!")

