#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


# Soporta common/combined:
# 127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "referer" "ua"
LOG_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<dt>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+)(?: \S+)?" '
    r'(?P<status>\d{3}) (?P<size>\S+)'
    r'(?: "(?P<referer>[^"]*)" "(?P<ua>[^"]*)")?$'
)

APACHE_DT_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


def parse_line(line: str):
    m = LOG_RE.match(line)
    if not m:
        return None

    gd = m.groupdict()

    # datetime
    try:
        dt = datetime.strptime(gd["dt"], APACHE_DT_FORMAT)
    except Exception:
        return None

    # size puede ser "-"
    size_raw = gd.get("size", "-")
    try:
        size = int(size_raw) if size_raw != "-" else 0
    except Exception:
        size = 0

    return {
        "ip": gd["ip"],
        "dt": dt,
        "method": gd["method"],
        "path": gd["path"],
        "status": int(gd["status"]),
        "size": size,
        "referer": gd.get("referer") or "",
        "ua": gd.get("ua") or "",
    }


def simplify_path(path: str) -> str:
    """
    Reduce ruido:
    - Quita query string
    - Quita fragment
    - Normaliza vacío
    """
    path = path.split("?", 1)[0].split("#", 1)[0]
    return path if path else "/"


def load_log(log_path: Path, max_lines: int | None = None):
    total = 0
    parsed = 0
    bad = 0

    per_hour = Counter()          # 0..23
    per_day = Counter()           # YYYY-MM-DD
    per_status = Counter()        # 200, 404...
    per_method = Counter()        # GET/POST...
    per_path = Counter()          # top URLs
    per_ip = Counter()            # top IPs
    bytes_per_hour = Counter()    # bytes por hora (0..23)
    status_by_hour = defaultdict(Counter)  # hour -> Counter(status_class)

    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            total += 1
            if max_lines and total > max_lines:
                break

            rec = parse_line(line.rstrip("\n"))
            if not rec:
                bad += 1
                continue

            parsed += 1
            dt = rec["dt"]
            hour = dt.hour
            day = dt.date().isoformat()

            per_hour[hour] += 1
            per_day[day] += 1
            per_status[rec["status"]] += 1
            per_method[rec["method"]] += 1

            p = simplify_path(rec["path"])
            per_path[p] += 1
            per_ip[rec["ip"]] += 1

            bytes_per_hour[hour] += rec["size"]

            cls = f"{rec['status'] // 100}xx"
            status_by_hour[hour][cls] += 1

    return {
        "total_lines": total,
        "parsed": parsed,
        "bad": bad,
        "per_hour": per_hour,
        "per_day": per_day,
        "per_status": per_status,
        "per_method": per_method,
        "per_path": per_path,
        "per_ip": per_ip,
        "bytes_per_hour": bytes_per_hour,
        "status_by_hour": status_by_hour,
    }


