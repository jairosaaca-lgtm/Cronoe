from datetime import datetime, timezone
from secrets import token_urlsafe

from app.errors import APIError
from app.modules.surveys.schemas import SurveyCreateRequest, SurveyUpdateRequest
from app.storage import Survey, db

PUBLIC_CODE_BYTES = 6


def _generate_public_code() -> str:
    return token_urlsafe(PUBLIC_CODE_BYTES)


def create_survey(payload: SurveyCreateRequest) -> Survey:
    public_code = _generate_public_code()
    while public_code in db.surveys:
        public_code = _generate_public_code()

    survey = Survey(
        id=db.next_id(),
        public_code=public_code,
        title=payload.title,
        questions=payload.questions,
        published=payload.published,
    )
    db.surveys[public_code] = survey
    return survey


def update_survey(public_code: str, payload: SurveyUpdateRequest) -> Survey:
    survey = get_survey_or_404(public_code)
    if payload.title is not None:
        survey.title = payload.title
    if payload.questions is not None:
        survey.questions = payload.questions
    if payload.published is not None:
        survey.published = payload.published
    survey.updated_at = datetime.now(timezone.utc)
    return survey


def get_survey_or_404(public_code: str) -> Survey:
    survey = db.surveys.get(public_code)
    if survey is None:
        raise APIError("Survey not found", 404)
    return survey
