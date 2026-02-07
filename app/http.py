from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class JSONResponse:
    status_code: int
    body: dict[str, Any]

    def to_http(self) -> tuple[int, bytes]:
        return self.status_code, json.dumps(self.body, default=str).encode("utf-8")


def parse_json(raw: bytes) -> dict[str, Any]:
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))
