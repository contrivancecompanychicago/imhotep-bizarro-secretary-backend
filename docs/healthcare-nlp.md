# IMHOTEP Healthcare NLP integration

The notebook `react_gemini_healthcare_api.ipynb` is a Google Colab demonstration. IMHOTEP ports its Google Cloud Healthcare Natural Language entity-extraction step into the authenticated FastAPI backend; it does not run notebook cells, use LangChain/ReAct, generate medical codes, or make clinical decisions.

## Endpoint

`POST /healthcare/analyze` (requires the same bearer-token authentication as other API routes)

```json
{
  "text": "Fictional note: patient requests an afternoon follow-up appointment."
}
```

The response contains normalized `entities` and `relationships`. Raw input and the complete upstream response are not returned or persisted by this endpoint. Input is limited to 100,000 characters.

## Configuration and credentials

Set `GOOGLE_CLOUD_PROJECT` and optionally `GOOGLE_CLOUD_LOCATION` (defaults to `us-central1`) and `HEALTHCARE_API_TIMEOUT_SECONDS` (defaults to 30). The runtime must have Google Application Default Credentials with permission to call Cloud Healthcare NLP and use the configured project. For local development, configure ADC using your organization's approved Google Cloud process; do not commit credentials or tokens. Enable the Cloud Healthcare API for the project.

Install backend dependencies with `pip install -r backend/requirements.txt`. Run the app from `backend/` using the repository's existing startup instructions.

## Safety and scope

This endpoint extracts text mentions and API-provided relationships only. It does not produce ICD/CPT/DRG/HCPCS assignments, validate coding, summarize a patient's record, or provide diagnosis/treatment advice. Do not treat extraction as clinically verified. Use synthetic text for development. Do not send identifiable health information to an external service unless the organization has approved the service, data handling, access controls, and applicable privacy/compliance requirements. Add human review before any downstream clinical or billing workflow.
