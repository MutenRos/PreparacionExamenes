#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
from datetime import datetime
from pathlib import Path

import psutil


TARGET_DEVICE = "/dev/nvme0n1p2"  # the disk device you want to track


def find_mountpoint_for_device(device: str) -> str | None:
    """
    Return the mountpoint for a given device (e.g., /dev/nvme0n1p2), or None if not found.
    """
    try:
        for p in psutil.disk_partitions(all=False):
            if p.device == device:
                return p.mountpoint
    except Exception:
        pass
    return None


def get_metrics() -> dict:
    # Timestamp
    ts = datetime.now().isoformat(timespec="seconds")

    # CPU
    # load averages are system-wide and match "uptime" style (1m, 5m, 15m)
    try:
        load1, load5, load15 = os.getloadavg()
    except Exception:
        load1 = load5 = load15 = ""

    # CPU percent (instant sample; cron interval is 60s anyway)
    cpu_percent = psutil.cpu_percent(interval=0.2)

    # RAM
    vm = psutil.virtual_memory()
    ram_percent = vm.percent
    ram_used_mb = int(vm.used / (1024 * 1024))
    ram_total_mb = int(vm.total / (1024 * 1024))

    # Disk: try to locate mountpoint for the device, otherwise use "/"
    mountpoint = find_mountpoint_for_device(TARGET_DEVICE) or "/"
    du = psutil.disk_usage(mountpoint)

    disk_percent = du.percent
    disk_used_gb = round(du.used / (1024 ** 3), 2)
    disk_total_gb = round(du.total / (1024 ** 3), 2)
    disk_free_gb = round(du.free / (1024 ** 3), 2)

    return {
        "timestamp": ts,
        "load1": load1,
        "load5": load5,
        "load15": load15,
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent,
        "ram_used_mb": ram_used_mb,
        "ram_total_mb": ram_total_mb,
        "disk_device": TARGET_DEVICE,
        "disk_mountpoint": mountpoint,
        "disk_percent": disk_percent,
        "disk_used_gb": disk_used_gb,
        "disk_free_gb": disk_free_gb,
        "disk_total_gb": disk_total_gb,
    }


def main():
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "system_metrics.csv"

    fieldnames = [
        "timestamp",
        "load1", "load5", "load15",
        "cpu_percent",
        "ram_percent", "ram_used_mb", "ram_total_mb",
        "disk_device", "disk_mountpoint",
        "disk_percent", "disk_used_gb", "disk_free_gb", "disk_total_gb",
    ]

    row = get_metrics()

    file_exists = csv_path.exists()

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()

