# src/agents/agent_setup.py
import time
import json
import logging

from src.agents.multi_tool_agent import MultiToolAgent
from src.agents.orchestration import Orchestrator
from src.agents.multi_tool_agent import retrieval_tool, summarizer_tool, file_writer_tool
from src.utils.logging_utils import setup_logging

# -------------------------------
# Initialize structured logging
# -------------------------------
log = setup_logging("session3.log", level=logging.INFO, logger_name="Session3")
log.info("Session 3 multi-agent setup starting...")

# -------------------------------
# Initialize Core Agent (from Session 2)
# -------------------------------
agent_core = MultiToolAgent("CoreAgent", llm=None, context={"session_history": []})
agent_core.register_tool("retrieval", retrieval_tool)
agent_core.register_tool("summarizer", summarizer_tool)
agent_core.register_tool("file_writer", file_writer_tool)
log.info("CoreAgent initialized with retrieval, summarizer, file_writer tools")

# -------------------------------
# Initialize Crew Orchestrator (Session 2)
# -------------------------------
# crew_agents can be pre-defined in orchestration.py
from src.agents.orchestration import crew_agents  

orchestrator = Orchestrator(crew_agents=crew_agents)
run_plan_with_crew = orchestrator.run_plan_with_crew
log.info("Orchestrator initialized with pre-defined crew_agents")

# -------------------------------
# TODO1: Session 3 - Multi-Agent Setup
# -------------------------------
# Students implement this function to create CrewAI agents & Crew orchestrator
def setup_multi_agent_system():
    """
    Returns:
        agents: dict[str, CrewAgentWrapper]
        crew: Orchestrator object
    """
    agents = {
        # "retrieval": CrewAgentWrapper(...),
        # "summarizer": CrewAgentWrapper(...),
        # "writer": CrewAgentWrapper(...),
    }

    # Initialize Orchestrator / Crew with these agents
    crew = Orchestrator(crew_agents=agents)

    log.info("Multi-agent system skeleton created (students to complete)")

    return agents, crew

# -------------------------------
# TODO2: Session 3 - Feedback-aware runner
# -------------------------------
# Students implement retry + feedback logic (using Agno RetryPolicy)
# Reference: Notebook Cells 4-5
async def run_with_feedback_loop(user_goal: str, workflow: list, crew: Orchestrator, retry_policy=None):
    """
    Executes a multi-agent workflow with optional retry/feedback.

    Args:
        user_goal: high-level task description
        workflow: list of steps (retrieval -> summarizer -> writer)
        crew: Orchestrator / Crew object
        retry_policy: Optional Agno RetryPolicy

    Returns:
        results: aggregated output of all steps
    """
    # Students fill in: call crew agents step-by-step, apply retry_policy if provided
    pass

# -------------------------------
# Optional utility: save report
# -------------------------------
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