def plot_grid(stats, out_path: Path | None = None, top_n: int = 10):
    plt.figure(figsize=(16, 10))

    # --- 1) Accesos por hora (principal) ---
    ax1 = plt.subplot(2, 3, 1)
    hours = list(range(24))
    vals = [stats["per_hour"].get(h, 0) for h in hours]
    ax1.plot(hours, vals, marker="o")
    ax1.set_title("Accesos por hora (0–23)")
    ax1.set_xlabel("Hora")
    ax1.set_ylabel("Nº accesos")
    ax1.set_xticks(hours)
    ax1.grid(True, alpha=0.3)

    # --- 2) Accesos por día ---
    ax2 = plt.subplot(2, 3, 2)
    days_sorted = sorted(stats["per_day"].items(), key=lambda x: x[0])
    if days_sorted:
        x = list(range(len(days_sorted)))
        y = [v for _, v in days_sorted]
        ax2.plot(x, y, marker="o")
        ax2.set_title("Accesos por día")
        ax2.set_xlabel("Día (ordenado)")
        ax2.set_ylabel("Nº accesos")
        ax2.grid(True, alpha=0.3)
        # Etiquetas si no hay demasiados días
        if len(days_sorted) <= 20:
            ax2.set_xticks(x)
            ax2.set_xticklabels([d for d, _ in days_sorted], rotation=45, ha="right")
        else:
            ax2.set_xticks([])
    else:
        ax2.set_title("Accesos por día (sin datos)")

    # --- 3) Status codes (Top) ---
    ax3 = plt.subplot(2, 3, 3)
    status_sorted = stats["per_status"].most_common(10)
    if status_sorted:
        labels = [str(k) for k, _ in status_sorted]
        y = [v for _, v in status_sorted]
        ax3.bar(labels, y)
        ax3.set_title("Códigos de estado (Top 10)")
        ax3.set_xlabel("Status")
        ax3.set_ylabel("Nº accesos")
        ax3.grid(True, axis="y", alpha=0.3)
    else:
        ax3.set_title("Códigos de estado (sin datos)")

    # --- 4) Métodos HTTP ---
    ax4 = plt.subplot(2, 3, 4)
    meth_sorted = stats["per_method"].most_common()
    if meth_sorted:
        labels = [k for k, _ in meth_sorted]
        y = [v for _, v in meth_sorted]
        ax4.bar(labels, y)
        ax4.set_title("Métodos HTTP")
        ax4.set_xlabel("Método")
        ax4.set_ylabel("Nº accesos")
        ax4.grid(True, axis="y", alpha=0.3)
    else:
        ax4.set_title("Métodos HTTP (sin datos)")

    # --- 5) Top URLs ---
    ax5 = plt.subplot(2, 3, 5)
    top_paths = stats["per_path"].most_common(top_n)
    if top_paths:
        labels = [p for p, _ in top_paths]
        y = [v for _, v in top_paths]
        ax5.barh(list(reversed(labels)), list(reversed(y)))
        ax5.set_title(f"Top {top_n} URLs (sin query)")
        ax5.set_xlabel("Nº accesos")
        ax5.grid(True, axis="x", alpha=0.3)
    else:
        ax5.set_title("Top URLs (sin datos)")

    # --- 6) Tráfico (bytes) por hora ---
    ax6 = plt.subplot(2, 3, 6)
    bytes_vals = [stats["bytes_per_hour"].get(h, 0) for h in hours]
    ax6.plot(hours, bytes_vals, marker="o")
    ax6.set_title("Bytes servidos por hora (0–23)")
    ax6.set_xlabel("Hora")
    ax6.set_ylabel("Bytes")
    ax6.set_xticks(hours)
    ax6.grid(True, alpha=0.3)

    plt.suptitle(
        f"Apache log: líneas={stats['total_lines']}, parseadas={stats['parsed']}, no parseadas={stats['bad']}",
        y=1.02
    )
    plt.tight_layout()

    if out_path:
        plt.savefig(out_path, dpi=150, bbox_inches="tight")

    plt.show()


def main():
    ap = argparse.ArgumentParser(description="Genera un grid de gráficas a partir de un access.log de Apache.")
    ap.add_argument("logfile", nargs="?", default="beige-access.log", help="Ruta al log de Apache")
    ap.add_argument("--out", default="apache_graficas.png", help="PNG de salida")
    ap.add_argument("--top", type=int, default=10, help="Top N URLs a mostrar")
    ap.add_argument("--max-lines", type=int, default=0, help="Procesa solo N líneas (0 = todas)")
    args = ap.parse_args()

    log_path = Path(args.logfile)
    if not log_path.exists():
        raise SystemExit(f"No existe el archivo: {log_path}")

    max_lines = args.max_lines if args.max_lines and args.max_lines > 0 else None
    stats = load_log(log_path, max_lines=max_lines)
    plot_grid(stats, out_path=Path(args.out), top_n=args.top)


if __name__ == "__main__":
    main()

