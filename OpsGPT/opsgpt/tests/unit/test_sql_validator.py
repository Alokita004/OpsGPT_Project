import pytest
from app.security.sql_validator import validate_sql, SQLValidationError


def test_valid_select():
    sql = "SELECT * FROM service_metrics WHERE service_name = 'checkout-service'"
    assert validate_sql(sql, allow_tables=["service_metrics"]) is True


@pytest.mark.parametrize('bad', [
    "DROP TABLE service_metrics;",
    "DELETE FROM service_metrics",
    "INSERT INTO service_metrics (a) VALUES (1)",
    "UPDATE service_metrics SET metric_value=1",
    "SELECT * FROM other_table",
    "SELECT 1; SELECT 2"
])
def test_invalid_sql(bad):
    with pytest.raises(SQLValidationError):
        validate_sql(bad, allow_tables=["service_metrics"])
