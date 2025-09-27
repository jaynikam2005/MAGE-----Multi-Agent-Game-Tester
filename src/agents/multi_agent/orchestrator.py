"""
Advanced Multi-Agent Gaming Test Orchestrator
Enterprise-Grade AI-Powered Testing with Specialized Agents
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import structlog

from src.core.config import get_settings, TestingMode, GameGenre
from src.agents.specialized.planner_agent import PlannerAgent
from src.agents.specialized.ranker_agent import RankerAgent
from src.agents.specialized.executor_agent import ExecutorAgent
from src.agents.specialized.analyzer_agent import AnalyzerAgent
from src.agents.specialized.performance_agent import PerformanceAgent
from src.agents.specialized.security_agent import SecurityAgent
from src.agents.specialized.graphics_agent import GraphicsAgent
from src.agents.specialized.ai_behavior_agent import AIBehaviorAgent


class AgentStatus(str, Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class TestPhase(str, Enum):
    """Test execution phases"""
    PLANNING = "planning"
    RANKING = "ranking"
    EXECUTION = "execution"
    ANALYSIS = "analysis"
    REPORTING = "reporting"
    COMPLETE = "complete"


@dataclass
class AgentMetrics:
    """Agent performance metrics"""
    agent_id: str
    agent_type: str
    tasks_completed: int
    tasks_failed: int
    average_response_time: float
    cpu_usage: float
    memory_usage: float
    status: AgentStatus
    last_activity: float


@dataclass
class TestSession:
    """Comprehensive test session data"""
    session_id: str
    user_id: str
    target_url: str
    game_genre: GameGenre
    testing_modes: List[TestingMode]
    configuration: Dict[str, Any]
    phase: TestPhase
    start_time: float
    estimated_duration: int
    progress: float
    active_agents: List[str]
    completed_tests: int
    failed_tests: int
    total_tests: int


class AdvancedMultiAgentOrchestrator:
    """Enterprise multi-agent orchestrator for game testing"""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = structlog.get_logger(__name__)
        
        # Agent registry and management
        self.agents: Dict[str, Any] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.agent_pool = ThreadPoolExecutor(max_workers=self.settings.max_agents_per_session)
        
        # Session management
        self.active_sessions: Dict[str, TestSession] = {}
        self.session_queue: List[str] = []
        
        # Performance monitoring
        self.system_metrics = {
            "total_tests_run": 0,
            "success_rate": 0.0,
            "average_test_duration": 0.0,
            "peak_concurrent_agents": 0,
            "system_uptime": time.time()
        }
        
    async def initialize(self) -> None:
        """Initialize the multi-agent system"""
        try:
            await self._initialize_specialized_agents()
            await self._setup_agent_communication()
            await self._start_monitoring_tasks()
            
            self.logger.info("Advanced multi-agent orchestrator initialized", 
                           extra={"agent_count": len(self.agents)})
        except Exception as e:
            self.logger.error(f"Failed to initialize orchestrator: {e}")
            raise
    
    async def _initialize_specialized_agents(self) -> None:
        """Initialize all specialized testing agents"""
        agent_configs = [
            ("planner_001", PlannerAgent, self.settings.planner_agent_config),
            ("planner_002", PlannerAgent, self.settings.planner_agent_config),
            ("ranker_001", RankerAgent, {}),
            ("executor_001", ExecutorAgent, self.settings.executor_agent_config),
            ("executor_002", ExecutorAgent, self.settings.executor_agent_config),
            ("executor_003", ExecutorAgent, self.settings.executor_agent_config),
            ("analyzer_001", AnalyzerAgent, self.settings.analyzer_agent_config),
            ("performance_001", PerformanceAgent, {}),
            ("security_001", SecurityAgent, {}),
            ("graphics_001", GraphicsAgent, {}),
            ("ai_behavior_001", AIBehaviorAgent, {})
        ]
        
        for agent_id, agent_class, config in agent_configs:
            try:
                agent = agent_class(agent_id, config)
                await agent.initialize()
                
                self.agents[agent_id] = agent
                self.agent_metrics[agent_id] = AgentMetrics(
                    agent_id=agent_id,
                    agent_type=agent_class.__name__,
                    tasks_completed=0,
                    tasks_failed=0,
                    average_response_time=0.0,
                    cpu_usage=0.0,
                    memory_usage=0.0,
                    status=AgentStatus.IDLE,
                    last_activity=time.time()
                )
                
                self.logger.info(f"Initialized agent: {agent_id}")
                
            except Exception as e:
                self.logger.error(f"Failed to initialize agent {agent_id}: {e}")
    
    async def _setup_agent_communication(self) -> None:
        """Setup inter-agent communication channels"""
        # Implementation for agent-to-agent messaging
        pass
    
    async def _start_monitoring_tasks(self) -> None:
        """Start background monitoring tasks"""
        asyncio.create_task(self._monitor_agent_health())
        asyncio.create_task(self._manage_session_queue())
        asyncio.create_task(self._collect_system_metrics())
    
    async def create_test_session(self, user_id: str, config: Dict[str, Any]) -> str:
        """Create a new comprehensive test session"""
        import uuid
        
        session_id = str(uuid.uuid4())
        
        # Validate configuration
        if not self._validate_test_config(config):
            raise ValueError("Invalid test configuration")
        
        # Estimate test duration based on configuration
        estimated_duration = self._estimate_test_duration(config)
        
        # Create session object
        session = TestSession(
            session_id=session_id,
            user_id=user_id,
            target_url=config["target_url"],
            game_genre=GameGenre(config.get("game_genre", "puzzle")),
            testing_modes=[TestingMode(mode) for mode in config.get("testing_modes", ["performance"])],
            configuration=config,
            phase=TestPhase.PLANNING,
            start_time=time.time(),
            estimated_duration=estimated_duration,
            progress=0.0,
            active_agents=[],
            completed_tests=0,
            failed_tests=0,
            total_tests=config.get("test_count", 20)
        )
        
        self.active_sessions[session_id] = session
        self.session_queue.append(session_id)
        
        self.logger.info(f"Created test session", extra={
            "session_id": session_id,
            "user_id": user_id,
            "estimated_duration": estimated_duration
        })
        
        return session_id
    
    async def execute_test_session(self, session_id: str) -> Dict[str, Any]:
        """Execute a comprehensive test session"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        
        try:
            # Phase 1: Planning
            session.phase = TestPhase.PLANNING
            test_plan = await self._execute_planning_phase(session)
            
            # Phase 2: Ranking and Selection
            session.phase = TestPhase.RANKING
            selected_tests = await self._execute_ranking_phase(session, test_plan)
            
            # Phase 3: Execution
            session.phase = TestPhase.EXECUTION
            test_results = await self._execute_testing_phase(session, selected_tests)
            
            # Phase 4: Analysis
            session.phase = TestPhase.ANALYSIS
            analysis_results = await self._execute_analysis_phase(session, test_results)
            
            # Phase 5: Reporting
            session.phase = TestPhase.REPORTING
            final_report = await self._generate_comprehensive_report(session, analysis_results)
            
            session.phase = TestPhase.COMPLETE
            session.progress = 100.0
            
            self.logger.info(f"Test session completed successfully", extra={
                "session_id": session_id,
                "total_tests": session.total_tests,
                "completed_tests": session.completed_tests,
                "success_rate": (session.completed_tests - session.failed_tests) / session.completed_tests if session.completed_tests > 0 else 0
            })
            
            return final_report
            
        except Exception as e:
            self.logger.error(f"Test session failed: {e}", extra={"session_id": session_id})
            session.phase = TestPhase.COMPLETE  # Mark as complete even if failed
            raise
    
    async def _execute_planning_phase(self, session: TestSession) -> Dict[str, Any]:
        """Execute test planning phase with multiple planner agents"""
        planner_agents = [agent for agent_id, agent in self.agents.items() 
                         if isinstance(agent, PlannerAgent)]
        
        if not planner_agents:
            raise RuntimeError("No planner agents available")
        
        # Run multiple planners in parallel for diverse perspectives
        planning_tasks = []
        for planner in planner_agents[:2]:  # Use top 2 planners
            task = asyncio.create_task(planner.generate_test_plan({
                "target_url": session.target_url,
                "game_genre": session.game_genre.value,
                "testing_modes": [mode.value for mode in session.testing_modes],
                "test_count": session.total_tests
            }))
            planning_tasks.append(task)
        
        # Collect planning results
        planning_results = await asyncio.gather(*planning_tasks, return_exceptions=True)
        
        # Merge and optimize plans
        merged_plan = self._merge_test_plans(planning_results)
        
        session.progress = 20.0  # 20% complete after planning
        
        return merged_plan
    
    async def _execute_ranking_phase(self, session: TestSession, test_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank and select the best test cases"""
        ranker_agents = [agent for agent_id, agent in self.agents.items() 
                        if isinstance(agent, RankerAgent)]
        
        if not ranker_agents:
            raise RuntimeError("No ranker agents available")
        
        ranker = ranker_agents[0]
        ranked_tests = await ranker.rank_test_cases(test_plan["test_cases"])
        
        # Select top tests based on configuration
        selected_count = min(session.total_tests, len(ranked_tests))
        selected_tests = ranked_tests[:selected_count]
        
        session.progress = 30.0  # 30% complete after ranking
        
        return selected_tests
    
    async def _execute_testing_phase(self, session: TestSession, selected_tests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute selected test cases with specialized agents"""
        executor_agents = [agent for agent_id, agent in self.agents.items() 
                          if isinstance(agent, ExecutorAgent)]
        
        if not executor_agents:
            raise RuntimeError("No executor agents available")
        
        # Distribute tests across available executor agents
        test_batches = self._distribute_tests(selected_tests, len(executor_agents))
        
        execution_tasks = []
        for i, (agent, batch) in enumerate(zip(executor_agents, test_batches)):
            task = asyncio.create_task(self._execute_test_batch(agent, batch, session))
            execution_tasks.append(task)
        
        # Wait for all execution tasks to complete
        batch_results = await asyncio.gather(*execution_tasks, return_exceptions=True)
        
        # Flatten results
        all_results = []
        for batch_result in batch_results:
            if isinstance(batch_result, list):
                all_results.extend(batch_result)
        
        session.progress = 80.0  # 80% complete after execution
        
        return all_results
    
    async def _execute_analysis_phase(self, session: TestSession, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze test results with specialized analysis agents"""
        analyzer_agents = [agent for agent_id, agent in self.agents.items() 
                          if isinstance(agent, AnalyzerAgent)]
        
        if not analyzer_agents:
            raise RuntimeError("No analyzer agents available")
        
        analyzer = analyzer_agents[0]
        analysis_results = await analyzer.analyze_results(test_results)
        
        # Run specialized analysis based on testing modes
        specialized_analyses = {}
        
        for mode in session.testing_modes:
            if mode == TestingMode.PERFORMANCE:
                perf_agents = [agent for agent_id, agent in self.agents.items() 
                              if isinstance(agent, PerformanceAgent)]
                if perf_agents:
                    specialized_analyses["performance"] = await perf_agents[0].analyze_performance(test_results)
            
            elif mode == TestingMode.SECURITY:
                sec_agents = [agent for agent_id, agent in self.agents.items() 
                             if isinstance(agent, SecurityAgent)]
                if sec_agents:
                    specialized_analyses["security"] = await sec_agents[0].analyze_security(test_results)
            
            elif mode == TestingMode.GRAPHICS:
                gfx_agents = [agent for agent_id, agent in self.agents.items() 
                             if isinstance(agent, GraphicsAgent)]
                if gfx_agents:
                    specialized_analyses["graphics"] = await gfx_agents[0].analyze_graphics(test_results)
        
        analysis_results["specialized_analyses"] = specialized_analyses
        
        session.progress = 95.0  # 95% complete after analysis
        
        return analysis_results
    
    async def _generate_comprehensive_report(self, session: TestSession, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final comprehensive test report"""
        end_time = time.time()
        duration = end_time - session.start_time
        
        report = {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "target_url": session.target_url,
            "game_genre": session.game_genre.value,
            "testing_modes": [mode.value for mode in session.testing_modes],
            "execution_summary": {
                "start_time": session.start_time,
                "end_time": end_time,
                "duration_seconds": duration,
                "total_tests": session.total_tests,
                "completed_tests": session.completed_tests,
                "failed_tests": session.failed_tests,
                "success_rate": (session.completed_tests - session.failed_tests) / session.completed_tests if session.completed_tests > 0 else 0
            },
            "analysis_results": analysis_results,
            "agent_metrics": dict(self.agent_metrics),
            "recommendations": self._generate_recommendations(analysis_results),
            "generated_at": time.time()
        }
        
        session.progress = 100.0  # Complete
        
        return report
    
    def _validate_test_config(self, config: Dict[str, Any]) -> bool:
        """Validate test configuration"""
        required_fields = ["target_url", "test_count"]
        return all(field in config for field in required_fields)
    
    def _estimate_test_duration(self, config: Dict[str, Any]) -> int:
        """Estimate test duration in seconds"""
        base_time = 60  # 1 minute base
        test_count = config.get("test_count", 20)
        
        # Add time based on test count
        estimated = base_time + (test_count * 30)  # 30 seconds per test
        
        # Add time for specialized testing modes
        testing_modes = config.get("testing_modes", [])
        if "performance" in testing_modes:
            estimated += 300  # 5 minutes for performance analysis
        if "security" in testing_modes:
            estimated += 600  # 10 minutes for security testing
        
        return estimated
    
    def _merge_test_plans(self, planning_results: List[Any]) -> Dict[str, Any]:
        """Merge multiple test plans into one optimized plan"""
        merged_plan = {
            "test_cases": [],
            "coverage_areas": set(),
            "priority_tests": []
        }
        
        for result in planning_results:
            if isinstance(result, dict) and "test_cases" in result:
                merged_plan["test_cases"].extend(result["test_cases"])
                merged_plan["coverage_areas"].update(result.get("coverage_areas", []))
        
        # Remove duplicates and optimize
        seen_tests = set()
        unique_tests = []
        for test in merged_plan["test_cases"]:
            test_signature = f"{test.get('name', '')}:{test.get('type', '')}"
            if test_signature not in seen_tests:
                seen_tests.add(test_signature)
                unique_tests.append(test)
        
        merged_plan["test_cases"] = unique_tests
        merged_plan["coverage_areas"] = list(merged_plan["coverage_areas"])
        
        return merged_plan
    
    def _distribute_tests(self, tests: List[Dict[str, Any]], agent_count: int) -> List[List[Dict[str, Any]]]:
        """Distribute tests evenly across available agents"""
        if agent_count == 0:
            return []
        
        batches = [[] for _ in range(agent_count)]
        for i, test in enumerate(tests):
            batch_index = i % agent_count
            batches[batch_index].append(test)
        
        return batches
    
    async def _execute_test_batch(self, agent: Any, tests: List[Dict[str, Any]], session: TestSession) -> List[Dict[str, Any]]:
        """Execute a batch of tests with a specific agent"""
        results = []
        
        for test in tests:
            try:
                start_time = time.time()
                result = await agent.execute_test(test)
                end_time = time.time()
                
                result["execution_time"] = end_time - start_time
                result["agent_id"] = agent.agent_id
                results.append(result)
                
                session.completed_tests += 1
                
                # Update progress
                progress_increment = 50.0 / session.total_tests  # 50% of total progress for execution
                session.progress += progress_increment
                
            except Exception as e:
                self.logger.error(f"Test execution failed: {e}", extra={"test": test})
                session.failed_tests += 1
                results.append({
                    "test_id": test.get("id", "unknown"),
                    "status": "failed",
                    "error": str(e),
                    "agent_id": agent.agent_id
                })
        
        return results
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Performance recommendations
        if "performance" in analysis_results.get("specialized_analyses", {}):
            perf_data = analysis_results["specialized_analyses"]["performance"]
            if perf_data.get("average_response_time", 0) > 2000:
                recommendations.append("Consider optimizing server response times")
            if perf_data.get("memory_usage", 0) > 0.8:
                recommendations.append("Memory usage is high - investigate potential memory leaks")
        
        # Security recommendations
        if "security" in analysis_results.get("specialized_analyses", {}):
            sec_data = analysis_results["specialized_analyses"]["security"]
            if sec_data.get("vulnerabilities_found", 0) > 0:
                recommendations.append("Security vulnerabilities detected - prioritize fixes")
        
        # General recommendations
        success_rate = analysis_results.get("success_rate", 1.0)
        if success_rate < 0.9:
            recommendations.append("Test success rate is below 90% - investigate failing test cases")
        
        return recommendations
    
    async def _monitor_agent_health(self) -> None:
        """Monitor agent health and performance"""
        while True:
            try:
                for agent_id, agent in self.agents.items():
                    if hasattr(agent, 'get_health_metrics'):
                        metrics = await agent.get_health_metrics()
                        self.agent_metrics[agent_id].cpu_usage = metrics.get("cpu_usage", 0.0)
                        self.agent_metrics[agent_id].memory_usage = metrics.get("memory_usage", 0.0)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Agent health monitoring failed: {e}")
                await asyncio.sleep(60)
    
    async def _manage_session_queue(self) -> None:
        """Manage test session execution queue"""
        while True:
            try:
                if self.session_queue:
                    session_id = self.session_queue.pop(0)
                    if session_id in self.active_sessions:
                        asyncio.create_task(self.execute_test_session(session_id))
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Session queue management failed: {e}")
                await asyncio.sleep(30)
    
    async def _collect_system_metrics(self) -> None:
        """Collect system-wide performance metrics"""
        while True:
            try:
                self.system_metrics["peak_concurrent_agents"] = max(
                    self.system_metrics["peak_concurrent_agents"],
                    len([agent for agent in self.agent_metrics.values() if agent.status == AgentStatus.BUSY])
                )
                
                await asyncio.sleep(60)  # Collect every minute
                
            except Exception as e:
                self.logger.error(f"Metrics collection failed: {e}")
                await asyncio.sleep(300)
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get current orchestrator status and metrics"""
        return {
            "agents": {
                "total": len(self.agents),
                "active": len([a for a in self.agent_metrics.values() if a.status == AgentStatus.BUSY]),
                "idle": len([a for a in self.agent_metrics.values() if a.status == AgentStatus.IDLE]),
                "error": len([a for a in self.agent_metrics.values() if a.status == AgentStatus.ERROR])
            },
            "sessions": {
                "active": len(self.active_sessions),
                "queued": len(self.session_queue)
            },
            "system_metrics": self.system_metrics,
            "agent_metrics": dict(self.agent_metrics)
        }
