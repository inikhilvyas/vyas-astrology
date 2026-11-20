import sqlite3
import json
import glob
import os

db_path = 'data/vyas_phalit_vault.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create table with high-speed indexes
cur.execute("""
CREATE TABLE IF NOT EXISTS sutras (
    sutra_id TEXT PRIMARY KEY,
    category TEXT,
    sub_category TEXT,
    primary_factor TEXT,
    planetary_condition TEXT,
    condition_hi TEXT,
    prediction_en TEXT,
    prediction_hi TEXT,
    life_domain TEXT,
    source TEXT,
    strength_modifiers TEXT
)
""")

cur.execute("CREATE INDEX IF NOT EXISTS idx_sutras_category ON sutras(category);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_sutras_domain ON sutras(life_domain);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_sutras_factor ON sutras(primary_factor);")

jsonl_files = sorted(glob.glob('books_downloaded/*.jsonl'))
print(f"Found {len(jsonl_files)} JSONL files to ingest into {db_path}...")

total_inserted = 0
total_skipped = 0

for jf in jsonl_files:
    fname = os.path.basename(jf)
    print(f"Processing {fname}...")
    batch = []
    with open(jf, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                sid = row.get('sutra_id')
                if not sid:
                    continue
                batch.append((
                    sid,
                    row.get('category', ''),
                    row.get('sub_category', ''),
                    row.get('primary_factor', ''),
                    row.get('planetary_condition', ''),
                    row.get('condition_hi', ''),
                    row.get('prediction_en', ''),
                    row.get('prediction_hi', ''),
                    row.get('life_domain', ''),
                    row.get('source', ''),
                    row.get('strength_modifiers', '')
                ))
            except Exception as err:
                print(f"  Error parsing row: {err}")
    
    if batch:
        cur.executemany("""
            INSERT OR IGNORE INTO sutras 
            (sutra_id, category, sub_category, primary_factor, planetary_condition, condition_hi, prediction_en, prediction_hi, life_domain, source, strength_modifiers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, batch)
        conn.commit()
        print(f"  ✓ Ingested {len(batch)} records from {fname}")
        total_inserted += len(batch)

cur.execute("SELECT count(*) FROM sutras")
final_count = cur.fetchone()[0]
conn.close()

print("\n==========================================")
print(f"INGESTION COMPLETE! Total sutras in SQLite DB: {final_count}")
print("==========================================")

