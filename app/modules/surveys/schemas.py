from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class SurveyCreateRequest:
    title: str
    questions: list[dict[str, Any]]
    published: bool

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SurveyCreateRequest":
        title = payload.get("title", "")
        if not isinstance(title, str) or not (3 <= len(title) <= 120):
            raise ValueError("title must be a string between 3 and 120 chars")

        questions = payload.get("questions", [])
        if not isinstance(questions, list):
            raise ValueError("questions must be a list")

        published = bool(payload.get("published", False))
        return cls(title=title, questions=questions, published=published)


@dataclass
class SurveyUpdateRequest:
    title: str | None = None
    questions: list[dict[str, Any]] | None = None
    published: bool | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SurveyUpdateRequest":
        title = payload.get("title")
        if title is not None and (not isinstance(title, str) or not (3 <= len(title) <= 120)):
            raise ValueError("title must be between 3 and 120 chars")

        questions = payload.get("questions")
        if questions is not None and not isinstance(questions, list):
            raise ValueError("questions must be a list")

        published = payload.get("published")
        if published is not None:
            published = bool(published)

        return cls(title=title, questions=questions, published=published)


@dataclass
class SurveyResponse:
    public_code: str
    title: str
    questions: list[dict[str, Any]]
    published: bool
    created_at: datetime
    updated_at: datetime
