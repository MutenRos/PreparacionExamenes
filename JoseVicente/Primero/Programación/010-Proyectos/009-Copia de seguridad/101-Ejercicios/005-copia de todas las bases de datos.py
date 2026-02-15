#!/usr/bin/env python3
"""
Backup all MySQL/MariaDB databases using mysqldump.

- User: copiadeseguridad
- Password: copiadeseguridad
- Creates one timestamped folder with one dump per DB.
- Excludes system DBs by default.

Requirements:
  - mysql client (for listing databases): `mysql`
  - mysqldump
  - gzip (optional, used here via Python gzip module, not external)

Run:
  python3 backup_mysql_all.py

Optional env vars:
  MYSQL_HOST (default: localhost)
  MYSQL_PORT (default: 3306)
  BACKUP_DIR (default: ./backups)
"""

from __future__ import annotations

import os
import sys
import gzip
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List


MYSQL_USER = "copiadeseguridad"
MYSQL_PASSWORD = "copiadeseguridad"

DEFAULT_EXCLUDE = {
    "information_schema",
    "performance_schema",
    "mysql",
    "sys",
}


def run(cmd: List[str], env: dict, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=check,
    )


def list_databases(host: str, port: int, env: dict) -> List[str]:
    # Use mysql client to list databases.
    cmd = [
        "mysql",
        f"--host={host}",
        f"--port={port}",
        f"--user={MYSQL_USER}",
        "-N",   # skip column names
        "-B",   # batch mode
        "-e",
        "SHOW DATABASES;",
    ]
    proc = run(cmd, env=env, check=True)
    dbs = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return dbs


def dump_database(db: str, host: str, port: int, env: dict, out_path_gz: Path) -> None:
    # Dump to stdout, gzip to file.
    cmd = [
        "mysqldump",
        f"--host={host}",
        f"--port={port}",
        f"--user={MYSQL_USER}",
        "--single-transaction",
        "--routines",
        "--triggers",
        "--events",
        "--hex-blob",
        "--databases",
        db,
    ]

    with subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,  # binary
    ) as p:
        assert p.stdout is not None
        assert p.stderr is not None

        with gzip.open(out_path_gz, "wb", compresslevel=6) as gz:
            shutil.copyfileobj(p.stdout, gz)

        stderr = p.stderr.read().decode("utf-8", errors="replace")
        rc = p.wait()
        if rc != 0:
            # Remove partial file
            try:
                out_path_gz.unlink(missing_ok=True)
            except Exception:
                pass
            raise RuntimeError(f"mysqldump failed for '{db}' (exit {rc}): {stderr.strip()}")


def main() -> int:
    host = os.environ.get("MYSQL_HOST", "localhost")
    port = int(os.environ.get("MYSQL_PORT", "3306"))
    backup_root = Path(os.environ.get("BACKUP_DIR", "./backups")).resolve()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_dir = backup_root / f"mysql_backup_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Avoid putting password on the command line: pass via env
    env = os.environ.copy()
    env["MYSQL_PWD"] = MYSQL_PASSWORD

    # Basic checks
    for bin_name in ("mysql", "mysqldump"):
        if shutil.which(bin_name) is None:
            print(f"ERROR: '{bin_name}' not found in PATH.", file=sys.stderr)
            return 2

    try:
        dbs = list_databases(host, port, env)
    except subprocess.CalledProcessError as e:
        print("ERROR listing databases.", file=sys.stderr)
        print(e.stderr.strip(), file=sys.stderr)
        return 3

    # Filter
    targets = [d for d in dbs if d not in DEFAULT_EXCLUDE]

    if not targets:
        print("No databases to backup (after exclusions).")
        return 0

    print(f"Backup folder: {out_dir}")
    print(f"Host: {host}:{port}")
    print(f"Databases ({len(targets)}): {', '.join(targets)}")

    ok = 0
    failed = 0

    for db in targets:
        out_file = out_dir / f"{db}.sql.gz"
        try:
            print(f"- Dumping {db} -> {out_file.name}")
            dump_database(db, host, port, env, out_file)
            ok += 1
        except Exception as ex:
            failed += 1
            print(f"  ERROR: {ex}", file=sys.stderr)

    print(f"Done. OK: {ok}, Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

