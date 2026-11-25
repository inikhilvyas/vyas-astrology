import os, sys, json, re

def main():
    treatise_path = os.path.join('docs', 'vyas_astra_complete_research_treatise.md')
    if not os.path.exists(treatise_path):
        print("Treatise file not found!")
        return

    with open(treatise_path, 'r', encoding='utf-8') as f:
        treatise_text = f.read()

    print(f"Loaded treatise: {len(treatise_text)} chars")

    # Split into parts
    parts = re.split(r'# भाग (\d+):', treatise_text)
    
    extracted_sutras = []
    
    for i in range(1, len(parts), 2):
        part_num = parts[i]
        part_content = parts[i+1]
        lines = part_content.split('\n')
        part_title = lines[0].strip() if lines else f"Part {part_num}"
        
        # Matches: "1. **Title:** text" or "* **Title:** text" or "### 1. सूर्य..."
        items = re.findall(r'(?:^|\n)(?:\d+\.|\*)\s+\*\*([^*]+)\*\*:?\s*([^\n]+(?:\n(?!\d+\.|\*|#).*)*)', part_content)
        for title, body in items:
            title = title.strip().rstrip(':')
            body = re.sub(r'\s+', ' ', body).strip()
            if len(body) > 10:
                extracted_sutras.append({
                    "part": part_num,
                    "section": part_title,
                    "title": title,
                    "body": body,
                    "source": f"व्यास अस्त्र महा-शोधग्रंथ (भाग {part_num}: {part_title}) — Nikhil Vyas"
                })
        
        # Also grab sub-bullet lines like "* **वैदिक व तांत्रिक मंत्र:** ..."
        sub_items = re.findall(r'(?:^|\n)\s*\*\s+\*\*([^*]+)\*\*:?\s*([^\n]+)', part_content)
        for stitle, sbody in sub_items:
            stitle = stitle.strip().rstrip(':')
            sbody = sbody.strip()
            if len(sbody) > 10 and not any(x['title'] == stitle for x in extracted_sutras):
                extracted_sutras.append({
                    "part": part_num,
                    "section": part_title,
                    "title": stitle,
                    "body": sbody,
                    "source": f"व्यास अस्त्र नवग्रह महा-संहिता (भाग {part_num}) — Nikhil Vyas"
                })

    print(f"Extracted {len(extracted_sutras)} structured sutras from treatise.")

    bank_path = os.path.join('js', 'vyas_sutras_bank.js')
    with open(bank_path, 'r', encoding='utf-8') as f:
        bank_content = f.read()

    # Create JS array for newly ingested treatise sutras
    treatise_entries = []
    for s in extracted_sutras:
        cond = f"{s['title']} ({s['section']})"
        pred = s['body']
        src = s['source']
        domain = "remedy" if any(w in cond for w in ["उपाय", "मंत्र", "यंत्र", "स्नान", "दान", "रुद्राक्ष"]) else "general"
        treatise_entries.append([cond, pred, src, domain])

    json_treatise = json.dumps(treatise_entries, ensure_ascii=False)

    # We want to attach NIKHIL_VYAS_TREATISE_SUTRAS to window.VyasSutrasBank and check it at the VERY BEGINNING of searchSutras
    # Let's clean any previous injection
    if "NIKHIL_VYAS_TREATISE_SUTRAS" in bank_content:
        bank_content = re.sub(r'// ═════════+\s*// VYAS ASTRA — NIKHIL VYAS MAHA-RESEARCH TREATISE DATA INGESTION.*?var NIKHIL_VYAS_TREATISE_SUTRAS = .*?;\s*', '', bank_content, flags=re.DOTALL)
        bank_content = re.sub(r'// --- NIKHIL VYAS TREATISE SCAN START ---.*?// --- NIKHIL VYAS TREATISE SCAN END ---\s*', '', bank_content, flags=re.DOTALL)

    # Code to inject right before `window.VyasSutrasBank = {`
    data_decl = f"""
    // ══════════════════════════════════════════════════════════════════════════════
    // VYAS ASTRA — NIKHIL VYAS MAHA-RESEARCH TREATISE DATA INGESTION (11 PARTS)
    // ══════════════════════════════════════════════════════════════════════════════
    var NIKHIL_VYAS_TREATISE_SUTRAS = {json_treatise};
"""
    idx_bank_decl = bank_content.find('window.VyasSutrasBank = {')
    if idx_bank_decl != -1:
        bank_content = bank_content[:idx_bank_decl] + data_decl + "\n    " + bank_content[idx_bank_decl:]

    # Code to inject at the top of searchSutras
    top_search_code = """
            // --- NIKHIL VYAS TREATISE SCAN START ---
            if (typeof NIKHIL_VYAS_TREATISE_SUTRAS !== 'undefined' && NIKHIL_VYAS_TREATISE_SUTRAS.length) {
                for (var ti = 0; ti < NIKHIL_VYAS_TREATISE_SUTRAS.length; ti++) {
                    var ts = NIKHIL_VYAS_TREATISE_SUTRAS[ti];
                    var tCond = (ts[0] || '').toLowerCase();
                    var tPred = (ts[1] || '').toLowerCase();
                    var tSrc = (ts[2] || '').toLowerCase();
                    if (tCond.indexOf(q) !== -1 || tPred.indexOf(q) !== -1 || tSrc.indexOf(q) !== -1) {
                        var tk = (ts[0] + ' ' + ts[1]).substring(0, 45);
                        if (!seen[tk]) {
                            seen[tk] = true;
                            results.push({
                                type: 'व्यास अस्त्र महा-शोधग्रंथ',
                                cond: ts[0],
                                pred: ts[1],
                                src: ts[2],
                                domain: ts[3]
                            });
                            if (results.length >= limit) return results;
                        }
                    }
                }
            }
            // --- NIKHIL VYAS TREATISE SCAN END ---
"""

    idx_search = bank_content.find('searchSutras: function(query, limit) {')
    if idx_search != -1:
        # Find where q is defined
        target_str = "var seen = {};"
        idx_seen = bank_content.find(target_str, idx_search)
        if idx_seen != -1:
            pos = idx_seen + len(target_str)
            bank_content = bank_content[:pos] + "\n" + top_search_code + "\n" + bank_content[pos:]

    with open(bank_path, 'w', encoding='utf-8') as f:
        f.write(bank_content)

    print(f"Successfully injected prioritized treatise search into {bank_path}!")

    # Copy to android assets
    android_bank = os.path.join('android_app', 'app', 'src', 'main', 'assets', 'js', 'vyas_sutras_bank.js')
    if os.path.exists(os.path.dirname(android_bank)):
        with open(android_bank, 'w', encoding='utf-8') as f:
            f.write(bank_content)
        print(f"Synced to {android_bank}!")

if __name__ == '__main__':
    main()
