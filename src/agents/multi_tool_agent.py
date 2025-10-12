from typing import List, Dict, Any
from .base_agent import BaseAgent
import logging
import time
import json

log = logging.getLogger(__name__)

# wrap the LLM, context, and tools (planning + tool methods like create_order, charge_payment, etc.).
class MultiToolAgent(BaseAgent):
    def plan(self, user_goal: str) -> List[Dict[str, Any]]:
        """
        Todo: Decompose user goal into subtasks.
        Notebook reference: Cell 6
        """
        pass

    # ----- Agent tools -----
    def create_order(self, sku: str, quantity: int):
        """
        Todo: Notebook reference: Cell 9
        """
        pass

    def charge_payment(self, card_number: str):
        """
        Todo: Notebook reference: Cell 9
        """
        pass

    def update_inventory(self, sku: str, delta: int):
        """
        Todo: Notebook reference: Cell 9
        """
        pass

    def summarize(self, content: str) -> str:
        """
        Todo: Notebook reference: summarizer_tool
        """
        pass

    def handle_returns(self, order_id: str):
        """
        Todo: Notebook reference: Cell 9
        """
        pass

    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Todo: Notebook reference: retrieval_tool
        """
        pass
