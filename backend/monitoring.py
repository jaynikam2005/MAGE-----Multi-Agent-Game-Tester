import time
import psutil
import logging
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from functools import wraps

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