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


@router.post("/analyze", response_model=HealthcareAnalyzeResponse)
def analyze_clinical_text(
    payload: HealthcareAnalyzeRequest,
    current_user: User = Depends(get_current_user),
) -> HealthcareAnalyzeResponse:
    """Extract clinical entities and links; this is not a coding or diagnosis service."""
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="text must not be blank")

    service = HealthcareNLPService(
        project_id=settings.google_cloud_project,
        location=settings.google_cloud_location,
        timeout_seconds=settings.healthcare_api_timeout_seconds,
    )
    try:
        result = service.analyze(text)
    except HealthcareNLPError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc

    return HealthcareAnalyzeResponse(**result)
