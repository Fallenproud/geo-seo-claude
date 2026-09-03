# PR-2 — Commercial Prospect Model

## Objective

Harden the CRM-lite prospect record into the canonical commercial operating model without introducing a database or breaking legacy records.

## Acceptance criteria

- Prospect identity, geography, industry, acquisition source, contacts, target queries, and competitors are represented.
- Readiness and observed AI visibility remain separate fields.
- Opportunity value and contracted recurring value remain separate.
- Probability-weighted pipeline calculations are deterministic.
- Legacy JSON records normalize safely.
- Commercial values can carry provenance.
- Unknown measurements remain null rather than being fabricated as zero.
- Unit tests cover legacy normalization, serialization, valuation, and invalid inputs.

## Scope boundary

PR-2 does not implement AI query collection, live platform integrations, revenue attribution, or a SaaS database. Those belong to subsequent PRs.
