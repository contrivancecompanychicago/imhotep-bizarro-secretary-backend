# Firebase Research Import Checkpoint

Date: 2026-11-05

## Scope

Fictional IMHOTEP development benchmark.
These experiments are not held-out evaluations or evidence of improved
access to care or clinical effectiveness.

## Stored data

- Documents: 5
- Reviewed questions: 14
- Relevance links: 11
- Experiments: 5
- Result rows: 42

| Experiment | Result rows |
|---|---:|
| IMHOTEP-DEV-001 | 18 |
| IMHOTEP-DEV-002 | 12 |
| IMHOTEP-DEV-003 | 4 |
| IMHOTEP-DEV-004 | 4 |
| IMHOTEP-DEV-005 | 4 |

## Firebase configuration

- Project: gupsy-288118
- SQL Connect service: gupsy-288118-2-service
- Region: us-east4
- Dataset version: IMHOTEP-DEV-001
- Dataset ID: df8c3cef146a40359ae8dca89bffd2a4

| Experiment | Firebase ID |
|---|---|
| IMHOTEP-DEV-001 | 113fbd4ad60e49b1b54b456512212182 |
| IMHOTEP-DEV-002 | 3f9a5057104a45d4a45dd4a31e44605a |
| IMHOTEP-DEV-003 | aa0eb11f9f1c4a1f85120f7348925e6b |
| IMHOTEP-DEV-004 | 2d601a0265854d0b84c4e57d139ae957 |
| IMHOTEP-DEV-005 | 366f9d60830a40ea94b6d4ed2c5a1eb2 |

## Verification

All 42 Firebase result rows were visually read back through console
screenshots and compared with recorded rankings and correctness values.
This was a manual comparison, not an automated database comparison.

The SQLite backup passed SHA-256 verification, integrity checks,
foreign-key checks, and expected table counts.

Backup: results/IMHOTEP_DEV_001_005_complete.sqlite

SHA-256:
17ef0ccf49b795a9429519c84d37accc609d601d96611d0b9bcd22c3f551d503

## Preservation and limitations

GitHub JSON files and SQLite preserve the full experiment records,
including DEV-005 retrieval function sources.

Firebase contains the manually imported questions, relevance links,
experiment records, and result values. Full source metadata was not
imported into Firebase.

SQLite and Firebase are not automatically synchronized.
Firebase createdAt values record cloud-entry creation times, not
original experiment execution times.
