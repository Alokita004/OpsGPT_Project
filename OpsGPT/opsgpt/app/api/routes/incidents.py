from fastapi import APIRouter, Depends, HTTPException, status
from app.models.incident import IncidentCreate, IncidentResponse
from app.config.settings import Settings
from uuid import uuid4

router = APIRouter()


def get_settings():
    return Settings()


@router.post("/incidents", response_model=IncidentResponse)
async def create_incident(incident: IncidentCreate, settings: Settings = Depends(get_settings)):
    # Generate incident id
    incident_id = f"INC-{uuid4().hex[:8].upper()}"

    # For Phase 1 we queue the incident (publishing to Pub/Sub is done in Phase 2)
    return IncidentResponse(incident_id=incident_id, status="QUEUED", message="Incident submitted for investigation")
