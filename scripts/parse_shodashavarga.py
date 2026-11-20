import json

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('SHODASHAVARGA_DATA =')
idx2 = text.find(';\n', idx)
json_str = text[idx + len('SHODASHAVARGA_DATA = '):idx2].strip()

try:
    data = json.loads(json_str)
    print("Parsed SHODASHAVARGA_DATA successfully! Keys:", list(data.keys()))
    for k, v in data.items():
        print(f"{k}: title='{v.get('title')}', ascSign='{v.get('ascSign')}', house1={v.get('houses', {}).get('1')}")
except Exception as e:
    print("JSON parse error:", e)
    print("Sample:", json_str[:500])

