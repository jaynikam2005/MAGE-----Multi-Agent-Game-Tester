"""
Simplified Logging System
"""

import logging
import sys
from pathlib import Path


def setup_logging(level: str = "INFO", log_file: str = None) -> None:
    """Setup simplified logging configuration"""
    
    # Create logs directory if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure logging with file and console
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(log_path)
            ]
        )
    else:
        # Console only
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized successfully")
