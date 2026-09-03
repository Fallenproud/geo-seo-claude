# Commercial Prospect Model v2

PR-2 turns the existing CRM-lite record into the canonical commercial operating model.
It remains JSON-backed and storage-agnostic.

## Separation of concerns

| Layer | Meaning |
|---|---|
| GEO Readiness | Website diagnostic/readiness evidence |
| AI Visibility | Observed benchmark performance |
| Commercial Opportunity | Estimated potential value and assumptions |
| Pipeline | Probability-weighted sales state |
| Revenue | Contracted recurring value for won clients |

A readiness score is never a substitute for observed AI performance. An opportunity estimate is never presented as realized revenue.

## Canonical commercial dimensions

- Identity: company, domain, geography, industry
- Acquisition: lead source, acquisition channel
- Contacts: name, email, role
- Market: target queries, competitor domains
- Evidence: GEO score, AI visibility metrics, audit/benchmark dates
- Economics: opportunity MRR, opportunity ARR, contracted MRR, close probability
- Operations: next action/date, implementation status
- Governance: per-value provenance and dated notes

## Valuation

`weighted pipeline MRR = opportunity MRR × probability`

`opportunity ARR = opportunity MRR × 12`

For explicit risk/opportunity scenarios:

`expected annual value = Δp × annual financial impact`

All assumptions must be labelled. These calculations quantify scenarios; they do not promise conversion, traffic, rankings, citations, or revenue.

## Backward compatibility

Legacy records can continue to contain only their original fields. The canonical normalizer applies safe defaults to newly introduced fields. Existing audit and proposal paths are preserved.

## Next stages

PR-3 will make proposal generation evidence-aware. PR-7/8 will populate AI visibility and competitive fields from actual query benchmarks. PR-9 will extend the opportunity model with market/revenue inputs.
