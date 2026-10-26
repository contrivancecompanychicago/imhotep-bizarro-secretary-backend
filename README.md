# IMHOTEP Bizarros Medical Secretary Backend

IMHOTEP Bizarros is a lightweight clinical workflow backend and frontend starter for a virtual lab and clinic assistant. The project is intentionally designed as a simple, beginner-friendly medical secretary prototype built around FastAPI, SQLite, and a search layer powered by XERJ.

This repository is not meant to be a full hospital EMR system or autonomous medical decision engine. It is a practical, focused first version for:

- patient intake
- provider scheduling
- appointment booking
- clinical notes
- symptom and triage tracking
- consent capture
- AI-assisted search over notes and documents

The goal is to help a small clinic, virtual lab, or front-end medical assistant surface patient context quickly without making the core project depend on the Rust/XERJ implementation itself.

## Why this project exists

Earlier in the project discussion, we clarified an important distinction:

- XERJ is a search and retrieval system for AI agents.
- It helps index and search notes, documents, PDFs, log data, and other unstructured information.
- It is not the core clinical workflow engine by itself.
- The business logic for patient intake, scheduling, triage, and data handling belongs in an app layer such as FastAPI.

This repository keeps that separation clear:

- FastAPI + SQLite = patient records, appointments, scheduling, intake, and notes
- XERJ = retrieval/search layer over patient notes and clinical documents
- frontend = simple UI for staff to capture intake information and interact with the backend

This keeps the focus on the medical secretary workflow instead of expanding the project into a full search-engine repo.

## Project architecture

The initial and simplest version follows this structure:

- Frontend: static HTML/CSS/JS form for patient intake and scheduling
- Backend: FastAPI app
- Storage: SQLite database
- Search: XERJ HTTP search layer for notes and documents
- Replit hosting: simple deployment target for the Python API

High-level flow:

1. Staff logs in or uses the app.
2. A patient is entered through intake.
3. Intake includes symptoms, triage status, and consent information.
4. Appointment is scheduled with a provider.
5. Clinical notes are stored in SQLite.
6. Important notes are indexed to XERJ for search and retrieval.
7. Staff can ask the system to search by symptom, issue, note keyword, or patient concern.

## Current starter features

The current implementation supports a minimal but practical medical secretary workflow:

- user login/signup
- provider creation
- patient creation
- patient intake fields:
  - first name
  - last name
  - date of birth
  - sex
  - phone
  - email
  - symptoms / reason for visit
  - triage status
  - consent received
  - consent notes/details
- appointment scheduling
- clinical note creation
- search across indexed note content
- SQLite persistence
- simple browser-based frontend for operational use

## Medical secretary design intent

This system is designed to act as an assistive medical secretary, not an autonomous clinical decision-maker.

It should help with:

- collecting patient intake information
- scheduling visits
- organizing triage status
- recording consent and notes
- retrieving patient and document context rapidly
- helping staff find relevant notes or symptoms quickly

It should not independently diagnose or prescribe treatment without clinician review.

## Minimal architecture for Replit

This repository is structured to support an easy Replit deployment pattern:

- FastAPI app runs as the backend service
- SQLite DB persists in the project directory or a mounted volume
- XERJ runs separately as a search backend or local service
- frontend is a simple static site that calls the API

Recommended deployment layout:

- Replit app 1: FastAPI backend
- Replit app 2: static frontend, or the frontend can live in the same project if desired
- XERJ service: local or external host when running document retrieval/search

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- XERJ (search integration layer)
- HTML/CSS/JavaScript frontend

## Repository layout

```text
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   ├── routers/
│   │   │   ├── appointments.py
│   │   │   ├── auth.py
│   │   │   ├── notes.py
│   │   │   ├── patients.py
│   │   │   ├── providers.py
│   │   │   └── search.py
│   │   └── services/
│   │       └── xerj_service.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── README.md
├── LICENSE
├── VERSION
├── pyproject.toml
├── docs/
└── data/
```

## Local run

From the repo root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
```

Then open the frontend or call the API directly.

## Replit run

For a simple Replit deployment:

1. Create a Python Replit project.
2. Copy the backend files into the project.
3. Install dependencies from `backend/requirements.txt`.
4. Start the app:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 3000
```

5. Serve the frontend as a static page, or keep it in the same project and call the backend URL.

## API basics

The starter backend exposes routes such as:

- `/health`
- `/auth/signup`
- `/auth/login`
- `/patients/`
- `/providers/`
- `/appointments/`
- `/notes/`
- `/search/`

Example patient creation payload:

```json
{
  "first_name": "Mary",
  "last_name": "Smith",
  "dob": "1990-01-15",
  "sex": "female",
  "phone": "555-1234",
  "email": "mary@example.com",
  "symptoms": "Fatigue, dizziness, recurring headaches",
  "triage_status": "urgent",
  "consent_received": true,
  "consent_text": "Consent received for intake and scheduling follow-up"
}
```

## Intake fields included

The intake workflow currently includes fields for:

- symptoms / reason for visit
- triage status
- consent received
- consent notes

This is intentionally minimal and useful for a first clinical workflow prototype.

## XERJ integration

The app keeps XERJ as a search layer rather than the primary transaction engine.

Usage pattern:

- patient notes are saved into SQLite
- clinical notes or selected documents are also indexed into XERJ
- staff search for symptoms, conditions, or document content through the backend
- search returns matched passages or note content for a clinician or front-end assistant to review

This is useful for AI-driven retrieval without forcing the project to be a heavy search-engine implementation.

## Why this was the right first version

This approach was chosen to keep the project approachable and focused:

- no need to rewrite the whole XERJ backend in Rust
- no need to build a full EMR from day one
- no need to over-engineer privacy, compliance, and medical workflows before the fundamentals are working
- easy to iterate on patient intake and scheduling
- clean path to later add alerting, document upload, chart summaries, and a richer AI assistant layer

## Security and healthcare caution

Although this project is a useful prototype, it should not be treated as a production medical platform without additional work.

Real healthcare deployment should include:

- role-based access control
- stronger authentication and audit trail
- encrypted storage
- HIPAA or equivalent privacy controls
- reviewer workflows for AI-generated summary output
- proper consent and data handling policies

## Roadmap

Near-term next steps:

- more detailed patient intake form
- front-end symptom summary panel
- appointment follow-up status
- AI secretary response summarizing patient needs
- document uploads and PDF indexing
- clinician note templates and triage recommendations
- stronger role-based access and audit logging

Later-stage ideas:

- Postgres migration
- appointment reminder system
- patient portal
- lab result tracking
- provider dashboards
- AI-assisted clinical summarization using retrieved context

## Notes

This repository was created as a lightweight starting point for a practical medical secretary backend, not as a final production specification. The design keeps the application simple, focused, and intentionally separated from the search-engine implementation itself.

The project is best understood as:

- operational workflow software for clinics and virtual labs
- an AI-ready intake and scheduling layer
- a clean Python/FastAPI prototype to iterate on quickly
- a foundation that can later grow into a richer medical assistant system

## License

This project is distributed under the repository’s current license. See the project files for exact licensing details.
