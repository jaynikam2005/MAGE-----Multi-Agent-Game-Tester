"""Artifact models for test execution and evidence collection"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class ArtifactType(str, Enum):
    """Types of artifacts that can be captured during test execution"""
    SCREENSHOT = "screenshot"
    DOM_SNAPSHOT = "dom_snapshot"
    CONSOLE_LOG = "console_log"
    NETWORK_TRACE = "network_trace"
    PERFORMANCE_METRICS = "performance_metrics"


@dataclass
class TestArtifact:
    """Base class for test artifacts"""
    id: str
    type: ArtifactType
    timestamp: datetime
    test_case_id: str
    step_number: int
    metadata: Dict[str, Any]


@dataclass
class Screenshot(TestArtifact):
    """Screenshot artifact with image data"""
    image_path: str
    viewport_size: Dict[str, int]
    element_highlighted: Optional[str] = None


@dataclass
class DOMSnapshot(TestArtifact):
    """DOM tree snapshot at a point in time"""
    html_content: str
    active_element: Optional[str] = None
    selector_path: Optional[str] = None


@dataclass
class ConsoleLog(TestArtifact):
    """Browser console log entries"""
    entries: List[Dict[str, Any]]
    log_level: str
    message_count: int


@dataclass
class NetworkTrace(TestArtifact):
    """Network request/response data"""
    requests: List[Dict[str, Any]]
    responses: List[Dict[str, Any]]
    timing_data: Dict[str, float]


@dataclass
class ArtifactCollection:
    """Collection of artifacts for a test case"""
    test_case_id: str
    artifacts: List[TestArtifact]
    start_time: datetime
    end_time: datetime
    total_artifacts: int

    def add_artifact(self, artifact: TestArtifact) -> None:
        """Add an artifact to the collection"""
        self.artifacts.append(artifact)
        self.total_artifacts = len(self.artifacts)

    def get_artifacts_by_type(self, artifact_type: ArtifactType) -> List[TestArtifact]:
        """Get all artifacts of a specific type"""
        return [a for a in self.artifacts if a.type == artifact_type]

    def get_artifacts_for_step(self, step_number: int) -> List[TestArtifact]:
        """Get all artifacts for a specific test step"""
        return [a for a in self.artifacts if a.step_number == step_number]