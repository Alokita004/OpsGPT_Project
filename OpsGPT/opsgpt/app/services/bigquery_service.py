from typing import List, Dict, Any
import logging
from app.config.settings import Settings
from app.security.sql_validator import validate_sql
import csv
import os

logger = logging.getLogger(__name__)


class BigQueryClient:
    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class LocalBigQueryClient(BigQueryClient):
    """A local mock BigQuery client that reads CSV data for `service_metrics`."""

    def __init__(self, dataset_path: str = None, settings: Settings | None = None):
        self.settings = settings or Settings()
        base = dataset_path or os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "data")
        self.data_file = os.path.join(base, "service_metrics.csv")

    def _load_rows(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.data_file):
            return []
        rows: List[Dict[str, Any]] = []
        with open(self.data_file, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for r in reader:
                rows.append(r)
        return rows

    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        # Validate SQL with guardrails
        validate_sql(sql, allow_tables=[self.settings.BIGQUERY_METRICS_TABLE])

        # Very small local implementation: return all rows for SELECT * FROM service_metrics
        sql_normalized = sql.strip().lower()
        if "select" in sql_normalized and self.settings.BIGQUERY_METRICS_TABLE in sql_normalized:
            rows = self._load_rows()
            logger.info("LocalBigQueryClient returning %d rows", len(rows))
            return rows
        return []


def get_bigquery_client(settings: Settings) -> BigQueryClient:
    if settings.LOCAL_MODE:
        return LocalBigQueryClient(settings=settings)
    raise NotImplementedError("GCP BigQuery client not implemented yet")
