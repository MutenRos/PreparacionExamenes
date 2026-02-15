"""Ensure HR tables and columns exist across all tenant DBs."""
import sqlite3
from pathlib import Path

DB_DIRS = [
    Path("/home/dario/src/data/org_dbs"),
    Path("/home/dario/src"),
    Path("/home/dario"),
]

DB_FILES = []
for d in DB_DIRS:
    if d.exists():
        DB_FILES.extend(list(d.glob("*.db")))

print(f"Found {len(DB_FILES)} db files")

HR_COLUMNS = [
    ("contract_type", "VARCHAR(100)"),
    ("ss_number", "VARCHAR(50)"),
    ("ss_status", "VARCHAR(30)"),
    ("ss_alta_date", "DATE"),
    ("ss_baja_date", "DATE"),
    ("ss_notes", "TEXT"),
]

CREATE_TABLES_SQL = {
    "hr_jobs": """
        CREATE TABLE IF NOT EXISTS hr_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            job_code VARCHAR(50) NOT NULL,
            title VARCHAR(255) NOT NULL,
            department VARCHAR(100),
            salary_min DECIMAL(12, 2),
            salary_max DECIMAL(12, 2),
            descripcion TEXT,
            activo BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "hr_positions": """
        CREATE TABLE IF NOT EXISTS hr_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            position_code VARCHAR(50) NOT NULL,
            title VARCHAR(255) NOT NULL,
            job_id INTEGER,
            department VARCHAR(100),
            location VARCHAR(255),
            manager_position_id INTEGER,
            status VARCHAR(30) DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "hr_employees": """
        CREATE TABLE IF NOT EXISTS hr_employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            employee_code VARCHAR(50) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255),
            position_id INTEGER,
            manager_id INTEGER,
            start_date DATE,
            end_date DATE,
            salary DECIMAL(12, 2),
            hourly_rate DECIMAL(10, 2),
            employment_type VARCHAR(50),
            contract_type VARCHAR(100),
            status VARCHAR(30) DEFAULT 'active',
            ss_number VARCHAR(50),
            ss_status VARCHAR(30),
            ss_alta_date DATE,
            ss_baja_date DATE,
            ss_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "hr_leave_requests": """
        CREATE TABLE IF NOT EXISTS hr_leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            leave_type VARCHAR(50) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status VARCHAR(30) DEFAULT 'pending',
            reason TEXT,
            approved_by_user_id INTEGER,
            approved_by_user_name VARCHAR(255),
            approved_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "hr_timesheets": """
        CREATE TABLE IF NOT EXISTS hr_timesheets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            period_start DATE NOT NULL,
            period_end DATE NOT NULL,
            status VARCHAR(30) DEFAULT 'draft',
            submitted_at TIMESTAMP,
            approved_at TIMESTAMP,
            approved_by_user_id INTEGER,
            approved_by_user_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "hr_timesheet_lines": """
        CREATE TABLE IF NOT EXISTS hr_timesheet_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            timesheet_id INTEGER NOT NULL,
            work_date DATE NOT NULL,
            project VARCHAR(100),
            task VARCHAR(255),
            hours DECIMAL(6, 2) NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "hr_payroll_runs": """
        CREATE TABLE IF NOT EXISTS hr_payroll_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            period_start DATE NOT NULL,
            period_end DATE NOT NULL,
            status VARCHAR(30) DEFAULT 'open',
            total_gross DECIMAL(14, 2) DEFAULT 0,
            total_net DECIMAL(14, 2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            posted_at TIMESTAMP
        )
    """,
    "hr_payroll_lines": """
        CREATE TABLE IF NOT EXISTS hr_payroll_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            payroll_run_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            gross_amount DECIMAL(14, 2) DEFAULT 0,
            tax_amount DECIMAL(14, 2) DEFAULT 0,
            net_amount DECIMAL(14, 2) DEFAULT 0,
            status VARCHAR(30) DEFAULT 'calculated',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
}

for db_path in DB_FILES:
    print(f"\n=== {db_path} ===")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}

    # Create tables if missing
    for tname, sql in CREATE_TABLES_SQL.items():
        if tname not in tables:
            print(f"Creating table {tname}")
            cursor.execute(sql)
        else:
            print(f"Table {tname} exists")

    # Ensure HR columns exist in hr_employees
    cursor.execute("PRAGMA table_info(hr_employees)")
    cols = {row[1] for row in cursor.fetchall()}
    if cols:
        for col_name, col_type in HR_COLUMNS:
            if col_name not in cols:
                try:
                    cursor.execute(f"ALTER TABLE hr_employees ADD COLUMN {col_name} {col_type}")
                    print(f"Added column {col_name}")
                except sqlite3.Error as e:
                    print(f"Error adding {col_name}: {e}")
            else:
                print(f"Column {col_name} ok")

    conn.commit()
    conn.close()

print("\n✓ Migration for all orgs complete")
