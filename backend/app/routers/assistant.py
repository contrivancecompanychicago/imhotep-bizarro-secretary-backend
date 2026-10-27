from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.services.assistant_service import build_onboarding_response

router = APIRouter(prefix="/assistant", tags=["assistant"])


class AssistantMessage(BaseModel):
    user_email: str | None = None
    user_name: str | None = None
    message: str
    user_type: str = "new"
    site_url: str | None = None


@router.post("/chat")
def assistant_chat(payload: AssistantMessage):
    if not payload.message or not payload.message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    reply = build_onboarding_response(
        message=payload.message,
        user_name=payload.user_name,
        user_email=payload.user_email,
        user_type=payload.user_type,
        site_url=payload.site_url or settings.deep_human_families_site_url,
    )

    return {
        "reply": reply,
        "user_type": payload.user_type,
        "site_url": payload.site_url or settings.deep_human_families_site_url,
    }
