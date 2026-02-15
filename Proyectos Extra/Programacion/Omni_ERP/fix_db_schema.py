import sqlite3
import os

DB_PATH = "/home/dario/src/data/org_dbs/org_1.db"

def add_column():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("Checking if column 'observaciones' exists in 'ventas_pos'...")
        cursor.execute("PRAGMA table_info(ventas_pos)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "observaciones" in columns:
            print("Column 'observaciones' already exists.")
        else:
            print("Adding column 'observaciones' to 'ventas_pos'...")
            cursor.execute("ALTER TABLE ventas_pos ADD COLUMN observaciones TEXT")
            conn.commit()
            print("Column added successfully.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_column()