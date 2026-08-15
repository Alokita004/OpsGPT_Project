from typing import List, Dict, Any
from app.agents.state import AgentState, ToolInvocation
from app.tools.registry import registry
from app.services.llm_service import MockLLMProvider
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)


class OpsAgent:
    def __init__(self, llm_provider=None, max_iterations: int = 8):
        self.llm = llm_provider or MockLLMProvider()
        self.max_iterations = max_iterations

    def run(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        run_id = f"RUN-{uuid4().hex[:8].upper()}"
        state = AgentState(incident=incident, run_id=run_id)

        while state.iterations < self.max_iterations:
            state.iterations += 1
            logger.info("Agent iteration %d for %s", state.iterations, incident.get('incident_id'))

            # Prepare lightweight state dict for LLM
            llm_state = {"incident": state.incident, "tool_history": [t.model_dump() for t in state.tool_history]}
            decision = self.llm.decide(llm_state, registry.list_tools())

            if decision.get('action') == 'TOOL':
                tool_name = decision.get('tool_name')
                tool_input = decision.get('tool_input', {})
                tool = registry.get(tool_name)
                if not tool:
                    logger.error("Tool %s not found", tool_name)
                    state.notes.append(f"Tool {tool_name} not found")
                    continue

                invocation = ToolInvocation(tool_name=tool_name, input=tool_input)
                try:
                    output = tool.func(tool_input)
                    invocation.output = output
                    state.tool_history.append(invocation)
                except Exception as e:
                    logger.exception("Tool %s failed: %s", tool_name, e)
                    state.notes.append(f"Tool {tool_name} failed: {e}")

                continue

            if decision.get('action') == 'FINISH':
                report = decision.get('final_report', {})
                return {"run_id": run_id, "status": "COMPLETED", "report": report, "state": state.model_dump()}

        # Exceeded iterations
        return {"run_id": run_id, "status": "MAX_ITERATIONS_EXCEEDED", "state": state.model_dump()}
