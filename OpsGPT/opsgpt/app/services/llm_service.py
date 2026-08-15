from typing import Dict, Any, List
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    @abstractmethod
    def decide(self, state: Dict[str, Any], tools: List[str]) -> Dict[str, Any]:
        pass


class MockLLMProvider(LLMProvider):
    def decide(self, state: Dict[str, Any], tools: List[str]) -> Dict[str, Any]:
        th = state.get("tool_history", [])
        if not th:
            return {"action": "TOOL", "tool_name": "query_historical_metrics", "tool_input": {"service_name": state['incident']['service_name'], "metric_name": state['incident']['metric_name'], "start_time": None, "end_time": None, "aggregation": "avg"}}
        names = [t.get('tool_name') for t in th]
        if "query_historical_metrics" in names and "analyze_anomaly" not in names:
            return {"action": "TOOL", "tool_name": "analyze_anomaly", "tool_input": {"rows": th[-1].get('output', {}).get('rows', [])}}
        if "analyze_anomaly" in names and "recommend_remediation" not in names:
            return {"action": "TOOL", "tool_name": "recommend_remediation", "tool_input": {"analysis": th[-1].get('output', {})}}
        if "recommend_remediation" in names and "generate_diagnosis" not in names:
            return {"action": "TOOL", "tool_name": "generate_diagnosis", "tool_input": {"analysis": th[-1].get('output', {}), "deployments": []}}
        return {"action": "FINISH", "final_report": {"summary": "Mock diagnosis: regression suspected", "root_cause": "deployment", "confidence": 0.85}}
