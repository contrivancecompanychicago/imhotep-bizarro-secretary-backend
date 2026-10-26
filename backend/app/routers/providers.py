from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Provider, User
from app.schemas import ProviderCreate

router = APIRouter(prefix="/providers", tags=["providers"])


@router.post("/")
def create_provider(
    provider: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_provider = Provider(
        name=provider.name,
        specialty=provider.specialty,
        email=provider.email,
    )
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return {"message": "provider created", "provider_id": new_provider.id}


@router.get("/")
def list_providers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    providers = db.query(Provider).all()
    return {"providers": providers}
