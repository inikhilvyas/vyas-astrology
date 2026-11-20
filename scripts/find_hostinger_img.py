import json

t_path = r'C:\Users\Administrator\.gemini\antigravity\brain\bf41d1cd-300b-445c-bfd4-855f546b57c2\.system_generated\logs\transcript.jsonl'
with open(t_path, 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if 30700 <= i <= 30850:
            try:
                obj = json.loads(line)
                if obj.get('media'):
                    print(f"Media at step {obj.get('step_index')}: {obj.get('media')}")
                txt = str(obj.get('content', ''))
                if 'webhook' in txt.lower():
                    print(f"Step {obj.get('step_index')} mentions webhook: {txt[:200]}")
            except Exception:
                pass

