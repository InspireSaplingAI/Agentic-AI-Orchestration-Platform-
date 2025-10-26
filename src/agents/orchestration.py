from typing import List, Dict, Any
import asyncio
import logging
import time
from src.agents.multi_tool_agent import retrieval_tool, summarizer_tool, file_writer_tool
from src.agents.agent_setup import agent_core

log = logging.getLogger(__name__)

# -------------------------------
# CrewAgentWrapper
# -------------------------------
class CrewAgentWrapper:
    def __init__(self, name: str, role: str, tool_map: Dict[str, Any]):
        self.name = name
        self.role = role
        self.tool_map = tool_map

    async def handle(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Route the task to the appropriate tool based on role."""
        action = task.get("action")
        params = task.get("params", {})

        log.info("[CrewAgent %s] Handling action=%s params=%s", self.name, action, params)

        try:
            if self.role == "retrieval":
                query = params.get("query") or params.get("text") or params
                hits = self.tool_map["retrieval"](str(query), k=3)
                return {"status": "ok", "hits": hits}

            elif self.role == "summarizer":
                text = params.get("text") or params.get("content", "")
                summary = self.tool_map["summarizer"](text)
                return {"status": "ok", "summary": summary}

            elif self.role == "writer":
                filename = params.get("filename", f"report_{int(time.time())}.txt")
                content = params.get("content", "")
                path = self.tool_map["file_writer"](filename, content)
                return {"status": "ok", "file": path}

            return {"status": "failed", "reason": "unknown_role"}
        except Exception as e:
            log.exception("Error in agent %s", self.name)
            return {"status": "error", "error": str(e)}

# -------------------------------
# Initialize crew_agents
# -------------------------------
crew_agents = {
    "retrieval": CrewAgentWrapper("Retriever", "retrieval", {"retrieval": retrieval_tool}),
    "summarizer": CrewAgentWrapper("Summarizer", "summarizer", {"summarizer": summarizer_tool}),
    "writer": CrewAgentWrapper("Writer", "writer", {"file_writer": file_writer_tool}),
}


class Orchestrator:
    def __init__(self, crew_agents: Dict[str, Any]):
        self.crew_agents = crew_agents

    async def run_plan_with_crew(self, plan: List[Dict[str, Any]]):
        """
        TODO3: Session 3 - Student Skeleton
        - Execute each step in the plan using the corresponding crew agent
        - Integrate retry_task_with_feedback() for fault tolerance
        - Aggregate results into a final report/dict

        Args:
            plan: List of task dicts, each with "step" and optional parameters

        Returns:
            results: aggregated results from all steps
        """

        results = {}

        # -------------------------------
        # Skeleton for students to complete
        # -------------------------------

        for step in plan:
            step_name = step.get("step")
            log.info("Processing step: %s", step_name)

            # TODO: 1) Map step_name to corresponding crew agent
            agent = self.crew_agents.get(step_name)

            # TODO: 2) Prepare task dict with params (students can customize)
            task = {
                "action": step_name,
                "params": step.get("params", {})
            }

            # TODO: 3) Call retry_task_with_feedback() with the agent.handle coroutine
            # Example:
            # step_result = await retry_task_with_feedback(agent.handle, task, retry_policy=...)
            step_result = None  # <- students replace with actual call

            # TODO: 4) Aggregate step_result into results dict
            results[step_name] = step_result

        # -------------------------------
        # Return aggregated results
        # -------------------------------
        return results
