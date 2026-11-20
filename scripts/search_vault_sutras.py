import sqlite3

conn = sqlite3.connect('data/vyas_phalit_vault.db')
cursor = conn.cursor()

cursor.execute("SELECT count(*) FROM sutras")
total = cursor.fetchone()[0]
print(f"Total sutras in vault: {total}")

cursor.execute("PRAGMA table_info(sutras)")
cols = cursor.fetchall()
print("Columns:", [c[1] for c in cols])

# Find sutras specifically matching Nikhil's key combinations:
# e.g. Mars in Capricorn, Saturn in Libra, Jupiter in Sagittarius, Sun in Scorpio, etc.
queries = [
    "मकर AND मंगल",
    "तुला AND शनि",
    "धनु AND गुरु",
    "दशम AND मंगल",
    "सप्तम AND शनि",
    "नवम AND गुरु",
    "रुचक",
    "शश",
    "नीचभंग"
]

for q in queries:
    parts = q.split(" AND ")
    sql = "SELECT id, treatise, condition_sanskrit, condition_hindi, prediction_hindi FROM sutras WHERE " + " AND ".join(["(condition_hindi LIKE ? OR prediction_hindi LIKE ?)" for _ in parts]) + " LIMIT 2"
    params = []
    for p in parts:
        params.extend([f"%{p}%", f"%{p}%"])
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    print(f"Query '{q}': found {len(rows)} matching sutras")
    for r in rows:
        print(f"  [{r[0]}] {r[1]}: cond='{r[3][:60]}...' -> pred='{r[4][:60]}...'")

conn.close()

