# src/agents/agent_setup.py
import time
import json
import logging

from src.agents.multi_tool_agent import MultiToolAgent
from src.agents.orchestration import Orchestrator
from src.agents.multi_tool_agent import retrieval_tool, summarizer_tool, file_writer_tool

log = logging.getLogger(__name__)

# -------------------------------
# Initialize Core Agent
# -------------------------------
agent_core = MultiToolAgent("CoreAgent", llm=None, context={"session_history": []})
agent_core.register_tool("retrieval", retrieval_tool)
agent_core.register_tool("summarizer", summarizer_tool)
agent_core.register_tool("file_writer", file_writer_tool)

# -------------------------------
# Crew Orchestrator
# -------------------------------
# crew_agents can be pre-defined in orchestration.py
# Example mapping: role -> agent wrapper
from src.agents.orchestration import crew_agents  

orchestrator = Orchestrator(crew_agents=crew_agents)
run_plan_with_crew = orchestrator.run_plan_with_crew

# Optional: utility function to save plan/report
def save_report(goal: str, plan: list, results: list, summary: str) -> str:
    report = {
        "goal": goal,
        "plan": plan,
        "results": results,
        "summary": summary,
        "timestamp": time.asctime(),
    }
    path = file_writer_tool(f"session_report_{int(time.time())}.json", json.dumps(report, indent=2))
    agent_core.context.setdefault("last_reports", []).append(
        {"path": path, "goal": goal, "time": time.asctime()}
    )
    log.info("Report saved to %s", path)
    return path
