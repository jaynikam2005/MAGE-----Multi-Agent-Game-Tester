"""Test report models for comprehensive result reporting"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class VerdictStatus(str, Enum):
    """Possible test verdict statuses"""
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"
    INCONCLUSIVE = "inconclusive"
    BLOCKED = "blocked"


class Severity(str, Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class TestEvidence:
    """Evidence collected during test execution"""
    evidence_id: str
    type: str
    description: str
    artifacts: List[str]  # References to artifact IDs
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class TestVerdict:
    """Verdict for a single test case"""
    test_case_id: str
    status: VerdictStatus
    execution_time: float
    evidence: List[TestEvidence]
    issues_found: List[Dict[str, Any]]
    reproducibility_score: float
    confidence_score: float
    validation_results: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class ValidationResult:
    """Result of cross-agent validation"""
    validator_id: str
    validated_by: List[str]
    agreement_score: float
    discrepancies: List[Dict[str, Any]]
    recommendations: List[str]


@dataclass
class TestReport:
    """Comprehensive test execution report"""
    report_id: str
    session_id: str
    timestamp: datetime
    target_url: str
    test_cases: List[Dict[str, Any]]
    verdicts: List[TestVerdict]
    validations: List[ValidationResult]
    summary_metrics: Dict[str, Any]
    artifacts_summary: Dict[str, int]
    execution_environment: Dict[str, Any]
    recommendations: List[Dict[str, Any]]

    def to_json(self) -> Dict[str, Any]:
        """Convert report to JSON format"""
        return {
            "report_id": self.report_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "target_url": self.target_url,
            "test_cases": self.test_cases,
            "verdicts": [
                {
                    "test_case_id": v.test_case_id,
                    "status": v.status.value,
                    "execution_time": v.execution_time,
                    "evidence": [
                        {
                            "evidence_id": e.evidence_id,
                            "type": e.type,
                            "description": e.description,
                            "artifacts": e.artifacts,
                            "timestamp": e.timestamp.isoformat(),
                            "metadata": e.metadata
                        }
                        for e in v.evidence
                    ],
                    "issues_found": v.issues_found,
                    "reproducibility_score": v.reproducibility_score,
                    "confidence_score": v.confidence_score,
                    "validation_results": v.validation_results,
                    "metadata": v.metadata
                }
                for v in self.verdicts
            ],
            "validations": [
                {
                    "validator_id": v.validator_id,
                    "validated_by": v.validated_by,
                    "agreement_score": v.agreement_score,
                    "discrepancies": v.discrepancies,
                    "recommendations": v.recommendations
                }
                for v in self.validations
            ],
            "summary_metrics": self.summary_metrics,
            "artifacts_summary": self.artifacts_summary,
            "execution_environment": self.execution_environment,
            "recommendations": self.recommendations
        }