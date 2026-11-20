import sqlite3

conn = sqlite3.connect('data/vyas_phalit_vault.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM sutras')
print('Total sutras in vault:', c.fetchone()[0])

c.execute('SELECT category, count(*) FROM sutras GROUP BY category ORDER BY count(*) DESC LIMIT 20')
for row in c.fetchall():
    print(row)
conn.close()
