from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ResponseCreateRequest:
    answers: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ResponseCreateRequest":
        answers = payload.get("answers", {})
        if not isinstance(answers, dict):
            raise ValueError("answers must be an object")
        return cls(answers=answers)


@dataclass
class ResponseCreateResult:
    survey_public_code: str
    submitted_at: datetime
