from typing import Literal

from pydantic import BaseModel, Field

CorpusName = Literal["safety", "maintenance", "quality"]


class RouteDecision(BaseModel):
    corpus: CorpusName
    rationale: str = Field(description="One sentence explaining the routing choice.")
    confidence: Literal["high", "medium", "low"] = "high"


class Citation(BaseModel):
    source: str
    doc_id: str
    excerpt: str


class SupervisorAnswer(BaseModel):
    summary: str
    steps: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    limitations: str = (
        "Answer grounded in retrieved playbook sections only. "
        "Verify with official project SOPs before acting."
    )
