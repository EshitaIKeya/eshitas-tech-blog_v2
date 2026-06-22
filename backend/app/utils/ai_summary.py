import httpx
import re
from app.config import GROQ_API_KEY


def strip_html(html: str) -> str:
    """Remove HTML tags to get plain text."""
    return re.sub(r"<[^>]*>", "", html).strip()


def generate_summary(content: str) -> str:
    """Call Groq's API to generate a 2-3 sentence summary of the post content.
    Returns the summary text, or raises an error if not configured."""

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in .env file")

    plain_text = strip_html(content)

    response = httpx.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 250,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Summarize this blog post in 2-3 short sentences. "
                        "Write in a friendly tone as if summarizing for a reader "
                        "who wants to decide whether to read the full post:\n\n"
                        + plain_text[:3000]
                    ),
                }
            ],
        },
        timeout=30.0,
    )

    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
