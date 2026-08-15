from app.agents.ops_agent import OpsAgent


def test_agent_runs_to_completion(monkeypatch):
    incident = {
        "incident_id": "INC-DEMO",
        "service_name": "checkout-service",
        "metric_name": "error_rate",
    }

    agent = OpsAgent()
    result = agent.run(incident)
    assert result["status"] in ("COMPLETED", "MAX_ITERATIONS_EXCEEDED")
