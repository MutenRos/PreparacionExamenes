# pip3 install requests lxml --break-system-packages

import re
import time
import random
import sqlite3
import threading
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from lxml import html
from concurrent.futures import ThreadPoolExecutor
import curses

DB_PATH = "emails_found.sqlite"

MAX_PAGES = 300
TIMEOUT = 12
MAX_WORKERS = 8
MIN_SECONDS_PER_HOST = 1.0

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 (EmailCrawler)"
}

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# -----------------------------
# SQLite (dedupe ONLY by email)
# -----------------------------
def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS found_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            url TEXT,
            title TEXT,
            first_seen TEXT NOT NULL DEFAULT (datetime('now')),
            last_seen  TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_found_emails_email ON found_emails(email)")
    conn.commit()
    return conn

def upsert_emails(conn: sqlite3.Connection, url: str, title: str, emails: list[str]) -> tuple[int, int]:
    norm = []
    for e in emails:
        if not e:
            continue
        e2 = e.strip().lower()
        if e2:
            norm.append(e2)

    if not norm:
        return (0, 0)

    cur = conn.cursor()
    cur.executemany(
        "INSERT OR IGNORE INTO found_emails (email, url, title) VALUES (?, ?, ?)",
        [(e, url, title) for e in norm]
    )
    inserted = cur.rowcount

    cur.executemany(
        "UPDATE found_emails SET last_seen = datetime('now') WHERE email = ?",
        [(e,) for e in norm]
    )
    updated = max(cur.rowcount - inserted, 0)

    conn.commit()
    return (inserted, updated)

# -----------------------------
# Helpers
# -----------------------------
def same_site(url: str, base_netloc: str) -> bool:
    try:
        u = urlparse(url)
        return u.scheme in ("http", "https") and u.netloc == base_netloc
    except Exception:
        return False

def normalize_url(current_url: str, href: str) -> str | None:
    if not href:
        return None
    href = href.strip()

    if href.startswith(("#", "javascript:", "mailto:", "tel:")):
        return None

    abs_url = urljoin(current_url, href)
    abs_url, _ = urldefrag(abs_url)

    if abs_url.endswith("/") and len(abs_url) > len("https://x/"):
        abs_url = abs_url[:-1]

    return abs_url

def extract_title_links_emails(response_text: str, response_bytes: bytes):
    try:
        tree = html.fromstring(response_bytes)
        title_list = tree.xpath("//title/text()")
        page_title = title_list[0].strip() if title_list else "(no title)"
        hrefs = tree.xpath("//a/@href")
    except Exception:
        page_title = "(no title)"
        hrefs = []

    emails = sorted(set(EMAIL_REGEX.findall(response_text)))
    return page_title, hrefs, emails

# -----------------------------
# Rate limiter per host
# -----------------------------
class RateLimiter:
    def __init__(self, min_interval_seconds: float):
        self.min_interval = float(min_interval_seconds)
        self._lock = threading.Lock()
        self._last = {}  # netloc -> last_time(monotonic)

    def wait(self, netloc: str):
        with self._lock:
            now = time.monotonic()
            last = self._last.get(netloc, 0.0)
            wait_s = (last + self.min_interval) - now
            if wait_s > 0:
                time.sleep(wait_s)
            self._last[netloc] = time.monotonic()

# -----------------------------
# Curses UI
# -----------------------------
def _safe_trim(s: str, width: int) -> str:
    if width <= 0:
        return ""
    return s if len(s) <= width else (s[: max(0, width - 1)] + "…")

