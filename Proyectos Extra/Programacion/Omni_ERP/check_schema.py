import sqlite3
import os

DB_PATH = "/home/dario/org_1.db"

def check_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(ventas_pos)")
    columns = cursor.fetchall()
    print("Columns in ventas_pos:")
    for col in columns:
        print(col)
    conn.close()

if __name__ == "__main__":
    check_schema()