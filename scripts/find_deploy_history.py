with open(r'C:\Users\Administrator\.gemini\antigravity\brain\bf41d1cd-300b-445c-bfd4-855f546b57c2\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if '"step_index":45454' in line or 'task-45454' in line:
            import json
            obj = json.loads(line)
            print(f"Step {obj.get('step_index')}: {str(obj.get('tool_calls') or obj.get('content'))[:250]}")
