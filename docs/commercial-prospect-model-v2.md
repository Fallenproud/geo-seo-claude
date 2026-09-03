# Commercial Prospect Model v2

The commercial CRM separates five concerns: GEO readiness, observed AI visibility, commercial opportunity, sales pipeline, and contracted revenue.

## Canonical fields

Identity and market: `company`, `domain`, `country`, `region`, `city`, `industry`, `target_queries`, `competitor_domains`.

Acquisition and contacts: `lead_source`, `acquisition_channel`, `contact_name`, `contact_email`, `contact_role`.

Evidence: `geo_score`, `ai_visibility_score`, `ai_share_of_voice`, `recommendation_rate`, `citation_rate`, `mention_rate`, `local_intent_coverage`, `competitor_gap`, `audit_date`, `benchmark_date`, `provenance`.

Economics and operations: `opportunity_value_monthly`, `opportunity_value_annual`, `monthly_value`, `probability`, `next_action`, `next_action_at`, `implementation_status`.

## Valuation

`weighted_pipeline_mrr = opportunity_value_monthly × probability`

`opportunity_arr = opportunity_value_monthly × 12`

`expected_annual_value = Δp × annual_financial_impact`

These are deterministic scenario calculations. They are not guarantees of conversion, traffic, rankings, citations, or revenue.

## Data governance

Unknown values remain `null`. Do not convert unavailable measurements into zero. AI visibility metrics must use the provenance vocabulary established by Metrics v2: `observed`, `derived`, `estimated`, `benchmark`, or `projected`.

## Compatibility

Legacy JSON records remain valid. `normalize_prospect()` supplies safe defaults for newly introduced fields. The JSON CRM remains the system of record until a later API/database stage.
