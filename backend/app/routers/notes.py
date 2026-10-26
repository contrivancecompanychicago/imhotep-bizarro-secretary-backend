from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import ClinicalNote, Patient, User
from app.schemas import ClinicalNoteCreate
from app.services.xerj_service import index_note

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/")
def create_note(
    note: ClinicalNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = db.query(Patient).filter(Patient.id == note.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="patient not found")

    new_note = ClinicalNote(
        patient_id=note.patient_id,
        title=note.title,
        content=note.content,
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    index_note(note.patient_id, note.title, note.content)
    return {"message": "note saved", "note_id": new_note.id}
