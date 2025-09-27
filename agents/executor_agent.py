from playwright.async_api import async_playwright
from typing import Dict, Any, List
import asyncio
import json
import base64
from datetime import datetime
from backend.core.architecture import TestCase, ExecutionResult
import aiohttp
import cv2
import numpy as np

class ExecutorAgent:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def setup(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch()
        self.context = await self.browser.new_context(
            record_video_dir="artifacts/videos",
            viewport={"width": 1920, "height": 1080}
        )
        self.page = await self.context.new_page()
        await self.context.tracing.start(screenshots=True, snapshots=True)

    async def execute_test_case(self, test_case: TestCase) -> ExecutionResult:
        start_time = datetime.now()
        artifacts = {}
        try:
            await self.setup()
            for step in test_case.steps:
                await self._execute_step(step)
                artifact = await self._capture_artifacts()
                artifacts.update(artifact)
            
            success = True
            error_message = None
            stack_trace = None
            
        except Exception as e:
            success = False
            error_message = str(e)
            stack_trace = e.__traceback__.format()
            
        finally:
            await self._cleanup()
            
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ExecutionResult(
            test_case_id=test_case.id,
            success=success,
            execution_time=execution_time,
            artifacts=artifacts,
            error_message=error_message,
            stack_trace=stack_trace,
            metrics=await self._collect_metrics()
        )

    async def _execute_step(self, step: Dict[str, Any]):
        action = step["action"]
        if action == "click":
            await self.page.click(step["selector"])
        elif action == "type":
            await self.page.fill(step["selector"], step["value"])
        elif action == "wait":
            await self.page.wait_for_selector(step["selector"])
        elif action == "navigate":
            await self.page.goto(step["url"])
        await asyncio.sleep(0.5)

    async def _capture_artifacts(self) -> Dict[str, str]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        artifacts = {}
        
        screenshot = await self.page.screenshot(type="jpeg", quality=80)
        artifacts[f"screenshot_{timestamp}"] = base64.b64encode(screenshot).decode()
        
        html = await self.page.content()
        artifacts[f"dom_{timestamp}"] = html
        
        console_logs = await self.page.evaluate("() => console.logs")
        artifacts[f"console_{timestamp}"] = json.dumps(console_logs)
        
        return artifacts

    async def _collect_metrics(self) -> Dict[str, float]:
        metrics = await self.page.evaluate("""
        () => ({
            loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart,
            domComplete: performance.timing.domComplete - performance.timing.domLoading,
            firstPaint: performance.getEntriesByType('paint')[0].startTime
        })
        """)
        return metrics

    async def _cleanup(self):
        if self.context:
            await self.context.tracing.stop(path="artifacts/trace.zip")
            await self.context.close()
        if self.browser:
            await self.browser.close()