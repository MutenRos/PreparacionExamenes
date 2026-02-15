# pip3 install requests lxml --break-system-packages

import re
import time
import random
import sqlite3
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from lxml import html

START_URL = "https://tameformacion.com/"
DB_PATH = "emails_found.sqlite"

MAX_PAGES = 300
TIMEOUT = 12

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 (EmailCrawler)"
}

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# -----------------------------
# SQLite (dedupe ONLY by email)
# -----------------------------
def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
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
    """
    Returns (inserted_count, updated_count)
    - Insert: first time we see the email -> store url/title and timestamps
    - Update: already exists -> just bump last_seen (keeps the first url/title seen)
    """
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

    inserted = 0
    updated = 0

    # Insert new emails (ignore duplicates)
    cur.executemany(
        "INSERT OR IGNORE INTO found_emails (email, url, title) VALUES (?, ?, ?)",
        [(e, url, title) for e in norm]
    )
    inserted = cur.rowcount

    # For emails that already exist, update last_seen
    # (This will also update last_seen for newly inserted rows, which is fine)
    cur.executemany(
        "UPDATE found_emails SET last_seen = datetime('now') WHERE email = ?",
        [(e,) for e in norm]
    )
    updated = cur.rowcount - inserted  # approximate: rows touched that weren't new

    conn.commit()
    return (inserted, max(updated, 0))

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

def crawl_emails(start_url: str, conn: sqlite3.Connection):
    base = urlparse(start_url)
    base_netloc = base.netloc

    session = requests.Session()
    session.headers.update(HEADERS)

    visited = set()
    to_visit = [start_url]
    pages_done = 0

    while to_visit and pages_done < MAX_PAGES:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
            r.raise_for_status()

            final_url = r.url
            if not same_site(final_url, base_netloc):
                continue

            title, hrefs, emails = extract_title_links_emails(r.text, r.content)

            ins, upd = upsert_emails(conn, final_url, title, emails)

            print(f"\nPAGE: {final_url}")
            print(f"TITLE: {title}")
            if emails:
                print(f"EMAILS FOUND ({len(emails)}), NEW ({ins}), SEEN BEFORE ({upd}):")
                for e in emails:
                    print(f" - {e}")
            else:
                print("EMAILS FOUND: (none)")

            for href in hrefs:
                nxt = normalize_url(final_url, href)
                if not nxt:
                    continue
                if same_site(nxt, base_netloc) and nxt not in visited:
                    to_visit.append(nxt)

            pages_done += 1
            time.sleep(random.uniform(1, 1))

        except requests.RequestException:
            continue

if __name__ == "__main__":
    conn = init_db(DB_PATH)
    try:
        crawl_emails(START_URL, conn)
    finally:
        conn.close()

