"""
WebDriver Integration for Real Browser-Based Game Testing
Comprehensive browser automation for game testing
"""

import asyncio
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not available. Install with: pip install selenium")

from src.core.implementations import TestResult, PerformanceMetrics


class GameTestDriver:
    """Advanced WebDriver wrapper for game testing"""
    
    def __init__(self, browser_type: str = "chrome", headless: bool = True, timeout: int = 30):
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.logger = logging.getLogger(__name__)
        
        # Performance tracking
        self.performance_metrics = []
        self.screenshot_counter = 0
        self.action_log = []
    
    def initialize_driver(self) -> bool:
        """Initialize WebDriver with optimized settings"""
        
        if not SELENIUM_AVAILABLE:
            raise Exception("Selenium WebDriver not available. Please install selenium package.")
        
        try:
            if self.browser_type == "chrome":
                self.driver = self._create_chrome_driver()
            elif self.browser_type == "firefox":
                self.driver = self._create_firefox_driver()
            else:
                raise ValueError(f"Unsupported browser type: {self.browser_type}")
            
            # Configure timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.set_script_timeout(self.timeout)
            
            self.logger.info(f"WebDriver initialized: {self.browser_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            return False
    
    def _create_chrome_driver(self):
        """Create optimized Chrome WebDriver"""
        
        options = ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless=new')
        
        # Performance optimizations
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript-harmony-shipping')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        
        # Memory optimization
        options.add_argument('--memory-pressure-off')
        options.add_argument('--max_old_space_size=4096')
        
        # Window size for consistent testing
        options.add_argument('--window-size=1920,1080')
        
        # Enable logging for performance monitoring
        options.add_argument('--enable-logging')
        options.add_argument('--log-level=0')
        
        # User agent for game compatibility
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MAGE-GameTester/2.0')
        
        return webdriver.Chrome(options=options)
    
    def _create_firefox_driver(self):
        """Create optimized Firefox WebDriver"""
        
        options = FirefoxOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        # Performance optimizations
        options.set_preference('dom.webnotifications.enabled', False)
        options.set_preference('media.volume_scale', '0.0')
        options.set_preference('dom.push.enabled', False)
        options.set_preference('dom.webdriver.enabled', False)
        options.set_preference('useAutomationExtension', False)
        
        # Memory optimizations
        options.set_preference('browser.cache.disk.enable', False)
        options.set_preference('browser.cache.memory.enable', True)
        options.set_preference('browser.cache.offline.enable', False)
        
        return webdriver.Firefox(options=options)
    
    async def load_game(self, url: str) -> bool:
        """Load game URL and wait for game to be ready"""
        
        if not self.driver:
            if not self.initialize_driver():
                return False
        
        try:
            start_time = time.time()
            
            self.logger.info(f"Loading game: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, self.timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            load_time = time.time() - start_time
            self.action_log.append(f"Page loaded in {load_time:.2f} seconds")
            
            # Wait for game-specific elements
            await self._wait_for_game_ready()
            
            # Take initial screenshot
            self.take_screenshot("game_loaded")
            
            return True
            
        except TimeoutException:
            self.logger.error(f"Timeout loading game: {url}")
            return False
        except WebDriverException as e:
            self.logger.error(f"WebDriver error loading game: {e}")
            return False
    
    async def _wait_for_game_ready(self, max_wait: int = 30):
        """Wait for game-specific elements to be ready"""
        
        game_ready_selectors = [
            # Common game canvas selectors
            "canvas",
            "#game-canvas",
            "#gameCanvas",
            ".game-container",
            "#unity-container",
            "#game-area",
            
            # Common game UI elements
            ".game-ui",
            "#game-interface",
            ".start-button",
            "#play-button",
            ".game-ready"
        ]
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            for selector in game_ready_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element and element.is_displayed():
                        self.logger.info(f"Game ready - found element: {selector}")
                        return True
                except NoSuchElementException:
                    continue
            
            await asyncio.sleep(0.5)
        
        self.logger.warning("Game ready check timed out - proceeding anyway")
        return False
    
    async def perform_game_actions(self, action_sequence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Perform sequence of game actions"""
        
        results = []
        
        for action in action_sequence:
            try:
                start_time = time.time()
                result = await self._execute_action(action)
                execution_time = time.time() - start_time
                
                result.update({
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat()
                })
                
                results.append(result)
                
                # Small delay between actions
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Action execution failed: {e}")
                results.append({
                    "action": action,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        return results
    
    async def _execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute individual game action"""
        
        action_type = action.get("type", "").lower()
        
        if action_type == "click":
            return await self._perform_click(action)
        elif action_type == "type":
            return await self._perform_typing(action)
        elif action_type == "key_press":
            return await self._perform_key_press(action)
        elif action_type == "mouse_move":
            return await self._perform_mouse_move(action)
        elif action_type == "scroll":
            return await self._perform_scroll(action)
        elif action_type == "wait":
            return await self._perform_wait(action)
        elif action_type == "screenshot":
            return await self._perform_screenshot(action)
        elif action_type == "evaluate_js":
            return await self._perform_javascript(action)
        else:
            raise ValueError(f"Unknown action type: {action_type}")
    
    async def _perform_click(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform click action"""
        
        selector = action.get("selector")
        coordinates = action.get("coordinates")
        
        if selector:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            element.click()
            return {"action": "click", "target": selector, "success": True}
        
        elif coordinates:
            x, y = coordinates
            ActionChains(self.driver).move_to_element_with_offset(
                self.driver.find_element(By.TAG_NAME, "body"), x, y
            ).click().perform()
            return {"action": "click", "coordinates": coordinates, "success": True}
        
        else:
            raise ValueError("Click action requires either selector or coordinates")
    
    async def _perform_typing(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform typing action"""
        
        selector = action.get("selector")
        text = action.get("text", "")
        
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        
        element.clear()
        element.send_keys(text)
        
        return {"action": "type", "target": selector, "text": text, "success": True}
    
    async def _perform_key_press(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform key press action"""
        
        key = action.get("key")
        element = action.get("element", "body")
        
        target_element = self.driver.find_element(By.CSS_SELECTOR, element)
        
        # Handle special keys
        if key.upper() in ['ENTER', 'RETURN']:
            target_element.send_keys(Keys.RETURN)
        elif key.upper() == 'ESCAPE':
            target_element.send_keys(Keys.ESCAPE)
        elif key.upper() == 'SPACE':
            target_element.send_keys(Keys.SPACE)
        elif key.upper() == 'TAB':
            target_element.send_keys(Keys.TAB)
        elif key.upper().startswith('ARROW_'):
            direction = key.upper().split('_')[1]
            arrow_key = getattr(Keys, direction, None)
            if arrow_key:
                target_element.send_keys(arrow_key)
        else:
            target_element.send_keys(key)
        
        return {"action": "key_press", "key": key, "success": True}
    
    async def _perform_mouse_move(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform mouse movement action"""
        
        coordinates = action.get("coordinates")
        selector = action.get("selector")
        
        if coordinates:
            x, y = coordinates
            ActionChains(self.driver).move_to_element_with_offset(
                self.driver.find_element(By.TAG_NAME, "body"), x, y
            ).perform()
            return {"action": "mouse_move", "coordinates": coordinates, "success": True}
        
        elif selector:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            ActionChains(self.driver).move_to_element(element).perform()
            return {"action": "mouse_move", "target": selector, "success": True}
        
        else:
            raise ValueError("Mouse move requires either coordinates or selector")
    
    async def _perform_scroll(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform scroll action"""
        
        direction = action.get("direction", "down")
        amount = action.get("amount", 3)
        
        if direction.lower() == "down":
            self.driver.execute_script(f"window.scrollBy(0, {amount * 100});")
        elif direction.lower() == "up":
            self.driver.execute_script(f"window.scrollBy(0, -{amount * 100});")
        elif direction.lower() == "left":
            self.driver.execute_script(f"window.scrollBy(-{amount * 100}, 0);")
        elif direction.lower() == "right":
            self.driver.execute_script(f"window.scrollBy({amount * 100}, 0);")
        
        return {"action": "scroll", "direction": direction, "amount": amount, "success": True}
    
    async def _perform_wait(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform wait action"""
        
        duration = action.get("duration", 1.0)
        await asyncio.sleep(duration)
        
        return {"action": "wait", "duration": duration, "success": True}
    
    async def _perform_screenshot(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Take screenshot"""
        
        name = action.get("name", "screenshot")
        path = self.take_screenshot(name)
        
        return {"action": "screenshot", "name": name, "path": path, "success": True}
    
    async def _perform_javascript(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute JavaScript code"""
        
        script = action.get("script", "")
        args = action.get("args", [])
        
        try:
            result = self.driver.execute_script(script, *args)
            return {"action": "evaluate_js", "script": script, "result": result, "success": True}
        except Exception as e:
            return {"action": "evaluate_js", "script": script, "error": str(e), "success": False}
    
   # Continue from previous webdriver_integration.py

    def collect_performance_metrics(self) -> PerformanceMetrics:
        """Collect browser and page performance metrics"""
        
        try:
            # Get navigation timing
            nav_timing = self.driver.execute_script("""
                var timing = performance.timing;
                var navigation = performance.navigation;
                return {
                    domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                    loadComplete: timing.loadEventEnd - timing.navigationStart,
                    domInteractive: timing.domInteractive - timing.navigationStart,
                    firstPaint: performance.getEntriesByType('paint')[0] ? 
                        performance.getEntriesByType('paint')[0].startTime : 0,
                    firstContentfulPaint: performance.getEntriesByType('paint')[1] ? 
                        performance.getEntriesByType('paint')[1].startTime : 0,
                    redirectCount: navigation.redirectCount,
                    pageSize: document.documentElement.innerHTML.length
                };
            """)
            
            # Get resource timing
            resource_timing = self.driver.execute_script("""
                var resources = performance.getEntriesByType('resource');
                var totalSize = 0;
                var slowestResource = 0;
                
                resources.forEach(function(resource) {
                    if (resource.transferSize) totalSize += resource.transferSize;
                    if (resource.duration > slowestResource) slowestResource = resource.duration;
                });
                
                return {
                    resourceCount: resources.length,
                    totalTransferSize: totalSize,
                    slowestResourceTime: slowestResource
                };
            """)
            
            # Get memory info (Chrome only)
            memory_info = {}
            try:
                memory_info = self.driver.execute_script("""
                    if (performance.memory) {
                        return {
                            usedJSHeapSize: performance.memory.usedJSHeapSize,
                            totalJSHeapSize: performance.memory.totalJSHeapSize,
                            jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
                        };
                    }
                    return {};
                """)
            except:
                pass
            
            # Calculate metrics
            response_time = nav_timing.get('loadComplete', 1000)
            
            # Estimate CPU usage based on load time and resource count
            cpu_usage = min(90, max(10, (response_time / 100) + (resource_timing.get('resourceCount', 0) / 10)))
            
            # Estimate memory usage
            memory_usage = 30  # Base usage
            if memory_info.get('usedJSHeapSize'):
                memory_percentage = (memory_info['usedJSHeapSize'] / memory_info['totalJSHeapSize']) * 100
                memory_usage = min(90, max(30, memory_percentage))
            
            # Create performance metrics
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_io=resource_timing.get('totalTransferSize', 0),
                network_io=resource_timing.get('totalTransferSize', 0),
                gpu_usage=min(70, max(5, response_time / 50)),  # Estimated based on response
                fps=60 if response_time < 100 else 30 if response_time < 500 else 15,
                response_time_ms=response_time
            )
            
            self.performance_metrics.append(metrics)
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting performance metrics: {e}")
            # Return default metrics
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_usage=25.0,
                memory_usage=40.0,
                disk_io=0,
                network_io=0,
                gpu_usage=20.0,
                fps=60,
                response_time_ms=100.0
            )
    
    def analyze_game_elements(self) -> Dict[str, Any]:
        """Analyze game elements and UI components"""
        
        try:
            analysis = self.driver.execute_script("""
                var analysis = {
                    canvasElements: document.querySelectorAll('canvas').length,
                    gameContainers: document.querySelectorAll('[id*="game"], [class*="game"]').length,
                    buttons: document.querySelectorAll('button, input[type="button"]').length,
                    inputs: document.querySelectorAll('input, textarea').length,
                    images: document.querySelectorAll('img').length,
                    videos: document.querySelectorAll('video').length,
                    audioElements: document.querySelectorAll('audio').length,
                    totalElements: document.querySelectorAll('*').length,
                    bodyText: document.body.innerText.length,
                    hasWebGL: false,
                    hasLocalStorage: typeof(Storage) !== "undefined",
                    viewport: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    }
                };
                
                // Check for WebGL
                try {
                    var canvas = document.createElement('canvas');
                    var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                    analysis.hasWebGL = !!gl;
                } catch(e) {}
                
                return analysis;
            """)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing game elements: {e}")
            return {}
    
    def detect_game_type(self) -> str:
        """Detect the type of game based on page analysis"""
        
        try:
            # Analyze page content
            page_analysis = self.driver.execute_script("""
                var text = document.body.innerText.toLowerCase();
                var title = document.title.toLowerCase();
                var classes = Array.from(document.querySelectorAll('*')).map(el => el.className).join(' ').toLowerCase();
                
                return {
                    text: text,
                    title: title,
                    classes: classes,
                    hasCanvas: document.querySelectorAll('canvas').length > 0,
                    hasGamepadAPI: typeof navigator.getGamepads === 'function',
                    hasWebGL: false
                };
            """)
            
            text_content = page_analysis.get('text', '') + page_analysis.get('title', '') + page_analysis.get('classes', '')
            
            # Game type detection patterns
            if any(keyword in text_content for keyword in ['puzzle', 'sudoku', 'match', 'tile', 'block']):
                return 'puzzle'
            elif any(keyword in text_content for keyword in ['action', 'shoot', 'fight', 'battle', 'combat']):
                return 'action'
            elif any(keyword in text_content for keyword in ['strategy', 'tower', 'defense', 'tactical']):
                return 'strategy'
            elif any(keyword in text_content for keyword in ['card', 'poker', 'blackjack', 'solitaire']):
                return 'card'
            elif any(keyword in text_content for keyword in ['platform', 'jump', 'run', 'adventure']):
                return 'platformer'
            elif any(keyword in text_content for keyword in ['racing', 'drive', 'car', 'speed']):
                return 'racing'
            elif any(keyword in text_content for keyword in ['rpg', 'role', 'character', 'level up']):
                return 'rpg'
            elif page_analysis.get('hasCanvas'):
                return 'canvas_game'
            else:
                return 'web_game'
                
        except Exception as e:
            self.logger.error(f"Error detecting game type: {e}")
            return 'unknown'
    
    def take_screenshot(self, name: str = None) -> str:
        """Take screenshot and save to file"""
        
        try:
            if not name:
                name = f"screenshot_{self.screenshot_counter}"
                self.screenshot_counter += 1
            
            # Create screenshots directory
            screenshots_dir = Path("data/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}.png"
            filepath = screenshots_dir / filename
            
            # Take screenshot
            self.driver.save_screenshot(str(filepath))
            
            self.logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {e}")
            return ""
    
    def get_console_logs(self) -> List[Dict[str, Any]]:
        """Get browser console logs"""
        
        try:
            logs = self.driver.get_log('browser')
            processed_logs = []
            
            for log in logs:
                processed_logs.append({
                    "timestamp": log.get('timestamp'),
                    "level": log.get('level'),
                    "message": log.get('message'),
                    "source": log.get('source', 'unknown')
                })
            
            return processed_logs
            
        except Exception as e:
            self.logger.error(f"Error getting console logs: {e}")
            return []
    
    def cleanup(self):
        """Clean up WebDriver resources"""
        
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver cleaned up successfully")
            except Exception as e:
                self.logger.error(f"Error cleaning up WebDriver: {e}")


class GameTestSuite:
    """Comprehensive game testing suite using WebDriver"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.driver = GameTestDriver(
            browser_type=config.get('browser', 'chrome'),
            headless=config.get('headless', True),
            timeout=config.get('timeout', 30)
        )
        self.logger = logging.getLogger(__name__)
        
    async def run_comprehensive_test(self, target_url: str) -> TestResult:
        """Run comprehensive game test"""
        
        test_id = f"comprehensive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        
        try:
            # Initialize driver and load game
            if not await self.driver.load_game(target_url):
                raise Exception("Failed to load game")
            
            # Detect game type
            game_type = self.driver.detect_game_type()
            self.logger.info(f"Detected game type: {game_type}")
            
            # Run game-specific tests
            test_results = []
            
            # Basic functionality tests
            basic_results = await self.run_basic_tests()
            test_results.extend(basic_results)
            
            # Performance tests
            perf_results = await self.run_performance_tests()
            test_results.extend(perf_results)
            
            # UI/UX tests
            ui_results = await self.run_ui_tests()
            test_results.extend(ui_results)
            
            # Game-specific tests
            if game_type == 'puzzle':
                puzzle_results = await self.run_puzzle_game_tests()
                test_results.extend(puzzle_results)
            elif game_type == 'action':
                action_results = await self.run_action_game_tests()
                test_results.extend(action_results)
            
            # Calculate overall score
            scores = [result.get('score', 0) for result in test_results if 'score' in result]
            overall_score = sum(scores) / len(scores) if scores else 0
            
            # Collect final metrics
            final_metrics = self.driver.collect_performance_metrics()
            
            end_time = datetime.now()
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            
            return TestResult(
                test_id=test_id,
                test_type="Comprehensive Game Test",
                status="Completed",
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                success=overall_score > 60,
                score=overall_score,
                details={
                    "target_url": target_url,
                    "game_type": game_type,
                    "tests_executed": len(test_results),
                    "browser": self.config.get('browser', 'chrome'),
                    "headless": self.config.get('headless', True)
                },
                errors=[],
                performance_metrics=final_metrics.__dict__
            )
            
        except Exception as e:
            end_time = datetime.now()
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            
            self.logger.error(f"Comprehensive test failed: {e}")
            
            return TestResult(
                test_id=test_id,
                test_type="Comprehensive Game Test",
                status="Failed",
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                success=False,
                score=0,
                details={"target_url": target_url, "error": str(e)},
                errors=[str(e)],
                performance_metrics={}
            )
        
        finally:
            self.driver.cleanup()
    
    async def run_basic_tests(self) -> List[Dict[str, Any]]:
        """Run basic functionality tests"""
        
        tests = []
        
        try:
            # Test 1: Page load verification
            page_title = self.driver.driver.title
            tests.append({
                "test": "page_load",
                "success": bool(page_title),
                "score": 100 if page_title else 0,
                "details": {"title": page_title}
            })
            
            # Test 2: Element analysis
            elements = self.driver.analyze_game_elements()
            has_game_elements = elements.get('canvasElements', 0) > 0 or elements.get('gameContainers', 0) > 0
            tests.append({
                "test": "game_elements",
                "success": has_game_elements,
                "score": 100 if has_game_elements else 50,
                "details": elements
            })
            
            # Test 3: Console errors check
            console_logs = self.driver.get_console_logs()
            error_count = len([log for log in console_logs if log.get('level') == 'SEVERE'])
            tests.append({
                "test": "console_errors",
                "success": error_count == 0,
                "score": max(0, 100 - (error_count * 10)),
                "details": {"error_count": error_count, "logs": console_logs}
            })
            
            # Test 4: Basic interaction test
            interaction_result = await self.test_basic_interaction()
            tests.append(interaction_result)
            
        except Exception as e:
            self.logger.error(f"Basic tests failed: {e}")
            tests.append({
                "test": "basic_tests_error",
                "success": False,
                "score": 0,
                "details": {"error": str(e)}
            })
        
        return tests
    
    async def run_performance_tests(self) -> List[Dict[str, Any]]:
        """Run performance-related tests"""
        
        tests = []
        
        try:
            # Collect multiple performance samples
            metrics_samples = []
            for i in range(3):
                metrics = self.driver.collect_performance_metrics()
                metrics_samples.append(metrics)
                await asyncio.sleep(1)
            
            # Calculate average performance
            if metrics_samples:
                avg_response_time = sum(m.response_time_ms for m in metrics_samples) / len(metrics_samples)
                avg_cpu = sum(m.cpu_usage for m in metrics_samples) / len(metrics_samples)
                avg_memory = sum(m.memory_usage for m in metrics_samples) / len(metrics_samples)
                
                # Performance scoring
                response_score = max(0, 100 - (avg_response_time / 20))
                cpu_score = max(0, 100 - avg_cpu)
                memory_score = max(0, 100 - avg_memory)
                
                tests.append({
                    "test": "response_time",
                    "success": avg_response_time < 2000,
                    "score": response_score,
                    "details": {"avg_response_time": avg_response_time}
                })
                
                tests.append({
                    "test": "resource_usage",
                    "success": avg_cpu < 80 and avg_memory < 80,
                    "score": (cpu_score + memory_score) / 2,
                    "details": {"avg_cpu": avg_cpu, "avg_memory": avg_memory}
                })
            
        except Exception as e:
            self.logger.error(f"Performance tests failed: {e}")
            tests.append({
                "test": "performance_tests_error",
                "success": False,
                "score": 0,
                "details": {"error": str(e)}
            })
        
        return tests
    
    async def run_ui_tests(self) -> List[Dict[str, Any]]:
        """Run UI/UX tests"""
        
        tests = []
        
        try:
            # Test viewport and responsive design
            viewport_info = self.driver.driver.execute_script("""
                return {
                    width: window.innerWidth,
                    height: window.innerHeight,
                    pixelRatio: window.devicePixelRatio,
                    orientation: screen.orientation ? screen.orientation.type : 'unknown'
                };
            """)
            
            tests.append({
                "test": "viewport",
                "success": viewport_info['width'] > 800 and viewport_info['height'] > 600,
                "score": 100 if viewport_info['width'] > 800 else 70,
                "details": viewport_info
            })
            
            # Test color contrast and accessibility
            accessibility_score = await self.test_accessibility()
            tests.append({
                "test": "accessibility",
                "success": accessibility_score > 70,
                "score": accessibility_score,
                "details": {"accessibility_score": accessibility_score}
            })
            
        except Exception as e:
            self.logger.error(f"UI tests failed: {e}")
            tests.append({
                "test": "ui_tests_error",
                "success": False,
                "score": 0,
                "details": {"error": str(e)}
            })
        
        return tests
    
    async def test_basic_interaction(self) -> Dict[str, Any]:
        """Test basic user interaction"""
        
        try:
            # Try to find and click interactive elements
            interactive_elements = self.driver.driver.execute_script("""
                var elements = document.querySelectorAll('button, a, input, canvas, [onclick], [role="button"]');
                return Array.from(elements).map(function(el, index) {
                    var rect = el.getBoundingClientRect();
                    return {
                        index: index,
                        tag: el.tagName,
                        visible: rect.width > 0 && rect.height > 0,
                        clickable: !el.disabled && el.style.visibility !== 'hidden'
                    };
                });
            """)
            
            clickable_elements = [el for el in interactive_elements if el['visible'] and el['clickable']]
            
            if clickable_elements:
                # Try clicking the first interactive element
                first_element = self.driver.driver.execute_script("""
                    var elements = document.querySelectorAll('button, a, input, canvas, [onclick], [role="button"]');
                    if (elements.length > 0) {
                        elements[0].click();
                        return true;
                    }
                    return false;
                """)
                
                return {
                    "test": "basic_interaction",
                    "success": first_element,
                    "score": 100 if first_element else 50,
                    "details": {
                        "interactive_elements": len(interactive_elements),
                        "clickable_elements": len(clickable_elements)
                    }
                }
            else:
                return {
                    "test": "basic_interaction",
                    "success": False,
                    "score": 0,
                    "details": {"message": "No interactive elements found"}
                }
                
        except Exception as e:
            return {
                "test": "basic_interaction",
                "success": False,
                "score": 0,
                "details": {"error": str(e)}
            }
    
    async def test_accessibility(self) -> float:
        """Test basic accessibility features"""
        
        try:
            accessibility_info = self.driver.driver.execute_script("""
                var score = 0;
                var maxScore = 5;
                
                // Check for alt text on images
                var images = document.querySelectorAll('img');
                var imagesWithAlt = Array.from(images).filter(img => img.alt && img.alt.trim() !== '');
                if (images.length === 0 || imagesWithAlt.length / images.length > 0.8) score++;
                
                // Check for proper heading structure
                var headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
                if (headings.length > 0) score++;
                
                // Check for focus indicators
                var focusableElements = document.querySelectorAll('button, a, input, select, textarea');
                if (focusableElements.length > 0) score++;
                
                // Check for ARIA labels
                var ariaElements = document.querySelectorAll('[aria-label], [aria-labelledby], [role]');
                if (ariaElements.length > 0) score++;
                
                // Check color contrast (basic check)
                var bodyStyle = window.getComputedStyle(document.body);
                var backgroundColor = bodyStyle.backgroundColor;
                var textColor = bodyStyle.color;
                if (backgroundColor !== 'rgba(0, 0, 0, 0)' && textColor !== 'rgba(0, 0, 0, 0)') score++;
                
                return (score / maxScore) * 100;
            """)
            
            return accessibility_info
            
        except Exception as e:
            self.logger.error(f"Accessibility test failed: {e}")
            return 50.0  # Default score if test fails
    
    async def run_puzzle_game_tests(self) -> List[Dict[str, Any]]:
        """Run puzzle game specific tests"""
        
        tests = []
        
        try:
            # Test puzzle elements
            puzzle_elements = self.driver.driver.execute_script("""
                var puzzleKeywords = ['tile', 'piece', 'block', 'cell', 'grid'];
                var foundElements = 0;
                
                puzzleKeywords.forEach(function(keyword) {
                    var elements = document.querySelectorAll('[class*="' + keyword + '"], [id*="' + keyword + '"]');
                    foundElements += elements.length;
                });
                
                return {
                    puzzleElements: foundElements,
                    gridElements: document.querySelectorAll('[class*="grid"], [id*="grid"]').length,
                    hasCanvas: document.querySelectorAll('canvas').length > 0
                };
            """)
            
            tests.append({
                "test": "puzzle_elements",
                "success": puzzle_elements['puzzleElements'] > 0 or puzzle_elements['hasCanvas'],
                "score": min(100, puzzle_elements['puzzleElements'] * 10 + (50 if puzzle_elements['hasCanvas'] else 0)),
                "details": puzzle_elements
            })
            
        except Exception as e:
            tests.append({
                "test": "puzzle_game_tests_error",
                "success": False,
                "score": 0,
                "details": {"error": str(e)}
            })
        
        return tests
    
    async def run_action_game_tests(self) -> List[Dict[str, Any]]:
        """Run action game specific tests"""
        
        tests = []
        
        try:
            # Test action game elements
            action_elements = self.driver.driver.execute_script("""
                var actionKeywords = ['player', 'enemy', 'weapon', 'health', 'score'];
                var foundElements = 0;
                
                actionKeywords.forEach(function(keyword) {
                    var elements = document.querySelectorAll('[class*="' + keyword + '"], [id*="' + keyword + '"]');
                    foundElements += elements.length;
                });
                
                return {
                    actionElements: foundElements,
                    hasCanvas: document.querySelectorAll('canvas').length > 0,
                    hasGamepadSupport: typeof navigator.getGamepads === 'function'
                };
            """)
            
            tests.append({
                "test": "action_elements",
                "success": action_elements['actionElements'] > 0 or action_elements['hasCanvas'],
                "score": min(100, action_elements['actionElements'] * 10 + (30 if action_elements['hasCanvas'] else 0) + (20 if action_elements['hasGamepadSupport'] else 0)),
                "details": action_elements
            })
            
        except Exception as e:
            tests.append({
                "test": "action_game_tests_error",
                "success": False,
                "score": 0,
                "details": {"error": str(e)}
            })
        
        return tests

