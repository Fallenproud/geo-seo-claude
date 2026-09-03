---
name: geo-prospect
description: >
  Commercial prospect and client CRM for the GEO agency pipeline. Track discovery,
  qualification, proposal, won/lost outcomes, observed AI visibility, opportunity
  value, contacts, competitors, target queries, and next actions.
version: 2.0.0
tags: [geo, business, crm, prospect, pipeline, sales, ai-visibility]
allowed-tools: Read, Write, Bash, Glob
---

# GEO Prospect Manager

## Purpose

Manage prospects and clients through the commercial lifecycle while preserving the
existing JSON CRM. The canonical field model is documented in
`scripts/commercial_prospect.py`.

The CRM is operational state, not evidence. AI visibility fields must retain
provenance and must never imply observed performance when only readiness,
estimates, or projections exist.

## Pipeline

`lead → qualified → proposal → won`

`lost` is a terminal outcome that retains the loss reason for future analysis.

## Commands

| Command | What It Does |
|---|---|
| `/geo prospect new <domain>` | Create a prospect with commercial discovery fields |
| `/geo prospect list` | Show pipeline and commercial metrics |
| `/geo prospect show <id-or-domain>` | Show complete prospect record and history |
| `/geo prospect audit <id-or-domain>` | Run readiness audit and save evidence |
| `/geo prospect note <id-or-domain> "<text>"` | Add dated interaction note |
| `/geo prospect status <id-or-domain> <status>` | Advance or close pipeline stage |
| `/geo prospect won <id-or-domain> <monthly-value>` | Mark won and set recurring value |
| `/geo prospect lost <id-or-domain> "<reason>"` | Mark lost and retain reason |
| `/geo prospect pipeline` | Revenue-weighted pipeline summary |

## Canonical data model

New records should support these fields in addition to all existing legacy fields:

```json
{
  "id": "PRO-001",
  "company": "Example AS",
  "domain": "example.no",
  "status": "lead",
  "country": "Norway",
  "region": "Oslo",
  "city": "Oslo",
  "industry": "Plumbing",
  "lead_source": "google_maps",
  "acquisition_channel": "outbound",
  "contact_name": "",
  "contact_email": "",
  "contact_role": "",
  "target_queries": [],
  "competitor_domains": [],
  "geo_score": null,
  "ai_visibility_score": null,
  "ai_share_of_voice": null,
  "recommendation_rate": null,
  "citation_rate": null,
  "mention_rate": null,
  "local_intent_coverage": null,
  "competitor_gap": null,
  "opportunity_value_monthly": null,
  "opportunity_value_annual": null,
  "monthly_value": null,
  "probability": null,
  "next_action": "Run discovery audit",
  "next_action_at": null,
  "audit_date": null,
  "benchmark_date": null,
  "implementation_status": null,
  "provenance": {},
  "notes": [],
  "created_at": null,
  "updated_at": null
}
```

### Field semantics

- `geo_score`: existing diagnostic/readiness score. Never substitute for observed AI visibility.
- `ai_visibility_score`: observed composite only when a defined benchmark exists.
- `ai_share_of_voice`: derived from consistently counted observed competitive mentions.
- `recommendation_rate`, `citation_rate`, `mention_rate`, `local_intent_coverage`: observed benchmark metrics.
- `competitor_gap`: percentage-point difference between target and named competitor metric.
- `target_queries`: canonical query set to benchmark; preserve exact query text.
- `competitor_domains`: explicit competitive set used for comparison.
- `lead_source` / `acquisition_channel`: acquisition attribution, not inferred unless known.
- `opportunity_value_monthly`: potential recurring value before probability weighting.
- `opportunity_value_annual`: monthly opportunity × 12.
- `monthly_value`: contracted recurring revenue for won clients.
- `probability`: explicit 0–1 close probability used for weighted pipeline reporting.
- `next_action` / `next_action_at`: operational follow-up state.
- `implementation_status`: delivery state after a deal is won.
- `provenance`: per-metric evidence classification using `observed`, `derived`, `estimated`, `benchmark`, or `projected`.

Unknown values are `null`; do not manufacture zeros for unavailable measurements.

## `/geo prospect new <domain>`

1. Create `~/.geo-prospects/prospects.json` if absent.
2. Detect a provisional company name from the domain.
3. Assign the next sequential ID.
4. Capture optional contact information, country/region/city, industry, lead source,
   acquisition channel, target queries, competitors, and opportunity value.
5. Set `status=lead` and a concrete `next_action`.
6. Do not invent contact or financial information.
7. Save the record and suggest the audit/benchmark next step.

## `/geo prospect audit <id-or-domain>`

1. Run `/geo quick <domain>`.
2. Save the existing `geo_score` and audit evidence.
3. Do not populate AI visibility metrics unless actual benchmark evidence exists.
4. Add/update provenance for any populated commercial metric.
5. If the readiness score indicates an opportunity, use it as a diagnostic sales signal,
   not proof of lost AI traffic or revenue.

## Qualification

A prospect may move to `qualified` when there is evidence of a commercial opportunity,
for example a readiness gap, a defined target market, a relevant query set, or observed
AI visibility/competitive gap. Record the evidence in notes rather than relying on score
thresholds alone.

Recommended qualification fields:

- ICP/industry fit
- geography and local intent
- target query set
- competitor set
- readiness findings
- observed AI benchmark, if available
- commercial opportunity estimate and its assumptions
- decision-maker/contact status
- next action and date

## Pipeline valuation

For each open prospect:

`weighted_monthly_pipeline = opportunity_value_monthly × probability`

For recurring revenue:

`annual_recurring_value = monthly_value × 12`

For opportunity scenarios, expected annual value may be represented as:

`expected_annual_value = Δp × annual_financial_impact`

where `Δp` and financial impact are explicit assumptions or observed/derived inputs.
This is an analytical scenario, not an ROI guarantee.

The implementation in `scripts/commercial_prospect.py` performs deterministic validation
and calculation of these values.

## Pipeline output

Show, at minimum:

- count by stage
- committed MRR from `won`
- unweighted pipeline MRR from open opportunities
- probability-weighted pipeline MRR
- annualized committed revenue
- prospects requiring a next action
- top opportunities by weighted value

Do not display missing values as zero unless zero is explicitly recorded.

## Backward compatibility

Existing fields such as `id`, `company`, `domain`, `status`, `geo_score`, `monthly_value`,
`notes`, audit paths, proposal paths, and timestamps remain valid. Legacy records are
normalized with safe defaults by `normalize_prospect()`.

## Storage

```text
~/.geo-prospects/
├── prospects.json
├── audits/
└── proposals/
```

The JSON database remains the single source of truth for this stage. A database/API layer
is intentionally deferred until later architecture work.
