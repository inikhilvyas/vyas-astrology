import json, re

t_path = r'C:\Users\Administrator\.gemini\antigravity\brain\bf41d1cd-300b-445c-bfd4-855f546b57c2\.system_generated\logs\transcript_full.jsonl'
with open(t_path, 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if 'webhook' in line.lower() and 'hostinger' in line.lower():
            urls = re.findall(r'https?://[^\s"\'<>]+', line)
            for u in urls:
                if 'hostinger' in u.lower() or 'deploy' in u.lower():
                    print(f"Line {i}: {u}")

