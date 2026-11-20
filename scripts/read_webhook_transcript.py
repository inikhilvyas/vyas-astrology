import json, os

t_path = r'C:\Users\Administrator\.gemini\antigravity\brain\bf41d1cd-300b-445c-bfd4-855f546b57c2\.system_generated\logs\transcript_full.jsonl'
with open(t_path, 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if 'webhook' in line.lower() and ('hostinger' in line.lower() or 'deploy' in line.lower()):
            obj = json.loads(line)
            txt = str(obj.get('content', ''))
            print(f"Match at line {i}: {txt[:400]}")

