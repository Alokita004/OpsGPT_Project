from pydantic import BaseModel, Field, Extra, ValidationError
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Environment(str, Enum):
    DEV = "DEV"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class IncidentBase(BaseModel):
    service_name: str = Field(..., min_length=1)
    environment: Environment
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    severity: Severity
    metric_name: str
    metric_value: float
    threshold: float
    description: Optional[str]
    metadata: Optional[Dict[str, Any]] = None

    model_config = {
        "extra": Extra.forbid
    }


class IncidentCreate(IncidentBase):
    pass


class IncidentResponse(BaseModel):
    incident_id: str
    status: str
    message: Optional[str]

    model_config = {"extra": Extra.forbid}
