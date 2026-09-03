"""Canonical commercial prospect model for the GEO sales pipeline.

Storage-agnostic model for discovery, qualification, benchmarking, proposal,
and retention workflows. Existing JSON CRM records remain backward compatible.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Optional

class ProspectStatus(str, Enum):
    LEAD = "lead"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    WON = "won"
    LOST = "lost"

class Provenance(str, Enum):
    OBSERVED = "observed"
    DERIVED = "derived"
    ESTIMATED = "estimated"
    BENCHMARK = "benchmark"
    PROJECTED = "projected"

@dataclass(frozen=True)
class Prospect:
    id: str
    company: str
    domain: str
    status: ProspectStatus = ProspectStatus.LEAD
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    industry: Optional[str] = None
    lead_source: Optional[str] = None
    acquisition_channel: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_role: Optional[str] = None
    target_queries: list[str] = field(default_factory=list)
    competitor_domains: list[str] = field(default_factory=list)
    geo_score: Optional[float] = None
    ai_visibility_score: Optional[float] = None
    ai_share_of_voice: Optional[float] = None
    recommendation_rate: Optional[float] = None
    citation_rate: Optional[float] = None
    mention_rate: Optional[float] = None
    local_intent_coverage: Optional[float] = None
    competitor_gap: Optional[float] = None
    opportunity_value_monthly: Optional[float] = None
    opportunity_value_annual: Optional[float] = None
    monthly_value: Optional[float] = None
    probability: Optional[float] = None
    next_action: Optional[str] = None
    next_action_at: Optional[str] = None
    audit_date: Optional[str] = None
    benchmark_date: Optional[str] = None
    implementation_status: Optional[str] = None
    provenance: dict[str, Provenance] = field(default_factory=dict)
    notes: list[dict[str, str]] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["status"] = self.status.value
        result["provenance"] = {key: value.value for key, value in self.provenance.items()}
        return result

def weighted_pipeline_value(monthly_value: float, probability: float) -> float:
    if monthly_value < 0 or not 0 <= probability <= 1:
        raise ValueError("monthly_value must be non-negative and probability must be between 0 and 1")
    return round(monthly_value * probability, 2)

def annual_value(monthly_value: float) -> float:
    if monthly_value < 0:
        raise ValueError("monthly_value must be non-negative")
    return round(monthly_value * 12, 2)

def expected_annual_value(delta_probability: float, annual_financial_impact: float) -> float:
    if not 0 <= delta_probability <= 1 or annual_financial_impact < 0:
        raise ValueError("delta_probability must be 0..1 and annual_financial_impact must be non-negative")
    return round(delta_probability * annual_financial_impact, 2)

def normalize_prospect(data: dict[str, Any]) -> Prospect:
    values = dict(data)
    values["status"] = ProspectStatus(values.get("status", "lead"))
    values.setdefault("target_queries", [])
    values.setdefault("competitor_domains", [])
    values.setdefault("provenance", {})
    values.setdefault("notes", [])
    values["provenance"] = {key: Provenance(value) for key, value in values["provenance"].items()}
    allowed = set(Prospect.__dataclass_fields__)
    return Prospect(**{key: value for key, value in values.items() if key in allowed})
