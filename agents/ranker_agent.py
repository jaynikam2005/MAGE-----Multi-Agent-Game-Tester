from typing import List
import numpy as np
from backend.core.architecture import TestCase
from concurrent.futures import ThreadPoolExecutor
import asyncio

class RankerAgent:
    def __init__(self):
        self.feature_weights = {
            "complexity": 0.3,
            "priority": 0.4,
            "coverage": 0.2,
            "efficiency": 0.1
        }
        
    async def rank_test_cases(self, test_cases: List[TestCase]) -> List[TestCase]:
        scores = await self._calculate_scores(test_cases)
        ranked_indices = np.argsort(scores)[::-1]
        return [test_cases[i] for i in ranked_indices]

    async def _calculate_scores(self, test_cases: List[TestCase]) -> np.ndarray:
        with ThreadPoolExecutor() as executor:
            scores = await asyncio.get_event_loop().run_in_executor(
                executor,
                self._parallel_score_calculation,
                test_cases
            )
        return scores

    def _parallel_score_calculation(self, test_cases: List[TestCase]) -> np.ndarray:
        scores = np.zeros(len(test_cases))
        for i, test_case in enumerate(test_cases):
            coverage_score = self._calculate_coverage_score(test_case)
            efficiency_score = self._calculate_efficiency_score(test_case)
            
            scores[i] = (
                self.feature_weights["complexity"] * test_case.complexity +
                self.feature_weights["priority"] * test_case.priority +
                self.feature_weights["coverage"] * coverage_score +
                self.feature_weights["efficiency"] * efficiency_score
            )
        return scores

    def _calculate_coverage_score(self, test_case: TestCase) -> float:
        unique_actions = len(set(step["action"] for step in test_case.steps))
        return min(1.0, unique_actions / 10)

    def _calculate_efficiency_score(self, test_case: TestCase) -> float:
        return 1.0 / (1.0 + test_case.estimated_duration / 300)