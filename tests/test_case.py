from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
import uuid

class TestStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class TestCase:
    id: str = uuid.uuid4().hex
    name: str
    steps: List[Dict[str, Any]]
    priority: int
    complexity: float
    estimated_duration: float
    tags: List[str]
    created_at: datetime = datetime.now()
    status: TestStatus = TestStatus.PENDING
    artifacts: Dict[str, Any] = None
    validation_results: Dict[str, Any] = None

@dataclass
class ExecutionResult:
    test_case_id: str
    success: bool
    execution_time: float
    artifacts: Dict[str, str]
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    metrics: Dict[str, float] = None

@dataclass
class ValidationReport:
    test_case_id: str
    is_valid: bool
    confidence_score: float
    cross_validation_results: List[Dict[str, Any]]
    reproducibility_score: float
    anomalies_detected: List[Dict[str, Any]]
    
@dataclass
class TestReport:
    id: str = uuid.uuid4().hex
    timestamp: datetime = datetime.now()
    total_tests: int
    successful_tests: int
    failed_tests: int
    execution_time: float
    validation_summary: Dict[str, Any]
    test_results: List[ExecutionResult]
    validation_results: List[ValidationReport]
    artifacts_location: str