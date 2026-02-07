from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Survey:
    id: int
    public_code: str
    title: str
    questions: list[dict[str, Any]] = field(default_factory=list)
    published: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ResponseRecord:
    survey_public_code: str
    answers: dict[str, Any]
    submitted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class InMemoryDB:
    def __init__(self) -> None:
        self.surveys: dict[str, Survey] = {}
        self.responses: dict[str, list[ResponseRecord]] = {}
        self._next_id = 1

    def next_id(self) -> int:
        next_value = self._next_id
        self._next_id += 1
        return next_value


db = InMemoryDB()
