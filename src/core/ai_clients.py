"""
AI Client implementations for different providers
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import openai
import anthropic
from google.cloud import aiplatform
from google.oauth2 import service_account
import httpx
import asyncio
import logging
from datetime import datetime

from .ai_providers import AIProvider, provider_manager
from .config import settings

logger = logging.getLogger(__name__)

class AIClient(ABC):
    """Abstract base class for AI clients"""
    
    @abstractmethod
    async def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion from the AI provider"""
        pass
    
    @abstractmethod
    async def get_rate_limit_info(self) -> Dict[str, float]:
        """Get rate limit information"""
        pass

class OpenAIClient(AIClient):
    def __init__(self):
        self.client = openai.AsyncClient(
            api_key=settings.OPENAI_API_KEY,
            organization=settings.OPENAI_ORG_ID
        )
        
    async def generate_completion(self, prompt: str, **kwargs) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=kwargs.get("model", "gpt-4"),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000)
            )
            
            await self._update_status()
            return response.choices[0].message.content
            
        except Exception as e:
            await provider_manager.update_provider_status(
                AIProvider.OPENAI,
                available=False,
                rate_limit_remaining=0,
                token_usage=100,
                error=str(e)
            )
            raise
    
    async def get_rate_limit_info(self) -> Dict[str, float]:
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.openai.com/v1/usage",
                headers=headers
            )
            data = response.json()
            return {
                "rate_limit_remaining": 100 - data["total_usage"],
                "token_usage": data["total_usage"]
            }
            
    async def _update_status(self):
        rate_info = await self.get_rate_limit_info()
        await provider_manager.update_provider_status(
            AIProvider.OPENAI,
            available=True,
            **rate_info
        )



class GoogleAIClient(AIClient):
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_info({
            "type": "service_account",
            "project_id": settings.GOOGLE_AI_PROJECT_ID,
            "private_key": settings.GOOGLE_AI_PRIVATE_KEY,
            "client_email": settings.GOOGLE_AI_CLIENT_EMAIL
        })
        
        self.client = aiplatform.gapic.PredictionServiceAsyncClient(
            credentials=credentials
        )
        
    async def generate_completion(self, prompt: str, **kwargs) -> str:
        try:
            instance = {
                "content": prompt
            }
            
            parameters = {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 1000),
                "topP": kwargs.get("top_p", 0.8),
                "topK": kwargs.get("top_k", 40)
            }
            
            response = await self.client.predict(
                endpoint=settings.GOOGLE_AI_ENDPOINT,
                instances=[instance],
                parameters=parameters
            )
            
            await self._update_status()
            return response.predictions[0]["content"]
            
        except Exception as e:
            await provider_manager.update_provider_status(
                AIProvider.GOOGLE,
                available=False,
                rate_limit_remaining=0,
                token_usage=100,
                error=str(e)
            )
            raise
    
    async def get_rate_limit_info(self) -> Dict[str, float]:
        # Google AI doesn't provide direct rate limit info
        return {
            "rate_limit_remaining": 90,  # Approximate
            "token_usage": 10  # Approximate
        }
        
    async def _update_status(self):
        rate_info = await self.get_rate_limit_info()
        await provider_manager.update_provider_status(
            AIProvider.GOOGLE,
            available=True,
            **rate_info
        )

class PerplexityClient(AIClient):
    def __init__(self):
        self.api_key = settings.PERPLEXITY_API_KEY
        self.client = httpx.AsyncClient(
            base_url="https://api.perplexity.ai",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
    async def generate_completion(self, prompt: str, **kwargs) -> str:
        try:
            response = await self.client.post(
                "/chat/completions",
                json={
                    "model": kwargs.get("model", "mixtral-8x7b"),
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": kwargs.get("max_tokens", 1000)
                }
            )
            
            await self._update_status()
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            await provider_manager.update_provider_status(
                AIProvider.PERPLEXITY,
                available=False,
                rate_limit_remaining=0,
                token_usage=100,
                error=str(e)
            )
            raise
    
    async def get_rate_limit_info(self) -> Dict[str, float]:
        response = await self.client.get("/v1/usage")
        data = response.json()
        return {
            "rate_limit_remaining": 100 - data["usage_percentage"],
            "token_usage": data["usage_percentage"]
        }
        
    async def _update_status(self):
        rate_info = await self.get_rate_limit_info()
        await provider_manager.update_provider_status(
            AIProvider.PERPLEXITY,
            available=True,
            **rate_info
        )

class AIClientFactory:
    """Factory for creating AI clients"""
    
    @staticmethod
    async def get_client() -> AIClient:
        """Get the appropriate AI client based on current provider"""
        provider = await provider_manager.get_current_provider()
        
        if provider == AIProvider.OPENAI:
            return OpenAIClient()
        elif provider == AIProvider.GOOGLE:
            return GoogleAIClient()
        elif provider == AIProvider.PERPLEXITY:
            return PerplexityClient()
        else:
            raise ValueError(f"Unknown provider: {provider}")

# Usage Example:
async def generate_with_failover(prompt: str, **kwargs) -> str:
    """Generate completion with automatic failover support"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            client = await AIClientFactory.get_client()
            return await client.generate_completion(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise