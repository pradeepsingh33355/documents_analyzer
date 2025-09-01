from typing import Dict, Any, List, Optional
import os
import requests
import textstat

LANGUAGETOOL_SERVER_URL = "http://localhost:8081/v2/check"

GUIDELINES = [
    "Aim for Flesch Reading Ease >= 60 (higher is easier).",
    "Keep average sentence length <= 20 words.",
    "Avoid grammar and spelling mistakes.",
    "Prefer active voice and clear phrasing (heuristic).",
]


def assess_text(text: str) -> Dict[str, Any]:
    data = {
        "text": text,
        "language": "en-US",
    }

    response = requests.post(LANGUAGETOOL_SERVER_URL, data=data)

    if response.status_code != 200:
        return {"error": f"LanguageTool API returned an error: {response.text}"}

    result = response.json()

    grammar_issues = [
        {
            "message": m["message"],
            "offset": m["offset"],
            "length": m["length"],
            "context": m["context"],
            "rule": m["rule"]["id"],
        }
        for m in result.get("matches", [])
    ]

    reading_ease = textstat.flesch_reading_ease(text)
    avg_sentence_len = textstat.avg_sentence_length(text)

    overall = _overall_judgement(
        grammar_count=len(grammar_issues),
        reading_ease=reading_ease,
        avg_sentence_len=avg_sentence_len,
    )

    return {
        "overall": overall,
        "issues": grammar_issues,
        "guideline_notes": GUIDELINES,
    }


def _overall_judgement(
    grammar_count: int, reading_ease: float, avg_sentence_len: float
) -> str:
    ok_read = reading_ease >= 60
    ok_sent = avg_sentence_len <= 20
    ok_grammar = grammar_count <= 3

    score = sum([ok_read, ok_sent, ok_grammar])
    if score == 3:
        return "Compliant"
    if score == 2:
        return "Mostly Compliant"
    if score == 1:
        return "Needs Improvement"
    return "Non-Compliant"


if __name__ == "__main__":
    sample_text = """
    This are an bad example. It have errors.
    Another paragraph which is also too long and maybe confusing for the readers because it has many words without a proper break.
    """

    result = assess_text(sample_text)
    print(result)
    print("Report saved as assessment_report.txt")
