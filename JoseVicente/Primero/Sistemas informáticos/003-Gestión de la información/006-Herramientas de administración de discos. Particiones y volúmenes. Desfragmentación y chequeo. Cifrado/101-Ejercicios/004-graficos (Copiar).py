#!/usr/bin/env python3
import json
import os
import stat
from pathlib import Path
from datetime import datetime

import paramiko
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TextColumn,
)

console = Console()


def print_banner() -> None:
    banner = r"""
      💾  Remote WWW Backup
      ─────────────────────
      🌐  Source : /var/www/html
      📁  Mode   : Recursive download
    """
    console.print(
        Panel.fit(
            banner,
            title="🚀 backup-www-html",
            border_style="cyan",
        )
    )


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_ssh_client(cfg: dict) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = cfg["host"]
    port = cfg.get("port", 22)
    username = cfg["username"]
    auth = cfg.get("auth", {})

    auth_type = auth.get("type", "password")

    if auth_type == "password":
        password = auth["password"]
        client.connect(hostname=host, port=port, username=username, password=password)
    elif auth_type == "key":
        key_filename = auth["key_filename"]
        passphrase = auth.get("passphrase")
        client.connect(
            hostname=host,
            port=port,
            username=username,
            key_filename=key_filename,
            passphrase=passphrase,
        )
    else:
        raise ValueError(f"Unsupported auth type: {auth_type}")

    return client


def is_dir(entry_attr) -> bool:
    return stat.S_ISDIR(entry_attr.st_mode)


def collect_files(sftp: paramiko.SFTPClient, root: str, rel: str = ""):
    """
    Returns a list of (remote_path, relative_path, size_in_bytes)
    """
    result = []

    current_remote = root if not rel else f"{root.rstrip('/')}/{rel}"
    try:
        entries = sftp.listdir_attr(current_remote)
    except IOError as e:
        console.print(f"[red]⚠️ Cannot list {current_remote}: {e}[/red]")
        return result

    for entry in entries:
        name = entry.filename
        entry_rel = name if not rel else f"{rel}/{name}"
        entry_remote = f"{root.rstrip('/')}/{entry_rel}"

        if is_dir(entry):
            # Recurse into directory
            result.extend(collect_files(sftp, root, entry_rel))
        else:
            size = entry.st_size
            result.append((entry_remote, entry_rel, size))

    return result


def ensure_local_root(base: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    local_root = base / timestamp
    local_root.mkdir(parents=True, exist_ok=True)
    return local_root


def print_summary_table(host: str, remote_root: str, local_root: Path, files_info):
    total_size = sum(size for _, _, size in files_info)
    total_mb = total_size / (1024 * 1024) if total_size else 0
    num_files = len(files_info)

    table = Table(title="📊 Backup summary (before download)", border_style="cyan")
    table.add_column("Item", style="bold magenta")
    table.add_column("Value", style="bold")

    table.add_row("🌐 Host", host)
    table.add_row("📂 Remote root", remote_root)
    table.add_row("💽 Local root", str(local_root))
    table.add_row("📄 Files to download", str(num_files))
    table.add_row("📦 Total size", f"{total_mb:.2f} MiB")

    console.print(table)


def main():
    print_banner()

    config = load_config("config.json")
    remote_root = config.get("remote_root", "/var/www/html/capitol").rstrip("/")
    local_base = Path(config.get("local_base", ".")).expanduser()

    console.print("[cyan]🔑 Connecting via SSH...[/cyan]")

    ssh = None
    sftp = None

    try:
        ssh = create_ssh_client(config)
        sftp = ssh.open_sftp()
        console.print("[green]✅ SSH connection established[/green]")

        console.print("[cyan]📂 Collecting file list from remote /var/www/html ...[/cyan]")
        files_info = collect_files(sftp, remote_root)

        if not files_info:
            console.print("[yellow]⚠️ No files found under /var/www/html[/yellow]")
            return

        local_root = ensure_local_root(local_base)

        print_summary_table(config["host"], remote_root, local_root, files_info)

        total_bytes = sum(size for _, _, size in files_info)

        console.print(
            Panel.fit(
                "⬇️  Starting download of remote contents...\n"
                "   Progress bar shows: [bytes], speed, elapsed, ETA, and %",
                border_style="green",
            )
        )

        # Progress bar configuration
        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            "[progress.percentage]{task.percentage:>5.1f}%",
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
            expand=True,
        )

        bytes_done_so_far = 0

        with progress:
            task_id = progress.add_task("💾 Downloading /var/www/html", total=total_bytes)

            for remote_path, rel_path, size in files_info:
                # Prepare local directory
                local_path = local_root / rel_path
                local_path.parent.mkdir(parents=True, exist_ok=True)

                file_offset = bytes_done_so_far

                def make_callback(offset, expected_total):
                    # expected_total is usually 'size', but we do not trust callback's total 100%.
                    def callback(transferred, total):
                        # total may be 0 or different; use expected_total if positive
                        effective_total = expected_total if expected_total > 0 else total
                        current_overall = offset + transferred
                        if effective_total > 0 and current_overall > (offset + effective_total):
                            # Clamp if overshoot
                            current_overall = offset + effective_total
                        progress.update(task_id, completed=current_overall)

                    return callback

                progress.console.log(f"📥 [bold]{rel_path}[/bold]")

                sftp.get(
                    remote_path,
                    str(local_path),
                    callback=make_callback(file_offset, size),
                )

                bytes_done_so_far += size

            # Ensure task completes exactly
            progress.update(task_id, completed=total_bytes)

        console.print(
            Panel.fit(
                f"✅ Backup completed successfully!\n\n"
                f"📂 Local folder: [bold]{local_root}[/bold]\n"
                f"🎉 All contents of /var/www/html have been downloaded.",
                title="Done",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(
            Panel.fit(
                f"❌ An error occurred:\n[red]{e}[/red]",
                title="Error",
                border_style="red",
            )
        )
    finally:
        if sftp is not None:
            sftp.close()
        if ssh is not None:
            ssh.close()
        console.print("[dim]🔌 Connections closed[/dim]")


if __name__ == "__main__":
    main()

