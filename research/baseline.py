"""Offline synthetic retrieval smoke demo. No backend, API key, or dependencies."""
import json
import re


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def rank(query, documents):
    query_tokens = tokens(query)
    scores = [
        (len(query_tokens & tokens(doc["text"])), doc["id"])
        for doc in documents
    ]
    return [doc_id for score, doc_id in sorted(scores, key=lambda item: (-item[0], item[1])) if score > 0]


def main():
    documents = [
        {"id": "SYN-001-N1", "text": "Fictional case SYN-001 requests an afternoon appointment."},
        {"id": "SYN-002-N1", "text": "Fictional case SYN-002 requests a morning appointment."},
        {"id": "SYN-003-N1", "text": "Fictional case SYN-003 needs interpreter assistance."},
    ]
    queries = [
        {"id": "Q1", "query": "afternoon appointment", "relevant": "SYN-001-N1"},
        {"id": "Q2", "query": "interpreter assistance", "relevant": "SYN-003-N1"},
    ]
    rankings = [
        {"query_id": q["id"], "ranked_ids": rank(q["query"], documents), "relevant_id": q["relevant"]}
        for q in queries
    ]
    correct = sum(bool(r["ranked_ids"]) and r["ranked_ids"][0] == r["relevant_id"] for r in rankings)
    print(json.dumps({
        "label": "synthetic smoke demo only; not a study result",
        "method": "token_overlap_v1",
        "query_count": len(queries),
        "top1_accuracy": correct / len(queries),
        "rankings": rankings,
    }, indent=2))


if __name__ == "__main__":
    main()

