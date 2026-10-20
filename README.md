# IMHOTEP Bizarros

IMHOTEP Bizarros is the Front End Medical Secretary AI for Emergent APHID.

Status: v0 (initial backend scaffold)

This repository is a fresh implementation created to serve as a clean product backend and knowledge-base workspace. The project is intentionally separated from the upstream reference material and preserves attribution to the original source work used for learning and adaptation.

## Purpose
- Provide a versioned backend foundation for medical secretary workflows
- Store operational knowledge and structured reference notes
- Support future patient intake, summarization, and document workflow features

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
- POST /api/v0/summary

## Version

```text
0.1.0
```
