"""Add SS fields to hr_employees table."""
import sqlite3
from pathlib import Path

# Try multiple possible database locations
db_paths = [
    Path("/home/dario/src/org_1.db"),
    Path("/home/dario/org_1.db"),
    Path("/home/dario/src/dario.db"),
    Path("/home/dario/src/data/erp.db"),
]

db_path = None
for path in db_paths:
    if path.exists():
        db_path = path
        print(f"Found database at: {db_path}")
        break

if not db_path:
    print(f"Database not found. Tried: {[str(p) for p in db_paths]}")
    exit(1)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check existing columns
cursor.execute("PRAGMA table_info(hr_employees)")
existing_columns = {row[1] for row in cursor.fetchall()}

print(f"Existing columns: {existing_columns}")

# Add new columns if they don't exist
new_columns = [
    ("contract_type", "VARCHAR(100)"),
    ("ss_number", "VARCHAR(50)"),
    ("ss_status", "VARCHAR(30)"),
    ("ss_alta_date", "DATE"),
    ("ss_baja_date", "DATE"),
    ("ss_notes", "TEXT"),
]

for col_name, col_type in new_columns:
    if col_name not in existing_columns:
        try:
            cursor.execute(f"ALTER TABLE hr_employees ADD COLUMN {col_name} {col_type}")
            print(f"✓ Added column: {col_name}")
        except sqlite3.Error as e:
            print(f"✗ Error adding {col_name}: {e}")
    else:
        print(f"- Column {col_name} already exists")

conn.commit()
conn.close()

print("\n✓ Migration complete!")
