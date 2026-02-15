#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canal -> SQLite (incremental, sin reprocesar)

Obtiene por vídeo:
1) título
2) descripción
3) thumbnail de mayor resolución disponible (URL y opcionalmente archivo)
4) id del vídeo
+ extras (SIN vistas): duración y fecha de publicación (si están disponibles)

Requisitos:
  pip install -U yt-dlp
  (o en Ubuntu: sudo apt install yt-dlp)

Notas:
- No usa API key de YouTube: se apoya en yt-dlp.
- Evita reprocesamiento: si el video_id ya existe en SQLite, lo salta.
  (Opcional: puedes forzar refresco poniendo FORCE_REFRESH=True)
"""

import json
import os
import sqlite3
import subprocess
import time
import urllib.request
from datetime import datetime
from typing import Any, Dict, Optional


# =========================
# CONFIG (editar aquí)
# =========================
CHANNEL_URL = "https://www.youtube.com/@dibujantes"

DB_PATH = "youtube_videos.sqlite"

SLEEP_BETWEEN_VIDEOS = 0.2  # segundos
MAX_VIDEOS = 0              # 0 = todos

DOWNLOAD_THUMBNAILS = True
THUMB_DIR = "thumbnails"

# Si True: re-descarga metadatos incluso si el vídeo ya está en DB.
# Si False: modo incremental (por defecto) -> NO reprocesa.
FORCE_REFRESH = False
# =========================


SCHEMA_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS videos (
  video_id          TEXT PRIMARY KEY,
  channel_url       TEXT NOT NULL,

  title             TEXT,
  description       TEXT,

  thumbnail_url     TEXT,
  thumbnail_path    TEXT,

  duration_seconds  INTEGER,   -- sin vistas
  upload_date       TEXT,      -- YYYYMMDD si yt-dlp lo provee

  added_at_utc      TEXT NOT NULL,
  updated_at_utc    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_videos_channel ON videos(channel_url);
"""


def run_yt_dlp_dump_json(url: str, flat: bool) -> Dict[str, Any]:
    cmd = ["yt-dlp", "-J", "--no-warnings", "--no-progress"]
    if flat:
        cmd += ["--flat-playlist"]
    cmd += [url]

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except FileNotFoundError:
        raise RuntimeError("No se encuentra 'yt-dlp'. Instálalo con: pip install -U yt-dlp")
    except subprocess.CalledProcessError as e:
        msg = e.output.decode("utf-8", errors="replace")
        raise RuntimeError(f"yt-dlp falló:\n{msg}")

    return json.loads(out.decode("utf-8", errors="replace"))


def pick_best_thumbnail(thumbnails: Any) -> Optional[str]:
    if not thumbnails or not isinstance(thumbnails, list):
        return None

    best_url = None
    best_area = -1

    for t in thumbnails:
        if not isinstance(t, dict):
            continue
        url = t.get("url")
        if not url:
            continue

        w = t.get("width")
        h = t.get("height")
        if isinstance(w, int) and isinstance(h, int) and w > 0 and h > 0:
            area = w * h
        else:
            area = 0

        if area > best_area:
            best_area = area
            best_url = url

    if best_url is None:
        for t in reversed(thumbnails):
            if isinstance(t, dict) and t.get("url"):
                return t["url"]
        return None

    return best_url


def download_file(url: str, dst_path: str, timeout: int = 30) -> None:
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r, open(dst_path, "wb") as f:
        f.write(r.read())


def ensure_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    return conn


def video_exists(conn: sqlite3.Connection, video_id: str) -> bool:
    cur = conn.execute("SELECT 1 FROM videos WHERE video_id = ? LIMIT 1", (video_id,))
    return cur.fetchone() is not None


def upsert_video(
    conn: sqlite3.Connection,
    channel_url: str,
    video_id: str,
    title: Optional[str],
    description: Optional[str],
    thumbnail_url: Optional[str],
    thumbnail_path: Optional[str],
    duration_seconds: Optional[int],
    upload_date: Optional[str],
) -> None:
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute(
        """
        INSERT INTO videos (
          video_id, channel_url,
          title, description,
          thumbnail_url, thumbnail_path,
          duration_seconds, upload_date,
          added_at_utc, updated_at_utc
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(video_id) DO UPDATE SET
          channel_url=excluded.channel_url,
          title=excluded.title,
          description=excluded.description,
          thumbnail_url=excluded.thumbnail_url,
          thumbnail_path=COALESCE(excluded.thumbnail_path, videos.thumbnail_path),
          duration_seconds=excluded.duration_seconds,
          upload_date=excluded.upload_date,
          updated_at_utc=excluded.updated_at_utc
        """,
        (
            video_id, channel_url,
            title, description,
            thumbnail_url, thumbnail_path,
            duration_seconds, upload_date,
            now, now
        ),
    )
    conn.commit()


