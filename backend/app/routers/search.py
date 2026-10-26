from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.services.xerj_service import search_documents

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
def search(query: str, current_user: User = Depends(get_current_user)):
    results = search_documents(query)
    return {"query": query, "results": results}
