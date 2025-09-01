import requests
from typing import List
from app.schemas.CorrectionRequest import Issue

LANGUAGETOOL_SERVER_URL = "http://localhost:8081/v2/check"


def _init_tool():
    return LANGUAGETOOL_SERVER_URL


def correct_text(text: str, issues: List[Issue]) -> str:
    corrected_text = text

    for issue in issues:
        error_text = issue.context.text
        start_offset = issue.offset
        length = issue.length

        data = {
            "text": error_text,
            "language": "en-US",
        }

        response = requests.post(LANGUAGETOOL_SERVER_URL, data=data)

        if response.status_code != 200:
            raise Exception(f"LanguageTool API returned an error: {response.text}")

        result = response.json()

        matches = result.get("matches", [])

        for match in matches:
            correction = match.get("replacements", [])
            if correction:
                corrected_text = (
                    corrected_text[:start_offset]
                    + correction[0]["value"]
                    + corrected_text[start_offset + length :]
                )

    return corrected_text
