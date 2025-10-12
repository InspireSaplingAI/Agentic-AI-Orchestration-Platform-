from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Incoming user goal request
class UserGoalRequest(BaseModel):
    goal: str
    user_id: Optional[str] = None  # optional multi-user support

# Crew step result
class StepResult(BaseModel):
    step: Dict[str, Any]
    result: Dict[str, Any]

# Full multi-agent plan result
class MultiAgentResponse(BaseModel):
    plan: List[Dict[str, Any]]
    results: List[StepResult]
    summary: str
    report_path: str
