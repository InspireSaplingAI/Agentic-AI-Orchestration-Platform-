from .base_agent import BaseAgent
from typing import List, Dict, Any

class RetrievalAgent(BaseAgent):
    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve documents based on query.
        Todo: Implementation reference: retrieval_tool in notebook
        """
        pass
