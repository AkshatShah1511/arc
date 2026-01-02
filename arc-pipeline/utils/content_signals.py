import re

KEYWORD_BUCKETS = {
    "tech": ["software", "cloud", "ai", "machine learning", "data", "platform"],
    "consulting": ["consulting", "services", "solutions", "enterprise"],
    "finance": ["bank", "fintech", "payments", "financial"],
    "education": ["university", "college", "research", "lab"],
}

RED_FLAGS = [
    "blog",
    "personal website",
    "portfolio",
    "music video",
    "lyrics",
    "youtube channel"
]


def extract_signals(text: str) -> dict:
    lower = text.lower()

    matched_domains = []
    for domain, keywords in KEYWORD_BUCKETS.items():
        if any(k in lower for k in keywords):
            matched_domains.append(domain)

    red_flags = [rf for rf in RED_FLAGS if rf in lower]

    possible_name = None
    lines = text.splitlines()
    if lines:
        possible_name = lines[0][:80]

    return {
        "possible_company_name": possible_name or "Unknown",
        "detected_domains": matched_domains,
        "red_flags": red_flags,
        "has_business_signals": len(matched_domains) > 0 and len(red_flags) == 0
    }
