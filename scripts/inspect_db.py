import sqlite3

def main():
    conn = sqlite3.connect("vyas_users.db")
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    print("Tables:", tables)
    for t in tables:
        cols = [col[1] for col in conn.execute(f"PRAGMA table_info({t})").fetchall()]
        count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"Table: {t} (Count: {count}) -> Columns: {cols}")

if __name__ == "__main__":
    main()

