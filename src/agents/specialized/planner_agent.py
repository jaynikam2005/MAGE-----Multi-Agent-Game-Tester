"""
Advanced AI Planner Agent
Game Testing Strategy & Test Case Generation
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import structlog

from src.core.config import get_settings, GameGenre, TestingMode


@dataclass
class TestCase:
    """Advanced test case structure"""
    id: str
    name: str
    category: str
    priority: int
    complexity: str
    estimated_duration: int
    prerequisites: List[str]
    expected_outcome: Dict[str, Any]
    automation_level: float
    game_specific: Dict[str, Any]


class PlannerAgent:
    """AI-powered test planning agent with game expertise"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.settings = get_settings()
        self.logger = structlog.get_logger(__name__)
        
        # Game testing knowledge base
        self.game_patterns = {
            GameGenre.ACTION: {
                "key_mechanics": ["movement", "combat", "collision", "physics"],
                "performance_critical": ["frame_rate", "input_lag", "physics_stability"],
                "common_issues": ["clipping", "animation_bugs", "hitbox_problems"]
            },
            GameGenre.RPG: {
                "key_mechanics": ["character_progression", "inventory", "dialogue", "quests"],
                "performance_critical": ["save_load_times", "world_streaming", "ui_responsiveness"],
                "common_issues": ["progression_blocks", "dialogue_errors", "balance_issues"]
            },
            GameGenre.PUZZLE: {
                "key_mechanics": ["logic_validation", "hint_system", "level_progression"],
                "performance_critical": ["ui_smoothness", "calculation_speed"],
                "common_issues": ["unsolvable_puzzles", "hint_accuracy", "difficulty_spikes"]
            }
        }
        
    async def initialize(self) -> None:
        """Initialize the planner agent"""
        self.logger.info(f"Planner agent {self.agent_id} initialized")
    
    async def generate_test_plan(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive test plan using AI reasoning"""
        try:
            target_url = requirements["target_url"]
            game_genre = GameGenre(requirements.get("game_genre", "puzzle"))
            testing_modes = [TestingMode(mode) for mode in requirements.get("testing_modes", ["performance"])]
            test_count = requirements.get("test_count", 20)
            
            # Analyze target game
            game_analysis = await self._analyze_target_game(target_url, game_genre)
            
            # Generate test cases based on analysis
            test_cases = await self._generate_intelligent_test_cases(
                game_analysis, testing_modes, test_count
            )
            
            # Create execution strategy
            execution_strategy = await self._create_execution_strategy(test_cases, testing_modes)
            
            plan = {
                "planner_id": self.agent_id,
                "target_analysis": game_analysis,
                "test_cases": [tc.__dict__ for tc in test_cases],
                "execution_strategy": execution_strategy,
                "coverage_areas": self._calculate_coverage_areas(test_cases),
                "estimated_duration": sum(tc.estimated_duration for tc in test_cases),
                "risk_assessment": await self._assess_testing_risks(game_analysis, test_cases),
                "recommendations": await self._generate_testing_recommendations(game_analysis)
            }
            
            self.logger.info(f"Generated test plan with {len(test_cases)} test cases")
            return plan
            
        except Exception as e:
            self.logger.error(f"Test plan generation failed: {e}")
            raise
    
    async def _analyze_target_game(self, url: str, genre: GameGenre) -> Dict[str, Any]:
        """Analyze target game using AI and predefined patterns"""
        
        # Simulate AI analysis (would use actual AI/ML models in production)
        analysis = {
            "url": url,
            "detected_genre": genre.value,
            "technology_stack": await self._detect_technology_stack(url),
            "complexity_score": await self._calculate_complexity_score(url, genre),
            "performance_characteristics": await self._analyze_performance_profile(url),
            "ui_elements": await self._identify_ui_components(url),
            "game_mechanics": self.game_patterns.get(genre, {}).get("key_mechanics", []),
            "potential_risks": await self._identify_potential_risks(url, genre)
        }
        
        return analysis
    
    async def _detect_technology_stack(self, url: str) -> Dict[str, Any]:
        """Detect game's technology stack"""
        # Simulate technology detection
        return {
            "engine": "Unity",  # Could be Unity, Unreal, Custom, etc.
            "rendering": "WebGL",
            "framework": "JavaScript",
            "mobile_optimized": True,
            "web_technologies": ["HTML5", "Canvas", "WebGL"]
        }
    
    async def _calculate_complexity_score(self, url: str, genre: GameGenre) -> float:
        """Calculate game complexity score (0.0 - 1.0)"""
        base_complexity = {
            GameGenre.PUZZLE: 0.3,
            GameGenre.ACTION: 0.7,
            GameGenre.RPG: 0.8,
            GameGenre.STRATEGY: 0.9,
            GameGenre.SIMULATION: 0.8
        }
        
        return base_complexity.get(genre, 0.5)
    
    async def _analyze_performance_profile(self, url: str) -> Dict[str, Any]:
        """Analyze expected performance characteristics"""
        return {
            "cpu_intensity": "medium",
            "memory_requirements": "low",
            "network_dependency": "low",
            "gpu_requirements": "medium",
            "expected_bottlenecks": ["DOM manipulation", "canvas rendering"]
        }
    
    async def _identify_ui_components(self, url: str) -> List[str]:
        """Identify UI components for testing"""
        return [
            "game_board", "score_display", "menu_system", 
            "settings_panel", "help_dialog", "touch_controls"
        ]
    
    async def _identify_potential_risks(self, url: str, genre: GameGenre) -> List[Dict[str, Any]]:
        """Identify potential testing risks"""
        common_risks = [
            {
                "risk": "Memory leaks in long sessions",
                "probability": "medium",
                "impact": "high",
                "mitigation": "Extended play testing"
            },
            {
                "risk": "Cross-browser compatibility",
                "probability": "high",
                "impact": "medium",
                "mitigation": "Multi-browser test suite"
            }
        ]
        
        genre_specific_risks = {
            GameGenre.PUZZLE: [
                {
                    "risk": "Unsolvable puzzle states",
                    "probability": "low",
                    "impact": "critical",
                    "mitigation": "Logic validation testing"
                }
            ],
            GameGenre.ACTION: [
                {
                    "risk": "Input lag affecting gameplay",
                    "probability": "medium",
                    "impact": "high",
                    "mitigation": "Input latency testing"
                }
            ]
        }
        
        return common_risks + genre_specific_risks.get(genre, [])
    
    async def _generate_intelligent_test_cases(self, analysis: Dict[str, Any], 
                                             modes: List[TestingMode], 
                                             count: int) -> List[TestCase]:
        """Generate intelligent test cases based on analysis"""
        
        test_cases = []
        test_id_counter = 1
        
        # Core functionality tests (always include)
        core_tests = await self._generate_core_functionality_tests(analysis)
        test_cases.extend(core_tests)
        
        # Mode-specific tests
        for mode in modes:
            if mode == TestingMode.PERFORMANCE:
                perf_tests = await self._generate_performance_tests(analysis)
                test_cases.extend(perf_tests)
            elif mode == TestingMode.AI_BEHAVIOR:
                ai_tests = await self._generate_ai_behavior_tests(analysis)
                test_cases.extend(ai_tests)
            elif mode == TestingMode.GRAPHICS:
                gfx_tests = await self._generate_graphics_tests(analysis)
                test_cases.extend(gfx_tests)
            elif mode == TestingMode.SECURITY:
                sec_tests = await self._generate_security_tests(analysis)
                test_cases.extend(sec_tests)
        
        # Assign IDs and limit to requested count
        for i, tc in enumerate(test_cases[:count], 1):
            tc.id = f"TC_{i:03d}"
        
        return test_cases[:count]
    
    async def _generate_core_functionality_tests(self, analysis: Dict[str, Any]) -> List[TestCase]:
        """Generate core functionality test cases"""
        tests = []
        
        # Game loading test
        tests.append(TestCase(
            id="",
            name="Game Loading and Initialization",
            category="core",
            priority=1,
            complexity="low",
            estimated_duration=30,
            prerequisites=[],
            expected_outcome={"game_loads": True, "ui_visible": True},
            automation_level=0.9,
            game_specific={"engine": analysis["technology_stack"]["engine"]}
        ))
        
        # Basic interaction test
        tests.append(TestCase(
            id="",
            name="Basic User Interaction",
            category="core",
            priority=1,
            complexity="medium",
            estimated_duration=45,
            prerequisites=["TC_001"],
            expected_outcome={"interactions_respond": True, "feedback_provided": True},
            automation_level=0.8,
            game_specific={"ui_elements": analysis["ui_elements"]}
        ))
        
        # Navigation test
        tests.append(TestCase(
            id="",
            name="Menu Navigation and Settings",
            category="core",
            priority=2,
            complexity="low",
            estimated_duration=30,
            prerequisites=["TC_001"],
            expected_outcome={"menus_accessible": True, "settings_persist": True},
            automation_level=0.9,
            game_specific={}
        ))
        
        return tests
    
    async def _generate_performance_tests(self, analysis: Dict[str, Any]) -> List[TestCase]:
        """Generate performance-focused test cases"""
        tests = []
        
        tests.append(TestCase(
            id="",
            name="Frame Rate Stability Test",
            category="performance",
            priority=1,
            complexity="medium",
            estimated_duration=120,
            prerequisites=["TC_001"],
            expected_outcome={"min_fps": 30, "avg_fps": 60, "frame_drops": "<5%"},
            automation_level=0.7,
            game_specific={"target_fps": 60}
        ))
        
        tests.append(TestCase(
            id="",
            name="Memory Usage Monitoring",
            category="performance",
            priority=1,
            complexity="medium",
            estimated_duration=300,
            prerequisites=["TC_001"],
            expected_outcome={"memory_stable": True, "no_leaks": True},
            automation_level=0.8,
            game_specific={"max_memory_mb": 512}
        ))
        
        return tests
    
    async def _generate_ai_behavior_tests(self, analysis: Dict[str, Any]) -> List[TestCase]:
        """Generate AI behavior test cases"""
        tests = []
        
        if "AI" in analysis.get("game_mechanics", []):
            tests.append(TestCase(
                id="",
                name="AI Decision Making Validation",
                category="ai_behavior",
                priority=2,
                complexity="high",
                estimated_duration=180,
                prerequisites=["TC_001", "TC_002"],
                expected_outcome={"ai_responds": True, "decisions_logical": True},
                automation_level=0.6,
                game_specific={"ai_complexity": "medium"}
            ))
        
        return tests
    
    async def _generate_graphics_tests(self, analysis: Dict[str, Any]) -> List[TestCase]:
        """Generate graphics and visual test cases"""
        tests = []
        
        tests.append(TestCase(
            id="",
            name="Visual Rendering Validation",
            category="graphics",
            priority=2,
            complexity="medium",
            estimated_duration=60,
            prerequisites=["TC_001"],
            expected_outcome={"graphics_render": True, "no_artifacts": True},
            automation_level=0.7,
            game_specific={"rendering_engine": analysis["technology_stack"]["rendering"]}
        ))
        
        return tests
    
    async def _generate_security_tests(self, analysis: Dict[str, Any]) -> List[TestCase]:
        """Generate security test cases"""
        tests = []
        
        tests.append(TestCase(
            id="",
            name="Input Validation Security Test",
            category="security",
            priority=1,
            complexity="high",
            estimated_duration=90,
            prerequisites=["TC_001"],
            expected_outcome={"no_xss": True, "input_sanitized": True},
            automation_level=0.8,
            game_specific={"input_vectors": ["text_fields", "url_params"]}
        ))
        
        return tests
    
    async def _create_execution_strategy(self, test_cases: List[TestCase], 
                                       modes: List[TestingMode]) -> Dict[str, Any]:
        """Create intelligent test execution strategy"""
        
        # Group tests by dependency and priority
        execution_phases = []
        
        # Phase 1: Core tests (no dependencies)
        phase_1 = [tc for tc in test_cases if not tc.prerequisites and tc.category == "core"]
        if phase_1:
            execution_phases.append({
                "phase": 1,
                "name": "Core Functionality",
                "tests": [tc.id for tc in phase_1],
                "parallel_execution": True,
                "estimated_duration": max(tc.estimated_duration for tc in phase_1)
            })
        
        # Phase 2: Basic feature tests
        phase_2 = [tc for tc in test_cases if tc.prerequisites and tc.priority <= 2]
        if phase_2:
            execution_phases.append({
                "phase": 2,
                "name": "Feature Validation",
                "tests": [tc.id for tc in phase_2],
                "parallel_execution": True,
                "estimated_duration": sum(tc.estimated_duration for tc in phase_2) // 3
            })
        
        # Phase 3: Advanced and specialized tests
        phase_3 = [tc for tc in test_cases if tc.priority > 2 or tc.complexity == "high"]
        if phase_3:
            execution_phases.append({
                "phase": 3,
                "name": "Advanced Testing",
                "tests": [tc.id for tc in phase_3],
                "parallel_execution": False,
                "estimated_duration": sum(tc.estimated_duration for tc in phase_3)
            })
        
        return {
            "execution_phases": execution_phases,
            "total_phases": len(execution_phases),
            "parallel_strategy": "adaptive",
            "fallback_strategy": "sequential",
            "retry_policy": {"max_retries": 3, "backoff_factor": 1.5}
        }
    
    def _calculate_coverage_areas(self, test_cases: List[TestCase]) -> List[str]:
        """Calculate test coverage areas"""
        coverage_areas = set()
        
        for tc in test_cases:
            coverage_areas.add(tc.category)
            if tc.game_specific:
                coverage_areas.update(tc.game_specific.keys())
        
        return list(coverage_areas)
    
    async def _assess_testing_risks(self, analysis: Dict[str, Any], 
                                  test_cases: List[TestCase]) -> Dict[str, Any]:
        """Assess risks in the testing plan"""
        
        risk_factors = []
        
        # Check test coverage
        categories = set(tc.category for tc in test_cases)
        if len(categories) < 3:
            risk_factors.append({
                "type": "coverage",
                "description": "Limited test coverage areas",
                "severity": "medium"
            })
        
        # Check for high complexity tests
        high_complexity_count = len([tc for tc in test_cases if tc.complexity == "high"])
        if high_complexity_count > len(test_cases) * 0.3:
            risk_factors.append({
                "type": "complexity",
                "description": "High proportion of complex tests",
                "severity": "low"
            })
        
        return {
            "overall_risk": "low" if len(risk_factors) <= 1 else "medium",
            "risk_factors": risk_factors,
            "mitigation_suggestions": [
                "Add more automated test cases",
                "Include smoke tests for quick validation",
                "Consider parallel execution for time optimization"
            ]
        }
    
    async def _generate_testing_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate testing recommendations based on analysis"""
        recommendations = []
        
        complexity = analysis.get("complexity_score", 0.5)
        if complexity > 0.7:
            recommendations.append("Consider extended testing duration due to game complexity")
        
        tech_stack = analysis.get("technology_stack", {})
        if tech_stack.get("engine") == "Unity":
            recommendations.append("Include Unity-specific performance profiling")
        
        if tech_stack.get("mobile_optimized"):
            recommendations.append("Add mobile device testing scenarios")
        
        return recommendations
    
    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get agent health metrics"""
        return {
            "agent_id": self.agent_id,
            "status": "healthy",
            "cpu_usage": 0.15,
            "memory_usage": 0.25,
            "last_activity": "planning",
            "total_plans_generated": 10  # Would track actual metrics
        }
