"""Test case ranking criteria and scoring system"""

from dataclasses import dataclass
from typing import Dict, List, Any
from enum import Enum


class RankingCriteria(str, Enum):
    """Criteria for ranking test cases"""
    COMPLEXITY = "complexity"
    PRIORITY = "priority"
    EXECUTION_TIME = "execution_time"
    COVERAGE = "coverage"
    DEPENDENCY_COUNT = "dependency_count"
    HISTORICAL_SUCCESS = "historical_success"
    AI_CONFIDENCE = "ai_confidence"


@dataclass
class RankingWeights:
    """Weights for different ranking criteria"""
    complexity: float = 0.15
    priority: float = 0.25
    execution_time: float = 0.10
    coverage: float = 0.20
    dependency_count: float = 0.10
    historical_success: float = 0.10
    ai_confidence: float = 0.10

    def validate(self) -> bool:
        """Ensure weights sum to 1.0"""
        total = sum([
            self.complexity,
            self.priority,
            self.execution_time,
            self.coverage,
            self.dependency_count,
            self.historical_success,
            self.ai_confidence
        ])
        return abs(total - 1.0) < 0.001


class CriteriaScorer:
    """Score calculator for individual ranking criteria"""

    @staticmethod
    def score_complexity(test_case: Dict[str, Any]) -> float:
        """Score test case complexity (0-1)"""
        complexity = test_case.get("complexity", "medium")
        return {
            "low": 0.3,
            "medium": 0.6,
            "high": 1.0
        }.get(complexity.lower(), 0.5)

    @staticmethod
    def score_priority(test_case: Dict[str, Any]) -> float:
        """Score test case priority (0-1)"""
        priority = test_case.get("priority", 1.0)
        return min(max(float(priority), 0.0), 1.0)

    @staticmethod
    def score_execution_time(test_case: Dict[str, Any]) -> float:
        """Score based on estimated execution time (0-1)"""
        est_time = test_case.get("estimated_duration", 60)  # seconds
        # Normalize: shorter time = higher score
        return 1.0 - min(est_time / 300.0, 1.0)  # Cap at 5 minutes

    @staticmethod
    def score_coverage(test_case: Dict[str, Any]) -> float:
        """Score based on test coverage (0-1)"""
        coverage = test_case.get("coverage_score", 0.5)
        return min(max(float(coverage), 0.0), 1.0)

    @staticmethod
    def score_dependency_count(test_case: Dict[str, Any]) -> float:
        """Score based on number of dependencies (0-1)"""
        deps = len(test_case.get("prerequisites", []))
        # Fewer dependencies = higher score
        return 1.0 - min(deps / 5.0, 1.0)  # Cap at 5 dependencies

    @staticmethod
    def score_historical_success(test_case: Dict[str, Any]) -> float:
        """Score based on historical success rate (0-1)"""
        success_rate = test_case.get("historical_success_rate", 0.5)
        return min(max(float(success_rate), 0.0), 1.0)

    @staticmethod
    def score_ai_confidence(test_case: Dict[str, Any]) -> float:
        """Score based on AI confidence in test case (0-1)"""
        confidence = test_case.get("ai_confidence", 0.5)
        return min(max(float(confidence), 0.0), 1.0)


def calculate_final_score(test_case: Dict[str, Any], weights: RankingWeights) -> float:
    """Calculate final weighted score for a test case"""
    if not weights.validate():
        raise ValueError("Ranking weights must sum to 1.0")

    scorer = CriteriaScorer()
    scores = {
        RankingCriteria.COMPLEXITY: scorer.score_complexity(test_case) * weights.complexity,
        RankingCriteria.PRIORITY: scorer.score_priority(test_case) * weights.priority,
        RankingCriteria.EXECUTION_TIME: scorer.score_execution_time(test_case) * weights.execution_time,
        RankingCriteria.COVERAGE: scorer.score_coverage(test_case) * weights.coverage,
        RankingCriteria.DEPENDENCY_COUNT: scorer.score_dependency_count(test_case) * weights.dependency_count,
        RankingCriteria.HISTORICAL_SUCCESS: scorer.score_historical_success(test_case) * weights.historical_success,
        RankingCriteria.AI_CONFIDENCE: scorer.score_ai_confidence(test_case) * weights.ai_confidence
    }

    return sum(scores.values())