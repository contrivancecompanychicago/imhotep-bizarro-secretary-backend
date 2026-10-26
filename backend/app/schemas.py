from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "staff"


class UserLogin(BaseModel):
    email: str
    password: str


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    dob: str | None = None
    sex: str | None = None
    phone: str | None = None
    email: str | None = None


class ProviderCreate(BaseModel):
    name: str
    specialty: str | None = None
    email: str | None = None


class AppointmentCreate(BaseModel):
    patient_id: int
    provider_id: int
    scheduled_at: datetime
    reason: str
    notes: str | None = None


class ClinicalNoteCreate(BaseModel):
    patient_id: int
    title: str
    content: str


class IntakeFormCreate(BaseModel):
    patient_id: int
    form_data: str
