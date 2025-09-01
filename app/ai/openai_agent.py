import os
from typing import Optional


def rewrite_with_llm(
    text: str,
    tone: str = "neutral",
    target_reading_ease: int = 60,
    max_sentence_length: int = 20,
) -> Optional[str]:
    """Optional: uses OpenAI if OPENAI_API_KEY is present.
    Returns None on failure so caller can fallback to rule-based correction."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        system = (
            "You are an expert English editor. Rewrite the user's document to conform to guidelines: "
            f"Flesch reading ease >= {target_reading_ease}, keep sentences <= {max_sentence_length} words, tone {tone}. "
            "Fix grammar, spelling, clarity, and structure while preserving meaning."
        )
        prompt = (
            "Rewrite the following document accordingly. Return only the corrected text without commentary.\n\n"
            f"Document:\n{text}"
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content
    except Exception:
        return None
