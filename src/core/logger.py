"""
Advanced Logging System with Security and Performance
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
import json
from datetime import datetime
import structlog
from structlog import get_logger


class SecurityLogFilter(logging.Filter):
    """Filter to prevent sensitive data from being logged"""
    
    SENSITIVE_PATTERNS = [
        "password", "token", "key", "secret", "credential",
        "authorization", "auth", "session", "cookie"
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out sensitive information"""
        message = record.getMessage().lower()
        
        # Check if message contains sensitive patterns
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern in message:
                # Replace sensitive data with asterisks
                record.msg = self._sanitize_message(str(record.msg))
                if hasattr(record, 'args'):
                    record.args = self._sanitize_args(record.args)
                break
        
        return True
    
    def _sanitize_message(self, message: str) -> str:
        """Sanitize sensitive data in message"""
        import re
        
        # Pattern to match key=value or key: value patterns
        pattern = r'([a-zA-Z_]*(?:password|token|key|secret|credential|auth)[a-zA-Z_]*)\s*[:=]\s*[^\s,}]+'
        return re.sub(pattern, r'\1=***REDACTED***', message, flags=re.IGNORECASE)
    
    def _sanitize_args(self, args: tuple) -> tuple:
        """Sanitize sensitive data in log arguments"""
        sanitized_args = []
        for arg in args:
            if isinstance(arg, str):
                sanitized_args.append(self._sanitize_message(arg))
            elif isinstance(arg, dict):
                sanitized_dict = {}
                for key, value in arg.items():
                    if any(pattern in key.lower() for pattern in self.SENSITIVE_PATTERNS):
                        sanitized_dict[key] = "***REDACTED***"
                    else:
                        sanitized_dict[key] = value
                sanitized_args.append(sanitized_dict)
            else:
                sanitized_args.append(arg)
        return tuple(sanitized_args)


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in log_data and not key.startswith('_'):
                log_data[key] = value
        
        return json.dumps(log_data, default=str)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = True,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> None:
    """Setup advanced logging configuration"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if json_format else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatters
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SecurityLogFilter())
    root_logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        file_handler.addFilter(SecurityLogFilter())
        root_logger.addHandler(file_handler)
    
    # Set levels for third-party loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('playwright').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    
    logger = get_logger(__name__)
    logger.info("Logging system initialized successfully")


def get_security_logger() -> structlog.BoundLogger:
    """Get security-focused logger"""
    return get_logger("security")


def get_performance_logger() -> structlog.BoundLogger:
    """Get performance-focused logger"""
    return get_logger("performance")


def get_audit_logger() -> structlog.BoundLogger:
    """Get audit logger for compliance"""
    return get_logger("audit")
