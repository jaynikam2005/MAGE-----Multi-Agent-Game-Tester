"""
FastAPI Server for MAGE Enterprise
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from pydantic import BaseModel

from src.core.config import get_settings
from src.agents.multi_agent.orchestrator import OrchestratorAgent
from src.reporting.report_generator import ReportGenerator

# Request Models
class TestPlanRequest(BaseModel):
    num_tests: int = 20

class TestExecuteRequest(BaseModel):
    test_ids: Optional[List[str]] = None

class ReportGenerateRequest(BaseModel):
    test_results: List[Dict[str, Any]]
    performance_data: Optional[List[Dict[str, Any]]] = []
    security_data: Optional[List[Dict[str, Any]]] = []
    format: str = "html"

# Get settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MAGE Enterprise API",
    description="Multi-Agent Game Testing Enterprise API",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
orchestrator = OrchestratorAgent()
report_generator = ReportGenerator()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await orchestrator.initialize()
    logger.info("Orchestrator initialized successfully")
    yield
    # Shutdown (if needed)
    # await orchestrator.cleanup()

# Update your FastAPI app initialization
app = FastAPI(
    title="MAGE Multi-Agent Game Tester API",
    description="Enterprise-grade AI-powered game testing platform",
    version="2.1.0",
    lifespan=lifespan  # Add this line
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "MAGE Enterprise API",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/tests/plan")
async def generate_test_plan(request: TestPlanRequest):
    """Generate a test plan"""
    try:
        plan = await orchestrator.generate_test_plan(request.num_tests)
        return {
            "status": "success",
            "message": f"Generated {request.num_tests} test cases",
            "plan": plan
        }
    except Exception as e:
        logger.error(f"Error generating test plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/api/v1/tests/execute")
async def execute_tests(request: TestExecuteRequest):
    """Execute tests"""
    try:
        results = await orchestrator.execute_tests(request.test_ids)
        return {
            "status": "success",
            "message": f"Executed {len(request.test_ids) if request.test_ids else 'all'} tests",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error executing tests: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/v1/reports")
async def get_reports():
    """Get list of available reports"""
    try:
        reports = report_generator.get_available_reports()
        return {
            "status": "success",
            "message": f"Found {len(reports)} reports",
            "reports": reports
        }
    except Exception as e:
        logger.error(f"Error getting reports: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/api/v1/reports/generate")
async def generate_report(request: ReportGenerateRequest):
    """Generate a new report"""
    try:
        report_path = report_generator.generate_comprehensive_report(
            test_results=request.test_results,
            performance_data=request.performance_data,
            security_data=request.security_data,
            format=request.format
        )
        return {
            "status": "success",
            "message": "Report generated successfully",
            "report_path": report_path
        }
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/v1/system/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "orchestrator": "operational",
            "report_generator": "operational",
            "database": "connected"
        }
    }
