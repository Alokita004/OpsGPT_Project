from typing import Dict, Any, List
from app.services.bigquery_service import get_bigquery_client
from app.config.settings import Settings
import logging

logger = logging.getLogger(__name__)


def query_historical_metrics(args: Dict[str, Any]) -> Dict[str, Any]:
    settings = Settings()
    client = get_bigquery_client(settings)
    service = args.get('service_name')
    metric = args.get('metric_name')
    sql = f"SELECT * FROM {settings.BIGQUERY_METRICS_TABLE} WHERE service_name = '{service}' AND metric_name = '{metric}'"
    rows = client.execute_query(sql)
    logger.info("Queried historical metrics, got %d rows", len(rows))
    return {"rows": rows}
