#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
raw_log_dump.py
Create a raw, concatenated dump of common Ubuntu logs and useful snapshots.
No parsing. Plain text. Good for later analysis.

Usage:
  sudo python3 raw_log_dump.py [-o raw_logs_dump.txt] [--since "YYYY-MM-DD HH:MM:SS"]

Notes:
  - Requires sudo to read some logs and run journalctl fully.
  - Handles rotated .gz logs.
  - Adds clear BEGIN/END headers for each source to keep provenance.
"""

import argparse
import datetime as dt
import gzip
import os
import io
from pathlib import Path
import subprocess
import sys
from typing import List, Tuple

DEF_OUTPUT = "raw_logs_dump.txt"

def try_run(cmd: List[str]) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", str(e)

def read_text(path: Path) -> str:
    try:
        if not path.exists():
            return ""
        if str(path).endswith(".gz"):
            with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
                return f.read()
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"[ERROR reading {path}: {e}]"

def write_block(fh, title: str, content: str):
    fh.write(f"\n===== BEGIN {title} =====\n")
    if content:
        fh.write(content.rstrip() + "\n")
    else:
        fh.write("[EMPTY]\n")
    fh.write(f"===== END {title} =====\n")

def dump_file_globs(fh, title: str, patterns: List[str]):
    # Gather and sort by filename so rotations appear together
    paths = []
    for pat in patterns:
        paths.extend(sorted(Path("/").glob(pat)))
    if not paths:
        write_block(fh, title, "[NO FILES MATCHED]")
        return
    for p in paths:
        write_block(fh, f"{title} :: {p}", read_text(p))

def dump_dir_listing(fh, title: str, directory: str):
    p = Path(directory)
    if not p.exists():
        write_block(fh, title, f"[MISSING DIR] {directory}")
        return
    try:
        items = []
        for child in sorted(p.glob("**/*")):
            try:
                mtime = dt.datetime.fromtimestamp(child.stat().st_mtime).isoformat(sep=" ", timespec="seconds")
            except Exception:
                mtime = "unknown"
            kind = "DIR " if child.is_dir() else "FILE"
            items.append(f"{kind} {mtime} {child}")
        write_block(fh, title, "\n".join(items))
    except Exception as e:
        write_block(fh, title, f"[ERROR listing {directory}: {e}]")

def dump_cmd(fh, title: str, cmd: List[str]):
    rc, out, err = try_run(cmd)
    body = out if out.strip() else ""
    if err.strip():
        body += ("\n[STDERR]\n" + err.strip() + "\n")
    if not body.strip():
        body = f"[NO OUTPUT] rc={rc}"
    write_block(fh, title + " :: " + " ".join(cmd), body)

def main():
    ap = argparse.ArgumentParser(description="Raw dump of Ubuntu logs into a single TXT.")
    ap.add_argument("-o", "--output", default=DEF_OUTPUT, help="Output TXT file")
    ap.add_argument("--since", default=None, help='Limit some command outputs, e.g., journalctl. Format: "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"')
    args = ap.parse_args()

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with io.open(args.output, "w", encoding="utf-8") as fh:
        fh.write("# RAW LOGS DUMP — Ubuntu Server\n")
        fh.write(f"Generated: {now}\n\n")

        # --- Basic system snapshots ---
        dump_cmd(fh, "hostnamectl", ["hostnamectl"])
        dump_cmd(fh, "os-release", ["bash", "-lc", "cat /etc/os-release || true"])
        dump_cmd(fh, "uname", ["uname", "-a"])
        dump_cmd(fh, "timedatectl", ["timedatectl"])
        dump_cmd(fh, "packages snapshot", ["dpkg", "-l"])
        dump_cmd(fh, "snap changes", ["bash", "-lc", "command -v snap >/dev/null 2>&1 && snap changes || echo 'snap not installed'"])
        dump_cmd(fh, "enabled services", ["systemctl", "list-unit-files", "--type=service", "--state=enabled", "--no-pager"])
        dump_cmd(fh, "failed services", ["systemctl", "--failed", "--no-pager"])
        dump_cmd(fh, "timers", ["systemctl", "list-timers", "--all", "--no-pager"])
        dump_cmd(fh, "UFW status", ["bash", "-lc", "command -v ufw >/dev/null 2>&1 && ufw status verbose || echo 'ufw not installed'"])
        dump_cmd(fh, "network (ip a)", ["ip", "a"])
        dump_cmd(fh, "routes (ip r)", ["ip", "r"])

        # --- Journald (current boot & recent history) ---
        j_since = []
        if args.since:
            j_since = ["--since", args.since]

        dump_cmd(fh, "journalctl current boot", ["journalctl", "-b", "-o", "short-iso", "--no-pager"] + j_since)
        dump_cmd(fh, "journalctl ufw", ["bash", "-lc", "journalctl -t ufw -o short-iso --no-pager " + (f"--since '{args.since}'" if args.since else "")])
        dump_cmd(fh, "journalctl apt/dpkg", ["bash", "-lc", "journalctl -o short-iso --no-pager | egrep -i ' apt | dpkg ' || true"])

        # --- Classic log files (rotated included) ---
        dump_file_globs(fh, "APT history", ["var/log/apt/history.log*", "var/log/apt/term.log*"])
        dump_file_globs(fh, "DPKG log", ["var/log/dpkg.log*"])
        dump_file_globs(fh, "Unattended upgrades", ["var/log/unattended-upgrades/unattended-upgrades*.log*"])
        dump_file_globs(fh, "Auth log", ["var/log/auth.log*"])
        dump_file_globs(fh, "Syslog", ["var/log/syslog*", "var/log/kern.log*"])
        dump_file_globs(fh, "Installer log", ["var/log/installer/syslog*", "var/log/installer/partman*"])
        dump_file_globs(fh, "Cloud-init", ["var/log/cloud-init.log*", "var/log/cloud-init-output.log*"])
        dump_file_globs(fh, "Bootstrap (dmesg)", ["var/log/dmesg*", "/var/log/boot.log*"])

        # --- Config snapshots (helpful context) ---
        dump_file_globs(fh, "Netplan YAML", ["etc/netplan/*.yaml"])
        dump_file_globs(fh, "UFW rules files", ["etc/ufw/*"])
        dump_file_globs(fh, "Cron system", ["etc/crontab", "etc/cron.*/*"])
        dump_cmd(fh, "User crontab (root)", ["bash", "-lc", "crontab -l 2>&1 || true"])

        # --- Users / groups / sudoers ---
        dump_file_globs(fh, "passwd/group", ["etc/passwd", "etc/group"])
        dump_file_globs(fh, "sudoers", ["etc/sudoers", "etc/sudoers.d/*"])

        # --- SSH config & known_hosts (paths only, no private keys) ---
        dump_file_globs(fh, "SSH server config", ["etc/ssh/sshd_config", "etc/ssh/sshd_config.d/*"])
        dump_dir_listing(fh, "SSH client dir listing", "/root/.ssh")
        dump_dir_listing(fh, "SSH client dir listing (all users)", "/home")

        # --- Bash history (raw) ---
        # Root
        bh = Path("/root/.bash_history")
        if bh.exists():
            write_block(fh, "Bash history :: /root/.bash_history", read_text(bh))
        # Per-user
        for home in Path("/home").glob("*"):
            h = home / ".bash_history"
            if h.exists():
                write_block(fh, f"Bash history :: {h}", read_text(h))

        # --- Last logins ---
        dump_cmd(fh, "last -F", ["last", "-F"])
        dump_cmd(fh, "lastlog", ["lastlog"])

    print(f"Wrote: {Path(args.output).resolve()}")

if __name__ == "__main__":
    main()

