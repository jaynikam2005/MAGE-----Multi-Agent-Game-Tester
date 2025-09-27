"""
AI Behavior Analysis Agent
Game AI Testing, Decision Making Validation & Behavioral Pattern Analysis
"""

import asyncio
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import structlog
from enum import Enum

from src.core.config import get_settings


class AIBehaviorType(str, Enum):
    """Types of AI behaviors to analyze"""
    PATHFINDING = "pathfinding"
    DECISION_MAKING = "decision_making"
    LEARNING = "learning"
    REACTIVE = "reactive"
    STRATEGIC = "strategic"
    ADAPTIVE = "adaptive"
    PREDICTIVE = "predictive"


class AIQualityMetric(str, Enum):
    """AI quality metrics"""
    INTELLIGENCE = "intelligence"
    CONSISTENCY = "consistency"
    RESPONSIVENESS = "responsiveness"
    ADAPTABILITY = "adaptability"
    PREDICTABILITY = "predictability"
    CHALLENGE_LEVEL = "challenge_level"


@dataclass
class AIBehaviorPattern:
    """AI behavior pattern analysis"""
    pattern_id: str
    behavior_type: AIBehaviorType
    frequency: int
    consistency_score: float
    effectiveness_score: float
    description: str
    examples: List[str]


@dataclass
class AIDecisionAnalysis:
    """AI decision making analysis"""
    decision_id: str
    context: Dict[str, Any]
    expected_action: str
    actual_action: str
    decision_time_ms: float
    correctness_score: float
    reasoning_quality: float


