import unittest

from scripts.commercial_prospect import (
    ProspectStatus,
    Provenance,
    annual_value,
    expected_annual_value,
    normalize_prospect,
    weighted_pipeline_value,
)


class TestCommercialProspect(unittest.TestCase):
    def test_legacy_record_normalizes_with_safe_defaults(self):
        prospect = normalize_prospect({"id": "PRO-001", "company": "Acme", "domain": "acme.com"})
        self.assertEqual(prospect.status, ProspectStatus.LEAD)
        self.assertEqual(prospect.target_queries, [])
        self.assertEqual(prospect.competitor_domains, [])
        self.assertEqual(prospect.provenance, {})

    def test_round_trip_serialization(self):
        prospect = normalize_prospect({
            "id": "PRO-002",
            "company": "Acme",
            "domain": "acme.com",
            "status": "qualified",
            "provenance": {"ai_share_of_voice": "derived"},
        })
        record = prospect.to_dict()
        self.assertEqual(record["status"], "qualified")
        self.assertEqual(record["provenance"]["ai_share_of_voice"], "derived")

    def test_pipeline_and_annual_values(self):
        self.assertEqual(weighted_pipeline_value(5000, 0.4), 2000.0)
        self.assertEqual(annual_value(5000), 60000.0)

    def test_expected_annual_value_is_explicit_scenario(self):
        self.assertEqual(expected_annual_value(0.2, 120000), 24000.0)

    def test_invalid_financial_inputs_fail(self):
        with self.assertRaises(ValueError):
            weighted_pipeline_value(-1, 0.5)
        with self.assertRaises(ValueError):
            weighted_pipeline_value(1000, 1.1)
        with self.assertRaises(ValueError):
            expected_annual_value(-0.1, 1000)

    def test_provenance_enum_is_canonical(self):
        self.assertEqual(Provenance.OBSERVED.value, "observed")
        self.assertEqual(Provenance.PROJECTED.value, "projected")


if __name__ == "__main__":
    unittest.main()
