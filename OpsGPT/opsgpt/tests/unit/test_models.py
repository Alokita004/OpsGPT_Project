import pytest
from app.models.incident import IncidentCreate, Severity, Environment
from pydantic import ValidationError


def test_valid_incident():
    data = {
        "service_name": "checkout-service",
        "environment": "PRODUCTION",
        "severity": "HIGH",
        "metric_name": "error_rate",
        "metric_value": 18.7,
        "threshold": 5.0,
        "description": "Checkout error rate increased significantly",
        "metadata": {"region": "asia-south1", "version": "v1.8.2"},
    }
    inc = IncidentCreate(**data)
    assert inc.service_name == "checkout-service"
    assert inc.environment == Environment.PRODUCTION
    assert inc.severity == Severity.HIGH


def test_invalid_severity():
    data = {
        "service_name": "s",
        "environment": "PRODUCTION",
        "severity": "UNKNOWN",
        "metric_name": "error_rate",
        "metric_value": 1.0,
        "threshold": 0.5,
    }
    with pytest.raises(ValidationError):
        IncidentCreate(**data)
