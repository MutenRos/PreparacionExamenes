#!/usr/bin/env python3
import subprocess
import json
import time
import os
from typing import Any, Dict, List, Optional

# =========================
# CONFIG
# =========================
CHANNEL_URL = "https://www.youtube.com/@screensaveryoutube/playlists"
OUT_JSON = "channel_playlists_with_videos.json"

THUMBS_DIR = "thumbnails"          # where thumbnails will be saved
SLEEP_BETWEEN_PLAYLISTS = 0.5      # seconds (politeness / rate-limit)
SLEEP_BETWEEN_THUMBS = 0.1         # seconds


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
    """
    Best-effort filtering for private/unavailable videos in flat playlist entries.
    Typical titles: 'Private video', '[Private video]', 'Deleted video', '[Deleted video]'
    Also filter items with missing id/url.
    """
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
        # sometimes flat entries put the id in "url"
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


def download_thumbnail(video_url: str, out_dir: str) -> Optional[str]:
    """
    Downloads the thumbnail for a video into out_dir.
    Returns the expected path if we can determine it, otherwise None.

    Uses yt-dlp (no API).
    """
    os.makedirs(out_dir, exist_ok=True)

    # We try to force a deterministic name:
    # - yt-dlp will write the thumbnail as "<output>.webp/jpg/..."
    # - %(id)s is stable; ext becomes the thumbnail ext (often webp)
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
        # Don’t crash the whole run for a thumbnail failure
        return None

    # We don’t know the exact extension in advance, so look for files starting with the id.
    # Extract id from URL (best effort)
    vid = None
    if "watch?v=" in video_url:
        vid = video_url.split("watch?v=", 1)[1].split("&", 1)[0].strip()

    if not vid:
        return None

    # Find any file with prefix vid. in out_dir
    for name in os.listdir(out_dir):
        if name.startswith(vid + "."):
            return os.path.join(out_dir, name)

    return None


# =========================
# Data extraction
# =========================
def get_playlists(channel_playlists_url: str) -> List[Dict[str, Any]]:
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

    # Keep only valid (id+url) after filtering
    videos = [x for x in videos if x.get("id") and x.get("url")]
    return videos


# =========================
# Main
# =========================
def main():
    os.makedirs(THUMBS_DIR, exist_ok=True)

    playlists = get_playlists(CHANNEL_URL)

    output: Dict[str, Any] = {
        "channel_playlists_url": CHANNEL_URL,
        "generated_at_epoch": int(time.time()),
        "playlists_count": len(playlists),
        "playlists": []
    }

    for i, p in enumerate(playlists, start=1):
        pl_url = p["url"]
        print(f"[{i}/{len(playlists)}] Fetching: {p.get('title')}")

        try:
            vids = get_videos_in_playlist(pl_url)
        except Exception as e:
            p_out = dict(p)
            p_out["error"] = str(e)
            p_out["videos_count"] = 0
            p_out["videos"] = []
            output["playlists"].append(p_out)
            continue

        # Download thumbnails + annotate JSON with local path
        for v in vids:
            thumb_path = download_thumbnail(v["url"], THUMBS_DIR)
            if thumb_path:
                v["thumbnail_file"] = thumb_path
            time.sleep(SLEEP_BETWEEN_THUMBS)

        p_out = dict(p)
        p_out["videos_count"] = len(vids)
        p_out["videos"] = vids
        output["playlists"].append(p_out)

        print(f"    -> {len(vids)} public videos (private/deleted excluded)")

        if SLEEP_BETWEEN_PLAYLISTS > 0:
            time.sleep(SLEEP_BETWEEN_PLAYLISTS)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSaved JSON: {OUT_JSON}")
    print(f"Saved thumbnails in: {THUMBS_DIR}/")


if __name__ == "__main__":
    main()

