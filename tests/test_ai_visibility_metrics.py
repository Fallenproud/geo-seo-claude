import unittest

from scripts.ai_visibility_metrics import (
    Confidence,
    Provenance,
    ai_share_of_voice,
    build_visibility_metrics,
    citation_rate,
    competitor_gap,
    confidence_for_sample,
    local_intent_coverage,
    recommendation_rate,
)


class TestAIVisibilityMetrics(unittest.TestCase):
    def test_rates_are_percentages(self):
        self.assertEqual(recommendation_rate(5, 20), 25.0)
        self.assertEqual(citation_rate(3, 20), 15.0)
        self.assertEqual(local_intent_coverage(7, 10), 70.0)

    def test_zero_denominator_is_unknown(self):
        self.assertIsNone(recommendation_rate(0, 0))
        self.assertIsNone(ai_share_of_voice(2, 0))

    def test_sov_uses_same_observed_denominator(self):
        self.assertEqual(ai_share_of_voice(6, 40), 15.0)

    def test_competitor_gap_is_percentage_points(self):
        self.assertEqual(competitor_gap(15.0, 45.0), -30.0)
        self.assertEqual(competitor_gap(55.0, 40.0), 15.0)

    def test_confidence_is_sample_size_label_only(self):
        self.assertEqual(confidence_for_sample(10), Confidence.LOW)
        self.assertEqual(confidence_for_sample(20), Confidence.MEDIUM)
        self.assertEqual(confidence_for_sample(50), Confidence.HIGH)

    def test_canonical_set_has_provenance(self):
        metrics = build_visibility_metrics(
            eligible_queries=50,
            recommended=10,
            mentioned=20,
            cited=8,
            target_entity_recognized=45,
            local_intent_covered=12,
            local_intent_queries=15,
            target_competitive_mentions=10,
            total_competitive_mentions=50,
        )
        self.assertEqual(len(metrics), 6)
        self.assertEqual(metrics[0].provenance, Provenance.OBSERVED)
        self.assertEqual(metrics[3].provenance, Provenance.DERIVED)
        self.assertEqual(metrics[0].confidence, Confidence.HIGH)
        self.assertEqual(metrics[0].value, 20.0)


if __name__ == "__main__":
    unittest.main()
