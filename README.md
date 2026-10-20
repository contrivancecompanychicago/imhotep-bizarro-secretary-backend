# IMHOTEP Bizarros

IMHOTEP Bizarros is the Front End Medical Secretary AI for Emergent APHID.

Status: v0 (initial backend scaffold)

This repository is a fresh implementation created to serve as a clean product backend and knowledge-base workspace. The project is intentionally separated from the upstream reference material and preserves attribution to the original source work used for learning and adaptation.

## Purpose
- Provide a versioned backend foundation for medical secretary workflows
- Store operational knowledge and structured reference notes
- Support future patient intake, summarization, and document workflow features
- Maintain support for diverse document formats like CSV, JSON, OWL, PDF, and RDF
- Model Chicago medically underserved communities with Type 2 Diabetes care-gap tracking
- Export patient knowledge as CSV, JSON, and RDF for downstream workflows

## Supported document formats
- CSV
- JSON
- OWL
- PDF
- RDF

## Chicago medically underserved focus
The v0 graph includes patient records and neighborhood candidates aligned to underserved Chicago communities, including:
- West Garfield Park
- Englewood
- North Lawndale
- Auburn Gresham
- South Shore
- Humboldt Park

These records support operational triage, care-gap mapping, and neighborhood-aware clinical summarization.

## Attributed Source
This repository draws inspiration from public reference work and research materials related to the DocScribe / IMHOTEP-Bizarros-DocScribe ecosystem, used as a knowledge base and adaptation reference. It is not a direct replacement or official fork of the upstream repository.

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

- GET /health
- GET /api/v0/documents
- POST /api/v0/documents/update
- GET /api/v0/graph/summary
- GET /api/v0/graph/candidates
- GET /api/v0/graph/patients?community=Chicago
- GET /api/v0/exports/csv
- GET /api/v0/exports/json
- GET /api/v0/exports/rdf
- POST /api/v0/summary

## Version

```text
0.1.0
```
