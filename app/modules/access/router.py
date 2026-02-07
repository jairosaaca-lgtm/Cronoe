from app.http import JSONResponse
from app.modules.surveys.router import _to_response
from app.modules.surveys.service import get_survey_or_404


def resolve_survey(public_code: str) -> JSONResponse:
    survey = get_survey_or_404(public_code)
    return JSONResponse(status_code=200, body=_to_response(survey).__dict__)
