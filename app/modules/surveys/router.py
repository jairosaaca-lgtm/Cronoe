from app.errors import APIError
from app.http import JSONResponse
from app.modules.surveys.schemas import SurveyCreateRequest, SurveyResponse, SurveyUpdateRequest
from app.modules.surveys.service import create_survey, update_survey


def _to_response(survey) -> SurveyResponse:
    return SurveyResponse(
        public_code=survey.public_code,
        title=survey.title,
        questions=survey.questions,
        published=survey.published,
        created_at=survey.created_at,
        updated_at=survey.updated_at,
    )


def create_survey_route(payload: dict) -> JSONResponse:
    try:
        parsed = SurveyCreateRequest.from_dict(payload)
    except ValueError as exc:
        raise APIError(str(exc), 400) from exc

    survey = create_survey(parsed)
    return JSONResponse(status_code=201, body=_to_response(survey).__dict__)


def update_survey_route(public_code: str, payload: dict) -> JSONResponse:
    try:
        parsed = SurveyUpdateRequest.from_dict(payload)
    except ValueError as exc:
        raise APIError(str(exc), 400) from exc

    survey = update_survey(public_code, parsed)
    return JSONResponse(status_code=200, body=_to_response(survey).__dict__)
