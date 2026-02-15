#!/usr/bin/env python3
import subprocess
import json
import time
import os
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

# =========================
# CONFIG
# =========================
CHANNEL_URL = "https://www.youtube.com/@screensaveryoutube/playlists"
OUT_JSON = "channel_playlists_with_videos.json"

THUMBS_DIR = "thumbnails"                # video thumbs
PLAYLIST_THUMBS_DIR = "playlist_thumbnails"  # playlist thumbs

SLEEP_BETWEEN_PLAYLISTS = 0.5
SLEEP_BETWEEN_THUMBS = 0.1


# =========================
# yt-dlp helpers
# =========================
def run_ytdlp_json(url: str, flat: bool = True) -> Dict[str, Any]:
    cmd = ["yt-dlp", "--dump-single-json", "--no-warnings"]
    if flat:
        cmd.append("--flat-playlist")
    cmd.append(url)

    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if res.returncode != 0:
        raise RuntimeError(f"yt-dlp failed for URL: {url}\n\nSTDERR:\n{res.stderr.strip()}")

    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Failed to parse yt-dlp JSON for URL: {url}\n\nError: {e}\n\nRaw output head:\n{res.stdout[:800]}"
        )


def is_private_video_entry(v: Dict[str, Any]) -> bool:
    title = (v.get("title") or "").strip().lower()
    if title in {"private video", "[private video]", "deleted video", "[deleted video]"}:
        return True
    if not (v.get("id") or v.get("url")):
        return True
    return False


def normalize_video_url(v: Dict[str, Any]) -> Optional[str]:
    vid = v.get("id")
    vurl = v.get("url")

    if isinstance(vurl, str) and vurl.startswith("http"):
        return vurl
    if isinstance(vid, str) and vid:
        return f"https://www.youtube.com/watch?v={vid}"
    if isinstance(vurl, str) and vurl:
        return f"https://www.youtube.com/watch?v={vurl}"
    return None


def normalize_playlist_url(entry: Dict[str, Any]) -> Optional[str]:
    pid = entry.get("id")
    url = entry.get("url")
    if isinstance(url, str) and url.startswith("http"):
        return url
    if isinstance(pid, str) and pid:
        return f"https://www.youtube.com/playlist?list={pid}"
    return None


def _pick_best_thumbnail_url(thumbnails: Any) -> Optional[str]:
    """
    thumbnails can be a list of dicts like: [{"url": "...", "width":..., "height":...}, ...]
    choose the largest by area, fallback to last with url.
    """
    if not isinstance(thumbnails, list) or not thumbnails:
        return None
    best: Tuple[int, str] = (-1, "")
    for t in thumbnails:
        if not isinstance(t, dict):
            continue
        url = t.get("url")
        if not isinstance(url, str) or not url:
            continue
        w = t.get("width") or 0
        h = t.get("height") or 0
        area = 0
        if isinstance(w, int) and isinstance(h, int) and w > 0 and h > 0:
            area = w * h
        # If no dims, treat as small but valid
        if area > best[0]:
            best = (area, url)
    return best[1] if best[1] else None


def _guess_ext_from_url(url: str) -> str:
    # Very simple: look at path ending; otherwise default jpg
    lower = url.lower().split("?", 1)[0]
    for ext in (".webp", ".jpg", ".jpeg", ".png"):
        if lower.endswith(ext):
            return ext.lstrip(".")
    return "jpg"


