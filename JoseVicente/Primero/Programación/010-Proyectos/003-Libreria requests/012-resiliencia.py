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

TIMEOUT = 12
MAX_WORKERS = 8
MIN_SECONDS_PER_HOST = 1.0

# Runs until queue is empty (or q)
# Safety caps so it doesn't explode:
MAX_PAGES_PER_DOMAIN = 500          # per base domain (subdomains included)
MAX_QUEUE_SIZE = 20000              # cap queued URLs in memory
MAX_LINKS_ENQUEUE_PER_PAGE = 500    # cap links added from a single page

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
def canon_host(netloc: str) -> str:
    netloc = (netloc or "").strip().lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc

COMMON_PUBLIC_SUFFIX_2LEVEL = {
    "co.uk", "org.uk", "ac.uk",
    "com.au", "net.au", "org.au",
    "co.nz", "org.nz",
    "com.br", "com.ar", "com.mx",
    "co.jp", "or.jp",
    "com.tr", "com.pl",
}

def base_domain_from_host(host: str) -> str:
    host = canon_host(host)
    parts = [p for p in host.split(".") if p]
    if len(parts) <= 2:
        return host
    suffix2 = ".".join(parts[-2:])
    if suffix2 in COMMON_PUBLIC_SUFFIX_2LEVEL:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])

def url_host(url: str) -> str:
    return canon_host(urlparse(url).netloc)

def url_base_domain(url: str) -> str:
    return base_domain_from_host(url_host(url))

def is_http_url(url: str) -> bool:
    try:
        u = urlparse(url)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False

def is_blocked_domain(url: str) -> bool:
    """Block google.com and any subdomain of google.com (initial URL is always allowed elsewhere)."""
    try:
        host = canon_host(urlparse(url).netloc)
    except Exception:
        return False
    return host == "google.com" or host.endswith(".google.com")

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
        self._last = {}  # host -> last_time(monotonic)

    def wait(self, host: str):
        host = canon_host(host)
        with self._lock:
            now = time.monotonic()
            last = self._last.get(host, 0.0)
            wait_s = (last + self.min_interval) - now
            if wait_s > 0:
                time.sleep(wait_s)
            self._last[host] = time.monotonic()

# -----------------------------
# Thread-safe deque with "prefer new domains"
# -----------------------------
class URLDeque:
    def __init__(self):
        self._dq = deque()
        self._lock = threading.Lock()
        self._cv = threading.Condition(self._lock)

    def put(self, url: str) -> bool:
        """Return False if queue is full."""
        with self._cv:
            if len(self._dq) >= MAX_QUEUE_SIZE:
                return False
            self._dq.append(url)
            self._cv.notify()
            return True

    def qsize(self) -> int:
        with self._lock:
            return len(self._dq)

    def has_items(self) -> bool:
        with self._lock:
            return len(self._dq) > 0

    def get_eligible_prefer_new(self, eligible_fn, is_new_domain_fn, timeout: float = 0.5) -> str | None:
        """
        Pick an eligible URL, prioritizing URLs whose base domain is "new"
        (i.e., domain not yet parsed). If none, pick any eligible.
        """
        end = time.monotonic() + timeout
        with self._cv:
            while True:
                n = len(self._dq)
                if n == 0:
                    remaining = end - time.monotonic()
                    if remaining <= 0:
                        return None
                    self._cv.wait(timeout=remaining)
                    continue

                # PASS 1: eligible + new domain
                for _ in range(n):
                    url = self._dq[0]
                    if eligible_fn(url) and is_new_domain_fn(url):
                        self._dq.popleft()
                        return url
                    self._dq.rotate(-1)

                # PASS 2: any eligible
                for _ in range(n):
                    url = self._dq[0]
                    if eligible_fn(url):
                        self._dq.popleft()
                        return url
                    self._dq.rotate(-1)

                remaining = end - time.monotonic()
                if remaining <= 0:
                    return None
                self._cv.wait(timeout=min(0.2, remaining))

# -----------------------------
# Curses UI
# -----------------------------
def _safe_trim(s: str, width: int) -> str:
    if width <= 0:
        return ""
    return s if len(s) <= width else (s[: max(0, width - 1)] + "…")

