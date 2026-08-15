from typing import Callable, Dict, Any
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class Tool(BaseModel):
    name: str
    description: str
    input_schema: Any = None
    func: Callable[[Dict[str, Any]], Dict[str, Any]]


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool
        logger.info("Registered tool %s", tool.name)

    def get(self, name: str) -> Tool:
        return self._tools.get(name)

    def list_tools(self):
        return list(self._tools.keys())


registry = ToolRegistry()
