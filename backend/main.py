from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
from datetime import datetime

app = FastAPI(title="Multi-Agent Game Tester")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (use Redis in production)
test_sessions = {}

class TestSessionRequest(BaseModel):
    game_url: str
    test_count: int = 20
    top_k: int = 10

class TestSession(BaseModel):
    session_id: str
    status: str
    created_at: datetime
    test_cases: Optional[List[TestCase]] = None
    results: Optional[List[TestResult]] = None
    report: Optional[Dict] = None

@app.post("/api/sessions/create")
async def create_test_session(request: TestSessionRequest, background_tasks: BackgroundTasks):
    """Create a new test session"""
    session_id = str(uuid.uuid4())
    
    session = TestSession(
        session_id=session_id,
        status="initializing",
        created_at=datetime.now()
    )
    
    test_sessions[session_id] = session
    
    # Start test execution in background
    background_tasks.add_task(
        execute_test_session,
        session_id,
        request.game_url,
        request.test_count,
        request.top_k
    )
    
    return {"session_id": session_id, "status": "created"}

@app.get("/api/sessions/{session_id}")
async def get_session_status(session_id: str):
    """Get test session status"""
    if session_id not in test_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = test_sessions[session_id]
    return {
        "session_id": session.session_id,
        "status": session.status,
        "created_at": session.created_at,
        "progress": calculate_progress(session)
    }

@app.get("/api/sessions/{session_id}/report")
async def get_session_report(session_id: str):
    """Get test session report"""
    if session_id not in test_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = test_sessions[session_id]
    if session.status != "completed":
        raise HTTPException(status_code=400, detail="Session not completed")
    
    return session.report

async def execute_test_session(session_id: str, game_url: str, test_count: int, top_k: int):
    """Execute complete test session"""
    session = test_sessions[session_id]
    
    try:
        # Phase 1: Generate test cases
        session.status = "generating_tests"
        planner = PlannerAgent()
        test_cases = planner.generate_test_cases(game_url, test_count)
        session.test_cases = test_cases
        
        # Phase 2: Rank and select top tests
        session.status = "ranking_tests"
        ranker = RankerAgent()
        top_tests = ranker.rank_test_cases(test_cases)[:top_k]
        
        # Phase 3: Execute tests
        session.status = "executing_tests"
        orchestrator = OrchestratorAgent()
        results = orchestrator.execute_test_suite(top_tests)
        session.results = results
        
        # Phase 4: Validate results
        session.status = "validating_results"
        analyzer = AnalyzerAgent()
        validation_report = analyzer.validate_results(results)
        
        # Phase 5: Generate final report
        session.status = "generating_report"
        report = generate_final_report(test_cases, results, validation_report)
        session.report = report
        
        session.status = "completed"
        
    except Exception as e:
        session.status = "failed"
        session.report = {"error": str(e)}

def generate_final_report(test_cases, results, validation_report):
    """Generate comprehensive test report"""
    report = {
        "summary": {
            "total_tests": len(test_cases),
            "executed_tests": len(results),
            "passed": sum(1 for r in results if r.status == "passed"),
            "failed": sum(1 for r in results if r.status == "failed"),
            "success_rate": sum(1 for r in results if r.status == "passed") / len(results) * 100
        },
        "test_results": [r.dict() for r in results],
        "validation": validation_report,
        "recommendations": generate_recommendations(results, validation_report),
        "artifacts_location": "/artifacts/",
        "timestamp": datetime.now().isoformat()
    }
    
    # Save report to file
    report_file = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    return report