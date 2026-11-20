import json

t_path = r'C:\Users\Administrator\.gemini\antigravity\brain\bf41d1cd-300b-445c-bfd4-855f546b57c2\.system_generated\logs\transcript_full.jsonl'
with open(t_path, 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if i in [30788, 30816]:
            obj = json.loads(line)
            print(f"=== Line {i} ===")
            print(str(obj.get('content', ''))[:1500])

