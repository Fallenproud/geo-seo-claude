"""Deterministic commercial AI-visibility metrics.

The existing GEO Score measures site readiness. This module defines the separate
measurement layer used once observed AI query results are available (PR-7/8).
It deliberately does not invent observations: missing observations return None.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Iterable, Mapping, Optional


class Provenance(str, Enum):
    OBSERVED = "observed"
    DERIVED = "derived"
    ESTIMATED = "estimated"
    BENCHMARK = "benchmark"
    PROJECTED = "projected"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


def _rate(numerator: int, denominator: int) -> Optional[float]:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 4)


def _pct(rate: Optional[float]) -> Optional[float]:
    return None if rate is None else round(rate * 100, 2)


def recommendation_rate(recommended: int, eligible_queries: int) -> Optional[float]:
    """Percentage of eligible queries where the target was recommended."""
    return _pct(_rate(recommended, eligible_queries))


def mention_rate(mentioned: int, eligible_queries: int) -> Optional[float]:
    """Percentage of eligible queries where the target was mentioned."""
    return _pct(_rate(mentioned, eligible_queries))


def citation_rate(cited: int, eligible_queries: int) -> Optional[float]:
    """Percentage of eligible queries where the target was cited."""
    return _pct(_rate(cited, eligible_queries))


def ai_share_of_voice(target_mentions: int, total_competitive_mentions: int) -> Optional[float]:
    """Target share of observed competitive mentions/recommendations.

    The denominator must be explicitly defined by the caller's benchmark: it is
    the sum of competitive entity mentions counted under the same rule.
    """
    return _pct(_rate(target_mentions, total_competitive_mentions))


def entity_recognition_rate(recognized: int, eligible_queries: int) -> Optional[float]:
    return _pct(_rate(recognized, eligible_queries))


def local_intent_coverage(covered: int, local_intent_queries: int) -> Optional[float]:
    return _pct(_rate(covered, local_intent_queries))


def competitor_gap(target_rate: float, competitor_rate: float) -> float:
    """Target minus competitor percentage-point rate.

    Positive means the target leads; negative means the competitor leads.
    Both inputs are percentage values, e.g. 20.0 and 35.0.
    """
    return round(target_rate - competitor_rate, 2)


def confidence_for_sample(eligible_queries: int) -> Confidence:
    """Deterministic sample-size confidence label, not statistical significance."""
    if eligible_queries >= 50:
        return Confidence.HIGH
    if eligible_queries >= 20:
        return Confidence.MEDIUM
    return Confidence.LOW


@dataclass(frozen=True)
class MetricValue:
    name: str
    value: Optional[float]
    unit: str
    provenance: Provenance
    confidence: Optional[Confidence] = None
    sample_size: Optional[int] = None
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        result = asdict(self)
        result["provenance"] = self.provenance.value
        if self.confidence is not None:
            result["confidence"] = self.confidence.value
        return result


def build_visibility_metrics(
    *,
    eligible_queries: int,
    recommended: int = 0,
    mentioned: int = 0,
    cited: int = 0,
    target_entity_recognized: int = 0,
    local_intent_covered: int = 0,
    local_intent_queries: int = 0,
    target_competitive_mentions: int = 0,
    total_competitive_mentions: int = 0,
) -> list[MetricValue]:
    """Build the canonical PR-1 metric set from observed query outcomes."""
    confidence = confidence_for_sample(eligible_queries)
    return [
        MetricValue("recommendation_rate", recommendation_rate(recommended, eligible_queries), "%", Provenance.OBSERVED, confidence, eligible_queries),
        MetricValue("mention_rate", mention_rate(mentioned, eligible_queries), "%", Provenance.OBSERVED, confidence, eligible_queries),
        MetricValue("citation_rate", citation_rate(cited, eligible_queries), "%", Provenance.OBSERVED, confidence, eligible_queries),
        MetricValue("ai_share_of_voice", ai_share_of_voice(target_competitive_mentions, total_competitive_mentions), "%", Provenance.DERIVED, confidence, eligible_queries),
        MetricValue("entity_recognition_rate", entity_recognition_rate(target_entity_recognized, eligible_queries), "%", Provenance.OBSERVED, confidence, eligible_queries),
        MetricValue("local_intent_coverage", local_intent_coverage(local_intent_covered, local_intent_queries), "%", Provenance.OBSERVED, confidence, local_intent_queries),
    ]


def metric_map(metrics: Iterable[MetricValue]) -> Mapping[str, MetricValue]:
    return {metric.name: metric for metric in metrics}
