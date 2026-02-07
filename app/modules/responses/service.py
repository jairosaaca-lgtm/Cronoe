from app.modules.responses.schemas import ResponseCreateRequest
from app.modules.surveys.service import get_survey_or_404
from app.storage import ResponseRecord, db


def create_response(public_code: str, payload: ResponseCreateRequest) -> ResponseRecord:
    get_survey_or_404(public_code)
    record = ResponseRecord(survey_public_code=public_code, answers=payload.answers)
    db.responses.setdefault(public_code, []).append(record)
    return record
