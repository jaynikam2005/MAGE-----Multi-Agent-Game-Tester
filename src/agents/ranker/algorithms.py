"""Ranking algorithms for test case prioritization"""

from typing import List, Dict, Any
from .criteria import RankingWeights, calculate_final_score


class RankingAlgorithm:
    """Base class for ranking algorithms"""

    def __init__(self, weights: RankingWeights = None):
        self.weights = weights or RankingWeights()

    def rank(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank test cases according to the algorithm"""
        raise NotImplementedError


class WeightedScoreRanking(RankingAlgorithm):
    """Rank test cases by weighted criteria scores"""

    def rank(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank test cases by their weighted scores"""
        scored_cases = [
            (case, calculate_final_score(case, self.weights))
            for case in test_cases
        ]
        
        # Sort by score in descending order
        scored_cases.sort(key=lambda x: x[1], reverse=True)
        
        # Return ranked test cases with scores
        return [
            {**case, "ranking_score": score}
            for case, score in scored_cases
        ]


class DependencyAwareRanking(RankingAlgorithm):
    """Rank test cases considering dependencies"""

    def _build_dependency_graph(self, test_cases: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Build a graph of test case dependencies"""
        graph = {}
        for case in test_cases:
            case_id = case["id"]
            graph[case_id] = case.get("prerequisites", [])
        return graph

    def _get_execution_order(self, graph: Dict[str, List[str]]) -> List[str]:
        """Get topologically sorted execution order"""
        visited = set()
        temp = set()
        order = []

        def visit(case_id: str):
            if case_id in temp:
                raise ValueError("Circular dependency detected")
            if case_id in visited:
                return
            temp.add(case_id)
            for dep in graph.get(case_id, []):
                visit(dep)
            temp.remove(case_id)
            visited.add(case_id)
            order.append(case_id)

        for case_id in graph:
            if case_id not in visited:
                visit(case_id)

        return order[::-1]  # Reverse to get correct order

    def rank(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank test cases considering dependencies and scores"""
        # First, calculate scores
        scored_cases = {
            case["id"]: (case, calculate_final_score(case, self.weights))
            for case in test_cases
        }

        # Build dependency graph
        graph = self._build_dependency_graph(test_cases)

        try:
            # Get execution order
            order = self._get_execution_order(graph)

            # Sort test cases by execution order and score
            ranked_cases = []
            for case_id in order:
                if case_id in scored_cases:
                    case, score = scored_cases[case_id]
                    ranked_cases.append({**case, "ranking_score": score})

            return ranked_cases

        except ValueError as e:
            # Fall back to simple weighted scoring if circular dependencies found
            return WeightedScoreRanking(self.weights).rank(test_cases)


class AdaptiveRanking(RankingAlgorithm):
    """Rank test cases adapting to historical results"""

    def __init__(self, weights: RankingWeights = None, history_weight: float = 0.3):
        super().__init__(weights)
        self.history_weight = history_weight
        self.historical_data = {}  # Would be loaded from database

    def _adjust_weights(self, test_case: Dict[str, Any]) -> RankingWeights:
        """Adjust weights based on historical performance"""
        case_id = test_case["id"]
        if case_id in self.historical_data:
            history = self.historical_data[case_id]
            
            # Example: Increase priority weight for historically problematic tests
            if history.get("failure_rate", 0) > 0.2:
                return RankingWeights(
                    priority=self.weights.priority * 1.2,
                    complexity=self.weights.complexity * 0.9,
                    execution_time=self.weights.execution_time,
                    coverage=self.weights.coverage,
                    dependency_count=self.weights.dependency_count,
                    historical_success=self.weights.historical_success,
                    ai_confidence=self.weights.ai_confidence
                )
        
        return self.weights

    def rank(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank test cases with adaptive weights"""
        scored_cases = []
        
        for case in test_cases:
            adjusted_weights = self._adjust_weights(case)
            base_score = calculate_final_score(case, adjusted_weights)
            
            # Blend with historical performance
            historical_score = self.historical_data.get(case["id"], {}).get("score", 0.5)
            final_score = (base_score * (1 - self.history_weight) + 
                         historical_score * self.history_weight)
            
            scored_cases.append((case, final_score))
        
        # Sort by final score
        scored_cases.sort(key=lambda x: x[1], reverse=True)
        
        return [
            {**case, "ranking_score": score}
            for case, score in scored_cases
        ]