def download_url_to_file(url: str, out_path: str) -> bool:
    try:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(out_path, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False


def download_thumbnail(video_url: str, out_dir: str) -> Optional[str]:
    """
    Downloads the thumbnail for a video into out_dir using yt-dlp.
    Returns the saved file path if found, otherwise None.
    """
    os.makedirs(out_dir, exist_ok=True)

    out_tmpl = os.path.join(out_dir, "%(id)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-thumbnail",
        "--no-warnings",
        "-o", out_tmpl,
        video_url
    ]

    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if res.returncode != 0:
        return None

    vid = None
    if "watch?v=" in video_url:
        vid = video_url.split("watch?v=", 1)[1].split("&", 1)[0].strip()

    if not vid:
        return None

    for name in os.listdir(out_dir):
        if name.startswith(vid + "."):
            return os.path.join(out_dir, name)

    return None


# =========================
# Data extraction
# =========================
def get_playlists_flat(channel_playlists_url: str) -> List[Dict[str, Any]]:
    data = run_ytdlp_json(channel_playlists_url, flat=True)

    playlists: List[Dict[str, Any]] = []
    for entry in data.get("entries", []) or []:
        pl_url = normalize_playlist_url(entry)
        if not pl_url:
            continue
        playlists.append({
            "id": entry.get("id"),
            "title": entry.get("title"),
            "url": pl_url,
        })
    return playlists


def enrich_playlist_metadata(p: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch full playlist metadata (non-flat) to get description + thumbnails.
    Then download playlist thumbnail into PLAYLIST_THUMBS_DIR.
    """
    pl_url = (p.get("url") or "").strip()
    if not pl_url:
        return p

    try:
        meta = run_ytdlp_json(pl_url, flat=False)
    except Exception as e:
        p2 = dict(p)
        p2["meta_error"] = str(e)
        return p2

    desc = meta.get("description") or meta.get("playlist_description") or ""
    thumbs = meta.get("thumbnails") or meta.get("thumbnail") or None
    # meta["thumbnail"] is often a string; normalize to list
    thumb_url = None
    if isinstance(thumbs, list):
        thumb_url = _pick_best_thumbnail_url(thumbs)
    elif isinstance(thumbs, str) and thumbs:
        thumb_url = thumbs

    p2 = dict(p)
    p2["description"] = desc if isinstance(desc, str) else ""

    # Download playlist thumbnail if we got a URL
    if thumb_url and isinstance(p2.get("id"), str) and p2["id"]:
        ext = _guess_ext_from_url(thumb_url)
        out_rel = os.path.join(PLAYLIST_THUMBS_DIR, f"{p2['id']}.{ext}")
        ok = download_url_to_file(thumb_url, out_rel)
        if ok:
            p2["thumbnail_file"] = out_rel

    return p2


def get_videos_in_playlist(playlist_url: str) -> List[Dict[str, Any]]:
    data = run_ytdlp_json(playlist_url, flat=True)

    videos: List[Dict[str, Any]] = []
    for v in data.get("entries", []) or []:
        if is_private_video_entry(v):
            continue

        video_url = normalize_video_url(v)
        if not video_url:
            continue

        vid = v.get("id") or v.get("url")
        videos.append({
            "id": vid,
            "title": v.get("title"),
            "url": video_url,
        })

    videos = [x for x in videos if x.get("id") and x.get("url")]
    return videos


# =========================
# Main
# =========================
def main():
    os.makedirs(THUMBS_DIR, exist_ok=True)
    os.makedirs(PLAYLIST_THUMBS_DIR, exist_ok=True)

    playlists = get_playlists_flat(CHANNEL_URL)

    output: Dict[str, Any] = {
        "channel_playlists_url": CHANNEL_URL,
        "generated_at_epoch": int(time.time()),
        "playlists_count": len(playlists),
        "playlists": []
    }

    for i, p in enumerate(playlists, start=1):
        print(f"[{i}/{len(playlists)}] Enriching playlist: {p.get('title')}")
        p_enriched = enrich_playlist_metadata(p)

        pl_url = p_enriched.get("url") or p.get("url") or ""
        if not pl_url:
            p_out = dict(p_enriched)
            p_out["videos_count"] = 0
            p_out["videos"] = []
            output["playlists"].append(p_out)
            continue

        try:
            vids = get_videos_in_playlist(pl_url)
        except Exception as e:
            p_out = dict(p_enriched)
            p_out["error"] = str(e)
            p_out["videos_count"] = 0
            p_out["videos"] = []
            output["playlists"].append(p_out)
            continue

        # Download video thumbnails + annotate JSON
        for v in vids:
            thumb_path = download_thumbnail(v["url"], THUMBS_DIR)
            if thumb_path:
                v["thumbnail_file"] = thumb_path
            time.sleep(SLEEP_BETWEEN_THUMBS)

        p_out = dict(p_enriched)
        p_out["videos_count"] = len(vids)
        p_out["videos"] = vids
        output["playlists"].append(p_out)

        print(f"    -> {len(vids)} public videos (private/deleted excluded)")

        if SLEEP_BETWEEN_PLAYLISTS > 0:
            time.sleep(SLEEP_BETWEEN_PLAYLISTS)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSaved JSON: {OUT_JSON}")
    print(f"Saved video thumbnails in: {THUMBS_DIR}/")
    print(f"Saved playlist thumbnails in: {PLAYLIST_THUMBS_DIR}/")


if __name__ == "__main__":
    main()

