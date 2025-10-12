# src/main.py
import uvicorn
from src.agents import agent_setup  # initialize agents, orchestrator, tools
from src.api.fastapi_app import app  # import FastAPI app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True  # optional for development
    )
