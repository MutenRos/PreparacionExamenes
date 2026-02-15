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
CHANNEL_PLAYLISTS_URL = CHANNEL_BASE + "/playlists"

DB_PATH = "youtube_videos.sqlite"

THUMB_DIR = "thumbnails"
DOWNLOAD_THUMBNAILS = True

SLEEP_BETWEEN_VIDEOS = 0.2
MAX_VIDEOS = 0      # 0 = todos (para videos+shorts)
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

CREATE TABLE IF NOT EXISTS playlists (
  playlist_id         TEXT PRIMARY KEY,
  channel_url         TEXT NOT NULL,

  title               TEXT,
  description         TEXT,

  thumbnail_url       TEXT,
  thumbnail_path      TEXT,
  thumbnail_local_url TEXT,

  entry_count         INTEGER,

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


def extract_playlist_id(entry: Dict[str, Any]) -> Optional[str]:
    # Typical forms:
    #  - https://www.youtube.com/playlist?list=PLxxxx
    #  - entry["id"] == "PLxxxx"
    for k in ("webpage_url", "url", "original_url"):
        v = entry.get(k)
        if isinstance(v, str) and "list=" in v:
            # keep only list param
            after = v.split("list=", 1)[1]
            pid = after.split("&", 1)[0]
            if pid:
                return pid

    pid = entry.get("id")
    if isinstance(pid, str):
        # playlists are usually PL / UU / OL / etc, but we accept any non-channel id
        if not pid.startswith("UC") and len(pid) >= 8:
            return pid
    return None


def collect_video_ids(url: str, kind: str) -> List[Tuple[str, str]]:
    data = run_yt_dlp_dump_json(url, flat=True)
    entries = data.get("entries") or []
    result: List[Tuple[str, str]] = []

    for e in entries:
        if not isinstance(e, dict):
            continue
        vid = extract_video_id(e)
        if vid:
            result.append((vid, kind))

    return result


def collect_playlist_ids(url: str) -> List[str]:
    data = run_yt_dlp_dump_json(url, flat=True)
    entries = data.get("entries") or []
    result: List[str] = []

    for e in entries:
        if not isinstance(e, dict):
            continue
        pid = extract_playlist_id(e)
        if pid:
            result.append(pid)

    # de-dup preserve order
    seen = set()
    out: List[str] = []
    for pid in result:
        if pid not in seen:
            seen.add(pid)
            out.append(pid)
    return out


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


def exists_video(conn: sqlite3.Connection, vid: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM videos WHERE video_id=? LIMIT 1", (vid,)
    ).fetchone() is not None


def exists_playlist(conn: sqlite3.Connection, pid: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM playlists WHERE playlist_id=? LIMIT 1", (pid,)
    ).fetchone() is not None


def upsert_video(conn: sqlite3.Connection, row: dict):
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
            row.get("title"), row.get("description"),
            row.get("thumbnail_url"), row.get("thumbnail_path"), row.get("thumbnail_local_url"),
            row.get("duration_seconds"), row.get("upload_date"),
            now, now
        )
    )
    conn.commit()


