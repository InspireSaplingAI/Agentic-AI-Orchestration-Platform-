import json
import time
import logging
from typing import Any, Dict

log = logging.getLogger(__name__)

# Core agent base class, LLM wrapper, context & memory support
class BaseAgent:
    def __init__(self, name: str, llm=None, context: Dict[str, Any] = None):
        self.name = name
        self.llm = llm
        self.context = context or {}
        self.tools = {}

    def register_tool(self, name: str, func):
        """Register a callable tool."""
        self.tools[name] = func
        log.info("[%s] Registered tool: %s", self.name, name)

    def call_llm(self, prompt: str) -> str:
        """Wrapper for calling LLM and extracting text."""
        """Todo: Call LLM and extract text (see notebook Cell 6)."""
        pass  # implement based on llm_text extraction logic from Cell 6
