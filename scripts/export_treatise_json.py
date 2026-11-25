import os, sys, json, re

def main():
    treatise_path = os.path.join('docs', 'vyas_astra_complete_research_treatise.md')
    with open(treatise_path, 'r', encoding='utf-8') as f:
        treatise_text = f.read()

    parts = re.split(r'# भाग (\d+):', treatise_text)
    extracted_sutras = []
    
    for i in range(1, len(parts), 2):
        part_num = parts[i]
        part_content = parts[i+1]
        lines = part_content.split('\n')
        part_title = lines[0].strip() if lines else f"Part {part_num}"
        
        items = re.findall(r'(?:^|\n)(?:\d+\.|\*)\s+\*\*([^*]+)\*\*:?\s*([^\n]+(?:\n(?!\d+\.|\*|#).*)*)', part_content)
        for title, body in items:
            title = title.strip().rstrip(':')
            body = re.sub(r'\s+', ' ', body).strip()
            if len(body) > 10:
                extracted_sutras.append({
                    "cond": f"{title} ({part_title})",
                    "pred": body,
                    "source": f"व्यास अस्त्र महा-शोधग्रंथ (भाग {part_num}) — Nikhil Vyas",
                    "domain": "remedy" if any(w in title for w in ["उपाय", "मंत्र", "यंत्र", "स्नान", "दान", "रुद्राक्ष"]) else "general"
                })

    out_json = os.path.join('data', 'nikhil_vyas_treatise_sutras.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(extracted_sutras, f, ensure_ascii=False, indent=2)

    print(f"Generated {out_json} with {len(extracted_sutras)} sutras.")

if __name__ == '__main__':
    main()

