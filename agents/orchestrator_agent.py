from typing import List, Dict, Any
import asyncio
import uuid
from datetime import datetime
from backend.core.architecture import TestCase, TestReport, ExecutionResult, TestStatus
from agents.executor_agent import ExecutorAgent
from agents.analyzer_agent import AnalyzerAgent

class OrchestratorAgent:
    def __init__(self):
        self.executions: Dict[str, Dict[str, Any]] = {}
        self.reports: Dict[str, TestReport] = {}
        self.executor_pool: List[ExecutorAgent] = []
        self.analyzer = AnalyzerAgent()
        self.max_concurrent_tests = 3
        self.execution_semaphore = asyncio.Semaphore(self.max_concurrent_tests)

    async def schedule_execution(self, test_cases: List[TestCase]) -> str:
        execution_id = str(uuid.uuid4())
        self.executions[execution_id] = {
            "test_cases": test_cases,
            "status": TestStatus.PENDING,
            "results": [],
            "start_time": datetime.now()
        }
        
        asyncio.create_task(self._execute_test_batch(execution_id))
        return execution_id

    async def _execute_test_batch(self, execution_id: str):
        execution = self.executions[execution_id]
        execution["status"] = TestStatus.RUNNING
        
        tasks = []
        for test_case in execution["test_cases"]:
            task = asyncio.create_task(self._execute_single_test(test_case))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        execution["results"] = results
        execution["status"] = TestStatus.COMPLETED
        
        report = await self._generate_report(execution_id)
        self.reports[report.id] = report

    async def _execute_single_test(self, test_case: TestCase) -> ExecutionResult:
        async with self.execution_semaphore:
            executor = ExecutorAgent()
            result = await executor.execute_test_case(test_case)
            validation = await self.analyzer.validate_test_result(result)
            result.validation_results = validation
            return result

    async def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        if execution_id not in self.executions:
            raise KeyError(f"Execution {execution_id} not found")
            
        execution = self.executions[execution_id]
        return {
            "status": execution["status"].value,
            "completed_tests": len(execution["results"]),
            "total_tests": len(execution["test_cases"]),
            "start_time": execution["start_time"].isoformat()
        }

    async def get_reports(self, limit: int = 10) -> List[TestReport]:
        reports = list(self.reports.values())
        reports.sort(key=lambda x: x.timestamp, reverse=True)
        return reports[:limit]

    async def get_report(self, report_id: str) -> TestReport:
        return self.reports.get(report_id)

    async def _generate_report(self, execution_id: str) -> TestReport:
        execution = self.executions[execution_id]
        results = execution["results"]
        
        successful_tests = sum(1 for r in results if r.success)
        failed_tests = len(results) - successful_tests
        
        execution_time = (datetime.now() - execution["start_time"]).total_seconds()
        
        validation_summary = await self.analyzer.generate_validation_summary(results)
        
        return TestReport(
            total_tests=len(results),
            successful_tests=successful_tests,
            failed_tests=failed_tests,
            execution_time=execution_time,
            validation_summary=validation_summary,
            test_results=results,
            validation_results=[r.validation_results for r in results],
            artifacts_location=f"artifacts/{execution_id}"
        )