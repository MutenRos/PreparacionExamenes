"""Check and create HR tables if needed."""
import sqlite3
from pathlib import Path

db_path = Path("/home/dario/src/org_1.db")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = {row[0] for row in cursor.fetchall()}

print(f"Existing tables: {sorted(tables)}")
print(f"\nHR tables exist: {'hr_employees' in tables}")

# Create HR tables if they don't exist
if 'hr_employees' not in tables:
    print("\nCreating HR tables...")
    
    # Create hr_jobs
    cursor.execute("""
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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES organizations(id)
        )
    """)
    
    # Create hr_positions
    cursor.execute("""
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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES organizations(id),
            FOREIGN KEY (job_id) REFERENCES hr_jobs(id)
        )
    """)
    
    # Create hr_employees
    cursor.execute("""
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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES organizations(id),
            FOREIGN KEY (position_id) REFERENCES hr_positions(id)
        )
    """)
    
    # Create hr_leave_requests
    cursor.execute("""
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES organizations(id),
            FOREIGN KEY (employee_id) REFERENCES hr_employees(id)
        )
    """)
    
    # Create hr_timesheets
    cursor.execute("""
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES organizations(id),
            FOREIGN KEY (employee_id) REFERENCES hr_employees(id)
        )
    """)
    
    # Create hr_timesheet_lines
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hr_timesheet_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            timesheet_id INTEGER NOT NULL,
            work_date DATE NOT NULL,
            project VARCHAR(100),
            task VARCHAR(255),
            hours DECIMAL(6, 2) NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES organizations(id),
            FOREIGN KEY (timesheet_id) REFERENCES hr_timesheets(id)
        )
    """)
    
    # Create hr_payroll_runs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hr_payroll_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            period_start DATE NOT NULL,
            period_end DATE NOT NULL,
            status VARCHAR(30) DEFAULT 'open',
            total_gross DECIMAL(14, 2) DEFAULT 0,
            total_net DECIMAL(14, 2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            posted_at TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES organizations(id)
        )
    """)
    
    # Create hr_payroll_lines
    cursor.execute("""
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES organizations(id),
            FOREIGN KEY (payroll_run_id) REFERENCES hr_payroll_runs(id),
            FOREIGN KEY (employee_id) REFERENCES hr_employees(id)
        )
    """)
    
    conn.commit()
    print("✓ HR tables created successfully!")
else:
    print("\nHR tables already exist.")

conn.close()
