from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
import asyncio
from datetime import datetime
import uvicorn

from agents.orchestrator_agent import OrchestratorAgent
from agents.planner_agent import PlannerAgent
from agents.ranker_agent import RankerAgent
from backend.security import authenticate_request, create_access_token
from backend.core.architecture import TestCase, TestReport

app = FastAPI(title="MAGE - Multi-Agent Game Tester", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
orchestrator = OrchestratorAgent()
planner = PlannerAgent()
ranker = RankerAgent()

@app.post("/api/v2/generate-plan")
async def generate_test_plan(target_url: str, token: str = Depends(oauth2_scheme)):
    authenticate_request(token)
    test_cases = await planner.generate_test_cases(target_url, count=20)
    ranked_cases = await ranker.rank_test_cases(test_cases)
    return {"test_cases": ranked_cases}

@app.post("/api/v2/execute-plan")
async def execute_test_plan(test_cases: List[TestCase], token: str = Depends(oauth2_scheme)):
    authenticate_request(token)
    execution_id = await orchestrator.schedule_execution(test_cases[:10])
    return {"execution_id": execution_id}

@app.get("/api/v2/execution-status/{execution_id}")
async def get_execution_status(execution_id: str, token: str = Depends(oauth2_scheme)):
    authenticate_request(token)
    status = await orchestrator.get_execution_status(execution_id)
    return status

@app.get("/api/v2/reports")
async def get_reports(limit: Optional[int] = 10, token: str = Depends(oauth2_scheme)):
    authenticate_request(token)
    reports = await orchestrator.get_reports(limit)
    return reports

@app.get("/api/v2/reports/{report_id}")
async def get_report(report_id: str, token: str = Depends(oauth2_scheme)):
    authenticate_request(token)
    report = await orchestrator.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)