def upsert_playlist(conn: sqlite3.Connection, row: dict):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute(
        """
        INSERT OR REPLACE INTO playlists (
          playlist_id, channel_url,
          title, description,
          thumbnail_url, thumbnail_path, thumbnail_local_url,
          entry_count,
          added_at_utc, updated_at_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row["playlist_id"], CHANNEL_BASE,
            row.get("title"), row.get("description"),
            row.get("thumbnail_url"), row.get("thumbnail_path"), row.get("thumbnail_local_url"),
            row.get("entry_count"),
            now, now
        )
    )
    conn.commit()


# ---------- MAIN ----------

def main():
    conn = ensure_db()

    if DOWNLOAD_THUMBNAILS:
        os.makedirs(THUMB_DIR, exist_ok=True)

    # -------------------------
    # VIDEOS + SHORTS
    # -------------------------
    ids: List[Tuple[str, str]] = []
    ids += collect_video_ids(CHANNEL_VIDEOS_URL, "video")
    ids += collect_video_ids(CHANNEL_SHORTS_URL, "short")

    # eliminar duplicados conservando el primer tipo encontrado
    seen_vid: Dict[str, str] = {}
    for vid, kind in ids:
        if vid not in seen_vid:
            seen_vid[vid] = kind

    items = list(seen_vid.items())
    total = len(items)
    if MAX_VIDEOS and MAX_VIDEOS > 0:
        items = items[:MAX_VIDEOS]

    print(f"Vídeos totales (vídeos + shorts): {total}")
    if MAX_VIDEOS and MAX_VIDEOS > 0:
        print(f"Procesando (limitado por MAX_VIDEOS): {len(items)}")

    for i, (vid, kind) in enumerate(items, 1):
        if not FORCE_REFRESH and exists_video(conn, vid):
            print(f"[V {i}/{len(items)}] SKIP {vid}")
            continue

        try:
            v = run_yt_dlp_dump_json(f"https://www.youtube.com/watch?v={vid}", flat=False)
        except Exception as e:
            print(f"[V {i}/{len(items)}] ERROR {vid}: {e}")
            continue

        thumb_url = pick_best_thumbnail(v.get("thumbnails")) or v.get("thumbnail")
        thumb_path = None
        thumb_local = None

        if DOWNLOAD_THUMBNAILS and thumb_url:
            thumb_path = os.path.join(THUMB_DIR, "videos", f"{vid}.jpg")
            if not os.path.exists(thumb_path):
                download_file(thumb_url, thumb_path)
            thumb_local = file_url(thumb_path)

        upsert_video(conn, {
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

        print(f"[V {i}/{len(items)}] OK {vid} ({kind})")

        if SLEEP_BETWEEN_VIDEOS:
            time.sleep(SLEEP_BETWEEN_VIDEOS)

    # -------------------------
    # PLAYLISTS
    # -------------------------
    try:
        playlist_ids = collect_playlist_ids(CHANNEL_PLAYLISTS_URL)
    except Exception as e:
        print(f"[P] ERROR obteniendo playlists: {e}")
        playlist_ids = []

    print(f"Playlists totales: {len(playlist_ids)}")

    for i, pid in enumerate(playlist_ids, 1):
        if not FORCE_REFRESH and exists_playlist(conn, pid):
            print(f"[P {i}/{len(playlist_ids)}] SKIP {pid}")
            continue

        playlist_url = f"https://www.youtube.com/playlist?list={pid}"

        try:
            p = run_yt_dlp_dump_json(playlist_url, flat=False)
        except Exception as e:
            print(f"[P {i}/{len(playlist_ids)}] ERROR {pid}: {e}")
            continue

        thumb_url = pick_best_thumbnail(p.get("thumbnails")) or p.get("thumbnail")
        thumb_path = None
        thumb_local = None

        if DOWNLOAD_THUMBNAILS and thumb_url:
            thumb_path = os.path.join(THUMB_DIR, "playlists", f"{pid}.jpg")
            if not os.path.exists(thumb_path):
                download_file(thumb_url, thumb_path)
            thumb_local = file_url(thumb_path)

        entries = p.get("entries") or []
        entry_count = len(entries) if isinstance(entries, list) else None

        upsert_playlist(conn, {
            "playlist_id": pid,
            "title": p.get("title"),
            "description": p.get("description"),
            "thumbnail_url": thumb_url,
            "thumbnail_path": thumb_path,
            "thumbnail_local_url": thumb_local,
            "entry_count": entry_count,
        })

        print(f"[P {i}/{len(playlist_ids)}] OK {pid}")

        if SLEEP_BETWEEN_VIDEOS:
            time.sleep(SLEEP_BETWEEN_VIDEOS)

    print("Finalizado correctamente.")


if __name__ == "__main__":
    main()

