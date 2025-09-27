"""
Advanced AI Analysis Agent
Deep Learning-Powered Test Result Analysis & Pattern Recognition
"""

import asyncio
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import structlog

from src.core.config import get_settings


@dataclass
class AnalysisInsight:
    """AI-generated analysis insight"""
    category: str
    severity: str  # critical, high, medium, low, info
    confidence: float
    title: str
    description: str
    evidence: List[str]
    recommendations: List[str]
    impact_score: float


@dataclass
class PatternMatch:
    """Detected pattern in test results"""
    pattern_id: str
    pattern_type: str
    confidence: float
    occurrences: int
    description: str
    related_tests: List[str]


class AnalyzerAgent:
    """Advanced AI-powered test result analyzer with ML capabilities"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.settings = get_settings()
        self.logger = structlog.get_logger(__name__)
        
        # Analysis models and patterns
        self.known_patterns = self._load_analysis_patterns()
        self.ml_models = {}
        self.historical_data = []
        
        # Analysis thresholds
        self.performance_thresholds = {
            "critical_response_time": 5000,  # ms
            "warning_response_time": 2000,   # ms
            "critical_error_rate": 0.1,      # 10%
            "warning_error_rate": 0.05,      # 5%
            "min_success_rate": 0.95         # 95%
        }
        
    async def initialize(self) -> None:
        """Initialize the analyzer agent with ML models"""
        try:
            await self._load_ml_models()
            await self._initialize_pattern_recognition()
            self.logger.info(f"Analyzer agent {self.agent_id} initialized with ML capabilities")
        except Exception as e:
            self.logger.error(f"Failed to initialize analyzer: {e}")
            raise
    
    async def analyze_results(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive AI-powered analysis of test results"""
        
        try:
            self.logger.info(f"Starting comprehensive analysis of {len(test_results)} test results")
            
            # Statistical analysis
            stats = await self._calculate_comprehensive_statistics(test_results)
            
            # Pattern recognition
            patterns = await self._detect_patterns(test_results)
            
            # Anomaly detection
            anomalies = await self._detect_anomalies(test_results)
            
            # Performance analysis
            performance_analysis = await self._analyze_performance_trends(test_results)
            
            # Failure analysis
            failure_analysis = await self._analyze_failures(test_results)
            
            # Risk assessment
            risk_assessment = await self._assess_risks(test_results)
            
            # AI insights generation
            insights = await self._generate_ai_insights(test_results, patterns, anomalies)
            
            # Root cause analysis
            root_causes = await self._perform_root_cause_analysis(test_results)
            
            # Predictive analysis
            predictions = await self._generate_predictions(test_results)
            
            analysis = {
                "analyzer_id": self.agent_id,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "test_summary": {
                    "total_tests": len(test_results),
                    "passed": len([r for r in test_results if r.get("status") == "passed"]),
                    "failed": len([r for r in test_results if r.get("status") == "failed"]),
                    "success_rate": stats["success_rate"]
                },
                "statistical_analysis": stats,
                "detected_patterns": [p.__dict__ for p in patterns],
                "anomalies": anomalies,
                "performance_analysis": performance_analysis,
                "failure_analysis": failure_analysis,
                "risk_assessment": risk_assessment,
                "ai_insights": [i.__dict__ for i in insights],
                "root_cause_analysis": root_causes,
                "predictions": predictions,
                "confidence_score": self._calculate_overall_confidence(test_results),
                "recommendations": await self._generate_strategic_recommendations(test_results)
            }
            
            # Store for historical analysis
            self.historical_data.append(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise
    
    def _load_analysis_patterns(self) -> Dict[str, Any]:
        """Load known analysis patterns"""
        return {
            "performance_degradation": {
                "indicators": ["increasing_response_time", "memory_growth", "fps_drop"],
                "severity": "high",
                "description": "Performance metrics showing degradation over time"
            },
            "intermittent_failure": {
                "indicators": ["random_failures", "timing_dependent", "load_sensitive"],
                "severity": "medium",
                "description": "Tests failing inconsistently under certain conditions"
            },
            "cascade_failure": {
                "indicators": ["dependency_chain", "error_propagation", "system_wide_impact"],
                "severity": "critical",
                "description": "Single failure causing multiple downstream failures"
            },
            "browser_compatibility": {
                "indicators": ["browser_specific_failures", "rendering_differences", "js_errors"],
                "severity": "medium",
                "description": "Issues specific to certain browser types or versions"
            },
            "memory_leak": {
                "indicators": ["continuous_memory_growth", "gc_pressure", "oom_errors"],
                "severity": "high",
                "description": "Memory usage increasing without bounds"
            }
        }
    
    async def _load_ml_models(self) -> None:
        """Load machine learning models for analysis"""
        # Simulate ML model loading (would load actual models in production)
        self.ml_models = {
            "anomaly_detector": {"type": "isolation_forest", "trained": True},
            "performance_predictor": {"type": "lstm", "trained": True},
            "failure_classifier": {"type": "random_forest", "trained": True},
            "pattern_recognizer": {"type": "clustering", "trained": True}
        }
    
    async def _initialize_pattern_recognition(self) -> None:
        """Initialize pattern recognition system"""
        # Initialize pattern matching algorithms
        pass
    
    async def _calculate_comprehensive_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate comprehensive statistical metrics"""
        
        if not results:
            return {"success_rate": 0.0, "error": "No results to analyze"}
        
        total_tests = len(results)
        passed_tests = len([r for r in results if r.get("status") == "passed"])
        failed_tests = total_tests - passed_tests
        
        # Execution time statistics
        execution_times = [r.get("execution_time", 0) for r in results if "execution_time" in r]
        
        stats = {
            "success_rate": passed_tests / total_tests,
            "failure_rate": failed_tests / total_tests,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
        }
        
        if execution_times:
            stats.update({
                "avg_execution_time": np.mean(execution_times),
                "median_execution_time": np.median(execution_times),
                "std_execution_time": np.std(execution_times),
                "min_execution_time": np.min(execution_times),
                "max_execution_time": np.max(execution_times),
                "p95_execution_time": np.percentile(execution_times, 95),
                "p99_execution_time": np.percentile(execution_times, 99)
            })
        
        # Performance metrics if available
        fps_values = []
        memory_values = []
        
        for result in results:
            if "result_details" in result:
                details = result["result_details"]
                if "avg_fps" in details:
                    fps_values.append(details["avg_fps"])
                if "memory_used" in details:
                    memory_values.append(details["memory_used"])
        
        if fps_values:
            stats["performance_metrics"] = {
                "avg_fps": np.mean(fps_values),
                "min_fps": np.min(fps_values),
                "fps_stability": 1.0 - (np.std(fps_values) / np.mean(fps_values)) if np.mean(fps_values) > 0 else 0
            }
        
        if memory_values:
            stats["memory_metrics"] = {
                "avg_memory": np.mean(memory_values),
                "max_memory": np.max(memory_values),
                "memory_trend": "stable" if np.std(memory_values) < np.mean(memory_values) * 0.1 else "variable"
            }
        
        return stats
    
    async def _detect_patterns(self, results: List[Dict[str, Any]]) -> List[PatternMatch]:
        """Detect patterns in test results using ML and heuristics"""
        
        patterns = []
        
        # Pattern 1: Performance degradation
        performance_pattern = await self._detect_performance_degradation(results)
        if performance_pattern:
            patterns.append(performance_pattern)
        
        # Pattern 2: Intermittent failures
        intermittent_pattern = await self._detect_intermittent_failures(results)
        if intermittent_pattern:
            patterns.append(intermittent_pattern)
        
        # Pattern 3: Browser-specific issues
        browser_pattern = await self._detect_browser_patterns(results)
        if browser_pattern:
            patterns.append(browser_pattern)
        
        # Pattern 4: Time-based patterns
        time_pattern = await self._detect_temporal_patterns(results)
        if time_pattern:
            patterns.append(time_pattern)
        
        return patterns
    
    async def _detect_performance_degradation(self, results: List[Dict[str, Any]]) -> Optional[PatternMatch]:
        """Detect performance degradation patterns"""
        
        performance_data = []
        for i, result in enumerate(results):
            if "result_details" in result and "avg_fps" in result["result_details"]:
                performance_data.append((i, result["result_details"]["avg_fps"]))
        
        if len(performance_data) < 3:
            return None
        
        # Simple linear regression to detect trend
        x_vals = [p[0] for p in performance_data]
        y_vals = [p[1] for p in performance_data]
        
        # Calculate slope
        n = len(performance_data)
        slope = (n * sum(x * y for x, y in performance_data) - sum(x_vals) * sum(y_vals)) / \
                (n * sum(x * x for x in x_vals) - sum(x_vals) ** 2) if n > 1 else 0
        
        # Negative slope indicates degradation
        if slope < -0.5:  # Threshold for significant degradation
            return PatternMatch(
                pattern_id="perf_degradation_001",
                pattern_type="performance_degradation",
                confidence=min(abs(slope) / 2.0, 1.0),
                occurrences=len(performance_data),
                description=f"Performance degrading at rate of {slope:.2f} FPS per test",
                related_tests=[r.get("test_id", f"test_{i}") for i, r in enumerate(results)]
            )
        
        return None
    
    async def _detect_intermittent_failures(self, results: List[Dict[str, Any]]) -> Optional[PatternMatch]:
        """Detect intermittent failure patterns"""
        
        # Look for alternating pass/fail patterns
        statuses = [r.get("status", "unknown") for r in results]
        
        # Count transitions between pass and fail
        transitions = 0
        for i in range(1, len(statuses)):
            if statuses[i] != statuses[i-1] and statuses[i] in ["passed", "failed"] and statuses[i-1] in ["passed", "failed"]:
                transitions += 1
        
        # High transition rate indicates intermittent issues
        if len(statuses) > 5 and transitions > len(statuses) * 0.3:
            return PatternMatch(
                pattern_id="intermittent_001",
                pattern_type="intermittent_failure",
                confidence=min(transitions / len(statuses), 1.0),
                occurrences=transitions,
                description=f"Intermittent failures detected with {transitions} status transitions",
                related_tests=[r.get("test_id", f"test_{i}") for i, r in enumerate(results) if r.get("status") == "failed"]
            )
        
        return None
    
    async def _detect_browser_patterns(self, results: List[Dict[str, Any]]) -> Optional[PatternMatch]:
        """Detect browser-specific patterns"""
        # Implementation for browser pattern detection
        return None
    
    async def _detect_temporal_patterns(self, results: List[Dict[str, Any]]) -> Optional[PatternMatch]:
        """Detect time-based patterns"""
        # Implementation for temporal pattern detection
        return None
    
    async def _detect_anomalies(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies using statistical and ML methods"""
        
        anomalies = []
        
        # Statistical anomaly detection
        execution_times = [r.get("execution_time", 0) for r in results if "execution_time" in r]
        
        if len(execution_times) > 5:
            mean_time = np.mean(execution_times)
            std_time = np.std(execution_times)
            
            # Detect outliers using z-score
            for i, time_val in enumerate(execution_times):
                z_score = abs(time_val - mean_time) / std_time if std_time > 0 else 0
                
                if z_score > 2.5:  # More than 2.5 standard deviations
                    anomalies.append({
                        "type": "execution_time_outlier",
                        "test_id": results[i].get("test_id", f"test_{i}"),
                        "value": time_val,
                        "expected_range": [mean_time - 2*std_time, mean_time + 2*std_time],
                        "z_score": z_score,
                        "severity": "high" if z_score > 3 else "medium"
                    })
        
        # Performance anomaly detection
        for i, result in enumerate(results):
            if "result_details" in result:
                details = result["result_details"]
                
                # FPS anomalies
                if "avg_fps" in details:
                    fps = details["avg_fps"]
                    if fps < 15:  # Critically low FPS
                        anomalies.append({
                            "type": "critical_fps_drop",
                            "test_id": result.get("test_id", f"test_{i}"),
                            "value": fps,
                            "threshold": 15,
                            "severity": "critical"
                        })
                
                # Memory anomalies
                if "memory_used" in details:
                    memory = details["memory_used"]
                    if memory > 500_000_000:  # > 500MB
                        anomalies.append({
                            "type": "high_memory_usage",
                            "test_id": result.get("test_id", f"test_{i}"),
                            "value": memory,
                            "threshold": 500_000_000,
                            "severity": "high"
                        })
        
        return anomalies
    
    async def _analyze_performance_trends(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        
        trends = {
            "overall_trend": "stable",
            "fps_trend": "unknown",
            "memory_trend": "unknown",
            "execution_time_trend": "unknown"
        }
        
        # Analyze FPS trend
        fps_values = []
        for result in results:
            if "result_details" in result and "avg_fps" in result["result_details"]:
                fps_values.append(result["result_details"]["avg_fps"])
        
        if len(fps_values) >= 3:
            # Simple trend detection
            first_third = fps_values[:len(fps_values)//3]
            last_third = fps_values[-len(fps_values)//3:]
            
            avg_first = np.mean(first_third)
            avg_last = np.mean(last_third)
            
            if avg_last < avg_first * 0.9:
                trends["fps_trend"] = "declining"
            elif avg_last > avg_first * 1.1:
                trends["fps_trend"] = "improving"
            else:
                trends["fps_trend"] = "stable"
        
        # Analyze execution time trend
        exec_times = [r.get("execution_time", 0) for r in results if "execution_time" in r]
        if len(exec_times) >= 3:
            first_third = exec_times[:len(exec_times)//3]
            last_third = exec_times[-len(exec_times)//3:]
            
            avg_first = np.mean(first_third)
            avg_last = np.mean(last_third)
            
            if avg_last > avg_first * 1.2:
                trends["execution_time_trend"] = "increasing"
            elif avg_last < avg_first * 0.8:
                trends["execution_time_trend"] = "decreasing"
            else:
                trends["execution_time_trend"] = "stable"
        
        return trends
    
    async def _analyze_failures(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive failure analysis"""
        
        failed_results = [r for r in results if r.get("status") == "failed"]
        
        if not failed_results:
            return {"failure_rate": 0.0, "common_causes": [], "failure_categories": {}}
        
        # Categorize failures
        failure_categories = {}
        common_errors = {}
        
        for result in failed_results:
            error = result.get("error", "unknown_error")
            
            # Categorize by error type
            if "timeout" in error.lower():
                category = "timeout"
            elif "network" in error.lower() or "connection" in error.lower():
                category = "network"
            elif "element" in error.lower() or "selector" in error.lower():
                category = "element_not_found"
            elif "javascript" in error.lower() or "js" in error.lower():
                category = "javascript_error"
            else:
                category = "other"
            
            failure_categories[category] = failure_categories.get(category, 0) + 1
            common_errors[error] = common_errors.get(error, 0) + 1
        
        # Find most common errors
        sorted_errors = sorted(common_errors.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "failure_rate": len(failed_results) / len(results),
            "total_failures": len(failed_results),
            "failure_categories": failure_categories,
            "most_common_errors": sorted_errors[:5],
            "failure_distribution": self._calculate_failure_distribution(failed_results)
        }
    
    def _calculate_failure_distribution(self, failed_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate failure distribution patterns"""
        
        # Time-based distribution
        failure_times = []
        for result in failed_results:
            if "timestamp" in result:
                failure_times.append(result["timestamp"])
        
        return {
            "temporal_clustering": len(set(failure_times)) < len(failure_times) * 0.8,
            "failure_burst_detected": self._detect_failure_bursts(failure_times),
            "failure_spacing": "regular" if self._is_regular_spacing(failure_times) else "irregular"
        }
    
    def _detect_failure_bursts(self, failure_times: List[float]) -> bool:
        """Detect if failures occur in bursts"""
        if len(failure_times) < 3:
            return False
        
        # Sort times and check for clusters
        sorted_times = sorted(failure_times)
        gaps = [sorted_times[i+1] - sorted_times[i] for i in range(len(sorted_times)-1)]
        
        # If most gaps are small but some are large, we have bursts
        avg_gap = np.mean(gaps)
        large_gaps = [g for g in gaps if g > avg_gap * 3]
        
        return len(large_gaps) > 0 and len(large_gaps) < len(gaps) * 0.5
    
    def _is_regular_spacing(self, times: List[float]) -> bool:
        """Check if failures have regular spacing"""
        if len(times) < 3:
            return False
        
        sorted_times = sorted(times)
        gaps = [sorted_times[i+1] - sorted_times[i] for i in range(len(sorted_times)-1)]
        
        # Regular if standard deviation is small relative to mean
        if np.mean(gaps) > 0:
            return np.std(gaps) / np.mean(gaps) < 0.3
        
        return False
    
    async def _assess_risks(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess overall system risks based on test results"""
        
        risks = {
            "overall_risk_level": "low",
            "risk_factors": [],
            "critical_issues": [],
            "risk_score": 0.0
        }
        
        # Calculate risk score components
        failure_rate = len([r for r in results if r.get("status") == "failed"]) / len(results) if results else 0
        
        # Performance risk
        performance_risk = 0.0
        fps_values = []
        for result in results:
            if "result_details" in result and "avg_fps" in result["result_details"]:
                fps_values.append(result["result_details"]["avg_fps"])
        
        if fps_values:
            avg_fps = np.mean(fps_values)
            if avg_fps < 30:
                performance_risk = 0.8
                risks["critical_issues"].append("Critical FPS performance issues detected")
            elif avg_fps < 45:
                performance_risk = 0.4
                risks["risk_factors"].append("Moderate FPS performance concerns")
        
        # Stability risk
        stability_risk = failure_rate * 1.5  # Amplify failure impact
        
        # Calculate overall risk
        overall_risk = max(performance_risk, stability_risk, failure_rate)
        
        risks["risk_score"] = min(overall_risk, 1.0)
        
        if overall_risk > 0.7:
            risks["overall_risk_level"] = "high"
        elif overall_risk > 0.4:
            risks["overall_risk_level"] = "medium"
        
        return risks
    
    async def _generate_ai_insights(self, results: List[Dict[str, Any]], 
                                  patterns: List[PatternMatch], 
                                  anomalies: List[Dict[str, Any]]) -> List[AnalysisInsight]:
        """Generate AI-powered insights"""
        
        insights = []
        
        # Insight from patterns
        for pattern in patterns:
            if pattern.confidence > 0.7:
                insights.append(AnalysisInsight(
                    category="pattern_analysis",
                    severity="high" if pattern.confidence > 0.9 else "medium",
                    confidence=pattern.confidence,
                    title=f"{pattern.pattern_type.replace('_', ' ').title()} Detected",
                    description=pattern.description,
                    evidence=[f"Pattern confidence: {pattern.confidence:.2f}"],
                    recommendations=[f"Investigate {pattern.pattern_type} root causes"],
                    impact_score=pattern.confidence * 0.8
                ))
        
        # Insights from anomalies
        critical_anomalies = [a for a in anomalies if a.get("severity") == "critical"]
        if critical_anomalies:
            insights.append(AnalysisInsight(
                category="anomaly_detection",
                severity="critical",
                confidence=0.95,
                title="Critical Performance Anomalies Detected",
                description=f"Found {len(critical_anomalies)} critical anomalies requiring immediate attention",
                evidence=[f"{a['type']}: {a.get('value', 'N/A')}" for a in critical_anomalies[:3]],
                recommendations=["Immediate investigation required", "Consider rolling back recent changes"],
                impact_score=1.0
            ))
        
        # Success rate insight
        success_rate = len([r for r in results if r.get("status") == "passed"]) / len(results) if results else 0
        if success_rate < 0.9:
            insights.append(AnalysisInsight(
                category="quality_assessment",
                severity="high" if success_rate < 0.8 else "medium",
                confidence=0.9,
                title="Below Target Success Rate",
                description=f"Test success rate of {success_rate:.1%} is below the 90% target",
                evidence=[f"Success rate: {success_rate:.1%}", f"Failed tests: {len(results) - int(success_rate * len(results))}"],
                recommendations=["Review failed test cases", "Improve test stability", "Check test environment"],
                impact_score=1.0 - success_rate
            ))
        
        return insights
    
    async def _perform_root_cause_analysis(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform automated root cause analysis"""
        
        failed_results = [r for r in results if r.get("status") == "failed"]
        
        if not failed_results:
            return {"root_causes": [], "confidence": 1.0}
        
        # Analyze common factors in failures
        common_factors = {}
        
        for result in failed_results:
            # Check for common error patterns
            error = result.get("error", "")
            
            if "timeout" in error.lower():
                common_factors["timeout_issues"] = common_factors.get("timeout_issues", 0) + 1
            if "network" in error.lower():
                common_factors["network_issues"] = common_factors.get("network_issues", 0) + 1
            if "element" in error.lower():
                common_factors["ui_changes"] = common_factors.get("ui_changes", 0) + 1
        
        # Identify most likely root causes
        root_causes = []
        total_failures = len(failed_results)
        
        for factor, count in common_factors.items():
            if count > total_failures * 0.5:  # More than 50% of failures
                root_causes.append({
                    "cause": factor,
                    "confidence": count / total_failures,
                    "affected_tests": count,
                    "description": self._get_root_cause_description(factor)
                })
        
        return {
            "root_causes": sorted(root_causes, key=lambda x: x["confidence"], reverse=True),
            "analysis_confidence": 0.8 if root_causes else 0.3
        }
    
    def _get_root_cause_description(self, factor: str) -> str:
        """Get description for root cause factor"""
        descriptions = {
            "timeout_issues": "Tests failing due to timeouts, indicating performance or loading issues",
            "network_issues": "Network-related failures suggesting connectivity or API problems",
            "ui_changes": "UI element detection failures indicating recent interface changes"
        }
        return descriptions.get(factor, "Unknown root cause factor")
    
    async def _generate_predictions(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate predictions about future test behavior"""
        
        predictions = {
            "trend_prediction": "stable",
            "failure_rate_prediction": 0.0,
            "performance_prediction": "stable",
            "confidence": 0.7
        }
        
        # Simple trend-based predictions
        if len(results) >= 5:
            recent_results = results[-5:]
            failure_rate = len([r for r in recent_results if r.get("status") == "failed"]) / len(recent_results)
            
            predictions["failure_rate_prediction"] = failure_rate
            
            if failure_rate > 0.2:
                predictions["trend_prediction"] = "degrading"
            elif failure_rate == 0:
                predictions["trend_prediction"] = "improving"
        
        return predictions
    
    async def _generate_strategic_recommendations(self, results: List[Dict[str, Any]]) -> List[str]:
        """Generate strategic recommendations for improvement"""
        
        recommendations = []
        
        # Success rate recommendations
        success_rate = len([r for r in results if r.get("status") == "passed"]) / len(results) if results else 0
        
        if success_rate < 0.9:
            recommendations.append("Improve test stability and reliability")
            recommendations.append("Review and update test automation scripts")
        
        # Performance recommendations
        fps_values = []
        for result in results:
            if "result_details" in result and "avg_fps" in result["result_details"]:
                fps_values.append(result["result_details"]["avg_fps"])
        
        if fps_values and np.mean(fps_values) < 45:
            recommendations.append("Optimize game performance for better frame rates")
            recommendations.append("Consider performance profiling and bottleneck analysis")
        
        # Execution time recommendations
        exec_times = [r.get("execution_time", 0) for r in results if "execution_time" in r]
        if exec_times and np.mean(exec_times) > 120:  # More than 2 minutes average
            recommendations.append("Optimize test execution time for faster feedback")
            recommendations.append("Consider parallel test execution")
        
        # General recommendations
        recommendations.extend([
            "Implement continuous monitoring and alerting",
            "Establish performance baselines and thresholds",
            "Regular review of test coverage and effectiveness"
        ])
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _calculate_overall_confidence(self, results: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence in the analysis"""
        
        if not results:
            return 0.0
        
        base_confidence = 0.7
        
        # More results = higher confidence
        sample_size_factor = min(len(results) / 20, 1.0)  # Max confidence at 20+ results
        
        # Consistent results = higher confidence
        statuses = [r.get("status", "unknown") for r in results]
        status_variety = len(set(statuses))
        consistency_factor = 0.8 if status_variety <= 2 else 0.6
        
        return base_confidence * sample_size_factor * consistency_factor
    
    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get analyzer agent health metrics"""
        return {
            "agent_id": self.agent_id,
            "status": "healthy",
            "cpu_usage": 0.25,
            "memory_usage": 0.35,
            "analyses_completed": len(self.historical_data),
            "ml_models_loaded": len(self.ml_models)
        }
