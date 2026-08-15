from pydantic import BaseModel
from typing import Any, List, Dict, Optional
from datetime import datetime


class ToolInvocation(BaseModel):
    tool_name: str
    input: Dict[str, Any]
    output: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.utcnow()


class AgentState(BaseModel):
    incident: Dict[str, Any]
    run_id: str
    iterations: int = 0
    tool_history: List[ToolInvocation] = []
    notes: List[str] = []
