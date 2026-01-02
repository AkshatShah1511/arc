import requests
from bs4 import BeautifulSoup

MAX_CHARS = 6000
TIMEOUT = 8


def fetch_website_text(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 ARC-Agent/1.0"
        }
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS]

        return text

    except Exception:
        return ""
    