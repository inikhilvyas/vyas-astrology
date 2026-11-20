import json

with open('data/vyas_sutras_fast_index.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("Total domains in fast index:", list(d.get('domains', {}).keys()))
for dom, pool in d.get('domains', {}).items():
    print(f"Domain {dom}: {len(pool)} sutras")
    if len(pool) > 0:
        sample = pool[0]
        print(f"  Sample keys: {list(sample.keys())}")
        print(f"  cond_hi: {sample.get('cond_hi')}")
        print(f"  pred_hi: {sample.get('pred_hi')}")
    print('---')

