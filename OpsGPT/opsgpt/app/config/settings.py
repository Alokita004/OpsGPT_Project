from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    GCP_PROJECT_ID: Optional[str] = None
    GCP_REGION: Optional[str] = None
    PUBSUB_TOPIC: str = "opsgpt-incidents"
    PUBSUB_SUBSCRIPTION: str = "opsgpt-worker-sub"
    BIGQUERY_DATASET: str = "opsgpt"
    BIGQUERY_METRICS_TABLE: str = "service_metrics"
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: Optional[str] = None
    EXECUTION_MODE: str = "DRY_RUN"
    LOG_LEVEL: str = "INFO"
    MAX_AGENT_ITERATIONS: int = 8
    LOCAL_MODE: bool = True

    class Config:
        env_file = ".env"
