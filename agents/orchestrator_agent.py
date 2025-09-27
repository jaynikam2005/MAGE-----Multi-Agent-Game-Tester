from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import asyncio

class OrchestratorAgent:
    def __init__(self, num_executors: int = 3):
        self.num_executors = num_executors
        self.executors = [
            ExecutorAgent(f"executor_{i}", headless=True) 
            for i in range(num_executors)
        ]
        
    def execute_test_suite(self, test_cases: List[TestCase]) -> List[TestResult]:
        """Execute multiple test cases in parallel"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.num_executors) as executor:
            # Submit test cases to executors
            future_to_test = {
                executor.submit(self._execute_with_retry, test_case, exec_agent): test_case
                for test_case, exec_agent in zip(test_cases, self._round_robin_executors(test_cases))
            }
            
            # Collect results
            for future in as_completed(future_to_test):
                test_case = future_to_test[future]
                try:
                    result = future.result(timeout=300)  # 5 min timeout
                    results.append(result)
                except Exception as e:
                    print(f"Test {test_case.id} failed: {e}")
                    results.append(self._create_error_result(test_case, str(e)))
        
        return results
    
    def _execute_with_retry(self, test_case: TestCase, executor: ExecutorAgent, max_retries: int = 2):
        """Execute test with retry logic"""
        for attempt in range(max_retries + 1):
            try:
                result = executor.execute_test(test_case)
                if result.status == "passed":
                    return result
            except Exception as e:
                if attempt == max_retries:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
        return result