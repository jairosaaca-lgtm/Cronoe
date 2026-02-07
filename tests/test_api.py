from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from http.server import HTTPServer

from app.main import AppHandler
from app.storage import db


def setup_function() -> None:
    db.surveys.clear()
    db.responses.clear()
    db._next_id = 1


def _start_server() -> tuple[HTTPServer, threading.Thread]:
    server = HTTPServer(("127.0.0.1", 0), AppHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _request(server: HTTPServer, method: str, path: str, payload: dict | None = None) -> tuple[int, dict]:
    conn = HTTPConnection("127.0.0.1", server.server_port)
    body = None if payload is None else json.dumps(payload)
    headers = {"Content-Type": "application/json"} if body else {}
    conn.request(method, path, body=body, headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    conn.close()
    return res.status, data


def test_create_and_resolve_survey_with_public_code() -> None:
    server, thread = _start_server()
    try:
        status, created = _request(
            server,
            "POST",
            "/surveys",
            {"title": "NPS Q1", "questions": [{"id": "q1", "type": "rating"}], "published": True},
        )
        assert status == 201
        assert created["public_code"]
        assert created["public_code"] != "1"

        status, found = _request(server, "GET", f"/surveys/{created['public_code']}")
        assert status == 200
        assert found["title"] == "NPS Q1"
    finally:
        server.shutdown()
        thread.join(timeout=1)


def test_submit_response() -> None:
    server, thread = _start_server()
    try:
        _, created = _request(server, "POST", "/surveys", {"title": "Encuesta UX", "published": True})
        code = created["public_code"]

        status, payload = _request(
            server,
            "POST",
            f"/surveys/{code}/responses",
            {"answers": {"satisfaction": 5, "comment": "Excelente"}},
        )

        assert status == 201
        assert payload["survey_public_code"] == code
        assert "submitted_at" in payload
    finally:
        server.shutdown()
        thread.join(timeout=1)
