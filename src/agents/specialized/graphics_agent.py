"""
Advanced Graphics Analysis Agent
Visual Testing, Rendering Analysis & Graphics Performance
"""

import asyncio
import json
import base64
import cv2
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import structlog
from PIL import Image, ImageChops, ImageStat
import io

from src.core.config import get_settings


@dataclass
class VisualDifference:
    """Visual difference detection result"""
    difference_percentage: float
    affected_regions: List[Tuple[int, int, int, int]]  # x, y, width, height
    severity: str
    description: str


@dataclass
class RenderingIssue:
    """Rendering issue detection"""
    issue_type: str
    severity: str
    location: Tuple[int, int]
    description: str
    evidence: str


class GraphicsAgent:
    """Advanced graphics and visual testing agent"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.settings = get_settings()
        self.logger = structlog.get_logger(__name__)
        
        # Visual analysis thresholds
        self.visual_thresholds = {
            "pixel_difference": 0.05,  # 5% pixel difference threshold
            "color_tolerance": 10,     # RGB color tolerance
            "blur_threshold": 100,     # Blur detection threshold
            "brightness_range": (50, 200),  # Acceptable brightness range
            "contrast_min": 50         # Minimum contrast requirement
        }
        
        # Reference images for comparison
        self.reference_images = {}
        
        # Graphics performance baselines
        self.performance_baselines = {
            "render_time": 16.67,  # 60 FPS = 16.67ms per frame
            "memory_usage": 256,   # MB
            "gpu_utilization": 70  # %
        }
    
    async def initialize(self) -> None:
        """Initialize graphics analysis agent"""
        try:
            await self._load_reference_images()
            self.logger.info(f"Graphics agent {self.agent_id} initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize graphics agent: {e}")
            raise
    
    async def analyze_graphics(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive graphics analysis"""
        
        try:
            self.logger.info(f"Analyzing graphics data from {len(test_results)} tests")
            
            # Visual comparison analysis
            visual_analysis = await self._perform_visual_analysis(test_results)
            
            # Rendering performance analysis
            rendering_analysis = await self._analyze_rendering_performance(test_results)
            
            # Color accuracy analysis
            color_analysis = await self._analyze_color_accuracy(test_results)
            
            # Visual quality assessment
            quality_analysis = await self._assess_visual_quality(test_results)
            
            # Animation and smoothness analysis
            animation_analysis = await self._analyze_animations(test_results)
            
            # Cross-platform visual consistency
            consistency_analysis = await self._analyze_visual_consistency(test_results)
            
            # Graphics error detection
            error_detection = await self._detect_graphics_errors(test_results)
            
            # Performance impact analysis
            performance_impact = await self._analyze_performance_impact(test_results)
            
            # Generate graphics score
            graphics_score = await self._calculate_graphics_score(
                visual_analysis, rendering_analysis, quality_analysis
            )
            
            analysis = {
                "agent_id": self.agent_id,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "graphics_score": graphics_score,
                "overall_rating": self._determine_graphics_rating(graphics_score),
                "visual_analysis": visual_analysis,
                "rendering_analysis": rendering_analysis,
                "color_analysis": color_analysis,
                "quality_analysis": quality_analysis,
                "animation_analysis": animation_analysis,
                "consistency_analysis": consistency_analysis,
                "error_detection": error_detection,
                "performance_impact": performance_impact,
                "recommendations": await self._generate_graphics_recommendations(
                    visual_analysis, rendering_analysis, quality_analysis
                )
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Graphics analysis failed: {e}")
            raise
    
    async def _perform_visual_analysis(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive visual analysis"""
        
        visual_issues = []
        screenshot_analyses = []
        
        for i, result in enumerate(results):
            if "artifacts" in result and "screenshot" in result["artifacts"]:
                try:
                    # Decode screenshot
                    screenshot_data = base64.b64decode(result["artifacts"]["screenshot"])
                    image = Image.open(io.BytesIO(screenshot_data))
                    
                    # Convert to numpy array for analysis
                    img_array = np.array(image)
                    
                    # Visual quality analysis
                    analysis = await self._analyze_single_image(img_array, f"test_{i}")
                    screenshot_analyses.append(analysis)
                    
                    # Check for visual artifacts
                    artifacts = await self._detect_visual_artifacts(img_array)
                    if artifacts:
                        visual_issues.extend(artifacts)
                    
                except Exception as e:
                    self.logger.error(f"Failed to analyze screenshot {i}: {e}")
        
        return {
            "screenshots_analyzed": len(screenshot_analyses),
            "visual_issues_found": len(visual_issues),
            "visual_issues": visual_issues,
            "screenshot_analyses": screenshot_analyses,
            "average_visual_quality": np.mean([a["quality_score"] for a in screenshot_analyses]) if screenshot_analyses else 0
        }
    
    async def _analyze_single_image(self, image: np.ndarray, image_id: str) -> Dict[str, Any]:
        """Analyze a single image for quality metrics"""
        
        # Convert to different color spaces for analysis
        if len(image.shape) == 3:
            # Color image
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        else:
            gray = image
            hsv = None
        
        # Brightness analysis
        brightness = np.mean(gray)
        
        # Contrast analysis (standard deviation of pixel intensities)
        contrast = np.std(gray)
        
        # Blur detection using Laplacian variance
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        is_blurry = blur_score < self.visual_thresholds["blur_threshold"]
        
        # Edge detection for sharpness
        edges = cv2.Canny(gray, 50, 150)
        sharpness = np.sum(edges) / (edges.shape[0] * edges.shape[1])
        
        # Color distribution analysis (for color images)
        color_stats = {}
        if len(image.shape) == 3:
            for i, channel in enumerate(['R', 'G', 'B']):
                color_stats[channel] = {
                    'mean': np.mean(image[:, :, i]),
                    'std': np.std(image[:, :, i]),
                    'min': np.min(image[:, :, i]),
                    'max': np.max(image[:, :, i])
                }
        
        # Calculate quality score
        quality_score = self._calculate_image_quality_score(
            brightness, contrast, blur_score, sharpness
        )
        
        return {
            "image_id": image_id,
            "dimensions": image.shape,
            "brightness": brightness,
            "contrast": contrast,
            "blur_score": blur_score,
            "is_blurry": is_blurry,
            "sharpness": sharpness,
            "color_stats": color_stats,
            "quality_score": quality_score,
            "quality_rating": self._rate_image_quality(quality_score)
        }
    
    def _calculate_image_quality_score(self, brightness: float, contrast: float, 
                                     blur_score: float, sharpness: float) -> float:
        """Calculate overall image quality score"""
        
        # Normalize metrics to 0-1 range
        brightness_score = 1.0 - abs(brightness - 127.5) / 127.5  # Optimal around 127.5
        contrast_score = min(contrast / 50, 1.0)  # Good contrast > 50
        blur_score_norm = min(blur_score / 500, 1.0)  # Good if > 500
        sharpness_score = min(sharpness / 0.1, 1.0)  # Good if > 0.1
        
        # Weighted average
        quality_score = (
            brightness_score * 0.2 +
            contrast_score * 0.3 +
            blur_score_norm * 0.3 +
            sharpness_score * 0.2
        ) * 100
        
        return quality_score
    
    def _rate_image_quality(self, score: float) -> str:
        """Rate image quality based on score"""
        
        if score >= 85:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 55:
            return "acceptable"
        elif score >= 40:
            return "poor"
        else:
            return "very_poor"
    
    async def _detect_visual_artifacts(self, image: np.ndarray) -> List[RenderingIssue]:
        """Detect visual artifacts and rendering issues"""
        
        artifacts = []
        
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Detect potential tearing (horizontal lines of different brightness)
        horizontal_diff = np.diff(gray, axis=0)
        tearing_candidates = np.where(np.abs(horizontal_diff) > 50)
        
        if len(tearing_candidates[0]) > image.shape[0] * 0.1:  # More than 10% of rows
            artifacts.append(RenderingIssue(
                issue_type="screen_tearing",
                severity="medium",
                location=(0, 0),
                description="Potential screen tearing artifacts detected",
                evidence=f"High horizontal brightness differences in {len(tearing_candidates[0])} rows"
            ))
        
        # Detect color banding
        if len(image.shape) == 3:
            for channel in range(3):
                hist, bins = np.histogram(image[:, :, channel], bins=256, range=(0, 256))
                # Look for unnatural spikes in histogram
                peaks = np.where(hist > np.mean(hist) * 5)[0]
                if len(peaks) > 10:
                    artifacts.append(RenderingIssue(
                        issue_type="color_banding",
                        severity="low",
                        location=(0, 0),
                        description=f"Color banding detected in channel {channel}",
                        evidence=f"{len(peaks)} histogram spikes detected"
                    ))
        
        # Detect pixelation (blocky artifacts)
        # Use morphological operations to detect square patterns
        kernel = np.ones((8, 8), np.uint8)
        morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        diff = cv2.absdiff(gray, morphed)
        pixelation_score = np.mean(diff)
        
        if pixelation_score > 10:
            artifacts.append(RenderingIssue(
                issue_type="pixelation",
                severity="medium",
                location=(0, 0),
                description="Pixelation or blocky artifacts detected",
                evidence=f"Pixelation score: {pixelation_score:.2f}"
            ))
        
        return artifacts
    
    async def _analyze_rendering_performance(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze rendering performance"""
        
        render_times = []
        frame_rates = []
        memory_usage = []
        
        for result in results:
            if "result_details" in result:
                details = result["result_details"]
                
                if "avg_fps" in details:
                    frame_rates.append(details["avg_fps"])
                
                if "frame_time" in details:
                    render_times.append(details["frame_time"])
                
                if "memory_used" in details:
                    memory_usage.append(details["memory_used"] / 1024 / 1024)  # Convert to MB
        
        analysis = {
            "frame_rate_analysis": {},
            "render_time_analysis": {},
            "memory_analysis": {},
            "performance_rating": "unknown"
        }
        
        if frame_rates:
            analysis["frame_rate_analysis"] = {
                "average_fps": np.mean(frame_rates),
                "min_fps": np.min(frame_rates),
                "max_fps": np.max(frame_rates),
                "fps_stability": 1.0 - (np.std(frame_rates) / np.mean(frame_rates)) if np.mean(frame_rates) > 0 else 0,
                "meets_60fps_target": np.mean(frame_rates) >= 58,
                "frame_drops": len([fps for fps in frame_rates if fps < 30])
            }
        
        if render_times:
            analysis["render_time_analysis"] = {
                "average_render_time": np.mean(render_times),
                "p95_render_time": np.percentile(render_times, 95),
                "p99_render_time": np.percentile(render_times, 99),
                "render_time_consistency": 1.0 - (np.std(render_times) / np.mean(render_times)) if np.mean(render_times) > 0 else 0
            }
        
        if memory_usage:
            analysis["memory_analysis"] = {
                "average_memory_mb": np.mean(memory_usage),
                "peak_memory_mb": np.max(memory_usage),
                "memory_growth": np.max(memory_usage) - np.min(memory_usage) if len(memory_usage) > 1 else 0
            }
        
        # Overall performance rating
        if frame_rates:
            avg_fps = np.mean(frame_rates)
            if avg_fps >= 58:
                analysis["performance_rating"] = "excellent"
            elif avg_fps >= 45:
                analysis["performance_rating"] = "good"
            elif avg_fps >= 30:
                analysis["performance_rating"] = "acceptable"
            else:
                analysis["performance_rating"] = "poor"
        
        return analysis
    
    async def _analyze_color_accuracy(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze color accuracy and consistency"""
        
        color_analyses = []
        
        for i, result in enumerate(results):
            if "artifacts" in result and "screenshot" in result["artifacts"]:
                try:
                    screenshot_data = base64.b64decode(result["artifacts"]["screenshot"])
                    image = Image.open(io.BytesIO(screenshot_data))
                    
                    # Color space analysis
                    color_analysis = await self._analyze_color_properties(image)
                    color_analysis["test_id"] = f"test_{i}"
                    color_analyses.append(color_analysis)
                    
                except Exception as e:
                    self.logger.error(f"Color analysis failed for test {i}: {e}")
        
        if not color_analyses:
            return {"status": "no_data"}
        
        # Aggregate color statistics
        color_gamuts = [ca["color_gamut_coverage"] for ca in color_analyses if "color_gamut_coverage" in ca]
        color_temperatures = [ca["color_temperature"] for ca in color_analyses if "color_temperature" in ca]
        
        return {
            "color_analyses_count": len(color_analyses),
            "average_color_gamut": np.mean(color_gamuts) if color_gamuts else 0,
            "color_temperature_consistency": np.std(color_temperatures) if len(color_temperatures) > 1 else 0,
            "color_accuracy_score": np.mean([ca.get("accuracy_score", 50) for ca in color_analyses]),
            "detailed_analyses": color_analyses
        }
    
    async def _analyze_color_properties(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze color properties of an image"""
        
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        img_array = np.array(image)
        
        # Color statistics
        r_channel = img_array[:, :, 0]
        g_channel = img_array[:, :, 1]
        b_channel = img_array[:, :, 2]
        
        # Color balance analysis
        r_mean, g_mean, b_mean = np.mean(r_channel), np.mean(g_channel), np.mean(b_channel)
        color_balance = {
            "red_bias": r_mean - (g_mean + b_mean) / 2,
            "green_bias": g_mean - (r_mean + b_mean) / 2,
            "blue_bias": b_mean - (r_mean + g_mean) / 2
        }
        
        # Color temperature estimation (simplified)
        color_temperature = self._estimate_color_temperature(r_mean, g_mean, b_mean)
        
        # Color gamut coverage estimation
        unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
        max_colors = 256 ** 3
        color_gamut_coverage = unique_colors / max_colors * 100
        
        # Saturation analysis
        hsv_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        saturation = np.mean(hsv_array[:, :, 1])
        
        return {
            "color_balance": color_balance,
            "color_temperature": color_temperature,
            "color_gamut_coverage": color_gamut_coverage,
            "average_saturation": saturation,
            "unique_colors": unique_colors,
            "accuracy_score": self._calculate_color_accuracy_score(color_balance, saturation)
        }
    
    def _estimate_color_temperature(self, r: float, g: float, b: float) -> float:
        """Estimate color temperature (simplified method)"""
        
        # Simplified color temperature estimation
        # Warmer images have more red, cooler have more blue
        if r + g + b == 0:
            return 6500  # Default daylight
        
        red_ratio = r / (r + g + b)
        blue_ratio = b / (r + g + b)
        
        # Rough estimation: higher red = warmer (lower K), higher blue = cooler (higher K)
        temperature = 6500 + (blue_ratio - red_ratio) * 2000
        return max(2000, min(10000, temperature))
    
    def _calculate_color_accuracy_score(self, color_balance: Dict[str, float], saturation: float) -> float:
        """Calculate color accuracy score"""
        
        # Penalize extreme color biases
        max_bias = max(abs(bias) for bias in color_balance.values())
        bias_score = max(0, 100 - max_bias * 2)
        
        # Optimal saturation around 128 (50% of 255)
        saturation_score = max(0, 100 - abs(saturation - 128) * 0.5)
        
        return (bias_score * 0.6 + saturation_score * 0.4)
    
    async def _assess_visual_quality(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess overall visual quality"""
        
        quality_metrics = {
            "sharpness_scores": [],
            "contrast_scores": [],
            "brightness_scores": [],
            "overall_scores": []
        }
        
        for result in results:
            if "artifacts" in result and "screenshot" in result["artifacts"]:
                try:
                    screenshot_data = base64.b64decode(result["artifacts"]["screenshot"])
                    image = Image.open(io.BytesIO(screenshot_data))
                    img_array = np.array(image)
                    
                    # Calculate quality metrics
                    sharpness = self._calculate_sharpness(img_array)
                    contrast = self._calculate_contrast(img_array)
                    brightness = self._calculate_brightness(img_array)
                    
                    quality_metrics["sharpness_scores"].append(sharpness)
                    quality_metrics["contrast_scores"].append(contrast)
                    quality_metrics["brightness_scores"].append(brightness)
                    
                    overall = (sharpness + contrast + brightness) / 3
                    quality_metrics["overall_scores"].append(overall)
                    
                except Exception as e:
                    self.logger.error(f"Quality assessment failed: {e}")
        
        if not quality_metrics["overall_scores"]:
            return {"status": "no_data"}
        
        return {
            "average_sharpness": np.mean(quality_metrics["sharpness_scores"]),
            "average_contrast": np.mean(quality_metrics["contrast_scores"]),
            "average_brightness": np.mean(quality_metrics["brightness_scores"]),
            "overall_quality_score": np.mean(quality_metrics["overall_scores"]),
            "quality_consistency": 1.0 - np.std(quality_metrics["overall_scores"]) / 100,
            "quality_rating": self._rate_visual_quality(np.mean(quality_metrics["overall_scores"]))
        }
    
    def _calculate_sharpness(self, image: np.ndarray) -> float:
        """Calculate image sharpness score"""
        
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Laplacian variance method
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Normalize to 0-100 scale
        return min(100, laplacian_var / 10)
    
    def _calculate_contrast(self, image: np.ndarray) -> float:
        """Calculate image contrast score"""
        
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # RMS contrast
        rms_contrast = np.std(gray)
        
        # Normalize to 0-100 scale
        return min(100, rms_contrast / 2.55)
    
    def _calculate_brightness(self, image: np.ndarray) -> float:
        """Calculate image brightness score"""
        
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        mean_brightness = np.mean(gray)
        
        # Score based on how close to optimal brightness (127.5)
        brightness_score = 100 - abs(mean_brightness - 127.5) / 127.5 * 100
        
        return max(0, brightness_score)
    
    def _rate_visual_quality(self, score: float) -> str:
        """Rate visual quality based on score"""
        
        if score >= 80:
            return "excellent"
        elif score >= 65:
            return "good"
        elif score >= 50:
            return "acceptable"
        elif score >= 35:
            return "poor"
        else:
            return "very_poor"
    
    async def _analyze_animations(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze animation smoothness and quality"""
        
        animation_data = {
            "frame_consistency": [],
            "animation_smoothness": [],
            "frame_drops": 0
        }
        
        fps_data = []
        for result in results:
            if "result_details" in result and "avg_fps" in result["result_details"]:
                fps_data.append(result["result_details"]["avg_fps"])
        
        if fps_data:
            # Calculate frame consistency
            fps_std = np.std(fps_data)
            fps_mean = np.mean(fps_data)
            consistency = 1.0 - (fps_std / fps_mean) if fps_mean > 0 else 0
            
            # Count frame drops (FPS below 30)
            frame_drops = len([fps for fps in fps_data if fps < 30])
            
            # Animation smoothness based on FPS stability
            smoothness = min(100, fps_mean / 60 * 100) * consistency
            
            return {
                "average_fps": fps_mean,
                "fps_consistency": consistency,
                "animation_smoothness": smoothness,
                "frame_drops_count": frame_drops,
                "animation_rating": self._rate_animation_quality(smoothness, frame_drops)
            }
        
        return {"status": "no_animation_data"}
    
    def _rate_animation_quality(self, smoothness: float, frame_drops: int) -> str:
        """Rate animation quality"""
        
        if smoothness >= 90 and frame_drops == 0:
            return "excellent"
        elif smoothness >= 75 and frame_drops <= 1:
            return "good"
        elif smoothness >= 60 and frame_drops <= 3:
            return "acceptable"
        else:
            return "poor"
    
    async def _analyze_visual_consistency(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze visual consistency across tests"""
        
        if len(results) < 2:
            return {"status": "insufficient_data"}
        
        visual_variations = []
        
        # Compare consecutive screenshots for consistency
        for i in range(len(results) - 1):
            result1 = results[i]
            result2 = results[i + 1]
            
            if ("artifacts" in result1 and "screenshot" in result1["artifacts"] and
                "artifacts" in result2 and "screenshot" in result2["artifacts"]):
                
                try:
                    # Compare screenshots
                    img1_data = base64.b64decode(result1["artifacts"]["screenshot"])
                    img2_data = base64.b64decode(result2["artifacts"]["screenshot"])
                    
                    img1 = Image.open(io.BytesIO(img1_data))
                    img2 = Image.open(io.BytesIO(img2_data))
                    
                    # Calculate visual difference
                    difference = self._calculate_visual_difference(img1, img2)
                    visual_variations.append(difference)
                    
                except Exception as e:
                    self.logger.error(f"Visual consistency check failed: {e}")
        
        if visual_variations:
            avg_variation = np.mean(visual_variations)
            consistency_score = max(0, 100 - avg_variation * 10)
            
            return {
                "average_variation": avg_variation,
                "consistency_score": consistency_score,
                "consistency_rating": self._rate_visual_consistency(consistency_score),
                "variations_analyzed": len(visual_variations)
            }
        
        return {"status": "no_comparison_data"}
    
    def _calculate_visual_difference(self, img1: Image.Image, img2: Image.Image) -> float:
        """Calculate visual difference between two images"""
        
        # Ensure same size
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)
        
        # Convert to same mode
        if img1.mode != img2.mode:
            img2 = img2.convert(img1.mode)
        
        # Calculate difference
        diff = ImageChops.difference(img1, img2)
        stat = ImageStat.Stat(diff)
        
        # Average difference across all channels
        avg_diff = sum(stat.mean) / len(stat.mean)
        
        # Normalize to 0-1 scale (assuming 8-bit images)
        return avg_diff / 255.0
    
    def _rate_visual_consistency(self, score: float) -> str:
        """Rate visual consistency"""
        
        if score >= 95:
            return "excellent"
        elif score >= 85:
            return "good"
        elif score >= 70:
            return "acceptable"
        else:
            return "poor"
    
    async def _detect_graphics_errors(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect graphics-related errors"""
        
        graphics_errors = []
        
        for result in results:
            # Check for graphics-related errors in console logs
            if "artifacts" in result and "console_logs" in result["artifacts"]:
                for log in result["artifacts"]["console_logs"]:
                    log_str = str(log).lower()
                    
                    graphics_error_keywords = [
                        "webgl", "shader", "texture", "rendering", "graphics",
                        "gpu", "canvas", "context lost", "memory"
                    ]
                    
                    error_keywords = ["error", "failed", "exception", "warning"]
                    
                    if (any(gfx in log_str for gfx in graphics_error_keywords) and
                        any(err in log_str for err in error_keywords)):
                        
                        graphics_errors.append({
                            "error_type": "graphics_console_error",
                            "severity": "medium",
                            "message": str(log)[:200],
                            "test_id": result.get("test_id", "unknown")
                        })
        
        return {
            "graphics_errors_found": len(graphics_errors),
            "graphics_errors": graphics_errors,
            "error_severity": self._assess_graphics_error_severity(graphics_errors)
        }
    
    def _assess_graphics_error_severity(self, errors: List[Dict[str, Any]]) -> str:
        """Assess overall graphics error severity"""
        
        if not errors:
            return "none"
        
        high_severity_count = len([e for e in errors if e.get("severity") == "high"])
        medium_severity_count = len([e for e in errors if e.get("severity") == "medium"])
        
        if high_severity_count > 0:
            return "high"
        elif medium_severity_count > 3:
            return "medium"
        elif len(errors) > 5:
            return "medium"
        else:
            return "low"
    
    async def _analyze_performance_impact(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze graphics performance impact"""
        
        performance_data = {
            "gpu_utilization": [],
            "memory_usage": [],
            "render_times": []
        }
        
        for result in results:
            if "result_details" in result:
                details = result["result_details"]
                
                # Extract performance metrics
                if "memory_used" in details:
                    performance_data["memory_usage"].append(details["memory_used"] / 1024 / 1024)
                
                if "frame_time" in details:
                    performance_data["render_times"].append(details["frame_time"])
        
        analysis = {}
        
        if performance_data["memory_usage"]:
            avg_memory = np.mean(performance_data["memory_usage"])
            analysis["memory_impact"] = {
                "average_memory_mb": avg_memory,
                "memory_efficiency": "good" if avg_memory < 256 else "poor",
                "peak_memory_mb": np.max(performance_data["memory_usage"])
            }
        
        if performance_data["render_times"]:
            avg_render_time = np.mean(performance_data["render_times"])
            analysis["render_performance"] = {
                "average_render_time_ms": avg_render_time,
                "performance_rating": "good" if avg_render_time < 16.67 else "poor",
                "frame_budget_utilization": avg_render_time / 16.67 * 100
            }
        
        return analysis
    
    async def _calculate_graphics_score(self, visual_analysis: Dict[str, Any],
                                      rendering_analysis: Dict[str, Any],
                                      quality_analysis: Dict[str, Any]) -> float:
        """Calculate overall graphics score"""
        
        score_components = []
        
        # Visual quality component
        if "average_visual_quality" in visual_analysis:
            visual_score = visual_analysis["average_visual_quality"]
            score_components.append(visual_score * 0.3)
        
        # Rendering performance component
        if "performance_rating" in rendering_analysis:
            perf_rating = rendering_analysis["performance_rating"]
            perf_scores = {"excellent": 100, "good": 80, "acceptable": 60, "poor": 30}
            perf_score = perf_scores.get(perf_rating, 50)
            score_components.append(perf_score * 0.4)
        
        # Visual quality assessment component
        if "overall_quality_score" in quality_analysis:
            quality_score = quality_analysis["overall_quality_score"]
            score_components.append(quality_score * 0.3)
        
        return sum(score_components) / len(score_components) if score_components else 50.0
    
    def _determine_graphics_rating(self, score: float) -> str:
        """Determine overall graphics rating"""
        
        if score >= 85:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 55:
            return "acceptable"
        elif score >= 40:
            return "poor"
        else:
            return "very_poor"
    
    async def _generate_graphics_recommendations(self, visual_analysis: Dict[str, Any],
                                               rendering_analysis: Dict[str, Any],
                                               quality_analysis: Dict[str, Any]) -> List[str]:
        """Generate graphics optimization recommendations"""
        
        recommendations = []
        
        # Visual quality recommendations
        if quality_analysis.get("overall_quality_score", 100) < 70:
            recommendations.append("Improve visual quality through better asset optimization")
            recommendations.append("Review texture compression and image quality settings")
        
        # Performance recommendations
        if rendering_analysis.get("performance_rating") in ["poor", "acceptable"]:
            recommendations.append("Optimize rendering pipeline for better frame rates")
            recommendations.append("Consider reducing visual complexity or implementing LOD")
        
        # Frame rate recommendations
        frame_analysis = rendering_analysis.get("frame_rate_analysis", {})
        if frame_analysis.get("average_fps", 60) < 45:
            recommendations.append("Target 60 FPS for smooth gameplay experience")
            recommendations.append("Profile GPU performance and identify bottlenecks")
        
        # Visual artifacts recommendations
        if visual_analysis.get("visual_issues_found", 0) > 0:
            recommendations.append("Address visual artifacts and rendering issues")
            recommendations.append("Review shader code and rendering algorithms")
        
        # General recommendations
        recommendations.extend([
            "Implement graphics quality options for different hardware",
            "Regular visual regression testing",
            "Monitor graphics performance across different devices",
            "Use appropriate texture formats and compression"
        ])
        
        return recommendations[:8]  # Return top 8 recommendations
    
    async def _load_reference_images(self) -> None:
        """Load reference images for comparison"""
        # In production, this would load reference images from files
        pass
    
    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get graphics agent health metrics"""
        return {
            "agent_id": self.agent_id,
            "status": "healthy",
            "cpu_usage": 0.22,
            "memory_usage": 0.35,
            "images_analyzed": 25,  # Would track actual metrics
            "reference_images_loaded": len(self.reference_images)
        }
