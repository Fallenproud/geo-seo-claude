---
name: geo-proposal
description: >
  Generate evidence-backed, client-ready GEO service proposals from audit, benchmark,
  prospect, and competitor data. Separates observed evidence from derived metrics,
  benchmarks, estimates, and projections. Use for proposals, offers, quotes, and
  commercial follow-up after a GEO audit or AI visibility benchmark.
version: 2.0.0
tags: [geo, business, proposal, sales, pricing, client, evidence]
allowed-tools: Read, Write, Bash, Glob, WebFetch
---

# Evidence-Backed GEO Proposal Generator

## Purpose

Generate a client-ready proposal that converts measured GEO/AI-search findings into a
commercial plan without presenting assumptions as facts.

The proposal must keep these layers separate:

1. **Observed** — directly measured audit or benchmark result.
2. **Derived** — deterministic calculation from observed inputs.
3. **Benchmark** — external comparison or reference value.
4. **Estimated** — explicit assumption or modeled input.
5. **Projected** — forward-looking scenario based on stated assumptions.

A readiness score is diagnostic evidence. It is not proof of lost traffic, rankings,
AI recommendations, citations, or revenue.

## Command

```text
/geo proposal <domain-or-audit-file> [--tier basic|standard|premium] [--client-name "Name"] [--monthly EUR]
```

## Required workflow

### 1. Load source evidence

Read the prospect record and relevant audit/benchmark files when available.
Capture company/domain, industry/geography, GEO readiness, critical findings, target
queries, competitor set, observed AI visibility metrics, dates, provenance, and confidence.

If AI benchmark data is absent, say that AI visibility is **not yet measured**. Never
invent an AI visibility value from a GEO readiness score.

### 2. Build the evidence register

Every material metric must have an evidence classification. Use
`scripts/commercial_proposal.py` for normalized evidence objects and deterministic
scenario calculations.

Recommended table:

| Metric | Value | Evidence | Source |
|---|---:|---|---|
| GEO Readiness | 42/100 | Observed | audit dated YYYY-MM-DD |
| AI Share of Voice | 12% | Observed | query benchmark |
| Competitor Gap | -18 pp | Derived | benchmark comparison |
| Industry reference | 25% | Benchmark | named source |
| Revenue impact | €X | Estimated | stated assumptions |

Do not silently upgrade evidence from one class to another.

### 3. Translate findings into business language

For every priority provide: **What we measured**, **Why it matters**, **What we will
change**, and **How we will verify it**. Avoid unsupported causal claims.

### 4. Select pricing

Use Basic / Standard / Premium as configurable commercial defaults, not market facts.
The recommendation may consider readiness severity, competitive intensity, scope, and
observed opportunity evidence.

Defaults:
- Basic — €2,500/month
- Standard — €5,000/month
- Premium — €9,500/month

A supplied price overrides the defaults.

### 5. Model opportunity carefully

Distinguish observed financial impact, derived values, benchmark inputs, estimated
assumptions, and projected scenarios.

`expected_annual_value = Δp × annual_financial_impact`

This is a scenario value, **not a guaranteed ROI or payback period**.

Do not claim traffic increases, conversion lifts, rankings, citation lifts, or revenue
gains unless observed. Future values must be scenarios with assumptions and uncertainty.

### 6. Generate the proposal

Use this structure:

```text
# GEO / AI Search Visibility Proposal
## [COMPANY]

Executive Summary
Current Measured State
Evidence Register
Competitive Gap
Opportunity & Assumptions
Recommended Work
Service Packages & Investment
90-Day Implementation Plan
Measurement & Verification Plan
Assumptions / Limitations
Next Steps
Terms
```

**Executive Summary:** current measured position, strongest evidence-backed opportunity,
and recommendation. If no AI benchmark exists, make benchmarking the first measurement step.

**Current Measured State:** show GEO readiness and observed AI visibility separately,
with dates and sources.

**Competitive Gap:** use only a defined competitor set and consistently measured query set.
Calculated gaps are derived evidence.

**Opportunity & Assumptions:** keep financial inputs and projections separate from measured results.

**Recommended Work:** map each recommendation to a finding and verification method.

**Measurement & Verification Plan:** define repeatable KPIs including GEO Readiness,
AI Visibility, AI Share of Voice, Recommendation Rate, Citation Rate, Mention Rate,
Local Intent Coverage, Competitor Gap, and commercial outcomes when available.

## Forbidden proposal patterns

Do not present these as facts without current, cited evidence:

- fixed AI traffic growth percentages
- fixed conversion multipliers
- user-count claims for AI platforms
- guaranteed score improvements
- guaranteed rankings or citations
- “revenue at risk” without a defined financial model
- “payback in X months” without explicit inputs
- unsupported industry averages

External benchmarks must be labelled **Benchmark**, sourced, and kept separate from
client-specific observations.

## Output

Save to `~/.geo-prospects/proposals/<domain>-proposal-<date>.md`.

If the prospect exists, set status to `proposal` only after generation, save the proposal
path, preserve evidence/benchmark dates, and retain provenance.

## Quality gate

- [ ] Every client-specific metric has source/date or explicit evidence type.
- [ ] AI visibility is never inferred from readiness.
- [ ] Competitor comparisons state the query and competitor sets.
- [ ] Estimates and projections are labelled.
- [ ] Financial scenarios expose assumptions.
- [ ] No unsupported guaranteed outcome appears.
- [ ] Pricing is treated as configuration, not market fact.
- [ ] Measurement defines how claims will be re-tested.
