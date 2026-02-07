from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from app.errors import APIError
from app.http import JSONResponse, parse_json
from app.modules.access.router import resolve_survey
from app.modules.responses.router import create_response_route
from app.modules.surveys.router import create_survey_route, update_survey_route


class AppHandler(BaseHTTPRequestHandler):
    def _send(self, response: JSONResponse) -> None:
        status_code, body = response.to_http()
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def _handle_error(self, exc: Exception) -> None:
        if isinstance(exc, APIError):
            self._send(JSONResponse(exc.status_code, {"detail": exc.message}))
            return
        self._send(JSONResponse(500, {"detail": "Internal server error"}))

    def _path_parts(self) -> list[str]:
        return [part for part in urlparse(self.path).path.split("/") if part]

    def do_GET(self) -> None:  # noqa: N802
        try:
            parts = self._path_parts()
            if parts == ["health"]:
                self._send(JSONResponse(200, {"status": "ok"}))
                return
            if len(parts) == 2 and parts[0] == "surveys":
                self._send(resolve_survey(parts[1]))
                return
            self._send(JSONResponse(404, {"detail": "Not found"}))
        except Exception as exc:  # noqa: BLE001
            self._handle_error(exc)

    def do_POST(self) -> None:  # noqa: N802
        try:
            parts = self._path_parts()
            content_length = int(self.headers.get("Content-Length", "0"))
            payload = parse_json(self.rfile.read(content_length))

            if parts == ["surveys"]:
                self._send(create_survey_route(payload))
                return
            if len(parts) == 3 and parts[0] == "surveys" and parts[2] == "responses":
                self._send(create_response_route(parts[1], payload))
                return
            self._send(JSONResponse(404, {"detail": "Not found"}))
        except Exception as exc:  # noqa: BLE001
            self._handle_error(exc)

    def do_PATCH(self) -> None:  # noqa: N802
        try:
            parts = self._path_parts()
            content_length = int(self.headers.get("Content-Length", "0"))
            payload = parse_json(self.rfile.read(content_length))

            if len(parts) == 2 and parts[0] == "surveys":
                self._send(update_survey_route(parts[1], payload))
                return
            self._send(JSONResponse(404, {"detail": "Not found"}))
        except Exception as exc:  # noqa: BLE001
            self._handle_error(exc)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = HTTPServer((host, port), AppHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
