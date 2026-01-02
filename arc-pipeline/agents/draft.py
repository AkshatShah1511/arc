import os
import json
from google import genai

MODEL_NAME = "gemini-2.5-flash"

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def generate_draft(
    company_name: str,
    industry: str,
    region: str,
    company_summary: str,
    receiver_email: str
) -> dict:
    prompt = f"""
    You are writing an email FROM an individual job seeker TO a company representative.

Sender profile:
- Background: Computer Science / IT background
- Intent: Learn about the company and explore relevant opportunities
- Tone: Professional, curious, concise
- The sender is NOT a company and is NOT pitching services.

Recipient context:
- Company name: {company_name}
- Industry: {industry}
- Region: {region}
- Company summary: {company_summary}

Task:
Draft a professional outreach email from the sender to the company.

Structure the email as follows:
1) Opening: Polite, natural greeting that mentions the company name.
2) Context: One sentence showing awareness of what the company does.
3) Intent: Express interest in learning more and exploring relevant opportunities.
4) Close: Low-pressure, respectful closing.

Rules:
- Do NOT describe the sender as a company or service provider.
- Do NOT pitch products or services.
- Avoid generic phrases like “I hope this email finds you well.”
- Keep it concise (~120 words).
- No emojis. No attachments.

Return STRICT JSON with exactly:
- draft_subject
- draft_body

Output ONLY valid JSON. No extra text.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    text = response.text.strip()

# Remove markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)

        # Hard guarantee keys exist
        if "draft_subject" in parsed and "draft_body" in parsed:
            return parsed

    except Exception:
        pass

    # Fallback (rare now)
    return {
        "draft_subject": "Quick introduction",
        "draft_body": (
            "Hello,\n\n"
            "I came across your organization and wanted to briefly introduce myself. "
            "I’d appreciate the opportunity to connect and learn more about your work.\n\n"
            "Best regards,"
        )
    }
    

