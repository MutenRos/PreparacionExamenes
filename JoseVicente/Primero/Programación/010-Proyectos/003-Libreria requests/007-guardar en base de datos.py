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

# Crawler limits
MAX_PAGES = 300
TIMEOUT = 12

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 (EmailCrawler)"
}

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# -----------------------------
# SQLite
# -----------------------------
def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS found_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            email TEXT NOT NULL,
            first_seen TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(url, email)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_found_emails_email ON found_emails(email)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_found_emails_url ON found_emails(url)")
    conn.commit()
    return conn

def save_emails(conn: sqlite3.Connection, url: str, title: str, emails: list[str]) -> int:
    # One row per email; avoid duplicates via UNIQUE(url,email) + INSERT OR IGNORE
    rows = [(url, title, e.strip().lower()) for e in emails if e and e.strip()]
    if not rows:
        return 0

    cur = conn.cursor()
    cur.executemany(
        "INSERT OR IGNORE INTO found_emails (url, title, email) VALUES (?, ?, ?)",
        rows
    )
    conn.commit()
    return cur.rowcount  # number of inserted rows (ignored duplicates not counted)

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

            inserted = save_emails(conn, final_url, title, emails)

            # Output: title + emails found (and how many new rows were inserted)
            print(f"\nPAGE: {final_url}")
            print(f"TITLE: {title}")
            if emails:
                print(f"EMAILS FOUND ({len(emails)}), NEW INSERTS ({inserted}):")
                for e in emails:
                    print(f" - {e}")
            else:
                print("EMAILS FOUND: (none)")

            # Queue internal links
            for href in hrefs:
                nxt = normalize_url(final_url, href)
                if not nxt:
                    continue
                if same_site(nxt, base_netloc) and nxt not in visited:
                    to_visit.append(nxt)

            pages_done += 1

            # Random delay 1..5 seconds between pages
            time.sleep(random.uniform(1, 2))

        except requests.RequestException:
            continue

if __name__ == "__main__":
    conn = init_db(DB_PATH)
    try:
        crawl_emails(START_URL, conn)
    finally:
        conn.close()
