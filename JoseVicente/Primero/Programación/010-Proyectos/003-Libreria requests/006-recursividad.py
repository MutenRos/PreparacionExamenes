# pip3 install requests lxml --break-system-packages

import re
import time
import random
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from lxml import html

START_URL = "https://tameformacion.com/"

# Límites / comportamiento del crawler
MAX_PAGES = 300          # tope de páginas a visitar (evita bucles infinitos)
TIMEOUT = 12

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 (EmailCrawler)"
}

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

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
    abs_url, _frag = urldefrag(abs_url)

    if abs_url.endswith("/") and len(abs_url) > len("https://x/"):
        abs_url = abs_url[:-1]

    return abs_url

def extract_title_and_links(page_url: str, response_text: str, response_bytes: bytes):
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

def crawl_emails(start_url: str):
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

            title, hrefs, emails = extract_title_and_links(final_url, r.text, r.content)

            print(f"\nPAGE: {final_url}")
            print(f"TITLE: {title}")
            if emails:
                print("EMAILS FOUND:")
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

            # 🔹 Random delay between 1 and 5 seconds
            sleep_time = random.uniform(1, 5)
            time.sleep(sleep_time)

        except requests.RequestException:
            continue

if __name__ == "__main__":
    crawl_emails(START_URL)