def extract_video_id(entry: Dict[str, Any]) -> Optional[str]:
    vid = entry.get("id")
    if isinstance(vid, str) and vid.strip():
        return vid.strip()

    for k in ("webpage_url", "url"):
        v = entry.get(k)
        if isinstance(v, str) and "watch?v=" in v:
            try:
                return v.split("watch?v=", 1)[1].split("&", 1)[0]
            except Exception:
                pass
    return None


def main() -> int:
    conn = ensure_db(DB_PATH)

    # Listado rápido del canal
    data = run_yt_dlp_dump_json(CHANNEL_URL, flat=True)
    entries = data.get("entries") or []
    if not isinstance(entries, list) or not entries:
        print("No se encontraron vídeos (o el canal no es accesible).")
        return 2

    total = len(entries)
    limit = total if MAX_VIDEOS == 0 else min(MAX_VIDEOS, total)

    print(f"Canal: {CHANNEL_URL}")
    print(f"Vídeos encontrados: {total} | Procesando: {limit}")
    print(f"DB: {os.path.abspath(DB_PATH)}")
    print(f"Modo incremental (sin reprocesar): {not FORCE_REFRESH}")

    saved = 0
    skipped = 0
    errors = 0

    for idx, entry in enumerate(entries[:limit], start=1):
        if not isinstance(entry, dict):
            continue

        video_id = extract_video_id(entry)
        if not video_id:
            errors += 1
            print(f"[{idx}/{limit}] ERROR: no se pudo obtener video_id")
            continue

        # Evitar reprocesamiento
        if (not FORCE_REFRESH) and video_exists(conn, video_id):
            skipped += 1
            print(f"[{idx}/{limit}] SKIP {video_id} (ya en DB)")
            continue

        video_url = f"https://www.youtube.com/watch?v={video_id}"

        try:
            vdata = run_yt_dlp_dump_json(video_url, flat=False)
        except Exception as e:
            errors += 1
            print(f"[{idx}/{limit}] ERROR yt-dlp {video_id}: {e}")
            continue

        title = vdata.get("title")
        description = vdata.get("description")

        # Thumbnail mayor resolución
        thumb_url = pick_best_thumbnail(vdata.get("thumbnails")) or vdata.get("thumbnail")

        # Extras (sin vistas)
        duration_seconds = vdata.get("duration")
        if not isinstance(duration_seconds, int):
            duration_seconds = None

        upload_date = vdata.get("upload_date")
        if not isinstance(upload_date, str) or not upload_date.strip():
            upload_date = None

        thumb_path = None
        if DOWNLOAD_THUMBNAILS and thumb_url:
            os.makedirs(THUMB_DIR, exist_ok=True)
            thumb_path = os.path.join(THUMB_DIR, f"{video_id}.jpg")
            # Si ya existe el archivo, no lo re-descargamos
            if not os.path.exists(thumb_path):
                try:
                    download_file(thumb_url, thumb_path)
                except Exception as e:
                    print(f"[{idx}/{limit}] Aviso: no se pudo descargar thumbnail ({video_id}): {e}")
                    thumb_path = None

        upsert_video(
            conn=conn,
            channel_url=CHANNEL_URL,
            video_id=video_id,
            title=title,
            description=description,
            thumbnail_url=thumb_url,
            thumbnail_path=thumb_path,
            duration_seconds=duration_seconds,
            upload_date=upload_date,
        )

        saved += 1
        print(f"[{idx}/{limit}] OK {video_id} | {title!r}")

        if SLEEP_BETWEEN_VIDEOS > 0:
            time.sleep(SLEEP_BETWEEN_VIDEOS)

    print(f"Listo. Guardados/actualizados: {saved} | Saltados: {skipped} | Errores: {errors}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

