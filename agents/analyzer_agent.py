from typing import List, Dict, Any
import asyncio
import numpy as np
from datetime import datetime
from backend.core.architecture import ExecutionResult, ValidationReport
import cv2
from PIL import Image
import io
import base64

class AnalyzerAgent:
    def __init__(self):
        self.confidence_threshold = 0.85
        self.similarity_threshold = 0.90
        self.reproducibility_threshold = 0.95

    async def validate_test_result(self, result: ExecutionResult) -> ValidationReport:
        artifact_validations = await self._validate_artifacts(result.artifacts)
        cross_validations = await self._perform_cross_validation(result)
        reproducibility_score = await self._calculate_reproducibility(result)
        
        anomalies = await self._detect_anomalies(result)
        
        overall_confidence = np.mean([
            artifact_validations.get("confidence", 0),
            cross_validations.get("confidence", 0),
            reproducibility_score
        ])
        
        return ValidationReport(
            test_case_id=result.test_case_id,
            is_valid=overall_confidence >= self.confidence_threshold,
            confidence_score=overall_confidence,
            cross_validation_results=cross_validations,
            reproducibility_score=reproducibility_score,
            anomalies_detected=anomalies
        )

    async def _validate_artifacts(self, artifacts: Dict[str, str]) -> Dict[str, float]:
        validations = {}
        
        for key, artifact in artifacts.items():
            if key.startswith("screenshot_"):
                validations.update(await self._analyze_screenshot(artifact))
            elif key.startswith("dom_"):
                validations.update(await self._analyze_dom(artifact))
            elif key.startswith("console_"):
                validations.update(await self._analyze_console_logs(artifact))
                
        return validations

    async def _analyze_screenshot(self, screenshot_base64: str) -> Dict[str, float]:
        try:
            image_data = base64.b64decode(screenshot_base64)
            image = Image.open(io.BytesIO(image_data))
            np_image = np.array(image)
            
            blur_score = await self._calculate_blur_score(np_image)
            noise_score = await self._calculate_noise_score(np_image)
            content_score = await self._analyze_image_content(np_image)
            
            return {
                "image_quality": np.mean([blur_score, noise_score]),
                "content_validity": content_score,
                "confidence": np.mean([blur_score, noise_score, content_score])
            }
        except Exception:
            return {"confidence": 0.0}

    async def _perform_cross_validation(self, result: ExecutionResult) -> Dict[str, Any]:
        metrics_validation = await self._validate_metrics(result.metrics)
        temporal_validation = await self._validate_temporal_consistency(result)
        
        return {
            "metrics_validation": metrics_validation,
            "temporal_validation": temporal_validation,
            "confidence": np.mean([
                metrics_validation.get("confidence", 0),
                temporal_validation.get("confidence", 0)
            ])
        }

    async def _calculate_reproducibility(self, result: ExecutionResult) -> float:
        if not result.metrics:
            return 0.0
            
        timing_consistency = 1.0 - (
            np.std([
                result.metrics.get("loadTime", 0),
                result.metrics.get("domComplete", 0)
            ]) / np.mean([
                result.metrics.get("loadTime", 1),
                result.metrics.get("domComplete", 1)
            ])
        )
        
        return min(1.0, max(0.0, timing_consistency))

    async def _detect_anomalies(self, result: ExecutionResult) -> List[Dict[str, Any]]:
        anomalies = []
        
        if result.error_message:
            anomalies.append({
                "type": "error",
                "message": result.error_message,
                "severity": "high"
            })
            
        if result.metrics:
            if result.metrics.get("loadTime", 0) > 5000:
                anomalies.append({
                    "type": "performance",
                    "message": "Page load time exceeded threshold",
                    "severity": "medium"
                })
                
        return anomalies

    async def generate_validation_summary(self, results: List[ExecutionResult]) -> Dict[str, Any]:
        validations = await asyncio.gather(*[
            self.validate_test_result(result) for result in results
        ])
        
        return {
            "overall_confidence": np.mean([v.confidence_score for v in validations]),
            "reproducibility_rate": np.mean([v.reproducibility_score for v in validations]),
            "anomaly_count": sum(len(v.anomalies_detected) for v in validations),
            "validation_timestamp": datetime.now().isoformat()
        }

    async def _calculate_blur_score(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return min(1.0, max(0.0, cv2.Laplacian(gray, cv2.CV_64F).var() / 500))

    async def _calculate_noise_score(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        noise_sigma = np.std(gray)
        return min(1.0, max(0.0, 1.0 - (noise_sigma / 128)))

    async def _analyze_image_content(self, image: np.ndarray) -> float:
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            saturation = hsv[:, :, 1]
            value = hsv[:, :, 2]
            
            content_score = np.mean([
                np.mean(saturation) / 255,
                np.mean(value) / 255
            ])
            
            return min(1.0, max(0.0, content_score))
        except Exception:
            return 0.0

    async def _validate_metrics(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        if not metrics:
            return {"confidence": 0.0}
            
        load_time_score = 1.0 - min(1.0, metrics.get("loadTime", 0) / 5000)
        dom_complete_score = 1.0 - min(1.0, metrics.get("domComplete", 0) / 3000)
        first_paint_score = 1.0 - min(1.0, metrics.get("firstPaint", 0) / 1000)
        
        return {
            "load_time_score": load_time_score,
            "dom_complete_score": dom_complete_score,
            "first_paint_score": first_paint_score,
            "confidence": np.mean([
                load_time_score,
                dom_complete_score,
                first_paint_score
            ])
        }

    async def _validate_temporal_consistency(self, result: ExecutionResult) -> Dict[str, Any]:
        if not result.metrics:
            return {"confidence": 0.0}
            
        temporal_order_valid = (
            result.metrics.get("firstPaint", 0) <=
            result.metrics.get("domComplete", 0) <=
            result.metrics.get("loadTime", 0)
        )
        
        return {
            "temporal_order_valid": temporal_order_valid,
            "confidence": 1.0 if temporal_order_valid else 0.0
        }