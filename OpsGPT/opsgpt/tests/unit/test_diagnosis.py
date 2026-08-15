from app.tools.diagnosis_tools import generate_diagnosis


def test_generate_diagnosis_basic():
    args = {"analysis": {"anomaly_score": 0.8}, "deployments": [{"version":"v1.8.2","timestamp":"2026-08-15T09:50:00Z"}]}
    out = generate_diagnosis(args)
    assert "summary" in out
    assert out["root_cause"].startswith("deployment_")
