from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from datetime import datetime

class ExecutorAgent:
    def __init__(self, agent_id: str, headless: bool = False):
        self.agent_id = agent_id
        self.driver = self._setup_driver(headless)
        self.artifacts = {}
        
    def _setup_driver(self, headless: bool) -> webdriver.Chrome:
        """Setup Selenium WebDriver with security configurations"""
        options = Options()
        
        # Security configurations
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        if headless:
            options.add_argument('--headless')
        
        # Enable logging for network and console
        options.set_capability('goog:loggingPrefs', {
            'browser': 'ALL',
            'performance': 'ALL'
        })
        
        return webdriver.Chrome(options=options)
    
    def execute_test(self, test_case: TestCase) -> TestResult:
        """Execute a single test case"""
        start_time = time.time()
        artifacts = {
            'screenshots': [],
            'dom_snapshots': [],
            'console_logs': [],
            'network_logs': []
        }
        
        try:
            # Navigate to game
            self.driver.get("https://play.ezygamers.com/")
            time.sleep(2)  # Wait for initial load
            
            # Execute test steps
            for i, step in enumerate(test_case.steps):
                step_artifacts = self._execute_step(step, i)
                self._collect_artifacts(artifacts, step_artifacts, i)
            
            # Capture final state
            final_artifacts = self._capture_final_state()
            artifacts.update(final_artifacts)
            
            status = "passed"
            
        except Exception as e:
            status = "failed"
            artifacts['error'] = str(e)
            self._capture_error_state(artifacts)
        
        execution_time = time.time() - start_time
        
        return TestResult(
            test_case_id=test_case.id,
            status=status,
            artifacts=artifacts,
            validation_results={},
            execution_time=execution_time,
            reproducibility_score=0.0
        )
    
    def _execute_step(self, step: dict, step_index: int) -> dict:
        """Execute a single test step"""
        action = step.get('action')
        target = step.get('target')
        value = step.get('value')
        
        step_artifacts = {}
        
        if action == 'click':
            element = self.driver.find_element(By.CSS_SELECTOR, target)
            element.click()
        elif action == 'input':
            element = self.driver.find_element(By.CSS_SELECTOR, target)
            element.clear()
            element.send_keys(value)
        elif action == 'wait':
            time.sleep(float(value))
        elif action == 'verify':
            # Verification logic
            pass
        
        # Capture artifacts after step
        step_artifacts['screenshot'] = self._capture_screenshot(f"step_{step_index}")
        step_artifacts['dom'] = self._capture_dom()
        step_artifacts['console'] = self._capture_console_logs()
        
        return step_artifacts
    
    def _capture_screenshot(self, name: str) -> str:
        """Capture and save screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"artifacts/screenshots/{self.agent_id}_{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        return filename
    
    def _capture_dom(self) -> str:
        """Capture DOM snapshot"""
        return self.driver.page_source
    
    def _capture_console_logs(self) -> List[dict]:
        """Capture browser console logs"""
        logs = self.driver.get_log('browser')
        return logs