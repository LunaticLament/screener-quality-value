import unittest
from datetime import date, timedelta
from valuation_engine import dcf_equity, implied_discount, analyze, generate

class ValuationQualityTests(unittest.TestCase):
    def sample(self):
        years=[]
        for i in (3,2,1):
            y=(date.today()-timedelta(days=365*i)).isoformat()
            years.append({"year_end":y,"cfo":150+i,"capex":40,"sbc":10,
                          "diluted_shares":100,"source_type":"fact_provider_standardized",
                          "source_name":"Unit test example","currency":"USD","revenue":500})
        return {"ticker":"TEST","name":"Example (test only)","model":"corporate",
                "region":"North America","sector":"Example","price":10,
                "price_asof":date.today().isoformat(),"currency":"USD",
                "financial_currency":"USD","financial_source":"Example (test only)",
                "financial_url":"https://example.test/","shares_outstanding":100,
                "financial_history":years}

    def test_perpetuity_identity(self):
        # A fixed growth rate for all 10 years equals the infinite growing annuity.
        self.assertAlmostEqual(dcf_equity(1, .02, .10, .02), 1.02/(.10-.02), places=6)

    def test_implied_rate_roundtrip(self):
        price=dcf_equity(2, .04, .11, .02)
        self.assertAlmostEqual(implied_discount(2,.04,.02,price),.11,places=6)

    def test_invalid_spread_is_rejected(self):
        with self.assertRaises(ValueError):
            dcf_equity(1,.04,.02,.02)

    def test_three_years_are_only_indicative(self):
        d=analyze(self.sample())
        self.assertEqual(d["status"],"screen-grade")
        self.assertFalse(d["decision_ready"])
        self.assertFalse(d["validated_opportunity"])
        self.assertEqual(len(d["historical"]),3)
        self.assertTrue(any("cinq ans" in w for w in d["warnings"]))

    def test_fx_mismatch_blocks(self):
        d=self.sample()
        d["financial_currency"]="EUR"
        self.assertEqual(analyze(d)["status"],"blocked")

    def test_no_shares_blocks(self):
        d=self.sample()
        d.pop("shares_outstanding")
        for h in d["financial_history"]:
            h["diluted_shares"]=None
        self.assertEqual(analyze(d)["status"],"blocked")

    def test_sector_method_blocks_generic(self):
        d=self.sample()
        d["model"]="bank"
        self.assertEqual(analyze(d)["status"],"blocked")

    def test_full_report_has_no_validated_buy(self):
        report=generate({"companies":[self.sample()]})
        self.assertEqual(report["counts"]["decision_ready"],0)
        self.assertEqual(report["counts"]["indicative"],1)

if __name__=="__main__":
    unittest.main()
