import os
import json
from utils.website_fetcher import fetch_website_text
from utils.content_signals import extract_signals

from google import genai

MODEL_NAME = "gemini-2.5-flash"

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def analyze_website(website_url: str) -> dict:
    website_text = fetch_website_text(website_url)
    signals = extract_signals(website_text)


    prompt = f"""
You are a research assistant.

Below is text extracted from a company website. Use ONLY this content to
understand what the organization does and decide whether it is suitable
for professional outreach.

Website overview (heuristic signals):
- Possible name: {signals["possible_company_name"]}
- Detected domains: {signals["detected_domains"]}
- Red flags: {signals["red_flags"]}
- Business signals present: {signals["has_business_signals"]}

Website content:
{website_text}



Return STRICT JSON with exactly these keys:
- company_name
- industry
- region
- company_summary
- match_decision
- match_reason

Rules:
- Be factual, no hype.
- If unclear, use "Unknown".
- Match = NO if site is dead, irrelevant, or personal blog.
- company_summary: 2–3 short factual lines.
- match_decision must be YES or NO.
- Output ONLY valid JSON. No extra text.
- If website content is empty or meaningless, set match_decision = NO.
- Use the heuristic signals as guidance, but rely on content for final judgment.


"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        return json.loads(text)

    except Exception:
        return {
            "company_name": "Unknown",
            "industry": "Unknown",
            "region": "Unknown",
            "company_summary": "Failed to parse website information.",
            "match_decision": "NO",
            "match_reason": "LLM output was not valid JSON"
        }