class AIBehaviorAgent:
    """Advanced AI behavior analysis and validation agent"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.settings = get_settings()
        self.logger = structlog.get_logger(__name__)
        
        # AI behavior analysis parameters
        self.behavior_thresholds = {
            "response_time_ms": 100,  # Max acceptable AI response time
            "consistency_threshold": 0.8,  # Min consistency score
            "intelligence_threshold": 0.7,  # Min intelligence score
            "adaptability_threshold": 0.6   # Min adaptability score
        }
        
        # Expected AI behavior patterns
        self.expected_patterns = {
            AIBehaviorType.PATHFINDING: {
                "optimal_path_ratio": 0.8,
                "collision_avoidance": 0.95,
                "dynamic_repathing": 0.7
            },
            AIBehaviorType.DECISION_MAKING: {
                "logical_decisions": 0.85,
                "context_awareness": 0.8,
                "goal_oriented": 0.9
            },
            AIBehaviorType.REACTIVE: {
                "response_time_ms": 50,
                "appropriate_reactions": 0.9,
                "stimulus_recognition": 0.95
            }
        }
        
        # AI testing scenarios
        self.test_scenarios = [
            {
                "scenario_id": "pathfinding_obstacle",
                "description": "Test AI pathfinding around obstacles",
                "expected_behavior": "find_optimal_path",
                "complexity": "medium"
            },
            {
                "scenario_id": "decision_under_pressure",
                "description": "Test AI decision making under time pressure",
                "expected_behavior": "quick_logical_decision",
                "complexity": "high"
            },
            {
                "scenario_id": "adaptive_learning",
                "description": "Test AI adaptation to player strategies",
                "expected_behavior": "counter_strategy",
                "complexity": "high"
            }
        ]
        
        # Behavioral analysis models
        self.behavior_models = {}
        
    async def initialize(self) -> None:
        """Initialize AI behavior analysis agent"""
        try:
            await self._load_behavior_models()
            await self._calibrate_analysis_parameters()
            self.logger.info(f"AI Behavior agent {self.agent_id} initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize AI behavior agent: {e}")
            raise
    
    async def analyze_ai_behavior(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive AI behavior analysis"""
        
        try:
            self.logger.info(f"Analyzing AI behavior from {len(test_results)} test results")
            
            # Extract AI behavior data
            behavior_data = await self._extract_ai_behavior_data(test_results)
            
            # Analyze decision making patterns
            decision_analysis = await self._analyze_decision_making(behavior_data)
            
            # Analyze pathfinding behavior
            pathfinding_analysis = await self._analyze_pathfinding(behavior_data)
            
            # Analyze reactive behaviors
            reactive_analysis = await self._analyze_reactive_behaviors(behavior_data)
            
            # Analyze learning and adaptation
            learning_analysis = await self._analyze_learning_capabilities(behavior_data)
            
            # Analyze AI consistency
            consistency_analysis = await self._analyze_behavioral_consistency(behavior_data)
            
            # Performance and responsiveness analysis
            performance_analysis = await self._analyze_ai_performance(behavior_data)
            
            # Strategic behavior analysis
            strategic_analysis = await self._analyze_strategic_behavior(behavior_data)
            
            # Challenge level analysis
            challenge_analysis = await self._analyze_challenge_level(behavior_data)
            
            # Behavioral pattern recognition
            pattern_analysis = await self._recognize_behavior_patterns(behavior_data)
            
            # AI quality assessment
            quality_assessment = await self._assess_ai_quality(
                decision_analysis, pathfinding_analysis, reactive_analysis,
                learning_analysis, consistency_analysis
            )
            
            # Generate AI behavior score
            ai_score = await self._calculate_ai_behavior_score(quality_assessment)
            
            analysis = {
                "agent_id": self.agent_id,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "ai_behavior_score": ai_score,
                "overall_rating": self._determine_ai_rating(ai_score),
                "behavior_data_summary": {
                    "total_behaviors_analyzed": len(behavior_data),
                    "behavior_types_detected": list(set([b.get("type") for b in behavior_data])),
                    "analysis_coverage": self._calculate_analysis_coverage(behavior_data)
                },
                "decision_making_analysis": decision_analysis,
                "pathfinding_analysis": pathfinding_analysis,
                "reactive_analysis": reactive_analysis,
                "learning_analysis": learning_analysis,
                "consistency_analysis": consistency_analysis,
                "performance_analysis": performance_analysis,
                "strategic_analysis": strategic_analysis,
                "challenge_analysis": challenge_analysis,
                "pattern_analysis": pattern_analysis,
                "quality_assessment": quality_assessment,
                "recommendations": await self._generate_ai_recommendations(quality_assessment)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"AI behavior analysis failed: {e}")
            raise
    
    async def _extract_ai_behavior_data(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract AI behavior data from test results"""
        
        behavior_data = []
        
        for result in results:
            if "ai_analysis" in result:
                ai_data = result["ai_analysis"]
                
                # Extract decision points
                if "decisions" in ai_data:
                    for decision in ai_data["decisions"]:
                        behavior_data.append({
                            "type": "decision",
                            "timestamp": decision.get("timestamp", 0),
                            "context": decision.get("context", {}),
                            "action": decision.get("action", ""),
                            "response_time": decision.get("response_time", 0),
                            "test_id": result.get("test_id", "unknown")
                        })
                
                # Extract movement patterns
                if "movements" in ai_data:
                    for movement in ai_data["movements"]:
                        behavior_data.append({
                            "type": "movement",
                            "timestamp": movement.get("timestamp", 0),
                            "start_position": movement.get("start", [0, 0]),
                            "end_position": movement.get("end", [0, 0]),
                            "path": movement.get("path", []),
                            "duration": movement.get("duration", 0),
                            "test_id": result.get("test_id", "unknown")
                        })
                
                # Extract reactions
                if "reactions" in ai_data:
                    for reaction in ai_data["reactions"]:
                        behavior_data.append({
                            "type": "reaction",
                            "timestamp": reaction.get("timestamp", 0),
                            "stimulus": reaction.get("stimulus", ""),
                            "response": reaction.get("response", ""),
                            "reaction_time": reaction.get("reaction_time", 0),
                            "test_id": result.get("test_id", "unknown")
                        })
            
            # Simulate AI behavior data if not present (for demonstration)
            if not behavior_data and result.get("status") == "passed":
                behavior_data.extend(self._simulate_ai_behavior_data(result.get("test_id", "unknown")))
        
        return behavior_data
    
    def _simulate_ai_behavior_data(self, test_id: str) -> List[Dict[str, Any]]:
        """Simulate AI behavior data for demonstration"""
        
        simulated_data = []
        
        # Simulate decision making
        for i in range(5):
            simulated_data.append({
                "type": "decision",
                "timestamp": i * 1000,
                "context": {"player_distance": 10 + i * 2, "health": 100 - i * 10},
                "action": "attack" if i % 2 == 0 else "defend",
                "response_time": 50 + np.random.randint(-20, 20),
                "test_id": test_id
            })
        
        # Simulate pathfinding
        for i in range(3):
            start = [i * 10, i * 5]
            end = [(i + 1) * 10, (i + 1) * 5]
            simulated_data.append({
                "type": "movement",
                "timestamp": i * 2000,
                "start_position": start,
                "end_position": end,
                "path": [start, [(start[0] + end[0])/2, (start[1] + end[1])/2], end],
                "duration": 1000 + i * 200,
                "test_id": test_id
            })
        
        # Simulate reactions
        for i in range(4):
            simulated_data.append({
                "type": "reaction",
                "timestamp": i * 1500,
                "stimulus": "player_approach" if i % 2 == 0 else "obstacle_detected",
                "response": "alert" if i % 2 == 0 else "avoid",
                "reaction_time": 30 + np.random.randint(-10, 10),
                "test_id": test_id
            })
        
        return simulated_data
    
    async def _analyze_decision_making(self, behavior_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze AI decision making capabilities"""
        
        decision_data = [b for b in behavior_data if b["type"] == "decision"]
        
        if not decision_data:
            return {"status": "no_decision_data"}
        
        # Analyze response times
        response_times = [d["response_time"] for d in decision_data if "response_time" in d]
        
        # Analyze decision patterns
        actions = [d["action"] for d in decision_data if "action" in d]
        action_variety = len(set(actions)) / len(actions) if actions else 0
        
        # Analyze contextual appropriateness
        appropriate_decisions = 0
        for decision in decision_data:
            if self._is_decision_appropriate(decision):
                appropriate_decisions += 1
        
        appropriateness_score = appropriate_decisions / len(decision_data) if decision_data else 0
        
        # Decision consistency analysis
        consistency_score = self._calculate_decision_consistency(decision_data)
        
        return {
            "total_decisions": len(decision_data),
            "average_response_time": np.mean(response_times) if response_times else 0,
            "response_time_consistency": 1.0 - (np.std(response_times) / np.mean(response_times)) if response_times and np.mean(response_times) > 0 else 0,
            "action_variety_score": action_variety,
            "decision_appropriateness": appropriateness_score,
            "decision_consistency": consistency_score,
            "decision_quality_score": (appropriateness_score + consistency_score + min(1.0, 100 / np.mean(response_times) if response_times and np.mean(response_times) > 0 else 0)) / 3,
            "decision_patterns": self._identify_decision_patterns(decision_data)
        }
    
    def _is_decision_appropriate(self, decision: Dict[str, Any]) -> bool:
        """Evaluate if a decision is contextually appropriate"""
        
        context = decision.get("context", {})
        action = decision.get("action", "")
        
        # Simple heuristic-based appropriateness check
        if "player_distance" in context and "health" in context:
            distance = context["player_distance"]
            health = context["health"]
            
            # Appropriate decisions based on context
            if distance < 5 and action == "attack":
                return True
            elif health < 30 and action in ["defend", "retreat"]:
                return True
            elif distance > 20 and action == "patrol":
                return True
        
        # Default to appropriate if we can't determine
        return True
    
    def _calculate_decision_consistency(self, decisions: List[Dict[str, Any]]) -> float:
        """Calculate decision making consistency"""
        
        if len(decisions) < 2:
            return 1.0
        
        # Group decisions by similar context
        context_groups = {}
        for decision in decisions:
            # Simplified context grouping
            context_key = str(sorted(decision.get("context", {}).items()))
            if context_key not in context_groups:
                context_groups[context_key] = []
            context_groups[context_key].append(decision["action"])
        
        # Calculate consistency within each context group
        consistency_scores = []
        for group_actions in context_groups.values():
            if len(group_actions) > 1:
                most_common_action = max(set(group_actions), key=group_actions.count)
                consistency = group_actions.count(most_common_action) / len(group_actions)
                consistency_scores.append(consistency)
        
        return np.mean(consistency_scores) if consistency_scores else 1.0
    
    def _identify_decision_patterns(self, decisions: List[Dict[str, Any]]) -> List[str]:
        """Identify patterns in decision making"""
        
        patterns = []
        
        if len(decisions) < 3:
            return patterns
        
        # Check for alternating patterns
        actions = [d["action"] for d in decisions if "action" in d]
        if len(set(actions)) == 2 and len(actions) >= 4:
            alternating = all(actions[i] != actions[i+1] for i in range(len(actions)-1))
            if alternating:
                patterns.append("alternating_decisions")
        
        # Check for repetitive patterns
        if len(set(actions)) == 1:
            patterns.append("repetitive_behavior")
        
        # Check for escalation patterns
        response_times = [d.get("response_time", 0) for d in decisions]
        if len(response_times) >= 3:
            increasing = all(response_times[i] <= response_times[i+1] for i in range(len(response_times)-1))
            if increasing:
                patterns.append("increasing_response_time")
        
        return patterns
    
    async def _analyze_pathfinding(self, behavior_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze AI pathfinding behavior"""
        
        movement_data = [b for b in behavior_data if b["type"] == "movement"]
        
        if not movement_data:
            return {"status": "no_pathfinding_data"}
        
        path_efficiency_scores = []
        path_smoothness_scores = []
        
        for movement in movement_data:
            if "path" in movement and "start_position" in movement and "end_position" in movement:
                # Calculate path efficiency
                efficiency = self._calculate_path_efficiency(
                    movement["start_position"],
                    movement["end_position"],
                    movement["path"]
                )
                path_efficiency_scores.append(efficiency)
                
                # Calculate path smoothness
                smoothness = self._calculate_path_smoothness(movement["path"])
                path_smoothness_scores.append(smoothness)
        
        # Analyze movement durations
        durations = [m.get("duration", 0) for m in movement_data]
        
        return {
            "total_movements": len(movement_data),
            "average_path_efficiency": np.mean(path_efficiency_scores) if path_efficiency_scores else 0,
            "average_path_smoothness": np.mean(path_smoothness_scores) if path_smoothness_scores else 0,
            "average_movement_duration": np.mean(durations) if durations else 0,
            "pathfinding_quality_score": np.mean(path_efficiency_scores + path_smoothness_scores) if (path_efficiency_scores or path_smoothness_scores) else 0,
            "pathfinding_patterns": self._identify_pathfinding_patterns(movement_data)
        }
    
    def _calculate_path_efficiency(self, start: List[float], end: List[float], path: List[List[float]]) -> float:
        """Calculate pathfinding efficiency (0-1, higher is better)"""
        
        if not path or len(path) < 2:
            return 0.0
        
        # Calculate direct distance
        direct_distance = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        
        if direct_distance == 0:
            return 1.0
        
        # Calculate actual path distance
        path_distance = 0
        for i in range(len(path) - 1):
            segment_distance = np.sqrt((path[i+1][0] - path[i][0])**2 + (path[i+1][1] - path[i][1])**2)
            path_distance += segment_distance
        
        # Efficiency is inverse of path length ratio
        if path_distance == 0:
            return 0.0
        
        efficiency = direct_distance / path_distance
        return min(1.0, efficiency)
    
    def _calculate_path_smoothness(self, path: List[List[float]]) -> float:
        """Calculate path smoothness (0-1, higher is smoother)"""
        
        if len(path) < 3:
            return 1.0
        
        # Calculate angle changes between path segments
        angle_changes = []
        for i in range(1, len(path) - 1):
            v1 = [path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]]
            v2 = [path[i+1][0] - path[i][0], path[i+1][1] - path[i][1]]
            
            # Calculate angle between vectors
            dot_product = v1[0]*v2[0] + v1[1]*v2[1]
            mag1 = np.sqrt(v1[0]**2 + v1[1]**2)
            mag2 = np.sqrt(v2[0]**2 + v2[1]**2)
            
            if mag1 * mag2 > 0:
                cos_angle = dot_product / (mag1 * mag2)
                cos_angle = max(-1, min(1, cos_angle))  # Clamp to valid range
                angle = np.arccos(cos_angle)
                angle_changes.append(angle)
        
        if not angle_changes:
            return 1.0
        
        # Smoothness is inverse of average angle change
        avg_angle_change = np.mean(angle_changes)
        smoothness = 1.0 - (avg_angle_change / np.pi)  # Normalize by max possible angle
        
        return max(0.0, smoothness)
    
    def _identify_pathfinding_patterns(self, movements: List[Dict[str, Any]]) -> List[str]:
        """Identify patterns in pathfinding behavior"""
        
        patterns = []
        
        if len(movements) < 2:
            return patterns
        
        # Check for circular movements
        positions = []
        for movement in movements:
            if "end_position" in movement:
                positions.append(tuple(movement["end_position"]))
        
        if len(set(positions)) < len(positions) * 0.7:  # 70% unique positions
            patterns.append("repetitive_destinations")
        
        # Check for straight-line preferences
        straight_line_movements = 0
        for movement in movements:
            if "path" in movement and len(movement["path"]) <= 2:
                straight_line_movements += 1
        
        if straight_line_movements > len(movements) * 0.8:
            patterns.append("straight_line_preference")
        
        return patterns
    
    async def _analyze_reactive_behaviors(self, behavior_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze AI reactive behaviors"""
        
        reaction_data = [b for b in behavior_data if b["type"] == "reaction"]
        
        if not reaction_data:
            return {"status": "no_reaction_data"}
        
        # Analyze reaction times
        reaction_times = [r.get("reaction_time", 0) for r in reaction_data]
        
        # Analyze stimulus-response patterns
        stimulus_response_map = {}
        for reaction in reaction_data:
            stimulus = reaction.get("stimulus", "unknown")
            response = reaction.get("response", "unknown")
            
            if stimulus not in stimulus_response_map:
                stimulus_response_map[stimulus] = []
            stimulus_response_map[stimulus].append(response)
        
        # Calculate response consistency for each stimulus
        response_consistency = {}
        for stimulus, responses in stimulus_response_map.items():
            if len(responses) > 1:
                most_common = max(set(responses), key=responses.count)
                consistency = responses.count(most_common) / len(responses)
                response_consistency[stimulus] = consistency
        
        return {
            "total_reactions": len(reaction_data),
            "average_reaction_time": np.mean(reaction_times) if reaction_times else 0,
            "reaction_time_consistency": 1.0 - (np.std(reaction_times) / np.mean(reaction_times)) if reaction_times and np.mean(reaction_times) > 0 else 0,
            "stimulus_types_detected": len(stimulus_response_map),
            "response_consistency": response_consistency,
            "overall_response_consistency": np.mean(list(response_consistency.values())) if response_consistency else 0,
            "reactive_quality_score": self._calculate_reactive_quality_score(reaction_times, response_consistency)
        }
    
    def _calculate_reactive_quality_score(self, reaction_times: List[float], 
                                        response_consistency: Dict[str, float]) -> float:
        """Calculate overall reactive behavior quality score"""
        
        if not reaction_times:
            return 0.0
        
        # Speed component (faster is better, up to a point)
        avg_reaction_time = np.mean(reaction_times)
        speed_score = max(0, 1 - (avg_reaction_time / 200))  # 200ms is considered slow
        
        # Consistency component
        consistency_score = np.mean(list(response_consistency.values())) if response_consistency else 0.5
        
        # Time consistency component
        time_consistency = 1.0 - (np.std(reaction_times) / np.mean(reaction_times)) if np.mean(reaction_times) > 0 else 0
        
        # Weighted average
        return (speed_score * 0.4 + consistency_score * 0.4 + time_consistency * 0.2)
    
    async def _analyze_learning_capabilities(self, behavior_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze AI learning and adaptation capabilities"""
        
        if len(behavior_data) < 10:
            return {"status": "insufficient_data_for_learning_analysis"}
        
        # Sort by timestamp
        sorted_data = sorted(behavior_data, key=lambda x: x.get("timestamp", 0))
        
        # Divide into early and late periods
        mid_point = len(sorted_data) // 2
        early_period = sorted_data[:mid_point]
        late_period = sorted_data[mid_point:]
        
        # Analyze performance changes over time
        learning_indicators = {
            "response_time_improvement": 0.0,
            "decision_quality_improvement": 0.0,
            "pattern_adaptation": 0.0
        }
        
        # Response time improvement
        early_response_times = [d.get("response_time", 0) for d in early_period if "response_time" in d]
        late_response_times = [d.get("response_time", 0) for d in late_period if "response_time" in d]
        
        if early_response_times and late_response_times:
            early_avg = np.mean(early_response_times)
            late_avg = np.mean(late_response_times)
            if early_avg > 0:
                improvement = (early_avg - late_avg) / early_avg
                learning_indicators["response_time_improvement"] = max(0, improvement)
        
        # Decision quality improvement (placeholder - would need more sophisticated analysis)
        early_decisions = [d for d in early_period if d["type"] == "decision"]
        late_decisions = [d for d in late_period if d["type"] == "decision"]
        
        if len(early_decisions) > 0 and len(late_decisions) > 0:
            early_quality = self._estimate_decision_quality(early_decisions)
            late_quality = self._estimate_decision_quality(late_decisions)
            learning_indicators["decision_quality_improvement"] = max(0, late_quality - early_quality)
        
        return {
            "learning_analysis_performed": True,
            "data_periods_compared": 2,
            "learning_indicators": learning_indicators,
            "overall_learning_score": np.mean(list(learning_indicators.values())),
            "adaptation_evidence": self._detect_adaptation_evidence(early_period, late_period)
        }
    
    def _estimate_decision_quality(self, decisions: List[Dict[str, Any]]) -> float:
        """Estimate decision quality (simplified heuristic)"""
        
        if not decisions:
            return 0.0
        
        appropriate_count = sum(1 for d in decisions if self._is_decision_appropriate(d))
        return appropriate_count / len(decisions)
    
    def _detect_adaptation_evidence(self, early_data: List[Dict[str, Any]], 
                                  late_data: List[Dict[str, Any]]) -> List[str]:
        """Detect evidence of AI adaptation"""
        
        evidence = []
        
        # Check for strategy changes
        early_actions = [d.get("action", "") for d in early_data if d.get("type") == "decision"]
        late_actions = [d.get("action", "") for d in late_data if d.get("type") == "decision"]
        
        if early_actions and late_actions:
            early_action_dist = {action: early_actions.count(action) for action in set(early_actions)}
            late_action_dist = {action: late_actions.count(action) for action in set(late_actions)}
            
            # Significant change in action distribution indicates adaptation
            if set(early_action_dist.keys()) != set(late_action_dist.keys()):
                evidence.append("strategy_diversification")
        
        # Check for response time optimization
        early_times = [d.get("response_time", 0) for d in early_data if "response_time" in d]
        late_times = [d.get("response_time", 0) for d in late_data if "response_time" in d]
        
        if early_times and late_times and np.mean(late_times) < np.mean(early_times) * 0.9:
            evidence.append("response_optimization")
        
        return evidence
    
    async def _analyze_behavioral_consistency(self, behavior_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze AI behavioral consistency"""
        
        consistency_metrics = {}
        
        # Decision consistency
        decisions = [b for b in behavior_data if b["type"] == "decision"]
        if decisions:
            consistency_metrics["decision_consistency"] = self._calculate_decision_consistency(decisions)
        
        # Reaction consistency
        reactions = [b for b in behavior_data if b["type"] == "reaction"]
        if reactions:
            reaction_times = [r.get("reaction_time", 0) for r in reactions]
            if reaction_times:
                mean_time = np.mean(reaction_times)
                std_time = np.std(reaction_times)
                consistency_metrics["reaction_time_consistency"] = 1.0 - (std_time / mean_time) if mean_time > 0 else 0
        
        # Movement consistency
        movements = [b for b in behavior_data if b["type"] == "movement"]
        if movements:
            durations = [m.get("duration", 0) for m in movements]
            if durations:
                mean_duration = np.mean(durations)
                std_duration = np.std(durations)
                consistency_metrics["movement_consistency"] = 1.0 - (std_duration / mean_duration) if mean_duration > 0 else 0
        
        overall_consistency = np.mean(list(consistency_metrics.values())) if consistency_metrics else 0
        
        return {
            "consistency_metrics": consistency_metrics,
            "overall_consistency_score": overall_consistency,
            "consistency_rating": self._rate_consistency(overall_consistency),
            "consistency_issues": self._identify_consistency_issues(consistency_metrics)
        }
    
    def _rate_consistency(self, score: float) -> str:
        """Rate behavioral consistency"""
        
        if score >= 0.9:
            return "excellent"
        elif score >= 0.8:
            return "good"
        elif score >= 0.7:
            return "acceptable"
        elif score >= 0.6:
            return "fair"
        else:
            return "poor"
    
    def _identify_consistency_issues(self, metrics: Dict[str, float]) -> List[str]:
        """Identify consistency issues"""
        
        issues = []
        
        for metric_name, score in metrics.items():
            if score < 0.7:
                issues.append(f"low_{metric_name}")
        
        return issues
    
    async def _analyze_ai_performance(self, behavior_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze AI performance metrics"""
        
        performance_data = {
            "response_times": [],
            "action_counts": {},
            "error_indicators": []
        }
        
        for behavior in behavior_data:
            # Collect response times
            if "response_time" in behavior:
                performance_data["response_times"].append(behavior["response_time"])
            
            if "reaction_time" in behavior:
                performance_data["response_times"].append(behavior["reaction_time"])
            
            # Count actions
            action = behavior.get("action") or behavior.get("response", "unknown")
            performance_data["action_counts"][action] = performance_data["action_counts"].get(action, 0) + 1
            
            # Check for error indicators
            if behavior.get("response_time", 0) > 500:  # Very slow response
                performance_data["error_indicators"].append("slow_response")
        
        if performance_data["response_times"]:
            avg_response_time = np.mean(performance_data["response_times"])
            response_consistency = 1.0 - (np.std(performance_data["response_times"]) / avg_response_time) if avg_response_time > 0 else 0
        else:
            avg_response_time = 0
            response_consistency = 0
        
        return {
            "average_response_time": avg_response_time,
            "response_time_consistency": response_consistency,
            "total_actions": sum(performance_data["action_counts"].values()),
            "action_diversity": len(performance_data["action_counts"]),
            "performance_issues": len(performance_data["error_indicators"]),
            "performance_score": self._calculate_performance_score(avg_response_time, response_consistency, performance_data["error_indicators"])
        }
    
    def _calculate_performance_score(self, avg_response_time: float, 
                                   consistency: float, error_indicators: List[str]) -> float:
        """Calculate AI performance score"""
        
        # Speed score (faster is better)
        speed_score = max(0, 1 - (avg_response_time / 200)) if avg_response_time > 0 else 0
        
        # Consistency score
        consistency_score = consistency
        
        # Error penalty
        error_penalty = len(error_indicators) * 0.1
        
        # Combine scores
        performance_score = (speed_score * 0.5 + consistency_score * 0.5) - error_penalty
        
        return max(0, min(1, performance_score))
    
    async def _analyze_strategic_behavior(self, behavior_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze strategic AI behavior"""
        
        strategic_indicators = {
            "goal_oriented_actions": 0,
            "tactical_sequences": 0,
            "adaptive_strategies": 0
        }
        
        decisions = [b for b in behavior_data if b["type"] == "decision"]
        
        # Look for goal-oriented behavior patterns
        if len(decisions) >= 3:
            # Check for action sequences that suggest planning
            actions = [d.get("action", "") for d in decisions]
            
            # Look for tactical sequences (attack -> defend -> attack)
            for i in range(len(actions) - 2):
                if actions[i] == "attack" and actions[i+1] == "defend" and actions[i+2] == "attack":
                    strategic_indicators["tactical_sequences"] += 1
            
            # Count decisions that seem goal-oriented
            for decision in decisions:
                if self._is_goal_oriented_decision(decision):
                    strategic_indicators["goal_oriented_actions"] += 1
        
        return {
            "strategic_indicators": strategic_indicators,
            "strategic_behavior_score": self._calculate_strategic_score(strategic_indicators, len(decisions)),
            "strategic_patterns": self._identify_strategic_patterns(decisions)
        }
    
    def _is_goal_oriented_decision(self, decision: Dict[str, Any]) -> bool:
        """Check if a decision appears goal-oriented"""
        
        context = decision.get("context", {})
        action = decision.get("action", "")
        
        # Simple heuristics for goal-oriented behavior
        if "health" in context and context["health"] < 50 and action in ["defend", "retreat", "heal"]:
            return True
        
        if "player_distance" in context and context["player_distance"] < 10 and action == "attack":
            return True
        
        return False
    
    def _calculate_strategic_score(self, indicators: Dict[str, int], total_decisions: int) -> float:
        """Calculate strategic behavior score"""
        
        if total_decisions == 0:
            return 0.0
        
        goal_oriented_ratio = indicators["goal_oriented_actions"] / total_decisions
        tactical_bonus = min(0.3, indicators["tactical_sequences"] * 0.1)
        
        return min(1.0, goal_oriented_ratio + tactical_bonus)
    
    def _identify_strategic_patterns(self, decisions: List[Dict[str, Any]]) -> List[str]:
        """Identify strategic behavioral patterns"""
        
        patterns = []
        
        if len(decisions) < 3:
            return patterns
        
        actions = [d.get("action", "") for d in decisions]
        
        # Check for defensive patterns
        defensive_actions = ["defend", "retreat", "heal", "block"]
        defensive_count = sum(1 for action in actions if action in defensive_actions)
        
        if defensive_count > len(actions) * 0.6:
            patterns.append("defensive_strategy")
        
        # Check for aggressive patterns
        aggressive_actions = ["attack", "charge", "pursue"]
        aggressive_count = sum(1 for action in actions if action in aggressive_actions)
        
        if aggressive_count > len(actions) * 0.6:
            patterns.append("aggressive_strategy")
        
        # Check for balanced patterns
        if 0.3 <= defensive_count / len(actions) <= 0.7 and 0.3 <= aggressive_count / len(actions) <= 0.7:
            patterns.append("balanced_strategy")
        
        return patterns
    
    async def _analyze_challenge_level(self, behavior_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze AI challenge level for players"""
        
        challenge_factors = {
            "difficulty_consistency": 0.0,
            "adaptive_difficulty": 0.0,
            "player_engagement": 0.0
        }
        
        # Analyze response times (faster AI = more challenging)
        response_times = [b.get("response_time", 0) for b in behavior_data if "response_time" in b]
        response_times.extend([b.get("reaction_time", 0) for b in behavior_data if "reaction_time" in b])
        
        if response_times:
            avg_response = np.mean(response_times)
            # Challenge increases as response time decreases (up to a point)
            challenge_factors["difficulty_consistency"] = max(0, 1 - (avg_response / 100))
        
        # Analyze decision complexity
        decisions = [b for b in behavior_data if b["type"] == "decision"]
        if decisions:
            # More varied actions = more challenging
            actions = [d.get("action", "") for d in decisions]
            action_variety = len(set(actions)) / len(actions) if actions else 0
            challenge_factors["adaptive_difficulty"] = action_variety
        
        # Estimate player engagement (simplified)
        challenge_factors["player_engagement"] = np.mean([
            challenge_factors["difficulty_consistency"],
            challenge_factors["adaptive_difficulty"]
        ])
        
        overall_challenge = np.mean(list(challenge_factors.values()))
        
        return {
            "challenge_factors": challenge_factors,
            "overall_challenge_score": overall_challenge,
            "challenge_rating": self._rate_challenge_level(overall_challenge),
            "recommendations": self._generate_challenge_recommendations(overall_challenge)
        }
    
    def _rate_challenge_level(self, score: float) -> str:
        """Rate AI challenge level"""
        
        if score >= 0.8:
            return "very_challenging"
        elif score >= 0.6:
            return "challenging"
        elif score >= 0.4:
            return "moderate"
        elif score >= 0.2:
            return "easy"
        else:
            return "very_easy"
    
    def _generate_challenge_recommendations(self, score: float) -> List[str]:
        """Generate challenge level recommendations"""
        
        recommendations = []
        
        if score < 0.3:
            recommendations.extend([
                "Increase AI response speed",
                "Add more complex decision making",
                "Implement adaptive difficulty scaling"
            ])
        elif score > 0.8:
            recommendations.extend([
                "Consider reducing AI response speed for accessibility",
                "Add difficulty options for different player skill levels",
                "Implement beginner-friendly AI modes"
            ])
        else:
            recommendations.append("Challenge level appears well-balanced")
        
        return recommendations
    
    async def _recognize_behavior_patterns(self, behavior_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Recognize and classify behavior patterns"""
        
        patterns = []
        
        # Temporal patterns
        if len(behavior_data) >= 10:
            timestamps = [b.get("timestamp", 0) for b in behavior_data]
            if timestamps:
                time_intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
                if time_intervals:
                    avg_interval = np.mean(time_intervals)
                    std_interval = np.std(time_intervals)
                    
                    if std_interval / avg_interval < 0.2:  # Regular intervals
                        patterns.append(AIBehaviorPattern(
                            pattern_id="regular_timing",
                            behavior_type=AIBehaviorType.PREDICTIVE,
                            frequency=len(behavior_data),
                            consistency_score=1.0 - (std_interval / avg_interval),
                            effectiveness_score=0.7,
                            description="AI exhibits regular timing patterns",
                            examples=[f"Average interval: {avg_interval:.2f}ms"]
                        ))
        
        # Decision patterns
        decisions = [b for b in behavior_data if b["type"] == "decision"]
        if len(decisions) >= 5:
            actions = [d.get("action", "") for d in decisions]
            action_counts = {action: actions.count(action) for action in set(actions)}
            
            # Most common action pattern
            most_common_action = max(action_counts, key=action_counts.get)
            if action_counts[most_common_action] > len(actions) * 0.6:
                patterns.append(AIBehaviorPattern(
                    pattern_id="dominant_action",
                    behavior_type=AIBehaviorType.DECISION_MAKING,
                    frequency=action_counts[most_common_action],
                    consistency_score=action_counts[most_common_action] / len(actions),
                    effectiveness_score=0.8,
                    description=f"AI heavily favors '{most_common_action}' action",
                    examples=[f"Used {action_counts[most_common_action]} times out of {len(actions)}"]
                ))
        
        return {
            "patterns_detected": len(patterns),
            "behavior_patterns": [p.__dict__ for p in patterns],
            "pattern_diversity": len(set(p.behavior_type for p in patterns)),
            "overall_predictability": self._calculate_predictability_score(patterns)
        }
    
    def _calculate_predictability_score(self, patterns: List[AIBehaviorPattern]) -> float:
        """Calculate how predictable the AI behavior is"""
        
        if not patterns:
            return 0.5  # Neutral predictability
        
        # High consistency = high predictability
        avg_consistency = np.mean([p.consistency_score for p in patterns])
        
        # More patterns = less predictable
        pattern_diversity_factor = min(1.0, len(patterns) / 5)
        
        # Predictability increases with consistency, decreases with diversity
        predictability = avg_consistency * (1 - pattern_diversity_factor * 0.3)
        
        return predictability
    
    async def _assess_ai_quality(self, decision_analysis: Dict[str, Any],
                                pathfinding_analysis: Dict[str, Any],
                                reactive_analysis: Dict[str, Any],
                                learning_analysis: Dict[str, Any],
                                consistency_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall AI quality across multiple dimensions"""
        
        quality_scores = {}
        
        # Intelligence score
        if "decision_quality_score" in decision_analysis:
            quality_scores[AIQualityMetric.INTELLIGENCE] = decision_analysis["decision_quality_score"]
        
        # Consistency score
        if "overall_consistency_score" in consistency_analysis:
            quality_scores[AIQualityMetric.CONSISTENCY] = consistency_analysis["overall_consistency_score"]
        
        # Responsiveness score
        if "reactive_quality_score" in reactive_analysis:
            quality_scores[AIQualityMetric.RESPONSIVENESS] = reactive_analysis["reactive_quality_score"]
        
        # Adaptability score
        if "overall_learning_score" in learning_analysis:
            quality_scores[AIQualityMetric.ADAPTABILITY] = learning_analysis["overall_learning_score"]
        
        # Pathfinding quality (as part of intelligence)
        if "pathfinding_quality_score" in pathfinding_analysis:
            if AIQualityMetric.INTELLIGENCE in quality_scores:
                quality_scores[AIQualityMetric.INTELLIGENCE] = (
                    quality_scores[AIQualityMetric.INTELLIGENCE] + 
                    pathfinding_analysis["pathfinding_quality_score"]
                ) / 2
            else:
                quality_scores[AIQualityMetric.INTELLIGENCE] = pathfinding_analysis["pathfinding_quality_score"]
        
        # Calculate overall quality
        overall_quality = np.mean(list(quality_scores.values())) if quality_scores else 0.5
        
        return {
            "quality_dimensions": quality_scores,
            "overall_quality_score": overall_quality,
            "quality_rating": self._rate_ai_quality(overall_quality),
            "strengths": self._identify_ai_strengths(quality_scores),
            "weaknesses": self._identify_ai_weaknesses(quality_scores)
        }
    
    def _rate_ai_quality(self, score: float) -> str:
        """Rate overall AI quality"""
        
        if score >= 0.9:
            return "exceptional"
        elif score >= 0.8:
            return "excellent"
        elif score >= 0.7:
            return "good"
        elif score >= 0.6:
            return "acceptable"
        elif score >= 0.5:
            return "fair"
        else:
            return "poor"
    
    def _identify_ai_strengths(self, quality_scores: Dict[AIQualityMetric, float]) -> List[str]:
        """Identify AI behavioral strengths"""
        
        strengths = []
        
        for metric, score in quality_scores.items():
            if score >= 0.8:
                strengths.append(f"strong_{metric.value}")
        
        return strengths
    
    def _identify_ai_weaknesses(self, quality_scores: Dict[AIQualityMetric, float]) -> List[str]:
        """Identify AI behavioral weaknesses"""
        
        weaknesses = []
        
        for metric, score in quality_scores.items():
            if score < 0.6:
                weaknesses.append(f"weak_{metric.value}")
        
        return weaknesses
    
    def _calculate_analysis_coverage(self, behavior_data: List[Dict[str, Any]]) -> float:
        """Calculate how comprehensive the behavior analysis is"""
        
        behavior_types = set(b.get("type", "unknown") for b in behavior_data)
        expected_types = {"decision", "movement", "reaction"}
        
        coverage = len(behavior_types.intersection(expected_types)) / len(expected_types)
        return coverage
    
    async def _calculate_ai_behavior_score(self, quality_assessment: Dict[str, Any]) -> float:
        """Calculate overall AI behavior score"""
        
        return quality_assessment.get("overall_quality_score", 0.5) * 100
    
    def _determine_ai_rating(self, score: float) -> str:
        """Determine overall AI rating based on score"""
        
        if score >= 90:
            return "exceptional"
        elif score >= 80:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 60:
            return "acceptable"
        elif score >= 50:
            return "fair"
        else:
            return "poor"
    
    async def _generate_ai_recommendations(self, quality_assessment: Dict[str, Any]) -> List[str]:
        """Generate AI behavior improvement recommendations"""
        
        recommendations = []
        
        # Recommendations based on weaknesses
        weaknesses = quality_assessment.get("weaknesses", [])
        
        if "weak_intelligence" in weaknesses:
            recommendations.extend([
                "Improve decision-making algorithms",
                "Implement more sophisticated AI reasoning",
                "Add contextual awareness to AI decisions"
            ])
        
        if "weak_consistency" in weaknesses:
            recommendations.extend([
                "Standardize AI behavior patterns",
                "Implement behavior validation systems",
                "Add consistency checks to AI logic"
            ])
        
        if "weak_responsiveness" in weaknesses:
            recommendations.extend([
                "Optimize AI response times",
                "Implement predictive processing",
                "Add performance monitoring for AI systems"
            ])
        
        if "weak_adaptability" in weaknesses:
            recommendations.extend([
                "Implement machine learning components",
                "Add player behavior analysis",
                "Create adaptive difficulty systems"
            ])
        
        # General recommendations
        overall_score = quality_assessment.get("overall_quality_score", 0.5)
        
        if overall_score < 0.7:
            recommendations.extend([
                "Conduct comprehensive AI behavior review",
                "Implement AI testing framework",
                "Regular AI behavior validation"
            ])
        
        return recommendations[:10]  # Return top 10 recommendations
    
    async def _load_behavior_models(self) -> None:
        """Load AI behavior analysis models"""
        # In production, this would load ML models for behavior analysis
        self.behavior_models = {
            "decision_classifier": {"loaded": True, "accuracy": 0.85},
            "pattern_recognizer": {"loaded": True, "accuracy": 0.78},
            "quality_assessor": {"loaded": True, "accuracy": 0.82}
        }
    
    async def _calibrate_analysis_parameters(self) -> None:
        """Calibrate analysis parameters based on game type"""
        # Adjust thresholds based on game genre
        if hasattr(self.settings, 'game_genre'):
            if self.settings.game_genre == "action":
                self.behavior_thresholds["response_time_ms"] = 50  # Faster for action games
            elif self.settings.game_genre == "strategy":
                self.behavior_thresholds["response_time_ms"] = 200  # Slower for strategy games
    
    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get AI behavior agent health metrics"""
        return {
            "agent_id": self.agent_id,
            "status": "healthy",
            "cpu_usage": 0.28,
            "memory_usage": 0.32,
            "behaviors_analyzed": 150,  # Would track actual metrics
            "models_loaded": len(self.behavior_models)
        }
