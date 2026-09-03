# AI Visibility Metrics v2

## Purpose

GEO Readiness and observed AI visibility are different measurements.

- **GEO Score** = diagnostic/readiness assessment of the website.
- **AI Visibility Metrics** = observed performance from a defined set of AI queries.

Do not use the GEO Score as evidence that a company is currently recommended or cited by an AI system.

## Canonical metrics

| Metric | Formula | Unit | Provenance |
|---|---|---|---|
| Recommendation Rate | recommended eligible queries / eligible queries | % | observed |
| Mention Rate | mentioned eligible queries / eligible queries | % | observed |
| Citation Rate | cited eligible queries / eligible queries | % | observed |
| AI Share of Voice | target competitive mentions / total competitive mentions | % | derived |
| Entity Recognition Rate | unambiguous target entity recognitions / eligible queries | % | observed |
| Local Intent Coverage | covered local-intent queries / local-intent queries | % | observed |
| Competitor Gap | target rate - competitor rate | percentage points | derived |

All formulas are implemented deterministically in `scripts/ai_visibility_metrics.py`.

## Observation rules

An **eligible query** is a query for which the benchmark runner successfully obtained a response that can be evaluated under the benchmark's protocol. Failed requests, unavailable surfaces, and malformed responses must not silently become negative observations.

If a denominator is zero, the metric is `null` rather than `0`. `0%` means an eligible observation measured no positive outcome; `null` means the metric was not measurable.

### Share of voice

The SOV denominator must use one consistent counting rule across the entire benchmark. For example, if one target mention and three competitor mentions are counted per response, the same rule must be applied to every entity. SOV is therefore derived from observed entity mentions; it is not a model estimate.

### Competitor gap

Competitor Gap is expressed in percentage points. A negative value means the target trails the competitor. A positive value means the target leads.

## Provenance

Every commercial metric must carry one provenance value:

- `observed` — directly measured from captured AI query evidence.
- `derived` — deterministic calculation from observed evidence.
- `estimated` — analyst/model estimate.
- `benchmark` — external comparison dataset.
- `projected` — forward-looking scenario.

Estimated and projected values must never be presented as observed performance.

## Confidence

PR-1 uses a deterministic sample-size label to communicate evidence volume:

| Eligible queries | Label |
|---:|---|
| 50+ | high |
| 20–49 | medium |
| <20 | low |

This is **not** a statistical significance test or confidence interval. Later benchmark work may add statistical uncertainty without changing the metric definitions.

## Backward compatibility

Existing `geo_score` and six-category readiness scores remain valid and unchanged. A v2 audit may add a separate `ai_visibility` section without renaming or reinterpreting existing fields.

Recommended report shape:

```json
{
  "geo_score": 72,
  "ai_visibility": {
    "metrics_version": "2.0",
    "metrics": [],
    "benchmark": {
      "eligible_queries": 50
    }
  }
}
```

The benchmark object and populated metric observations are introduced by subsequent query-benchmark work. PR-1 establishes the canonical vocabulary, formulas, provenance semantics, and deterministic implementation.
