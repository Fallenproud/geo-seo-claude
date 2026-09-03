import unittest

from scripts.commercial_proposal import (
    EvidenceType,
    ProposalContext,
    build_evidence_table,
    evidence_from_mapping,
    scenario_value,
)


class TestCommercialProposal(unittest.TestCase):
    def test_mapping_preserves_provenance_and_metadata(self):
        evidence = evidence_from_mapping({
            "ai_share_of_voice": {
                "value": 0.12,
                "evidence_type": "observed",
                "source": "query-benchmark",
                "observed_at": "2026-09-03",
            },
            "industry_reference": {
                "value": 0.25,
                "evidence_type": "benchmark",
                "source": "industry-report",
            },
        })
        self.assertEqual(evidence[0].evidence_type, EvidenceType.OBSERVED)
        self.assertEqual(evidence[0].source, "query-benchmark")
        self.assertEqual(evidence[1].evidence_type, EvidenceType.BENCHMARK)

    def test_proposal_context_detects_observed_ai_visibility(self):
        context = ProposalContext(
            company="Acme",
            domain="acme.com",
            evidence=evidence_from_mapping({
                "ai_share_of_voice": {"value": 0.12, "evidence_type": "observed"},
            }),
        )
        self.assertTrue(context.has_observed_ai_visibility())

    def test_readiness_does_not_count_as_ai_visibility(self):
        context = ProposalContext(
            company="Acme",
            domain="acme.com",
            evidence=evidence_from_mapping({"geo_score": 42}),
        )
        self.assertFalse(context.has_observed_ai_visibility())

    def test_evidence_table_has_explicit_type(self):
        evidence = evidence_from_mapping({
            "competitor_gap": {"value": -18, "evidence_type": "derived"}
        })
        table = build_evidence_table(evidence)
        self.assertIn("| competitor_gap | -18 | derived |", table)

    def test_scenario_value_is_deterministic(self):
        self.assertEqual(scenario_value(0.2, 120000), 24000.0)

    def test_scenario_value_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            scenario_value(-0.1, 1000)
        with self.assertRaises(ValueError):
            scenario_value(0.2, -1)


if __name__ == "__main__":
    unittest.main()
