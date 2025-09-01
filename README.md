# AI Document Compliance (FastAPI)

This project implements an API that:
- accepts PDF/DOCX uploads,
- assesses them against English writing guidelines (grammar, clarity, readability),
- optionally produces a guideline-compliant corrected document for download.

## Features
- **Upload** PDF/DOCX (`/upload`)
- **Assess** compliance report (`/assess/{doc_id}`)
- **Correct** the document and **download** (`/correct/{doc_id}`)
- Basic **unit tests**

## Tech
FastAPI, PyMuPDF, python-docx, language-tool-python, textstat,LLM(Opoen AI)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

LanguageTool runs in serverless mode by default. If you want to point to a local LanguageTool server, set env:
```
LANGUAGETOOL_URL=http://localhost:8081
```

## API

### POST /upload
Multipart form: `file` (pdf/docx)

**Response**
```json
{
  "doc_id": "uuid",
  "filename": "file.docx",
  "chars": 12345,
  "words": 2345,
  "preview": "first 300 chars..."
}
```

### POST /assess/{doc_id}
Returns compliance report:
```json
{
  "doc_id": "...",
  "overall": "Needs Improvement",
  "scores": {
    "grammar_issues": 12,
    "flesch_reading_ease": 55.3,
    "avg_sentence_length": 23.4
  },
  "issues": [
    {"message": "...", "offset": 120, "length": 5, "rule": "UPPERCASE_SENTENCE_START"}
  ],
  "guideline_notes": [
    "Aim for Flesch Reading Ease >= 60",
    "Keep average sentence length <= 20 words"
  ]
}
```

### POST /correct/{doc_id}
Optional JSON body:
```json
{
    "doc_id": "10",
    "overall": "Needs Improvement",
    "issues": [
        
        {
            "message": "Possible spelling mistake found.",
            "offset": 817,
            "length": 6,
            "context": {
                "text": "...ibility: Directly feed JSON from LLM to Plotly • No HTML File Handling: Avoids local H...",
                "offset": 43,
                "length": 6
            },
            "rule": "MORFOLOGIK_RULE_EN_US"
        }
        
    ],
    "guideline_notes": [
        "Aim for Flesch Reading Ease >= 60 (higher is easier).",
        "Keep average sentence length <= 20 words.",
        "Avoid grammar and spelling mistakes.",
        "Prefer active voice and clear phrasing (heuristic)."
    ]
}
```
Returns a corrected `.docx` file as attachment.

## Testing
```bash
pytest -q
```

## Notes
- If `OPENAI_API_KEY` is set, the service will attempt to use OpenAI for higher-quality rewrites; otherwise it falls back to rule-based corrections via LanguageTool + heuristics.
