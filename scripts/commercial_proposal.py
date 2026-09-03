"""Evidence-aware proposal primitives for the commercial GEO workflow.

The proposal layer consumes measured audit/benchmark evidence and explicitly labels
assumptions. It does not turn readiness scores into claims about traffic, rankings,
AI recommendations, or revenue.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional


class EvidenceType(str, Enum):
    OBSERVED = "observed"
    DERIVED = "derived"
    BENCHMARK = "benchmark"
    ESTIMATED = "estimated"
    PROJECTED = "projected"


@dataclass(frozen=True)
class Evidence:
    metric: str
    value: Any
    evidence_type: EvidenceType
    source: Optional[str] = None
    observed_at: Optional[str] = None
    confidence: Optional[str] = None
    assumption: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric": self.metric,
            "value": self.value,
            "evidence_type": self.evidence_type.value,
            "source": self.source,
            "observed_at": self.observed_at,
            "confidence": self.confidence,
            "assumption": self.assumption,
        }


@dataclass(frozen=True)
class ProposalContext:
    company: str
    domain: str
    evidence: list[Evidence] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    tier: Optional[str] = None
    monthly_price: Optional[float] = None

    def evidence_by_type(self, evidence_type: EvidenceType) -> list[Evidence]:
        return [item for item in self.evidence if item.evidence_type == evidence_type]

    def has_observed_ai_visibility(self) -> bool:
        ai_metrics = {
            "ai_visibility_score",
            "ai_share_of_voice",
            "recommendation_rate",
            "citation_rate",
            "mention_rate",
        }
        return any(
            item.metric in ai_metrics and item.evidence_type == EvidenceType.OBSERVED
            for item in self.evidence
        )


def evidence_from_mapping(data: Mapping[str, Any]) -> list[Evidence]:
    """Normalize a metric mapping while preserving provenance.

    Accepted values may be scalars or mappings containing ``value``, ``evidence_type``
    and optional source/date/confidence/assumption metadata.
    """
    result: list[Evidence] = []
    for metric, raw in data.items():
        if isinstance(raw, Mapping):
            value = raw.get("value")
            kind = raw.get("evidence_type", raw.get("provenance", "observed"))
            result.append(
                Evidence(
                    metric=metric,
                    value=value,
                    evidence_type=EvidenceType(kind),
                    source=raw.get("source"),
                    observed_at=raw.get("observed_at"),
                    confidence=raw.get("confidence"),
                    assumption=raw.get("assumption"),
                )
            )
        else:
            # Bare values are treated as observed only when supplied by an audit/benchmark
            # adapter. Callers that cannot establish observation should provide metadata.
            result.append(Evidence(metric, raw, EvidenceType.OBSERVED))
    return result


def format_evidence_line(item: Evidence) -> str:
    label = item.evidence_type.value.capitalize()
    suffix = f" — source: {item.source}" if item.source else ""
    if item.assumption:
        suffix += f" — assumption: {item.assumption}"
    return f"- **{item.metric}**: {item.value} ({label}){suffix}"


def build_evidence_table(evidence: list[Evidence]) -> str:
    if not evidence:
        return "| Metric | Value | Evidence | Source |\n|---|---:|---|---|\n| — | — | Not measured | — |"
    rows = ["| Metric | Value | Evidence | Source |", "|---|---:|---|---|"]
    for item in evidence:
        rows.append(
            f"| {item.metric} | {item.value} | {item.evidence_type.value} | {item.source or '—'} |"
        )
    return "\n".join(rows)


def scenario_value(delta_probability: float, annual_financial_impact: float) -> float:
    """Calculate an explicitly assumed scenario value; never a guaranteed ROI."""
    if not 0 <= delta_probability <= 1:
        raise ValueError("delta_probability must be between 0 and 1")
    if annual_financial_impact < 0:
        raise ValueError("annual_financial_impact must be non-negative")
    return round(delta_probability * annual_financial_impact, 2)
