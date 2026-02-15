#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sqlite3
import subprocess
import time
import urllib.request
from datetime import datetime
from typing import Any, Dict, Optional, List, Tuple


# =========================
# CONFIG
# =========================
CHANNEL_BASE = "https://www.youtube.com/@dibujantes"
CHANNEL_VIDEOS_URL = CHANNEL_BASE + "/videos"
CHANNEL_SHORTS_URL = CHANNEL_BASE + "/shorts"

DB_PATH = "youtube_videos.sqlite"

THUMB_DIR = "thumbnails"
DOWNLOAD_THUMBNAILS = True

SLEEP_BETWEEN_VIDEOS = 0.2
MAX_VIDEOS = 0      # 0 = todos
FORCE_REFRESH = False
# =========================


SCHEMA_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS videos (
  video_id            TEXT PRIMARY KEY,
  channel_url         TEXT NOT NULL,
  type                TEXT NOT NULL CHECK(type IN ('video','short')),

  title               TEXT,
  description         TEXT,

  thumbnail_url       TEXT,
  thumbnail_path      TEXT,
  thumbnail_local_url TEXT,

  duration_seconds    INTEGER,
  upload_date         TEXT,

  added_at_utc        TEXT NOT NULL,
  updated_at_utc      TEXT NOT NULL
);
"""


# ---------- yt-dlp helpers ----------

def run_yt_dlp_dump_json(url: str, flat: bool) -> Dict[str, Any]:
    cmd = ["yt-dlp", "-J", "--no-warnings", "--no-progress"]
    if flat:
        cmd.append("--flat-playlist")
    cmd.append(url)

    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    return json.loads(out.decode("utf-8", errors="replace"))


def extract_video_id(entry: Dict[str, Any]) -> Optional[str]:
    for k in ("webpage_url", "url"):
        v = entry.get(k)
        if isinstance(v, str) and "watch?v=" in v:
            return v.split("watch?v=", 1)[1].split("&", 1)[0]

    vid = entry.get("id")
    if isinstance(vid, str) and not vid.startswith("UC"):
        return vid
    return None


def collect_ids(url: str, kind: str) -> List[Tuple[str, str]]:
    data = run_yt_dlp_dump_json(url, flat=True)
    entries = data.get("entries") or []
    result = []

    for e in entries:
        if not isinstance(e, dict):
            continue
        vid = extract_video_id(e)
        if vid:
            result.append((vid, kind))

    return result


# ---------- thumbnails ----------

def pick_best_thumbnail(thumbnails: Any) -> Optional[str]:
    if not isinstance(thumbnails, list):
        return None

    best = None
    area = -1

    for t in thumbnails:
        if not isinstance(t, dict) or "url" not in t:
            continue
        w = t.get("width") or 0
        h = t.get("height") or 0
        if w * h >= area:
            area = w * h
            best = t["url"]

    return best


def download_file(url: str, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r, open(path, "wb") as f:
        f.write(r.read())


def file_url(path: str) -> str:
    return "file://" + os.path.abspath(path)


# ---------- DB ----------

def ensure_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    return conn


def exists(conn: sqlite3.Connection, vid: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM videos WHERE video_id=? LIMIT 1", (vid,)
    ).fetchone() is not None


def upsert(conn: sqlite3.Connection, row: dict):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute(
        """
        INSERT OR REPLACE INTO videos (
          video_id, channel_url, type,
          title, description,
          thumbnail_url, thumbnail_path, thumbnail_local_url,
          duration_seconds, upload_date,
          added_at_utc, updated_at_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row["video_id"], CHANNEL_BASE, row["type"],
            row["title"], row["description"],
            row["thumbnail_url"], row["thumbnail_path"], row["thumbnail_local_url"],
            row["duration_seconds"], row["upload_date"],
            now, now
        )
    )
    conn.commit()


# ---------- MAIN ----------

def main():
    conn = ensure_db()

    ids = []
    ids += collect_ids(CHANNEL_VIDEOS_URL, "video")
    ids += collect_ids(CHANNEL_SHORTS_URL, "short")

    # eliminar duplicados conservando tipo
    seen = {}
    for vid, kind in ids:
        if vid not in seen:
            seen[vid] = kind

    items = list(seen.items())
    total = len(items)

    print(f"Vídeos totales (vídeos + shorts): {total}")

    if DOWNLOAD_THUMBNAILS:
        os.makedirs(THUMB_DIR, exist_ok=True)

    for i, (vid, kind) in enumerate(items, 1):
        if not FORCE_REFRESH and exists(conn, vid):
            print(f"[{i}/{total}] SKIP {vid}")
            continue

        try:
            v = run_yt_dlp_dump_json(f"https://www.youtube.com/watch?v={vid}", flat=False)
        except Exception as e:
            print(f"[{i}/{total}] ERROR {vid}: {e}")
            continue

        thumb_url = pick_best_thumbnail(v.get("thumbnails")) or v.get("thumbnail")
        thumb_path = None
        thumb_local = None

        if DOWNLOAD_THUMBNAILS and thumb_url:
            thumb_path = os.path.join(THUMB_DIR, f"{vid}.jpg")
            if not os.path.exists(thumb_path):
                try:
                    download_file(thumb_url, thumb_path)
                except Exception as e:
                    print(f"[{i}/{total}] Aviso: no se pudo descargar thumbnail ({vid}): {e}")
                    thumb_path = None
            if thumb_path and os.path.exists(thumb_path):
                thumb_local = file_url(thumb_path)

        upsert(conn, {
            "video_id": vid,
            "type": kind,
            "title": v.get("title"),
            "description": v.get("description"),
            "thumbnail_url": thumb_url,
            "thumbnail_path": thumb_path,
            "thumbnail_local_url": thumb_local,
            "duration_seconds": v.get("duration"),
            "upload_date": v.get("upload_date"),
        })

        print(f"[{i}/{total}] OK {vid} ({kind})")

        if SLEEP_BETWEEN_VIDEOS:
            time.sleep(SLEEP_BETWEEN_VIDEOS)

    print("Finalizado correctamente.")


if __name__ == "__main__":
    main()

