"""
Advanced Configuration Management
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from functools import lru_cache
from enum import Enum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestingMode(str, Enum):
    """Advanced testing modes"""
    PERFORMANCE = "performance"
    STRESS = "stress"
    LOAD = "load"
    AI_BEHAVIOR = "ai_behavior"
    GRAPHICS = "graphics"
    NETWORK = "network"
    SECURITY = "security"


class GameGenre(str, Enum):
    """Supported game genres"""
    ACTION = "action"
    RPG = "rpg"
    STRATEGY = "strategy"
    PUZZLE = "puzzle"
    SIMULATION = "simulation"


class AdvancedSettings(BaseSettings):
    """Advanced gaming industry configuration"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application Metadata
    app_name: str = "MAGE - Multi-Agent Game Tester Enterprise"
    version: str = "2.0.0"
    build_number: str = "20250928"
    codename: str = "Phoenix"
    debug: bool = False
    environment: str = Field(default="enterprise", description="deployment environment")
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 8
    api_reload: bool = False
    
    # Database Configuration
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "mage_enterprise"
    db_user: str = "mage_admin"
    db_password: str = Field(default="", description="Database password")
    
    # Security Configuration
    secret_key: str = Field(default="", description="JWT secret")
    encryption_key: str = Field(default="", description="Fernet encryption key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Configuration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_model: str = "gpt-4-turbo-preview"
    openai_max_tokens: int = 4000
    openai_temperature: float = 0.7
    
    # File Storage
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path("data"))
    log_dir: Path = Field(default_factory=lambda: Path("logs"))
    reports_dir: Path = Field(default_factory=lambda: Path("reports"))
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "game_tester.log"
    
    # Agent Configuration
    max_agents_per_session: int = 10
    planner_agent_config: Dict[str, Any] = Field(default_factory=lambda: {})
    executor_agent_config: Dict[str, Any] = Field(default_factory=lambda: {
        "browser_headless": False,
        "screenshot_dir": "data/screenshots",
        "artifact_dir": "data/artifacts",
        "timeout": 30,
        "retry_count": 3
    })
    analyzer_agent_config: Dict[str, Any] = Field(default_factory=lambda: {})
    
    # Browser Configuration
    browser_headless: bool = False
    browser_type: str = "chromium"
    browser_viewport_width: int = 1920
    browser_viewport_height: int = 1080
    
    # Game Testing Configuration
    supported_genres: List[GameGenre] = [GameGenre.PUZZLE, GameGenre.ACTION]
    default_testing_modes: List[TestingMode] = [TestingMode.PERFORMANCE, TestingMode.SECURITY]
    
    # Target Game Configuration
    target_game_url: str = "https://play.ezygamers.com/"
    game_type: str = "number_puzzle"
    
    @field_validator("secret_key", "encryption_key")
    @classmethod
    def generate_keys_if_empty(cls, v: str) -> str:
        """Generate secure keys if not provided"""
        if not v:
            import secrets
            return secrets.token_urlsafe(32)
        return v
    
    @field_validator("data_dir", "log_dir", "reports_dir")
    @classmethod
    def create_directories(cls, v: Path) -> Path:
        """Ensure directories exist"""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @property
    def database_url(self) -> str:
        """Construct database URL"""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


# Use the simpler Settings class by default for compatibility
Settings = AdvancedSettings

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
