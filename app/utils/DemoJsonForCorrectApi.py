sample_json = {
    "doc_id": "6",
    "overall": "Mostly Compliant",
    "issues": [
        {
            "message": "Possible spelling mistake found.",
            "offset": 609,
            "length": 7,
            "context": {
                "text": "...int in any Python web framework (Flask, FastAPI, Django, etc.) to  accept PDF or Word d...",
                "offset": 43,
                "length": 7,
            },
            "rule": "MORFOLOGIK_RULE_EN_US",
        },
        {
            "message": "Possible spelling mistake found.",
            "offset": 1709,
            "length": 7,
            "context": {
                "text": "...   - Use a Python framework like Flask, FastAPI, or Django.  - Ensure efficient and sec...",
                "offset": 43,
                "length": 7,
            },
            "rule": "MORFOLOGIK_RULE_EN_US",
        },
        {
            "message": "Possible spelling mistake found.",
            "offset": 1916,
            "length": 5,
            "context": {
                "text": "... Utilize NLP models such as OpenAI GPT, spaCy, or LanguageTool for guideline checking...",
                "offset": 43,
                "length": 5,
            },
            "rule": "MORFOLOGIK_RULE_EN_US",
        },
    ],
    "guideline_notes": [
        "Aim for Flesch Reading Ease >= 60 (higher is easier).",
        "Keep average sentence length <= 20 words.",
        "Avoid grammar and spelling mistakes.",
        "Prefer active voice and clear phrasing (heuristic).",
    ],
}
