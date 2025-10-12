# src/api/fastapi_app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
import time

from src.api.schemas import UserGoalRequest, MultiAgentResponse
from src.agents.agent_setup import agent_core, run_plan_with_crew, summarizer_tool, save_report

log = logging.getLogger("uvicorn")
app = FastAPI(title="Multi-Agent E-commerce API", version="1.0")

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/user_goal", response_model=MultiAgentResponse)
async def process_user_goal(request: UserGoalRequest):
    user_goal = request.goal
    log.info("Received user goal: %s", user_goal)

    # 1) Save in planner context
    agent_core.context.setdefault("session_history", []).append(
        {"goal": user_goal, "time": time.asctime()}
    )

    # 2) Generate plan
    plan = agent_core.plan(user_goal)
    if not plan:
        raise HTTPException(status_code=400, detail="Planner returned empty plan")

    # 3) Execute plan asynchronously
    results = await run_plan_with_crew(plan)

    # 4) Summarize results
    summary = summarizer_tool(json.dumps(results, indent=2))

    # 5) Save report and update context
    report_path = save_report(user_goal, plan, results, summary)

    # 6) Return structured response
    return MultiAgentResponse(
        plan=plan,
        results=[{"step": r["step"], "result": r["result"]} for r in results],
        summary=summary,
        report_path=report_path,
    )
