from pydantic import BaseModel
from typing import List, Union


class Context(BaseModel):
    text: str
    offset: int
    length: int


class Issue(BaseModel):
    message: str
    offset: int
    length: int
    context: Context
    rule: str


class CorrectionRequest(BaseModel):
    doc_id: str
    issues: List[Issue]
    guideline_notes: List[str]
