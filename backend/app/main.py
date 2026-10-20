from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="IMHOTEP Bizarros", version="0.1.0")


class IntakeRequest(BaseModel):
    patient_name: str | None = None
    notes: str = ""
    specialty: str | None = None


class SummaryResponse(BaseModel):
    status: str
    message: str
    version: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "IMHOTEP Bizarros", "version": "0.1.0"}


@app.post("/api/v0/summary", response_model=SummaryResponse)
def summarize_case(payload: IntakeRequest):
    return {
        "status": "success",
        "message": f"Clinical summary ready for {payload.patient_name or 'patient'}",
        "version": "0.1.0",
    }
