import time
import psutil
import logging
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from functools import wraps
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
import time
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import psutil
import logging

REQUEST_COUNT = Counter(
    "http_request_count",
    "Count of HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

TEST_EXECUTION_TIME = Histogram(
    "test_execution_time_seconds",
    "Test case execution time",
    ["test_type"]
)

VALIDATION_TIME = Histogram(
    "validation_time_seconds",
    "Test validation processing time",
    ["validation_type"]
)

class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response

def init_monitoring(app: FastAPI):
    app.add_middleware(MonitoringMiddleware)
    
    @app.get("/metrics")
    async def metrics():
        return Response(
            generate_latest(),
            media_type="text/plain"
        )
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent
        }

def log_test_execution(test_type: str, duration: float):
    TEST_EXECUTION_TIME.labels(test_type=test_type).observe(duration)
    logging.info(f"Test execution completed - Type: {test_type}, Duration: {duration}s")

def log_validation_time(validation_type: str, duration: float):
    VALIDATION_TIME.labels(validation_type=validation_type).observe(duration)
    logging.info(f"Validation completed - Type: {validation_type}, Duration: {duration}s")


# Metrics
test_execution_counter = Counter('test_executions_total', 'Total test executions')
test_duration_histogram = Histogram('test_duration_seconds', 'Test execution duration')
active_sessions_gauge = Gauge('active_sessions', 'Number of active test sessions')
system_cpu_gauge = Gauge('system_cpu_percent', 'System CPU usage')
system_memory_gauge = Gauge('system_memory_percent', 'System memory usage')

class PerformanceMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def track_execution(self, func):
        """Decorator to track function execution"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            test_execution_counter.inc()
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                test_duration_histogram.observe(duration)
                
                self.logger.info(f"{func.__name__} executed in {duration:.2f}s")
                return result
                
            except Exception as e:
                self.logger.error(f"Error in {func.__name__}: {e}")
                raise
                
        return wrapper
    
    @staticmethod
    def update_system_metrics():
        """Update system resource metrics"""
        system_cpu_gauge.set(psutil.cpu_percent())
        system_memory_gauge.set(psutil.virtual_memory().percent)
    
    @staticmethod
    def get_metrics():
        """Get Prometheus metrics"""
        return generate_latest()