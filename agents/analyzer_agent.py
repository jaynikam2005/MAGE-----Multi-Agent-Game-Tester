import hashlib
import difflib
from typing import List, Dict

class AnalyzerAgent:
    def __init__(self, llm_model="gpt-4"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.2)
        
    def validate_results(self, test_results: List[TestResult]) -> Dict:
        """Validate test results with multiple strategies"""
        validation_report = {
            'repeat_validation': {},
            'cross_agent_validation': {},
            'consistency_scores': {},
            'anomalies': []
        }
        
        # Repeat validation - run same test multiple times
        for result in test_results:
            repeat_score = self._validate_repeatability(result)
            validation_report['repeat_validation'][result.test_case_id] = repeat_score
        
        # Cross-agent validation - compare results across agents
        cross_validation = self._cross_validate_results(test_results)
        validation_report['cross_agent_validation'] = cross_validation
        
        # Detect anomalies
        anomalies = self._detect_anomalies(test_results)
        validation_report['anomalies'] = anomalies
        
        return validation_report
    
    def _validate_repeatability(self, result: TestResult, runs: int = 3) -> float:
        """Validate test repeatability"""
        executor = ExecutorAgent("validator", headless=True)
        outcomes = []
        
        for _ in range(runs):
            repeat_result = executor.execute_test(result.test_case_id)
            outcomes.append(repeat_result.status)
        
        # Calculate consistency score
        consistency = outcomes.count(result.status) / len(outcomes)
        return consistency
    
    def _cross_validate_results(self, results: List[TestResult]) -> Dict:
        """Cross-validate results between different agents"""
        validation_matrix = {}
        
        # Group results by test case
        grouped = {}
        for result in results:
            if result.test_case_id not in grouped:
                grouped[result.test_case_id] = []
            grouped[result.test_case_id].append(result)
        
        # Compare results within groups
        for test_id, group_results in grouped.items():
            if len(group_results) > 1:
                consistency = self._calculate_consistency(group_results)
                validation_matrix[test_id] = consistency
        
        return validation_matrix