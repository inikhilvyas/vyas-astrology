import json

log_path = r'C:\Users\Administrator\.gemini\antigravity\brain\bf41d1cd-300b-445c-bfd4-855f546b57c2\.system_generated\logs\transcript.jsonl'
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index', 0)
        if 27383 <= idx <= 27405:
            tc = data.get('tool_calls')
            content = str(data.get('content'))[:250]
            print(f"STEP {idx} [{data.get('type')}]: tc={tc} content={content}")
