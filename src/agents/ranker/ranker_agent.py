"""
Ranker Agent for test case prioritization
"""
import asyncio
from typing import List, Dict, Any

from .criteria import (
    RankingCriteria,
    RankingWeights,
    calculate_final_score
)


class RankerAgent:
    """Agent responsible for ranking test cases"""

    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.weights = RankingWeights()
        
        # Customize weights if provided in config
        if "ranking_weights" in self.config:
            for criterion, weight in self.config["ranking_weights"].items():
                if hasattr(self.weights, criterion):
                    setattr(self.weights, criterion, weight)

    async def initialize(self) -> None:
        """Initialize agent"""
        # Validate weights
        if not self.weights.validate():
            raise ValueError("Invalid ranking weights configuration")

    async def rank_test_cases(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank test cases based on configured criteria"""
        # Calculate scores for each test case
        scored_cases = []
        for test in test_cases:
            score = calculate_final_score(test, self.weights)
            scored_cases.append((score, test))
        
        # Sort by score in descending order
        scored_cases.sort(reverse=True, key=lambda x: x[0])
        
        # Return sorted test cases
        return [case for _, case in scored_cases]

    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get agent health metrics"""
        return {
            "cpu_usage": 0.0,  # Placeholder
            "memory_usage": 0.0,  # Placeholder
            "status": "operational"
        }