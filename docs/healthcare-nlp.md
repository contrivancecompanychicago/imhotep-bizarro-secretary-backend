# IMHOTEP Healthcare NLP integration

The notebook `react_gemini_healthcare_api.ipynb` is a Google Colab demonstration. IMHOTEP ports its Google Cloud Healthcare Natural Language entity-extraction step into the authenticated FastAPI backend; it does not run notebook cells, use LangChain/ReAct, or make clinical decisions.

## Entity extraction

`POST /healthcare/analyze` (requires the same bearer-token authentication as other API routes)

```json
{
  "text": "Fictional note: patient requests an afternoon follow-up appointment."
}
```

The response contains normalized `entities` and `relationships`. Raw input and the complete upstream response are not returned or persisted by this endpoint. Input is limited to 100,000 characters.

## Code candidates

`POST /healthcare/code-suggest` accepts the same request and returns ICD-10-CM candidates only when the Healthcare NLP response explicitly links an extracted mention to an ICD-10-CM vocabulary code. Candidates are included only after a conservative keyword screen finds diabetes language, foot/toe context, and at least one active ulcer/wound, infection, or ischemia/gangrene keyword in the note; the linked entity text must also contain a complication keyword. Candidates are ordered for review: ulcer/wound first, infection second, then ischemia/gangrene. The response includes the screening terms, matched signals, and candidate evidence.

The keyword screen is a prioritization heuristic, not clinical NLP or a diagnosis. It can miss relevant wording, mishandle complex negation, and does not determine whether conditions are related. A candidate is not a confirmed diagnosis or billable assignment. Empty candidates do not rule out a condition. A qualified clinician/coder must verify the source record, laterality, ulcer site/depth, infection, encounter context, and current official code-set rules. CPT is reported as unavailable: the configured NLP vocabularies do not include CPT, and the endpoint does not guess procedure codes from narrative text.

## Configuration and credentials

Set `GOOGLE_CLOUD_PROJECT` and optionally `GOOGLE_CLOUD_LOCATION` (defaults to `us-central1`) and `HEALTHCARE_API_TIMEOUT_SECONDS` (defaults to 30). The runtime must have Google Application Default Credentials with permission to call Cloud Healthcare NLP and use the configured project. For local development, configure ADC using your organization's approved Google Cloud process; do not commit credentials or tokens. Enable the Cloud Healthcare API for the project.

Install backend dependencies with `pip install -r backend/requirements.txt`. Run the app from `backend/` using the repository's existing startup instructions.

## Safety and scope

These endpoints extract text mentions and API-provided relationships or linked ICD-10-CM vocabulary codes only. They do not generate CPT/DRG/HCPCS assignments, validate coding, summarize a patient's record, or provide diagnosis/treatment advice. Do not treat extraction as clinically verified. Use synthetic text for development. Do not send identifiable health information to an external service unless the organization has approved the service, data handling, access controls, and applicable privacy/compliance requirements. Add human review before any downstream clinical or billing workflow.
