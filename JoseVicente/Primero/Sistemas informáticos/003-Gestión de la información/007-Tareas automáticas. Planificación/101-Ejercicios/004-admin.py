#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


CSV_FILENAME = "system_metrics.csv"


def parse_float(x, default=None):
    try:
        return float(x)
    except Exception:
        return default


def parse_time(s):
    # Expected: ISO like 2025-12-15T16:30:01
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def read_metrics(csv_path: Path):
    times, cpu, ram, disk = [], [], [], []

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = parse_time(row.get("timestamp", ""))
            c = parse_float(row.get("cpu_percent", ""), None)
            r = parse_float(row.get("ram_percent", ""), None)
            d = parse_float(row.get("disk_percent", ""), None)

            # Keep only valid rows
            if t is None or c is None or r is None or d is None:
                continue

            times.append(t)
            cpu.append(c)
            ram.append(r)
            disk.append(d)

    if not times:
        raise ValueError("No valid rows found in CSV (timestamp/cpu_percent/ram_percent/disk_percent).")

    return times, cpu, ram, disk


def draw_gauge(ax, value, label, vmin=0, vmax=100):
    """
    Simple semicircle gauge (0..100 by default).
    """
    ax.set_aspect("equal")
    ax.axis("off")

    # Clamp
    if value < vmin:
        value = vmin
    if value > vmax:
        value = vmax

    frac = (value - vmin) / (vmax - vmin) if vmax != vmin else 0.0
    angle = 180 * frac  # 0..180

    # Background arc
    bg = plt.matplotlib.patches.Wedge((0, 0), 1.0, 180, 0, width=0.25)
    ax.add_patch(bg)

    # Value arc
    fg = plt.matplotlib.patches.Wedge((0, 0), 1.0, 180, 180 - angle, width=0.25)
    ax.add_patch(fg)

    # Needle
    import math
    theta = math.radians(180 - angle)
    x = 0.85 * math.cos(theta)
    y = 0.85 * math.sin(theta)
    ax.plot([0, x], [0, y], linewidth=2)
    ax.scatter([0], [0], s=25)

    ax.text(0, -0.15, f"{value:.1f}%", ha="center", va="center", fontsize=14)
    ax.text(0, -0.38, label, ha="center", va="center", fontsize=11)


def format_time_axis(ax):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.grid(True, linestyle="--", linewidth=0.5)
    ax.tick_params(axis="x", rotation=0)


def main():
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / CSV_FILENAME

    times, cpu, ram, disk = read_metrics(csv_path)

    # Last row for gauges
    cpu_last, ram_last, disk_last = cpu[-1], ram[-1], disk[-1]
    last_time = times[-1].strftime("%Y-%m-%d %H:%M:%S")

    fig = plt.figure(figsize=(14, 7))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.2])

    # -------------------------
    # Row 1: Gauges
    # -------------------------
    ax_g1 = fig.add_subplot(gs[0, 0])
    ax_g2 = fig.add_subplot(gs[0, 1])
    ax_g3 = fig.add_subplot(gs[0, 2])

    draw_gauge(ax_g1, cpu_last, "CPU")
    draw_gauge(ax_g2, ram_last, "RAM")
    draw_gauge(ax_g3, disk_last, "DISK")

    fig.suptitle(f"System Metrics Dashboard (last sample: {last_time})", fontsize=14)

    # -------------------------
    # Row 2: Line charts
    # -------------------------
    ax_c = fig.add_subplot(gs[1, 0])
    ax_r = fig.add_subplot(gs[1, 1])
    ax_d = fig.add_subplot(gs[1, 2])

    ax_c.plot(times, cpu, linewidth=1.5)
    ax_c.set_title("CPU % over time")
    ax_c.set_ylim(0, 100)
    format_time_axis(ax_c)

    ax_r.plot(times, ram, linewidth=1.5)
    ax_r.set_title("RAM % over time")
    ax_r.set_ylim(0, 100)
    format_time_axis(ax_r)

    ax_d.plot(times, disk, linewidth=1.5)
    ax_d.set_title("Disk % over time")
    ax_d.set_ylim(0, 100)
    format_time_axis(ax_d)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

