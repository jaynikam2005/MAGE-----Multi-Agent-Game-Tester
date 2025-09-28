"""
AI Provider Manager with automatic failover support
"""
from enum import Enum
from typing import Optional, List, Dict, Any
import asyncio
from datetime import datetime, timedelta
import logging
from pydantic import BaseModel

from .config import settings

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    PERPLEXITY = "perplexity"

class ProviderStatus(BaseModel):
    provider: AIProvider
    available: bool
    rate_limit_remaining: float
    token_usage: float
    last_error: Optional[str] = None
    last_check: datetime
    consecutive_failures: int = 0

class AIProviderManager:
    def __init__(self):
        self._providers: Dict[AIProvider, ProviderStatus] = {}
        self._current_provider = AIProvider(settings.PRIMARY_AI_PROVIDER)
        self._initialize_providers()
        self._lock = asyncio.Lock()

    def _initialize_providers(self):
        """Initialize provider status tracking"""
        now = datetime.now()
        for provider in AIProvider:
            self._providers[provider] = ProviderStatus(
                provider=provider,
                available=True,
                rate_limit_remaining=100,
                token_usage=0,
                last_check=now,
                consecutive_failures=0
            )

    async def get_current_provider(self) -> AIProvider:
        """Get the current active provider"""
        async with self._lock:
            if not self._should_switch_provider():
                return self._current_provider
            
            new_provider = await self._find_next_available_provider()
            if new_provider:
                logger.info(f"Switching from {self._current_provider} to {new_provider}")
                self._current_provider = new_provider
            
            return self._current_provider

    def _should_switch_provider(self) -> bool:
        """Determine if we should switch providers based on status"""
        if not settings.ENABLE_AUTO_FAILOVER:
            return False

        current = self._providers[self._current_provider]
        
        # Check rate limits
        if current.rate_limit_remaining < settings.RATE_LIMIT_THRESHOLD:
            return True
            
        # Check token usage
        if current.token_usage > settings.TOKEN_USAGE_THRESHOLD:
            return True
            
        # Check consecutive failures
        if current.consecutive_failures >= 3:
            return True
            
        return False

    async def _find_next_available_provider(self) -> Optional[AIProvider]:
        """Find the next available provider based on fallback order"""
        fallback_order = settings.FALLBACK_ORDER.split(",")
        
        for provider_name in fallback_order:
            provider = AIProvider(provider_name)
            if provider == self._current_provider:
                continue
                
            status = self._providers[provider]
            if (status.available and 
                status.rate_limit_remaining > settings.RATE_LIMIT_THRESHOLD and
                status.token_usage < settings.TOKEN_USAGE_THRESHOLD and
                status.consecutive_failures < 3):
                return provider
                
        return None

    async def update_provider_status(
        self,
        provider: AIProvider,
        available: bool,
        rate_limit_remaining: float,
        token_usage: float,
        error: Optional[str] = None
    ):
        """Update the status of a provider"""
        async with self._lock:
            status = self._providers[provider]
            status.available = available
            status.rate_limit_remaining = rate_limit_remaining
            status.token_usage = token_usage
            status.last_check = datetime.now()
            
            if error:
                status.last_error = error
                status.consecutive_failures += 1
            else:
                status.consecutive_failures = 0

    async def get_provider_status(self) -> Dict[AIProvider, ProviderStatus]:
        """Get status of all providers"""
        return self._providers.copy()

# Global instance
provider_manager = AIProviderManager()