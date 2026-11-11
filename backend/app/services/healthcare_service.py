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

    Coding candidates are surfaced only when the upstream response explicitly
    links a mention to an ICD-10-CM vocabulary code. This service does not
    infer codes, generate CPT codes, or make clinical decisions.
    """

    API_BASE_URL = "https://healthcare.googleapis.com/v1"
    ICD10_VOCABULARIES = {"ICD10CM", "ICD-10-CM"}

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

    def suggest_codes(self, text: str) -> dict[str, Any]:
        """Surface only ICD-10-CM codes explicitly linked by Healthcare NLP.

        CPT is not among the configured NLP vocabularies and is deliberately
        reported as unavailable instead of guessed from a narrative.
        """
        response = self.analyze_entities(text)
        mentions = response.get("entityMentions", [])
        vocabulary_entities = response.get("entities", [])
        if not isinstance(mentions, list):
            mentions = []
        if not isinstance(vocabulary_entities, list):
            vocabulary_entities = []

        evidence_by_entity: dict[str, list[str]] = {}
        for mention in mentions:
            if not isinstance(mention, dict) or mention.get("entityId") is None:
                continue
            mention_text = mention.get("text")
            content = mention_text.get("content") if isinstance(mention_text, dict) else None
            if isinstance(content, str) and content.strip():
                evidence_by_entity.setdefault(str(mention["entityId"]), []).append(content.strip())

        candidates: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for entity in vocabulary_entities:
            if not isinstance(entity, dict) or entity.get("entityId") is None:
                continue
            entity_id = str(entity["entityId"])
            evidence = list(dict.fromkeys(evidence_by_entity.get(entity_id, [])))
            if not evidence:
                continue

            vocabulary_codes = entity.get("vocabularyCodes", [])
            if not isinstance(vocabulary_codes, list):
                continue
            for vocabulary_code in vocabulary_codes:
                if not isinstance(vocabulary_code, dict):
                    continue
                vocabulary_name = str(vocabulary_code.get("vocabularyName", ""))
                if vocabulary_name.upper() not in self.ICD10_VOCABULARIES:
                    continue
                code = vocabulary_code.get("vocabularyCode")
                if not isinstance(code, str) or not code.strip():
                    continue
                key = (vocabulary_name.upper(), code.strip())
                if key in seen:
                    continue
                seen.add(key)
                candidates.append(
                    {
                        "code_system": "ICD-10-CM",
                        "code": code.strip(),
                        "display": str(entity.get("preferredTerm") or ""),
                        "evidence": evidence,
                        "review_required": True,
                    }
                )

        return {
            "focus": "diabetes-related foot complication",
            "code_candidates": candidates,
            "unavailable_code_systems": [
                {
                    "code_system": "CPT",
                    "reason": "CPT is not provided by the configured Healthcare NLP vocabularies; no procedure code was inferred.",
                }
            ],
            "coding_review_required": True,
            "notice": (
                "These are extraction-linked candidates, not confirmed diagnoses or billable coding. "
                "A qualified clinician/coder must verify the record, laterality, ulcer depth, "
                "infection status, encounter context, and current code-set rules. "
                "No code is suggested when the upstream service supplies no linked code."
            ),
        }


__all__ = ["HealthcareNLPError", "HealthcareNLPService"]