def run_crawl_with_ui(stdscr, start_url: str):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)  # UI refresh ~10 fps

    base = urlparse(start_url)
    base_netloc = base.netloc

    conn = init_db(DB_PATH)
    db_lock = threading.Lock()

    visited = set()
    visited_lock = threading.Lock()

    q = deque([start_url])
    q_lock = threading.Lock()

    pages_done = 0
    pages_lock = threading.Lock()

    limiter = RateLimiter(MIN_SECONDS_PER_HOST)

    # slot status (one line each)
    status_lock = threading.Lock()
    status = [{
        "state": "idle",
        "url": "",
        "emails": 0,
        "ins": 0,
        "upd": 0,
        "err": ""
    } for _ in range(MAX_WORKERS)]

    stop_event = threading.Event()

    def set_status(slot: int, **kwargs):
        with status_lock:
            status[slot].update(kwargs)

    def worker(slot: int):
        nonlocal pages_done
        session = requests.Session()
        session.headers.update(HEADERS)

        while not stop_event.is_set():
            with pages_lock:
                if pages_done >= MAX_PAGES:
                    return

            with q_lock:
                if not q:
                    return
                url = q.popleft()

            with visited_lock:
                if url in visited:
                    continue
                visited.add(url)

            set_status(slot, state="wait", url=url, err="")

            try:
                limiter.wait(base_netloc)

                set_status(slot, state="fetch", url=url, err="")
                r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
                r.raise_for_status()

                final_url = r.url
                if not same_site(final_url, base_netloc):
                    set_status(slot, state="skip", url=final_url, err="off-site")
                    continue

                set_status(slot, state="parse", url=final_url, err="")
                title, hrefs, emails = extract_title_links_emails(r.text, r.content)

                with db_lock:
                    ins, upd = upsert_emails(conn, final_url, title, emails)

                set_status(slot, state="done", url=final_url, emails=len(emails), ins=ins, upd=upd, err="")

                new_links = []
                for href in hrefs:
                    nxt = normalize_url(final_url, href)
                    if not nxt:
                        continue
                    if same_site(nxt, base_netloc):
                        new_links.append(nxt)

                if new_links:
                    with q_lock:
                        q.extend(new_links)

                with pages_lock:
                    pages_done += 1

                time.sleep(random.uniform(0.0, 0.05))

            except requests.RequestException as e:
                set_status(slot, state="err", url=url, err=str(e)[:120])
                continue
            except Exception as e:
                set_status(slot, state="err", url=url, err=str(e)[:120])
                continue

    # start workers
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(worker, i) for i in range(MAX_WORKERS)]

        # UI loop
        while True:
            # key handling
            try:
                ch = stdscr.getch()
                if ch in (ord('q'), ord('Q')):
                    stop_event.set()
                    break
            except Exception:
                pass

            # check completion
            done_all = all(f.done() for f in futures)
            with pages_lock:
                pd = pages_done
            with q_lock:
                qlen = len(q)
            with visited_lock:
                vlen = len(visited)

            # draw
            stdscr.erase()
            h, w = stdscr.getmaxyx()

            header = f"EmailCrawler UI | workers={MAX_WORKERS} | pages_done={pd}/{MAX_PAGES} | queue={qlen} | visited={vlen} | q=quit"
            stdscr.addstr(0, 0, _safe_trim(header, w - 1))

            stdscr.addstr(1, 0, _safe_trim("-" * (w - 1), w - 1))

            with status_lock:
                snap = [dict(s) for s in status]

            # 8 slots
            for i in range(MAX_WORKERS):
                line = 2 + i
                if line >= h:
                    break
                s = snap[i]
                state = s["state"]
                url = s["url"]
                emails = s["emails"]
                ins = s["ins"]
                upd = s["upd"]
                err = s["err"]

                left = f"[{i}] {state:5} emails={emails:3} new={ins:3} old={upd:3} "
                right = url
                if err:
                    right = f"{url} | {err}"

                stdscr.addstr(line, 0, _safe_trim(left + right, w - 1))

            stdscr.refresh()

            if done_all:
                break

            time.sleep(0.1)

        # ensure stop and wait
        stop_event.set()
        for f in futures:
            try:
                f.result()
            except Exception:
                pass

    conn.close()

def main():
    start_url = input("Introduce página inicial: ").strip()
    curses.wrapper(run_crawl_with_ui, start_url)

if __name__ == "__main__":
    main()

