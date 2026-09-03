import unittest

from scripts.commercial_prospect import (
    ProspectStatus,
    Provenance,
    annual_value,
    expected_annual_value,
    normalize_prospect,
    weighted_pipeline_value,
)


class TestCommercialProspectV2(unittest.TestCase):
    def test_legacy_normalization(self):
        p = normalize_prospect({"id": "PRO-1", "company": "Acme", "domain": "acme.com"})
        self.assertEqual(p.status, ProspectStatus.LEAD)
        self.assertEqual(p.target_queries, [])
        self.assertEqual(p.competitor_domains, [])

    def test_provenance_round_trip(self):
        p = normalize_prospect({"id": "PRO-2", "company": "Acme", "domain": "acme.com", "provenance": {"citation_rate": "observed"}})
        self.assertEqual(p.to_dict()["provenance"]["citation_rate"], "observed")
        self.assertEqual(Provenance.DERIVED.value, "derived")

    def test_pipeline_math(self):
        self.assertEqual(weighted_pipeline_value(5000, 0.4), 2000.0)
        self.assertEqual(annual_value(5000), 60000.0)
        self.assertEqual(expected_annual_value(0.25, 100000), 25000.0)

    def test_invalid_values_raise(self):
        for args in [(-1, 0.5), (1000, -0.1), (1000, 1.1)]:
            with self.assertRaises(ValueError):
                weighted_pipeline_value(*args)
        with self.assertRaises(ValueError):
            expected_annual_value(1.1, 1000)


if __name__ == "__main__":
    unittest.main()
