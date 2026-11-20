import json, os

t_path = r'C:\Users\Administrator\.gemini\antigravity\brain\bf41d1cd-300b-445c-bfd4-855f546b57c2\.system_generated\logs\transcript.jsonl'
if os.path.exists(t_path):
    with open(t_path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if 'ftp' in line.lower() or 'webhook' in line.lower() or 'hostinger' in line.lower():
                try:
                    obj = json.loads(line)
                    txt = str(obj.get('content', ''))
                    if 'git push' in txt or 'push_to_inikhil' in txt or 'deploy' in txt:
                        print(f"Step {obj.get('step_index')}: {txt[:250]}")
                except Exception:
                    pass

