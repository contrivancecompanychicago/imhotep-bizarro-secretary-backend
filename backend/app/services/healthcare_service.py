from __future__ import annotations

from typing import Any
from urllib.parse import quote

import google.auth
import requests
from google.auth.transport.requests import Request


class HealthcareNLPError(RuntimeError):
    """Safe, client-facing error from the Healthcare NLP integration."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


class HealthcareNLPService:
    """Client for Google Cloud Healthcare Natural Language entity analysis.

    The service returns extracted mentions and relationships only. It does not
    generate diagnoses, treatment advice, or medical-code assignments.
    """

    API_BASE_URL = "https://healthcare.googleapis.com/v1"

    def __init__(
        self,
        project_id: str | None,
        location: str = "us-central1",
        timeout_seconds: int = 30,
        session: requests.Session | None = None,
    ) -> None:
        self.project_id = project_id
        self.location = location
        self.timeout_seconds = timeout_seconds
        self.session = session or requests.Session()

    def analyze_entities(self, text: str) -> dict[str, Any]:
        if not self.project_id:
            raise HealthcareNLPError(
                "Healthcare NLP is not configured. Set GOOGLE_CLOUD_PROJECT.",
                status_code=503,
            )

        try:
            credentials, _ = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            credentials.refresh(Request())
        except Exception as exc:
            raise HealthcareNLPError(
                "Google Cloud credentials are unavailable or could not be refreshed.",
                status_code=503,
            ) from exc

        project = quote(self.project_id, safe="")
        location = quote(self.location, safe="")
        url = (
            f"{self.API_BASE_URL}/projects/{project}/locations/{location}/"
            "services/nlp:analyzeEntities"
        )
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "X-Goog-User-Project": self.project_id,
            "Accept": "application/json",
        }
        payload = {
            "documentContent": text,
            "licensedVocabularies": ["SNOMEDCT_US", "ICD10CM"],
        }

        try:
            response = self.session.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            result = response.json()
        except requests.Timeout as exc:
            raise HealthcareNLPError("Healthcare NLP request timed out.", 504) from exc
        except requests.RequestException as exc:
            raise HealthcareNLPError(
                "Healthcare NLP request failed. Check the API and project permissions.",
                502,
            ) from exc
        except ValueError as exc:
            raise HealthcareNLPError(
                "Healthcare NLP returned an invalid response.", 502
            ) from exc

        if not isinstance(result, dict):
            raise HealthcareNLPError("Healthcare NLP returned an invalid response.", 502)
        return result

    def analyze(self, text: str) -> dict[str, list[dict[str, Any]]]:
        """Return normalized entities and relationships without echoing raw text."""
        response = self.analyze_entities(text)
        mentions = response.get("entityMentions", [])
        if not isinstance(mentions, list):
            mentions = []

        entities: list[dict[str, Any]] = []
        by_id: dict[str, dict[str, Any]] = {}
        for mention in mentions:
            if not isinstance(mention, dict):
                continue
            mention_id = mention.get("mentionId")
            mention_text = mention.get("text")
            content = mention_text.get("content") if isinstance(mention_text, dict) else None
            if mention_id is None or not isinstance(content, str) or not content.strip():
                continue
            entity = {
                "id": str(mention_id),
                "type": mention.get("type", "UNKNOWN"),
                "text": content.strip(),
            }
            entities.append(entity)
            by_id[entity["id"]] = entity

        raw_relationships = response.get("relationships", [])
        if not isinstance(raw_relationships, list):
            raw_relationships = []

        relationships: list[dict[str, str]] = []
        for relationship in raw_relationships:
            if not isinstance(relationship, dict):
                continue
            subject_id = relationship.get("subjectId")
            object_id = relationship.get("objectId")
            if subject_id is None or object_id is None:
                continue
            subject_key, object_key = str(subject_id), str(object_id)
            if subject_key not in by_id or object_key not in by_id:
                continue
            relationships.append(
                {
                    "subject_id": subject_key,
                    "object_id": object_key,
                    "type": str(
                        relationship.get("type")
                        or relationship.get("relationshipType")
                        or "RELATED_TO"
                    ),
                }
            )

        return {"entities": entities, "relationships": relationships}


__all__ = ["HealthcareNLPError", "HealthcareNLPService"]
