from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Appointment, Patient, Provider, User
from app.schemas import AppointmentCreate

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/")
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointments = db.query(Appointment).all()
    return {"appointments": appointments}


@router.post("/")
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="patient not found")

    provider = db.query(Provider).filter(Provider.id == appointment.provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="provider not found")

    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        provider_id=appointment.provider_id,
        scheduled_at=appointment.scheduled_at,
        reason=appointment.reason,
        notes=appointment.notes,
        status="scheduled",
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return {"message": "appointment created", "appointment_id": new_appointment.id}