def safe_addstr(stdscr, y: int, x: int, s: str):
    try:
        stdscr.addstr(y, x, s)
    except curses.error:
        pass

def run_crawl_with_ui(stdscr, start_url: str):
    try:
        curses.curs_set(0)
    except Exception:
        pass
    stdscr.nodelay(True)
    stdscr.timeout(100)

    conn = init_db(DB_PATH)
    db_lock = threading.Lock()

    visited = set()
    visited_lock = threading.Lock()

    q = URLDeque()
    q.put(start_url)  # initial always allowed

    limiter = RateLimiter(MIN_SECONDS_PER_HOST)

    # per-base-domain counters (subdomains grouped)
    domain_count: dict[str, int] = {}
    domain_lock = threading.Lock()

    # overall counters (for UI)
    pages_done = 0
    pages_lock = threading.Lock()

    in_flight = 0
    in_flight_lock = threading.Lock()

    status_lock = threading.Lock()
    status = [{
        "state": "idle",
        "url": "",
        "host": "",
        "domain": "",
        "emails": 0,
        "ins": 0,
        "upd": 0,
        "err": ""
    } for _ in range(MAX_WORKERS)]

    stop_event = threading.Event()
    stop_reason_lock = threading.Lock()
    stop_reason = ""

    dropped_lock = threading.Lock()
    dropped_queue_full = 0

    def inc_dropped():
        nonlocal dropped_queue_full
        with dropped_lock:
            dropped_queue_full += 1

    def get_dropped():
        with dropped_lock:
            return dropped_queue_full

    def set_stop_reason(msg: str):
        nonlocal stop_reason
        with stop_reason_lock:
            stop_reason = msg

    def get_stop_reason() -> str:
        with stop_reason_lock:
            return stop_reason

    def set_status(slot: int, **kwargs):
        with status_lock:
            status[slot].update(kwargs)

    def domain_limit_reached(base_domain: str) -> bool:
        with domain_lock:
            return domain_count.get(base_domain, 0) >= MAX_PAGES_PER_DOMAIN

    def bump_domain(base_domain: str):
        with domain_lock:
            domain_count[base_domain] = domain_count.get(base_domain, 0) + 1

    def is_new_domain_url(url: str) -> bool:
        bd = url_base_domain(url)
        with domain_lock:
            return domain_count.get(bd, 0) == 0

    def eligible(url: str) -> bool:
        if not is_http_url(url):
            return False
        # block google.com (+subdomains) for FOLLOWING URLs, not initial
        if url != start_url and is_blocked_domain(url):
            return False
        bd = url_base_domain(url)
        if domain_limit_reached(bd):
            return False
        return True

    def worker(slot: int):
        nonlocal pages_done, in_flight
        session = requests.Session()
        session.headers.update(HEADERS)

        while not stop_event.is_set():
            url = q.get_eligible_prefer_new(eligible, is_new_domain_url, timeout=0.5)
            if url is None:
                with in_flight_lock:
                    infl = in_flight
                if infl == 0:
                    if q.has_items():
                        set_stop_reason("Stopped: queue has URLs but none are eligible (all blocked/capped/visited).")
                    else:
                        set_stop_reason("Finished: queue empty and no work in flight.")
                    stop_event.set()
                    return
                continue

            with visited_lock:
                if url in visited:
                    continue
                visited.add(url)

            with in_flight_lock:
                in_flight += 1

            host = url_host(url)
            bd = url_base_domain(url)
            set_status(slot, state="wait", url=url, host=host, domain=bd, err="", emails=0, ins=0, upd=0)

            try:
                limiter.wait(host)

                set_status(slot, state="fetch", url=url, host=host, domain=bd, err="")
                r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
                r.raise_for_status()

                final_url = r.url
                final_host = url_host(final_url)
                final_bd = url_base_domain(final_url)

                if url != start_url and is_blocked_domain(final_url):
                    set_status(slot, state="skip", url=final_url, host=final_host, domain=final_bd, err="blocked google.com")
                    continue

                if domain_limit_reached(final_bd):
                    set_status(slot, state="skip", url=final_url, host=final_host, domain=final_bd,
                               err=f"domain cap reached ({MAX_PAGES_PER_DOMAIN})")
                    continue

                set_status(slot, state="parse", url=final_url, host=final_host, domain=final_bd, err="")
                title, hrefs, emails_found = extract_title_links_emails(r.text, r.content)

                with db_lock:
                    ins, upd = upsert_emails(conn, final_url, title, emails_found)

                bump_domain(final_bd)

                with pages_lock:
                    pages_done += 1

                set_status(slot, state="done", url=final_url, host=final_host, domain=final_bd,
                           emails=len(emails_found), ins=ins, upd=upd, err="")

                # enqueue links with safety cap per page
                added = 0
                for href in hrefs:
                    if added >= MAX_LINKS_ENQUEUE_PER_PAGE:
                        break
                    nxt = normalize_url(final_url, href)
                    if not nxt or not is_http_url(nxt):
                        continue
                    if is_blocked_domain(nxt):
                        continue
                    with visited_lock:
                        if nxt in visited:
                            continue
                    ok = q.put(nxt)
                    if not ok:
                        inc_dropped()
                        break
                    added += 1

                time.sleep(random.uniform(0.0, 0.05))

            except requests.RequestException as e:
                set_status(slot, state="err", url=url, host=host, domain=bd, err=str(e)[:180])
            except Exception as e:
                set_status(slot, state="err", url=url, host=host, domain=bd, err=str(e)[:180])
            finally:
                with in_flight_lock:
                    in_flight -= 1

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(worker, i) for i in range(MAX_WORKERS)]

        while True:
            try:
                ch = stdscr.getch()
                if ch in (ord('q'), ord('Q')):
                    set_stop_reason("Stopped by user (q).")
                    stop_event.set()
                    break
            except Exception:
                pass

            with pages_lock:
                pd = pages_done
            with in_flight_lock:
                infl = in_flight
            qlen = q.qsize()
            with visited_lock:
                vlen = len(visited)
            with domain_lock:
                domains_seen = len(domain_count)
                capped = sum(1 for _, v in domain_count.items() if v >= MAX_PAGES_PER_DOMAIN)
                new_domains_pending = None  # computed cheaply below (optional)

            dropped = get_dropped()

            stdscr.erase()
            h, w = stdscr.getmaxyx()

            header = (
                f"EmailCrawler UI | workers={MAX_WORKERS} | pages_done={pd} | queue={qlen}/{MAX_QUEUE_SIZE} "
                f"| in_flight={infl} | visited={vlen} | base-domains-parsed={domains_seen} | capped={capped} "
                f"| cap/base-domain={MAX_PAGES_PER_DOMAIN} | dropped={dropped} | PRIORITY=new domains | q=quit"
            )
            safe_addstr(stdscr, 0, 0, _safe_trim(header, w - 1))
            safe_addstr(stdscr, 1, 0, _safe_trim("-" * (w - 1), w - 1))

            with status_lock:
                snap = [dict(s) for s in status]

            for i in range(MAX_WORKERS):
                line = 2 + i
                if line >= h:
                    break
                s = snap[i]
                state = s["state"]
                url = s["url"]
                host = s.get("host", "")
                dom = s.get("domain", "")
                emails = s["emails"]
                ins = s["ins"]
                upd = s["upd"]
                err = s["err"]

                left = f"[{i}] {state:5} dom={dom[:18]:18} host={host[:22]:22} emails={emails:3} +{ins:3} ~{upd:3} "
                right = url if not err else f"{url} | {err}"
                safe_addstr(stdscr, line, 0, _safe_trim(left + right, w - 1))

            reason = get_stop_reason()
            if reason:
                safe_addstr(stdscr, min(h - 1, 2 + MAX_WORKERS), 0, _safe_trim(reason, w - 1))

            stdscr.refresh()

            if stop_event.is_set():
                break
            if all(f.done() for f in futures):
                break

            time.sleep(0.1)

        stop_event.set()
        for f in futures:
            try:
                f.result()
            except Exception:
                pass

    conn.close()

def main():
    start_url = input("Introduce página inicial: ").strip()
    if not start_url:
        print("URL vacía.")
        return
    curses.wrapper(run_crawl_with_ui, start_url)

if __name__ == "__main__":
    main()

