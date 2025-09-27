"""
Performance Analysis Agent
Advanced Performance Monitoring & Optimization Analysis
"""

import asyncio
import json
import time
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import structlog
import numpy as np

from src.core.config import get_settings


@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    name: str
    value: float
    unit: str
    timestamp: float
    threshold: Optional[float]
    status: str  # ok, warning, critical


@dataclass
class PerformanceBottleneck:
    """Identified performance bottleneck"""
    component: str
    severity: str
    impact: float
    description: str
    recommendations: List[str]
    metrics: List[PerformanceMetric]


class PerformanceAgent:
    """Advanced performance analysis and monitoring agent"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.settings = get_settings()
        self.logger = structlog.get_logger(__name__)
        
        # Performance thresholds
        self.thresholds = {
            "fps": {"warning": 45, "critical": 30},
            "frame_time": {"warning": 22, "critical": 33},  # ms (1000/fps)
            "memory": {"warning": 500_000_000, "critical": 1_000_000_000},  # bytes
            "load_time": {"warning": 3.0, "critical": 5.0},  # seconds
            "response_time": {"warning": 100, "critical": 200},  # ms
            "cpu_usage": {"warning": 70, "critical": 90},  # percentage
            "network_latency": {"warning": 100, "critical": 300}  # ms
        }
        
        # Performance baselines (learned from historical data)
        self.baselines = {}
        
        # Performance tracking
        self.performance_history = []
        self.bottleneck_patterns = {}
    
    async def initialize(self) -> None:
        """Initialize performance monitoring agent"""
        try:
            await self._load_performance_baselines()
            self.logger.info(f"Performance agent {self.agent_id} initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize performance agent: {e}")
            raise
    
    async def analyze_performance(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive performance analysis"""
        
        try:
            self.logger.info(f"Analyzing performance data from {len(test_results)} tests")
            
            # Extract performance metrics
            metrics = await self._extract_performance_metrics(test_results)
            
            # Analyze frame rate performance
            fps_analysis = await self._analyze_fps_performance(test_results)
            
            # Analyze memory performance
            memory_analysis = await self._analyze_memory_performance(test_results)
            
            # Analyze loading performance
            loading_analysis = await self._analyze_loading_performance(test_results)
            
            # Identify bottlenecks
            bottlenecks = await self._identify_bottlenecks(test_results, metrics)
            
            # Performance trend analysis
            trends = await self._analyze_performance_trends(test_results)
            
            # Generate performance score
            performance_score = await self._calculate_performance_score(metrics)
            
            # Optimization recommendations
            recommendations = await self._generate_optimization_recommendations(
                bottlenecks, trends, performance_score
            )
            
            # Regression analysis
            regression_analysis = await self._detect_performance_regressions(test_results)
            
            analysis = {
                "agent_id": self.agent_id,
                "analysis_timestamp": time.time(),
                "performance_score": performance_score,
                "overall_status": self._determine_overall_status(performance_score),
                "metrics_summary": {
                    "total_metrics": len(metrics),
                    "critical_issues": len([m for m in metrics if m.status == "critical"]),
                    "warnings": len([m for m in metrics if m.status == "warning"])
                },
                "fps_analysis": fps_analysis,
                "memory_analysis": memory_analysis,
                "loading_analysis": loading_analysis,
                "bottlenecks": [b.__dict__ for b in bottlenecks],
                "performance_trends": trends,
                "regression_analysis": regression_analysis,
                "optimization_recommendations": recommendations,
                "detailed_metrics": [m.__dict__ for m in metrics]
            }
            
            # Store for trend analysis
            self.performance_history.append(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Performance analysis failed: {e}")
            raise
    
    async def _extract_performance_metrics(self, results: List[Dict[str, Any]]) -> List[PerformanceMetric]:
        """Extract performance metrics from test results"""
        
        metrics = []
        current_time = time.time()
        
        for result in results:
            if "result_details" not in result:
                continue
            
            details = result["result_details"]
            test_id = result.get("test_id", "unknown")
            
            # FPS metrics
            if "avg_fps" in details:
                fps = details["avg_fps"]
                status = self._evaluate_metric_status(fps, self.thresholds["fps"], reverse=True)
                
                metrics.append(PerformanceMetric(
                    name=f"fps_{test_id}",
                    value=fps,
                    unit="fps",
                    timestamp=current_time,
                    threshold=self.thresholds["fps"]["warning"],
                    status=status
                ))
            
            # Memory metrics
            if "memory_used" in details:
                memory = details["memory_used"]
                status = self._evaluate_metric_status(memory, self.thresholds["memory"])
                
                metrics.append(PerformanceMetric(
                    name=f"memory_{test_id}",
                    value=memory,
                    unit="bytes",
                    timestamp=current_time,
                    threshold=self.thresholds["memory"]["warning"],
                    status=status
                ))
            
            # Load time metrics
            if "load_time" in details:
                load_time = details["load_time"]
                status = self._evaluate_metric_status(load_time, self.thresholds["load_time"])
                
                metrics.append(PerformanceMetric(
                    name=f"load_time_{test_id}",
                    value=load_time,
                    unit="seconds",
                    timestamp=current_time,
                    threshold=self.thresholds["load_time"]["warning"],
                    status=status
                ))
        
        return metrics
    
    def _evaluate_metric_status(self, value: float, thresholds: Dict[str, float], reverse: bool = False) -> str:
        """Evaluate metric status against thresholds"""
        
        if reverse:  # For metrics where higher is better (like FPS)
            if value < thresholds["critical"]:
                return "critical"
            elif value < thresholds["warning"]:
                return "warning"
            else:
                return "ok"
        else:  # For metrics where lower is better (like load time)
            if value > thresholds["critical"]:
                return "critical"
            elif value > thresholds["warning"]:
                return "warning"
            else:
                return "ok"
    
    async def _analyze_fps_performance(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detailed FPS performance analysis"""
        
        fps_data = []
        min_fps_data = []
        
        for result in results:
            if "result_details" in result:
                details = result["result_details"]
                if "avg_fps" in details:
                    fps_data.append(details["avg_fps"])
                if "min_fps" in details:
                    min_fps_data.append(details["min_fps"])
        
        if not fps_data:
            return {"status": "no_data", "message": "No FPS data available"}
        
        # Statistical analysis
        avg_fps = statistics.mean(fps_data)
        median_fps = statistics.median(fps_data)
        std_fps = statistics.stdev(fps_data) if len(fps_data) > 1 else 0
        min_fps = min(fps_data)
        max_fps = max(fps_data)
        
        # Frame time analysis (1000ms / fps)
        frame_times = [1000 / fps if fps > 0 else 1000 for fps in fps_data]
        avg_frame_time = statistics.mean(frame_times)
        
        # Performance consistency (lower std = more consistent)
        consistency_score = max(0, 1 - (std_fps / avg_fps)) if avg_fps > 0 else 0
        
        # FPS stability analysis
        stable_fps_threshold = 5  # FPS variation threshold
        fps_drops = len([fps for fps in fps_data if fps < avg_fps - stable_fps_threshold])
        stability_score = max(0, 1 - (fps_drops / len(fps_data)))
        
        return {
            "average_fps": avg_fps,
            "median_fps": median_fps,
            "min_fps": min_fps,
            "max_fps": max_fps,
            "fps_standard_deviation": std_fps,
            "average_frame_time": avg_frame_time,
            "consistency_score": consistency_score,
            "stability_score": stability_score,
            "fps_drops_count": fps_drops,
            "performance_rating": self._rate_fps_performance(avg_fps, consistency_score),
            "target_fps": self.settings.target_fps,
            "meets_target": avg_fps >= self.settings.target_fps * 0.9  # 90% of target
        }
    
    def _rate_fps_performance(self, avg_fps: float, consistency: float) -> str:
        """Rate FPS performance"""
        
        if avg_fps >= 55 and consistency >= 0.8:
            return "excellent"
        elif avg_fps >= 45 and consistency >= 0.7:
            return "good"
        elif avg_fps >= 30 and consistency >= 0.6:
            return "acceptable"
        elif avg_fps >= 20:
            return "poor"
        else:
            return "unacceptable"
    
    async def _analyze_memory_performance(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detailed memory performance analysis"""
        
        memory_data = []
        
        for result in results:
            if "result_details" in result and "memory_used" in result["result_details"]:
                memory_data.append(result["result_details"]["memory_used"])
        
        if not memory_data:
            return {"status": "no_data", "message": "No memory data available"}
        
        # Convert to MB for readability
        memory_mb = [mem / 1024 / 1024 for mem in memory_data]
        
        avg_memory = statistics.mean(memory_mb)
        max_memory = max(memory_mb)
        min_memory = min(memory_mb)
        
        # Memory growth analysis
        memory_growth = max_memory - min_memory if len(memory_mb) > 1 else 0
        growth_rate = memory_growth / len(memory_mb) if len(memory_mb) > 0 else 0
        
        # Memory leak detection (continuous growth)
        potential_leak = False
        if len(memory_mb) >= 5:
            # Check if memory consistently increases
            increases = 0
            for i in range(1, len(memory_mb)):
                if memory_mb[i] > memory_mb[i-1]:
                    increases += 1
            
            # If more than 70% of measurements show increase, potential leak
            potential_leak = increases > len(memory_mb) * 0.7
        
        return {
            "average_memory_mb": avg_memory,
            "max_memory_mb": max_memory,
            "min_memory_mb": min_memory,
            "memory_growth_mb": memory_growth,
            "growth_rate_mb_per_test": growth_rate,
            "potential_memory_leak": potential_leak,
            "memory_efficiency": self._rate_memory_efficiency(avg_memory),
            "peak_memory_concern": max_memory > 512  # More than 512MB
        }
    
    def _rate_memory_efficiency(self, avg_memory_mb: float) -> str:
        """Rate memory efficiency"""
        
        if avg_memory_mb < 100:
            return "excellent"
        elif avg_memory_mb < 250:
            return "good"
        elif avg_memory_mb < 500:
            return "acceptable"
        elif avg_memory_mb < 1000:
            return "concerning"
        else:
            return "critical"
    
    async def _analyze_loading_performance(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze loading and initialization performance"""
        
        load_times = []
        
        for result in results:
            if "result_details" in result and "load_time" in result["result_details"]:
                load_times.append(result["result_details"]["load_time"])
        
        if not load_times:
            return {"status": "no_data", "message": "No loading time data available"}
        
        avg_load_time = statistics.mean(load_times)
        median_load_time = statistics.median(load_times)
        max_load_time = max(load_times)
        min_load_time = min(load_times)
        
        # Loading consistency
        std_load_time = statistics.stdev(load_times) if len(load_times) > 1 else 0
        consistency = max(0, 1 - (std_load_time / avg_load_time)) if avg_load_time > 0 else 0
        
        return {
            "average_load_time": avg_load_time,
            "median_load_time": median_load_time,
            "max_load_time": max_load_time,
            "min_load_time": min_load_time,
            "load_time_consistency": consistency,
            "loading_rating": self._rate_loading_performance(avg_load_time),
            "meets_target": avg_load_time <= 3.0  # 3 second target
        }
    
    def _rate_loading_performance(self, avg_load_time: float) -> str:
        """Rate loading performance"""
        
        if avg_load_time < 1.0:
            return "excellent"
        elif avg_load_time < 2.0:
            return "good"
        elif avg_load_time < 3.0:
            return "acceptable"
        elif avg_load_time < 5.0:
            return "poor"
        else:
            return "unacceptable"
    
    async def _identify_bottlenecks(self, results: List[Dict[str, Any]], 
                                   metrics: List[PerformanceMetric]) -> List[PerformanceBottleneck]:
        """Identify performance bottlenecks"""
        
        bottlenecks = []
        
        # FPS bottleneck detection
        fps_metrics = [m for m in metrics if "fps" in m.name and m.status in ["warning", "critical"]]
        if len(fps_metrics) > len(metrics) * 0.3:  # More than 30% of tests have FPS issues
            severity = "critical" if any(m.status == "critical" for m in fps_metrics) else "high"
            
            bottlenecks.append(PerformanceBottleneck(
                component="rendering",
                severity=severity,
                impact=len(fps_metrics) / len(metrics),
                description="Frame rate performance below acceptable thresholds",
                recommendations=[
                    "Optimize rendering pipeline",
                    "Reduce visual complexity",
                    "Check for GPU bottlenecks",
                    "Profile rendering performance"
                ],
                metrics=fps_metrics
            ))
        
        # Memory bottleneck detection
        memory_metrics = [m for m in metrics if "memory" in m.name and m.status in ["warning", "critical"]]
        if memory_metrics:
            avg_memory = statistics.mean([m.value for m in memory_metrics])
            
            if avg_memory > 500_000_000:  # > 500MB
                bottlenecks.append(PerformanceBottleneck(
                    component="memory",
                    severity="high" if avg_memory > 1_000_000_000 else "medium",
                    impact=len(memory_metrics) / len(metrics),
                    description=f"High memory usage detected (avg: {avg_memory/1024/1024:.1f}MB)",
                    recommendations=[
                        "Investigate memory leaks",
                        "Optimize asset loading",
                        "Implement object pooling",
                        "Review memory allocation patterns"
                    ],
                    metrics=memory_metrics
                ))
        
        # Loading time bottleneck detection
        load_metrics = [m for m in metrics if "load_time" in m.name and m.status in ["warning", "critical"]]
        if load_metrics:
            avg_load_time = statistics.mean([m.value for m in load_metrics])
            
            bottlenecks.append(PerformanceBottleneck(
                component="loading",
                severity="medium",
                impact=len(load_metrics) / len(metrics),
                description=f"Slow loading times detected (avg: {avg_load_time:.2f}s)",
                recommendations=[
                    "Optimize asset compression",
                    "Implement progressive loading",
                    "Use content delivery network",
                    "Minimize initial payload size"
                ],
                metrics=load_metrics
            ))
        
        return bottlenecks
    
    async def _analyze_performance_trends(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        
        if len(results) < 3:
            return {"status": "insufficient_data"}
        
        # Extract time-series data
        fps_trend = []
        memory_trend = []
        load_time_trend = []
        
        for i, result in enumerate(results):
            if "result_details" in result:
                details = result["result_details"]
                
                if "avg_fps" in details:
                    fps_trend.append((i, details["avg_fps"]))
                if "memory_used" in details:
                    memory_trend.append((i, details["memory_used"]))
                if "load_time" in details:
                    load_time_trend.append((i, details["load_time"]))
        
        trends = {}
        
        # Analyze FPS trend
        if len(fps_trend) >= 3:
            trends["fps"] = self._calculate_trend(fps_trend)
        
        # Analyze memory trend
        if len(memory_trend) >= 3:
            trends["memory"] = self._calculate_trend(memory_trend)
        
        # Analyze load time trend
        if len(load_time_trend) >= 3:
            trends["load_time"] = self._calculate_trend(load_time_trend)
        
        return trends
    
    def _calculate_trend(self, data_points: List[Tuple[int, float]]) -> Dict[str, Any]:
        """Calculate trend direction and strength"""
        
        if len(data_points) < 2:
            return {"direction": "unknown", "strength": 0.0}
        
        # Simple linear regression
        n = len(data_points)
        sum_x = sum(point[0] for point in data_points)
        sum_y = sum(point[1] for point in data_points)
        sum_xy = sum(point[0] * point[1] for point in data_points)
        sum_x_sq = sum(point[0] ** 2 for point in data_points)
        
        # Calculate slope
        denominator = n * sum_x_sq - sum_x ** 2
        if denominator == 0:
            return {"direction": "stable", "strength": 0.0}
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        
        # Determine trend direction and strength
        if abs(slope) < 0.01:
            direction = "stable"
        elif slope > 0:
            direction = "increasing"
        else:
            direction = "decreasing"
        
        # Strength is absolute value of slope normalized
        strength = min(abs(slope), 1.0)
        
        return {
            "direction": direction,
            "strength": strength,
            "slope": slope,
            "confidence": min(len(data_points) / 10, 1.0)  # More data points = higher confidence
        }
    
    async def _calculate_performance_score(self, metrics: List[PerformanceMetric]) -> float:
        """Calculate overall performance score (0-100)"""
        
        if not metrics:
            return 0.0
        
        # Weight different metric types
        weights = {"fps": 0.4, "memory": 0.3, "load_time": 0.3}
        
        scores = {}
        
        for metric_type, weight in weights.items():
            type_metrics = [m for m in metrics if metric_type in m.name]
            
            if type_metrics:
                # Calculate score for this metric type
                ok_count = len([m for m in type_metrics if m.status == "ok"])
                warning_count = len([m for m in type_metrics if m.status == "warning"])
                critical_count = len([m for m in type_metrics if m.status == "critical"])
                
                # Score: OK=100, Warning=50, Critical=0
                type_score = (ok_count * 100 + warning_count * 50) / len(type_metrics)
                scores[metric_type] = type_score * weight
        
        # Calculate weighted average
        total_score = sum(scores.values())
        max_possible_score = sum(weights.values()) * 100
        
        return total_score / max_possible_score * 100 if max_possible_score > 0 else 0
    
    def _determine_overall_status(self, performance_score: float) -> str:
        """Determine overall performance status"""
        
        if performance_score >= 90:
            return "excellent"
        elif performance_score >= 75:
            return "good"
        elif performance_score >= 60:
            return "acceptable"
        elif performance_score >= 40:
            return "poor"
        else:
            return "critical"
    
    async def _generate_optimization_recommendations(self, 
                                                   bottlenecks: List[PerformanceBottleneck],
                                                   trends: Dict[str, Any],
                                                   performance_score: float) -> List[str]:
        """Generate optimization recommendations"""
        
        recommendations = []
        
        # Recommendations based on bottlenecks
        for bottleneck in bottlenecks:
            recommendations.extend(bottleneck.recommendations[:2])  # Top 2 per bottleneck
        
        # Recommendations based on trends
        for metric_type, trend in trends.items():
            if trend.get("direction") == "decreasing" and trend.get("strength", 0) > 0.5:
                if metric_type == "fps":
                    recommendations.append("FPS is declining - investigate rendering optimizations")
                elif metric_type == "memory":
                    recommendations.append("Memory usage is decreasing - good optimization trend")
                elif metric_type == "load_time":
                    recommendations.append("Load times are improving - continue optimization efforts")
        
        # General recommendations based on performance score
        if performance_score < 60:
            recommendations.extend([
                "Conduct comprehensive performance audit",
                "Implement performance monitoring dashboard",
                "Establish performance regression testing"
            ])
        elif performance_score < 80:
            recommendations.extend([
                "Focus on identified bottlenecks",
                "Implement performance budgets",
                "Regular performance reviews"
            ])
        
        # Remove duplicates and limit
        return list(dict.fromkeys(recommendations))[:10]
    
    async def _detect_performance_regressions(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect performance regressions compared to baseline"""
        
        regressions = {
            "detected": False,
            "regression_points": [],
            "severity": "none"
        }
        
        if not self.baselines or len(results) < 5:
            return regressions
        
        # Check for significant deviations from baseline
        for result in results:
            if "result_details" not in result:
                continue
            
            details = result["result_details"]
            
            # Check FPS regression
            if "avg_fps" in details and "fps" in self.baselines:
                baseline_fps = self.baselines["fps"]
                current_fps = details["avg_fps"]
                
                # Regression if 15% below baseline
                if current_fps < baseline_fps * 0.85:
                    regressions["detected"] = True
                    regressions["regression_points"].append({
                        "metric": "fps",
                        "baseline": baseline_fps,
                        "current": current_fps,
                        "regression_percentage": ((baseline_fps - current_fps) / baseline_fps) * 100
                    })
        
        if regressions["detected"]:
            # Determine severity based on worst regression
            max_regression = max([rp["regression_percentage"] for rp in regressions["regression_points"]])
            
            if max_regression > 30:
                regressions["severity"] = "critical"
            elif max_regression > 15:
                regressions["severity"] = "high"
            else:
                regressions["severity"] = "medium"
        
        return regressions
    
    async def _load_performance_baselines(self) -> None:
        """Load performance baselines from historical data"""
        
        # In production, this would load from database
        # For now, use default baselines
        self.baselines = {
            "fps": 60.0,
            "memory": 256_000_000,  # 256MB
            "load_time": 2.0
        }
    
    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get performance agent health metrics"""
        return {
            "agent_id": self.agent_id,
            "status": "healthy",
            "cpu_usage": 0.20,
            "memory_usage": 0.30,
            "analyses_completed": len(self.performance_history),
            "baselines_loaded": len(self.baselines)
        }
