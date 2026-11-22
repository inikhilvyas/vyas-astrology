with open('js/vyas_daivagya_engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
in_prastara = False
for l in lines:
    if 'generateComprehensivePrastaraPhalkathan' in l:
        in_prastara = True
    elif in_prastara and 'evaluateDashaPrastara' in l:
        in_prastara = False

    if in_prastara:
        # replace unescaped ' with " where appropriate
        if "rule: '" in l:
            # Change outer single quotes to double quotes
            val = l.strip()[len("rule: '"):-1]
            if val.endswith(","): val = val[:-1]
            if val.endswith("'"): val = val[:-1]
            val = val.replace('"', '\\"')
            l = f'                    rule: "{val}",\n'
        elif "range: '" in l:
            val = l.strip()[len("range: '"):-1]
            if val.endswith(","): val = val[:-1]
            if val.endswith("'"): val = val[:-1]
            val = val.replace("'", "\\'")
            l = f'                    range: "{val}",\n'
    out.append(l)

with open('js/vyas_daivagya_engine.js', 'w', encoding='utf-8') as f:
    f.writelines(out)

print("Safely quoted all rule and range properties")

