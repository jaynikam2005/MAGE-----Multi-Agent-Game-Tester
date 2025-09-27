from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel

class AgentType(Enum):
    PLANNER = "planner"
    RANKER = "ranker"
    ORCHESTRATOR = "orchestrator"
    EXECUTOR = "executor"
    ANALYZER = "analyzer"

class TestCase(BaseModel):
    id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    priority: int
    estimated_duration: int
    tags: List[str]

class TestResult(BaseModel):
    test_case_id: str
    status: str  # passed, failed, error
    artifacts: Dict[str, Any]
    validation_results: Dict[str, Any]
    execution_time: float
    reproducibility_score: float