"""
Minimal Database Manager
"""

import logging
from src.core.config import Settings


class DatabaseManager:
    """Minimal database manager"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self) -> None:
        """Initialize database connection"""
        self.logger.info("Database manager initialized (minimal mode)")
    
    async def close(self) -> None:
        """Close database connections"""
        self.logger.info("Database connections closed")
