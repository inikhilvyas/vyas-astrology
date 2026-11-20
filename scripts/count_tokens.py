content = open('api/ai_chat.php','r',encoding='utf-8').read()
start = content.find("<<<'EOD'")
end = content.find("EOD;")
if start > 0 and end > 0:
    block = content[start:end]
    print(f'jevAiSystemInstruction: ~{len(block)//4} tokens, {len(block)} chars')

gt_match = "INVIOLABLE VEDIC AXIOMS"
gt_start = content.find(gt_match)
print(f'Ground truth block found at char {gt_start}')

# Find the total PHP file size
print(f'Total PHP file: {len(content)} chars, ~{len(content)//4} tokens')
