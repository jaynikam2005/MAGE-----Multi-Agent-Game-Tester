"""
Minimal API Server
"""

import logging
from src.core.config import Settings


class APIServer:
    """Minimal API server"""
    
    def __init__(self, settings: Settings, db_manager=None, security_manager=None):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
    
    async def start(self):
        """Start the API server"""
        self.logger.info(f"API server started (minimal mode) on port {self.settings.api_port}")
    
    async def stop(self):
        """Stop the API server"""
        self.logger.info("API server stopped")
