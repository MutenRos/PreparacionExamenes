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
    # check_same_thread=False -> permitimos uso desde varios hilos (con lock)
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
# Crawler helpers
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
# Rate limiter por host
# -----------------------------
class RateLimiter:
    def __init__(self, min_interval_seconds: float):
        self.min_interval = float(min_interval_seconds)
        self._lock = threading.Lock()
        self._last = {}  # netloc -> last_time

    def wait(self, netloc: str):
        """Bloquea lo necesario para garantizar min_interval entre requests por netloc."""
        with self._lock:
            now = time.monotonic()
            last = self._last.get(netloc, 0.0)
            wait_s = (last + self.min_interval) - now
            if wait_s > 0:
                time.sleep(wait_s)
            self._last[netloc] = time.monotonic()

# -----------------------------
# Crawl paralelo
# -----------------------------
def crawl_emails_parallel(start_url: str, conn: sqlite3.Connection):
    base = urlparse(start_url)
    base_netloc = base.netloc

    visited = set()
    visited_lock = threading.Lock()

    q = deque([start_url])
    q_lock = threading.Lock()

    pages_done = 0
    pages_lock = threading.Lock()

    db_lock = threading.Lock()

    limiter = RateLimiter(MIN_SECONDS_PER_HOST)

    def worker():
        nonlocal pages_done

        # Session por hilo
        session = requests.Session()
        session.headers.update(HEADERS)

        while True:
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

            try:
                # respeta mínimo 1s por host
                limiter.wait(base_netloc)

                r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
                r.raise_for_status()

                final_url = r.url
                if not same_site(final_url, base_netloc):
                    continue

                title, hrefs, emails = extract_title_links_emails(r.text, r.content)

                with db_lock:
                    ins, upd = upsert_emails(conn, final_url, title, emails)

                print(f"\nPAGE: {final_url}")
                print(f"TITLE: {title}")
                if emails:
                    print(f"EMAILS FOUND ({len(emails)}), NEW ({ins}), SEEN BEFORE ({upd}):")
                    for e in emails:
                        print(f" - {e}")
                else:
                    print("EMAILS FOUND: (none)")

                # Encolar siguientes URLs
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

                # jitter opcional (sin bajar de 1s por host porque el limiter manda)
                time.sleep(random.uniform(0.0, 0.05))

            except requests.RequestException:
                continue

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(worker) for _ in range(MAX_WORKERS)]
        for f in futures:
            f.result()

if __name__ == "__main__":
    START_URL = input("Introduce página inicial: ").strip()
    conn = init_db(DB_PATH)
    try:
        crawl_emails_parallel(START_URL, conn)
    finally:
        conn.close()

