import os

import requests

XERJ_URL = os.getenv("XERJ_URL", "http://localhost:9200")


def index_note(patient_id: int, title: str, content: str):
    payload = {
        "title": title,
        "content": content,
        "patient_id": patient_id,
        "type": "clinical_note",
    }
    doc_id = f"note-{patient_id}-{title.lower().replace(' ', '-')}"
    response = requests.put(f"{XERJ_URL}/clinical-notes/_doc/{doc_id}", json=payload, timeout=10)
    return response.status_code, response.json()


def search_documents(query: str, limit: int = 5):
    body = {
        "size": limit,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content", "patient_id"],
            }
        },
    }
    response = requests.post(f"{XERJ_URL}/clinical-notes/_search", json=body, timeout=10)
    return response.json()
