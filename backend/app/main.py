from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import appointments, assistant, auth, notes, patients, providers, search

app = FastAPI(title="IMHOTEP Bizarros Medical Secretary")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(providers.router)
app.include_router(appointments.router)
app.include_router(notes.router)
app.include_router(search.router)
app.include_router(assistant.router)


@app.get("/")
def root():
    return {"message": "IMHOTEP Bizarros Medical Secretary API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
