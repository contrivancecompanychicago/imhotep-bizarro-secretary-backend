from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.auth import get_current_user
from app.config import settings
from app.models import User
from app.services.healthcare_service import HealthcareNLPError, HealthcareNLPService

router = APIRouter(prefix="/healthcare", tags=["healthcare"])


class HealthcareAnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100_000, description="Clinical text to analyze")


class HealthcareEntity(BaseModel):
    id: str
    type: str
    text: str


class HealthcareRelationship(BaseModel):
    subject_id: str
    object_id: str
    type: str


class HealthcareAnalyzeResponse(BaseModel):
    entities: list[HealthcareEntity]
    relationships: list[HealthcareRelationship]


class HealthcareCodeCandidate(BaseModel):
    code_system: str
    code: str
    display: str
    evidence: list[str]
    matched_signals: dict[str, list[str]]
    priority: str
    review_required: bool


class DiabetesFootScreening(BaseModel):
    diabetes_terms: list[str]
    foot_terms: list[str]
    complication_terms: dict[str, list[str]]
    eligible_for_prioritized_candidates: bool
    method: str


class UnavailableCodeSystem(BaseModel):
    code_system: str
    reason: str


class HealthcareCodeSuggestResponse(BaseModel):
    focus: str
    screening: DiabetesFootScreening
    code_candidates: list[HealthcareCodeCandidate]
    unavailable_code_systems: list[UnavailableCodeSystem]
    coding_review_required: bool
    notice: str


def _healthcare_service() -> HealthcareNLPService:
    return HealthcareNLPService(
        project_id=settings.google_cloud_project,
        location=settings.google_cloud_location,
        timeout_seconds=settings.healthcare_api_timeout_seconds,
    )


def _analyze(text: str, operation: str) -> dict:
    normalized_text = text.strip()
    if not normalized_text:
        raise HTTPException(status_code=422, detail="text must not be blank")

    service = _healthcare_service()
    try:
        return getattr(service, operation)(normalized_text)
    except HealthcareNLPError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


@router.post("/analyze", response_model=HealthcareAnalyzeResponse)
def analyze_clinical_text(
    payload: HealthcareAnalyzeRequest,
    current_user: User = Depends(get_current_user),
) -> HealthcareAnalyzeResponse:
    """Extract clinical entities and links; not a coding or diagnosis service."""
    return HealthcareAnalyzeResponse(**_analyze(payload.text, "analyze"))


@router.post("/code-suggest", response_model=HealthcareCodeSuggestResponse)
def suggest_clinical_codes(
    payload: HealthcareAnalyzeRequest,
    current_user: User = Depends(get_current_user),
) -> HealthcareCodeSuggestResponse:
    """Return keyword-prioritized, extraction-linked candidates for review."""
    return HealthcareCodeSuggestResponse(**_analyze(payload.text, "suggest_codes"))
