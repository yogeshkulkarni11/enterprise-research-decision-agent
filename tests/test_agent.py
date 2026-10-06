from src.agent import risk_agent, decision_agent, ResearchEvidence


def test_risk_band_is_derived():
    vendor = {
        "vendor_id": "V1", "vendor_name": "Test", "category": "Cloud",
        "annual_cost_m": 1.0, "security_score": 95, "financial_score": 95,
        "resilience_score": 95, "regulatory_score": 95, "concentration_pct": 5,
        "implementation_months": 2,
    }
    result = risk_agent([vendor])[0]
    assert result["risk_band"] == "Low"
    assert result["risk_score"] >= 0


def test_decision_returns_best_vendor():
    vendors = [
        {"vendor_name": "A", "risk_score": 10, "risk_band": "Low", "security_score": 90,
         "resilience_score": 90, "regulatory_score": 90, "annual_cost_m": 1.0, "concentration_pct": 10},
        {"vendor_name": "B", "risk_score": 20, "risk_band": "Medium", "security_score": 80,
         "resilience_score": 80, "regulatory_score": 80, "annual_cost_m": 0.5, "concentration_pct": 20},
    ]
    result = decision_agent(vendors, [ResearchEvidence("policy.md", "policy evidence")])
    assert result["decision"] == "A"
    assert result["evidence"]
