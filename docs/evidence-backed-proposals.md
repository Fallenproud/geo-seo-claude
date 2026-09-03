# Evidence-Backed Proposals

PR-3 defines the commercial proposal contract for turning GEO audits and AI visibility
benchmarks into client-facing recommendations.

## Evidence contract

Every material metric belongs to one of five classes:

| Class | Meaning | Client-facing use |
|---|---|---|
| Observed | Directly measured | State as measured fact |
| Derived | Deterministic calculation | Show formula/input relationship |
| Benchmark | External comparison | Identify source |
| Estimated | Assumption/model input | State assumption |
| Projected | Forward scenario | State assumptions and uncertainty |

## Critical rule

GEO Readiness and AI Visibility are different measurements. A readiness score may justify
an audit or remediation recommendation, but it must not be converted into an invented AI
recommendation rate, citation rate, share of voice, traffic loss, or revenue loss.

## Proposal flow

```text
AUDIT / BENCHMARK
      ↓
EVIDENCE REGISTER
      ↓
COMPETITIVE GAP
      ↓
OPPORTUNITY + ASSUMPTIONS
      ↓
RECOMMENDED WORK
      ↓
PRICING
      ↓
MEASUREMENT PLAN
```

## Financial scenarios

When financial impact is modeled:

`expected_annual_value = Δp × annual_financial_impact`

The inputs must be explicit and classified. The result is a scenario, not a guarantee.

## Verification

Every recommendation should define how it will be re-tested. The preferred commercial
loop is:

`baseline → implementation → repeat benchmark → delta → business outcome`

This establishes the foundation for PR-4 outcome/delta measurement and PR-7/8 actual AI
query benchmarking and share-of-voice measurement.
