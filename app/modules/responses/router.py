from app.errors import APIError
from app.http import JSONResponse
from app.modules.responses.schemas import ResponseCreateRequest, ResponseCreateResult
from app.modules.responses.service import create_response


def create_response_route(public_code: str, payload: dict) -> JSONResponse:
    try:
        parsed = ResponseCreateRequest.from_dict(payload)
    except ValueError as exc:
        raise APIError(str(exc), 400) from exc

    record = create_response(public_code, parsed)
    body = ResponseCreateResult(
        survey_public_code=record.survey_public_code,
        submitted_at=record.submitted_at,
    ).__dict__
    return JSONResponse(status_code=201, body=body)
