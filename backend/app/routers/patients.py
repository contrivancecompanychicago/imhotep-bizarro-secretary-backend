from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Patient, User
from app.schemas import PatientCreate, PatientUpdate

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/")
def get_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patients = db.query(Patient).all()
    return {"patients": patients}


@router.post("/")
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_patient = Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        dob=patient.dob,
        sex=patient.sex,
        phone=patient.phone,
        email=patient.email,
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {"message": "patient created", "patient_id": new_patient.id}


@router.get("/{patient_id}")
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="patient not found")
    return patient
