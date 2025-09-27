"""
Minimal Security Manager
"""

import logging


class SecurityManager:
    """Minimal security manager"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self) -> None:
        """Initialize security components"""
        self.logger.info("Security manager initialized (minimal mode)")
    
    def cleanup(self) -> None:
        """Cleanup security resources"""
        self.logger.info("Security manager cleanup completed")
